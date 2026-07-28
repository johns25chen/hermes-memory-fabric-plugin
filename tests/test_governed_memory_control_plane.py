from __future__ import annotations

from dataclasses import FrozenInstanceError, fields

import pytest

from hermes_memory_fabric.governed_memory_control_plane import (
    EXPLICIT_HUMAN_APPROVAL,
    AdoptedMemory,
    AuthorizationError,
    GovernedMemoryError,
    GovernedMemoryControlPlane,
    InvalidTransitionError,
    NotFoundError,
    ScopeError,
)


def _candidate(control_plane, *, content="Governed memory content", scope="project/a"):
    source = control_plane.create_source(
        reference="source://one",
        provenance="unit-test",
    )
    candidate = control_plane.create_candidate(
        source_id=source.source_id,
        content=content,
        scope=scope,
    )
    return source, candidate


def _reviewed(control_plane, *, content="Governed memory content", scope="project/a"):
    source, candidate = _candidate(
        control_plane,
        content=content,
        scope=scope,
    )
    control_plane.attach_evidence(
        candidate_id=candidate.candidate_id,
        source_id=source.source_id,
        reference="evidence://one",
        description="independent evidence",
    )
    control_plane.record_human_review(
        candidate_id=candidate.candidate_id,
        reviewer="reviewer",
        decision="approve",
    )
    return source, candidate


def _approved(control_plane, *, content="Governed memory content", scope="project/a"):
    source, candidate = _reviewed(
        control_plane,
        content=content,
        scope=scope,
    )
    approved = control_plane.approve_candidate(
        candidate_id=candidate.candidate_id,
        approver="approver",
        confirmation=EXPLICIT_HUMAN_APPROVAL,
    )
    return source, approved


def _adopted(control_plane, *, content="Governed memory content", scope="project/a"):
    _, candidate = _approved(control_plane, content=content, scope=scope)
    memory = control_plane.adopt_candidate(
        candidate_id=candidate.candidate_id,
        scope=scope,
        actor="operator",
    )
    return candidate, memory


def test_constructor_and_fresh_reads_create_no_storage(tmp_path):
    control_plane = GovernedMemoryControlPlane(tmp_path)

    assert control_plane.recall(query="missing", scope="project/a") == ()
    assert control_plane.list_audit_events() == ()
    with pytest.raises(NotFoundError):
        control_plane.get_tombstone(memory_id="memory-000001")
    assert not (tmp_path / ".local").exists()
    assert not control_plane.state_path.exists()


def test_deterministic_identifiers_and_persistence_across_restart(tmp_path):
    first = GovernedMemoryControlPlane(tmp_path)
    source, candidate = _candidate(first)
    evidence = first.attach_evidence(
        candidate_id=candidate.candidate_id,
        source_id=source.source_id,
        reference="evidence://one",
        description="evidence",
    )
    review = first.record_human_review(
        candidate_id=candidate.candidate_id,
        reviewer="reviewer",
        decision="approve",
    )
    first.approve_candidate(
        candidate_id=candidate.candidate_id,
        approver="approver",
        confirmation=EXPLICIT_HUMAN_APPROVAL,
    )
    memory = first.adopt_candidate(
        candidate_id=candidate.candidate_id,
        scope="project/a",
        actor="operator",
    )

    restarted = GovernedMemoryControlPlane(tmp_path)

    assert source.source_id == "source-000001"
    assert candidate.candidate_id == "candidate-000001"
    assert evidence.evidence_id == "evidence-000001"
    assert review.review_id == "review-000001"
    assert memory.memory_id == "memory-000001"
    assert [event.audit_id for event in restarted.list_audit_events()] == [
        f"audit-{number:06d}" for number in range(1, 7)
    ]
    assert restarted.recall(query="GOVERNED", scope="project/a") == (memory,)


def test_evidence_attachment_does_not_approve(tmp_path):
    control_plane = GovernedMemoryControlPlane(tmp_path)
    source, candidate = _candidate(control_plane)

    control_plane.attach_evidence(
        candidate_id=candidate.candidate_id,
        source_id=source.source_id,
        reference="evidence://one",
        description="evidence",
    )

    with pytest.raises(AuthorizationError):
        control_plane.adopt_candidate(
            candidate_id=candidate.candidate_id,
            scope=candidate.scope,
            actor="operator",
        )


def test_approve_review_alone_does_not_authorize_adoption(tmp_path):
    control_plane = GovernedMemoryControlPlane(tmp_path)
    _, candidate = _reviewed(control_plane)

    with pytest.raises(AuthorizationError):
        control_plane.adopt_candidate(
            candidate_id=candidate.candidate_id,
            scope=candidate.scope,
            actor="operator",
        )


