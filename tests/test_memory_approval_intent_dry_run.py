from __future__ import annotations

import io
import json
import os
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

from hermes_memory_fabric.codex_task_summary_ingestion import (
    candidates_to_jsonl,
    generate_codex_task_summary_candidates,
)
from hermes_memory_fabric.memory_candidate_proposal_dry_run import run_memory_candidate_proposal_dry_run
from hermes_memory_fabric.memory_approval_intent_dry_run import run_memory_approval_intent_dry_run


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLI_SCRIPT = PROJECT_ROOT / "scripts" / "create_approval_intent_dry_run.py"
SMOKE_SCRIPT = PROJECT_ROOT / "scripts" / "smoke_approval_intent_dry_run.py"

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


def _summary() -> str:
    return """# v1.7.0 Approval Intent Dry Run

Goal / Purpose
Convert v1.5 proposal dry-run previews into approval intent candidates.

Included / Changed files
- src/hermes_memory_fabric/memory_approval_intent_dry_run.py
- scripts/create_approval_intent_dry_run.py

Validation
- focused pytest
- smoke_approval_intent_dry_run.py

Boundary
- Dry-run intent only.
- No token issuance.
- No proposal creation.
- No operation ledger append.
- No executor invocation.
- No memory write.

Version
1.7.0

Result
Generated local approval intent dry-run objects for human review.
"""


def _preview() -> dict[str, object]:
    candidates = generate_codex_task_summary_candidates(_summary())
    low_risk = [candidate for candidate in candidates if candidate["risk_level"] == "low"]
    return run_memory_candidate_proposal_dry_run(low_risk)


def _assert_no_write_intent(result: dict[str, object]) -> None:
    assert result["dry_run"] is True
    assert result["human_review_required"] is True
    assert result["approval_token_issued"] is False
    assert result["approval_token_id"] is None
    assert result["creates_real_proposal"] is False
    assert result["writes_proposal_files"] is False
    assert result["writes_operation_ledger"] is False
    assert result["writes_memory"] is False
    assert result["writes_graph"] is False
    assert result["writes_config"] is False
    assert result["writes_sqlite"] is False
    assert result["writes_token_files"] is False
    assert result["writes_approval_audit"] is False
    assert result["invokes_real_executor"] is False
    assert result["applies_proposals"] is False
    assert result["provider_tools"] == []


def _hermes_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(path.relative_to(root) for path in root.rglob("*") if path.is_file())


def test_ready_intent_from_valid_v15_preview():
    preview = _preview()

    result = run_memory_approval_intent_dry_run(preview, repo_root=PROJECT_ROOT)

    assert result["version"] == "1.7.0"
    assert result["approval_intent_status"] == "ready"
    assert result["approval_intent_id"].startswith("approval-intent-dry-run-")
    assert result["source_preview_version"] == "1.5.0"
    assert result["source_accepted_count"] == preview["accepted_count"]
    assert result["intent_kind"] == "memory_write_proposal_approval_intent_candidate"
    assert result["required_human_decision"] == "review_approval_intent_candidate"
    assert result["safety_summary"]["v16_executor_surface_lockdown_audit"]["audit_status"] == "pass"
    _assert_no_write_intent(result)


def test_locked_when_accepted_count_is_zero():
    preview = _preview()
    preview["accepted_count"] = 0
    preview["proposal_previews"] = []

    result = run_memory_approval_intent_dry_run(preview, repo_root=PROJECT_ROOT)

    assert result["approval_intent_status"] == "locked"
    assert result["required_human_decision"] == "none_no_accepted_source_previews"
    _assert_no_write_intent(result)


def test_rejected_when_any_write_flag_is_true():
    for flag in (
        "created_real_proposal",
        "writes_proposal_files",
        "writes_operation_ledger",
        "writes_memory",
        "writes_graph",
        "writes_config",
        "writes_sqlite",
        "writes_token_files",
        "writes_approval_audit",
        "applies_proposals",
    ):
        preview = _preview()
        preview[flag] = True

        result = run_memory_approval_intent_dry_run(preview, repo_root=PROJECT_ROOT)

        assert result["approval_intent_status"] == "rejected"
        assert f"source_{flag}_must_be_false" in result["safety_summary"]["source_preview_errors"]
        _assert_no_write_intent(result)


def test_rejected_when_provider_tools_is_not_empty():
    preview = _preview()
    preview["provider_tools"] = ["unsafe_tool"]

    result = run_memory_approval_intent_dry_run(preview, repo_root=PROJECT_ROOT)

    assert result["approval_intent_status"] == "rejected"
    assert "source_provider_tools_must_be_empty" in result["safety_summary"]["source_preview_errors"]
    _assert_no_write_intent(result)


