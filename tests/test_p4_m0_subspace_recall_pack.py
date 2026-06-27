from __future__ import annotations

import io
import os
import subprocess
import sys
import tomllib
from pathlib import Path

from hermes_memory_fabric.p4_m0_subspace_recall_pack import run_recall_pack_export
from hermes_memory_fabric.p4_m0_subspace_workspace import create_workspace_subspace_memory_store


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _run(argv: list[str]) -> tuple[int, str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_recall_pack_export(argv, stdout=stdout, stderr=stderr)

    return exit_code, stdout.getvalue(), stderr.getvalue()


def test_recall_pack_includes_query_scope_result_metadata_and_content(tmp_path):
    memory_id = _approved_memory(
        tmp_path,
        project="civilization-core",
        namespace="boundary",
        content="Recall pack export keeps approved boundary memory human-copyable.",
        source="unit-test",
    )

    exit_code, pack, stderr = _run(
        [
            "--workspace-root",
            str(tmp_path),
            "--query",
            "approved boundary",
            "--project",
            "civilization-core",
            "--namespace",
            "boundary",
            "--limit",
            "5",
        ]
    )

    assert exit_code == 0
    assert stderr == ""
    assert "# Subspace Memory Recall Pack" in pack
    assert "## Query\n\napproved boundary" in pack
    assert "- Project: civilization-core" in pack
    assert "- Namespace: boundary" in pack
    assert "- Limit: 5" in pack
    assert f"- Storage Root: {tmp_path / '.local' / 'subspace_memory'}" in pack
    assert f"### 1. {memory_id}" in pack
    assert "- Score: 2" in pack
    assert "- Source: unit-test" in pack
    assert "- Matched Terms: approved, boundary" in pack
    assert "Recall pack export keeps approved boundary memory human-copyable." in pack
    assert "Use this recall pack as human-provided context only." in pack


def test_recall_pack_is_deterministic_for_same_store_and_query(tmp_path):
    _approved_memory(
        tmp_path,
        project="civilization-core",
        namespace="determinism",
        content="Deterministic pack output repeats approved context.",
    )

    argv = [
        "--workspace-root",
        str(tmp_path),
        "--query",
        "deterministic approved",
        "--project",
        "civilization-core",
        "--namespace",
        "determinism",
    ]

    first_code, first_pack, first_stderr = _run(argv)
    second_code, second_pack, second_stderr = _run(argv)

    assert first_code == 0
    assert second_code == 0
    assert first_stderr == ""
    assert second_stderr == ""
    assert first_pack == second_pack


def test_recall_pack_respects_project_and_namespace_filters(tmp_path):
    matching_id = _approved_memory(
        tmp_path,
        project="civilization-core",
        namespace="recall-pack",
        content="Filter keyword belongs to the recall pack namespace.",
    )
    _approved_memory(
        tmp_path,
        project="other-project",
        namespace="recall-pack",
        content="Filter keyword belongs to another project.",
    )
    _approved_memory(
        tmp_path,
        project="civilization-core",
        namespace="other-namespace",
        content="Filter keyword belongs to another namespace.",
    )

    exit_code, pack, stderr = _run(
        [
            "--workspace-root",
            str(tmp_path),
            "--query",
            "filter keyword",
            "--project",
            "civilization-core",
            "--namespace",
            "recall-pack",
        ]
    )

    assert exit_code == 0
    assert stderr == ""
    assert f"### 1. {matching_id}" in pack
    assert "other-project" not in pack
    assert "other-namespace" not in pack


def test_limit_is_respected(tmp_path):
    first_id = _approved_memory(
        tmp_path,
        project="civilization-core",
        namespace="limit",
        content="Limit keyword alpha beta.",
    )
    _approved_memory(
        tmp_path,
        project="civilization-core",
        namespace="limit",
        content="Limit keyword alpha.",
    )

    exit_code, pack, stderr = _run(
        [
            "--workspace-root",
            str(tmp_path),
            "--query",
            "limit keyword alpha beta",
            "--project",
            "civilization-core",
            "--namespace",
            "limit",
            "--limit",
            "1",
        ]
    )

    assert exit_code == 0
    assert stderr == ""
    assert f"### 1. {first_id}" in pack
    assert "### 2." not in pack


def test_empty_recall_output_is_deterministic_when_include_empty_is_used(tmp_path):
    argv = [
        "--workspace-root",
        str(tmp_path),
        "--query",
        "missing recall",
        "--project",
        "civilization-core",
        "--namespace",
        "empty",
        "--include-empty",
    ]

    first_code, first_pack, first_stderr = _run(argv)
    second_code, second_pack, second_stderr = _run(argv)

    assert first_code == 0
    assert second_code == 0
    assert first_stderr == ""
    assert second_stderr == ""
    assert first_pack == second_pack
    assert "No approved recall results matched this query." in first_pack


def test_missing_required_query_returns_nonzero_with_stderr(tmp_path):
    exit_code, stdout, stderr = _run(["--workspace-root", str(tmp_path)])

    assert exit_code != 0
    assert stdout == ""
    assert "the following arguments are required: --query" in stderr


def test_non_positive_limit_returns_nonzero_with_stderr(tmp_path):
    exit_code, stdout, stderr = _run(
        [
            "--workspace-root",
            str(tmp_path),
            "--query",
            "approved",
            "--limit",
            "0",
            "--include-empty",
        ]
    )

    assert exit_code == 1
    assert stdout == ""
    assert stderr == "limit_must_be_positive\n"


def test_recall_pack_export_does_not_create_proposal_memory_or_audit_records(tmp_path):
    _approved_memory(
        tmp_path,
        project="civilization-core",
        namespace="read-only",
        content="Read only recall pack export uses approved memory.",
    )
    storage_root = tmp_path / ".local" / "subspace_memory"
    before = {
        path.name: path.read_text(encoding="utf-8")
        for path in sorted(storage_root.iterdir())
        if path.is_file()
    }

    exit_code, _, stderr = _run(
        [
            "--workspace-root",
            str(tmp_path),
            "--query",
            "read only approved",
            "--project",
            "civilization-core",
            "--namespace",
            "read-only",
        ]
    )

    after = {
        path.name: path.read_text(encoding="utf-8")
        for path in sorted(storage_root.iterdir())
        if path.is_file()
    }
    assert exit_code == 0
    assert stderr == ""
    assert after == before


def test_default_workspace_root_uses_local_subspace_memory(tmp_path, monkeypatch):
    _approved_memory(
        tmp_path,
        project="civilization-core",
        namespace="default-root",
        content="Default root approved memory is recallable.",
    )
    monkeypatch.chdir(tmp_path)

    exit_code, pack, stderr = _run(
        [
            "--query",
            "default approved",
            "--project",
            "civilization-core",
            "--namespace",
            "default-root",
        ]
    )

    assert exit_code == 0
    assert stderr == ""
    assert f"- Storage Root: {tmp_path / '.local' / 'subspace_memory'}" in pack


def test_explicit_workspace_root_works(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    _approved_memory(
        workspace,
        project="civilization-core",
        namespace="explicit-root",
        content="Explicit root approved memory is recallable.",
    )

    exit_code, pack, stderr = _run(
        [
            "--workspace-root",
            str(workspace),
            "--query",
            "explicit approved",
            "--project",
            "civilization-core",
            "--namespace",
            "explicit-root",
        ]
    )

    assert exit_code == 0
    assert stderr == ""
    assert f"- Storage Root: {workspace / '.local' / 'subspace_memory'}" in pack


def test_manual_python_module_execution_is_safe(tmp_path):
    _approved_memory(
        tmp_path,
        project="civilization-core",
        namespace="manual",
        content="Manual module execution exports approved recall context.",
    )
    env = {**os.environ, "PYTHONPATH": str(PROJECT_ROOT / "src")}

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "hermes_memory_fabric.p4_m0_subspace_recall_pack",
            "--workspace-root",
            str(tmp_path),
            "--query",
            "manual approved",
            "--project",
            "civilization-core",
            "--namespace",
            "manual",
        ],
        cwd=PROJECT_ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0
    assert completed.stderr == ""
    assert "# Subspace Memory Recall Pack" in completed.stdout
    assert "Manual module execution exports approved recall context." in completed.stdout


def test_output_file_is_only_written_when_explicitly_requested(tmp_path):
    _approved_memory(
        tmp_path,
        project="civilization-core",
        namespace="output",
        content="Explicit output file receives the recall pack.",
    )
    output = tmp_path / "recall-pack.md"

    exit_code, stdout, stderr = _run(
        [
            "--workspace-root",
            str(tmp_path),
            "--query",
            "explicit output",
            "--project",
            "civilization-core",
            "--namespace",
            "output",
            "--output",
            str(output),
        ]
    )

    assert exit_code == 0
    assert stdout == ""
    assert stderr == ""
    assert output.read_text(encoding="utf-8").startswith("# Subspace Memory Recall Pack\n")


def test_package_version_remains_6_16_0():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert pyproject["project"]["version"] == "6.16.0"


def test_no_uv_lock_is_created():
    assert not Path("uv.lock").exists()


def test_no_pyproject_entry_point_is_added_for_recall_pack():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert "scripts" not in pyproject["project"]
    assert "gui-scripts" not in pyproject["project"]
    assert "console_scripts" not in pyproject["project"].get("entry-points", {})
    assert "p4_m0_subspace_recall_pack" not in str(pyproject["project"].get("entry-points", {}))


def _approved_memory(
    workspace_root: Path,
    *,
    project: str,
    namespace: str,
    content: str,
    source: str = "recall-pack-test",
) -> str:
    store = create_workspace_subspace_memory_store(workspace_root)
    proposal = store.propose_memory(
        project=project,
        namespace=namespace,
        content=content,
        source=source,
    )
    memory = store.approve_proposal(proposal.id, approver="human")
    return memory.id