def test_invalid_explicit_confirmation_is_rejected(tmp_path):
    control_plane = GovernedMemoryControlPlane(tmp_path)
    _, candidate = _reviewed(control_plane)

    with pytest.raises(AuthorizationError):
        control_plane.approve_candidate(
            candidate_id=candidate.candidate_id,
            approver="approver",
            confirmation="looks-positive",
        )


def test_explicit_approval_permits_exact_scope_adoption(tmp_path):
    control_plane = GovernedMemoryControlPlane(tmp_path)
    _, candidate = _approved(control_plane)

    memory = control_plane.adopt_candidate(
        candidate_id=candidate.candidate_id,
        scope=candidate.scope,
        actor="operator",
    )

    assert memory.status == "active"
    assert memory.scope == candidate.scope


def test_wrong_scope_adoption_is_rejected(tmp_path):
    control_plane = GovernedMemoryControlPlane(tmp_path)
    _, candidate = _approved(control_plane)

    with pytest.raises(ScopeError):
        control_plane.adopt_candidate(
            candidate_id=candidate.candidate_id,
            scope="project/b",
            actor="operator",
        )


def test_candidate_cannot_adopt_itself(tmp_path):
    control_plane = GovernedMemoryControlPlane(tmp_path)
    _, candidate = _approved(control_plane)

    with pytest.raises(AuthorizationError):
        control_plane.adopt_candidate(
            candidate_id=candidate.candidate_id,
            scope=candidate.scope,
            actor=candidate.candidate_id,
        )


def test_pending_candidate_is_not_recalled(tmp_path):
    control_plane = GovernedMemoryControlPlane(tmp_path)
    _candidate(control_plane, content="pending secret")

    assert control_plane.recall(query="pending", scope="project/a") == ()


def test_reviewed_but_unapproved_candidate_is_not_recalled(tmp_path):
    control_plane = GovernedMemoryControlPlane(tmp_path)
    _reviewed(control_plane, content="reviewed secret")

    assert control_plane.recall(query="reviewed", scope="project/a") == ()


def test_rejected_candidate_is_not_recalled_and_cannot_be_approved(tmp_path):
    control_plane = GovernedMemoryControlPlane(tmp_path)
    source, candidate = _candidate(control_plane, content="rejected secret")
    control_plane.attach_evidence(
        candidate_id=candidate.candidate_id,
        source_id=source.source_id,
        reference="evidence://one",
        description="evidence",
    )
    control_plane.record_human_review(
        candidate_id=candidate.candidate_id,
        reviewer="reviewer",
        decision="reject",
    )

    assert control_plane.recall(query="rejected", scope="project/a") == ()
    with pytest.raises(InvalidTransitionError):
        control_plane.approve_candidate(
            candidate_id=candidate.candidate_id,
            approver="approver",
            confirmation=EXPLICIT_HUMAN_APPROVAL,
        )
    with pytest.raises(InvalidTransitionError):
        control_plane.adopt_candidate(
            candidate_id=candidate.candidate_id,
            scope=candidate.scope,
            actor="operator",
        )


def test_approved_but_not_adopted_candidate_is_not_recalled(tmp_path):
    control_plane = GovernedMemoryControlPlane(tmp_path)
    _approved(control_plane, content="approved secret")

    assert control_plane.recall(query="approved", scope="project/a") == ()


def test_active_memory_is_recalled_only_in_exact_scope_and_is_immutable(tmp_path):
    control_plane = GovernedMemoryControlPlane(tmp_path)
    _, memory = _adopted(control_plane, content="CaseFold Needle")

    result = control_plane.recall(query="casefold", scope="project/a")

    assert result == (memory,)
    assert isinstance(result, tuple)
    assert control_plane.recall(query="casefold", scope="project") == ()
    with pytest.raises(FrozenInstanceError):
        result[0].content = "mutation"


@pytest.mark.parametrize(
    ("query", "scope", "expected_error"),
    [
        ("", "project/a", GovernedMemoryError),
        ("needle", " ", ScopeError),
    ],
)
def test_recall_rejects_blank_query_or_scope(
    tmp_path,
    query,
    scope,
    expected_error,
):
    control_plane = GovernedMemoryControlPlane(tmp_path)

    with pytest.raises(expected_error):
        control_plane.recall(query=query, scope=scope)


