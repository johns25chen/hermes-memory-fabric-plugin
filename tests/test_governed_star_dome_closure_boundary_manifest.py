from __future__ import annotations

import json

from hermes_memory_fabric.governed_star_dome_closure_boundary_manifest import (
    build_governed_star_dome_closure_boundary_manifest,
    governed_star_dome_closure_boundary_manifest_to_json,
)


SOURCE_CHAIN = [
    "v2.9.0",
    "v2.10.0",
    "v2.11.0",
    "v2.12.0",
    "v2.13.0",
    "v2.14.0",
    "v2.15.0",
    "v2.16.0",
]

MANIFESTED_CHAIN = [
    *SOURCE_CHAIN,
    "v2.17.0",
]


def _valid_audit_report() -> dict[str, object]:
    return {
        "version": "2.17.0",
        "status": "chain_closure_audit_passed",
        "read_only": True,
        "read_only_memory": True,
        "audit_only": True,
        "closure_audit_only": True,
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
        "closure_authorized": False,
        "star_dome_closed": False,
        "handoff_authorized": False,
        "human_decision_recorded": False,
        "approval_request_created": False,
        "approval_request_submitted": False,
        "approval_request_authorized": False,
        "approval_granted": False,
        "memory_write_authorized": False,
        "openclaw_execution_authorized": False,
        "civilization_core_layer_mapping": {
            "primary_layer": "星穹记忆",
            "supporting_layers": ["星界记忆", "星辰记忆", "星域记忆"],
            "direction": "v2.9-v2.16 星穹治理链 -> Star-Dome chain closure audit",
        },
        "audited_chain_versions": list(SOURCE_CHAIN),
        "next_allowed_step": "v2.18.0 Star-Dome closure boundary manifest",
        "blocking_reasons": [],
        "chain_closure_summary": {
            "star_dome_final_closure_claimed": False,
        },
        "non_authorization_boundary": {
            "chain_closure_audit_passed_is_star_dome_final_closure": False,
        },
    }


def test_valid_audit_report_creates_boundary_manifest_ready():
    result = build_governed_star_dome_closure_boundary_manifest(_valid_audit_report())

    assert result["version"] == "2.18.0"
    assert result["status"] == "boundary_manifest_ready"
    assert result["read_only"] is True
    assert result["read_only_memory"] is True
    assert result["manifest_only"] is True
    assert result["boundary_manifest_only"] is True
    assert result["star_dome_stage_boundary_manifested"] is True
    assert result["blocking_reasons"] == []
    assert all(check["passed"] is True for check in result["boundary_manifest_checks"])


def test_manifested_chain_versions_exactly_match_v2_9_0_to_v2_17_0():
    result = build_governed_star_dome_closure_boundary_manifest(_valid_audit_report())

    assert result["manifested_chain_versions"] == MANIFESTED_CHAIN


def test_blocked_audit_report_blocks_boundary_manifest():
    report = _valid_audit_report()
    report["status"] = "blocked"
    report["blocking_reasons"] = ["source blocked"]

    result = build_governed_star_dome_closure_boundary_manifest(report)

    assert result["status"] == "blocked"
    assert result["star_dome_stage_boundary_manifested"] is False
    assert result["star_dome_stage_closure_statement"][
        "star_dome_governance_chain_stage_ready_for_closure"
    ] is False
    assert result["blocking_reasons"]
    assert result["required_human_actions"]


def test_unsafe_authorization_flag_blocks_boundary_manifest():
    report = _valid_audit_report()
    report["authorization_granted"] = True

    result = build_governed_star_dome_closure_boundary_manifest(report)

    assert result["status"] == "blocked"
    assert result["star_dome_stage_boundary_manifested"] is False


def test_star_dome_final_closure_claim_blocks_boundary_manifest():
    report = _valid_audit_report()
    report["star_dome_closed"] = True

    result = build_governed_star_dome_closure_boundary_manifest(report)

    assert result["status"] == "blocked"
    assert result["star_dome_final_closure_claimed"] is False


def test_handoff_authorization_claim_blocks_boundary_manifest():
    report = _valid_audit_report()
    report["handoff_authorized"] = True

    result = build_governed_star_dome_closure_boundary_manifest(report)

    assert result["status"] == "blocked"
    assert result["handoff_authorized"] is False


def test_star_hub_scheduling_authorization_claim_blocks_boundary_manifest():
    report = _valid_audit_report()
    report["star_hub_scheduling_authorized"] = True

    result = build_governed_star_dome_closure_boundary_manifest(report)

    assert result["status"] == "blocked"
    assert result["star_hub_scheduling_authorized"] is False


def test_memory_write_authorization_claim_blocks_boundary_manifest():
    report = _valid_audit_report()
    report["memory_write_authorized"] = True

    result = build_governed_star_dome_closure_boundary_manifest(report)

    assert result["status"] == "blocked"
    assert result["memory_write_authorized"] is False


