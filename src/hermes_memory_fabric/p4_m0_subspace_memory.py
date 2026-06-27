from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable


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

    def __init__(self, storage_root: str | Path):
        if storage_root is None:
            raise ValueError("storage_root_must_be_explicit")
        self.storage_root = Path(storage_root).expanduser()
        self.storage_root.mkdir(parents=True, exist_ok=True)
        if not self.storage_root.is_dir():
            raise ValueError("storage_root_must_be_directory")
        self._proposals_path = self.storage_root / _PROPOSALS_FILE
        self._memories_path = self.storage_root / _MEMORIES_FILE
        self._audit_path = self.storage_root / _AUDIT_FILE

    def propose_memory(
        self,
        *,
        project: str,
        namespace: str,
        content: str,
        source: str = "local",
        tags: Iterable[str] | None = None,
        confidence: float = 1.0,
    ) -> MemoryProposal:
        project_value = _required_text(project, "project")
        namespace_value = _required_text(namespace, "namespace")
        content_value = _required_text(content, "content")
        source_value = _clean_text(source) or "local"
        tag_values = _normalize_tags(tags)
        confidence_value = _normalize_confidence(confidence)
        now = _utc_now()
        proposal = MemoryProposal(
            schema_version=SCHEMA_VERSION,
            id=_stable_id(
                "proposal",
                {
                    "project": project_value,
                    "namespace": namespace_value,
                    "content": content_value,
                    "source": source_value,
                    "tags": tag_values,
                    "confidence": confidence_value,
                },
            ),
            project=project_value,
            namespace=namespace_value,
            kind=PROPOSAL_KIND,
            content=content_value,
            source=source_value,
            tags=tag_values,
            confidence=confidence_value,
            status="pending",
            created_at=now,
            updated_at=now,
        )
        self._append_record(self._proposals_path, proposal)
        self._append_audit_event(
            event_type="proposal_created",
            target_id=proposal.id,
            project=proposal.project,
            namespace=proposal.namespace,
            actor=proposal.source,
            detail={"status": proposal.status},
        )
        return proposal

    def approve_proposal(
        self,
        proposal_id: str,
        approver: str,
        note: str | None = None,
    ) -> ApprovedMemory:
        proposal = self._pending_proposal_or_raise(proposal_id)
        approver_value = _required_text(approver, "approver")
        note_value = _optional_text(note)
        now = _utc_now()
        approved_proposal = MemoryProposal(
            **{
                **asdict(proposal),
                "status": "approved",
                "updated_at": now,
                "approver": approver_value,
                "note": note_value,
            }
        )
        memory = ApprovedMemory(
            schema_version=SCHEMA_VERSION,
            id=_stable_id("memory", {"proposal_id": proposal.id}),
            proposal_id=proposal.id,
            project=proposal.project,
            namespace=proposal.namespace,
            kind=APPROVED_MEMORY_KIND,
            content=proposal.content,
            source=proposal.source,
            tags=proposal.tags,
            confidence=proposal.confidence,
            status="approved",
            lifecycle="active",
            created_at=now,
            updated_at=now,
            approver=approver_value,
            note=note_value,
        )
        self._append_record(self._proposals_path, approved_proposal)
        self._append_record(self._memories_path, memory)
        self._append_audit_event(
            event_type="proposal_approved",
            target_id=proposal.id,
            project=proposal.project,
            namespace=proposal.namespace,
            actor=approver_value,
            detail={"memory_id": memory.id, "note": note_value, "status": "approved"},
        )
        return memory

    def reject_proposal(self, proposal_id: str, reviewer: str, reason: str) -> MemoryProposal:
        proposal = self._pending_proposal_or_raise(proposal_id)
        reviewer_value = _required_text(reviewer, "reviewer")
        reason_value = _required_text(reason, "reason")
        now = _utc_now()
        rejected = MemoryProposal(
            **{
                **asdict(proposal),
                "status": "rejected",
                "updated_at": now,
                "reviewer": reviewer_value,
                "reason": reason_value,
            }
        )
        self._append_record(self._proposals_path, rejected)
        self._append_audit_event(
            event_type="proposal_rejected",
            target_id=proposal.id,
            project=proposal.project,
            namespace=proposal.namespace,
            actor=reviewer_value,
            detail={"reason": reason_value, "status": "rejected"},
        )
        return rejected

    def set_memory_lifecycle(
        self,
        memory_id: str,
        lifecycle: str,
        *,
        actor: str,
        reason: str | None = None,
    ) -> ApprovedMemory:
        clean_id = _required_text(memory_id, "memory_id")
        lifecycle_value = _normalize_lifecycle(lifecycle)
        actor_value = _required_text(actor, "actor")
        reason_value = _optional_text(reason)
        records = self._read_jsonl(self._memories_path)
        memory_index: int | None = None
        memory: ApprovedMemory | None = None
        for index, record in enumerate(records):
            if str(record.get("id")) == clean_id:
                memory_index = index
                memory = _memory_from_record(record)
        if memory is None or memory_index is None:
            raise ValueError("memory_not_found")

        previous_lifecycle = memory.lifecycle
        now = _utc_now()
        updated = ApprovedMemory(
            **{
                **asdict(memory),
                "lifecycle": lifecycle_value,
                "updated_at": now,
            }
        )
        records[memory_index] = asdict(updated)
        self._write_jsonl(self._memories_path, records)
        self._append_audit_event(
            event_type="memory_lifecycle_updated",
            target_id=updated.id,
            project=updated.project,
            namespace=updated.namespace,
            actor=actor_value,
            detail={
                "previous_lifecycle": previous_lifecycle,
                "lifecycle": lifecycle_value,
                "reason": reason_value,
            },
        )
        return updated

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
        terms = _query_terms(query)
        if limit < 1:
            return []
        project_filter = _optional_text(project)
        namespace_filter = _optional_text(namespace)
        results: list[RecallResult] = []
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
            results.append(
                RecallResult(
                    memory_id=memory.id,
                    score=len(matched),
                    matched_terms=matched,
                    content=memory.content,
                    project=memory.project,
                    namespace=memory.namespace,
                    source=memory.source,
                    lifecycle=memory.lifecycle,
                )
            )
        results.sort(key=lambda item: (-item.score, item.project, item.namespace, item.memory_id))
        return results[:limit]

    def list_audit_events(self) -> list[AuditEvent]:
        return [AuditEvent(**record) for record in self._read_jsonl(self._audit_path)]

    def _pending_proposal_or_raise(self, proposal_id: str) -> MemoryProposal:
        clean_id = _required_text(proposal_id, "proposal_id")
        proposal = self._latest_proposals().get(clean_id)
        if proposal is None:
            raise ValueError("proposal_not_found")
        if proposal.status != "pending":
            raise ValueError(f"proposal_not_pending:{proposal.status}")
        return proposal

    def _latest_proposals(self) -> dict[str, MemoryProposal]:
        proposals: dict[str, MemoryProposal] = {}
        for record in self._read_jsonl(self._proposals_path):
            proposals[str(record["id"])] = _proposal_from_record(record)
        return proposals

    def _read_memories(self) -> list[ApprovedMemory]:
        return [_memory_from_record(record) for record in self._read_jsonl(self._memories_path)]

    def _append_audit_event(
        self,
        *,
        event_type: str,
        target_id: str,
        project: str,
        namespace: str,
        actor: str,
        detail: dict[str, Any],
    ) -> AuditEvent:
        now = _utc_now()
        event = AuditEvent(
            schema_version=SCHEMA_VERSION,
            id=_stable_id(
                "audit",
                {
                    "event_type": event_type,
                    "target_id": target_id,
                    "actor": actor,
                    "created_at": now,
                    "detail": detail,
                },
            ),
            kind=AUDIT_KIND,
            event_type=event_type,
            target_id=target_id,
            project=project,
            namespace=namespace,
            actor=actor,
            created_at=now,
            detail=dict(detail),
        )
        self._append_record(self._audit_path, event)
        return event

    def _append_record(self, path: Path, record: Any) -> None:
        self._assert_store_path(path)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(_stable_json(asdict(record)))
            handle.write("\n")

    def _write_jsonl(self, path: Path, records: list[dict[str, Any]]) -> None:
        self._assert_store_path(path)
        with path.open("w", encoding="utf-8") as handle:
            for record in records:
                handle.write(_stable_json(record))
                handle.write("\n")

    def _read_jsonl(self, path: Path) -> list[dict[str, Any]]:
        self._assert_store_path(path)
        if not path.exists():
            return []
        records: list[dict[str, Any]] = []
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    records.append(json.loads(line))
        return records

    def _assert_store_path(self, path: Path) -> None:
        allowed = {
            self._proposals_path.resolve(strict=False),
            self._memories_path.resolve(strict=False),
            self._audit_path.resolve(strict=False),
        }
        if path.resolve(strict=False) not in allowed:
            raise ValueError("path_outside_subspace_memory_store")


def _required_text(value: str, field: str) -> str:
    cleaned = _clean_text(value)
    if not cleaned:
        raise ValueError(f"{field}_must_be_non_empty")
    return cleaned


def _optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = _clean_text(value)
    return cleaned or None


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _normalize_tags(tags: Iterable[str] | None) -> tuple[str, ...]:
    return tuple(sorted({_clean_text(tag) for tag in tags or [] if _clean_text(tag)}))


def _normalize_confidence(confidence: float) -> float:
    value = float(confidence)
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


def _proposal_from_record(record: dict[str, Any]) -> MemoryProposal:
    return MemoryProposal(**{**record, "tags": tuple(record.get("tags", ()))})


def _memory_from_record(record: dict[str, Any]) -> ApprovedMemory:
    normalized = {
        **record,
        "tags": tuple(record.get("tags", ())),
        "lifecycle": _normalize_lifecycle(record.get("lifecycle", "active")),
    }
    return ApprovedMemory(**normalized)


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _stable_id(prefix: str, payload: dict[str, Any]) -> str:
    digest = hashlib.sha256(_stable_json(payload).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}:{SCHEMA_VERSION}:{digest}"


def _stable_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
