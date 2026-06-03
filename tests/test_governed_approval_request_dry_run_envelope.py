from __future__ import annotations

import json

from hermes_memory_fabric.governed_approval_request_dry_run_envelope import (
    build_governed_approval_request_dry_run_envelope,
)


def _valid_preparation_report() -> dict[str, object]:
    return {
        "version": "2.12.0",
        "status": "preparation_ready",
        "read_only": True,
        "read_only_memory": True,
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
        "authorization_granted": False,
        "preparation_authorized": False,
        "approval_request_created": False,
        "approval_request_authorized": False,
        "approval_granted": False,
        "memory_write_authorized": False,
        "openclaw_execution_authorized": False,
        "civilization_core_layer_mapping": {
            "primary_layer": "星穹记忆",
            "supporting_layers": ["星辰记忆", "星域记忆", "星界记忆"],
            "direction": "星穹治理评审闸门 -> 受治理 approval request 准备",
        },
        "candidate_ids_for_human_review": ["star-dome-envelope-candidate"],
        "blocked_candidate_ids": [],
        "approval_request_draft_material": {
            "draft_status": "prepared_for_human_operator_only",
            "is_real_approval_request": False,
            "candidate_ids": ["star-dome-envelope-candidate"],
            "structural_status_only": True,
        },
    }


def test_valid_preparation_report_creates_envelope_ready():
    result = build_governed_approval_request_dry_run_envelope(_valid_preparation_report())

    assert result["version"] == "2.13.0"
    assert result["status"] == "envelope_ready"
    assert result["read_only"] is True
    assert result["read_only_memory"] is True
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
    assert result["envelope_authorized"] is False
    assert result["approval_request_created"] is False
    assert result["approval_request_submitted"] is False
    assert result["approval_request_authorized"] is False
    assert result["approval_granted"] is False
    assert result["memory_write_authorized"] is False
    assert result["openclaw_execution_authorized"] is False
    assert result["candidate_ids_in_envelope"] == ["star-dome-envelope-candidate"]
    envelope = result["dry_run_envelope"]
    assert envelope["envelope_status"] == "dry_run_prepared_for_human_operator_only"
    assert envelope["is_real_approval_request"] is False
    assert envelope["is_submittable"] is False
    assert envelope["source_preparation_version"] == "2.12.0"
    assert envelope["envelope_type"] == "approval_request_dry_run"


def test_blocked_preparation_report_creates_blocked_envelope_report():
    preparation = _valid_preparation_report()
    preparation["status"] = "blocked"

    result = build_governed_approval_request_dry_run_envelope(preparation)

    assert result["status"] == "blocked"
    assert result["candidate_ids_in_envelope"] == []
    assert result["dry_run_envelope"]["is_real_approval_request"] is False
    assert "preparation_status_must_be_preparation_ready" in result["blocking_reasons"]
    assert "repair_v2_12_preparation_report_before_dry_run_envelope_can_continue" in (
        result["required_human_actions"]
    )


def test_unsafe_authorization_flag_blocks_dry_run_envelope():
    preparation = _valid_preparation_report()
    preparation["approval_request_authorized"] = True

    result = build_governed_approval_request_dry_run_envelope(preparation)

    assert result["status"] == "blocked"
    assert result["approval_request_authorized"] is False
    assert result["candidate_ids_in_envelope"] == []
    assert "preparation_flag_approval_request_authorized_must_be_false" in (
        result["blocking_reasons"]
    )


def test_real_approval_request_draft_blocks_dry_run_envelope():
    preparation = _valid_preparation_report()
    draft = preparation["approval_request_draft_material"]
    assert isinstance(draft, dict)
    draft["is_real_approval_request"] = True

    result = build_governed_approval_request_dry_run_envelope(preparation)

    assert result["status"] == "blocked"
    assert result["dry_run_envelope"]["is_real_approval_request"] is False
    assert "approval_request_draft_material_must_not_be_real_approval_request" in (
        result["blocking_reasons"]
    )


