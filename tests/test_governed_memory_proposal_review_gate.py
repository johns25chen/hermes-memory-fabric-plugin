from __future__ import annotations

import json

from hermes_memory_fabric.governed_memory_proposal_review_gate import (
    build_governed_memory_proposal_review_gate,
)


def _valid_proposal_report() -> dict[str, object]:
    return {
        "version": "2.10.0",
        "status": "proposal_ready",
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
        "authorization_granted": False,
        "memory_write_authorized": False,
        "openclaw_execution_authorized": False,
        "civilization_core_layer_mapping": {
            "primary_layer": "星辰记忆",
            "supporting_layers": ["星域记忆", "星穹记忆", "星界记忆"],
            "direction": "星界闭环证据 -> 星辰候选记忆提案",
        },
        "candidate_memories": [
            {
                "candidate_id": "star-memory-review-gate-candidate",
                "memory_layer": "星辰记忆",
                "title": "Review gate candidate",
                "summary": "Structurally complete candidate memory for review gate tests.",
                "evidence_basis": {"source": "test", "categories": [{"category": "local", "present": True}]},
                "scope": "Test candidate only.",
                "risks": ["candidate_must_not_be_treated_as_durable_memory"],
                "required_review": ["human_operator_review"],
            }
        ],
    }


def test_valid_proposal_creates_review_ready():
    result = build_governed_memory_proposal_review_gate(_valid_proposal_report())

    assert result["version"] == "2.11.0"
    assert result["status"] == "review_ready"
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
    assert result["authorization_granted"] is False
    assert result["review_gate_authorized"] is False
    assert result["approval_request_authorized"] is False
    assert result["memory_write_authorized"] is False
    assert result["openclaw_execution_authorized"] is False
    assert result["accepted_candidate_ids"] == ["star-memory-review-gate-candidate"]
    assert result["blocked_candidate_ids"] == []


def test_blocked_proposal_creates_blocked_review_gate_report():
    proposal = _valid_proposal_report()
    proposal["status"] = "blocked"

    result = build_governed_memory_proposal_review_gate(proposal)

    assert result["status"] == "blocked"
    assert result["accepted_candidate_ids"] == []
    assert "proposal_status_must_be_proposal_ready" in result["blocking_reasons"]
    assert "resolve_blocking_reasons_before_human_review_preparation" in result["required_review_actions"]


def test_malformed_candidate_creates_blocked_review_gate_report():
    proposal = _valid_proposal_report()
    proposal["candidate_memories"] = [
        {
            "candidate_id": "malformed-candidate",
            "memory_layer": "星辰记忆",
            "title": "",
        }
    ]

    result = build_governed_memory_proposal_review_gate(proposal)

    assert result["status"] == "blocked"
    assert result["accepted_candidate_ids"] == []
    assert result["blocked_candidate_ids"] == ["malformed-candidate"]
    assert "candidate_summary_missing" in result["blocking_reasons"]
    assert "candidate_title_must_be_non_empty" in result["blocking_reasons"]


def test_unsafe_authorization_flag_blocks_review_gate():
    proposal = _valid_proposal_report()
    proposal["memory_write_authorized"] = True

    result = build_governed_memory_proposal_review_gate(proposal)

    assert result["status"] == "blocked"
    assert result["memory_write_authorized"] is False
    assert result["accepted_candidate_ids"] == []
    assert "proposal_flag_memory_write_authorized_must_be_false" in result["blocking_reasons"]


def test_sensitive_field_names_and_values_are_not_leaked_in_serialized_output():
    proposal = _valid_proposal_report()
    proposal["approval_phrase"] = "phrase must not leak"
    proposal["stdout_tail"] = "tail must not leak"
    proposal["stdout"] = "stdout must not leak"
    proposal["raw_logs"] = {"secret": "secret must not leak"}
    proposal["nested"] = {
        "token": "token must not leak",
        "api_key": "api key must not leak",
        "password": "password must not leak",
        "credential": "credential must not leak",
    }

    result = build_governed_memory_proposal_review_gate(proposal)
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


def test_review_gate_does_not_authorize_approval_request():
    result = build_governed_memory_proposal_review_gate(_valid_proposal_report())

    assert result["would_create_approval_request"] is False
    assert result["approval_request_authorized"] is False
    assert result["authorization_granted"] is False


def test_review_gate_does_not_authorize_memory_write():
    result = build_governed_memory_proposal_review_gate(_valid_proposal_report())

    assert result["would_write_durable_memory"] is False
    assert result["would_mutate_memory_graph"] is False
    assert result["would_create_operation_ledger_entry"] is False
    assert result["memory_write_authorized"] is False


def test_review_gate_does_not_authorize_openclaw_execution():
    result = build_governed_memory_proposal_review_gate(_valid_proposal_report())

    assert result["invokes_openclaw"] is False
    assert result["openclaw_execution_authorized"] is False


def test_layer_mapping_is_correct():
    result = build_governed_memory_proposal_review_gate(_valid_proposal_report())
    mapping = result["civilization_core_layer_mapping"]

    assert mapping["primary_layer"] == "星穹记忆"
    assert "星辰记忆" in mapping["supporting_layers"]
    assert "星域记忆" in mapping["supporting_layers"]
    assert "星界记忆" in mapping["supporting_layers"]
    assert mapping["direction"] == "星辰候选记忆提案 -> 星穹治理评审闸门"


def test_candidate_review_results_are_structural_only():
    result = build_governed_memory_proposal_review_gate(_valid_proposal_report())
    candidate_result = result["candidate_review_results"][0]
    serialized = json.dumps(candidate_result, ensure_ascii=False)

    assert candidate_result["candidate_id"] == "star-memory-review-gate-candidate"
    assert candidate_result["review_status"] == "accepted_for_review"
    assert "Structurally complete candidate memory" not in serialized
    assert "Test candidate only" not in serialized
