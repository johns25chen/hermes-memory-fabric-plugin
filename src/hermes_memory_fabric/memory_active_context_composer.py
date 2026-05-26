from __future__ import annotations

import re
from copy import deepcopy
from typing import Any, Iterable, Mapping

from hermes_memory_fabric.memory_retrieval_fusion import fuse_memory_retrieval_v2


ACTIVE_CONTEXT_COMPOSER_VERSION = "0.1"
ACTIVE_CONTEXT_PACKET_TYPE = "active_context_packet"
DEFAULT_CONTEXT_BUDGET_CHARS = 4000
DEFAULT_MEMORY_LIMIT = 5
DEFAULT_MAX_ACTIVE_SUBSPACES = 3
DEFAULT_NOW = "1970-01-01T00:00:00Z"

ACTIVE_CONTEXT_COMPOSER_POLICY = {
    "read_only": True,
    "would_write_memory": False,
    "would_modify_config": False,
    "would_write_graph": False,
    "writes_proposal_files": False,
    "writes_operation_ledger": False,
    "writes_token_files": False,
    "writes_approval_audit": False,
    "invokes_real_token_write_executor": False,
    "implements_real_token_write_executor": False,
    "exposes_provider_tools": False,
}

REQUIRED_ACTIVE_CONTEXT_PACKET_FIELDS = (
    "packet_type",
    "version",
    "query",
    "project_scope",
    "agent_scope",
    "selected_subspaces",
    "selected_memories",
    "rejected_subspaces",
    "rejected_memories",
    "context_items",
    "compact_context_text",
    "budget",
    "explanation",
    "policy",
)

_SPACE_RE = re.compile(r"\s+")


def compose_active_context(
    *,
    query: str,
    memory_candidates: Iterable[Mapping[str, Any]],
    subspace_registry: Mapping[str, Any] | None = None,
    context: Mapping[str, Any] | None = None,
    project_scope: str | None = None,
    agent_scope: str | None = None,
    entity_ids: Iterable[str] | None = None,
    now: Any | None = None,
    max_active_subspaces: int = DEFAULT_MAX_ACTIVE_SUBSPACES,
    memory_limit: int = DEFAULT_MEMORY_LIMIT,
    context_budget_chars: int = DEFAULT_CONTEXT_BUDGET_CHARS,
    include_archived: bool = False,
    allowed_risk_levels: Iterable[str] | None = None,
    required_tags: Iterable[str] | None = None,
    include_rejected: bool = False,
) -> dict[str, Any]:
    """Compose a deterministic, read-only active context packet."""
    candidates = [_copy_mapping(candidate) for candidate in _as_list(memory_candidates)]
    candidate_lookup = {
        _memory_id(candidate, index): candidate
        for index, candidate in enumerate(candidates)
    }
    budget_chars = _non_negative_int(context_budget_chars, DEFAULT_CONTEXT_BUDGET_CHARS)
    selected_limit = _non_negative_int(memory_limit, DEFAULT_MEMORY_LIMIT)
    subspace_limit = _non_negative_int(max_active_subspaces, DEFAULT_MAX_ACTIVE_SUBSPACES)

    fusion = fuse_memory_retrieval_v2(
        query=query,
        candidates=candidates,
        subspace_registry=deepcopy(dict(subspace_registry)) if isinstance(subspace_registry, Mapping) else None,
        context=deepcopy(dict(context)) if isinstance(context, Mapping) else None,
        project_scope=project_scope,
        agent_scope=agent_scope,
        entity_ids=list(entity_ids) if entity_ids is not None else None,
        now=now or DEFAULT_NOW,
        limit=selected_limit,
        include_archived=include_archived,
        allowed_risk_levels=list(allowed_risk_levels) if allowed_risk_levels is not None else None,
        required_tags=list(required_tags) if required_tags is not None else None,
        max_active_subspaces=subspace_limit,
    )

    selected_subspaces = deepcopy(list(fusion.get("selected_subspaces", [])))
    rejected_subspaces = deepcopy(list(fusion.get("rejected_subspaces", [])))
    selected_memories = deepcopy(list(fusion.get("selected_memories", [])))
    rejected_memories = deepcopy(list(fusion.get("rejected_memories", [])))
    context_items = _compose_context_items(
        selected_subspaces=selected_subspaces,
        selected_memories=selected_memories,
        rejected_memories=rejected_memories,
        candidate_lookup=candidate_lookup,
        subspace_selection_reasons=fusion.get("subspace_selection_reasons", {}),
        include_rejected=include_rejected,
        budget_chars=budget_chars,
    )
    compact_context_text = _compact_text(context_items)
    budget = {
        "context_budget_chars": budget_chars,
        "used_context_chars": len(compact_context_text),
        "remaining_context_chars": max(budget_chars - len(compact_context_text), 0),
        "context_item_count": len(context_items),
        "memory_limit": selected_limit,
        "max_active_subspaces": subspace_limit,
        "include_rejected": bool(include_rejected),
    }

    packet = {
        "packet_type": ACTIVE_CONTEXT_PACKET_TYPE,
        "version": ACTIVE_CONTEXT_COMPOSER_VERSION,
        "query": str(query),
        "project_scope": project_scope,
        "agent_scope": agent_scope,
        "selected_subspaces": selected_subspaces,
        "selected_memories": selected_memories,
        "rejected_subspaces": rejected_subspaces,
        "rejected_memories": rejected_memories,
        "context_items": context_items,
        "compact_context_text": compact_context_text,
        "budget": budget,
        "explanation": {},
        "policy": dict(ACTIVE_CONTEXT_COMPOSER_POLICY),
    }
    packet["explanation"] = _packet_explanation(packet, fusion)
    return packet


