from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from hermes_memory_fabric.governed_memory_proposal_review_gate_dry_run import (
    governed_memory_proposal_review_gate_to_json,
    run_governed_memory_proposal_review_gate_dry_run,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROPOSAL_PATH = PROJECT_ROOT / "docs" / "CIVILIZATION_CORE_VIDEO_AI_SKILLS_MEMORY_PROPOSAL.md"
SMOKE_SCRIPT = PROJECT_ROOT / "scripts" / "smoke_governed_memory_proposal_review_gate_dry_run.py"


def _result() -> dict[str, object]:
    return run_governed_memory_proposal_review_gate_dry_run(PROPOSAL_PATH)


def _decision(result: dict[str, object], entry_key: str) -> dict[str, object]:
    return next(decision for decision in result["decisions"] if decision["entry_key"] == entry_key)


def _assert_no_write_or_token_flags(value: dict[str, object]) -> None:
    assert value["writes_memory"] is False
    assert value["writes_graph"] is False
    assert value["writes_operation_ledger"] is False
    assert value["invokes_real_executor"] is False
    assert value["provider_tools"] == []
    assert value["issues_approval_token"] is False


def test_review_gate_status_ready_and_source_digest_stable():
    first = _result()
    second = _result()

    assert first["version"] == "2.5.0"
    assert first["review_gate_status"] == "ready"
    assert first["pack_status"] == "ready"
    assert first["source_sha256"]
    assert first["source_sha256"] == second["source_sha256"]
    assert first == second


def test_decision_counts_match_entries_and_safe_expected_counts_are_nonzero():
    result = _result()

    assert result["entry_count"] > 0
    assert result["decision_count"] == result["entry_count"]
    assert result["approve_candidate_count"] > 0
    assert result["reject_locked_count"] > 0
    assert result["risk_note_only_count"] > 0
    assert result["defer_for_human_review_count"] == 0


def test_proposed_durable_surface_entries_become_approve_candidates():
    result = _result()
    durable_surfaces = {
        "long_term_memory",
        "short_term_memory",
        "operation_ledger",
        "knowledge_surface",
    }
    proposed = [
        decision for decision in result["decisions"]
        if decision["source_status"] == "proposed"
        and decision["source_target_surface"] in durable_surfaces
    ]

    assert proposed
    assert all(decision["review_decision"] == "approve_candidate" for decision in proposed)
    assert all(decision in result["approve_candidates"] for decision in proposed)


def test_rejected_entries_become_reject_locked():
    result = _result()
    rejected = [decision for decision in result["decisions"] if decision["source_status"] == "rejected"]

    assert rejected
    assert all(decision["review_decision"] == "reject_locked" for decision in rejected)
    assert all(decision in result["reject_locked"] for decision in rejected)


def test_risk_notes_become_risk_note_only():
    result = _result()
    risk_notes = [decision for decision in result["decisions"] if decision["source_status"] == "risk_note"]

    assert risk_notes
    assert all(decision["review_decision"] == "risk_note_only" for decision in risk_notes)
    assert all(decision in result["risk_note_only"] for decision in risk_notes)


def test_temporary_command_authorizations_are_locked_rejected():
    result = _result()
    decision = _decision(result, "temporary_command_authorizations")

    assert decision["review_decision"] == "reject_locked"
    assert "temporary_command_authorization" in decision["non_durable_reasons"]
    assert decision["must_not_become_durable_memory"] is True


def test_api_key_or_secret_risk_is_not_approved():
    result = _result()
    sensitive = [
        decision for decision in result["decisions"]
        if "api_key_or_secret" in decision["non_durable_reasons"]
        or "raw_credentials" in decision["non_durable_reasons"]
    ]

    assert sensitive
    assert all(decision["review_decision"] != "approve_candidate" for decision in sensitive)
    assert all(
        decision["review_decision"] in {"reject_locked", "risk_note_only"} for decision in sensitive
    )


def test_provider_tools_empty_and_approval_token_disabled():
    result = _result()

    assert result["provider_tools"] == []
    assert result["issues_approval_token"] is False
    assert result["approval_token_issued"] is False
    assert result["approval_token_value"] is None
    assert result["creates_usable_token"] is False


def test_all_report_and_decision_write_flags_are_false():
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
    for decision in result["decisions"]:
        _assert_no_write_or_token_flags(decision)


def test_report_is_json_serializable():
    result = _result()

    payload = governed_memory_proposal_review_gate_to_json(result)
    decoded = json.loads(payload)

    assert decoded["review_gate_status"] == "ready"
    assert decoded["decisions"] == result["decisions"]


def test_smoke_script_exits_zero():
    completed = subprocess.run(
        [sys.executable, str(SMOKE_SCRIPT)],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert completed.stdout == "governed_memory_proposal_review_gate_dry_run=passed\n"
    assert completed.stderr == ""
