from copy import deepcopy

from benchmarks.hermes_memory_bench.core import DIMENSIONS, _answer_case
from hermes_memory_fabric.memory_retrieval_fusion import (
    FUSION_POLICY,
    FUSION_POLICY_V2,
    SCORING_DIMENSIONS_V2,
    explain_memory_retrieval_v2_result,
    fuse_memory_retrieval,
    fuse_memory_retrieval_v2,
    summarize_memory_retrieval_v2_result,
)
from hermes_memory_fabric.memory_subspace_index import create_subspace_descriptor, create_subspace_registry


NOW = "2026-05-23T00:00:00Z"


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
        "active_summary": "Hermes Memory Fabric project subspace.",
        "source_index": {"source_ids": ["test:recall-fusion-v2"]},
        "fact_graph_ref": {"node_id": f"fact-graph:{project_scope}"},
        "memory_blocks_ref": {"block_ids": [f"block:{project_scope}"]},
        "tags": ["memory-fabric", "recall-fusion"],
        "priority": 10,
        "created_at": "2026-05-23T00:00:00Z",
        "updated_at": "2026-05-23T00:00:00Z",
        "last_compacted_at": None,
        "governance_status": "governed",
    }
    base.update(overrides)
    return create_subspace_descriptor(**base)


def _candidate(memory_id: str, **overrides):
    base = {
        "id": memory_id,
        "content": "Hermes Memory Fabric should use Recall Fusion v2.",
        "project_id": "hermes-memory-fabric",
        "subspace_id": "project:hermes-memory-fabric",
        "entity_ids": ["hermes-memory-fabric"],
        "created_at": "2026-05-22T10:00:00Z",
        "source": "design_doc",
        "provenance": f"test:{memory_id}",
        "risk_level": "low",
        "governance": {"read_only": True, "proposal_governed": True},
    }
    base.update(overrides)
    return base


def test_exact_keyword_recall_beats_unrelated_text():
    result = fuse_memory_retrieval(
        query="graphite dashboard theme",
        candidates=[
            {"id": "unrelated", "content": "Use staging for OpenClaw.", "created_at": "2026-05-22T00:00:00Z"},
            {
                "id": "theme",
                "content": "Han prefers graphite dashboard theme.",
                "created_at": "2026-05-22T00:00:00Z",
            },
        ],
        now=NOW,
    )

    assert result["selected_memories"][0]["id"] == "theme"
    assert result["scores"]["theme"]["keyword_score"] > result["scores"]["unrelated"]["keyword_score"]


def test_project_scope_isolation_rejects_unrelated_project():
    result = fuse_memory_retrieval(
        query="deployment target",
        project_scope="openclaw",
        candidates=[
            {"id": "lovart", "content": "Use production deployment target.", "project_id": "lovart"},
            {"id": "openclaw", "content": "Use staging deployment target.", "project_id": "openclaw"},
        ],
        now=NOW,
    )

    assert result["selected_memories"][0]["id"] == "openclaw"
    rejected = {item["id"]: item for item in result["rejected_memories"]}
    assert rejected["lovart"]["reason"] == "project_scope_mismatch"


def test_newer_valid_preference_beats_older_expired_preference():
    result = fuse_memory_retrieval(
        query="release note tone",
        project_scope="hermes-agent",
        candidates=[
            {
                "id": "old",
                "content": "Use expansive release note tone.",
                "project_id": "hermes-agent",
                "valid_until": "2026-05-10T00:00:00Z",
                "created_at": "2026-05-01T00:00:00Z",
            },
            {
                "id": "new",
                "content": "Use terse release note tone.",
                "project_id": "hermes-agent",
                "valid_from": "2026-05-22T00:00:00Z",
                "created_at": "2026-05-22T00:00:00Z",
            },
        ],
        now=NOW,
    )

    assert result["selected_memories"][0]["id"] == "new"
    assert result["scores"]["new"]["temporal_score"] > result["scores"]["old"]["temporal_score"]


def test_provenance_bearing_source_wins_when_content_is_similar():
    result = fuse_memory_retrieval(
        query="durable memory updates governed proposals",
        candidates=[
            {
                "id": "untrusted",
                "content": "Durable memory updates require governed proposals.",
                "source": "chat",
            },
            {
                "id": "trusted",
                "content": "Durable memory updates require governed proposals.",
                "source": "policy_doc",
                "provenance": "memory-fabric-policy:v1",
            },
        ],
        now=NOW,
    )

    assert result["selected_memories"][0]["id"] == "trusted"
    assert result["scores"]["trusted"]["source_trust_score"] > result["scores"]["untrusted"]["source_trust_score"]


