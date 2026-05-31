from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from hermes_memory_fabric.memory_executor_surface_lockdown_audit import (
    audit_executor_surface_lockdown,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLI_SCRIPT = PROJECT_ROOT / "scripts" / "audit_executor_surface_lockdown.py"

_NO_WRITE_FLAG_SOURCE = """
MEMORY_HUMAN_APPROVAL_TOKEN_REAL_WRITE_EXECUTOR_IMPLEMENTATION_PLAN_POLICY = {
    "invokes_real_token_write_executor": False,
    "implements_real_token_write_executor": False,
    "issues_real_approval_tokens": False,
    "writes_operation_ledger": False,
    "writes_token_files": False,
    "writes_approval_audit": False,
    "applies_proposals": False,
}
"""


def test_current_repo_passes_executor_surface_lockdown_audit():
    report = audit_executor_surface_lockdown(PROJECT_ROOT)

    assert report["audit_status"] == "pass"
    assert report["provider_tools"] == []
    assert report["forbidden_files_present"] == []
    assert report["forbidden_calls"] == []
    assert report["forbidden_write_surfaces"] == []
    assert report["missing_no_write_flags"] == []
    assert report["v15_boundary_status"] == "pass"


def test_fake_repo_with_forbidden_real_write_executor_module_fails(tmp_path):
    repo = _minimal_repo(tmp_path)
    _write(repo / "src/hermes_memory_fabric/memory_human_approval_token_real_write_executor.py", "")

    report = audit_executor_surface_lockdown(repo)

    assert report["audit_status"] == "fail"
    assert report["forbidden_files_present"] == [
        "src/hermes_memory_fabric/memory_human_approval_token_real_write_executor.py"
    ]


def test_fake_repo_with_forbidden_real_write_executor_test_fails(tmp_path):
    repo = _minimal_repo(tmp_path)
    _write(repo / "tests/test_memory_human_approval_token_real_write_executor.py", "")

    report = audit_executor_surface_lockdown(repo)

    assert report["audit_status"] == "fail"
    assert report["forbidden_files_present"] == [
        "tests/test_memory_human_approval_token_real_write_executor.py"
    ]


def test_fake_repo_with_create_memory_write_proposal_call_fails(tmp_path):
    repo = _minimal_repo(tmp_path)
    _write(
        repo / "src/hermes_memory_fabric/memory_candidate_proposal_dry_run.py",
        _v15_source()
        + """
def unsafe_path(memory_fabric_bridge):
    memory_fabric_bridge.create_memory_write_proposal({})
""",
    )

    report = audit_executor_surface_lockdown(repo)

    assert report["audit_status"] == "fail"
    assert len(report["forbidden_calls"]) == 1
    finding = report["forbidden_calls"][0]
    assert finding["path"] == "src/hermes_memory_fabric/memory_candidate_proposal_dry_run.py"
    assert finding["line"] > 0
    assert finding["surface"] == "memory_fabric_bridge.create_memory_write_proposal"
    assert finding["snippet"] == "memory_fabric_bridge.create_memory_write_proposal({})"


def test_fake_executor_module_missing_no_write_flags_fails(tmp_path):
    repo = _minimal_repo(tmp_path)
    _write(
        repo / "src/hermes_memory_fabric/memory_human_approval_token_real_write_executor_implementation_plan.py",
        "IMPLEMENTATION_PLAN = {}\n",
    )

    report = audit_executor_surface_lockdown(repo)

    assert report["audit_status"] == "fail"
    assert report["missing_no_write_flags"] == [
        {
            "path": (
                "src/hermes_memory_fabric/"
                "memory_human_approval_token_real_write_executor_implementation_plan.py"
            ),
            "missing_flags": [
                "invokes_real_token_write_executor",
                "implements_real_token_write_executor",
                "issues_real_approval_tokens",
                "writes_operation_ledger",
                "writes_token_files",
                "writes_approval_audit",
                "applies_proposals",
            ],
        }
    ]


def test_fake_executor_module_with_path_write_text_fails(tmp_path):
    repo = _minimal_repo(tmp_path)
    _write(
        repo / "src/hermes_memory_fabric/memory_human_approval_token_real_write_executor_implementation_plan.py",
        _NO_WRITE_FLAG_SOURCE
        + """
from pathlib import Path


def unsafe_write():
    Path("token.json").write_text("real write", encoding="utf-8")
""",
    )

    report = audit_executor_surface_lockdown(repo)

    assert report["audit_status"] == "fail"
    assert len(report["forbidden_write_surfaces"]) == 1
    finding = report["forbidden_write_surfaces"][0]
    assert finding["path"] == (
        "src/hermes_memory_fabric/"
        "memory_human_approval_token_real_write_executor_implementation_plan.py"
    )
    assert finding["line"] > 0
    assert finding["surface"] == "path_write_text"
    assert finding["snippet"] == 'Path("token.json").write_text("real write", encoding="utf-8")'


def test_pycache_files_are_ignored(tmp_path):
    repo = _minimal_repo(tmp_path)
    _write(
        repo
        / "src/hermes_memory_fabric/__pycache__/memory_human_approval_token_real_write_executor.py",
        'from pathlib import Path\nPath("x").write_text("unsafe")\n',
    )

    report = audit_executor_surface_lockdown(repo)

    assert report["audit_status"] == "pass"
    assert report["forbidden_files_present"] == []
    assert report["forbidden_write_surfaces"] == []
    assert report["skipped_files"] == [
        "src/hermes_memory_fabric/__pycache__/memory_human_approval_token_real_write_executor.py"
    ]


def test_cli_stdout_writes_no_files(tmp_path):
    repo = _minimal_repo(tmp_path)
    before = _snapshot_files(repo)

    completed = _run_cli(["--repo-root", str(repo)], tmp_path)

    after = _snapshot_files(repo)
    report = json.loads(completed.stdout)
    assert completed.returncode == 0
    assert completed.stderr == ""
    assert after == before
    assert report["audit_status"] == "pass"


def test_cli_explicit_output_writes_only_requested_file(tmp_path):
    repo = _minimal_repo(tmp_path)
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    output_path = output_dir / "executor-surface-lockdown-audit.json"
    before_repo = _snapshot_files(repo)

    completed = _run_cli(
        ["--repo-root", str(repo), "--output", str(output_path), "--print-summary"],
        tmp_path,
    )

    assert completed.returncode == 0
    assert completed.stdout == ""
    assert "executor_surface_lockdown_audit_summary=" in completed.stderr
    assert _snapshot_files(repo) == before_repo
    assert sorted(path.relative_to(output_dir) for path in output_dir.rglob("*") if path.is_file()) == [
        Path("executor-surface-lockdown-audit.json")
    ]
    report = json.loads(output_path.read_text(encoding="utf-8"))
    assert report["audit_status"] == "pass"


def test_input_repo_files_are_not_mutated(tmp_path):
    repo = _minimal_repo(tmp_path)
    before = _snapshot_files(repo)

    report = audit_executor_surface_lockdown(repo)

    assert report["audit_status"] == "pass"
    assert _snapshot_files(repo) == before


def test_provider_tools_are_empty():
    report = audit_executor_surface_lockdown(PROJECT_ROOT)

    assert report["provider_tools"] == []


def _minimal_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    package = repo / "src/hermes_memory_fabric"
    package.mkdir(parents=True)
    (repo / "tests").mkdir()
    (repo / "scripts").mkdir()
    _write(
        package / "provider.py",
        """
class MemoryFabricProvider:
    def get_tool_schemas(self):
        return []
""",
    )
    _write(package / "memory_candidate_proposal_dry_run.py", _v15_source())
    _write(
        package / "memory_human_approval_token_real_write_executor_implementation_plan.py",
        _NO_WRITE_FLAG_SOURCE,
    )
    return repo


def _v15_source() -> str:
    return """
REAL_WRITE_FLAGS = {
    "created_real_proposal": False,
    "writes_proposal_files": False,
    "writes_operation_ledger": False,
    "writes_memory": False,
    "writes_graph": False,
    "writes_config": False,
    "writes_sqlite": False,
    "writes_token_files": False,
    "writes_approval_audit": False,
    "applies_proposals": False,
}


def run_memory_candidate_proposal_dry_run():
    return {
        **REAL_WRITE_FLAGS,
        "provider_tools": [],
    }
"""


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.lstrip(), encoding="utf-8")


def _snapshot_files(root: Path) -> dict[Path, bytes]:
    return {
        path.relative_to(root): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _run_cli(args: list[str], tmp_path: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    pythonpath_parts = [str(PROJECT_ROOT / "src"), str(PROJECT_ROOT)]
    if env.get("PYTHONPATH"):
        pythonpath_parts.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["HERMES_HOME"] = str(tmp_path / "hermes-home")
    return subprocess.run(
        [sys.executable, str(CLI_SCRIPT), *args],
        cwd=PROJECT_ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