def test_correction_increments_revision_and_replaces_recalled_content(tmp_path):
    control_plane = GovernedMemoryControlPlane(tmp_path)
    _, memory = _adopted(control_plane, content="old governed content")

    corrected = control_plane.correct_memory(
        memory_id=memory.memory_id,
        new_content="new governed content",
        actor="corrector",
        reason="fact update",
    )

    assert corrected.revision == 2
    assert corrected.memory_id == memory.memory_id
    assert corrected.candidate_id == memory.candidate_id
    assert corrected.source_id == memory.source_id
    assert corrected.scope == memory.scope
    assert control_plane.recall(query="old governed", scope=memory.scope) == ()
    assert control_plane.recall(query="NEW GOVERNED", scope=memory.scope) == (
        corrected,
    )


def test_correction_audit_does_not_retain_content(tmp_path):
    control_plane = GovernedMemoryControlPlane(tmp_path)
    _, memory = _adopted(control_plane, content="old-content-sentinel")

    control_plane.correct_memory(
        memory_id=memory.memory_id,
        new_content="new-content-sentinel",
        actor="corrector",
        reason="correction reason",
    )
    event = control_plane.list_audit_events()[-1]

    assert event.event_type == "memory_corrected"
    assert "content" not in {field.name for field in fields(event)}
    assert "old-content-sentinel" not in repr(event)
    assert "new-content-sentinel" not in repr(event)


def test_revocation_removes_active_recall_and_repeated_revocation_fails(tmp_path):
    control_plane = GovernedMemoryControlPlane(tmp_path)
    _, memory = _adopted(control_plane, content="revocation sentinel")

    revoked = control_plane.revoke_memory(
        memory_id=memory.memory_id,
        actor="revoker",
        reason="no longer valid",
    )

    assert revoked.status == "revoked"
    assert control_plane.recall(query="revocation", scope=memory.scope) == ()
    with pytest.raises(InvalidTransitionError):
        control_plane.revoke_memory(
            memory_id=memory.memory_id,
            actor="revoker",
            reason="again",
        )


def test_deletion_removes_content_and_leaves_non_content_tombstone(tmp_path):
    control_plane = GovernedMemoryControlPlane(tmp_path)
    deleted_content = "deleted-content-sentinel-93271"
    _, memory = _adopted(control_plane, content=deleted_content)

    tombstone = control_plane.delete_memory(
        memory_id=memory.memory_id,
        actor="deleter",
        reason="retention expired",
    )

    assert "content" not in {field.name for field in fields(tombstone)}
    assert control_plane.get_tombstone(memory_id=memory.memory_id) == tombstone
    assert control_plane.recall(query="deleted-content", scope=memory.scope) == ()
    assert deleted_content not in control_plane.state_path.read_text(encoding="utf-8")
    assert deleted_content not in repr(control_plane.list_audit_events())
    with pytest.raises(InvalidTransitionError):
        control_plane.delete_memory(
            memory_id=memory.memory_id,
            actor="deleter",
            reason="again",
        )


def test_revoked_memory_can_be_deleted(tmp_path):
    control_plane = GovernedMemoryControlPlane(tmp_path)
    _, memory = _adopted(control_plane)
    control_plane.revoke_memory(
        memory_id=memory.memory_id,
        actor="revoker",
        reason="invalid",
    )

    tombstone = control_plane.delete_memory(
        memory_id=memory.memory_id,
        actor="deleter",
        reason="remove",
    )

    assert tombstone.memory_id == memory.memory_id


def test_audit_inspection_does_not_modify_state_bytes_or_event_count(tmp_path):
    control_plane = GovernedMemoryControlPlane(tmp_path)
    _candidate(control_plane)
    before_bytes = control_plane.state_path.read_bytes()
    before_mtime = control_plane.state_path.stat().st_mtime_ns
    before_events = control_plane.list_audit_events()

    after_events = control_plane.list_audit_events()

    assert after_events == before_events
    assert control_plane.state_path.read_bytes() == before_bytes
    assert control_plane.state_path.stat().st_mtime_ns == before_mtime


def test_invalid_transitions_fail_deterministically(tmp_path):
    control_plane = GovernedMemoryControlPlane(tmp_path)
    _, memory = _adopted(control_plane)
    control_plane.revoke_memory(
        memory_id=memory.memory_id,
        actor="revoker",
        reason="invalid",
    )

    with pytest.raises(InvalidTransitionError, match="cannot correct memory"):
        control_plane.correct_memory(
            memory_id=memory.memory_id,
            new_content="replacement",
            actor="corrector",
            reason="fact update",
        )


def test_all_returned_record_types_are_frozen(tmp_path):
    control_plane = GovernedMemoryControlPlane(tmp_path)
    source, candidate = _candidate(control_plane)

    with pytest.raises(FrozenInstanceError):
        source.reference = "changed"
    with pytest.raises(FrozenInstanceError):
        candidate.status = "approved"
    assert isinstance(AdoptedMemory.__dataclass_fields__, dict)
