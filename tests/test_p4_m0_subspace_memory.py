from __future__ import annotations

import tomllib
import hashlib
import json

import pytest

from hermes_memory_fabric.p4_m0_subspace_memory import (
    SubspaceMemoryStore as _ProductionStore,
)
from hermes_memory_fabric.r8_local_persistence_governance import (
    GovernanceError,
)


_Contract21TestStore = _ProductionStore
SubspaceMemoryStore = _ProductionStore


def _logical_sha256(payload):
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _explicit_decision(
    store, *, operation, payload, project, namespace, target, sequence, decision_id
):
    return {
        "schema_version": "hermes.local-mutation-decision.v1",
        "contract_version": "2.2.0",
        "operation": operation,
        "workspace_scope": str(store._governance.workspace_root),
        "storage_scope": str(store.storage_root),
        "project": project,
        "namespace": namespace,
        "target": target,
        "payload_sha256": _logical_sha256(payload),
        "expected_sequence": sequence,
        "decision_id": decision_id,
        "issued_at": "2000-01-01T00:00:00Z",
        "expires_at": "2999-01-01T00:00:00Z",
        "audit": {"actor": "trusted-test-operator"},
    }


def _propose(store, sequence, decision_id, *, project, namespace, content, source="local", tags=None, confidence=1.0):
    payload = {
        "project": project, "namespace": namespace, "content": content,
        "source": source, "tags": list(tags or []), "confidence": confidence,
    }
    target = f"proposal:{_logical_sha256(payload)[:32]}"
    return store.propose_memory(
        **payload,
        decision=_explicit_decision(
            store, operation="PROPOSE_MEMORY", payload=payload, project=project,
            namespace=namespace, target=target, sequence=sequence, decision_id=decision_id,
        ),
    )


def _approve(store, proposal, sequence, decision_id, *, approver, note=None):
    payload = {"proposal_id": proposal.id, "approver": approver, "note": note}
    return store.approve_proposal(
        proposal.id, approver=approver, note=note,
        decision=_explicit_decision(
            store, operation="APPROVE_PROPOSAL", payload=payload,
            project=proposal.project, namespace=proposal.namespace, target=proposal.id,
            sequence=sequence, decision_id=decision_id,
        ),
    )


def _reject(store, proposal, sequence, decision_id, *, reviewer, reason):
    payload = {"proposal_id": proposal.id, "reviewer": reviewer, "reason": reason}
    return store.reject_proposal(
        proposal.id, reviewer=reviewer, reason=reason,
        decision=_explicit_decision(
            store, operation="REJECT_PROPOSAL", payload=payload,
            project=proposal.project, namespace=proposal.namespace, target=proposal.id,
            sequence=sequence, decision_id=decision_id,
        ),
    )


def _lifecycle(store, memory, sequence, decision_id, *, lifecycle, actor, reason=None):
    payload = {"memory_id": memory.id, "lifecycle": lifecycle, "actor": actor, "reason": reason}
    return store.set_memory_lifecycle(
        memory.id, lifecycle, actor=actor, reason=reason,
        decision=_explicit_decision(
            store, operation="SET_MEMORY_LIFECYCLE", payload=payload,
            project=memory.project, namespace=memory.namespace, target=memory.id,
            sequence=sequence, decision_id=decision_id,
        ),
    )


def _set_do_not_retry(store, memory, sequence, decision_id, *, reason, actor, alternative=None):
    payload = {"memory_id": memory.id, "reason": reason, "actor": actor, "alternative": alternative}
    return store.set_do_not_retry(
        memory.id, reason=reason, actor=actor, alternative=alternative,
        decision=_explicit_decision(
            store, operation="SET_DO_NOT_RETRY", payload=payload,
            project=memory.project, namespace=memory.namespace, target=memory.id,
            sequence=sequence, decision_id=decision_id,
        ),
    )


def _clear_do_not_retry(store, memory, sequence, decision_id, *, actor, reason=None):
    payload = {"memory_id": memory.id, "actor": actor, "reason": reason}
    return store.clear_do_not_retry(
        memory.id, actor=actor, reason=reason,
        decision=_explicit_decision(
            store, operation="CLEAR_DO_NOT_RETRY", payload=payload,
            project=memory.project, namespace=memory.namespace, target=memory.id,
            sequence=sequence, decision_id=decision_id,
        ),
    )


