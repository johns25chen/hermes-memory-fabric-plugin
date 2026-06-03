from __future__ import annotations

import json

from hermes_memory_fabric.governed_star_hub_scheduling_design_boundary_proposal import (
    build_governed_star_hub_scheduling_design_boundary_proposal,
    governed_star_hub_scheduling_design_boundary_proposal_to_json,
)


EXPECTED_CHAIN = [
    "v2.9.0",
    "v2.10.0",
    "v2.11.0",
    "v2.12.0",
    "v2.13.0",
    "v2.14.0",
    "v2.15.0",
    "v2.16.0",
    "v2.17.0",
    "v2.18.0",
    "v2.19.0",
]

SOURCE_CHAIN = EXPECTED_CHAIN[:-1]


def _valid_preflight_report() -> dict[str, object]:
    return {
        "version": "2.19.0",
        "status": "star_hub_preflight_boundary_analysis_ready",
        "read_only": True,
        "read_only_memory": True,
        "analysis_only": True,
        "preflight_only": True,
        "boundary_analysis_only": True,
        "star_hub_preflight_only": True,
        "would_mutate_memory": False,
        "writes_files": False,
        "invokes_openclaw": False,
        "would_call_github_api": False,
        "would_merge_pr": False,
        "would_create_tag": False,
        "would_write_durable_memory": False,
        "would_mutate_memory_graph": False,
        "would_create_operation_ledger_entry": False,
        "would_create_approval_request": False,
        "would_submit_approval_request": False,
        "would_execute_approval_request": False,
        "would_record_human_decision": False,
        "would_grant_approval": False,
        "authorization_granted": False,
        "preflight_analysis_authorized": False,
        "star_hub_design_authorized": False,
        "star_hub_handoff_authorized": False,
        "star_hub_scheduling_authorized": False,
        "scheduling_performed": False,
        "handoff_authorized": False,
        "human_decision_recorded": False,
        "approval_request_created": False,
        "approval_request_submitted": False,
        "approval_request_authorized": False,
        "approval_granted": False,
        "memory_write_authorized": False,
        "openclaw_execution_authorized": False,
        "civilization_core_complete_claimed": False,
        "star_dome_final_closure_claimed": False,
        "civilization_core_layer_mapping": {
            "primary_layer": "星枢记忆",
            "primary_layer_status": "preflight boundary analysis only, not scheduling",
            "supporting_layers": ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"],
        },
        "analyzed_chain_versions": SOURCE_CHAIN,
        "next_allowed_step": "v2.20.0 Star-Hub scheduling design boundary proposal",
        "blocking_reasons": [],
        "non_authorization_boundary": {
            "star_hub_preflight_boundary_analysis_ready_is_star_hub_scheduling": False,
            "star_hub_preflight_boundary_analysis_ready_is_star_hub_handoff": False,
            "star_hub_preflight_boundary_analysis_ready_is_authorization": False,
            "star_hub_preflight_boundary_analysis_ready_is_civilization_core_completion": False,
        },
    }


def test_valid_preflight_report_creates_star_hub_scheduling_design_boundary_proposal_ready():
    result = build_governed_star_hub_scheduling_design_boundary_proposal(
        _valid_preflight_report()
    )

    assert result["version"] == "2.20.0"
    assert result["status"] == "star_hub_scheduling_design_boundary_proposal_ready"
    assert result["source_preflight_version"] == "2.19.0"
    assert all(check["passed"] is True for check in result["proposal_checks"])
    assert result["blocking_reasons"] == []
    proposal = result["proposed_star_hub_design_boundary"]
    assert proposal["proposal_status"] == (
        "star_hub_scheduling_design_boundary_proposed_for_human_review_only"
    )
    assert proposal["boundary_type"] == "star_hub_scheduling_design_boundary_proposal"
    assert proposal["star_hub_design_boundary_proposed"] is True


def test_proposed_chain_versions_exactly_match_v2_9_0_through_v2_19_0():
    result = build_governed_star_hub_scheduling_design_boundary_proposal(
        _valid_preflight_report()
    )

    assert result["proposed_chain_versions"] == EXPECTED_CHAIN


