from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from itertools import islice
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping

from .r8_local_persistence_governance import (
    GovernedSnapshotStore,
    GovernanceError,
    MAX_BUSINESS_STRING_CHARS,
    MAX_IDENTIFIER_CHARS,
    MAX_TAGS,
    MutationReceipt,
    proposal_target,
)


SCHEMA_VERSION = "p4-m0.subspace-memory.v1"
PROPOSAL_KIND = "subspace_memory_proposal"
APPROVED_MEMORY_KIND = "approved_subspace_memory"
AUDIT_KIND = "subspace_memory_audit_event"
VALID_LIFECYCLE_STATES = ("active", "stale", "archived")

_PROPOSALS_FILE = "proposals.jsonl"
_MEMORIES_FILE = "memories.jsonl"
_AUDIT_FILE = "audit.jsonl"
_TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")


@dataclass(frozen=True)
class MemoryProposal:
    schema_version: str
    id: str
    project: str
    namespace: str
    kind: str
    content: str
    source: str
    tags: tuple[str, ...]
    confidence: float
    status: str
    created_at: str
    updated_at: str
    reviewer: str | None = None
    approver: str | None = None
    reason: str | None = None
    note: str | None = None


@dataclass(frozen=True)
class DoNotRetryWarning:
    enabled: bool
    reason: str
    alternative: str | None
    actor: str
    updated_at: str


@dataclass(frozen=True)
class ApprovedMemory:
    schema_version: str
    id: str
    proposal_id: str
    project: str
    namespace: str
    kind: str
    content: str
    source: str
    tags: tuple[str, ...]
    confidence: float
    status: str
    created_at: str
    updated_at: str
    approver: str
    note: str | None = None
    lifecycle: str = "active"
    do_not_retry: DoNotRetryWarning | None = None


@dataclass(frozen=True)
class RecallTrace:
    query: str
    query_terms: tuple[str, ...]
    matched_terms: tuple[str, ...]
    score: int
    rank: int
    memory_id: str
    project: str
    namespace: str
    source: str
    lifecycle: str
    include_stale: bool
    include_archived: bool
    explanation: str


@dataclass(frozen=True)
class RecallResult:
    memory_id: str
    score: int
    matched_terms: tuple[str, ...]
    content: str
    project: str
    namespace: str
    source: str
    lifecycle: str
    do_not_retry: DoNotRetryWarning | None
    do_not_retry_warning: str | None
    trace: RecallTrace


@dataclass(frozen=True)
class AuditEvent:
    schema_version: str
    id: str
    kind: str
    event_type: str
    target_id: str
    project: str
    namespace: str
    actor: str
    created_at: str
    detail: dict[str, Any]


