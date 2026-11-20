#!/usr/bin/env python3
"""Inject the explicitly admitted Corpus Iuris canon at Codex session start."""

from __future__ import annotations

import json
import os
import sys
import tomllib
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from string import ascii_lowercase, ascii_uppercase
from typing import TextIO, TypedDict, cast


CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path(__file__).resolve().parents[1]))
CORPUS_DIR = Path(os.environ.get("CORPUS_IURIS_ROOT", CODEX_HOME / "corpus"))
CANON_PATH = CODEX_HOME / "canon.md"
MAX_CONTEXT_BYTES = 64_000
MAX_IMPORT_DEPTH = 16


class CanonError(Exception):
    """The admitted canon cannot be loaded completely and safely."""


class CanonBudgetError(CanonError):
    """The expanded doctrine exceeds the context budget."""


class SavedTrust(Enum):
    TRUSTED = "trusted"
    UNTRUSTED = "untrusted"
    UNDETERMINED = "undetermined"


class ProjectOmission(Enum):
    """Fixed reasons keep the notice and separator within 512 UTF-8 bytes."""

    DISCOVERY_UNCERTAIN = "the hook could not determine whether project canon exists"
    TRUST_DENIED = "the project is saved as untrusted"
    TRUST_UNAVAILABLE = "saved trust for this project could not be established"
    LOAD_FAILED = "canon could not be loaded"
    OVER_BUDGET = "expanded doctrine exceeded the context limit"


@dataclass(frozen=True, slots=True, kw_only=True)
class SessionStart:
    cwd: str | None


@dataclass(frozen=True, slots=True, kw_only=True)
class AdmittedProject:
    root: Path


class SessionStartContext(TypedDict):
    hookEventName: str
    additionalContext: str


class HookOutput(TypedDict, total=False):
    systemMessage: str
    hookSpecificOutput: SessionStartContext


@dataclass(frozen=True)
class MarkdownFence:
    marker: str
    length: int
    trailing: str


def read_hook_payload(stdin: TextIO) -> SessionStart:
    if stdin.isatty():
        return SessionStart(cwd=None)

    try:
        payload: object = json.load(stdin)
    except (OSError, ValueError, RecursionError):
        return SessionStart(cwd=None)

    if not isinstance(payload, dict):
        return SessionStart(cwd=None)

    cwd = cast(dict[str, object], payload).get("cwd")
    return SessionStart(cwd=cwd if isinstance(cwd, str) else None)


def resolve_session_cwd(payload: SessionStart) -> Path | None:
    if payload.cwd is None:
        return None
    cwd = Path(payload.cwd)
    if not cwd.is_absolute():
        return None

    try:
        resolved = cwd.resolve(strict=True)
        return resolved if resolved.is_dir() else None
    except (OSError, RuntimeError, ValueError):
        return None


def resolve_project_root(session_cwd: Path) -> Path:
    for candidate in (session_cwd, *session_cwd.parents):
        try:
            (candidate / ".git").stat()
        except FileNotFoundError:
            continue
        return candidate
    return session_cwd


def project_canon_path(session_cwd: Path | None) -> Path | ProjectOmission | None:
    if session_cwd is None:
        return ProjectOmission.DISCOVERY_UNCERTAIN

    try:
        candidate = resolve_project_root(session_cwd) / ".codex" / "canon.md"
        candidate.lstat()
    except FileNotFoundError:
        return None
    except OSError:
        return ProjectOmission.DISCOVERY_UNCERTAIN
    return candidate


def read_saved_project_trust(codex_home: Path, project_root: Path) -> SavedTrust:
    try:
        with (codex_home / "config.toml").open("rb") as config_file:
            config: dict[str, object] = tomllib.load(config_file)
    except (OSError, ValueError, RecursionError):
        return SavedTrust.UNDETERMINED

    projects = config.get("projects")
    if not isinstance(projects, dict):
        return SavedTrust.UNDETERMINED

    project_key = str(project_root)
    if os.name == "nt":
        project_key = project_key.translate(str.maketrans(ascii_uppercase, ascii_lowercase))
    project = cast(dict[str, object], projects).get(project_key)
    if not isinstance(project, dict):
        return SavedTrust.UNDETERMINED

    trust_level = cast(dict[str, object], project).get("trust_level")
    if trust_level == SavedTrust.TRUSTED.value:
        return SavedTrust.TRUSTED
    if trust_level == SavedTrust.UNTRUSTED.value:
        return SavedTrust.UNTRUSTED
    return SavedTrust.UNDETERMINED