def validate_active_context_packet(packet: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the Active Context Composer packet contract without side effects."""
    if not isinstance(packet, Mapping):
        return {"valid": False, "errors": ["packet_must_be_mapping"]}

    errors: list[str] = []
    for field in REQUIRED_ACTIVE_CONTEXT_PACKET_FIELDS:
        if field not in packet:
            errors.append(f"missing_{field}")

    if packet.get("packet_type") != ACTIVE_CONTEXT_PACKET_TYPE:
        errors.append("packet_type_must_be_active_context_packet")
    if packet.get("version") != ACTIVE_CONTEXT_COMPOSER_VERSION:
        errors.append("version_must_be_0.1")
    if not isinstance(packet.get("context_items"), list):
        errors.append("context_items_must_be_list")

    budget = packet.get("budget")
    budget_chars = None
    if not isinstance(budget, Mapping):
        errors.append("budget_must_be_mapping")
    else:
        budget_chars = _non_negative_int(budget.get("context_budget_chars"), DEFAULT_CONTEXT_BUDGET_CHARS)

    compact_text = packet.get("compact_context_text")
    if not isinstance(compact_text, str):
        errors.append("compact_context_text_must_be_string")
    elif budget_chars is not None and len(compact_text) > budget_chars:
        errors.append("compact_context_text_exceeds_context_budget_chars")

    policy = packet.get("policy")
    if not isinstance(policy, Mapping):
        errors.append("policy_must_be_mapping")
    else:
        for key, expected in ACTIVE_CONTEXT_COMPOSER_POLICY.items():
            if key not in policy:
                errors.append(f"missing_policy_{key}")
            elif policy.get(key) is not expected:
                expected_text = "true" if expected is True else "false"
                errors.append(f"policy_{key}_must_be_{expected_text}")

    return {"valid": not errors, "errors": _dedupe_strings(errors)}


def explain_active_context_packet(packet: Mapping[str, Any]) -> dict[str, Any]:
    """Return selected/rejected ids, budget, reasons, and policy for a packet."""
    packet_map = _copy_mapping(packet)
    return {
        "version": "active_context_composer_v0.1",
        "selected_memory_ids": [
            _clean_text(item.get("id"))
            for item in _as_mappings(packet_map.get("selected_memories"))
            if _clean_text(item.get("id"))
        ],
        "rejected_memory_ids": [
            _clean_text(item.get("id"))
            for item in _as_mappings(packet_map.get("rejected_memories"))
            if _clean_text(item.get("id"))
        ],
        "selected_subspace_ids": [
            _clean_text(item.get("subspace_id"))
            for item in _as_mappings(packet_map.get("selected_subspaces"))
            if _clean_text(item.get("subspace_id"))
        ],
        "rejected_subspace_ids": [
            _clean_text(item.get("subspace_id"))
            for item in _as_mappings(packet_map.get("rejected_subspaces"))
            if _clean_text(item.get("subspace_id"))
        ],
        "context_item_ids": [
            _clean_text(item.get("item_id"))
            for item in _as_mappings(packet_map.get("context_items"))
            if _clean_text(item.get("item_id"))
        ],
        "budget": deepcopy(dict(packet_map.get("budget", {}))) if isinstance(packet_map.get("budget"), Mapping) else {},
        "selection_rejection_explanation": _selection_rejection_explanation(packet_map),
        "policy": _safe_policy(packet_map.get("policy")),
    }


def summarize_active_context_packet(packet: Mapping[str, Any]) -> dict[str, Any]:
    """Summarize selected/rejected counts, budget usage, and policy."""
    packet_map = _copy_mapping(packet)
    budget = dict(packet_map.get("budget", {})) if isinstance(packet_map.get("budget"), Mapping) else {}
    context_budget = _non_negative_int(budget.get("context_budget_chars"), DEFAULT_CONTEXT_BUDGET_CHARS)
    used_budget = len(packet_map.get("compact_context_text", "")) if isinstance(packet_map.get("compact_context_text"), str) else 0
    return {
        "version": "active_context_composer_v0.1",
        "selected_memory_count": len(_as_mappings(packet_map.get("selected_memories"))),
        "rejected_memory_count": len(_as_mappings(packet_map.get("rejected_memories"))),
        "selected_subspace_count": len(_as_mappings(packet_map.get("selected_subspaces"))),
        "rejected_subspace_count": len(_as_mappings(packet_map.get("rejected_subspaces"))),
        "context_item_count": len(_as_mappings(packet_map.get("context_items"))),
        "used_budget": used_budget,
        "budget_utilization_ratio": round(used_budget / context_budget, 4) if context_budget else 0.0,
        "policy": _safe_policy(packet_map.get("policy")),
    }


def _compose_context_items(
    *,
    selected_subspaces: list[dict[str, Any]],
    selected_memories: list[dict[str, Any]],
    rejected_memories: list[dict[str, Any]],
    candidate_lookup: Mapping[str, Mapping[str, Any]],
    subspace_selection_reasons: Any,
    include_rejected: bool,
    budget_chars: int,
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    used_text = ""
    reason_map = _reason_map(subspace_selection_reasons)

    for subspace in selected_subspaces:
        subspace_id = _clean_text(subspace.get("subspace_id"))
        text = _clean_text(subspace.get("active_summary"))
        if not subspace_id or not text:
            continue
        item = {
            "item_id": f"subspace_summary:{subspace_id}",
            "item_type": "subspace_summary",
            "source_id": subspace_id,
            "subspace_id": subspace_id,
            "project_id": _subspace_project_id(subspace),
            "text": text,
            "reason": reason_map.get(subspace_id, ["selected_subspace"]),
            "score": _score_from_reasons(reason_map.get(subspace_id, [])),
            "provenance": _subspace_provenance(subspace),
            "risk_level": _clean_text(subspace.get("risk_level")) or None,
        }
        used_text, added = _try_add_item(
            item=item,
            items=items,
            seen=seen,
            used_text=used_text,
            budget_chars=budget_chars,
        )
        if not added:
            continue

    sorted_memories = sorted(
        selected_memories,
        key=lambda item: (-_as_float(item.get("final_score")), _clean_text(item.get("id"))),
    )
    for memory in sorted_memories:
        memory_id = _clean_text(memory.get("id"))
        source = candidate_lookup.get(memory_id, {})
        item = _memory_context_item(
            memory=memory,
            source=source,
            item_id=f"memory:{memory_id}",
            rejected=False,
        )
        used_text, _ = _try_add_item(
            item=item,
            items=items,
            seen=seen,
            used_text=used_text,
            budget_chars=budget_chars,
        )

    if include_rejected:
        sorted_rejected = sorted(
            rejected_memories,
            key=lambda item: (-_as_float(item.get("final_score")), _clean_text(item.get("id"))),
        )
        for memory in sorted_rejected:
            memory_id = _clean_text(memory.get("id"))
            source = candidate_lookup.get(memory_id, {})
            item = _memory_context_item(
                memory=memory,
                source=source,
                item_id=f"rejected_memory:{memory_id}",
                rejected=True,
            )
            used_text, _ = _try_add_item(
                item=item,
                items=items,
                seen=seen,
                used_text=used_text,
                budget_chars=budget_chars,
            )

    return items


def _try_add_item(
    *,
    item: dict[str, Any],
    items: list[dict[str, Any]],
    seen: set[tuple[str, str]],
    used_text: str,
    budget_chars: int,
) -> tuple[str, bool]:
    text = _clean_text(item.get("text"))
    source_id = _clean_text(item.get("source_id"))
    dedupe_key = (_normalize_text(text), source_id)
    if not text or dedupe_key in seen:
        return used_text, False

    candidate_items = items + [item]
    next_text = _compact_text(candidate_items)
    if len(next_text) > budget_chars:
        return used_text, False

    seen.add(dedupe_key)
    items.append(item)
    return next_text, True


def _memory_context_item(
    *,
    memory: Mapping[str, Any],
    source: Mapping[str, Any],
    item_id: str,
    rejected: bool,
) -> dict[str, Any]:
    memory_id = _clean_text(memory.get("id") or source.get("id"))
    text = _clean_text(memory.get("text") or _candidate_text(source))
    reason = _memory_reason(memory, rejected)
    if rejected:
        text = f"[REJECTED] {text}" if text else "[REJECTED]"
    return {
        "item_id": item_id,
        "item_type": "memory",
        "source_id": _source_id(memory, source, memory_id),
        "subspace_id": _clean_text(memory.get("subspace_id") or source.get("subspace_id")) or None,
        "project_id": _clean_text(memory.get("project_id") or source.get("project_id") or source.get("project_scope")) or None,
        "text": text,
        "reason": reason,
        "score": _as_float(memory.get("final_score")),
        "provenance": deepcopy(memory.get("provenance") if memory.get("provenance") is not None else source.get("provenance")),
        "risk_level": _clean_text(memory.get("risk_level") or source.get("risk_level") or source.get("risk")) or None,
    }


def _compact_text(items: Iterable[Mapping[str, Any]]) -> str:
    lines: list[str] = []
    for item in items:
        item_type = _clean_text(item.get("item_type"))
        source_id = _clean_text(item.get("source_id"))
        text = _clean_text(item.get("text"))
        if not text:
            continue
        if item_type == "subspace_summary":
            lines.append(f"[SUBSPACE {source_id}] {text}")
        elif text.startswith("[REJECTED]"):
            lines.append(f"[REJECTED MEMORY {source_id}] {text.removeprefix('[REJECTED]').strip()}")
        else:
            lines.append(f"[MEMORY {source_id}] {text}")
    return "\n".join(lines)


def _packet_explanation(packet: Mapping[str, Any], fusion: Mapping[str, Any]) -> dict[str, Any]:
    explanation = explain_active_context_packet(packet)
    explanation.update(
        {
            "fusion_explanation": deepcopy(dict(fusion.get("explanation", {})))
            if isinstance(fusion.get("explanation"), Mapping)
            else {},
            "rules": [
                "Recall Fusion v2 selects and rejects memory candidates before composition.",
                "Selected subspace summaries are considered before memory content and only included if they fit.",
                "Selected memories are ordered by final_score, then memory id.",
                "Context items are deduplicated by normalized text and source id.",
                "Rejected memories are excluded from compact_context_text unless include_rejected is true.",
                "The composer is deterministic, local, and read-only.",
            ],
        }
    )
    return explanation


def _selection_rejection_explanation(packet: Mapping[str, Any]) -> dict[str, Any]:
    embedded = packet.get("explanation") if isinstance(packet.get("explanation"), Mapping) else {}
    fusion = embedded.get("fusion_explanation") if isinstance(embedded, Mapping) else {}
    fusion = fusion if isinstance(fusion, Mapping) else {}
    return {
        "selected_memories": {
            _clean_text(item.get("id")): list(_as_list(item.get("why_selected")))
            for item in _as_mappings(packet.get("selected_memories"))
            if _clean_text(item.get("id"))
        },
        "rejected_memories": {
            _clean_text(item.get("id")): _clean_text(item.get("reason"))
            for item in _as_mappings(packet.get("rejected_memories"))
            if _clean_text(item.get("id"))
        },
        "selected_subspaces": {
            _clean_text(item.get("subspace_id")): "selected_for_active_context"
            for item in _as_mappings(packet.get("selected_subspaces"))
            if _clean_text(item.get("subspace_id"))
        },
        "rejected_subspaces": {
            _clean_text(item.get("subspace_id")): "rejected_by_subspace_index"
            for item in _as_mappings(packet.get("rejected_subspaces"))
            if _clean_text(item.get("subspace_id"))
        },
        "subspace_selection_reasons": deepcopy(dict(fusion.get("subspace_selection_reasons", {})))
        if isinstance(fusion.get("subspace_selection_reasons"), Mapping)
        else {},
        "subspace_rejected_reasons": deepcopy(dict(fusion.get("subspace_rejected_reasons", {})))
        if isinstance(fusion.get("subspace_rejected_reasons"), Mapping)
        else {},
    }


def _reason_map(value: Any) -> dict[str, list[str]]:
    if not isinstance(value, Mapping):
        return {}
    return {
        _clean_text(key): [_clean_text(reason) for reason in _as_list(value[key]) if _clean_text(reason)]
        for key in sorted(value, key=lambda item: str(item))
        if _clean_text(key)
    }


def _memory_reason(memory: Mapping[str, Any], rejected: bool) -> list[str]:
    if rejected:
        reason = _clean_text(memory.get("reason")) or "rejected"
        return [f"rejected:{reason}"]
    reasons = [_clean_text(reason) for reason in _as_list(memory.get("why_selected")) if _clean_text(reason)]
    return reasons or ["selected_memory"]


def _score_from_reasons(reasons: Iterable[Any]) -> float:
    for reason in reasons:
        text = _clean_text(reason)
        if text.startswith("score:"):
            return _as_float(text.split(":", 1)[1])
    return 0.0


def _candidate_text(candidate: Mapping[str, Any]) -> str:
    parts = [
        candidate.get("title"),
        candidate.get("summary"),
        candidate.get("content"),
        candidate.get("text"),
    ]
    return " ".join(_clean_text(part) for part in parts if _clean_text(part))


def _source_id(memory: Mapping[str, Any], source: Mapping[str, Any], memory_id: str) -> str:
    for value in (
        source.get("source_id"),
        memory.get("source_id"),
        memory.get("provenance"),
        source.get("provenance"),
        memory.get("source"),
        source.get("source"),
        memory_id,
    ):
        text = _clean_text(value)
        if text:
            return text
    return memory_id


def _subspace_project_id(subspace: Mapping[str, Any]) -> str | None:
    scope = subspace.get("scope")
    if isinstance(scope, Mapping):
        for key in ("project_scope", "project_id", "scope_id"):
            value = _clean_text(scope.get(key))
            if value:
                return value
    return None


def _subspace_provenance(subspace: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "source_index": deepcopy(subspace.get("source_index")),
        "fact_graph_ref": deepcopy(subspace.get("fact_graph_ref")),
        "memory_blocks_ref": deepcopy(subspace.get("memory_blocks_ref")),
    }


def _memory_id(candidate: Mapping[str, Any], index: int) -> str:
    return _clean_text(candidate.get("id") or candidate.get("memory_id") or f"candidate_{index}")


def _normalize_text(value: Any) -> str:
    return _SPACE_RE.sub(" ", _clean_text(value).lower())


def _safe_policy(policy: Any) -> dict[str, Any]:
    if not isinstance(policy, Mapping):
        return dict(ACTIVE_CONTEXT_COMPOSER_POLICY)
    safe = dict(ACTIVE_CONTEXT_COMPOSER_POLICY)
    for key, expected in ACTIVE_CONTEXT_COMPOSER_POLICY.items():
        safe[key] = policy.get(key) if policy.get(key) is expected else expected
    return safe


def _copy_mapping(value: Any) -> dict[str, Any]:
    return deepcopy(dict(value)) if isinstance(value, Mapping) else {}


def _as_mappings(value: Any) -> list[dict[str, Any]]:
    return [_copy_mapping(item) for item in _as_list(value) if isinstance(item, Mapping)]


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return list(value)
    if isinstance(value, (str, bytes, bytearray)):
        return [value]
    try:
        return list(value)
    except TypeError:
        return [value]


def _as_float(value: Any) -> float:
    try:
        return round(float(value), 4)
    except (TypeError, ValueError):
        return 0.0


def _non_negative_int(value: Any, default: int) -> int:
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return default


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _dedupe_strings(values: Iterable[Any]) -> list[str]:
    deduped: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = _clean_text(value)
        if text and text not in seen:
            seen.add(text)
            deduped.append(text)
    return deduped
