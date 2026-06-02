from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from hermes_memory_fabric.governed_memory_approval_request_dry_run import (
    governed_memory_approval_request_to_json,
    build_governed_memory_approval_request_dry_run,
)
from hermes_memory_fabric.governed_memory_proposal_review_gate_dry_run import (
    run_governed_memory_proposal_review_gate_dry_run,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROPOSAL_PATH = PROJECT_ROOT / "docs" / "CIVILIZATION_CORE_VIDEO_AI_SKILLS_MEMORY_PROPOSAL.md"
SMOKE_SCRIPT = PROJECT_ROOT / "scripts" / "smoke_governed_memory_approval_request_dry_run.py"


def _result() -> dict[str, object]:
    return build_governed_memory_approval_request_dry_run(PROPOSAL_PATH)


def test_approval_request_status_ready_and_expected_counts():
    result = _result()

    assert result["version"] == "2.6.0"
    assert result["approval_request_status"] == "ready"
    assert result["review_gate_status"] == "ready"
    assert result["approval_request_count"] == 15
    assert result["approve_candidate_count"] == 15
    assert result["blocked_decision_count"] == 3
    assert result["approval_request_count"] == result["approve_candidate_count"]


def test_only_approve_candidate_decisions_become_approval_requests():
    result = _result()
    review_gate = run_governed_memory_proposal_review_gate_dry_run(PROPOSAL_PATH)
    request_decision_ids = {
        request["decision_id"] for request in result["approval_requests"]
    }
    approve_candidate_ids = {
        decision["decision_id"] for decision in review_gate["approve_candidates"]
    }

    assert request_decision_ids == approve_candidate_ids
    assert all(
        request["request_status"] == "pending_human_approval"
        and request["requested_action"] == "authorize_future_memory_write_plan_candidate"
        for request in result["approval_requests"]
    )


def test_reject_locked_decisions_do_not_become_approval_requests():
    result = _result()
    request_decision_ids = {
        request["decision_id"] for request in result["approval_requests"]
    }
    reject_locked = [
        decision
        for decision in result["blocked_decisions"]
        if decision["review_decision"] == "reject_locked"
    ]

    assert reject_locked
    assert all(decision["decision_id"] not in request_decision_ids for decision in reject_locked)


def test_risk_note_only_decisions_do_not_become_approval_requests():
    result = _result()
    request_decision_ids = {
        request["decision_id"] for request in result["approval_requests"]
    }
    risk_note_only = [
        decision
        for decision in result["blocked_decisions"]
        if decision["review_decision"] == "risk_note_only"
    ]

    assert risk_note_only
    assert all(decision["decision_id"] not in request_decision_ids for decision in risk_note_only)


def test_approval_requests_preserve_source_fields_and_have_stable_ids():
    first = _result()
    second = _result()

    assert first == second
    for request in first["approval_requests"]:
        assert request["approval_request_id"].startswith("gmar-dry-run-")
        assert request["decision_id"]
        assert request["proposal_id"]
        assert request["entry_key"]
        assert request["target_surface"]
        assert request["review_reason"]


def test_no_approval_token_is_issued_and_no_usable_token_created():
    result = _result()

    assert result["issues_approval_token"] is False
    assert result["approval_token_issued"] is False
    assert result["approval_token_value"] is None
    assert result["creates_usable_token"] is False
    for request in result["approval_requests"]:
        assert request["issues_approval_token"] is False
        assert request["approval_token_issued"] is False
        assert request["approval_token_value"] is None
        assert request["creates_usable_token"] is False


def test_all_write_flags_are_false_and_provider_tools_empty():
    result = _result()

    assert result["writes_memory"] is False
    assert result["writes_graph"] is False
    assert result["writes_operation_ledger"] is False
    assert result["writes_config"] is False
    assert result["writes_sqlite"] is False
    assert result["invokes_real_executor"] is False
    assert result["creates_real_memory_write_proposal"] is False
    assert result["creates_real_operation_ledger_entry"] is False
    assert result["modifies_hermes_agent"] is False
    assert result["no_network_surface"] is True
    assert result["provider_tools"] == []
    for request in result["approval_requests"]:
        assert request["writes_memory"] is False
        assert request["writes_graph"] is False
        assert request["writes_operation_ledger"] is False
        assert request["invokes_real_executor"] is False
        assert request["provider_tools"] == []


def test_report_is_json_serializable():
    result = _result()

    payload = governed_memory_approval_request_to_json(result)
    decoded = json.loads(payload)

    assert decoded["approval_request_status"] == "ready"
    assert decoded["approval_requests"] == result["approval_requests"]


def test_smoke_script_exits_zero():
    completed = subprocess.run(
        [sys.executable, str(SMOKE_SCRIPT)],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert completed.stdout == "governed_memory_approval_request_dry_run=passed\n"
    assert completed.stderr == ""
