from __future__ import annotations

import json
import os
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest

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
ADMISSION_WORKSPACE = "/workspace/active-context-quality-harness"
ADMISSION_NAMESPACE = "active-context-quality"
HARNESS_SOURCE = {
    "provider_id": "quality-harness-local-caller",
    "source_class": "LOCAL_CALLER",
    "source_instance": "harness:v09",
}
HARNESS_PROVIDER_REGISTRY = {
    "quality-harness-local-caller": {
        "enabled": True,
        "source_classes": ["LOCAL_CALLER"],
        "capabilities": ["READ_CANDIDATE"],
        "review_only": False,
        "trusted_ingestion": True,
    }
}


@pytest.fixture(scope="module")
def admitted_cases_path(tmp_path_factory) -> Path:
    cases = deepcopy(load_cases())
    for case in cases:
        existing = case.get("provider_runtime_config", {})
        runtime_config = deepcopy(dict(existing)) if isinstance(existing, dict) else {}
        runtime_config.update(
            {
                "admission_scope": {
                    "project": case["project_scope"],
                    "workspace": ADMISSION_WORKSPACE,
                    "namespace": ADMISSION_NAMESPACE,
                },
                "provider_registry_snapshot": deepcopy(HARNESS_PROVIDER_REGISTRY),
                "direct_candidate_source": deepcopy(HARNESS_SOURCE),
            }
        )
        case["provider_runtime_config"] = runtime_config
    path = tmp_path_factory.mktemp("active-context-quality-admission") / "v09_cases.json"
    path.write_text(json.dumps(cases, sort_keys=True), encoding="utf-8")
    return path


def test_default_fixture_exists_and_has_required_cases():
    cases = load_cases()
    dimensions = {case["dimension"] for case in cases}

    assert DEFAULT_CASES_PATH.exists()
    assert len(cases) >= 6
    assert REQUIRED_DIMENSIONS.issubset(dimensions)


def test_harness_scores_default_fixture_perfectly(admitted_cases_path):
    report = run_harness(admitted_cases_path)

    assert report["harness_type"] == "active_context_quality_harness_v0.9.0"
    assert report["aggregate"]["overall_score"] == 1.0
    assert report["aggregate"]["failed_count"] == 0
    assert all(case["passed"] for case in report["cases"])


def test_default_cli_uses_builtin_admission_for_builtin_fixture(tmp_path):
    before = DEFAULT_CASES_PATH.read_bytes()
    hermes_home = tmp_path / "hermes-home"
    result = _run_harness_subprocess(
        "--json", "--fail-on-score-below", "1.0", hermes_home=hermes_home
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["cases_path"] == str(DEFAULT_CASES_PATH)
    assert payload["aggregate"]["overall_score"] == 1.0
    assert DEFAULT_CASES_PATH.read_bytes() == before
    assert not hermes_home.exists() or not any(hermes_home.rglob("*"))


def test_external_fixture_does_not_receive_builtin_admission_defaults(tmp_path):
    external_path = tmp_path / "external-v09-cases.json"
    external_path.write_bytes(DEFAULT_CASES_PATH.read_bytes())

    report = run_harness(external_path)

    assert report["aggregate"]["overall_score"] == 0.0
    assert all(not case["passed"] for case in report["cases"])


def test_explicit_rejection_configuration_is_not_overridden_for_external_fixture(tmp_path):
    cases = deepcopy(load_cases())
    case = cases[0]
    case["provider_runtime_config"] = {
        "admission_scope": {
            "project": case["project_scope"],
            "workspace": ADMISSION_WORKSPACE,
            "namespace": ADMISSION_NAMESPACE,
        },
        "provider_registry_snapshot": {
            HARNESS_SOURCE["provider_id"]: {
                "enabled": False,
                "source_classes": ["LOCAL_CALLER"],
                "capabilities": ["READ_CANDIDATE"],
                "review_only": False,
                "trusted_ingestion": True,
            }
        },
        "direct_candidate_source": deepcopy(HARNESS_SOURCE),
    }
    external_path = tmp_path / "explicit-rejection-cases.json"
    external_path.write_text(json.dumps([case], sort_keys=True), encoding="utf-8")

    report = run_harness(external_path)

    assert report["aggregate"]["overall_score"] == 0.0
    assert report["cases"][0]["evidence"]["selected_memory_ids"] == []


def test_selected_and_rejected_memory_ids_match_expectations(admitted_cases_path):
    cases = {case["id"]: case for case in load_cases()}
    report = run_harness(admitted_cases_path)

    for result in report["cases"]:
        case = cases[result["id"]]
        evidence = result["evidence"]
        assert evidence["selected_memory_ids"] == case.get("expected_selected_memory_ids", [])
        assert set(evidence["rejected_memory_ids"]) == set(case.get("expected_rejected_memory_ids", []))


def test_rejected_memory_content_is_not_present_in_compact_context_text(admitted_cases_path):
    cases = {case["id"]: case for case in load_cases()}
    report = run_harness(admitted_cases_path)

    for result in report["cases"]:
        case = cases[result["id"]]
        rejected_ids = set(result["evidence"]["rejected_memory_ids"])
        compact_context_text = result["evidence"]["compact_context_text"]
        for memory in case.get("memories", []):
            if memory["id"] in rejected_ids:
                assert memory["content"] not in compact_context_text


def test_policy_remains_read_only_and_provider_tools_stay_hidden(admitted_cases_path):
    provider = MemoryFabricProvider()
    report = run_harness(admitted_cases_path)

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


def test_json_output_is_valid_json(admitted_cases_path):
    result = _run_harness_subprocess("--json", cases_path=admitted_cases_path)

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["aggregate"]["overall_score"] == 1.0
    assert payload["aggregate"]["case_count"] >= 6


def test_fail_on_score_below_one_exits_zero_for_passing_fixture(admitted_cases_path):
    result = _run_harness_subprocess(
        "--fail-on-score-below", "1.0", cases_path=admitted_cases_path
    )

    assert result.returncode == 0
    assert "overall_score=1.000" in result.stdout


def test_harness_writes_no_files_to_temp_hermes_memory_directory(tmp_path, admitted_cases_path):
    hermes_home = tmp_path / "hermes-home"
    hermes_home.mkdir()
    memory_dir = hermes_home / "memory"
    result = _run_harness_subprocess(
        "--json", hermes_home=hermes_home, cases_path=admitted_cases_path
    )

    assert result.returncode == 0
    assert not memory_dir.exists() or not any(memory_dir.rglob("*"))


def _run_harness_subprocess(
    *args: str,
    hermes_home: Path | None = None,
    cases_path: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{REPO_ROOT / 'src'}:{REPO_ROOT}"
    if hermes_home is not None:
        env["HERMES_HOME"] = str(hermes_home)
    return subprocess.run(
        [
            sys.executable,
            "scripts/run_active_context_quality_harness.py",
            *(["--cases", str(cases_path)] if cases_path is not None else []),
            *args,
        ],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
