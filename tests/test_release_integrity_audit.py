from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

from hermes_memory_fabric.release_integrity_audit import (
    release_integrity_audit_to_json,
    run_release_integrity_audit,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_release_integrity_audit_passes():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert result["version"] == "2.48.0"
    assert result["audit_status"] == "pass"
    assert result["release_chain_status"] == "pass"
    assert result["pyproject_version"] == "2.48.0"


def test_release_integrity_expected_tags_are_present():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert result["expected_tags_present"] is True
    assert result["missing_tags"] == []


def test_release_integrity_expected_files_are_present():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert result["expected_files_present"] is True
    assert result["missing_files"] == []


def test_release_integrity_provider_tools_are_empty():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert result["provider_tools"] == []
    assert result["provider_tools_empty"] is True


def test_release_integrity_authority_contract_safety_remains_true():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert result["authority_contract_status"] == "ready"
    assert result["authority_contract_safe"] is True


def test_release_integrity_skill_fabric_safety_remains_true():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert result["skill_fabric_verify_status"] == "pass"
    assert result["skill_fabric_safe"] is True
    assert "registry.json" in result["skill_fabric_files"]
    assert "locks/skills.lock.json" in result["skill_fabric_files"]
    assert "audit/skill_operation_ledger.jsonl" in result["skill_fabric_files"]


def test_release_integrity_simulation_safety_remains_true():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert result["simulation_status"] == "pass"
    assert result["simulation_safe"] is True
    assert result["simulation_used_network"] is False
    assert result["simulation_used_local_archive"] is True


def test_release_integrity_proposal_pack_safety_remains_true():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert result["proposal_pack_status"] == "ready"
    assert result["proposal_pack_safe"] is True
    assert result["proposal_pack_entry_count"] > 0
    assert result["proposal_pack_rejected_count"] > 0
    assert result["proposal_pack_risk_note_count"] > 0


def test_release_integrity_review_gate_safety_remains_true():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert result["review_gate_status"] == "ready"
    assert result["review_gate_safe"] is True
    assert result["review_gate_decision_count"] > 0
    assert result["review_gate_approve_candidate_count"] > 0
    assert result["review_gate_reject_locked_count"] > 0
    assert result["review_gate_risk_note_only_count"] > 0


def test_release_integrity_approval_request_safety_remains_true():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert result["approval_request_status"] == "ready"
    assert result["approval_request_safe"] is True
    assert result["approval_request_count"] == 15
    assert result["blocked_decision_count"] == 3


def test_release_integrity_unsafe_source_hits_are_empty():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert result["unsafe_source_hits"] == []
    assert result["no_network_surface"] is True
    assert result["no_hermes_memory_write"] is True
    assert result["no_github_write"] is True
    assert result["no_composio_execution"] is True
    assert result["modifies_hermes_agent"] is False


def test_release_integrity_report_is_json_serializable():
    result = run_release_integrity_audit(PROJECT_ROOT)

    payload = release_integrity_audit_to_json(result)
    decoded = json.loads(payload)

    assert decoded["audit_status"] == "pass"
    assert decoded["unsafe_source_hits"] == []


def test_release_integrity_smoke_script_exits_zero():
    completed = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "smoke_release_integrity_audit.py")],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert completed.stdout == "release_integrity_audit=passed\n"
    assert completed.stderr == ""


def test_release_integrity_openclaw_audit_review_safety_remains_true():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert result["openclaw_audit_review_status"] == "missing_audit_log"
    assert result["openclaw_audit_review_safe"] is True


def test_release_integrity_openclaw_audit_review_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert result["openclaw_audit_review_smoke_status"] == "pass"
    assert result["openclaw_audit_review_smoke_safe"] is True


def test_release_integrity_closed_loop_evidence_validation_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert result["closed_loop_evidence_validation_smoke_status"] == "pass"
    assert result["closed_loop_evidence_validation_smoke_safe"] is True


def test_release_integrity_governed_memory_proposal_from_evidence_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert result["governed_memory_proposal_from_evidence_smoke_status"] == "pass"
    assert result["governed_memory_proposal_from_evidence_smoke_safe"] is True


def test_release_integrity_governed_memory_proposal_review_gate_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert result["governed_memory_proposal_review_gate_smoke_status"] == "pass"
    assert result["governed_memory_proposal_review_gate_smoke_safe"] is True


def test_release_integrity_governed_approval_request_preparation_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert result["governed_approval_request_preparation_smoke_status"] == "pass"
    assert result["governed_approval_request_preparation_smoke_safe"] is True


def test_release_integrity_governed_approval_request_dry_run_envelope_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert result["governed_approval_request_dry_run_envelope_smoke_status"] == "pass"
    assert result["governed_approval_request_dry_run_envelope_smoke_safe"] is True


def test_release_integrity_governed_approval_request_dry_run_envelope_validation_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result["governed_approval_request_dry_run_envelope_validation_smoke_status"]
        == "pass"
    )
    assert result["governed_approval_request_dry_run_envelope_validation_smoke_safe"] is True


