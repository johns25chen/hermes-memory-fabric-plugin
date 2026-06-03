from __future__ import annotations

import json

from hermes_memory_fabric.governed_approval_request_dry_run_envelope_validation import (
    build_governed_approval_request_dry_run_envelope_validation,
)


def _valid_envelope_report() -> dict[str, object]:
    return {
        "version": "2.13.0",
        "status": "envelope_ready",
        "read_only": True,
        "read_only_memory": True,
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
            "direction": "星穹 approval request 准备材料 -> 星穹 dry-run envelope",
        },
        "candidate_ids_in_envelope": ["star-dome-validation-candidate"],
        "blocked_candidate_ids": [],
        "dry_run_envelope": {
            "envelope_status": "dry_run_prepared_for_human_operator_only",
            "is_real_approval_request": False,
            "is_submittable": False,
            "candidate_ids": ["star-dome-validation-candidate"],
            "source_preparation_version": "2.12.0",
            "envelope_type": "approval_request_dry_run",
            "candidate_body": "candidate body must not leak",
            "hidden_approval_material": "hidden approval material must not leak",
        },
    }


def test_valid_dry_run_envelope_creates_validation_ready():
    result = build_governed_approval_request_dry_run_envelope_validation(
        _valid_envelope_report()
    )

    assert result["version"] == "2.14.0"
    assert result["status"] == "validation_ready"
    assert result["read_only"] is True
    assert result["read_only_memory"] is True
    assert result["validation_only"] is True
    assert result["dry_run_only"] is True
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
    assert result["authorization_granted"] is False
    assert result["validation_authorized"] is False
    assert result["envelope_authorized"] is False
    assert result["approval_request_created"] is False
    assert result["approval_request_submitted"] is False
    assert result["approval_request_authorized"] is False
    assert result["approval_granted"] is False
    assert result["memory_write_authorized"] is False
    assert result["openclaw_execution_authorized"] is False
    assert result["candidate_ids_validated"] == ["star-dome-validation-candidate"]
    summary = result["validated_dry_run_envelope_summary"]
    assert summary["validation_status"] == "dry_run_envelope_validated_for_human_review_only"
    assert summary["is_real_approval_request"] is False
    assert summary["is_submittable"] is False
    assert summary["is_executable"] is False
    assert summary["candidate_ids"] == ["star-dome-validation-candidate"]
    assert summary["source_envelope_version"] == "2.13.0"
    assert summary["source_preparation_version"] == "2.12.0"
    assert summary["envelope_type"] == "approval_request_dry_run"


def test_blocked_dry_run_envelope_creates_blocked_validation_report():
    envelope = _valid_envelope_report()
    envelope["status"] = "blocked"

    result = build_governed_approval_request_dry_run_envelope_validation(envelope)

    assert result["status"] == "blocked"
    assert result["candidate_ids_validated"] == []
    assert result["validated_dry_run_envelope_summary"]["is_real_approval_request"] is False
    assert "envelope_report_status_must_be_envelope_ready" in result["blocking_reasons"]
    assert "repair_v2_13_dry_run_envelope_report_before_validation_can_continue" in (
        result["required_human_actions"]
    )


def test_unsafe_authorization_flag_blocks_validation():
    envelope = _valid_envelope_report()
    envelope["approval_request_authorized"] = True

    result = build_governed_approval_request_dry_run_envelope_validation(envelope)

    assert result["status"] == "blocked"
    assert result["approval_request_authorized"] is False
    assert result["candidate_ids_validated"] == []
    assert "envelope_flag_approval_request_authorized_must_be_false" in (
        result["blocking_reasons"]
    )


def test_real_approval_request_envelope_blocks_validation():
    envelope = _valid_envelope_report()
    dry_run_envelope = envelope["dry_run_envelope"]
    assert isinstance(dry_run_envelope, dict)
    dry_run_envelope["is_real_approval_request"] = True

    result = build_governed_approval_request_dry_run_envelope_validation(envelope)

    assert result["status"] == "blocked"
    assert result["validated_dry_run_envelope_summary"]["is_real_approval_request"] is False
    assert "dry_run_envelope_must_not_be_real_approval_request" in result["blocking_reasons"]


def test_submittable_envelope_blocks_validation():
    envelope = _valid_envelope_report()
    dry_run_envelope = envelope["dry_run_envelope"]
    assert isinstance(dry_run_envelope, dict)
    dry_run_envelope["is_submittable"] = True

    result = build_governed_approval_request_dry_run_envelope_validation(envelope)

    assert result["status"] == "blocked"
    assert result["validated_dry_run_envelope_summary"]["is_submittable"] is False
    assert "dry_run_envelope_must_not_be_submittable" in result["blocking_reasons"]


