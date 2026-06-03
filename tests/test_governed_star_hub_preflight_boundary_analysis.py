from __future__ import annotations

import json

from hermes_memory_fabric.governed_star_hub_preflight_boundary_analysis import (
    build_governed_star_hub_preflight_boundary_analysis,
    governed_star_hub_preflight_boundary_analysis_to_json,
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
]


def _valid_manifest_report() -> dict[str, object]:
    return {
        "version": "2.18.0",
        "status": "boundary_manifest_ready",
        "read_only": True,
        "read_only_memory": True,
        "manifest_only": True,
        "boundary_manifest_only": True,
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
        "boundary_manifest_authorized": False,
        "star_dome_stage_boundary_manifested": True,
        "star_dome_final_closure_claimed": False,
        "star_hub_handoff_authorized": False,
        "star_hub_scheduling_authorized": False,
        "handoff_authorized": False,
        "closure_authorized": False,
        "human_decision_recorded": False,
        "approval_request_created": False,
        "approval_request_submitted": False,
        "approval_request_authorized": False,
        "approval_granted": False,
        "memory_write_authorized": False,
        "openclaw_execution_authorized": False,
        "civilization_core_complete_claimed": False,
        "civilization_core_layer_mapping": {
            "primary_layer": "星穹记忆",
            "supporting_layers": ["星界记忆", "星辰记忆", "星域记忆"],
        },
        "manifested_chain_versions": EXPECTED_CHAIN[:-1],
        "next_allowed_step": "v2.19.0 Star-Hub preflight boundary analysis",
        "blocking_reasons": [],
        "star_dome_stage_closure_statement": {
            "statement_status": "star_dome_stage_boundary_manifested_for_human_review_only",
            "star_dome_governance_chain_stage_ready_for_closure": True,
            "star_dome_final_closure_claimed": False,
            "civilization_core_complete_claimed": False,
            "star_hub_handoff_authorized": False,
            "star_hub_scheduling_authorized": False,
            "durable_memory_write_authorized": False,
            "memory_graph_mutation_authorized": False,
            "operation_ledger_creation_authorized": False,
            "openclaw_execution_authorized": False,
            "approval_authorized": False,
            "real_human_decision_recorded": False,
        },
        "non_authorization_boundary": {
            "boundary_manifest_ready_is_star_hub_scheduling_permission": False,
            "boundary_manifest_ready_is_star_hub_handoff_permission": False,
            "boundary_manifest_ready_is_civilization_core_completion": False,
        },
    }


def test_valid_manifest_report_creates_star_hub_preflight_boundary_analysis_ready():
    result = build_governed_star_hub_preflight_boundary_analysis(_valid_manifest_report())

    assert result["version"] == "2.19.0"
    assert result["status"] == "star_hub_preflight_boundary_analysis_ready"
    assert result["source_manifest_version"] == "2.18.0"
    assert all(check["passed"] is True for check in result["star_hub_preflight_checks"])
    assert result["blocking_reasons"] == []


def test_analyzed_chain_versions_exactly_match_v2_9_0_through_v2_18_0():
    result = build_governed_star_hub_preflight_boundary_analysis(_valid_manifest_report())

    assert result["analyzed_chain_versions"] == EXPECTED_CHAIN


def test_blocked_manifest_report_blocks_preflight_analysis():
    report = _valid_manifest_report()
    report["status"] = "blocked"
    report["blocking_reasons"] = ["source_blocked"]

    result = build_governed_star_hub_preflight_boundary_analysis(report)

    assert result["status"] == "blocked"
    assert result["source_star_dome_boundary_summary"]["source_boundary_status"] == "blocked"
    assert result["source_star_dome_boundary_summary"]["star_dome_stage_boundary_manifested"] is False
    assert result["blocking_reasons"]


def test_unsafe_authorization_flag_blocks_preflight_analysis():
    report = _valid_manifest_report()
    report["authorization_granted"] = True

    result = build_governed_star_hub_preflight_boundary_analysis(report)

    assert result["status"] == "blocked"


def test_star_hub_scheduling_authorization_claim_blocks_preflight_analysis():
    report = _valid_manifest_report()
    report["star_hub_scheduling_authorized"] = True

    result = build_governed_star_hub_preflight_boundary_analysis(report)

    assert result["status"] == "blocked"


def test_star_hub_handoff_authorization_claim_blocks_preflight_analysis():
    report = _valid_manifest_report()
    report["star_hub_handoff_authorized"] = True

    result = build_governed_star_hub_preflight_boundary_analysis(report)

    assert result["status"] == "blocked"


def test_memory_write_authorization_claim_blocks_preflight_analysis():
    report = _valid_manifest_report()
    report["memory_write_authorized"] = True

    result = build_governed_star_hub_preflight_boundary_analysis(report)

    assert result["status"] == "blocked"


def test_openclaw_execution_authorization_claim_blocks_preflight_analysis():
    report = _valid_manifest_report()
    report["openclaw_execution_authorized"] = True

    result = build_governed_star_hub_preflight_boundary_analysis(report)

    assert result["status"] == "blocked"