def test_rejected_when_source_preview_missing_required_fields():
    preview = _preview()
    del preview["accepted_count"]

    result = run_memory_approval_intent_dry_run(preview, repo_root=PROJECT_ROOT)

    assert result["approval_intent_status"] == "rejected"
    assert "missing_accepted_count" in result["safety_summary"]["source_preview_errors"]
    _assert_no_write_intent(result)


def test_rejected_when_v16_audit_fails_using_fake_repo(tmp_path):
    repo = _minimal_repo(tmp_path)
    _write(repo / "src/hermes_memory_fabric/memory_human_approval_token_real_write_executor.py", "")

    result = run_memory_approval_intent_dry_run(_preview(), repo_root=repo)

    assert result["approval_intent_status"] == "rejected"
    assert result["safety_summary"]["v16_executor_surface_lockdown_audit"]["audit_status"] == "fail"
    _assert_no_write_intent(result)


def test_deterministic_approval_intent_id():
    preview = _preview()

    first = run_memory_approval_intent_dry_run(preview, repo_root=PROJECT_ROOT)
    second = run_memory_approval_intent_dry_run(preview, repo_root=PROJECT_ROOT)

    assert first["approval_intent_id"] == second["approval_intent_id"]
    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)


def test_input_preview_dict_is_not_mutated():
    preview = _preview()
    before = deepcopy(preview)

    result = run_memory_approval_intent_dry_run(preview, repo_root=PROJECT_ROOT)
    result["source_preview_snapshot"]["proposal_previews"].clear()

    assert preview == before


def test_cli_stdout_writes_no_files(tmp_path):
    preview_path = tmp_path / "preview.json"
    preview_path.write_text(json.dumps(_preview(), sort_keys=True), encoding="utf-8")
    before = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*") if path.is_file())

    completed = _run_cli(["--input", str(preview_path), "--repo-root", str(PROJECT_ROOT)], tmp_path)

    after = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*") if path.is_file())
    result = json.loads(completed.stdout)
    assert completed.returncode == 0
    assert completed.stderr == ""
    assert after == before == [Path("preview.json")]
    assert result["approval_intent_status"] == "ready"
    _assert_no_write_intent(result)


def test_cli_explicit_output_writes_only_requested_file(tmp_path):
    preview_path = tmp_path / "preview.json"
    output_path = tmp_path / "intent.json"
    preview_path.write_text(json.dumps(_preview(), sort_keys=True), encoding="utf-8")

    completed = _run_cli(
        [
            "--input",
            str(preview_path),
            "--repo-root",
            str(PROJECT_ROOT),
            "--output",
            str(output_path),
            "--print-summary",
        ],
        tmp_path,
    )

    assert completed.returncode == 0
    assert completed.stdout == ""
    assert "approval_intent_dry_run_summary=" in completed.stderr
    assert sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*") if path.is_file()) == [
        Path("intent.json"),
        Path("preview.json"),
    ]
    result = json.loads(output_path.read_text(encoding="utf-8"))
    assert result["approval_intent_status"] == "ready"
    _assert_no_write_intent(result)


def test_cli_refuses_output_under_hermes_home(tmp_path):
    hermes_home = tmp_path / "hermes-home"
    preview_path = tmp_path / "preview.json"
    output_path = hermes_home / "intent.json"
    preview_path.write_text(json.dumps(_preview(), sort_keys=True), encoding="utf-8")
    env = dict(os.environ)
    env["PYTHONPATH"] = f"{PROJECT_ROOT / 'src'}:{PROJECT_ROOT}"
    env["HERMES_HOME"] = str(hermes_home)

    completed = subprocess.run(
        [
            sys.executable,
            str(CLI_SCRIPT),
            "--input",
            str(preview_path),
            "--repo-root",
            str(PROJECT_ROOT),
            "--output",
            str(output_path),
        ],
        cwd=tmp_path,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 2
    assert completed.stdout == ""
    assert "refusing_output_under_hermes_home" in completed.stderr
    assert _hermes_files(hermes_home) == []


def test_smoke_chain_remains_no_write(tmp_path, monkeypatch):
    hermes_home = tmp_path / "hermes-home"
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))
    candidates = generate_codex_task_summary_candidates(_summary())
    candidate_jsonl = candidates_to_jsonl(candidates)
    loaded_candidates = [json.loads(line) for line in io.StringIO(candidate_jsonl) if line.strip()]

    before = _hermes_files(hermes_home)
    preview = run_memory_candidate_proposal_dry_run(loaded_candidates)
    result = run_memory_approval_intent_dry_run(preview, repo_root=PROJECT_ROOT)
    after = _hermes_files(hermes_home)

    assert result["approval_intent_status"] == "ready"
    _assert_no_write_intent(result)
    assert before == []
    assert after == []


def _run_cli(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = f"{PROJECT_ROOT / 'src'}:{PROJECT_ROOT}"
    return subprocess.run(
        [sys.executable, str(CLI_SCRIPT), *args],
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


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


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
