from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import pytest


HOOK_PATH = Path(__file__).resolve().parents[1] / "corpus_iuris_session_start.py"


@pytest.fixture()
def hook_module():
    module_name = "corpus_iuris_session_start_under_test"
    spec = importlib.util.spec_from_file_location(module_name, HOOK_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
        yield module
    finally:
        sys.modules.pop(module_name, None)


def write_text(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def build_fixture_context(hook, codex_home: Path) -> str:
    return hook.build_context(codex_home / "corpus", codex_home / "canon.md")


def test_entrypoint_controls_admission_and_import_order(hook_module, tmp_path):
    codex_home = tmp_path / "codex-home"
    corpus_dir = codex_home / "corpus"
    write_text(corpus_dir / "rules" / "ius.md", "ius first\n")
    write_text(corpus_dir / "rules" / "rules.md", "rules second\n")
    write_text(corpus_dir / "unreferenced.md", "must remain absent\n")
    write_text(
        codex_home / "canon.md",
        "@import corpus/rules/ius.md\n@import corpus/rules/rules.md\n",
    )

    context = build_fixture_context(hook_module, codex_home)

    assert context.index("ius first") < context.index("rules second")
    assert "must remain absent" not in context
    assert "@import" not in context


def test_nested_imports_expand_but_fenced_and_indented_imports_remain_literal(
    hook_module, tmp_path
):
    codex_home = tmp_path / "codex-home"
    corpus_dir = codex_home / "corpus"
    write_text(corpus_dir / "nested" / "leaf.md", "expanded leaf\n")
    write_text(
        corpus_dir / "body.md",
        "@import nested/leaf.md\n```md\n@import nested/leaf.md\n```\n"
        "    @import nested/leaf.md\n",
    )
    write_text(codex_home / "canon.md", "@import corpus/body.md\n")

    context = build_fixture_context(hook_module, codex_home)

    assert context.count("expanded leaf") == 1
    assert context.count("@import nested/leaf.md") == 2


def test_canon_outside_corpus_root_is_accepted_and_escaping_import_is_rejected(
    hook_module, tmp_path
):
    codex_home = tmp_path / "codex-home"
    corpus_dir = codex_home / "corpus"
    write_text(corpus_dir / "rules" / "ius.md", "admitted doctrine\n")
    write_text(codex_home / "canon.md", "@import corpus/rules/ius.md\n")

    context = build_fixture_context(hook_module, codex_home)
    assert "admitted doctrine" in context

    write_text(codex_home.parent / "secret.md", "must never load\n")
    write_text(codex_home / "canon.md", "@import ../secret.md\n")
    with pytest.raises(hook_module.CanonError, match="escapes"):
        build_fixture_context(hook_module, codex_home)


@pytest.mark.parametrize(
    ("canon", "extra_files", "message"),
    [
        ("@import corpus/missing.md\n", {}, "missing import target"),
        (
            "@import corpus/cycle-a.md\n",
            {
                "cycle-a.md": "@import cycle-b.md\n",
                "cycle-b.md": "@import cycle-a.md\n",
            },
            "import cycle",
        ),
        (
            "@import corpus/escape.md\n",
            {
                "escape.md": "@import ../outside.md\n",
                "../outside.md": "outside\n",
            },
            "escapes",
        ),
        ("@import /absolute.md\n", {}, "absolute import target"),
    ],
)
def test_invalid_imports_fail_the_complete_canon(
    hook_module, tmp_path, canon, extra_files, message
):
    codex_home = tmp_path / "codex-home"
    corpus_dir = codex_home / "corpus"
    corpus_dir.mkdir(parents=True)
    write_text(codex_home / "canon.md", canon)
    for relative_path, content in extra_files.items():
        write_text(corpus_dir / relative_path, content)

    with pytest.raises(hook_module.CanonError, match=message):
        build_fixture_context(hook_module, codex_home)


def test_context_budget_accepts_exact_fit_and_rejects_overflow(hook_module, tmp_path):
    codex_home = tmp_path / "codex-home"
    corpus_dir = codex_home / "corpus"
    corpus_dir.mkdir(parents=True)
    write_text(codex_home / "canon.md", "bounded content\n")
    context = build_fixture_context(hook_module, codex_home)
    exact_bytes = len(context.encode("utf-8"))

    hook_module.MAX_CONTEXT_BYTES = exact_bytes
    assert build_fixture_context(hook_module, codex_home) == context

    hook_module.MAX_CONTEXT_BYTES = exact_bytes - 1
    with pytest.raises(hook_module.CanonError, match="expanded canon"):
        build_fixture_context(hook_module, codex_home)


def test_main_emits_sessionstart_additional_context(tmp_path):
    codex_home = tmp_path / "codex-home"
    write_text(codex_home / "corpus" / "rules" / "ius.md", "admitted doctrine\n")
    write_text(codex_home / "canon.md", "@import corpus/rules/ius.md\n")
    env = {**os.environ, "CODEX_HOME": str(codex_home)}

    completed = subprocess.run(
        [sys.executable, str(HOOK_PATH)],
        input=json.dumps({"hook_event_name": "SessionStart", "source": "startup", "cwd": str(tmp_path)}),
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )

    assert completed.returncode == 0
    assert completed.stderr == ""
    output = json.loads(completed.stdout)
    hook_output = output["hookSpecificOutput"]
    assert hook_output["hookEventName"] == "SessionStart"
    assert "admitted doctrine" in hook_output["additionalContext"]


def test_main_reports_missing_corpus_directory_without_partial_context(tmp_path):
    codex_home = tmp_path / "codex-home"
    codex_home.mkdir()
    write_text(codex_home / "canon.md", "@import corpus/rules/ius.md\n")
    env = {**os.environ, "CODEX_HOME": str(codex_home)}

    completed = subprocess.run(
        [sys.executable, str(HOOK_PATH)],
        input=json.dumps({"cwd": str(tmp_path)}),
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )

    assert completed.returncode == 0
    assert completed.stderr == ""
    output = json.loads(completed.stdout)
    assert "not loaded" in output["systemMessage"]
    assert "corpus directory not found" in output["systemMessage"]
    assert "hookSpecificOutput" not in output


def test_main_honors_explicit_production_root(tmp_path):
    codex_home = tmp_path / "codex-home"
    production_root = tmp_path / "production-corpus"
    write_text(production_root / "rules" / "ius.md", "selected production root\n")
    write_text(codex_home / "canon.md", "@import ../production-corpus/rules/ius.md\n")
    env = {
        **os.environ,
        "CODEX_HOME": str(codex_home),
        "CORPUS_IURIS_ROOT": str(production_root),
    }

    completed = subprocess.run(
        [sys.executable, str(HOOK_PATH)],
        input=json.dumps({"cwd": str(tmp_path)}),
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )

    assert completed.returncode == 0
    assert completed.stderr == ""
    output = json.loads(completed.stdout)
    assert "selected production root" in output["hookSpecificOutput"]["additionalContext"]


def test_missing_canon_is_a_successful_noop(hook_module, tmp_path):
    codex_home = tmp_path / "codex-home"
    codex_home.mkdir()
    env = {**os.environ, "CODEX_HOME": str(codex_home)}

    assert build_fixture_context(hook_module, codex_home) == ""

    completed = subprocess.run(
        [sys.executable, str(HOOK_PATH)],
        input=json.dumps({"cwd": str(tmp_path)}),
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )

    assert completed.returncode == 0
    assert completed.stdout == ""
    assert completed.stderr == ""


def test_empty_canon_is_a_successful_noop(hook_module, tmp_path):
    codex_home = tmp_path / "codex-home"
    write_text(codex_home / "canon.md", "\n")
    env = {**os.environ, "CODEX_HOME": str(codex_home)}

    assert build_fixture_context(hook_module, codex_home) == ""

    completed = subprocess.run(
        [sys.executable, str(HOOK_PATH)],
        input=json.dumps({"cwd": str(tmp_path)}),
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )

    assert completed.returncode == 0
    assert completed.stdout == ""
    assert completed.stderr == ""


@dataclass(frozen=True, slots=True, kw_only=True)
class ProjectSession:
    codex_home: Path
    root: Path
    workdir: Path

    @property
    def canon(self) -> Path:
        return self.root / ".codex" / "canon.md"

    @property
    def config(self) -> Path:
        return self.codex_home / "config.toml"


@pytest.fixture()
def project_session(tmp_path: Path) -> ProjectSession:
    codex_home = tmp_path / "codex-home"
    project = tmp_path / "project"
    nested = project / "src/module"
    (project / ".git").mkdir(parents=True)
    nested.mkdir(parents=True)
    write_text(codex_home / "canon.md", "@import corpus/global.md\n")
    write_text(codex_home / "corpus/global.md", "global provision\n")
    write_text(project / ".codex/canon.md", "@import corpus/project.md\n")
    write_text(project / ".codex/corpus/project.md", "project provision\n")
    return ProjectSession(codex_home=codex_home, root=project, workdir=nested)


def saved_entry(project: Path, level: str) -> str:
    project_key = str(project.resolve())
    if os.name == "nt":
        project_key = project_key.lower()
    return f"[projects.{json.dumps(project_key, ensure_ascii=False)}]\ntrust_level = {json.dumps(level)}\n"


def run_project_hook(session: ProjectSession, *, cwd: object) -> dict[str, object]:
    env = {
        **os.environ,
        "CODEX_HOME": str(session.codex_home),
        "CORPUS_IURIS_ROOT": str(session.codex_home / "corpus"),
    }
    completed = subprocess.run(
        [sys.executable, str(HOOK_PATH)],
        input=json.dumps({"hook_event_name": "SessionStart", "source": "startup", "cwd": cwd}),
        cwd=session.workdir,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert completed.stderr == ""
    return cast(dict[str, object], json.loads(completed.stdout))


def additional_context(output: dict[str, object]) -> str:
    hook_output = output["hookSpecificOutput"]
    assert isinstance(hook_output, dict)
    assert hook_output["hookEventName"] == "SessionStart"
    context = hook_output["additionalContext"]
    assert isinstance(context, str)
    return context


def assert_notice(context: str, reason: str) -> None:
    assert context.startswith("# Project canon status\n\n")
    assert context.count("# Project canon status") == 1
    assert reason in context
    assert "first user-facing reply" in context


def test_saved_grant_and_revocation_control_nested_project_canon(project_session: ProjectSession) -> None:
    session = project_session
    write_text(session.config, saved_entry(session.root, "trusted"))
    output = run_project_hook(session, cwd=str(session.workdir))
    context = additional_context(output)

    assert context.index("global provision") < context.index("project provision")
    assert context.count("global provision") == 1
    assert context.count("project provision") == 1
    assert "Project canon status" not in context
    assert "systemMessage" not in output

    write_text(session.config, saved_entry(session.root, "untrusted"))
    output = run_project_hook(session, cwd=str(session.workdir))
    context = additional_context(output)

    assert_notice(context, "saved as untrusted")
    assert "global provision" in context
    assert "project provision" not in context
    assert "systemMessage" not in output


@pytest.mark.parametrize("main_grant_only", [True, False])
def test_linked_worktree_requires_its_own_saved_grant(
    project_session: ProjectSession, main_grant_only: bool
) -> None:
    session = project_session
    (session.root / ".git").rmdir()
    primary = session.root.parent / "primary"
    write_text(session.root / ".git", f"gitdir: {primary / '.git/worktrees/project'}\n")
    entries = saved_entry(primary, "trusted")
    if not main_grant_only:
        entries += saved_entry(session.root, "trusted")
    write_text(session.config, entries)

    context = additional_context(run_project_hook(session, cwd=str(session.workdir)))
    if main_grant_only:
        assert_notice(context, "saved trust for this project could not be established")
        assert "project provision" not in context
    else:
        assert "project provision" in context
        assert "Project canon status" not in context


@pytest.mark.parametrize(
    "trust_case",
    [
        "missing-config", "unreadable-config", "malformed-config", "malformed-project-table",
        "unsupported-value", "untrusted", "other-checkouts", "project-local",
    ],
)
def test_withheld_project_canon_does_not_prevent_global_canon(
    project_session: ProjectSession, trust_case: str
) -> None:
    session = project_session
    write_text(session.canon, "@import\nnever disclose this project text\n")

    if trust_case == "unreadable-config":
        session.config.mkdir()
    elif trust_case == "malformed-config":
        write_text(session.config, "projects = [\nnever disclose this configuration")
    elif trust_case == "malformed-project-table":
        write_text(session.config, "projects = false\n")
    elif trust_case == "unsupported-value":
        write_text(session.config, saved_entry(session.root, "unsupported"))
    elif trust_case == "untrusted":
        write_text(session.config, saved_entry(session.root.parent, "trusted") + saved_entry(session.root, "untrusted"))
    elif trust_case == "other-checkouts":
        write_text(session.config, saved_entry(session.root.parent, "trusted") + saved_entry(session.workdir, "trusted"))
    elif trust_case == "project-local":
        write_text(session.canon.parent / "config.toml", saved_entry(session.root, "trusted"))

    output = run_project_hook(session, cwd=str(session.workdir))
    context = additional_context(output)
    reason = "saved as untrusted" if trust_case == "untrusted" else "saved trust for this project could not be established"
    assert_notice(context, reason)
    assert "global provision" in context
    assert "never disclose" not in context
    assert "systemMessage" not in output


@pytest.mark.parametrize("cwd", [None, 12, ".", "/missing\x00path"])
def test_invalid_event_cwd_omits_project_with_discovery_uncertainty(project_session: ProjectSession, cwd: object) -> None:
    session = project_session
    write_text(session.config, saved_entry(session.root, "trusted"))

    context = additional_context(run_project_hook(session, cwd=cwd))

    assert_notice(context, "could not determine whether project canon exists")
    assert "global provision" in context
    assert "project provision" not in context


@pytest.mark.parametrize("rejection", ["redirected-directory", "entrypoint", "invalid-import", "malformed", "early-global"])
def test_admitted_canon_rejection_sends_warning_and_notice(
    project_session: ProjectSession, rejection: str
) -> None:
    session = project_session
    write_text(session.config, saved_entry(session.root, "trusted"))
    outside = write_text(session.root.parent / "other-docs/canon.md", "external inert fixture\n")
    if rejection == "redirected-directory":
        session.canon.parent.rename(session.root / "old-canon-directory")
        session.canon.parent.symlink_to(outside.parent, target_is_directory=True)
    elif rejection == "entrypoint":
        session.canon.unlink()
        session.canon.symlink_to(outside)
    elif rejection == "invalid-import":
        (session.canon.parent / "outside.md").symlink_to(outside)
        write_text(session.canon, "@import outside.md\n")
    elif rejection == "malformed":
        write_text(session.canon, "@import\n")
    elif rejection == "early-global":
        write_text(session.codex_home / "canon.md", "@import corpus/missing.md\n")

    output = run_project_hook(session, cwd=str(session.workdir))
    context = additional_context(output)

    assert str(output["systemMessage"]).startswith("Corpus Iuris was not loaded")
    assert_notice(context, "canon could not be loaded")
    assert "global provision" not in context
    assert "project provision" not in context
    assert "external inert fixture" not in context
    assert str(outside) not in context


def test_notice_is_delivered_with_empty_global_canon(project_session: ProjectSession) -> None:
    session = project_session
    write_text(session.config, saved_entry(session.root, "untrusted"))
    write_text(session.codex_home / "canon.md", "\n")

    output = run_project_hook(session, cwd=str(session.workdir))
    context = additional_context(output)

    assert_notice(context, "saved as untrusted")
    assert "provision" not in context
    assert "systemMessage" not in output


def test_absent_candidate_has_no_notice(project_session: ProjectSession) -> None:
    session = project_session
    session.canon.unlink()

    context = additional_context(run_project_hook(session, cwd=str(session.workdir)))

    assert "global provision" in context
    assert "Project canon status" not in context


def test_notice_fits_beside_exact_global_limit_and_overflow_rejects_doctrine(project_session: ProjectSession) -> None:
    session = project_session
    write_text(session.config, saved_entry(session.root, "untrusted"))
    canon = write_text(session.codex_home / "canon.md", "G")
    context = additional_context(run_project_hook(session, cwd=str(session.workdir)))
    _, doctrine = context.split("\n\n# Global Corpus Iuris Canon", maxsplit=1)
    exact_content_size = 64_000 - len(("# Global Corpus Iuris Canon" + doctrine).encode("utf-8")) + 1
    write_text(canon, "G" * exact_content_size)
    context = additional_context(run_project_hook(session, cwd=str(session.workdir)))
    notice, doctrine = context.split("# Global Corpus Iuris Canon", maxsplit=1)

    assert_notice(notice, "saved as untrusted")
    assert len(notice.encode("utf-8")) <= 512
    assert len(("# Global Corpus Iuris Canon" + doctrine).encode("utf-8")) == 64_000

    write_text(session.config, saved_entry(session.root, "trusted"))
    output = run_project_hook(session, cwd=str(session.workdir))
    context = additional_context(output)

    assert str(output["systemMessage"]).startswith("Corpus Iuris was not loaded")
    assert_notice(context, "expanded doctrine exceeded the context limit")
    assert "Global Corpus Iuris Canon" not in context
    assert "Project Corpus Iuris Canon" not in context
