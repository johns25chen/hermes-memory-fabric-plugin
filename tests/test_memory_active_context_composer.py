from __future__ import annotations

from copy import deepcopy

from hermes_memory_fabric.memory_active_context_composer import (
    ACTIVE_CONTEXT_COMPOSER_POLICY,
    compose_active_context,
    explain_active_context_packet,
    summarize_active_context_packet,
    validate_active_context_packet,
)
from hermes_memory_fabric.memory_subspace_index import create_subspace_descriptor, create_subspace_registry


NOW = "2026-05-26T00:00:00Z"


def _project_subspace(
    subspace_id: str = "project:hermes-memory-fabric",
    project_scope: str = "hermes-memory-fabric",
    **overrides,
):
    base = {
        "subspace_id": subspace_id,
        "subspace_kind": "project",
        "scope": {"project_scope": project_scope},
        "owner": "memory-fabric-team",
        "access_policy": {
            "read": "allowed",
            "write": "forbidden",
            "proposal_required_for_writes": True,
        },
        "risk_level": "low",
        "lifecycle_status": "active",
        "active_summary": "Hermes Memory Fabric active context composer project summary.",
        "source_index": {"source_ids": ["test:active-context-composer"]},
        "fact_graph_ref": {"node_id": f"fact-graph:{project_scope}"},
        "memory_blocks_ref": {"block_ids": [f"block:{project_scope}"]},
        "tags": ["memory-fabric", "active-context"],
        "priority": 10,
        "created_at": NOW,
        "updated_at": NOW,
        "last_compacted_at": None,
        "governance_status": "governed",
    }
    base.update(overrides)
    return create_subspace_descriptor(**base)


def _registry():
    return create_subspace_registry(
        [
            _project_subspace(),
            _project_subspace(
                subspace_id="project:lovart",
                project_scope="lovart",
                tags=["lovart"],
                active_summary="Lovart unrelated project summary.",
            ),
            _project_subspace(
                subspace_id="project:hermes-memory-fabric:archive",
                lifecycle_status="archived",
                active_summary="Archived Hermes Memory Fabric summary.",
            ),
        ]
    )


def _candidate(memory_id: str, **overrides):
    base = {
        "id": memory_id,
        "content": "Hermes Memory Fabric Active Context Composer keeps one bounded context packet.",
        "project_id": "hermes-memory-fabric",
        "subspace_id": "project:hermes-memory-fabric",
        "entity_ids": ["hermes-memory-fabric"],
        "created_at": "2026-05-25T10:00:00Z",
        "source": "design_doc",
        "provenance": f"test:active-context:{memory_id}",
        "risk_level": "low",
        "governance": {"read_only": True, "proposal_governed": True},
    }
    base.update(overrides)
    return base


def _packet(**overrides):
    args = {
        "query": "Hermes Memory Fabric Active Context Composer bounded context packet",
        "memory_candidates": [
            _candidate("target"),
            _candidate(
                "lovart-memory",
                content="Lovart creative memory belongs to another project.",
                project_id="lovart",
                subspace_id="project:lovart",
                entity_ids=["lovart"],
            ),
            _candidate(
                "archived-memory",
                content="Archived Hermes Memory Fabric context should stay inactive by default.",
                subspace_id="project:hermes-memory-fabric:archive",
            ),
        ],
        "subspace_registry": _registry(),
        "project_scope": "hermes-memory-fabric",
        "entity_ids": ["hermes-memory-fabric"],
        "now": NOW,
        "memory_limit": 2,
        "context_budget_chars": 1200,
    }
    args.update(overrides)
    return compose_active_context(**args)


def test_valid_packet_validates():
    packet = _packet()

    assert validate_active_context_packet(packet) == {"valid": True, "errors": []}
    assert packet["packet_type"] == "active_context_packet"
    assert packet["version"] == "0.1"


def test_policy_proves_read_only_no_writes_no_executor_no_provider_tools(tmp_path, monkeypatch):
    hermes_home = tmp_path / "hermes-home"
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))

    packet = _packet()

    assert packet["policy"] == ACTIVE_CONTEXT_COMPOSER_POLICY
    assert packet["policy"]["read_only"] is True
    assert packet["policy"]["would_write_memory"] is False
    assert packet["policy"]["would_modify_config"] is False
    assert packet["policy"]["would_write_graph"] is False
    assert packet["policy"]["writes_proposal_files"] is False
    assert packet["policy"]["writes_operation_ledger"] is False
    assert packet["policy"]["writes_token_files"] is False
    assert packet["policy"]["writes_approval_audit"] is False
    assert packet["policy"]["invokes_real_token_write_executor"] is False
    assert packet["policy"]["implements_real_token_write_executor"] is False
    assert packet["policy"]["exposes_provider_tools"] is False
    assert not (hermes_home / "memory" / "graph" / "memory_graph.sqlite").exists()
    assert not (hermes_home / "memory" / "audit" / "memory_operation_ledger.jsonl").exists()
    assert not (hermes_home / "memory" / "approval" / "approval_audit.jsonl").exists()