def test_blocked_preflight_report_blocks_proposal():
    report = _valid_preflight_report()
    report["status"] = "blocked"
    report["blocking_reasons"] = ["source_blocked"]

    result = build_governed_star_hub_scheduling_design_boundary_proposal(report)

    assert result["status"] == "blocked"
    assert result["proposed_chain_versions"] == EXPECTED_CHAIN
    assert result["proposed_star_hub_design_boundary"]["star_hub_design_boundary_proposed"] is False
    assert result["blocking_reasons"]
    assert result["required_human_actions"]


def test_unsafe_authorization_flag_blocks_proposal():
    report = _valid_preflight_report()
    report["authorization_granted"] = True

    result = build_governed_star_hub_scheduling_design_boundary_proposal(report)

    assert result["status"] == "blocked"


def test_star_hub_scheduling_authorization_claim_blocks_proposal():
    report = _valid_preflight_report()
    report["star_hub_scheduling_authorized"] = True

    result = build_governed_star_hub_scheduling_design_boundary_proposal(report)

    assert result["status"] == "blocked"


def test_star_hub_scheduling_performed_claim_blocks_proposal():
    report = _valid_preflight_report()
    report["scheduling_performed"] = True

    result = build_governed_star_hub_scheduling_design_boundary_proposal(report)

    assert result["status"] == "blocked"


def test_star_hub_handoff_authorization_claim_blocks_proposal():
    report = _valid_preflight_report()
    report["star_hub_handoff_authorized"] = True

    result = build_governed_star_hub_scheduling_design_boundary_proposal(report)

    assert result["status"] == "blocked"


def test_memory_write_authorization_claim_blocks_proposal():
    report = _valid_preflight_report()
    report["memory_write_authorized"] = True

    result = build_governed_star_hub_scheduling_design_boundary_proposal(report)

    assert result["status"] == "blocked"


def test_openclaw_execution_authorization_claim_blocks_proposal():
    report = _valid_preflight_report()
    report["openclaw_execution_authorized"] = True

    result = build_governed_star_hub_scheduling_design_boundary_proposal(report)

    assert result["status"] == "blocked"


def test_approval_claim_blocks_proposal():
    report = _valid_preflight_report()
    report["approval_granted"] = True

    result = build_governed_star_hub_scheduling_design_boundary_proposal(report)

    assert result["status"] == "blocked"


def test_civilization_core_completion_claim_blocks_proposal():
    report = _valid_preflight_report()
    report["civilization_core_complete_claimed"] = True

    result = build_governed_star_hub_scheduling_design_boundary_proposal(report)

    assert result["status"] == "blocked"


def test_star_dome_final_closure_claim_blocks_proposal():
    report = _valid_preflight_report()
    report["star_dome_final_closure_claimed"] = True

    result = build_governed_star_hub_scheduling_design_boundary_proposal(report)

    assert result["status"] == "blocked"


def test_malformed_analyzed_chain_versions_blocks_proposal():
    report = _valid_preflight_report()
    report["analyzed_chain_versions"] = ["v2.9.0", "v2.19.0"]

    result = build_governed_star_hub_scheduling_design_boundary_proposal(report)

    assert result["status"] == "blocked"
    assert result["proposed_chain_versions"] == EXPECTED_CHAIN


def test_sensitive_field_names_and_values_are_not_leaked_in_serialized_output():
    report = _valid_preflight_report()
    report["approval_phrase"] = "approve-secret-material"
    report["nested"] = {
        "stdout_tail": "hidden-tail",
        "token": "hidden-token",
        "safe": [{"password": "hidden-password"}],
    }

    result = build_governed_star_hub_scheduling_design_boundary_proposal(report)
    payload = governed_star_hub_scheduling_design_boundary_proposal_to_json(result)

    assert result["sensitive_fields_omitted"] is True
    assert "approval_phrase" not in payload
    assert "stdout_tail" not in payload
    assert "token" not in payload
    assert "password" not in payload
    assert "approve-secret-material" not in payload
    assert "hidden-tail" not in payload
    assert "hidden-token" not in payload
    assert "hidden-password" not in payload
    json.loads(payload)