def test_unsafe_governance_candidate_is_rejected():
    result = fuse_memory_retrieval(
        query="direct durable memory write",
        candidates=[
            {
                "id": "unsafe",
                "content": "Direct durable memory write is allowed.",
                "governance": {"would_write_memory": True},
            },
            {
                "id": "safe",
                "content": "Direct durable memory writes require governed proposals.",
                "governance": {"read_only": True, "proposal_governed": True},
            },
        ],
        now=NOW,
    )

    assert result["selected_memories"][0]["id"] == "safe"
    rejected = {item["id"]: item for item in result["rejected_memories"]}
    assert rejected["unsafe"]["reason"].startswith("unsafe_governance")
    assert rejected["unsafe"]["component_scores"]["governance_score"] == 0.0


def test_rejected_memories_explain_why_items_lost():
    result = fuse_memory_retrieval(
        query="Hermes memory retrieval fusion",
        candidates=[
            {"id": "winner", "content": "Hermes memory retrieval fusion is enabled."},
            {"id": "loser", "content": "Calendar sync is enabled."},
        ],
        now=NOW,
        limit=1,
    )

    rejected = {item["id"]: item for item in result["rejected_memories"]}
    assert "loser" in rejected
    assert rejected["loser"]["reason"] in {"below_selection_threshold", "ranked_below_limit"}
    assert "final_score" in rejected["loser"]
    assert "component_scores" in rejected["loser"]


def test_policy_proves_read_only_and_no_memory_config_or_graph_writes():
    result = fuse_memory_retrieval(query="policy", candidates=[], now=NOW)

    assert result["policy"] == FUSION_POLICY
    assert result["policy"]["read_only"] is True
    assert result["policy"]["would_write_memory"] is False
    assert result["policy"]["would_modify_config"] is False
    assert result["policy"]["would_write_graph"] is False
    assert result["policy"]["does_not_create_operation_events"] is True


def test_v2_selects_candidate_from_matching_selected_subspace():
    registry = create_subspace_registry([_project_subspace()])
    result = fuse_memory_retrieval_v2(
        query="Recall Fusion v2",
        candidates=[
            _candidate("project-only", subspace_id=None),
            _candidate("direct-subspace"),
        ],
        subspace_registry=registry,
        project_scope="hermes-memory-fabric",
        entity_ids=["hermes-memory-fabric"],
        now=NOW,
    )

    assert result["selected_memories"][0]["id"] == "direct-subspace"
    assert result["scores"]["direct-subspace"]["subspace_score"] > result["scores"]["project-only"]["subspace_score"]
    assert result["selected_subspaces"][0]["subspace_id"] == "project:hermes-memory-fabric"


def test_v2_rejects_unrelated_project_candidate():
    registry = create_subspace_registry([_project_subspace()])
    result = fuse_memory_retrieval_v2(
        query="Recall Fusion v2",
        candidates=[
            _candidate("lovart", project_id="lovart", subspace_id="project:lovart"),
            _candidate("hermes"),
        ],
        subspace_registry=registry,
        project_scope="hermes-memory-fabric",
        now=NOW,
    )

    rejected = {item["id"]: item for item in result["rejected_memories"]}
    assert rejected["lovart"]["reason"] == "project_scope_mismatch"
    assert rejected["lovart"]["component_scores"]["project_scope_score"] == 0.0


def test_v2_rejects_archived_subspace_candidate_by_default():
    archived = _project_subspace(
        subspace_id="project:hermes-memory-fabric:archive",
        lifecycle_status="archived",
    )
    registry = create_subspace_registry([archived])
    result = fuse_memory_retrieval_v2(
        query="Recall Fusion v2",
        candidates=[_candidate("archived", subspace_id="project:hermes-memory-fabric:archive")],
        subspace_registry=registry,
        project_scope="hermes-memory-fabric",
        now=NOW,
    )

    assert result["selected_memories"] == []
    rejected = {item["id"]: item for item in result["rejected_memories"]}
    assert rejected["archived"]["reason"] == "archived_subspace_excluded"
    assert result["subspace_rejected_reasons"]["project:hermes-memory-fabric:archive"] == ["archived_excluded"]


