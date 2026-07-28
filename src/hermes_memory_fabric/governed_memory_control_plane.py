from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any


EXPLICIT_HUMAN_APPROVAL = "EXPLICIT_HUMAN_APPROVAL"


class GovernedMemoryError(Exception):
    """Base error for the governed-memory control plane."""


class NotFoundError(GovernedMemoryError):
    """Raised when a requested record does not exist."""


class InvalidTransitionError(GovernedMemoryError):
    """Raised when a lifecycle transition is not permitted."""


class AuthorizationError(GovernedMemoryError):
    """Raised when explicit authorization requirements are not satisfied."""


class ScopeError(GovernedMemoryError):
    """Raised when a scope is blank or does not match exactly."""


@dataclass(frozen=True)
class SourceRecord:
    source_id: str
    reference: str
    provenance: str


@dataclass(frozen=True)
class CandidateMemory:
    candidate_id: str
    source_id: str
    content: str
    scope: str
    status: str
    evidence_ids: tuple[str, ...]
    review_ids: tuple[str, ...]
    approved_by: str
    approval_note: str
    memory_id: str


@dataclass(frozen=True)
class EvidenceAttachment:
    evidence_id: str
    candidate_id: str
    source_id: str
    reference: str
    description: str


@dataclass(frozen=True)
class HumanReview:
    review_id: str
    candidate_id: str
    reviewer: str
    decision: str
    note: str


@dataclass(frozen=True)
class AdoptedMemory:
    memory_id: str
    candidate_id: str
    source_id: str
    content: str
    scope: str
    status: str
    revision: int


@dataclass(frozen=True)
class AuditEvent:
    audit_id: str
    sequence: int
    event_type: str
    subject_id: str
    actor: str
    reason: str
    scope: str
    decision: str
    revision: int


@dataclass(frozen=True)
class DeletionTombstone:
    memory_id: str
    candidate_id: str
    source_id: str
    scope: str
    final_revision: int
    deleted_by: str
    deletion_reason: str