def test_release_integrity_governed_human_operator_decision_packet_dry_run_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result["governed_human_operator_decision_packet_dry_run_smoke_status"]
        == "pass"
    )
    assert result["governed_human_operator_decision_packet_dry_run_smoke_safe"] is True


def test_release_integrity_governed_human_operator_decision_packet_validation_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result["governed_human_operator_decision_packet_validation_smoke_status"]
        == "pass"
    )
    assert result["governed_human_operator_decision_packet_validation_smoke_safe"] is True


def test_release_integrity_governed_star_dome_chain_closure_audit_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert result["governed_star_dome_chain_closure_audit_smoke_status"] == "pass"
    assert result["governed_star_dome_chain_closure_audit_smoke_safe"] is True


def test_release_integrity_governed_star_dome_closure_boundary_manifest_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert result["governed_star_dome_closure_boundary_manifest_smoke_status"] == "pass"
    assert result["governed_star_dome_closure_boundary_manifest_smoke_safe"] is True


def test_release_integrity_governed_star_hub_preflight_boundary_analysis_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert result["governed_star_hub_preflight_boundary_analysis_smoke_status"] == "pass"
    assert result["governed_star_hub_preflight_boundary_analysis_smoke_safe"] is True


def test_release_integrity_governed_star_hub_scheduling_design_boundary_proposal_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result["governed_star_hub_scheduling_design_boundary_proposal_smoke_status"]
        == "pass"
    )
    assert (
        result["governed_star_hub_scheduling_design_boundary_proposal_smoke_safe"]
        is True
    )


def test_release_integrity_governed_star_hub_scheduling_design_boundary_review_gate_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result["governed_star_hub_scheduling_design_boundary_review_gate_smoke_status"]
        == "pass"
    )
    assert (
        result["governed_star_hub_scheduling_design_boundary_review_gate_smoke_safe"]
        is True
    )


def test_release_integrity_governed_star_hub_scheduling_dry_run_plan_boundary_proposal_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result[
            "governed_star_hub_scheduling_dry_run_plan_boundary_proposal_smoke_status"
        ]
        == "pass"
    )
    assert (
        result[
            "governed_star_hub_scheduling_dry_run_plan_boundary_proposal_smoke_safe"
        ]
        is True
    )


def test_release_integrity_governed_star_hub_scheduling_dry_run_plan_boundary_review_gate_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result[
            "governed_star_hub_scheduling_dry_run_plan_boundary_review_gate_smoke_status"
        ]
        == "pass"
    )
    assert (
        result[
            "governed_star_hub_scheduling_dry_run_plan_boundary_review_gate_smoke_safe"
        ]
        is True
    )


def test_release_integrity_governed_star_hub_scheduling_dry_run_execution_boundary_proposal_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result[
            "governed_star_hub_scheduling_dry_run_execution_boundary_proposal_smoke_status"
        ]
        == "pass"
    )
    assert (
        result[
            "governed_star_hub_scheduling_dry_run_execution_boundary_proposal_smoke_safe"
        ]
        is True
    )


def test_release_integrity_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result[
            "governed_star_hub_scheduling_dry_run_execution_boundary_review_gate_smoke_status"
        ]
        == "pass"
    )
    assert (
        result[
            "governed_star_hub_scheduling_dry_run_execution_boundary_review_gate_smoke_safe"
        ]
        is True
    )


def test_release_integrity_governed_star_hub_chain_closure_audit_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert result["governed_star_hub_chain_closure_audit_smoke_status"] == "pass"
    assert result["governed_star_hub_chain_closure_audit_smoke_safe"] is True


def test_release_integrity_governed_star_hub_closure_boundary_manifest_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result["governed_star_hub_closure_boundary_manifest_smoke_status"] == "pass"
    )
    assert result["governed_star_hub_closure_boundary_manifest_smoke_safe"] is True


def test_release_integrity_governed_star_law_preflight_boundary_analysis_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result["governed_star_law_preflight_boundary_analysis_smoke_status"] == "pass"
    )
    assert result["governed_star_law_preflight_boundary_analysis_smoke_safe"] is True


def test_release_integrity_governed_star_law_design_boundary_proposal_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result["governed_star_law_design_boundary_proposal_smoke_status"] == "pass"
    )
    assert result["governed_star_law_design_boundary_proposal_smoke_safe"] is True


def test_release_integrity_governed_star_law_design_boundary_review_gate_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result["governed_star_law_design_boundary_review_gate_smoke_status"] == "pass"
    )
    assert result["governed_star_law_design_boundary_review_gate_smoke_safe"] is True


def test_release_integrity_governed_star_law_candidate_rule_set_boundary_proposal_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result[
            "governed_star_law_candidate_rule_set_boundary_proposal_smoke_status"
        ]
        == "pass"
    )
    assert (
        result["governed_star_law_candidate_rule_set_boundary_proposal_smoke_safe"]
        is True
    )