def test_v2_allows_archived_subspace_candidate_only_when_included():
    archived = _project_subspace(
        subspace_id="project:hermes-memory-fabric:archive",
        lifecycle_status="archived",
    )
    registry = create_subspace_registry([archived])

    result = fuse_memory_retrieval_v2(
        query="Recall Fusion v2",
        candidates=[_candidate("archived", subspace_id="project:hermes-memory-fabric:archive")],
        subspace_registry=registry,
        project_scope="hermes-memory-fabric",
        include_archived=True,
        now=NOW,
    )

    assert result["selected_memories"][0]["id"] == "archived"
    assert result["selected_subspaces"][0]["subspace_id"] == "project:hermes-memory-fabric:archive"


def test_v2_rejects_high_risk_candidate_unless_allowed():
    high_risk = _candidate("high-risk", risk_level="high")

    blocked = fuse_memory_retrieval_v2(query="Recall Fusion v2", candidates=[high_risk], now=NOW)
    allowed = fuse_memory_retrieval_v2(
        query="Recall Fusion v2",
        candidates=[high_risk],
        allowed_risk_levels=["high"],
        now=NOW,
    )

    assert blocked["rejected_memories"][0]["reason"] == "risk_level_not_allowed:high"
    assert allowed["selected_memories"][0]["id"] == "high-risk"


def test_v2_required_tags_affects_active_subspace_selection():
    docs = _project_subspace(
        subspace_id="project:hermes-memory-fabric:docs",
        tags=["docs", "memory-fabric"],
        priority=9,
    )
    runtime = _project_subspace(
        subspace_id="project:hermes-memory-fabric:runtime",
        tags=["runtime"],
        priority=20,
    )
    registry = create_subspace_registry([runtime, docs])

    result = fuse_memory_retrieval_v2(
        query="Recall Fusion v2",
        candidates=[
            _candidate("runtime", subspace_id="project:hermes-memory-fabric:runtime"),
            _candidate("docs", subspace_id="project:hermes-memory-fabric:docs"),
        ],
        subspace_registry=registry,
        project_scope="hermes-memory-fabric",
        required_tags=["docs"],
        limit=1,
        now=NOW,
    )

    assert [item["subspace_id"] for item in result["selected_subspaces"]] == [
        "project:hermes-memory-fabric:docs"
    ]
    assert result["selected_memories"][0]["id"] == "docs"
    assert result["subspace_rejected_reasons"]["project:hermes-memory-fabric:runtime"] == [
        "missing_required_tags:docs"
    ]


def test_v2_selected_memory_includes_why_selected():
    registry = create_subspace_registry([_project_subspace()])
    result = fuse_memory_retrieval_v2(
        query="Recall Fusion v2",
        candidates=[_candidate("selected")],
        subspace_registry=registry,
        project_scope="hermes-memory-fabric",
        entity_ids=["hermes-memory-fabric"],
        now=NOW,
    )

    why_selected = result["selected_memories"][0]["why_selected"]
    assert any(reason.startswith("selected_subspace_") for reason in why_selected)
    assert "keyword_overlap" in why_selected


def test_v2_rejected_memory_includes_reason_and_component_scores():
    result = fuse_memory_retrieval_v2(
        query="Recall Fusion v2",
        candidates=[
            _candidate("winner"),
            _candidate("loser", content="Calendar sync is enabled.", provenance=None, source=None),
        ],
        limit=1,
        now=NOW,
    )

    rejected = {item["id"]: item for item in result["rejected_memories"]}
    assert rejected["loser"]["reason"] in {"below_selection_threshold", "ranked_below_limit"}
    assert set(SCORING_DIMENSIONS_V2[:-1]).issubset(rejected["loser"]["component_scores"])


def test_v2_explanation_includes_selected_and_rejected_subspaces():
    active = _project_subspace()
    archived = _project_subspace(
        subspace_id="project:hermes-memory-fabric:archive",
        lifecycle_status="archived",
    )
    registry = create_subspace_registry([active, archived])

    result = fuse_memory_retrieval_v2(
        query="Recall Fusion v2",
        candidates=[_candidate("selected")],
        subspace_registry=registry,
        project_scope="hermes-memory-fabric",
        now=NOW,
    )
    explanation = explain_memory_retrieval_v2_result(result)

    assert explanation["selected_subspace_ids"] == ["project:hermes-memory-fabric"]
    assert explanation["rejected_subspace_ids"] == ["project:hermes-memory-fabric:archive"]
    assert result["explanation"] == explanation


def test_v2_summary_counts_selected_and_rejected_memories():
    result = fuse_memory_retrieval_v2(
        query="Recall Fusion v2",
        candidates=[
            _candidate("winner"),
            _candidate("rejected", project_id="lovart"),
        ],
        project_scope="hermes-memory-fabric",
        now=NOW,
    )

    summary = summarize_memory_retrieval_v2_result(result)

    assert summary["selected_memory_count"] == 1
    assert summary["rejected_memory_count"] == 1
    assert summary["top_selected_memory_id"] == "winner"