def parse_import_target(line: str) -> str | None:
    if line.startswith(("    ", "\t")):
        return None

    stripped = line.strip()
    parts = stripped.split()
    if not parts or parts[0] != "@import":
        return None
    if len(parts) != 2:
        raise CanonError(f"malformed import directive `{stripped}`")

    target = parts[1]
    if target.startswith(("'", '"')) or target.endswith(("'", '"')):
        raise CanonError(f"malformed import target `{target}`")
    if Path(target).is_absolute():
        raise CanonError(f"absolute import target `{target}`")
    return target


def markdown_fence_marker(line: str) -> MarkdownFence | None:
    content = line.rstrip("\r\n")
    leading_spaces = len(content) - len(content.lstrip(" "))
    if leading_spaces > 3:
        return None

    stripped = content[leading_spaces:]
    if not stripped.startswith(("`", "~")):
        return None

    marker = stripped[0]
    marker_length = len(stripped) - len(stripped.lstrip(marker))
    if marker_length < 3:
        return None
    return MarkdownFence(marker, marker_length, stripped[marker_length:])


def closes_markdown_fence(candidate: MarkdownFence | None, active: MarkdownFence) -> bool:
    return (
        candidate is not None
        and candidate.marker == active.marker
        and candidate.length >= active.length
        and not candidate.trailing.strip()
    )


def display_path(path: Path) -> str:
    return path.name or str(path)


def expand_imports(
    text: str,
    path: Path,
    active_stack: tuple[Path, ...],
    depth: int,
    corpus_root: Path,
) -> str:
    expanded_parts: list[str] = []
    active_fence: MarkdownFence | None = None

    for line in text.splitlines(keepends=True):
        fence = markdown_fence_marker(line)
        if active_fence is not None:
            expanded_parts.append(line)
            if closes_markdown_fence(fence, active_fence):
                active_fence = None
            continue

        if fence is not None:
            active_fence = fence
            expanded_parts.append(line)
            continue

        target = parse_import_target(line)
        if target is None:
            expanded_parts.append(line)
            continue

        if depth >= MAX_IMPORT_DEPTH:
            raise CanonError(f"maximum import depth exceeded at `{target}`")

        try:
            resolved_target = (path.parent / target).resolve(strict=True)
        except FileNotFoundError as error:
            raise CanonError(f"missing import target `{target}`") from error
        except (OSError, RuntimeError, ValueError) as error:
            raise CanonError(f"invalid import target `{target}`") from error

        if not resolved_target.is_relative_to(corpus_root):
            raise CanonError(f"import target escapes the corpus root: `{target}`")
        if resolved_target in active_stack:
            cycle_start = active_stack.index(resolved_target)
            cycle_paths = (*active_stack[cycle_start:], resolved_target)
            cycle = " -> ".join(display_path(item) for item in cycle_paths)
            raise CanonError(f"import cycle: {cycle}")
        try:
            if not resolved_target.is_file():
                raise CanonError(f"import target is not a file: `{target}`")
            imported_text = resolved_target.read_text(encoding="utf-8")
        except UnicodeDecodeError as error:
            raise CanonError(f"import target is not UTF-8: `{target}`") from error
        except OSError as error:
            raise CanonError(f"unreadable import target `{target}`") from error

        expanded_parts.append(
            expand_imports(
                imported_text,
                resolved_target,
                (*active_stack, resolved_target),
                depth + 1,
                corpus_root,
            )
        )

    return "".join(expanded_parts)


def resolve_corpus_root(corpus_dir: Path) -> Path:
    try:
        corpus_root = corpus_dir.resolve(strict=True)
        if not corpus_root.is_dir():
            raise CanonError(f"corpus root is not a directory: `{corpus_root}`")
    except FileNotFoundError as error:
        raise CanonError(f"corpus directory not found at `{corpus_dir}`") from error
    except (OSError, RuntimeError, ValueError) as error:
        raise CanonError(f"cannot resolve corpus directory `{corpus_dir}`") from error

    return corpus_root