def test_matching_project_memory_appears_in_compact_context_text():
    packet = _packet()

    assert "Active Context Composer keeps one bounded context packet" in packet["compact_context_text"]
    assert packet["selected_memories"][0]["id"] == "target"


def test_unrelated_project_memory_is_rejected():
    packet = _packet()
    rejected = {item["id"]: item for item in packet["rejected_memories"]}

    assert rejected["lovart-memory"]["reason"] == "project_scope_mismatch"
    assert "Lovart creative memory" not in packet["compact_context_text"]


def test_archived_subspace_memory_excluded_by_default():
    packet = _packet()
    rejected = {item["id"]: item for item in packet["rejected_memories"]}

    assert rejected["archived-memory"]["reason"] == "archived_subspace_excluded"
    assert "Archived Hermes Memory Fabric context" not in packet["compact_context_text"]


def test_high_risk_memory_rejected_unless_explicitly_allowed():
    high_risk = _candidate("high-risk", risk_level="high")

    blocked = compose_active_context(
        query="Hermes Memory Fabric high risk context",
        memory_candidates=[high_risk],
        project_scope="hermes-memory-fabric",
        now=NOW,
    )
    allowed = compose_active_context(
        query="Hermes Memory Fabric high risk context",
        memory_candidates=[high_risk],
        project_scope="hermes-memory-fabric",
        allowed_risk_levels=["high"],
        now=NOW,
    )

    assert blocked["rejected_memories"][0]["reason"] == "risk_level_not_allowed:high"
    assert allowed["selected_memories"][0]["id"] == "high-risk"


def test_context_budget_chars_limits_context_size():
    packet = _packet(context_budget_chars=80)

    assert len(packet["compact_context_text"]) <= 80
    assert packet["budget"]["context_budget_chars"] == 80
    assert validate_active_context_packet(packet)["valid"] is True


def test_composer_does_not_mutate_input_candidates_registry_or_context():
    candidates = [_candidate("target"), _candidate("archived-memory", subspace_id="project:hermes-memory-fabric:archive")]
    registry = _registry()
    context = {"project_scope": "hermes-memory-fabric", "query": "active context"}
    original_candidates = deepcopy(candidates)
    original_registry = deepcopy(registry)
    original_context = deepcopy(context)

    compose_active_context(
        query="Hermes Memory Fabric Active Context Composer",
        memory_candidates=candidates,
        subspace_registry=registry,
        context=context,
        project_scope="hermes-memory-fabric",
        now=NOW,
    )

    assert candidates == original_candidates
    assert registry == original_registry
    assert context == original_context


def test_selected_and_rejected_explanations_are_present():
    packet = _packet()
    explanation = explain_active_context_packet(packet)

    assert explanation["selected_memory_ids"] == ["target"]
    assert {"lovart-memory", "archived-memory"}.issubset(set(explanation["rejected_memory_ids"]))
    assert explanation["selected_subspace_ids"] == ["project:hermes-memory-fabric"]
    assert {"project:lovart", "project:hermes-memory-fabric:archive"}.issubset(
        set(explanation["rejected_subspace_ids"])
    )
    assert explanation["selection_rejection_explanation"]["selected_memories"]["target"]
    assert explanation["selection_rejection_explanation"]["rejected_memories"]["lovart-memory"] == (
        "project_scope_mismatch"
    )
    assert explanation["selection_rejection_explanation"]["subspace_rejected_reasons"][
        "project:hermes-memory-fabric:archive"
    ] == ["archived_excluded"]


def test_deduplication_prevents_duplicate_context_items():
    duplicate_text = "Hermes Memory Fabric Active Context Composer duplicate text."
    packet = compose_active_context(
        query="Hermes Memory Fabric Active Context Composer duplicate text",
        memory_candidates=[
            _candidate("duplicate-a", content=duplicate_text, provenance=None, source="same-source"),
            _candidate("duplicate-b", content=duplicate_text, provenance=None, source="same-source"),
        ],
        subspace_registry=create_subspace_registry([_project_subspace()]),
        project_scope="hermes-memory-fabric",
        now=NOW,
        memory_limit=2,
    )

    memory_items = [item for item in packet["context_items"] if item["item_type"] == "memory"]
    assert [item["source_id"] for item in memory_items] == ["same-source"]
    assert packet["compact_context_text"].count(duplicate_text) == 1


def test_summary_counts_are_correct():
    packet = _packet()
    summary = summarize_active_context_packet(packet)

    assert summary["selected_memory_count"] == 1
    assert summary["rejected_memory_count"] == 2
    assert summary["selected_subspace_count"] == 1
    assert summary["rejected_subspace_count"] == 2
    assert summary["context_item_count"] == len(packet["context_items"])
    assert summary["used_budget"] == len(packet["compact_context_text"])


def test_validate_rejects_missing_required_fields():
    packet = _packet()
    del packet["packet_type"]

    validity = validate_active_context_packet(packet)

    assert validity["valid"] is False
    assert "missing_packet_type" in validity["errors"]
    assert "packet_type_must_be_active_context_packet" in validity["errors"]