def test_v2_does_not_mutate_candidates_or_registry():
    registry = create_subspace_registry(
        [
            _project_subspace(),
            _project_subspace(
                subspace_id="project:hermes-memory-fabric:archive",
                lifecycle_status="archived",
            ),
        ]
    )
    candidates = [
        _candidate("selected", governance={"read_only": True, "proposal_governed": True}),
        _candidate("archived", subspace_id="project:hermes-memory-fabric:archive"),
    ]
    original_registry = deepcopy(registry)
    original_candidates = deepcopy(candidates)

    fuse_memory_retrieval_v2(
        query="Recall Fusion v2",
        candidates=candidates,
        subspace_registry=registry,
        project_scope="hermes-memory-fabric",
        now=NOW,
    )

    assert registry == original_registry
    assert candidates == original_candidates


def test_v2_policy_proves_read_only_no_writes_no_executor_no_provider_tools(tmp_path, monkeypatch):
    hermes_home = tmp_path / "hermes-home"
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))

    result = fuse_memory_retrieval_v2(query="policy", candidates=[], now=NOW)

    assert result["policy"] == FUSION_POLICY_V2
    assert result["policy"]["read_only"] is True
    assert result["policy"]["would_write_memory"] is False
    assert result["policy"]["would_modify_config"] is False
    assert result["policy"]["would_write_graph"] is False
    assert result["policy"]["writes_proposal_files"] is False
    assert result["policy"]["writes_operation_ledger"] is False
    assert result["policy"]["writes_token_files"] is False
    assert result["policy"]["writes_approval_audit"] is False
    assert result["policy"]["invokes_real_token_write_executor"] is False
    assert result["policy"]["implements_real_token_write_executor"] is False
    assert result["policy"]["exposes_provider_tools"] is False

    assert not (hermes_home / "memory" / "graph" / "memory_graph.sqlite").exists()
    assert not (hermes_home / "memory" / "audit" / "memory_operation_ledger.jsonl").exists()
    assert not (hermes_home / "memory" / "proposals" / "memory_write_proposals.jsonl").exists()
    assert not (hermes_home / "memory" / "approval" / "approval_audit.jsonl").exists()


def test_benchmark_smoke_case_covers_memory_recall_fusion_v2():
    case = {
        "id": "memory_recall_fusion_v2_subspace_guarded_selection",
        "dimension": "memory_recall_fusion_v2",
        "query": "Which memory should Recall Fusion v2 activate?",
        "project_scope": "hermes-memory-fabric",
        "entity_ids": ["hermes-memory-fabric"],
        "now": NOW,
        "limit": 1,
        "expected_answer": "memory_recall_fusion_v2_passed",
        "expected_top_selected_memory_id": "fusion-v2-current",
        "expected_rejected_memory_ids": ["fusion-v2-archived", "lovart-unrelated"],
        "expected_selected_subspace_ids": ["project:hermes-memory-fabric"],
        "expected_rejected_subspace_ids": ["project:hermes-memory-fabric:archive", "project:lovart"],
        "context": {"project_scope": "hermes-memory-fabric", "query": "recall fusion v2"},
        "memories": [
            _candidate("lovart-unrelated", project_id="lovart", subspace_id="project:lovart"),
            _candidate("fusion-v2-current"),
            _candidate("fusion-v2-archived", subspace_id="project:hermes-memory-fabric:archive"),
        ],
        "subspaces": [
            _project_subspace(),
            _project_subspace(subspace_id="project:lovart", project_scope="lovart", tags=["lovart"]),
            _project_subspace(
                subspace_id="project:hermes-memory-fabric:archive",
                lifecycle_status="archived",
            ),
        ],
    }

    actual, evidence = _answer_case(case)

    assert "memory_recall_fusion_v2" in DIMENSIONS
    assert actual == "memory_recall_fusion_v2_passed"
    assert evidence["selected_memory_ids"] == ["fusion-v2-current"]
    assert set(evidence["rejected_memory_ids"]) == {"fusion-v2-archived", "lovart-unrelated"}
    assert evidence["selected_subspace_ids"] == ["project:hermes-memory-fabric"]
    assert set(evidence["rejected_subspace_ids"]) == {"project:hermes-memory-fabric:archive", "project:lovart"}
    assert evidence["writes_operation_ledger"] is False
    assert evidence["writes_token_files"] is False
    assert evidence["writes_approval_audit"] is False
    assert evidence["invokes_real_token_write_executor"] is False