def _adapt_mutation_argv(argv, decision=None):
    if decision is None:
        return list(argv)
    return list(argv) + [
        "--mutation-decision-json",
        json.dumps(decision, sort_keys=True, separators=(",", ":"), ensure_ascii=False),
    ]


def test_proposing_memory_creates_pending_proposal_and_audit_event(tmp_path):
    store = SubspaceMemoryStore(tmp_path)

    proposal = _propose(store, 0, "propose-1",
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
    assert (tmp_path / "snapshot.json").exists()
    events = store.list_audit_events()
    assert [event.event_type for event in events] == ["proposal_created"]
    assert events[0].target_id == proposal.id


def test_approving_proposal_creates_approved_memory_and_audit_event(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    proposal = _propose(store, 0, "propose-1",
        project="hermes-memory-fabric",
        namespace="runtime",
        content="Subspace runtime stores approved memory locally.",
    )

    memory = _approve(store, proposal, 1, "approve-1", approver="human", note="approved")

    assert memory.status == "approved"
    assert memory.proposal_id == proposal.id
    assert memory.approver == "human"
    assert (tmp_path / "snapshot.json").exists()
    assert [event.event_type for event in store.list_audit_events()] == [
        "proposal_created",
        "proposal_approved",
    ]
    repeated_payload = {"proposal_id": proposal.id, "approver": "human", "note": None}
    with pytest.raises(ValueError, match="proposal_not_pending:approved"):
        store.approve_proposal(
            proposal.id,
            approver="human",
            decision=_explicit_decision(
                store, operation="APPROVE_PROPOSAL", payload=repeated_payload,
                project=proposal.project, namespace=proposal.namespace,
                target=proposal.id, sequence=2, decision_id="approve-again",
            ),
        )


def test_rejected_proposal_is_not_recalled(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    proposal = _propose(store, 0, "propose-1",
        project="hermes-memory-fabric",
        namespace="runtime",
        content="Rejected memory must not become recallable.",
    )

    rejected = _reject(store, proposal, 1, "reject-1", reviewer="human", reason="not suitable")

    assert rejected.status == "rejected"
    assert store.recall("Rejected", project="hermes-memory-fabric", namespace="runtime") == []
    assert [event.event_type for event in store.list_audit_events()] == [
        "proposal_created",
        "proposal_rejected",
    ]


def test_approved_memory_is_recalled_by_keyword_with_explainable_structure(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    proposal = _propose(store, 0, "propose-1",
        project="hermes-memory-fabric",
        namespace="runtime",
        content="Keyword recall returns deterministic matched terms.",
        source="local-test",
    )
    memory = _approve(store, proposal, 1, "approve-1", approver="human")

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
    matching = _propose(store, 0, "propose-alpha",
        project="alpha",
        namespace="runtime",
        content="Isolation keyword belongs to alpha.",
    )
    other = _propose(store, 1, "propose-beta",
        project="beta",
        namespace="runtime",
        content="Isolation keyword belongs to beta.",
    )
    alpha_memory = _approve(store, matching, 2, "approve-alpha", approver="human")
    _approve(store, other, 3, "approve-beta", approver="human")

    results = store.recall("isolation", project="alpha")

    assert [result.memory_id for result in results] == [alpha_memory.id]
    assert results[0].project == "alpha"


def test_namespace_isolation_works(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    matching = _propose(store, 0, "propose-runtime",
        project="hermes-memory-fabric",
        namespace="runtime",
        content="Namespace keyword belongs to runtime.",
    )
    other = _propose(store, 1, "propose-docs",
        project="hermes-memory-fabric",
        namespace="docs",
        content="Namespace keyword belongs to docs.",
    )
    runtime_memory = _approve(store, matching, 2, "approve-runtime", approver="human")
    _approve(store, other, 3, "approve-docs", approver="human")

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
    payload = {"proposal_id": "proposal:missing", "approver": "human", "note": None}

    with pytest.raises(ValueError, match="proposal_not_found"):
        store.approve_proposal(
            "proposal:missing",
            approver="human",
            decision=_explicit_decision(
                store, operation="APPROVE_PROPOSAL", payload=payload,
                project="project", namespace="namespace", target="proposal:missing",
                sequence=0, decision_id="approve-missing",
            ),
        )


def test_runtime_only_uses_fixed_files_under_explicit_storage_root(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    proposal = _propose(store, 0, "propose-1", project="p", namespace="n", content="fixed local files only")
    _approve(store, proposal, 1, "approve-1", approver="human")

    assert sorted(path.name for path in tmp_path.iterdir()) == [".snapshot.lock", "snapshot.json"]


def test_approved_memory_storage_survives_store_reopen(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    proposal = _propose(store, 0, "propose-1",
        project="hermes-memory-fabric",
        namespace="runtime",
        content="Reopened store can recall approved local memory.",
        tags=["reopen"],
    )
    memory = _approve(store, proposal, 1, "approve-1", approver="human")
    reopened = SubspaceMemoryStore(tmp_path)

    results = reopened.recall("reopened", project="hermes-memory-fabric", namespace="runtime")

    assert [result.memory_id for result in results] == [memory.id]


def test_no_uv_lock_is_created():
    assert not __import__("pathlib").Path("uv.lock").exists()


def test_package_version_remains_6_16_0():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert pyproject["project"]["version"] == "6.16.0"


def test_explicit_empty_decision_is_not_replaced_by_test_adapter(tmp_path):
    store = SubspaceMemoryStore(tmp_path)

    with pytest.raises(GovernanceError, match="BLOCK_DECISION_REQUIRED_OR_MALFORMED"):
        store.propose_memory(
            project="p",
            namespace="n",
            content="explicit decision boundary",
            decision={},
        )


def test_tags_over_limit_consumes_only_limit_plus_one_and_does_not_persist(tmp_path):
    class CountingTags:
        def __init__(self):
            self.request_count = 0

        def __iter__(self):
            return self

        def __next__(self):
            self.request_count += 1
            if self.request_count > 129:
                raise AssertionError("requested_tag_130")
            return f"tag-{self.request_count}"

    tags = CountingTags()
    store = SubspaceMemoryStore(tmp_path / "store")

    with pytest.raises(ValueError, match="tags_exceed_count_limit"):
        store.propose_memory(project="p", namespace="n", content="bounded", tags=tags)

    assert tags.request_count == 129
    assert not store.storage_root.exists()


def test_tags_at_limit_preserve_order_and_commit(tmp_path):
    expected = [f"tag-{index}" for index in range(128)]
    store = SubspaceMemoryStore(tmp_path / "store")
    payload = {
        "project": "p",
        "namespace": "n",
        "content": "bounded",
        "source": "local",
        "tags": expected,
        "confidence": 1.0,
    }
    target = f"proposal:{_logical_sha256(payload)[:32]}"

    proposal = store.propose_memory(
        project="p",
        namespace="n",
        content="bounded",
        tags=iter(expected),
        decision=_explicit_decision(
            store,
            operation="PROPOSE_MEMORY",
            payload=payload,
            project="p",
            namespace="n",
            target=target,
            sequence=0,
            decision_id="tags-at-limit",
        ),
    )

    assert proposal.tags == tuple(expected)
    assert store.current_sequence == 1


@pytest.mark.parametrize("failure_point", ["iter", "next"])
def test_tags_iterator_failure_uses_stable_validation_error(tmp_path, failure_point):
    class FailingTags:
        def __iter__(self):
            if failure_point == "iter":
                raise RuntimeError("private iterator failure")
            return self

        def __next__(self):
            raise RuntimeError("private iterator failure")

    store = SubspaceMemoryStore(tmp_path / "store")

    with pytest.raises(ValueError) as captured:
        store.propose_memory(
            project="p", namespace="n", content="bounded", tags=FailingTags()
        )

    assert str(captured.value) == "tags_must_be_an_iterable_of_strings"
    assert not store.storage_root.exists()