class SubspaceMemoryStore:
    """P4-M0 local file-backed Subspace Memory runtime."""

    def __init__(
        self,
        storage_root: str | Path,
        *,
        workspace_root: str | Path | None = None,
        clock: Callable[[], datetime] | None = None,
    ):
        self._governance = GovernedSnapshotStore(
            storage_root, workspace_root=workspace_root, clock=clock
        )
        self.storage_root = self._governance.storage_root

    @property
    def last_receipt(self) -> MutationReceipt | None:
        return self._governance.last_receipt

    @property
    def current_sequence(self) -> int:
        return self._governance.current_sequence()

    def propose_memory(
        self,
        *,
        project: str,
        namespace: str,
        content: str,
        source: str = "local",
        tags: Iterable[str] | None = None,
        confidence: float = 1.0,
        decision: Mapping[str, Any] | str | bytes | None = None,
    ) -> MemoryProposal:
        project_value = _required_text(project, "project")
        namespace_value = _required_text(namespace, "namespace")
        content_value = _required_text(content, "content")
        source_value = _required_text(source, "source")
        tag_values = _normalize_tags(tags)
        confidence_value = _normalize_confidence(confidence)
        payload = {
            "project": project_value, "namespace": namespace_value, "content": content_value,
            "source": source_value, "tags": list(tag_values), "confidence": confidence_value,
        }
        target = proposal_target(payload)
        def mutate(
            snapshot: dict[str, Any], mutation_at: str, parsed: Mapping[str, Any]
        ) -> MemoryProposal:
            self._assert_decision_scope(parsed, project_value, namespace_value)
            proposal = MemoryProposal(
                schema_version=SCHEMA_VERSION, id=target, project=project_value,
                namespace=namespace_value, kind=PROPOSAL_KIND, content=content_value,
                source=source_value, tags=tag_values, confidence=confidence_value,
                status="pending", created_at=mutation_at, updated_at=mutation_at,
            )
            snapshot["proposals"].append(asdict(proposal))
            snapshot["audit_events"].append(asdict(self._audit_event(
                event_type="proposal_created", target_id=proposal.id, project=proposal.project,
                namespace=proposal.namespace, actor=proposal.source, detail={"status": proposal.status},
                created_at=mutation_at,
            )))
            return proposal
        result, _ = self._governance.transact(
            decision, operation="PROPOSE_MEMORY", project=project_value,
            namespace=namespace_value, target=target, payload=payload, mutate=mutate,
        )
        return result

    def approve_proposal(
        self,
        proposal_id: str,
        approver: str,
        note: str | None = None,
        *,
        decision: Mapping[str, Any] | str | bytes | None = None,
    ) -> ApprovedMemory:
        clean_id = _required_text(proposal_id, "proposal_id")
        approver_value = _required_text(approver, "approver")
        note_value = _optional_text(note)
        payload = {"proposal_id": clean_id, "approver": approver_value, "note": note_value}
        def mutate(
            snapshot: dict[str, Any], mutation_at: str, parsed: Mapping[str, Any]
        ) -> ApprovedMemory:
            proposal = self._pending_proposal_from_records(snapshot["proposals"], clean_id)
            self._assert_decision_scope(parsed, proposal.project, proposal.namespace)
            approved_proposal = MemoryProposal(
                **{
                    **asdict(proposal), "status": "approved", "updated_at": mutation_at,
                    "approver": approver_value, "note": note_value,
                }
            )
            memory = ApprovedMemory(
                schema_version=SCHEMA_VERSION,
                id=_stable_id("memory", {"proposal_id": proposal.id}),
                proposal_id=proposal.id, project=proposal.project,
                namespace=proposal.namespace, kind=APPROVED_MEMORY_KIND,
                content=proposal.content, source=proposal.source, tags=proposal.tags,
                confidence=proposal.confidence, status="approved", lifecycle="active",
                created_at=mutation_at, updated_at=mutation_at,
                approver=approver_value, note=note_value,
            )
            snapshot["proposals"].append(asdict(approved_proposal))
            snapshot["memories"].append(asdict(memory))
            snapshot["audit_events"].append(asdict(self._audit_event(
                event_type="proposal_approved", target_id=proposal.id, project=proposal.project,
                namespace=proposal.namespace, actor=approver_value,
                detail={"memory_id": memory.id, "note": note_value, "status": "approved"},
                created_at=mutation_at,
            )))
            return memory
        result, _ = self._governance.transact(
            decision, operation="APPROVE_PROPOSAL", project=None,
            namespace=None, target=clean_id, payload=payload, mutate=mutate,
        )
        return result

    def reject_proposal(
        self, proposal_id: str, reviewer: str, reason: str, *,
        decision: Mapping[str, Any] | str | bytes | None = None,
    ) -> MemoryProposal:
        clean_id = _required_text(proposal_id, "proposal_id")
        reviewer_value = _required_text(reviewer, "reviewer")
        reason_value = _required_text(reason, "reason")
        payload = {"proposal_id": clean_id, "reviewer": reviewer_value, "reason": reason_value}
        def mutate(
            snapshot: dict[str, Any], mutation_at: str, parsed: Mapping[str, Any]
        ) -> MemoryProposal:
            proposal = self._pending_proposal_from_records(snapshot["proposals"], clean_id)
            self._assert_decision_scope(parsed, proposal.project, proposal.namespace)
            rejected = MemoryProposal(
                **{
                    **asdict(proposal), "status": "rejected", "updated_at": mutation_at,
                    "reviewer": reviewer_value, "reason": reason_value,
                }
            )
            snapshot["proposals"].append(asdict(rejected))
            snapshot["audit_events"].append(asdict(self._audit_event(
                event_type="proposal_rejected", target_id=proposal.id, project=proposal.project,
                namespace=proposal.namespace, actor=reviewer_value,
                detail={"reason": reason_value, "status": "rejected"},
                created_at=mutation_at,
            )))
            return rejected
        result, _ = self._governance.transact(
            decision, operation="REJECT_PROPOSAL", project=None,
            namespace=None, target=clean_id, payload=payload, mutate=mutate,
        )
        return result

    def set_memory_lifecycle(
        self,
        memory_id: str,
        lifecycle: str,
        *,
        actor: str,
        reason: str | None = None,
        decision: Mapping[str, Any] | str | bytes | None = None,
    ) -> ApprovedMemory:
        clean_id = _required_text(memory_id, "memory_id")
        lifecycle_value = _normalize_lifecycle(lifecycle)
        actor_value = _required_text(actor, "actor")
        reason_value = _optional_text(reason)
        payload = {"memory_id": clean_id, "lifecycle": lifecycle_value, "actor": actor_value, "reason": reason_value}
        def mutate(
            snapshot: dict[str, Any], mutation_at: str, parsed: Mapping[str, Any]
        ) -> ApprovedMemory:
            index, memory = self._memory_record_or_raise(snapshot["memories"], clean_id)
            self._assert_decision_scope(parsed, memory.project, memory.namespace)
            previous_lifecycle = memory.lifecycle
            updated = ApprovedMemory(
                **{
                    **asdict(memory), "lifecycle": lifecycle_value,
                    "updated_at": mutation_at,
                }
            )
            snapshot["memories"][index] = asdict(updated)
            snapshot["audit_events"].append(asdict(self._audit_event(
                event_type="memory_lifecycle_updated", target_id=updated.id,
                project=updated.project, namespace=updated.namespace, actor=actor_value,
                detail={"previous_lifecycle": previous_lifecycle, "lifecycle": lifecycle_value, "reason": reason_value},
                created_at=mutation_at,
            )))
            return updated
        result, _ = self._governance.transact(
            decision, operation="SET_MEMORY_LIFECYCLE", project=None,
            namespace=None, target=clean_id, payload=payload, mutate=mutate,
        )
        return result

    def set_do_not_retry(
        self,
        memory_id: str,
        *,
        reason: str,
        actor: str,
        alternative: str | None = None,
        decision: Mapping[str, Any] | str | bytes | None = None,
    ) -> ApprovedMemory:
        clean_id = _required_text(memory_id, "memory_id")
        reason_value = _required_text(reason, "reason")
        actor_value = _required_text(actor, "actor")
        alternative_value = _optional_text(alternative)
        payload = {"memory_id": clean_id, "reason": reason_value, "actor": actor_value, "alternative": alternative_value}
        def mutate(
            snapshot: dict[str, Any], mutation_at: str, parsed: Mapping[str, Any]
        ) -> ApprovedMemory:
            index, memory = self._memory_record_or_raise(snapshot["memories"], clean_id)
            self._assert_decision_scope(parsed, memory.project, memory.namespace)
            warning = DoNotRetryWarning(
                enabled=True, reason=reason_value, alternative=alternative_value,
                actor=actor_value, updated_at=mutation_at,
            )
            updated = ApprovedMemory(
                **{
                    **asdict(memory), "do_not_retry": warning,
                    "updated_at": mutation_at,
                }
            )
            snapshot["memories"][index] = asdict(updated)
            snapshot["audit_events"].append(asdict(self._audit_event(
                event_type="memory_do_not_retry_set", target_id=updated.id,
                project=updated.project, namespace=updated.namespace, actor=actor_value,
                detail={"reason": reason_value, "alternative": alternative_value},
                created_at=mutation_at,
            )))
            return updated
        result, _ = self._governance.transact(
            decision, operation="SET_DO_NOT_RETRY", project=None,
            namespace=None, target=clean_id, payload=payload, mutate=mutate,
        )
        return result

    def clear_do_not_retry(
        self,
        memory_id: str,
        *,
        actor: str,
        reason: str | None = None,
        decision: Mapping[str, Any] | str | bytes | None = None,
    ) -> ApprovedMemory:
        clean_id = _required_text(memory_id, "memory_id")
        actor_value = _required_text(actor, "actor")
        reason_value = _optional_text(reason)
        payload = {"memory_id": clean_id, "actor": actor_value, "reason": reason_value}
        def mutate(
            snapshot: dict[str, Any], mutation_at: str, parsed: Mapping[str, Any]
        ) -> ApprovedMemory:
            index, memory = self._memory_record_or_raise(snapshot["memories"], clean_id)
            self._assert_decision_scope(parsed, memory.project, memory.namespace)
            previous = asdict(memory.do_not_retry) if memory.do_not_retry is not None else None
            updated = ApprovedMemory(
                **{
                    **asdict(memory), "do_not_retry": None,
                    "updated_at": mutation_at,
                }
            )
            snapshot["memories"][index] = asdict(updated)
            snapshot["audit_events"].append(asdict(self._audit_event(
                event_type="memory_do_not_retry_cleared", target_id=updated.id,
                project=updated.project, namespace=updated.namespace, actor=actor_value,
                detail={"previous_do_not_retry": previous, "reason": reason_value},
                created_at=mutation_at,
            )))
            return updated
        result, _ = self._governance.transact(
            decision, operation="CLEAR_DO_NOT_RETRY", project=None,
            namespace=None, target=clean_id, payload=payload, mutate=mutate,
        )
        return result

    def recall(
        self,
        query: str,
        *,
        project: str | None = None,
        namespace: str | None = None,
        limit: int = 10,
        include_stale: bool = False,
        include_archived: bool = False,
    ) -> list[RecallResult]:
        query_value = _required_text(query, "query")
        terms = _query_terms(query_value)
        if limit < 1:
            return []
        project_filter = _optional_text(project)
        namespace_filter = _optional_text(namespace)
        candidates: list[tuple[ApprovedMemory, tuple[str, ...]]] = []
        for memory in self._read_memories():
            if memory.status != "approved":
                continue
            if memory.lifecycle == "stale" and not include_stale:
                continue
            if memory.lifecycle == "archived" and not include_archived:
                continue
            if project_filter is not None and memory.project != project_filter:
                continue
            if namespace_filter is not None and memory.namespace != namespace_filter:
                continue
            content_lower = memory.content.lower()
            matched = tuple(term for term in terms if term in content_lower)
            if not matched:
                continue
            candidates.append((memory, matched))
        candidates.sort(key=lambda item: (-len(item[1]), item[0].project, item[0].namespace, item[0].id))
        results: list[RecallResult] = []
        for rank, (memory, matched) in enumerate(candidates[:limit], start=1):
            score = len(matched)
            trace = RecallTrace(
                query=query_value,
                query_terms=terms,
                matched_terms=matched,
                score=score,
                rank=rank,
                memory_id=memory.id,
                project=memory.project,
                namespace=memory.namespace,
                source=memory.source,
                lifecycle=memory.lifecycle,
                include_stale=bool(include_stale),
                include_archived=bool(include_archived),
                explanation=_trace_explanation(matched),
            )
            results.append(
                RecallResult(
                    memory_id=memory.id,
                    score=score,
                    matched_terms=matched,
                    content=memory.content,
                    project=memory.project,
                    namespace=memory.namespace,
                    source=memory.source,
                    lifecycle=memory.lifecycle,
                    do_not_retry=memory.do_not_retry,
                    do_not_retry_warning=_do_not_retry_warning_text(memory.do_not_retry),
                    trace=trace,
                )
            )
        return results

    def list_audit_events(self) -> list[AuditEvent]:
        return [AuditEvent(**record) for record in self._governance.read_snapshot()["audit_events"]]

    def _pending_proposal_or_raise(self, proposal_id: str) -> MemoryProposal:
        clean_id = _required_text(proposal_id, "proposal_id")
        proposal = self._latest_proposals().get(clean_id)
        if proposal is None:
            raise ValueError("proposal_not_found")
        if proposal.status != "pending":
            raise ValueError(f"proposal_not_pending:{proposal.status}")
        return proposal

    def _pending_proposal_from_records(
        self, records: list[dict[str, Any]], proposal_id: str
    ) -> MemoryProposal:
        proposal: MemoryProposal | None = None
        for record in records:
            if str(record.get("id")) == proposal_id:
                proposal = _proposal_from_record(record)
        if proposal is None:
            raise ValueError("proposal_not_found")
        if proposal.status != "pending":
            raise ValueError(f"proposal_not_pending:{proposal.status}")
        return proposal

    @staticmethod
    def _assert_decision_scope(
        parsed: Mapping[str, Any], project: str, namespace: str
    ) -> None:
        if parsed["project"] != project or parsed["namespace"] != namespace:
            raise GovernanceError("BLOCK_DECISION_BINDING_MISMATCH")

    def _latest_proposals(self) -> dict[str, MemoryProposal]:
        proposals: dict[str, MemoryProposal] = {}
        for record in self._governance.read_snapshot()["proposals"]:
            proposals[str(record["id"])] = _proposal_from_record(record)
        return proposals

    def _read_memories(self) -> list[ApprovedMemory]:
        return [_memory_from_record(record) for record in self._governance.read_snapshot()["memories"]]

    def _memory_record_or_raise(
        self,
        records: list[dict[str, Any]],
        memory_id: str,
    ) -> tuple[int, ApprovedMemory]:
        memory_index: int | None = None
        memory: ApprovedMemory | None = None
        for index, record in enumerate(records):
            if str(record.get("id")) == memory_id:
                memory_index = index
                memory = _memory_from_record(record)
        if memory is None or memory_index is None:
            raise ValueError("memory_not_found")
        return memory_index, memory

    def _audit_event(
        self,
        *,
        event_type: str,
        target_id: str,
        project: str,
        namespace: str,
        actor: str,
        detail: dict[str, Any],
        created_at: str,
    ) -> AuditEvent:
        event = AuditEvent(
            schema_version=SCHEMA_VERSION,
            id=_stable_id(
                "audit",
                {
                    "event_type": event_type,
                    "target_id": target_id,
                    "actor": actor,
                    "created_at": created_at,
                    "detail": detail,
                },
            ),
            kind=AUDIT_KIND,
            event_type=event_type,
            target_id=target_id,
            project=project,
            namespace=namespace,
            actor=actor,
            created_at=created_at,
            detail=dict(detail),
        )
        return event

    def _utc_now(self) -> str:
        return self._governance._clock().astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def _required_text(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field}_must_be_non_empty")
    limit = MAX_IDENTIFIER_CHARS if field in {
        "project", "namespace", "proposal_id", "memory_id"
    } else MAX_BUSINESS_STRING_CHARS
    if len(value) > limit:
        raise ValueError(f"{field}_exceeds_character_limit")
    return value


