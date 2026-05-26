from __future__ import annotations

from copy import deepcopy

from benchmarks.hermes_memory_bench.core import DIMENSIONS, _answer_case
from hermes_memory_fabric.memory_subspace_index import (
    MEMORY_SUBSPACE_INDEX_POLICY,
    REQUIRED_POLICY_FIELDS,
    REQUIRED_SUBSPACE_DESCRIPTOR_FIELDS,
    add_subspace_to_registry,
    create_subspace_descriptor,
    create_subspace_registry,
    explain_subspace_selection,
    resolve_subspace,
    select_subspaces_for_context,
    summarize_subspace_registry,
    validate_subspace_descriptor,
    validate_subspace_registry,
)


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
        "active_summary": "Project-scoped Memory Fabric domain.",
        "source_index": {"source_ids": ["episode:subspace-index"]},
        "fact_graph_ref": {"node_id": f"fact-graph:{project_scope}"},
        "memory_blocks_ref": {"block_ids": [f"block:{project_scope}"]},
        "tags": ["memory-fabric", "subspace-index"],
        "priority": 10,
        "created_at": "2026-05-26T00:00:00Z",
        "updated_at": "2026-05-26T00:00:00Z",
        "last_compacted_at": None,
        "governance_status": "governed",
    }
    base.update(overrides)
    return create_subspace_descriptor(**base)


def _agent_subspace():
    return create_subspace_descriptor(
        subspace_id="agent:codex",
        subspace_kind="agent",
        scope={"agent_scope": "codex"},
        owner="memory-fabric-team",
        risk_level="low",
        lifecycle_status="active",
        active_summary="Codex agent working-memory domain.",
        source_index={"source_ids": ["episode:codex"]},
        fact_graph_ref={"node_id": "fact-graph:codex"},
        memory_blocks_ref={"block_ids": ["block:codex"]},
        tags=["codex"],
        priority=4,
        created_at="2026-05-26T00:00:00Z",
        updated_at="2026-05-26T00:00:00Z",
        last_compacted_at=None,
        governance_status="governed",
    )


def test_valid_project_subspace_descriptor_validates():
    subspace = _project_subspace()

    validity = validate_subspace_descriptor(subspace)

    assert validity == {"valid": True, "errors": []}
    for field in REQUIRED_SUBSPACE_DESCRIPTOR_FIELDS:
        assert field in subspace
    for field in REQUIRED_POLICY_FIELDS:
        assert field in subspace["policy"]


def test_invalid_missing_subspace_id_fails_validation():
    subspace = _project_subspace()
    del subspace["subspace_id"]

    validity = validate_subspace_descriptor(subspace)

    assert validity["valid"] is False
    assert "missing_subspace_id" in validity["errors"]


def test_registry_validates_with_multiple_subspaces():
    registry = create_subspace_registry([_project_subspace(), _agent_subspace()])

    assert validate_subspace_registry(registry) == {"valid": True, "errors": []}


def test_add_subspace_does_not_mutate_original_registry():
    registry = create_subspace_registry([_project_subspace()])
    original = deepcopy(registry)

    updated = add_subspace_to_registry(registry, _agent_subspace())

    assert registry == original
    assert len(registry["subspaces"]) == 1
    assert len(updated["subspaces"]) == 2


def test_resolve_subspace_returns_the_right_descriptor_copy():
    registry = create_subspace_registry([_project_subspace(), _agent_subspace()])

    resolved = resolve_subspace(registry, "agent:codex")
    assert resolved is not None
    resolved["owner"] = "changed"

    assert resolved["subspace_id"] == "agent:codex"
    assert resolve_subspace(registry, "agent:codex")["owner"] == "memory-fabric-team"


def test_exact_project_scope_gets_selected():
    registry = create_subspace_registry([_project_subspace()])

    selection = select_subspaces_for_context(
        registry,
        {"project_scope": "hermes-memory-fabric", "query": "subspace index"},
    )

    assert [item["subspace_id"] for item in selection["selected_subspaces"]] == [
        "project:hermes-memory-fabric"
    ]
    assert selection["selection_reasons"]["project:hermes-memory-fabric"][0] == "project_scope_exact_match"


