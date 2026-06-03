from __future__ import annotations

import json

from hermes_memory_fabric.governed_human_operator_decision_packet_dry_run import (
    build_governed_human_operator_decision_packet_dry_run,
)


def _valid_validation_report() -> dict[str, object]:
    return {
        "version": "2.14.0",
        "status": "validation_ready",
        "read_only": True,
        "read_only_memory": True,
        "validation_only": True,
        "dry_run_only": True,
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
        "authorization_granted": False,
        "validation_authorized": False,
        "envelope_authorized": False,
        "approval_request_created": False,
        "approval_request_submitted": False,
        "approval_request_authorized": False,
        "approval_granted": False,
        "memory_write_authorized": False,
        "openclaw_execution_authorized": False,
        "civilization_core_layer_mapping": {
            "primary_layer": "星穹记忆",
            "supporting_layers": ["星辰记忆", "星域记忆", "星界记忆"],
            "direction": "星穹 dry-run envelope -> 星穹 dry-run envelope validation gate",
        },
        "candidate_ids_validated": ["star-dome-decision-packet-candidate"],
        "blocked_candidate_ids": [],
        "validated_dry_run_envelope_summary": {
            "validation_status": "dry_run_envelope_validated_for_human_review_only",
            "is_real_approval_request": False,
            "is_submittable": False,
            "is_executable": False,
            "candidate_ids": ["star-dome-decision-packet-candidate"],
            "source_envelope_version": "2.13.0",
            "source_preparation_version": "2.12.0",
            "envelope_type": "approval_request_dry_run",
            "candidate_body": "candidate body must not leak",
            "hidden_approval_material": "hidden approval material must not leak",
        },
    }


def test_valid_validation_report_creates_decision_packet_ready():
    result = build_governed_human_operator_decision_packet_dry_run(
        _valid_validation_report()
    )

    assert result["version"] == "2.15.0"
    assert result["status"] == "decision_packet_ready"
    assert result["read_only"] is True
    assert result["read_only_memory"] is True
    assert result["dry_run_only"] is True
    assert result["decision_packet_only"] is True
    assert result["would_mutate_memory"] is False
    assert result["writes_files"] is False
    assert result["invokes_openclaw"] is False
    assert result["would_call_github_api"] is False
    assert result["would_merge_pr"] is False
    assert result["would_create_tag"] is False
    assert result["would_write_durable_memory"] is False
    assert result["would_mutate_memory_graph"] is False
    assert result["would_create_operation_ledger_entry"] is False
    assert result["would_create_approval_request"] is False
    assert result["would_submit_approval_request"] is False
    assert result["would_execute_approval_request"] is False
    assert result["would_record_human_decision"] is False
    assert result["would_grant_approval"] is False
    assert result["authorization_granted"] is False
    assert result["decision_packet_authorized"] is False
    assert result["human_decision_recorded"] is False
    assert result["approval_request_created"] is False
    assert result["approval_request_submitted"] is False
    assert result["approval_request_authorized"] is False
    assert result["approval_granted"] is False
    assert result["memory_write_authorized"] is False
    assert result["openclaw_execution_authorized"] is False
    assert result["candidate_ids_for_decision_review"] == [
        "star-dome-decision-packet-candidate"
    ]

    packet = result["human_operator_decision_packet"]
    assert packet["packet_status"] == "prepared_for_human_operator_review_only"
    assert packet["is_real_human_decision"] is False
    assert packet["is_approval"] is False
    assert packet["is_submittable"] is False
    assert packet["is_executable"] is False
    assert packet["candidate_ids"] == ["star-dome-decision-packet-candidate"]
    assert packet["source_validation_version"] == "2.14.0"
    assert packet["source_envelope_version"] == "2.13.0"
    assert packet["source_preparation_version"] == "2.12.0"
    assert packet["packet_type"] == "human_operator_decision_packet_dry_run"
    assert packet["decision_options"] == [
        "request_changes",
        "reject",
        "prepare_separate_real_approval_process",
    ]
    assert "selected_decision" not in packet


def test_blocked_validation_report_creates_blocked_decision_packet_report():
    report = _valid_validation_report()
    report["status"] = "blocked"

    result = build_governed_human_operator_decision_packet_dry_run(report)

    assert result["status"] == "blocked"
    assert result["candidate_ids_for_decision_review"] == []
    assert result["human_operator_decision_packet"]["packet_status"] == (
        "blocked_not_prepared_for_review"
    )
    assert "validation_report_status_must_be_validation_ready" in result["blocking_reasons"]
    assert "repair_v2_14_validation_report_before_decision_packet_dry_run_can_continue" in (
        result["required_human_actions"]
    )


def test_unsafe_authorization_flag_blocks_decision_packet():
    report = _valid_validation_report()
    report["authorization_granted"] = True

    result = build_governed_human_operator_decision_packet_dry_run(report)

    assert result["status"] == "blocked"
    assert result["authorization_granted"] is False
    assert result["candidate_ids_for_decision_review"] == []
    assert "validation_flag_authorization_granted_must_be_false" in (
        result["blocking_reasons"]
    )