def _optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("optional_text_must_be_string_or_none")
    if len(value) > MAX_BUSINESS_STRING_CHARS:
        raise ValueError("optional_text_exceeds_character_limit")
    return value


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    if not isinstance(value, str):
        raise ValueError("text_must_be_string")
    return value


def _normalize_tags(tags: Iterable[str] | None) -> tuple[str, ...]:
    if tags is None:
        return ()
    if isinstance(tags, (str, bytes)):
        raise ValueError("tags_must_be_an_iterable_of_strings")
    try:
        values = tuple(islice(tags, MAX_TAGS + 1))
    except Exception:
        raise ValueError("tags_must_be_an_iterable_of_strings") from None
    if len(values) > MAX_TAGS:
        raise ValueError("tags_exceed_count_limit")
    for value in values:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("tag_must_be_non_empty_string")
        if len(value) > MAX_BUSINESS_STRING_CHARS:
            raise ValueError("tag_exceeds_character_limit")
    return values


def _normalize_confidence(confidence: float) -> float:
    if type(confidence) not in {int, float} or not math.isfinite(confidence):
        raise ValueError("confidence_must_be_finite_number")
    value = confidence
    if value < 0.0 or value > 1.0:
        raise ValueError("confidence_must_be_between_0_and_1")
    return value