def test_executable_envelope_blocks_validation():
    envelope = _valid_envelope_report()
    dry_run_envelope = envelope["dry_run_envelope"]
    assert isinstance(dry_run_envelope, dict)
    dry_run_envelope["is_executable"] = True

    result = build_governed_approval_request_dry_run_envelope_validation(envelope)

    assert result["status"] == "blocked"
    assert result["validated_dry_run_envelope_summary"]["is_executable"] is False
    assert "dry_run_envelope_must_not_be_executable" in result["blocking_reasons"]


def test_non_empty_blocked_candidate_ids_blocks_validation():
    envelope = _valid_envelope_report()
    envelope["blocked_candidate_ids"] = ["blocked-candidate"]

    result = build_governed_approval_request_dry_run_envelope_validation(envelope)

    assert result["status"] == "blocked"
    assert result["candidate_ids_validated"] == []
    assert result["blocked_candidate_ids"] == ["blocked-candidate"]
    assert "blocked_candidate_ids_must_be_empty" in result["blocking_reasons"]


def test_empty_candidate_ids_in_envelope_blocks_validation():
    envelope = _valid_envelope_report()
    envelope["candidate_ids_in_envelope"] = []

    result = build_governed_approval_request_dry_run_envelope_validation(envelope)

    assert result["status"] == "blocked"
    assert result["candidate_ids_validated"] == []
    assert "candidate_ids_in_envelope_must_be_non_empty_safe_string_list" in (
        result["blocking_reasons"]
    )


def test_sensitive_field_names_and_values_are_not_leaked_in_serialized_output():
    envelope = _valid_envelope_report()
    envelope["approval_phrase"] = "phrase must not leak"
    envelope["stdout_tail"] = "tail must not leak"
    envelope["stdout"] = "stdout must not leak"
    envelope["raw_logs"] = {"secret": "secret must not leak"}
    envelope["nested"] = {
        "token": "token must not leak",
        "api_key": "api key must not leak",
        "password": "password must not leak",
        "credential": "credential must not leak",
    }

    result = build_governed_approval_request_dry_run_envelope_validation(envelope)
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


def test_validation_does_not_create_approval_request():
    result = build_governed_approval_request_dry_run_envelope_validation(
        _valid_envelope_report()
    )

    assert result["would_create_approval_request"] is False
    assert result["approval_request_created"] is False
    assert result["validated_dry_run_envelope_summary"]["is_real_approval_request"] is False


def test_validation_does_not_submit_approval_request():
    result = build_governed_approval_request_dry_run_envelope_validation(
        _valid_envelope_report()
    )

    assert result["would_submit_approval_request"] is False
    assert result["approval_request_submitted"] is False
    assert result["validated_dry_run_envelope_summary"]["is_submittable"] is False


def test_validation_does_not_execute_approval_request():
    result = build_governed_approval_request_dry_run_envelope_validation(
        _valid_envelope_report()
    )

    assert result["would_execute_approval_request"] is False
    assert result["validated_dry_run_envelope_summary"]["is_executable"] is False


def test_validation_does_not_authorize_approval():
    result = build_governed_approval_request_dry_run_envelope_validation(
        _valid_envelope_report()
    )

    assert result["authorization_granted"] is False
    assert result["validation_authorized"] is False
    assert result["envelope_authorized"] is False
    assert result["approval_request_authorized"] is False
    assert result["approval_granted"] is False


def test_validation_does_not_authorize_memory_write():
    result = build_governed_approval_request_dry_run_envelope_validation(
        _valid_envelope_report()
    )

    assert result["would_write_durable_memory"] is False
    assert result["would_mutate_memory_graph"] is False
    assert result["would_create_operation_ledger_entry"] is False
    assert result["memory_write_authorized"] is False


def test_validation_does_not_authorize_openclaw_execution():
    result = build_governed_approval_request_dry_run_envelope_validation(
        _valid_envelope_report()
    )

    assert result["invokes_openclaw"] is False
    assert result["would_execute_approval_request"] is False
    assert result["openclaw_execution_authorized"] is False


def test_layer_mapping_is_correct():
    result = build_governed_approval_request_dry_run_envelope_validation(
        _valid_envelope_report()
    )
    mapping = result["civilization_core_layer_mapping"]

    assert mapping["primary_layer"] == "星穹记忆"
    assert "星辰记忆" in mapping["supporting_layers"]
    assert "星域记忆" in mapping["supporting_layers"]
    assert "星界记忆" in mapping["supporting_layers"]
    assert mapping["direction"] == "星穹 dry-run envelope -> 星穹 dry-run envelope validation gate"
