from __future__ import annotations

import json

from hermes_memory_fabric.governed_memory_proposal_from_evidence import (
    build_governed_memory_proposal_from_evidence,
)


def _valid_evidence_validation() -> dict[str, object]:
    return {
        "version": "2.9.0",
        "status": "closed_loop_evidence_ready",
        "read_only": True,
        "read_only_memory": True,
        "would_mutate_memory": False,
        "invokes_openclaw": False,
        "writes_files": False,
        "would_call_github_api": False,
        "would_merge_pr": False,
        "would_create_tag": False,
        "authorization_granted": False,
        "openclaw_execution_authorized": False,
        "evidence_summary": {
            "categories_present": [
                "natural_language_task",
                "codex_cli_implementation",
                "terminal_or_openclaw_validation",
                "chatgpt_review",
                "human_operator_decision",
                "github_record",
            ],
            "natural_language_task": {
                "present": True,
                "true_flag_count": 1,
                "non_empty_list_count": 0,
                "non_empty_text_field_count": 2,
            },
            "codex_cli_implementation": {
                "present": True,
                "true_flag_count": 3,
                "non_empty_list_count": 1,
                "non_empty_text_field_count": 1,
            },
            "terminal_or_openclaw_validation": {
                "present": True,
                "true_flag_count": 4,
                "non_empty_list_count": 1,
                "non_empty_text_field_count": 0,
            },
            "chatgpt_review": {
                "present": True,
                "true_flag_count": 4,
                "non_empty_list_count": 0,
                "non_empty_text_field_count": 0,
            },
            "human_operator_decision": {
                "present": True,
                "true_flag_count": 2,
                "non_empty_list_count": 0,
                "non_empty_text_field_count": 0,
            },
            "github_record": {
                "present": True,
                "true_flag_count": 2,
                "non_empty_list_count": 0,
                "non_empty_text_field_count": 0,
            },
        },
        "missing_evidence": [],
        "blocking_reasons": [],
        "required_actions": ["human_operator_may_review_evidence_no_authorization_granted"],
    }


def test_valid_closed_loop_evidence_creates_proposal_ready():
    result = build_governed_memory_proposal_from_evidence(_valid_evidence_validation())

    assert result["version"] == "2.10.0"
    assert result["status"] == "proposal_ready"
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
    assert result["authorization_granted"] is False
    assert result["memory_write_authorized"] is False
    assert result["openclaw_execution_authorized"] is False
    assert len(result["candidate_memories"]) == 4


def test_blocked_evidence_creates_blocked_proposal_report():
    evidence_validation = _valid_evidence_validation()
    evidence_validation["status"] = "blocked"
    evidence_validation["blocking_reasons"] = ["required_evidence_missing_or_incomplete"]
    evidence_validation["required_actions"] = ["provide_missing_closed_loop_evidence"]

    result = build_governed_memory_proposal_from_evidence(evidence_validation)

    assert result["status"] == "blocked"
    assert result["candidate_memories"] == []
    assert "required_evidence_missing_or_incomplete" in result["blocking_reasons"]
    assert "provide_missing_closed_loop_evidence" in result["required_review_actions"]


def test_sensitive_fields_are_not_leaked_in_serialized_output():
    evidence_validation = _valid_evidence_validation()
    evidence_validation["approval_phrase"] = "phrase must not leak"
    evidence_validation["stdout_tail"] = "tail must not leak"
    evidence_validation["stdout"] = "stdout must not leak"
    evidence_validation["raw_logs"] = {"secret": "secret must not leak"}
    evidence_validation["nested"] = {
        "token": "token must not leak",
        "api_key": "api key must not leak",
        "password": "password must not leak",
        "credential": "credential must not leak",
    }

    result = build_governed_memory_proposal_from_evidence(evidence_validation)
    serialized = json.dumps(result, ensure_ascii=False)

    assert result["sensitive_field_count"] >= 8
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


def test_proposal_generation_does_not_authorize_memory_write():
    result = build_governed_memory_proposal_from_evidence(_valid_evidence_validation())

    assert result["authorization_granted"] is False
    assert result["memory_write_authorized"] is False
    assert result["would_write_durable_memory"] is False
    assert result["would_mutate_memory_graph"] is False
    assert result["would_create_operation_ledger_entry"] is False


def test_proposal_generation_does_not_authorize_openclaw_execution():
    result = build_governed_memory_proposal_from_evidence(_valid_evidence_validation())

    assert result["invokes_openclaw"] is False
    assert result["openclaw_execution_authorized"] is False


def test_layer_mapping_is_correct():
    result = build_governed_memory_proposal_from_evidence(_valid_evidence_validation())
    mapping = result["civilization_core_layer_mapping"]

    assert mapping["primary_layer"] == "星辰记忆"
    assert "星域记忆" in mapping["supporting_layers"]
    assert "星穹记忆" in mapping["supporting_layers"]
    assert "星界记忆" in mapping["supporting_layers"]
    assert mapping["direction"] == "星界闭环证据 -> 星辰候选记忆提案"
    assert {candidate["memory_layer"] for candidate in result["candidate_memories"]} == {"星辰记忆"}