def test_unrelated_project_subspace_gets_rejected():
    matching = _project_subspace()
    unrelated = _project_subspace(
        subspace_id="project:lovart",
        project_scope="lovart",
        tags=["lovart"],
    )
    registry = create_subspace_registry([unrelated, matching])

    selection = select_subspaces_for_context(registry, {"project_scope": "hermes-memory-fabric"})

    assert [item["subspace_id"] for item in selection["selected_subspaces"]] == [
        "project:hermes-memory-fabric"
    ]
    assert selection["rejected_reasons"]["project:lovart"] == ["project_scope_mismatch"]


def test_archived_subspace_rejected_by_default():
    archived = _project_subspace(lifecycle_status="archived")
    registry = create_subspace_registry([archived])

    selection = select_subspaces_for_context(registry, {"project_scope": "hermes-memory-fabric"})

    assert selection["selected_subspaces"] == []
    assert selection["rejected_reasons"]["project:hermes-memory-fabric"] == ["archived_excluded"]


def test_archived_subspace_selected_only_when_include_archived_true():
    archived = _project_subspace(lifecycle_status="archived")
    registry = create_subspace_registry([archived])

    selection = select_subspaces_for_context(
        registry,
        {"project_scope": "hermes-memory-fabric", "include_archived": True},
    )

    assert [item["subspace_id"] for item in selection["selected_subspaces"]] == [
        "project:hermes-memory-fabric"
    ]


def test_high_risk_subspace_rejected_unless_allowed():
    high_risk = _project_subspace(risk_level="high")
    registry = create_subspace_registry([high_risk])

    default_selection = select_subspaces_for_context(registry, {"project_scope": "hermes-memory-fabric"})
    allowed_selection = select_subspaces_for_context(
        registry,
        {
            "project_scope": "hermes-memory-fabric",
            "allowed_risk_levels": ["high"],
        },
    )

    assert default_selection["selected_subspaces"] == []
    assert default_selection["rejected_reasons"]["project:hermes-memory-fabric"] == [
        "risk_level_not_allowed:high"
    ]
    assert [item["subspace_id"] for item in allowed_selection["selected_subspaces"]] == [
        "project:hermes-memory-fabric"
    ]


def test_max_active_subspaces_limits_activation():
    high_priority = _project_subspace(subspace_id="project:hermes-memory-fabric:primary", priority=20)
    low_priority = _project_subspace(subspace_id="project:hermes-memory-fabric:secondary", priority=1)
    registry = create_subspace_registry([low_priority, high_priority])

    selection = select_subspaces_for_context(
        registry,
        {"project_scope": "hermes-memory-fabric", "max_active_subspaces": 1},
    )

    assert [item["subspace_id"] for item in selection["selected_subspaces"]] == [
        "project:hermes-memory-fabric:primary"
    ]
    assert selection["rejected_reasons"]["project:hermes-memory-fabric:secondary"][0] == (
        "ranked_below_active_context_budget"
    )


def test_required_tags_filter_selection():
    tagged = _project_subspace(subspace_id="project:hermes-memory-fabric:docs", tags=["docs", "memory-fabric"])
    untagged = _project_subspace(subspace_id="project:hermes-memory-fabric:runtime", tags=["runtime"])
    registry = create_subspace_registry([tagged, untagged])

    selection = select_subspaces_for_context(
        registry,
        {"project_scope": "hermes-memory-fabric", "required_tags": ["docs"]},
    )

    assert [item["subspace_id"] for item in selection["selected_subspaces"]] == [
        "project:hermes-memory-fabric:docs"
    ]
    assert selection["rejected_reasons"]["project:hermes-memory-fabric:runtime"] == [
        "missing_required_tags:docs"
    ]