def test_non_empty_blocked_candidate_ids_blocks_dry_run_envelope():
    preparation = _valid_preparation_report()
    preparation["blocked_candidate_ids"] = ["blocked-candidate"]

    result = build_governed_approval_request_dry_run_envelope(preparation)

    assert result["status"] == "blocked"
    assert result["candidate_ids_in_envelope"] == []
    assert result["blocked_candidate_ids"] == ["blocked-candidate"]
    assert "blocked_candidate_ids_must_be_empty" in result["blocking_reasons"]


def test_empty_candidate_ids_for_human_review_blocks_dry_run_envelope():
    preparation = _valid_preparation_report()
    preparation["candidate_ids_for_human_review"] = []

    result = build_governed_approval_request_dry_run_envelope(preparation)

    assert result["status"] == "blocked"
    assert result["candidate_ids_in_envelope"] == []
    assert "candidate_ids_for_human_review_must_be_non_empty_safe_string_list" in (
        result["blocking_reasons"]
    )


def test_sensitive_field_names_and_values_are_not_leaked_in_serialized_output():
    preparation = _valid_preparation_report()
    preparation["approval_phrase"] = "phrase must not leak"
    preparation["stdout_tail"] = "tail must not leak"
    preparation["stdout"] = "stdout must not leak"
    preparation["raw_logs"] = {"secret": "secret must not leak"}
    preparation["nested"] = {
        "token": "token must not leak",
        "api_key": "api key must not leak",
        "password": "password must not leak",
        "credential": "credential must not leak",
    }

    result = build_governed_approval_request_dry_run_envelope(preparation)
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


def test_dry_run_envelope_does_not_create_approval_request():
    result = build_governed_approval_request_dry_run_envelope(_valid_preparation_report())

    assert result["would_create_approval_request"] is False
    assert result["approval_request_created"] is False
    assert result["dry_run_envelope"]["is_real_approval_request"] is False


def test_dry_run_envelope_does_not_submit_approval_request():
    result = build_governed_approval_request_dry_run_envelope(_valid_preparation_report())

    assert result["would_submit_approval_request"] is False
    assert result["approval_request_submitted"] is False
    assert result["dry_run_envelope"]["is_submittable"] is False


def test_dry_run_envelope_does_not_authorize_approval():
    result = build_governed_approval_request_dry_run_envelope(_valid_preparation_report())

    assert result["authorization_granted"] is False
    assert result["envelope_authorized"] is False
    assert result["approval_request_authorized"] is False
    assert result["approval_granted"] is False


def test_dry_run_envelope_does_not_authorize_memory_write():
    result = build_governed_approval_request_dry_run_envelope(_valid_preparation_report())

    assert result["would_write_durable_memory"] is False
    assert result["would_mutate_memory_graph"] is False
    assert result["would_create_operation_ledger_entry"] is False
    assert result["memory_write_authorized"] is False


def test_dry_run_envelope_does_not_authorize_openclaw_execution():
    result = build_governed_approval_request_dry_run_envelope(_valid_preparation_report())

    assert result["invokes_openclaw"] is False
    assert result["would_execute_approval_request"] is False
    assert result["openclaw_execution_authorized"] is False


def test_layer_mapping_is_correct():
    result = build_governed_approval_request_dry_run_envelope(_valid_preparation_report())
    mapping = result["civilization_core_layer_mapping"]

    assert mapping["primary_layer"] == "星穹记忆"
    assert "星辰记忆" in mapping["supporting_layers"]
    assert "星域记忆" in mapping["supporting_layers"]
    assert "星界记忆" in mapping["supporting_layers"]
    assert mapping["direction"] == "星穹 approval request 准备材料 -> 星穹 dry-run envelope"


def test_dry_run_envelope_uses_ids_and_structural_preparation_status_only():
    preparation = _valid_preparation_report()
    preparation["approval_request_draft_material"] = {
        "draft_status": "prepared_for_human_operator_only",
        "is_real_approval_request": False,
        "candidate_ids": ["star-dome-envelope-candidate"],
        "candidate_body": "candidate body must not leak",
        "hidden_approval_material": "hidden approval material must not leak",
    }

    result = build_governed_approval_request_dry_run_envelope(preparation)
    serialized = json.dumps(result["dry_run_envelope"], ensure_ascii=False)

    assert "star-dome-envelope-candidate" in serialized
    assert "candidate body must not leak" not in serialized
    assert "hidden approval material must not leak" not in serialized
