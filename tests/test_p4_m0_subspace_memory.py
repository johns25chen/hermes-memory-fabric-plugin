from __future__ import annotations

import tomllib

import pytest

from hermes_memory_fabric.p4_m0_subspace_memory import SubspaceMemoryStore


def test_proposing_memory_creates_pending_proposal_and_audit_event(tmp_path):
    store = SubspaceMemoryStore(tmp_path)

    proposal = store.propose_memory(
        project="hermes-memory-fabric",
        namespace="governance",
        content="Approved memories require explicit human approval.",
        source="unit-test",
        tags=["approval", "governance"],
        confidence=0.9,
    )

    assert proposal.status == "pending"
    assert proposal.kind == "subspace_memory_proposal"
    assert proposal.project == "hermes-memory-fabric"
    assert proposal.namespace == "governance"
    assert (tmp_path / "proposals.jsonl").exists()
    events = store.list_audit_events()
    assert [event.event_type for event in events] == ["proposal_created"]
    assert events[0].target_id == proposal.id


def test_approving_proposal_creates_approved_memory_and_audit_event(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    proposal = store.propose_memory(
        project="hermes-memory-fabric",
        namespace="runtime",
        content="Subspace runtime stores approved memory locally.",
    )

    memory = store.approve_proposal(proposal.id, approver="human", note="approved")

    assert memory.status == "approved"
    assert memory.proposal_id == proposal.id
    assert memory.approver == "human"
    assert (tmp_path / "memories.jsonl").exists()
    assert [event.event_type for event in store.list_audit_events()] == [
        "proposal_created",
        "proposal_approved",
    ]
    with pytest.raises(ValueError, match="proposal_not_pending:approved"):
        store.approve_proposal(proposal.id, approver="human")


def test_rejected_proposal_is_not_recalled(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    proposal = store.propose_memory(
        project="hermes-memory-fabric",
        namespace="runtime",
        content="Rejected memory must not become recallable.",
    )

    rejected = store.reject_proposal(proposal.id, reviewer="human", reason="not suitable")

    assert rejected.status == "rejected"
    assert store.recall("Rejected", project="hermes-memory-fabric", namespace="runtime") == []
    assert [event.event_type for event in store.list_audit_events()] == [
        "proposal_created",
        "proposal_rejected",
    ]


def test_approved_memory_is_recalled_by_keyword_with_explainable_structure(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    proposal = store.propose_memory(
        project="hermes-memory-fabric",
        namespace="runtime",
        content="Keyword recall returns deterministic matched terms.",
        source="local-test",
    )
    memory = store.approve_proposal(proposal.id, approver="human")

    results = store.recall("keyword deterministic missing", project="hermes-memory-fabric")

    assert len(results) == 1
    assert results[0].memory_id == memory.id
    assert results[0].score == 2
    assert results[0].matched_terms == ("keyword", "deterministic")
    assert results[0].content == "Keyword recall returns deterministic matched terms."
    assert results[0].project == "hermes-memory-fabric"
    assert results[0].namespace == "runtime"
    assert results[0].source == "local-test"


def test_project_isolation_works(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    matching = store.propose_memory(
        project="alpha",
        namespace="runtime",
        content="Isolation keyword belongs to alpha.",
    )
    other = store.propose_memory(
        project="beta",
        namespace="runtime",
        content="Isolation keyword belongs to beta.",
    )
    alpha_memory = store.approve_proposal(matching.id, approver="human")
    store.approve_proposal(other.id, approver="human")

    results = store.recall("isolation", project="alpha")

    assert [result.memory_id for result in results] == [alpha_memory.id]
    assert results[0].project == "alpha"


def test_namespace_isolation_works(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    matching = store.propose_memory(
        project="hermes-memory-fabric",
        namespace="runtime",
        content="Namespace keyword belongs to runtime.",
    )
    other = store.propose_memory(
        project="hermes-memory-fabric",
        namespace="docs",
        content="Namespace keyword belongs to docs.",
    )
    runtime_memory = store.approve_proposal(matching.id, approver="human")
    store.approve_proposal(other.id, approver="human")

    results = store.recall("namespace", project="hermes-memory-fabric", namespace="runtime")

    assert [result.memory_id for result in results] == [runtime_memory.id]
    assert results[0].namespace == "runtime"


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"project": "", "namespace": "runtime", "content": "x"}, "project_must_be_non_empty"),
        ({"project": "p", "namespace": "", "content": "x"}, "namespace_must_be_non_empty"),
        ({"project": "p", "namespace": "n", "content": ""}, "content_must_be_non_empty"),
    ],
)
def test_empty_content_project_namespace_validation_works(tmp_path, kwargs, message):
    store = SubspaceMemoryStore(tmp_path)

    with pytest.raises(ValueError, match=message):
        store.propose_memory(**kwargs)


def test_empty_query_validation_works(tmp_path):
    store = SubspaceMemoryStore(tmp_path)

    with pytest.raises(ValueError, match="query_must_be_non_empty"):
        store.recall("")


def test_approval_of_missing_proposal_is_rejected(tmp_path):
    store = SubspaceMemoryStore(tmp_path)

    with pytest.raises(ValueError, match="proposal_not_found"):
        store.approve_proposal("proposal:missing", approver="human")


def test_runtime_only_uses_fixed_files_under_explicit_storage_root(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    proposal = store.propose_memory(project="p", namespace="n", content="fixed local files only")
    store.approve_proposal(proposal.id, approver="human")

    assert sorted(path.name for path in tmp_path.iterdir()) == [
        "audit.jsonl",
        "memories.jsonl",
        "proposals.jsonl",
    ]


def test_approved_memory_storage_survives_store_reopen(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    proposal = store.propose_memory(
        project="hermes-memory-fabric",
        namespace="runtime",
        content="Reopened store can recall approved local memory.",
        tags=["reopen"],
    )
    memory = store.approve_proposal(proposal.id, approver="human")
    reopened = SubspaceMemoryStore(tmp_path)

    results = reopened.recall("reopened", project="hermes-memory-fabric", namespace="runtime")

    assert [result.memory_id for result in results] == [memory.id]


def test_no_uv_lock_is_created():
    assert not __import__("pathlib").Path("uv.lock").exists()


def test_package_version_remains_6_16_0():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert pyproject["project"]["version"] == "6.16.0"
