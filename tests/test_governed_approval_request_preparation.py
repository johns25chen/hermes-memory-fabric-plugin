from __future__ import annotations

import json

from hermes_memory_fabric.governed_approval_request_preparation import (
    build_governed_approval_request_preparation,
)


def _valid_review_gate_report() -> dict[str, object]:
    return {
        "version": "2.11.0",
        "status": "review_ready",
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
        "authorization_granted": False,
        "review_gate_authorized": False,
        "approval_request_authorized": False,
        "memory_write_authorized": False,
        "openclaw_execution_authorized": False,
        "civilization_core_layer_mapping": {
            "primary_layer": "星穹记忆",
            "supporting_layers": ["星辰记忆", "星域记忆", "星界记忆"],
            "direction": "星辰候选记忆提案 -> 星穹治理评审闸门",
        },
        "accepted_candidate_ids": ["star-dome-preparation-candidate"],
        "blocked_candidate_ids": [],
    }


def test_valid_review_gate_creates_preparation_ready():
    result = build_governed_approval_request_preparation(_valid_review_gate_report())

    assert result["version"] == "2.12.0"
    assert result["status"] == "preparation_ready"
    assert result["read_only"] is True
    assert result["read_only_memory"] is True
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
    assert result["authorization_granted"] is False
    assert result["preparation_authorized"] is False
    assert result["approval_request_created"] is False
    assert result["approval_request_authorized"] is False
    assert result["approval_granted"] is False
    assert result["memory_write_authorized"] is False
    assert result["openclaw_execution_authorized"] is False
    assert result["candidate_ids_for_human_review"] == ["star-dome-preparation-candidate"]
    assert result["blocked_candidate_ids"] == []
    assert result["approval_request_draft_material"]["draft_status"] == (
        "prepared_for_human_operator_only"
    )
    assert result["approval_request_draft_material"]["is_real_approval_request"] is False


def test_blocked_review_gate_creates_blocked_preparation_report():
    review_gate = _valid_review_gate_report()
    review_gate["status"] = "blocked"

    result = build_governed_approval_request_preparation(review_gate)

    assert result["status"] == "blocked"
    assert result["candidate_ids_for_human_review"] == []
    assert result["approval_request_draft_material"]["is_real_approval_request"] is False
    assert "review_gate_status_must_be_review_ready" in result["blocking_reasons"]
    assert "resolve_blocking_reasons_before_human_approval_request_preparation" in (
        result["required_human_actions"]
    )


def test_unsafe_authorization_flag_blocks_preparation():
    review_gate = _valid_review_gate_report()
    review_gate["approval_request_authorized"] = True

    result = build_governed_approval_request_preparation(review_gate)

    assert result["status"] == "blocked"
    assert result["approval_request_authorized"] is False
    assert result["candidate_ids_for_human_review"] == []
    assert "review_gate_flag_approval_request_authorized_must_be_false" in result["blocking_reasons"]


def test_non_empty_blocked_candidate_ids_blocks_preparation():
    review_gate = _valid_review_gate_report()
    review_gate["blocked_candidate_ids"] = ["blocked-candidate"]

    result = build_governed_approval_request_preparation(review_gate)

    assert result["status"] == "blocked"
    assert result["candidate_ids_for_human_review"] == []
    assert result["blocked_candidate_ids"] == ["blocked-candidate"]
    assert "blocked_candidate_ids_must_be_empty" in result["blocking_reasons"]


def test_empty_accepted_candidate_ids_blocks_preparation():
    review_gate = _valid_review_gate_report()
    review_gate["accepted_candidate_ids"] = []

    result = build_governed_approval_request_preparation(review_gate)

    assert result["status"] == "blocked"
    assert result["candidate_ids_for_human_review"] == []
    assert "accepted_candidate_ids_must_be_non_empty_safe_string_list" in (
        result["blocking_reasons"]
    )


def test_sensitive_field_names_and_values_are_not_leaked_in_serialized_output():
    review_gate = _valid_review_gate_report()
    review_gate["approval_phrase"] = "phrase must not leak"
    review_gate["stdout_tail"] = "tail must not leak"
    review_gate["stdout"] = "stdout must not leak"
    review_gate["raw_logs"] = {"secret": "secret must not leak"}
    review_gate["nested"] = {
        "token": "token must not leak",
        "api_key": "api key must not leak",
        "password": "password must not leak",
        "credential": "credential must not leak",
    }

    result = build_governed_approval_request_preparation(review_gate)
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


def test_preparation_does_not_create_approval_request():
    result = build_governed_approval_request_preparation(_valid_review_gate_report())

    assert result["would_create_approval_request"] is False
    assert result["would_submit_approval_request"] is False
    assert result["approval_request_created"] is False
    assert result["approval_request_draft_material"]["is_real_approval_request"] is False


def test_preparation_does_not_authorize_approval():
    result = build_governed_approval_request_preparation(_valid_review_gate_report())

    assert result["authorization_granted"] is False
    assert result["preparation_authorized"] is False
    assert result["approval_request_authorized"] is False
    assert result["approval_granted"] is False


def test_preparation_does_not_authorize_memory_write():
    result = build_governed_approval_request_preparation(_valid_review_gate_report())

    assert result["would_write_durable_memory"] is False
    assert result["would_mutate_memory_graph"] is False
    assert result["would_create_operation_ledger_entry"] is False
    assert result["memory_write_authorized"] is False


def test_preparation_does_not_authorize_openclaw_execution():
    result = build_governed_approval_request_preparation(_valid_review_gate_report())

    assert result["invokes_openclaw"] is False
    assert result["openclaw_execution_authorized"] is False


def test_layer_mapping_is_correct():
    result = build_governed_approval_request_preparation(_valid_review_gate_report())
    mapping = result["civilization_core_layer_mapping"]

    assert mapping["primary_layer"] == "星穹记忆"
    assert "星辰记忆" in mapping["supporting_layers"]
    assert "星域记忆" in mapping["supporting_layers"]
    assert "星界记忆" in mapping["supporting_layers"]
    assert mapping["direction"] == "星穹治理评审闸门 -> 受治理 approval request 准备"


def test_draft_material_uses_ids_and_structural_gate_status_only():
    review_gate = _valid_review_gate_report()
    review_gate["candidate_review_results"] = [
        {
            "candidate_id": "star-dome-preparation-candidate",
            "summary": "candidate body must not leak",
        }
    ]

    result = build_governed_approval_request_preparation(review_gate)
    serialized = json.dumps(result["approval_request_draft_material"], ensure_ascii=False)

    assert "star-dome-preparation-candidate" in serialized
    assert "candidate body must not leak" not in serialized
