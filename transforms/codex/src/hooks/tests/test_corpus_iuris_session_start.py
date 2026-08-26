from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

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
        input=json.dumps({"hook_event_name": "SessionStart", "source": "startup"}),
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
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )

    assert completed.returncode == 0
    assert completed.stdout == ""
    assert completed.stderr == ""


def test_global_and_project_canons_are_loaded_in_order(hook_module, tmp_path):
    codex_home = tmp_path / "codex-home"
    project = tmp_path / "project"
    (project / ".git").mkdir(parents=True)

    write_text(codex_home / "canon.md", "@import corpus/global.md\n")
    write_text(codex_home / "corpus/global.md", "global provision\n")
    write_text(project / ".codex/canon.md", "@import corpus/project.md\n")
    write_text(project / ".codex/corpus/project.md", "project provision\n")

    context = hook_module.build_context(
        codex_home / "corpus",
        codex_home / "canon.md",
        project / ".codex/canon.md",
    )

    assert context.index("global provision") < context.index("project provision")
    assert context.count("global provision") == 1
    assert context.count("project provision") == 1


def test_main_loads_project_canon_from_nested_session_directory(tmp_path):
    codex_home = tmp_path / "codex-home"
    project = tmp_path / "project"
    nested = project / "src/module"
    (project / ".git").mkdir(parents=True)
    nested.mkdir(parents=True)
    (codex_home / "corpus").mkdir(parents=True)
    write_text(codex_home / "canon.md", "global canon\n")
    write_text(project / ".codex/canon.md", "project canon\n")
    env = {**os.environ, "CODEX_HOME": str(codex_home)}

    completed = subprocess.run(
        [sys.executable, str(HOOK_PATH)],
        input=json.dumps({"cwd": str(nested)}),
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )

    assert completed.returncode == 0
    assert completed.stderr == ""
    output = json.loads(completed.stdout)
    context = output["hookSpecificOutput"]["additionalContext"]
    assert context.index("global canon") < context.index("project canon")
