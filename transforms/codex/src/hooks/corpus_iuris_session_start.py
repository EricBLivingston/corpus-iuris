#!/usr/bin/env python3
"""Inject the explicitly admitted Corpus Iuris canon at Codex session start."""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO, cast


CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path(__file__).resolve().parents[1]))
CORPUS_DIR = Path(os.environ.get("CORPUS_IURIS_ROOT", CODEX_HOME / "corpus"))
CANON_PATH = CODEX_HOME / "canon.md"
MAX_CONTEXT_BYTES = 64_000
MAX_IMPORT_DEPTH = 16


class CanonError(Exception):
    """The admitted canon cannot be loaded completely and safely."""


@dataclass(frozen=True)
class MarkdownFence:
    marker: str
    length: int
    trailing: str


def read_hook_payload(stdin: TextIO = sys.stdin) -> dict[str, object]:
    if stdin.isatty():
        return {}

    try:
        raw_payload = stdin.read()
    except OSError:
        return {}

    if not raw_payload.strip():
        return {}

    try:
        payload = json.loads(raw_payload)
    except json.JSONDecodeError:
        return {}

    if not isinstance(payload, dict):
        return {}

    return cast(dict[str, object], payload)


def resolve_session_cwd(payload: dict[str, object]) -> Path:
    cwd = payload.get("cwd")
    if isinstance(cwd, str) and cwd.strip():
        candidate = Path(cwd).expanduser()
        try:
            if candidate.is_absolute() and candidate.is_dir():
                return candidate.resolve()
        except (OSError, RuntimeError, ValueError):
            pass

    return Path.cwd().resolve()


def resolve_project_root(session_cwd: Path) -> Path:
    current = session_cwd
    for candidate in (current, *current.parents):
        try:
            if (candidate / ".git").exists():
                return candidate
        except OSError:
            continue
    return session_cwd


def project_canon_path(session_cwd: Path) -> Path | None:
    candidate = resolve_project_root(session_cwd) / ".codex" / "canon.md"
    try:
        return candidate if candidate.is_file() else None
    except OSError:
        return None


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


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


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

        if not is_relative_to(resolved_target, corpus_root):
            raise CanonError(f"import target escapes the corpus root: `{target}`")
        if resolved_target in active_stack:
            cycle_start = active_stack.index(resolved_target)
            cycle_paths = (*active_stack[cycle_start:], resolved_target)
            cycle = " -> ".join(display_path(item) for item in cycle_paths)
            raise CanonError(f"import cycle: {cycle}")
        if not resolved_target.is_file():
            raise CanonError(f"import target is not a file: `{target}`")

        try:
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


def load_canon(corpus_dir: Path, canon_path: Path) -> str:
    try:
        resolved_canon = canon_path.resolve(strict=True)
    except FileNotFoundError:
        return ""
    except (OSError, RuntimeError, ValueError) as error:
        raise CanonError(f"cannot resolve canon entrypoint `{canon_path}`") from error

    if not resolved_canon.is_file():
        raise CanonError(f"canon entrypoint is not a file: `{resolved_canon}`")

    try:
        canon_text = resolved_canon.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise CanonError("canon entrypoint is not UTF-8") from error
    except OSError as error:
        raise CanonError("canon entrypoint is unreadable") from error

    if not canon_text.strip():
        return ""

    try:
        corpus_root = corpus_dir.resolve(strict=True)
    except FileNotFoundError as error:
        raise CanonError(f"corpus directory not found at `{corpus_dir}`") from error
    except (OSError, RuntimeError, ValueError) as error:
        raise CanonError(f"cannot resolve corpus directory `{corpus_dir}`") from error

    if not corpus_root.is_dir():
        raise CanonError(f"corpus root is not a directory: `{corpus_root}`")

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
    corpus_dir: Path = CORPUS_DIR,
    canon_path: Path = CANON_PATH,
    project_canon: Path | None = None,
) -> str:
    sections: list[str] = []
    global_context = load_canon(corpus_dir, canon_path)
    if global_context:
        sections.append(f"# Global Corpus Iuris Canon\n\n{global_context}")

    if project_canon is not None:
        project_context = load_canon(project_canon.parent, project_canon)
        if project_context:
            sections.append(f"# Project Corpus Iuris Canon\n\n{project_context}")

    if not sections:
        return ""

    context = "\n\n".join(sections)
    context_bytes = len(context.encode("utf-8"))
    if context_bytes > MAX_CONTEXT_BYTES:
        raise CanonError(
            f"expanded canon is {context_bytes} bytes; limit is {MAX_CONTEXT_BYTES}"
        )
    return context


def main() -> None:
    payload = read_hook_payload()
    session_cwd = resolve_session_cwd(payload)
    try:
        context = build_context(project_canon=project_canon_path(session_cwd))
    except CanonError as error:
        print(json.dumps({"systemMessage": f"Corpus Iuris was not loaded: {error}."}))
        return

    if not context:
        return

    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": context,
                }
            }
        )
    )


if __name__ == "__main__":
    main()
