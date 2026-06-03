from __future__ import annotations

import json

from hermes_memory_fabric.governed_star_dome_chain_closure_audit import (
    governed_star_dome_chain_closure_audit_to_json,
    run_governed_star_dome_chain_closure_audit,
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
]

EXPECTED_STAGES = {
    "v2.9.0": ("closed-loop evidence validation", "星界记忆"),
    "v2.10.0": ("governed memory proposal from evidence", "星辰记忆"),
    "v2.11.0": ("governed proposal review gate", "星穹记忆"),
    "v2.12.0": ("governed approval request preparation", "星穹记忆"),
    "v2.13.0": ("governed approval request dry-run envelope", "星穹记忆"),
    "v2.14.0": ("governed dry-run envelope validation gate", "星穹记忆"),
    "v2.15.0": ("governed Human Operator decision packet dry-run", "星穹记忆"),
    "v2.16.0": ("governed Human Operator decision packet validation gate", "星穹记忆"),
}


def _valid_release_integrity_report() -> dict[str, object]:
    return {
        "audit_status": "pass",
        "release_chain_status": "pass",
        "pyproject_version": "2.17.0",
        "no_network_surface": True,
        "no_hermes_memory_write": True,
        "no_github_write": True,
        "no_composio_execution": True,
        "provider_tool_surface_empty": True,
        "previous_governed_smoke_safe": True,
    }


def test_valid_default_audit_creates_chain_closure_audit_passed():
    result = run_governed_star_dome_chain_closure_audit()

    assert result["version"] == "2.17.0"
    assert result["status"] == "chain_closure_audit_passed"
    assert result["read_only"] is True
    assert result["read_only_memory"] is True
    assert result["audit_only"] is True
    assert result["closure_audit_only"] is True
    assert result["blocking_reasons"] == []
    assert all(check["passed"] is True for check in result["chain_closure_checks"])


def test_audited_chain_versions_exactly_match_v2_9_0_to_v2_16_0():
    result = run_governed_star_dome_chain_closure_audit()

    assert result["audited_chain_versions"] == EXPECTED_CHAIN


def test_chain_stage_matrix_has_all_stages_and_correct_layers():
    result = run_governed_star_dome_chain_closure_audit()
    matrix = {stage["version"]: stage for stage in result["chain_stage_matrix"]}

    assert list(matrix) == EXPECTED_CHAIN
    for version, (stage_name, layer) in EXPECTED_STAGES.items():
        assert matrix[version]["stage"] == stage_name
        assert matrix[version]["primary_layer"] == layer


def test_valid_release_integrity_report_still_passes():
    result = run_governed_star_dome_chain_closure_audit(_valid_release_integrity_report())

    assert result["status"] == "chain_closure_audit_passed"


def test_blocked_release_integrity_report_blocks_closure_audit():
    report = _valid_release_integrity_report()
    report["audit_status"] = "fail"

    result = run_governed_star_dome_chain_closure_audit(report)

    assert result["status"] == "blocked"
    assert any(check["passed"] is False for check in result["chain_closure_checks"])
    assert result["blocking_reasons"]
    assert result["required_human_actions"]
    assert result["star_dome_closed"] is False
    assert result["closure_authorized"] is False
    assert result["handoff_authorized"] is False


def test_unsafe_release_integrity_booleans_block_closure_audit():
    for key in (
        "no_network_surface",
        "no_hermes_memory_write",
        "no_github_write",
        "no_composio_execution",
        "provider_tool_surface_empty",
    ):
        report = _valid_release_integrity_report()
        report[key] = False

        result = run_governed_star_dome_chain_closure_audit(report)

        assert result["status"] == "blocked"
        assert result["blocking_reasons"]


def test_unsafe_smoke_safe_fields_block_closure_audit():
    report = _valid_release_integrity_report()
    report["governed_human_operator_decision_packet_validation_smoke_safe"] = False

    result = run_governed_star_dome_chain_closure_audit(report)

    assert result["status"] == "blocked"
    assert "release_integrity_existing_smoke_safe_fields_must_not_be_false" in result[
        "blocking_reasons"
    ]


def test_sensitive_field_names_and_values_are_not_leaked_in_serialized_output():
    result = run_governed_star_dome_chain_closure_audit(
        {
            **_valid_release_integrity_report(),
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
    )

    payload = governed_star_dome_chain_closure_audit_to_json(result)
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


def test_audit_does_not_close_star_dome():
    result = run_governed_star_dome_chain_closure_audit()

    assert result["star_dome_closed"] is False


def test_audit_does_not_authorize_handoff():
    result = run_governed_star_dome_chain_closure_audit()

    assert result["handoff_authorized"] is False


def test_audit_does_not_create_approval_request():
    result = run_governed_star_dome_chain_closure_audit()

    assert result["would_create_approval_request"] is False
    assert result["approval_request_created"] is False


def test_audit_does_not_submit_approval_request():
    result = run_governed_star_dome_chain_closure_audit()

    assert result["would_submit_approval_request"] is False
    assert result["approval_request_submitted"] is False


def test_audit_does_not_execute_approval_request():
    result = run_governed_star_dome_chain_closure_audit()

    assert result["would_execute_approval_request"] is False


def test_audit_does_not_record_human_decision():
    result = run_governed_star_dome_chain_closure_audit()

    assert result["would_record_human_decision"] is False
    assert result["human_decision_recorded"] is False


def test_audit_does_not_authorize_approval():
    result = run_governed_star_dome_chain_closure_audit()

    assert result["would_grant_approval"] is False
    assert result["approval_granted"] is False
    assert result["approval_request_authorized"] is False


def test_audit_does_not_authorize_memory_write():
    result = run_governed_star_dome_chain_closure_audit()

    assert result["would_write_durable_memory"] is False
    assert result["memory_write_authorized"] is False


def test_audit_does_not_authorize_openclaw_execution():
    result = run_governed_star_dome_chain_closure_audit()

    assert result["invokes_openclaw"] is False
    assert result["openclaw_execution_authorized"] is False


def test_layer_mapping_is_correct():
    result = run_governed_star_dome_chain_closure_audit()
    mapping = result["civilization_core_layer_mapping"]

    assert mapping["primary_layer"] == "星穹记忆"
    assert mapping["supporting_layers"] == ["星界记忆", "星辰记忆", "星域记忆"]
    assert (
        mapping["direction"]
        == "v2.9-v2.16 星穹治理链 -> Star-Dome chain closure audit"
    )


def test_next_allowed_step_is_star_dome_closure_boundary_manifest():
    result = run_governed_star_dome_chain_closure_audit()

    assert result["next_allowed_step"] == "v2.18.0 Star-Dome closure boundary manifest"