def test_proposal_does_not_authorize_star_hub_design():
    result = build_governed_star_hub_scheduling_design_boundary_proposal(
        _valid_preflight_report()
    )

    assert result["design_boundary_authorized"] is False
    assert result["proposed_star_hub_design_boundary"]["star_hub_design_authorized"] is False


def test_proposal_does_not_authorize_star_hub_scheduling():
    result = build_governed_star_hub_scheduling_design_boundary_proposal(
        _valid_preflight_report()
    )

    assert result["star_hub_scheduling_authorized"] is False
    assert result["proposed_star_hub_design_boundary"]["star_hub_scheduling_authorized"] is False


def test_proposal_does_not_perform_scheduling():
    result = build_governed_star_hub_scheduling_design_boundary_proposal(
        _valid_preflight_report()
    )

    assert result["scheduling_performed"] is False
    assert result["would_schedule_anything"] is False
    assert result["proposed_star_hub_design_boundary"]["star_hub_scheduling_executed"] is False


def test_proposal_does_not_authorize_handoff():
    result = build_governed_star_hub_scheduling_design_boundary_proposal(
        _valid_preflight_report()
    )

    assert result["handoff_authorized"] is False
    assert result["star_hub_handoff_authorized"] is False


def test_proposal_does_not_create_approval_request():
    result = build_governed_star_hub_scheduling_design_boundary_proposal(
        _valid_preflight_report()
    )

    assert result["approval_request_created"] is False
    assert result["would_create_approval_request"] is False


def test_proposal_does_not_submit_approval_request():
    result = build_governed_star_hub_scheduling_design_boundary_proposal(
        _valid_preflight_report()
    )

    assert result["approval_request_submitted"] is False
    assert result["would_submit_approval_request"] is False


def test_proposal_does_not_execute_approval_request():
    result = build_governed_star_hub_scheduling_design_boundary_proposal(
        _valid_preflight_report()
    )

    assert result["would_execute_approval_request"] is False


def test_proposal_does_not_record_human_decision():
    result = build_governed_star_hub_scheduling_design_boundary_proposal(
        _valid_preflight_report()
    )

    assert result["human_decision_recorded"] is False
    assert result["would_record_human_decision"] is False


def test_proposal_does_not_authorize_approval():
    result = build_governed_star_hub_scheduling_design_boundary_proposal(
        _valid_preflight_report()
    )

    assert result["approval_granted"] is False
    assert result["would_grant_approval"] is False


def test_proposal_does_not_authorize_memory_write():
    result = build_governed_star_hub_scheduling_design_boundary_proposal(
        _valid_preflight_report()
    )

    assert result["memory_write_authorized"] is False
    assert result["would_write_durable_memory"] is False


def test_proposal_does_not_authorize_openclaw_execution():
    result = build_governed_star_hub_scheduling_design_boundary_proposal(
        _valid_preflight_report()
    )

    assert result["openclaw_execution_authorized"] is False
    assert result["invokes_openclaw"] is False


def test_layer_mapping_is_correct():
    result = build_governed_star_hub_scheduling_design_boundary_proposal(
        _valid_preflight_report()
    )
    mapping = result["civilization_core_layer_mapping"]

    assert mapping["primary_layer"] == "星枢记忆"
    assert mapping["primary_layer_status"] == (
        "scheduling design boundary proposal only, not scheduling"
    )
    assert "星穹记忆" in mapping["supporting_layers"]
    assert "星域记忆" in mapping["supporting_layers"]
    assert "星界记忆" in mapping["supporting_layers"]
    assert "星辰记忆" in mapping["supporting_layers"]
    assert mapping["direction"] == (
        "Star-Hub preflight boundary analysis -> Star-Hub scheduling design boundary proposal"
    )


def test_next_allowed_step_is_v2_21_star_hub_scheduling_design_boundary_review_gate():
    result = build_governed_star_hub_scheduling_design_boundary_proposal(
        _valid_preflight_report()
    )

    assert result["next_allowed_step"] == (
        "v2.21.0 Star-Hub scheduling design boundary review gate"
    )
    assert result["proposed_star_hub_design_boundary"]["next_allowed_step"] == (
        "v2.21.0 Star-Hub scheduling design boundary review gate"
    )