def test_selection_explanation_is_deterministic():
    registry = create_subspace_registry([_project_subspace(), _agent_subspace()])
    context = {
        "project_scope": "hermes-memory-fabric",
        "agent_scope": "codex",
        "query": "codex memory fabric",
    }

    explanation_a = explain_subspace_selection(select_subspaces_for_context(registry, context))
    explanation_b = explain_subspace_selection(select_subspaces_for_context(registry, context))

    assert explanation_a == explanation_b
    assert explanation_a["policy"] == MEMORY_SUBSPACE_INDEX_POLICY


def test_summary_counts_by_scope_lifecycle_risk_and_governance():
    registry = create_subspace_registry(
        [
            _project_subspace(),
            _project_subspace(
                subspace_id="project:hermes-memory-fabric:archive",
                lifecycle_status="archived",
                risk_level="medium",
                governance_status="review_required",
            ),
            _agent_subspace(),
        ]
    )

    summary = summarize_subspace_registry(registry)

    assert summary["by_scope"] == {"agent:codex": 1, "project:hermes-memory-fabric": 2}
    assert summary["by_lifecycle_status"] == {"active": 2, "archived": 1}
    assert summary["by_risk_level"] == {"low": 2, "medium": 1}
    assert summary["by_governance_status"] == {"governed": 2, "review_required": 1}


def test_policy_proves_read_only_no_writes_no_executor_no_provider_tools(tmp_path, monkeypatch):
    hermes_home = tmp_path / "hermes-home"
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))
    registry = create_subspace_registry([_project_subspace()])
    selection = select_subspaces_for_context(registry, {"project_scope": "hermes-memory-fabric"})

    for policy in (MEMORY_SUBSPACE_INDEX_POLICY, registry["policy"], selection["policy"]):
        assert policy["read_only"] is True
        assert policy["would_write_memory"] is False
        assert policy["would_modify_config"] is False
        assert policy["would_write_graph"] is False
        assert policy["writes_proposal_files"] is False
        assert policy["writes_operation_ledger"] is False
        assert policy["writes_token_files"] is False
        assert policy["writes_approval_audit"] is False
        assert policy["invokes_real_token_write_executor"] is False
        assert policy["implements_real_token_write_executor"] is False
        assert policy["exposes_provider_tools"] is False

    assert not (hermes_home / "memory" / "graph" / "memory_graph.sqlite").exists()
    assert not (hermes_home / "memory" / "audit" / "memory_operation_ledger.jsonl").exists()
    assert not (hermes_home / "memory" / "proposals" / "memory_write_proposals.jsonl").exists()


def test_benchmark_smoke_case_covers_memory_subspace_index():
    case = {
        "id": "memory_subspace_index_project_selection",
        "dimension": "memory_subspace_index",
        "query": "Which subspace should activate for Hermes Memory Fabric?",
        "expected_answer": "subspace_index_selection_passed",
        "context": {
            "project_scope": "hermes-memory-fabric",
            "query": "memory fabric subspace index",
        },
        "expected_selected_subspace_ids": ["project:hermes-memory-fabric"],
        "expected_rejected_subspace_ids": ["project:lovart", "project:hermes-memory-fabric:archive"],
        "subspaces": [
            _project_subspace(),
            _project_subspace(subspace_id="project:lovart", project_scope="lovart"),
            _project_subspace(
                subspace_id="project:hermes-memory-fabric:archive",
                lifecycle_status="archived",
            ),
        ],
    }

    actual, evidence = _answer_case(case)

    assert "memory_subspace_index" in DIMENSIONS
    assert actual == "subspace_index_selection_passed"
    assert evidence["selected_subspace_ids"] == ["project:hermes-memory-fabric"]
    assert set(evidence["rejected_subspace_ids"]) == {
        "project:hermes-memory-fabric:archive",
        "project:lovart",
    }
    assert evidence["policy"] == MEMORY_SUBSPACE_INDEX_POLICY