def test_release_integrity_governed_star_law_candidate_rule_set_boundary_review_gate_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result[
            "governed_star_law_candidate_rule_set_boundary_review_gate_smoke_status"
        ]
        == "pass"
    )
    assert (
        result["governed_star_law_candidate_rule_set_boundary_review_gate_smoke_safe"]
        is True
    )


def test_release_integrity_governed_star_law_candidate_rule_activation_boundary_proposal_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result[
            "governed_star_law_candidate_rule_activation_boundary_proposal_smoke_status"
        ]
        == "pass"
    )
    assert (
        result[
            "governed_star_law_candidate_rule_activation_boundary_proposal_smoke_safe"
        ]
        is True
    )


def test_release_integrity_governed_star_law_candidate_rule_activation_boundary_review_gate_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result[
            "governed_star_law_candidate_rule_activation_boundary_review_gate_smoke_status"
        ]
        == "pass"
    )
    assert (
        result[
            "governed_star_law_candidate_rule_activation_boundary_review_gate_smoke_safe"
        ]
        is True
    )


def test_release_integrity_governed_star_law_candidate_rule_enforcement_boundary_proposal_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result[
            "governed_star_law_candidate_rule_enforcement_boundary_proposal_smoke_status"
        ]
        == "pass"
    )
    assert (
        result[
            "governed_star_law_candidate_rule_enforcement_boundary_proposal_smoke_safe"
        ]
        is True
    )


def test_release_integrity_governed_star_law_candidate_rule_enforcement_boundary_review_gate_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result[
            "governed_star_law_candidate_rule_enforcement_boundary_review_gate_smoke_status"
        ]
        == "pass"
    )
    assert (
        result[
            "governed_star_law_candidate_rule_enforcement_boundary_review_gate_smoke_safe"
        ]
        is True
    )


def test_release_integrity_governed_star_law_candidate_rule_violation_observation_boundary_proposal_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result[
            "governed_star_law_candidate_rule_violation_observation_boundary_proposal_smoke_status"
        ]
        == "pass"
    )
    assert (
        result[
            "governed_star_law_candidate_rule_violation_observation_boundary_proposal_smoke_safe"
        ]
        is True
    )


def test_release_integrity_governed_star_law_candidate_rule_violation_observation_boundary_review_gate_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result[
            "governed_star_law_candidate_rule_violation_observation_boundary_review_gate_smoke_status"
        ]
        == "pass"
    )
    assert (
        result[
            "governed_star_law_candidate_rule_violation_observation_boundary_review_gate_smoke_safe"
        ]
        is True
    )


def test_release_integrity_governed_star_law_candidate_rule_violation_response_boundary_proposal_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result[
            "governed_star_law_candidate_rule_violation_response_boundary_proposal_smoke_status"
        ]
        == "pass"
    )
    assert (
        result[
            "governed_star_law_candidate_rule_violation_response_boundary_proposal_smoke_safe"
        ]
        is True
    )


def test_release_integrity_governed_star_law_candidate_rule_violation_response_boundary_review_gate_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result[
            "governed_star_law_candidate_rule_violation_response_boundary_review_gate_smoke_status"
        ]
        == "pass"
    )
    assert (
        result[
            "governed_star_law_candidate_rule_violation_response_boundary_review_gate_smoke_safe"
        ]
        is True
    )


def test_release_integrity_governed_star_law_candidate_rule_violation_response_audit_boundary_proposal_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result[
            "governed_star_law_candidate_rule_violation_response_audit_boundary_proposal_smoke_status"
        ]
        == "pass"
    )
    assert (
        result[
            "governed_star_law_candidate_rule_violation_response_audit_boundary_proposal_smoke_safe"
        ]
        is True
    )


def test_release_integrity_governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result[
            "governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate_smoke_status"
        ]
        == "pass"
    )
    assert (
        result[
            "governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate_smoke_safe"
        ]
        is True
    )


def test_release_integrity_governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result[
            "governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_smoke_status"
        ]
        == "pass"
    )
    assert (
        result[
            "governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_smoke_safe"
        ]
        is True
    )


def test_release_integrity_governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result[
            "governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate_smoke_status"
        ]
        == "pass"
    )
    assert (
        result[
            "governed_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate_smoke_safe"
        ]
        is True
    )


def test_release_integrity_governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result[
            "governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal_smoke_status"
        ]
        == "pass"
    )
    assert (
        result[
            "governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_proposal_smoke_safe"
        ]
        is True
    )


def test_release_integrity_governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result[
            "governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate_smoke_status"
        ]
        == "pass"
    )
    assert (
        result[
            "governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate_smoke_safe"
        ]
        is True
    )


def test_release_integrity_governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result[
            "governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal_smoke_status"
        ]
        == "pass"
    )
    assert (
        result[
            "governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal_smoke_safe"
        ]
        is True
    )


def test_release_integrity_governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate_smoke_remains_safe():
    result = run_release_integrity_audit(PROJECT_ROOT)

    assert (
        result[
            "governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate_smoke_status"
        ]
        == "pass"
    )
    assert (
        result[
            "governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate_smoke_safe"
        ]
        is True
    )