def test_approval_claim_blocks_preflight_analysis():
    report = _valid_manifest_report()
    report["approval_granted"] = True

    result = build_governed_star_hub_preflight_boundary_analysis(report)

    assert result["status"] == "blocked"


def test_civilization_core_completion_claim_blocks_preflight_analysis():
    report = _valid_manifest_report()
    report["civilization_core_complete_claimed"] = True

    result = build_governed_star_hub_preflight_boundary_analysis(report)

    assert result["status"] == "blocked"


def test_star_dome_final_closure_claim_blocks_preflight_analysis():
    report = _valid_manifest_report()
    report["star_dome_final_closure_claimed"] = True

    result = build_governed_star_hub_preflight_boundary_analysis(report)

    assert result["status"] == "blocked"


def test_malformed_manifested_chain_versions_blocks_preflight_analysis():
    report = _valid_manifest_report()
    report["manifested_chain_versions"] = ["v2.9.0", "v2.18.0"]

    result = build_governed_star_hub_preflight_boundary_analysis(report)

    assert result["status"] == "blocked"
    assert result["analyzed_chain_versions"] == EXPECTED_CHAIN


def test_sensitive_field_names_and_values_are_not_leaked_in_serialized_output():
    report = _valid_manifest_report()
    report["approval_phrase"] = "approve-secret-material"
    report["nested"] = {
        "stdout_tail": "hidden-tail",
        "token": "hidden-token",
        "safe": [{"password": "hidden-password"}],
    }

    result = build_governed_star_hub_preflight_boundary_analysis(report)
    payload = governed_star_hub_preflight_boundary_analysis_to_json(result)

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


def test_analysis_does_not_authorize_star_hub_design():
    result = build_governed_star_hub_preflight_boundary_analysis(_valid_manifest_report())

    assert result["star_hub_design_authorized"] is False


def test_analysis_does_not_authorize_star_hub_scheduling():
    result = build_governed_star_hub_preflight_boundary_analysis(_valid_manifest_report())

    assert result["star_hub_scheduling_authorized"] is False
    assert result["scheduling_performed"] is False


def test_analysis_does_not_authorize_handoff():
    result = build_governed_star_hub_preflight_boundary_analysis(_valid_manifest_report())

    assert result["handoff_authorized"] is False
    assert result["star_hub_handoff_authorized"] is False


def test_analysis_does_not_create_approval_request():
    result = build_governed_star_hub_preflight_boundary_analysis(_valid_manifest_report())

    assert result["approval_request_created"] is False
    assert result["would_create_approval_request"] is False


def test_analysis_does_not_submit_approval_request():
    result = build_governed_star_hub_preflight_boundary_analysis(_valid_manifest_report())

    assert result["approval_request_submitted"] is False
    assert result["would_submit_approval_request"] is False


def test_analysis_does_not_execute_approval_request():
    result = build_governed_star_hub_preflight_boundary_analysis(_valid_manifest_report())

    assert result["would_execute_approval_request"] is False


def test_analysis_does_not_record_human_decision():
    result = build_governed_star_hub_preflight_boundary_analysis(_valid_manifest_report())

    assert result["human_decision_recorded"] is False
    assert result["would_record_human_decision"] is False


def test_analysis_does_not_authorize_approval():
    result = build_governed_star_hub_preflight_boundary_analysis(_valid_manifest_report())

    assert result["approval_granted"] is False
    assert result["would_grant_approval"] is False


def test_analysis_does_not_authorize_memory_write():
    result = build_governed_star_hub_preflight_boundary_analysis(_valid_manifest_report())

    assert result["memory_write_authorized"] is False
    assert result["would_write_durable_memory"] is False


def test_analysis_does_not_authorize_openclaw_execution():
    result = build_governed_star_hub_preflight_boundary_analysis(_valid_manifest_report())

    assert result["openclaw_execution_authorized"] is False
    assert result["invokes_openclaw"] is False


def test_layer_mapping_is_correct():
    result = build_governed_star_hub_preflight_boundary_analysis(_valid_manifest_report())
    mapping = result["civilization_core_layer_mapping"]

    assert mapping["primary_layer"] == "星枢记忆"
    assert mapping["primary_layer_status"] == "preflight boundary analysis only, not scheduling"
    assert "星穹记忆" in mapping["supporting_layers"]
    assert "星域记忆" in mapping["supporting_layers"]
    assert "星界记忆" in mapping["supporting_layers"]
    assert "星辰记忆" in mapping["supporting_layers"]
    assert mapping["direction"] == (
        "Star-Dome closure boundary manifest -> Star-Hub preflight boundary analysis"
    )


def test_next_allowed_step_is_v2_20_star_hub_scheduling_design_boundary_proposal():
    result = build_governed_star_hub_preflight_boundary_analysis(_valid_manifest_report())

    assert result["next_allowed_step"] == (
        "v2.20.0 Star-Hub scheduling design boundary proposal"
    )