def test_openclaw_execution_authorization_claim_blocks_boundary_manifest():
    report = _valid_audit_report()
    report["openclaw_execution_authorized"] = True

    result = build_governed_star_dome_closure_boundary_manifest(report)

    assert result["status"] == "blocked"
    assert result["openclaw_execution_authorized"] is False


def test_approval_claim_blocks_boundary_manifest():
    report = _valid_audit_report()
    report["approval_granted"] = True

    result = build_governed_star_dome_closure_boundary_manifest(report)

    assert result["status"] == "blocked"
    assert result["approval_granted"] is False


def test_malformed_audited_chain_versions_blocks_boundary_manifest():
    report = _valid_audit_report()
    report["audited_chain_versions"] = ["v2.9.0", "v2.11.0"]

    result = build_governed_star_dome_closure_boundary_manifest(report)

    assert result["status"] == "blocked"
    assert "source_audited_chain_versions_must_exactly_match_v2_9_0_through_v2_16_0" in result[
        "blocking_reasons"
    ]


def test_sensitive_field_names_and_values_are_not_leaked_in_serialized_output():
    report = {
        **_valid_audit_report(),
        "approval_phrase": "approve everything",
        "stdout_tail": "tail text",
        "nested": {
            "stdout": "raw text",
            "raw_logs": "logs",
            "token": "token-value",
            "api_key": "key-value",
            "secret": "secret-value",
            "password": "password-value",
            "credential": "credential-value",
        },
    }

    result = build_governed_star_dome_closure_boundary_manifest(report)
    payload = governed_star_dome_closure_boundary_manifest_to_json(result)
    decoded = json.loads(payload)

    assert decoded["sensitive_fields_omitted"] is True
    for text in (
        "approval_phrase",
        "stdout_tail",
        "stdout",
        "raw_logs",
        "token",
        "api_key",
        "secret",
        "password",
        "credential",
        "approve everything",
        "tail text",
        "raw text",
        "logs",
        "token-value",
        "key-value",
        "secret-value",
        "password-value",
        "credential-value",
    ):
        assert text not in payload


def test_manifest_does_not_authorize_handoff():
    result = build_governed_star_dome_closure_boundary_manifest(_valid_audit_report())

    assert result["star_hub_handoff_authorized"] is False
    assert result["handoff_authorized"] is False


def test_manifest_does_not_authorize_star_hub_scheduling():
    result = build_governed_star_dome_closure_boundary_manifest(_valid_audit_report())

    assert result["star_hub_scheduling_authorized"] is False


def test_manifest_does_not_create_approval_request():
    result = build_governed_star_dome_closure_boundary_manifest(_valid_audit_report())

    assert result["would_create_approval_request"] is False
    assert result["approval_request_created"] is False


def test_manifest_does_not_submit_approval_request():
    result = build_governed_star_dome_closure_boundary_manifest(_valid_audit_report())

    assert result["would_submit_approval_request"] is False
    assert result["approval_request_submitted"] is False


def test_manifest_does_not_execute_approval_request():
    result = build_governed_star_dome_closure_boundary_manifest(_valid_audit_report())

    assert result["would_execute_approval_request"] is False


def test_manifest_does_not_record_human_decision():
    result = build_governed_star_dome_closure_boundary_manifest(_valid_audit_report())

    assert result["would_record_human_decision"] is False
    assert result["human_decision_recorded"] is False


def test_manifest_does_not_authorize_approval():
    result = build_governed_star_dome_closure_boundary_manifest(_valid_audit_report())

    assert result["would_grant_approval"] is False
    assert result["approval_granted"] is False
    assert result["approval_request_authorized"] is False


def test_manifest_does_not_authorize_memory_write():
    result = build_governed_star_dome_closure_boundary_manifest(_valid_audit_report())

    assert result["would_write_durable_memory"] is False
    assert result["memory_write_authorized"] is False


def test_manifest_does_not_authorize_openclaw_execution():
    result = build_governed_star_dome_closure_boundary_manifest(_valid_audit_report())

    assert result["invokes_openclaw"] is False
    assert result["openclaw_execution_authorized"] is False


def test_layer_mapping_is_correct():
    result = build_governed_star_dome_closure_boundary_manifest(_valid_audit_report())
    mapping = result["civilization_core_layer_mapping"]

    assert mapping["primary_layer"] == "星穹记忆"
    assert mapping["supporting_layers"] == ["星界记忆", "星辰记忆", "星域记忆"]
    assert (
        mapping["direction"]
        == "Star-Dome chain closure audit -> Star-Dome closure boundary manifest"
    )


def test_next_allowed_step_is_star_hub_preflight_boundary_analysis():
    result = build_governed_star_dome_closure_boundary_manifest(_valid_audit_report())

    assert result["next_allowed_step"] == "v2.19.0 Star-Hub preflight boundary analysis"