def load_canon(corpus_dir: Path, canon_path: Path, *, project: bool = False) -> str:
    if project and resolve_corpus_root(corpus_dir) != corpus_dir:
        raise CanonError("project corpus directory was redirected")

    try:
        resolved_canon = canon_path.resolve(strict=True)
    except FileNotFoundError as error:
        if project:
            raise CanonError("project canon entrypoint is missing") from error
        return ""
    except (OSError, RuntimeError, ValueError) as error:
        raise CanonError(f"cannot resolve canon entrypoint `{canon_path}`") from error

    if project and not resolved_canon.is_relative_to(corpus_dir):
        raise CanonError("project canon entrypoint escapes the corpus root")

    try:
        if not resolved_canon.is_file():
            raise CanonError(f"canon entrypoint is not a file: `{resolved_canon}`")
        canon_text = resolved_canon.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise CanonError("canon entrypoint is not UTF-8") from error
    except OSError as error:
        raise CanonError("canon entrypoint is unreadable") from error

    if not canon_text.strip():
        return ""

    corpus_root = corpus_dir if project else resolve_corpus_root(corpus_dir)
    expanded = expand_imports(
        canon_text,
        resolved_canon,
        (resolved_canon,),
        0,
        corpus_root,
    ).strip()
    if not expanded:
        return ""

    return f"Injected from `{resolved_canon}` by `{Path(__file__).resolve()}`.\n\n{expanded}"


def build_context(
    corpus_dir: Path,
    canon_path: Path,
    *,
    admitted_project: AdmittedProject | None = None,
) -> str:
    sections: list[str] = []
    global_context = load_canon(corpus_dir, canon_path)
    if global_context:
        sections.append(f"# Global Corpus Iuris Canon\n\n{global_context}")

    if admitted_project is not None:
        project_corpus = admitted_project.root / ".codex"
        project_context = load_canon(project_corpus, project_corpus / "canon.md", project=True)
        if project_context:
            sections.append(f"# Project Corpus Iuris Canon\n\n{project_context}")

    if not sections:
        return ""

    context = "\n\n".join(sections)
    context_bytes = len(context.encode("utf-8"))
    if context_bytes > MAX_CONTEXT_BYTES:
        raise CanonBudgetError(
            f"expanded canon is {context_bytes} bytes; limit is {MAX_CONTEXT_BYTES}"
        )
    return context


def main() -> None:
    payload = read_hook_payload(sys.stdin)
    session_cwd = resolve_session_cwd(payload)
    discovery = project_canon_path(session_cwd)
    omission = discovery if isinstance(discovery, ProjectOmission) else None
    admitted_project: AdmittedProject | None = None
    if isinstance(discovery, Path):
        project_root = discovery.parent.parent
        trust = read_saved_project_trust(CODEX_HOME, project_root)
        if trust is SavedTrust.TRUSTED:
            admitted_project = AdmittedProject(root=project_root)
        elif trust is SavedTrust.UNTRUSTED:
            omission = ProjectOmission.TRUST_DENIED
        else:
            omission = ProjectOmission.TRUST_UNAVAILABLE

    output: HookOutput = {}
    try:
        context = build_context(CORPUS_DIR, CANON_PATH, admitted_project=admitted_project)
    except CanonError as error:
        output["systemMessage"] = f"Corpus Iuris was not loaded: {error}."
        context = ""
        if admitted_project is not None:
            omission = (
                ProjectOmission.OVER_BUDGET if isinstance(error, CanonBudgetError) else ProjectOmission.LOAD_FAILED
            )

    if omission is not None:
        notice = (
            "# Project canon status\n\n"
            f"Project canon is inactive because {omission.value}. "
            "State this status and its reason in your first user-facing reply."
        )
        context = f"{notice}\n\n{context}" if context else notice

    if context:
        output["hookSpecificOutput"] = {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    if output:
        print(json.dumps(output))


if __name__ == "__main__":
    main()