class GovernedMemoryControlPlane:
    """A deterministic, workspace-local governed-memory lifecycle."""

    def __init__(self, workspace_root: str | os.PathLike[str]) -> None:
        self._workspace_root = Path(workspace_root)

    @property
    def state_path(self) -> Path:
        return (
            self._workspace_root
            / ".local"
            / "governed_memory_control_plane"
            / "state.json"
        )

    def create_source(self, *, reference: str, provenance: str) -> SourceRecord:
        reference = self._required(reference, "reference")
        provenance = self._required(provenance, "provenance")
        state = self._load_state()
        source_id = self._next_id(state, "source", "source")
        record = {
            "source_id": source_id,
            "reference": reference,
            "provenance": provenance,
        }
        state["sources"][source_id] = record
        self._append_audit(
            state,
            event_type="source_created",
            subject_id=source_id,
        )
        self._write_state(state)
        return self._source(record)

    def create_candidate(
        self,
        *,
        source_id: str,
        content: str,
        scope: str,
    ) -> CandidateMemory:
        state = self._load_state()
        self._require_source(state, source_id)
        content = self._required(content, "content")
        scope = self._required_scope(scope)
        candidate_id = self._next_id(state, "candidate", "candidate")
        record = {
            "candidate_id": candidate_id,
            "source_id": source_id,
            "content": content,
            "scope": scope,
            "status": "pending",
            "evidence_ids": [],
            "review_ids": [],
            "approved_by": "",
            "approval_note": "",
            "memory_id": "",
        }
        state["candidates"][candidate_id] = record
        self._append_audit(
            state,
            event_type="candidate_created",
            subject_id=candidate_id,
            scope=scope,
        )
        self._write_state(state)
        return self._candidate(record)

    def attach_evidence(
        self,
        *,
        candidate_id: str,
        source_id: str,
        reference: str,
        description: str,
    ) -> EvidenceAttachment:
        state = self._load_state()
        candidate = self._require_candidate(state, candidate_id)
        self._require_source(state, source_id)
        if candidate["source_id"] != source_id:
            raise GovernedMemoryError("evidence source must match candidate source")
        if candidate["status"] not in {"pending", "reviewed"}:
            raise InvalidTransitionError(
                f"cannot attach evidence to candidate in {candidate['status']} status"
            )
        reference = self._required(reference, "reference")
        description = self._required(description, "description")
        evidence_id = self._next_id(state, "evidence", "evidence")
        record = {
            "evidence_id": evidence_id,
            "candidate_id": candidate_id,
            "source_id": source_id,
            "reference": reference,
            "description": description,
        }
        state["evidence"][evidence_id] = record
        candidate["evidence_ids"].append(evidence_id)
        self._append_audit(
            state,
            event_type="evidence_attached",
            subject_id=candidate_id,
            scope=candidate["scope"],
        )
        self._write_state(state)
        return self._evidence(record)

    def record_human_review(
        self,
        *,
        candidate_id: str,
        reviewer: str,
        decision: str,
        note: str = "",
    ) -> HumanReview:
        state = self._load_state()
        candidate = self._require_candidate(state, candidate_id)
        if candidate["status"] != "pending":
            raise InvalidTransitionError(
                f"cannot review candidate in {candidate['status']} status"
            )
        reviewer = self._required(reviewer, "reviewer")
        normalized_decision = decision.strip().casefold()
        if normalized_decision not in {"approve", "reject"}:
            raise GovernedMemoryError("decision must be approve or reject")
        review_id = self._next_id(state, "review", "review")
        record = {
            "review_id": review_id,
            "candidate_id": candidate_id,
            "reviewer": reviewer,
            "decision": normalized_decision,
            "note": note,
        }
        state["reviews"][review_id] = record
        candidate["review_ids"].append(review_id)
        candidate["status"] = (
            "reviewed" if normalized_decision == "approve" else "rejected"
        )
        self._append_audit(
            state,
            event_type="human_review_recorded",
            subject_id=candidate_id,
            actor=reviewer,
            scope=candidate["scope"],
            decision=normalized_decision,
        )
        self._write_state(state)
        return self._review(record)

    def approve_candidate(
        self,
        *,
        candidate_id: str,
        approver: str,
        confirmation: str,
        note: str = "",
    ) -> CandidateMemory:
        state = self._load_state()
        candidate = self._require_candidate(state, candidate_id)
        if candidate["status"] == "rejected":
            raise InvalidTransitionError("rejected candidate cannot be approved")
        if candidate["status"] != "reviewed":
            raise InvalidTransitionError(
                f"cannot approve candidate in {candidate['status']} status"
            )
        if not candidate["evidence_ids"]:
            raise AuthorizationError("attached evidence is required")
        reviews = [
            state["reviews"][review_id] for review_id in candidate["review_ids"]
        ]
        if not any(review["decision"] == "approve" for review in reviews):
            raise AuthorizationError("prior approve review is required")
        approver = self._required_authorization(approver, "approver")
        if confirmation != EXPLICIT_HUMAN_APPROVAL:
            raise AuthorizationError("explicit human confirmation is required")
        candidate["status"] = "approved"
        candidate["approved_by"] = approver
        candidate["approval_note"] = note
        self._append_audit(
            state,
            event_type="candidate_approved",
            subject_id=candidate_id,
            actor=approver,
            scope=candidate["scope"],
            decision="approve",
        )
        self._write_state(state)
        return self._candidate(candidate)

    def adopt_candidate(
        self,
        *,
        candidate_id: str,
        scope: str,
        actor: str,
    ) -> AdoptedMemory:
        state = self._load_state()
        candidate = self._require_candidate(state, candidate_id)
        if candidate["status"] == "rejected":
            raise InvalidTransitionError("rejected candidate cannot be adopted")
        if candidate["status"] != "approved":
            raise AuthorizationError("explicitly approved candidate is required")
        scope = self._required_scope(scope)
        if scope != candidate["scope"]:
            raise ScopeError("adoption scope must exactly match candidate scope")
        actor = self._required_authorization(actor, "actor")
        if actor == candidate_id:
            raise AuthorizationError("candidate cannot adopt itself")
        memory_id = self._next_id(state, "memory", "memory")
        record = {
            "memory_id": memory_id,
            "candidate_id": candidate_id,
            "source_id": candidate["source_id"],
            "content": candidate["content"],
            "scope": scope,
            "status": "active",
            "revision": 1,
        }
        state["memories"][memory_id] = record
        candidate["status"] = "adopted"
        candidate["memory_id"] = memory_id
        self._append_audit(
            state,
            event_type="candidate_adopted",
            subject_id=memory_id,
            actor=actor,
            scope=scope,
            revision=1,
        )
        self._write_state(state)
        return self._memory(record)

    def recall(self, *, query: str, scope: str) -> tuple[AdoptedMemory, ...]:
        query = self._required(query, "query")
        scope = self._required_scope(scope)
        state = self._load_state()
        folded_query = query.casefold()
        matches = [
            self._memory(record)
            for memory_id, record in sorted(state["memories"].items())
            if record["status"] == "active"
            and record["scope"] == scope
            and folded_query in record["content"].casefold()
        ]
        return tuple(matches)

    def correct_memory(
        self,
        *,
        memory_id: str,
        new_content: str,
        actor: str,
        reason: str,
    ) -> AdoptedMemory:
        state = self._load_state()
        memory = self._require_memory(state, memory_id)
        self._require_active(memory, "correct")
        new_content = self._required(new_content, "new_content")
        actor = self._required_authorization(actor, "actor")
        reason = self._required(reason, "reason")
        memory["content"] = new_content
        memory["revision"] += 1
        candidate = state["candidates"][memory["candidate_id"]]
        candidate["content"] = new_content
        self._append_audit(
            state,
            event_type="memory_corrected",
            subject_id=memory_id,
            actor=actor,
            reason=reason,
            scope=memory["scope"],
            revision=memory["revision"],
        )
        self._write_state(state)
        return self._memory(memory)

    def revoke_memory(
        self,
        *,
        memory_id: str,
        actor: str,
        reason: str,
    ) -> AdoptedMemory:
        state = self._load_state()
        memory = self._require_memory(state, memory_id)
        self._require_active(memory, "revoke")
        actor = self._required_authorization(actor, "actor")
        reason = self._required(reason, "reason")
        memory["status"] = "revoked"
        self._append_audit(
            state,
            event_type="memory_revoked",
            subject_id=memory_id,
            actor=actor,
            reason=reason,
            scope=memory["scope"],
            revision=memory["revision"],
        )
        self._write_state(state)
        return self._memory(memory)

    def delete_memory(
        self,
        *,
        memory_id: str,
        actor: str,
        reason: str,
    ) -> DeletionTombstone:
        state = self._load_state()
        if memory_id in state["tombstones"]:
            raise InvalidTransitionError("memory is already deleted")
        memory = self._require_memory(state, memory_id)
        if memory["status"] not in {"active", "revoked"}:
            raise InvalidTransitionError(
                f"cannot delete memory in {memory['status']} status"
            )
        actor = self._required_authorization(actor, "actor")
        reason = self._required(reason, "reason")
        tombstone_record = {
            "memory_id": memory_id,
            "candidate_id": memory["candidate_id"],
            "source_id": memory["source_id"],
            "scope": memory["scope"],
            "final_revision": memory["revision"],
            "deleted_by": actor,
            "deletion_reason": reason,
        }
        state["candidates"][memory["candidate_id"]]["content"] = ""
        del state["memories"][memory_id]
        state["tombstones"][memory_id] = tombstone_record
        self._append_audit(
            state,
            event_type="memory_deleted",
            subject_id=memory_id,
            actor=actor,
            reason=reason,
            scope=tombstone_record["scope"],
            revision=tombstone_record["final_revision"],
        )
        self._write_state(state)
        return self._tombstone(tombstone_record)

    def get_tombstone(self, *, memory_id: str) -> DeletionTombstone:
        state = self._load_state()
        try:
            record = state["tombstones"][memory_id]
        except KeyError as exc:
            raise NotFoundError(f"tombstone not found: {memory_id}") from exc
        return self._tombstone(record)

    def list_audit_events(self) -> tuple[AuditEvent, ...]:
        state = self._load_state()
        return tuple(self._audit(record) for record in state["audit_events"])

    @staticmethod
    def _empty_state() -> dict[str, Any]:
        return {
            "schema_version": 1,
            "counters": {
                "source": 0,
                "candidate": 0,
                "evidence": 0,
                "review": 0,
                "memory": 0,
                "audit": 0,
            },
            "sources": {},
            "candidates": {},
            "evidence": {},
            "reviews": {},
            "memories": {},
            "tombstones": {},
            "audit_events": [],
        }

    def _load_state(self) -> dict[str, Any]:
        if not self.state_path.exists():
            return self._empty_state()
        with self.state_path.open("r", encoding="utf-8") as handle:
            state = json.load(handle)
        if state.get("schema_version") != 1:
            raise GovernedMemoryError("unsupported state schema")
        return state

    def _write_state(self, state: dict[str, Any]) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.state_path.with_name(f".{self.state_path.name}.tmp")
        payload = json.dumps(
            state,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ) + "\n"
        with temporary_path.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, self.state_path)

    @staticmethod
    def _next_id(state: dict[str, Any], counter: str, prefix: str) -> str:
        state["counters"][counter] += 1
        return f"{prefix}-{state['counters'][counter]:06d}"

    def _append_audit(
        self,
        state: dict[str, Any],
        *,
        event_type: str,
        subject_id: str,
        actor: str = "",
        reason: str = "",
        scope: str = "",
        decision: str = "",
        revision: int = 0,
    ) -> None:
        audit_id = self._next_id(state, "audit", "audit")
        state["audit_events"].append(
            {
                "audit_id": audit_id,
                "sequence": state["counters"]["audit"],
                "event_type": event_type,
                "subject_id": subject_id,
                "actor": actor,
                "reason": reason,
                "scope": scope,
                "decision": decision,
                "revision": revision,
            }
        )

    @staticmethod
    def _required(value: str, field_name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise GovernedMemoryError(f"{field_name} must be non-empty")
        return value

    @classmethod
    def _required_authorization(cls, value: str, field_name: str) -> str:
        try:
            return cls._required(value, field_name)
        except GovernedMemoryError as exc:
            raise AuthorizationError(str(exc)) from exc

    @classmethod
    def _required_scope(cls, scope: str) -> str:
        try:
            return cls._required(scope, "scope")
        except GovernedMemoryError as exc:
            raise ScopeError(str(exc)) from exc

    @staticmethod
    def _require_source(state: dict[str, Any], source_id: str) -> dict[str, Any]:
        try:
            return state["sources"][source_id]
        except KeyError as exc:
            raise NotFoundError(f"source not found: {source_id}") from exc

    @staticmethod
    def _require_candidate(
        state: dict[str, Any], candidate_id: str
    ) -> dict[str, Any]:
        try:
            return state["candidates"][candidate_id]
        except KeyError as exc:
            raise NotFoundError(f"candidate not found: {candidate_id}") from exc

    @staticmethod
    def _require_memory(state: dict[str, Any], memory_id: str) -> dict[str, Any]:
        try:
            return state["memories"][memory_id]
        except KeyError as exc:
            raise NotFoundError(f"memory not found: {memory_id}") from exc

    @staticmethod
    def _require_active(memory: dict[str, Any], action: str) -> None:
        if memory["status"] != "active":
            raise InvalidTransitionError(
                f"cannot {action} memory in {memory['status']} status"
            )

    @staticmethod
    def _source(record: dict[str, Any]) -> SourceRecord:
        return SourceRecord(**record)

    @staticmethod
    def _candidate(record: dict[str, Any]) -> CandidateMemory:
        return CandidateMemory(
            **{
                **record,
                "evidence_ids": tuple(record["evidence_ids"]),
                "review_ids": tuple(record["review_ids"]),
            }
        )

    @staticmethod
    def _evidence(record: dict[str, Any]) -> EvidenceAttachment:
        return EvidenceAttachment(**record)

    @staticmethod
    def _review(record: dict[str, Any]) -> HumanReview:
        return HumanReview(**record)

    @staticmethod
    def _memory(record: dict[str, Any]) -> AdoptedMemory:
        return AdoptedMemory(**record)

    @staticmethod
    def _audit(record: dict[str, Any]) -> AuditEvent:
        return AuditEvent(**record)

    @staticmethod
    def _tombstone(record: dict[str, Any]) -> DeletionTombstone:
        return DeletionTombstone(**record)


__all__ = [
    "EXPLICIT_HUMAN_APPROVAL",
    "GovernedMemoryError",
    "NotFoundError",
    "InvalidTransitionError",
    "AuthorizationError",
    "ScopeError",
    "SourceRecord",
    "CandidateMemory",
    "EvidenceAttachment",
    "HumanReview",
    "AdoptedMemory",
    "AuditEvent",
    "DeletionTombstone",
    "GovernedMemoryControlPlane",
]