def _normalize_lifecycle(lifecycle: str) -> str:
    value = _required_text(lifecycle, "lifecycle")
    if value not in VALID_LIFECYCLE_STATES:
        raise ValueError("invalid_lifecycle_state")
    return value


def _query_terms(query: str) -> tuple[str, ...]:
    cleaned = _required_text(query, "query")
    terms = tuple(dict.fromkeys(match.group(0).lower() for match in _TOKEN_RE.finditer(cleaned)))
    if not terms:
        raise ValueError("query_must_include_keyword")
    return terms


def _trace_explanation(matched_terms: tuple[str, ...]) -> str:
    term_label = "term" if len(matched_terms) == 1 else "terms"
    return f"Matched {len(matched_terms)} query {term_label}: {', '.join(matched_terms)}."


def _do_not_retry_warning_text(warning: DoNotRetryWarning | None) -> str | None:
    if warning is None:
        return None
    text = (
        f"DO NOT RETRY: This memory is marked do-not-retry by {warning.actor}. "
        f"Reason: {_warning_sentence(warning.reason)}."
    )
    if warning.alternative is not None:
        text = f"{text} Alternative: {_warning_sentence(warning.alternative)}."
    return text


def _warning_sentence(value: str) -> str:
    return value.rstrip(".!?")


def _proposal_from_record(record: dict[str, Any]) -> MemoryProposal:
    return MemoryProposal(**{**record, "tags": tuple(record.get("tags", ()))})


def _do_not_retry_from_record(record: dict[str, Any]) -> DoNotRetryWarning | None:
    warning = record.get("do_not_retry")
    if warning is None:
        return None
    return DoNotRetryWarning(
        enabled=bool(warning.get("enabled", True)),
        reason=_required_text(warning.get("reason"), "reason"),
        alternative=_optional_text(warning.get("alternative")),
        actor=_required_text(warning.get("actor"), "actor"),
        updated_at=_required_text(warning.get("updated_at"), "updated_at"),
    )


def _memory_from_record(record: dict[str, Any]) -> ApprovedMemory:
    normalized = {
        **record,
        "tags": tuple(record.get("tags", ())),
        "lifecycle": _normalize_lifecycle(record.get("lifecycle", "active")),
        "do_not_retry": _do_not_retry_from_record(record),
    }
    return ApprovedMemory(**normalized)


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _stable_id(prefix: str, payload: dict[str, Any]) -> str:
    digest = hashlib.sha256(_stable_json(payload).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}:{SCHEMA_VERSION}:{digest}"


def _stable_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
