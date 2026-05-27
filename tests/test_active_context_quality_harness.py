from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from hermes_memory_fabric import MemoryFabricProvider
from scripts.run_active_context_quality_harness import DEFAULT_CASES_PATH, load_cases, run_harness


REPO_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_DIMENSIONS = {
    "project_scope_isolation",
    "archived_memory_rejection",
    "context_budget_and_rejection_compaction",
    "high_risk_rejection",
    "high_risk_allowed",
    "temporal_conflict_resolution",
    "no_write_safety_policy",
}


def test_default_fixture_exists_and_has_required_cases():
    cases = load_cases()
    dimensions = {case["dimension"] for case in cases}

    assert DEFAULT_CASES_PATH.exists()
    assert len(cases) >= 6
    assert REQUIRED_DIMENSIONS.issubset(dimensions)


def test_harness_scores_default_fixture_perfectly():
    report = run_harness()

    assert report["harness_type"] == "active_context_quality_harness_v0.9.0"
    assert report["aggregate"]["overall_score"] == 1.0
    assert report["aggregate"]["failed_count"] == 0
    assert all(case["passed"] for case in report["cases"])


def test_selected_and_rejected_memory_ids_match_expectations():
    cases = {case["id"]: case for case in load_cases()}
    report = run_harness()

    for result in report["cases"]:
        case = cases[result["id"]]
        evidence = result["evidence"]
        assert evidence["selected_memory_ids"] == case.get("expected_selected_memory_ids", [])
        assert set(evidence["rejected_memory_ids"]) == set(case.get("expected_rejected_memory_ids", []))


def test_rejected_memory_content_is_not_present_in_compact_context_text():
    cases = {case["id"]: case for case in load_cases()}
    report = run_harness()

    for result in report["cases"]:
        case = cases[result["id"]]
        rejected_ids = set(result["evidence"]["rejected_memory_ids"])
        compact_context_text = result["evidence"]["compact_context_text"]
        for memory in case.get("memories", []):
            if memory["id"] in rejected_ids:
                assert memory["content"] not in compact_context_text


def test_policy_remains_read_only_and_provider_tools_stay_hidden():
    provider = MemoryFabricProvider()
    report = run_harness()

    assert provider.get_tool_schemas() == []
    for result in report["cases"]:
        evidence = result["evidence"]
        policy = evidence["policy"]
        assert policy["read_only"] is True
        assert policy["would_write_memory"] is False
        assert policy["would_modify_config"] is False
        assert policy["would_write_graph"] is False
        assert policy["writes_token_files"] is False
        assert policy["writes_approval_audit"] is False
        assert policy["invokes_real_token_write_executor"] is False
        assert policy["implements_real_token_write_executor"] is False
        assert policy["exposes_provider_tools"] is False
        assert evidence["provider_tools"] == []


def test_json_output_is_valid_json():
    result = _run_harness_subprocess("--json")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["aggregate"]["overall_score"] == 1.0
    assert payload["aggregate"]["case_count"] >= 6


def test_fail_on_score_below_one_exits_zero_for_passing_fixture():
    result = _run_harness_subprocess("--fail-on-score-below", "1.0")

    assert result.returncode == 0
    assert "overall_score=1.000" in result.stdout


def test_harness_writes_no_files_to_temp_hermes_memory_directory(tmp_path):
    hermes_home = tmp_path / "hermes-home"
    hermes_home.mkdir()
    memory_dir = hermes_home / "memory"
    result = _run_harness_subprocess("--json", hermes_home=hermes_home)

    assert result.returncode == 0
    assert not memory_dir.exists() or not any(memory_dir.rglob("*"))


def _run_harness_subprocess(*args: str, hermes_home: Path | None = None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{REPO_ROOT / 'src'}:{REPO_ROOT}"
    if hermes_home is not None:
        env["HERMES_HOME"] = str(hermes_home)
    return subprocess.run(
        [sys.executable, "scripts/run_active_context_quality_harness.py", *args],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