def test_real_submittable_executable_validated_summary_blocks_decision_packet():
    report = _valid_validation_report()
    summary = report["validated_dry_run_envelope_summary"]
    assert isinstance(summary, dict)
    summary["is_real_approval_request"] = True
    summary["is_submittable"] = True
    summary["is_executable"] = True

    result = build_governed_human_operator_decision_packet_dry_run(report)

    assert result["status"] == "blocked"
    assert result["human_operator_decision_packet"]["is_real_human_decision"] is False
    assert "validated_summary_must_not_be_real_approval_request" in result["blocking_reasons"]
    assert "validated_summary_must_not_be_submittable" in result["blocking_reasons"]
    assert "validated_summary_must_not_be_executable" in result["blocking_reasons"]


def test_non_empty_blocked_candidate_ids_blocks_decision_packet():
    report = _valid_validation_report()
    report["blocked_candidate_ids"] = ["blocked-candidate"]

    result = build_governed_human_operator_decision_packet_dry_run(report)

    assert result["status"] == "blocked"
    assert result["candidate_ids_for_decision_review"] == []
    assert result["blocked_candidate_ids"] == ["blocked-candidate"]
    assert "blocked_candidate_ids_must_be_empty" in result["blocking_reasons"]


def test_empty_candidate_ids_validated_blocks_decision_packet():
    report = _valid_validation_report()
    report["candidate_ids_validated"] = []

    result = build_governed_human_operator_decision_packet_dry_run(report)

    assert result["status"] == "blocked"
    assert result["candidate_ids_for_decision_review"] == []
    assert "candidate_ids_validated_must_be_non_empty_safe_string_list" in (
        result["blocking_reasons"]
    )


def test_sensitive_field_names_and_values_are_not_leaked_in_serialized_output():
    report = _valid_validation_report()
    report["approval_phrase"] = "phrase must not leak"
    report["stdout_tail"] = "tail must not leak"
    report["stdout"] = "stdout must not leak"
    report["raw_logs"] = {"secret": "secret must not leak"}
    report["nested"] = {
        "token": "token must not leak",
        "api_key": "api key must not leak",
        "password": "password must not leak",
        "credential": "credential must not leak",
    }

    result = build_governed_human_operator_decision_packet_dry_run(report)
    serialized = json.dumps(result, ensure_ascii=False)

    assert result["sensitive_field_count"] >= 8
    assert result["sensitive_fields_omitted"] is True
    assert "phrase must not leak" not in serialized
    assert "tail must not leak" not in serialized
    assert "stdout must not leak" not in serialized
    assert "secret must not leak" not in serialized
    assert "token must not leak" not in serialized
    assert "api key must not leak" not in serialized
    assert "password must not leak" not in serialized
    assert "credential must not leak" not in serialized
    assert "approval_phrase" not in serialized
    assert "stdout_tail" not in serialized
    assert "stdout" not in serialized
    assert "raw_logs" not in serialized
    assert "token" not in serialized
    assert "api_key" not in serialized
    assert "secret" not in serialized
    assert "password" not in serialized
    assert "credential" not in serialized
    assert "candidate body must not leak" not in serialized
    assert "hidden approval material must not leak" not in serialized


def test_decision_packet_does_not_create_approval_request():
    result = build_governed_human_operator_decision_packet_dry_run(
        _valid_validation_report()
    )

    assert result["would_create_approval_request"] is False
    assert result["approval_request_created"] is False
    assert result["human_operator_decision_packet"]["is_approval"] is False


def test_decision_packet_does_not_submit_approval_request():
    result = build_governed_human_operator_decision_packet_dry_run(
        _valid_validation_report()
    )

    assert result["would_submit_approval_request"] is False
    assert result["approval_request_submitted"] is False


def test_decision_packet_does_not_execute_approval_request():
    result = build_governed_human_operator_decision_packet_dry_run(
        _valid_validation_report()
    )

    assert result["would_execute_approval_request"] is False
    assert result["human_operator_decision_packet"]["is_executable"] is False


def test_decision_packet_does_not_record_human_decision():
    result = build_governed_human_operator_decision_packet_dry_run(
        _valid_validation_report()
    )

    assert result["would_record_human_decision"] is False
    assert result["human_decision_recorded"] is False


def test_decision_packet_does_not_authorize_approval():
    result = build_governed_human_operator_decision_packet_dry_run(
        _valid_validation_report()
    )

    assert result["would_grant_approval"] is False
    assert result["approval_request_authorized"] is False
    assert result["approval_granted"] is False


def test_decision_packet_does_not_authorize_memory_write():
    result = build_governed_human_operator_decision_packet_dry_run(
        _valid_validation_report()
    )

    assert result["would_write_durable_memory"] is False
    assert result["would_mutate_memory_graph"] is False
    assert result["memory_write_authorized"] is False


def test_decision_packet_does_not_authorize_openclaw_execution():
    result = build_governed_human_operator_decision_packet_dry_run(
        _valid_validation_report()
    )

    assert result["invokes_openclaw"] is False
    assert result["openclaw_execution_authorized"] is False


def test_layer_mapping_is_correct():
    result = build_governed_human_operator_decision_packet_dry_run(
        _valid_validation_report()
    )
    mapping = result["civilization_core_layer_mapping"]

    assert mapping["primary_layer"] == "星穹记忆"
    assert "星辰记忆" in mapping["supporting_layers"]
    assert "星域记忆" in mapping["supporting_layers"]
    assert "星界记忆" in mapping["supporting_layers"]
    assert mapping["direction"] == (
        "星穹 dry-run envelope validation gate -> Human Operator decision packet dry-run"
    )
