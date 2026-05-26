from __future__ import annotations

import re
from copy import deepcopy
from datetime import UTC, datetime
from typing import Any, Iterable, Mapping

from hermes_memory_fabric.memory_subspace_index import select_subspaces_for_context


FUSION_POLICY = {
    "read_only": True,
    "would_write_memory": False,
    "would_modify_config": False,
    "would_write_graph": False,
    "does_not_create_operation_events": True,
}

FUSION_POLICY_V2 = {
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

SCORING_DIMENSIONS = (
    "semantic_score",
    "keyword_score",
    "entity_score",
    "temporal_score",
    "project_scope_score",
    "source_trust_score",
    "governance_score",
    "final_score",
)

SCORING_DIMENSIONS_V2 = (
    "semantic_score",
    "keyword_score",
    "entity_score",
    "temporal_score",
    "project_scope_score",
    "subspace_score",
    "source_trust_score",
    "governance_score",
    "risk_score",
    "final_score",
)

WEIGHTS = {
    "semantic_score": 0.22,
    "keyword_score": 0.2,
    "entity_score": 0.12,
    "temporal_score": 0.14,
    "project_scope_score": 0.13,
    "source_trust_score": 0.09,
    "governance_score": 0.1,
}

WEIGHTS_V2 = {
    "semantic_score": 0.18,
    "keyword_score": 0.17,
    "entity_score": 0.1,
    "temporal_score": 0.11,
    "project_scope_score": 0.12,
    "subspace_score": 0.14,
    "source_trust_score": 0.07,
    "governance_score": 0.07,
    "risk_score": 0.04,
}

SELECTION_THRESHOLD = 0.35
DEFAULT_LIMIT = 5
DEFAULT_ALLOWED_RISK_LEVELS_V2 = ("low", "medium")
HIGH_RISK_LEVELS_V2 = {"high", "critical"}

_TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9_-]*", re.IGNORECASE)
_UNSAFE_TEXT_MARKERS = (
    "direct_write",
    "direct memory write",
    "write_memory",
    "write graph",
    "modify config",
    "approve allowlist",
    "operation ledger event",
    "create proposal",
)
_UNSAFE_BOOL_KEYS = (
    "unsafe",
    "write_allowed",
    "would_write_memory",
    "would_modify_config",
    "would_write_graph",
    "creates_operation_event",
    "create_operation_event",
    "approves_allowlist",
    "approve_allowlist",
    "external_auto_recall_allowed",
    "writes_proposal_files",
    "writes_operation_ledger",
    "writes_token_files",
    "writes_approval_audit",
    "invokes_real_token_write_executor",
    "implements_real_token_write_executor",
    "exposes_provider_tools",
)


def fuse_memory_retrieval(
    *,
    query: str,
    candidates: Iterable[Mapping[str, Any]],
    project_scope: str | None = None,
    entity_ids: Iterable[str] | None = None,
    now: str | datetime | None = None,
    limit: int = DEFAULT_LIMIT,
) -> dict[str, Any]:
    """Rank candidate memory records without writing memory, config, graph, or ledger state."""
    evaluation_now = _coerce_datetime(now) or datetime.now(UTC)
    query_tokens = _tokens(query)
    entity_set = {str(entity_id) for entity_id in entity_ids or [] if str(entity_id)}
    scored = [
        _score_candidate(
            query=query,
            query_tokens=query_tokens,
            candidate=dict(candidate),
            project_scope=project_scope,
            query_entity_ids=entity_set,
            now=evaluation_now,
            index=index,
        )
        for index, candidate in enumerate(candidates)
    ]
    scored.sort(key=lambda item: (-item["final_score"], str(item["id"]), item["_index"]))

    selected: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for item in scored:
        hard_reject = item.pop("_hard_reject")
        index = item.pop("_index")
        item["_index"] = index
        if hard_reject:
            rejected.append(_rejected_item(item, item["reason"]))
        elif len(selected) < limit and item["final_score"] >= SELECTION_THRESHOLD:
            selected.append(_selected_item(item))
        else:
            reason = "ranked_below_limit" if len(selected) >= limit else "below_selection_threshold"
            rejected.append(_rejected_item(item, reason))

    return {
        "query": query,
        "selected_memories": selected,
        "rejected_memories": rejected,
        "scores": {str(item["id"]): item["component_scores"] | {"final_score": item["final_score"]} for item in scored},
        "policy": dict(FUSION_POLICY),
        "explanation": {
            "version": "hybrid_retrieval_fusion_v0.1",
            "scoring_dimensions": list(SCORING_DIMENSIONS),
            "weights": dict(WEIGHTS),
            "selection_threshold": SELECTION_THRESHOLD,
            "limit": limit,
            "now": evaluation_now.isoformat().replace("+00:00", "Z"),
            "rules": [
                "Unsafe governance indicators are rejected before selection.",
                "Project-scoped queries hard-reject candidates from unrelated projects.",
                "Expired or future-validity candidates are penalized by temporal_score.",
                "All non-selected candidates remain visible in rejected_memories.",
            ],
        },
    }


def fuse_memory_retrieval_v2(
    *,
    query: str,
    candidates: Iterable[Mapping[str, Any]],
    subspace_registry: Mapping[str, Any] | None = None,
    context: Mapping[str, Any] | None = None,
    project_scope: str | None = None,
    agent_scope: str | None = None,
    entity_ids: Iterable[str] | None = None,
    now: str | datetime | None = None,
    limit: int = DEFAULT_LIMIT,
    include_archived: bool = False,
    allowed_risk_levels: Iterable[str] | None = None,
    required_tags: Iterable[str] | None = None,
    max_active_subspaces: int | None = None,
) -> dict[str, Any]:
    """Rank memory records through governed, deterministic subspace-aware fusion."""
    evaluation_now = _coerce_datetime(now) or datetime.now(UTC)
    context_map = _build_v2_context(
        query=query,
        context=context,
        project_scope=project_scope,
        agent_scope=agent_scope,
        include_archived=include_archived,
        allowed_risk_levels=allowed_risk_levels,
        required_tags=required_tags,
        max_active_subspaces=max_active_subspaces,
    )
    effective_project_scope = (
        _strip_scope_prefix_v2(_clean_text(project_scope) or _clean_text(context_map.get("project_scope")), "project")
        or None
    )
    effective_agent_scope = (
        _strip_scope_prefix_v2(_clean_text(agent_scope) or _clean_text(context_map.get("agent_scope")), "agent")
        or None
    )
    effective_entity_ids = entity_ids if entity_ids is not None else context_map.get("entity_ids")
    query_tokens = _tokens(query)
    entity_set = {str(entity_id) for entity_id in _as_list(effective_entity_ids) if str(entity_id)}
    allowed_risks = _allowed_risk_levels_v2(context_map.get("allowed_risk_levels"))

    subspace_selection = (
        select_subspaces_for_context(subspace_registry, context_map)
        if subspace_registry is not None
        else _empty_subspace_selection(max_active_subspaces=max_active_subspaces)
    )
    subspace_state = _build_subspace_state(subspace_selection)

    scored = [
        _score_candidate_v2(
            query=query,
            query_tokens=query_tokens,
            candidate=_copy_candidate(candidate),
            project_scope=effective_project_scope,
            agent_scope=effective_agent_scope,
            query_entity_ids=entity_set,
            now=evaluation_now,
            index=index,
            include_archived=include_archived,
            allowed_risk_levels=allowed_risks,
            subspace_state=subspace_state,
            has_subspace_registry=subspace_registry is not None,
        )
        for index, candidate in enumerate(candidates)
    ]
    scored.sort(key=lambda item: (-item["final_score"], str(item["id"]), item["_index"]))

    selection_limit = _selection_limit(limit)
    selected: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for item in scored:
        hard_reject = item.pop("_hard_reject")
        index = item.pop("_index")
        item["_index"] = index
        if hard_reject:
            rejected.append(_rejected_item_v2(item, item["reason"]))
        elif len(selected) < selection_limit and item["final_score"] >= SELECTION_THRESHOLD:
            selected.append(_selected_item_v2(item))
        else:
            reason = "ranked_below_limit" if len(selected) >= selection_limit else "below_selection_threshold"
            rejected.append(_rejected_item_v2(item, reason))

    result = {
        "query": query,
        "selected_memories": selected,
        "rejected_memories": rejected,
        "selected_subspaces": deepcopy(subspace_selection.get("selected_subspaces", [])),
        "rejected_subspaces": deepcopy(subspace_selection.get("rejected_subspaces", [])),
        "subspace_selection_reasons": _sort_reason_map_v2(subspace_selection.get("selection_reasons")),
        "subspace_rejected_reasons": _sort_reason_map_v2(subspace_selection.get("rejected_reasons")),
        "active_context_budget": deepcopy(dict(subspace_selection.get("active_context_budget", {}))),
        "scores": {
            str(item["id"]): item["component_scores"] | {"final_score": item["final_score"], "reason": item["reason"]}
            for item in scored
        },
        "policy": dict(FUSION_POLICY_V2),
    }
    result["explanation"] = explain_memory_retrieval_v2_result(result)
    return result


def explain_memory_retrieval_v2_result(result: Mapping[str, Any]) -> dict[str, Any]:
    """Return a stable explanation for a Recall Fusion v2 result."""
    result_map = _as_mapping_copy(result)
    selected_memories = _as_list(result_map.get("selected_memories"))
    rejected_memories = _as_list(result_map.get("rejected_memories"))
    selected_subspaces = _as_list(result_map.get("selected_subspaces"))
    rejected_subspaces = _as_list(result_map.get("rejected_subspaces"))
    return {
        "version": "memory_recall_fusion_v2",
        "selected_memory_ids": [_clean_text(item.get("id")) for item in selected_memories if isinstance(item, Mapping)],
        "rejected_memory_ids": [_clean_text(item.get("id")) for item in rejected_memories if isinstance(item, Mapping)],
        "selected_subspace_ids": [
            _clean_text(item.get("subspace_id")) for item in selected_subspaces if isinstance(item, Mapping)
        ],
        "rejected_subspace_ids": [
            _clean_text(item.get("subspace_id")) for item in rejected_subspaces if isinstance(item, Mapping)
        ],
        "subspace_selection_reasons": _sort_reason_map_v2(result_map.get("subspace_selection_reasons")),
        "subspace_rejected_reasons": _sort_reason_map_v2(result_map.get("subspace_rejected_reasons")),
        "memory_rejection_reasons": {
            _clean_text(item.get("id")): _clean_text(item.get("reason"))
            for item in rejected_memories
            if isinstance(item, Mapping) and _clean_text(item.get("id"))
        },
        "memory_selection_reasons": {
            _clean_text(item.get("id")): [str(reason) for reason in _as_list(item.get("why_selected"))]
            for item in selected_memories
            if isinstance(item, Mapping) and _clean_text(item.get("id"))
        },
        "scoring_dimensions": list(SCORING_DIMENSIONS_V2),
        "weights": dict(WEIGHTS_V2),
        "selection_threshold": SELECTION_THRESHOLD,
        "active_context_budget": deepcopy(dict(result_map.get("active_context_budget", {}))),
        "rules": [
            "Subspace Index selection is used when a registry is provided.",
            "Selected subspace id, project scope, or agent scope matches boost subspace_score.",
            "Unsafe governance indicators are rejected before selection.",
            "Project-scoped queries hard-reject candidates from unrelated projects.",
            "Archived subspace candidates are rejected unless include_archived is true.",
            "High and critical risk candidates require explicit allowed_risk_levels.",
            "All decisions are deterministic and read-only.",
        ],
        "policy": _safe_policy_v2(result_map.get("policy")),
    }


def summarize_memory_retrieval_v2_result(result: Mapping[str, Any]) -> dict[str, Any]:
    """Summarize Recall Fusion v2 selected/rejected memory and subspace counts."""
    result_map = _as_mapping_copy(result)
    selected_memories = _as_list(result_map.get("selected_memories"))
    rejected_memories = _as_list(result_map.get("rejected_memories"))
    selected_subspaces = _as_list(result_map.get("selected_subspaces"))
    rejected_subspaces = _as_list(result_map.get("rejected_subspaces"))
    return {
        "version": "memory_recall_fusion_v2",
        "selected_memory_count": len(selected_memories),
        "rejected_memory_count": len(rejected_memories),
        "selected_subspace_count": len(selected_subspaces),
        "rejected_subspace_count": len(rejected_subspaces),
        "top_selected_memory_id": (
            selected_memories[0].get("id") if selected_memories and isinstance(selected_memories[0], Mapping) else None
        ),
        "policy": _safe_policy_v2(result_map.get("policy")),
    }


def _score_candidate(
    *,
    query: str,
    query_tokens: set[str],
    candidate: dict[str, Any],
    project_scope: str | None,
    query_entity_ids: set[str],
    now: datetime,
    index: int,
) -> dict[str, Any]:
    candidate_id = str(candidate.get("id") or f"candidate_{index}")
    text = _candidate_text(candidate)
    candidate_tokens = _tokens(text)
    governance_score, unsafe_reasons = _governance_score(candidate.get("governance"))
    project_score = _project_scope_score(candidate.get("project_id"), project_scope)
    temporal_score = _temporal_score(candidate, now)
    component_scores = {
        "semantic_score": _semantic_score(query_tokens, candidate_tokens),
        "keyword_score": _keyword_score(query, query_tokens, text, candidate_tokens),
        "entity_score": _entity_score(candidate.get("entity_ids"), query_entity_ids),
        "temporal_score": temporal_score,
        "project_scope_score": project_score,
        "source_trust_score": _source_trust_score(candidate),
        "governance_score": governance_score,
    }
    final_score = round(sum(component_scores[name] * weight for name, weight in WEIGHTS.items()), 4)

    reason = "eligible"
    hard_reject = False
    if unsafe_reasons:
        reason = "unsafe_governance:" + ",".join(unsafe_reasons)
        hard_reject = True
    elif project_scope and candidate.get("project_id") and str(candidate.get("project_id")) != str(project_scope):
        reason = "project_scope_mismatch"
        hard_reject = True

    return {
        "id": candidate_id,
        "text": text,
        "project_id": candidate.get("project_id"),
        "source": candidate.get("source"),
        "provenance": candidate.get("provenance"),
        "component_scores": component_scores,
        "final_score": final_score,
        "reason": reason,
        "_hard_reject": hard_reject,
        "_index": index,
    }


def _score_candidate_v2(
    *,
    query: str,
    query_tokens: set[str],
    candidate: dict[str, Any],
    project_scope: str | None,
    agent_scope: str | None,
    query_entity_ids: set[str],
    now: datetime,
    index: int,
    include_archived: bool,
    allowed_risk_levels: set[str],
    subspace_state: Mapping[str, Any],
    has_subspace_registry: bool,
) -> dict[str, Any]:
    candidate_id = str(candidate.get("id") or candidate.get("memory_id") or f"candidate_{index}")
    text = _candidate_text(candidate)
    candidate_tokens = _tokens(text)
    governance_score, unsafe_reasons = _governance_score(_candidate_governance(candidate))
    candidate_project_scope = _candidate_project_scope(candidate)
    candidate_subspace_ids = _candidate_subspace_ids(candidate)
    risk_level = _candidate_risk_level(candidate)
    subspace_score, subspace_matches = _subspace_score(
        candidate=candidate,
        candidate_subspace_ids=candidate_subspace_ids,
        candidate_project_scope=candidate_project_scope,
        agent_scope=agent_scope,
        subspace_state=subspace_state,
        has_subspace_registry=has_subspace_registry,
    )
    component_scores = {
        "semantic_score": _semantic_score(query_tokens, candidate_tokens),
        "keyword_score": _keyword_score(query, query_tokens, text, candidate_tokens),
        "entity_score": _entity_score(candidate.get("entity_ids"), query_entity_ids),
        "temporal_score": _temporal_score(candidate, now),
        "project_scope_score": _project_scope_score(candidate_project_scope or None, project_scope),
        "subspace_score": subspace_score,
        "source_trust_score": _source_trust_score(candidate),
        "governance_score": governance_score,
        "risk_score": _risk_score(risk_level),
    }
    final_score = round(sum(component_scores[name] * weight for name, weight in WEIGHTS_V2.items()), 4)

    reason = "eligible"
    hard_reject = False
    archived_reason = _archived_subspace_rejection_reason(
        candidate=candidate,
        candidate_subspace_ids=candidate_subspace_ids,
        subspace_state=subspace_state,
        include_archived=include_archived,
    )
    if unsafe_reasons:
        reason = "unsafe_governance:" + ",".join(unsafe_reasons)
        hard_reject = True
    elif project_scope and candidate_project_scope and candidate_project_scope != str(project_scope):
        reason = "project_scope_mismatch"
        hard_reject = True
    elif archived_reason:
        reason = archived_reason
        hard_reject = True
    elif risk_level in HIGH_RISK_LEVELS_V2 and risk_level not in allowed_risk_levels:
        reason = f"risk_level_not_allowed:{risk_level}"
        hard_reject = True

    return {
        "id": candidate_id,
        "text": text,
        "project_id": candidate_project_scope or candidate.get("project_id"),
        "subspace_id": candidate_subspace_ids[0] if candidate_subspace_ids else candidate.get("subspace_id"),
        "source": candidate.get("source"),
        "provenance": candidate.get("provenance"),
        "risk_level": risk_level or None,
        "subspace_matches": subspace_matches,
        "component_scores": component_scores,
        "final_score": final_score,
        "why_selected": _why_selected_v2(
            component_scores=component_scores,
            final_score=final_score,
            project_scope=project_scope,
            risk_level=risk_level,
            subspace_matches=subspace_matches,
            query_entity_ids=query_entity_ids,
        ),
        "reason": reason,
        "_hard_reject": hard_reject,
        "_index": index,
    }


def _selected_item(item: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "id": item["id"],
        "text": item["text"],
        "project_id": item.get("project_id"),
        "source": item.get("source"),
        "provenance": item.get("provenance"),
        "final_score": item["final_score"],
        "component_scores": dict(item["component_scores"]),
    }


def _selected_item_v2(item: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "id": item["id"],
        "text": item["text"],
        "project_id": item.get("project_id"),
        "subspace_id": item.get("subspace_id"),
        "source": item.get("source"),
        "provenance": item.get("provenance"),
        "risk_level": item.get("risk_level"),
        "final_score": item["final_score"],
        "component_scores": dict(item["component_scores"]),
        "subspace_matches": deepcopy(list(item.get("subspace_matches", []))),
        "why_selected": list(item.get("why_selected", [])),
    }


def _rejected_item(item: Mapping[str, Any], reason: str) -> dict[str, Any]:
    return {
        "id": item["id"],
        "reason": reason,
        "final_score": item["final_score"],
        "component_scores": dict(item["component_scores"]),
    }


def _rejected_item_v2(item: Mapping[str, Any], reason: str) -> dict[str, Any]:
    return {
        "id": item["id"],
        "reason": reason,
        "project_id": item.get("project_id"),
        "subspace_id": item.get("subspace_id"),
        "risk_level": item.get("risk_level"),
        "final_score": item["final_score"],
        "component_scores": dict(item["component_scores"]),
        "subspace_matches": deepcopy(list(item.get("subspace_matches", []))),
    }


def _candidate_text(candidate: Mapping[str, Any]) -> str:
    parts = [
        candidate.get("title"),
        candidate.get("summary"),
        candidate.get("content"),
        candidate.get("text"),
    ]
    return " ".join(str(part) for part in parts if part)


def _copy_candidate(candidate: Any) -> dict[str, Any]:
    if isinstance(candidate, Mapping):
        return deepcopy(dict(candidate))
    return {"content": str(candidate)}


def _build_v2_context(
    *,
    query: str,
    context: Mapping[str, Any] | None,
    project_scope: str | None,
    agent_scope: str | None,
    include_archived: bool,
    allowed_risk_levels: Iterable[str] | None,
    required_tags: Iterable[str] | None,
    max_active_subspaces: int | None,
) -> dict[str, Any]:
    context_map = _as_mapping_copy(context)
    context_map["query"] = query
    if project_scope is not None:
        context_map["project_scope"] = _strip_scope_prefix_v2(_clean_text(project_scope), "project")
    elif context_map.get("project_scope") is not None:
        context_map["project_scope"] = _strip_scope_prefix_v2(_clean_text(context_map.get("project_scope")), "project")
    if agent_scope is not None:
        context_map["agent_scope"] = _strip_scope_prefix_v2(_clean_text(agent_scope), "agent")
    elif context_map.get("agent_scope") is not None:
        context_map["agent_scope"] = _strip_scope_prefix_v2(_clean_text(context_map.get("agent_scope")), "agent")
    context_map["include_archived"] = bool(include_archived)
    if allowed_risk_levels is not None:
        context_map["allowed_risk_levels"] = list(allowed_risk_levels)
    elif "allowed_risk_levels" not in context_map:
        context_map["allowed_risk_levels"] = list(DEFAULT_ALLOWED_RISK_LEVELS_V2)
    if required_tags is not None:
        context_map["required_tags"] = list(required_tags)
    if max_active_subspaces is not None:
        context_map["max_active_subspaces"] = max_active_subspaces
    return context_map


def _empty_subspace_selection(max_active_subspaces: int | None) -> dict[str, Any]:
    budget = DEFAULT_LIMIT if max_active_subspaces is None else _selection_limit(max_active_subspaces)
    return {
        "selected_subspaces": [],
        "rejected_subspaces": [],
        "selection_reasons": {},
        "rejected_reasons": {},
        "active_context_budget": {
            "max_active_subspaces": budget,
            "eligible_subspace_count": 0,
            "selected_subspace_count": 0,
            "rejected_subspace_count": 0,
        },
        "policy": dict(FUSION_POLICY_V2),
    }


def _build_subspace_state(selection: Mapping[str, Any]) -> dict[str, Any]:
    selected_subspaces = [item for item in _as_list(selection.get("selected_subspaces")) if isinstance(item, Mapping)]
    rejected_subspaces = [item for item in _as_list(selection.get("rejected_subspaces")) if isinstance(item, Mapping)]
    selected_ids = {_clean_text(item.get("subspace_id")) for item in selected_subspaces if _clean_text(item.get("subspace_id"))}
    rejected_reasons = _sort_reason_map_v2(selection.get("rejected_reasons"))
    rejected_ids = {_clean_text(item.get("subspace_id")) for item in rejected_subspaces if _clean_text(item.get("subspace_id"))}
    archived_ids = {
        _clean_text(item.get("subspace_id"))
        for item in selected_subspaces + rejected_subspaces
        if _clean_text(item.get("subspace_id")) and _clean_text(item.get("lifecycle_status")) == "archived"
    }
    archived_ids.update(
        subspace_id
        for subspace_id, reasons in rejected_reasons.items()
        if any(reason == "archived_excluded" for reason in reasons)
    )

    selected_project_scopes: dict[str, list[str]] = {}
    selected_agent_scopes: dict[str, list[str]] = {}
    rejected_project_scopes: dict[str, list[str]] = {}
    for subspace in selected_subspaces:
        subspace_id = _clean_text(subspace.get("subspace_id"))
        project = _subspace_project_scope_v2(subspace)
        agent = _subspace_agent_scope_v2(subspace)
        if subspace_id and project:
            selected_project_scopes.setdefault(project, []).append(subspace_id)
        if subspace_id and agent:
            selected_agent_scopes.setdefault(agent, []).append(subspace_id)
    for subspace in rejected_subspaces:
        subspace_id = _clean_text(subspace.get("subspace_id"))
        project = _subspace_project_scope_v2(subspace)
        if subspace_id and project:
            rejected_project_scopes.setdefault(project, []).append(subspace_id)

    return {
        "selected_ids": selected_ids,
        "rejected_ids": rejected_ids,
        "archived_ids": archived_ids,
        "selected_project_scopes": {key: sorted(value) for key, value in selected_project_scopes.items()},
        "selected_agent_scopes": {key: sorted(value) for key, value in selected_agent_scopes.items()},
        "rejected_project_scopes": {key: sorted(value) for key, value in rejected_project_scopes.items()},
        "rejected_reasons": rejected_reasons,
    }


def _subspace_score(
    *,
    candidate: Mapping[str, Any],
    candidate_subspace_ids: list[str],
    candidate_project_scope: str,
    agent_scope: str | None,
    subspace_state: Mapping[str, Any],
    has_subspace_registry: bool,
) -> tuple[float, list[dict[str, str]]]:
    matches: list[dict[str, str]] = []
    selected_ids = set(subspace_state.get("selected_ids", set()))
    selected_project_scopes = _mapping_of_lists(subspace_state.get("selected_project_scopes"))
    selected_agent_scopes = _mapping_of_lists(subspace_state.get("selected_agent_scopes"))

    for subspace_id in candidate_subspace_ids:
        if subspace_id in selected_ids:
            matches.append({"subspace_id": subspace_id, "match_type": "subspace_id"})

    if candidate_project_scope and candidate_project_scope in selected_project_scopes:
        for subspace_id in selected_project_scopes[candidate_project_scope]:
            matches.append({"subspace_id": subspace_id, "match_type": "project_scope"})

    candidate_agent_scope = _candidate_agent_scope(candidate) or _clean_text(agent_scope)
    if candidate_agent_scope and candidate_agent_scope in selected_agent_scopes:
        for subspace_id in selected_agent_scopes[candidate_agent_scope]:
            matches.append({"subspace_id": subspace_id, "match_type": "agent_scope"})

    deduped_matches = _dedupe_matches(matches)
    match_types = {item["match_type"] for item in deduped_matches}
    if "subspace_id" in match_types:
        return 1.0, deduped_matches
    if "project_scope" in match_types:
        return 0.9, deduped_matches
    if "agent_scope" in match_types:
        return 0.8, deduped_matches
    if not has_subspace_registry:
        return 0.5, []
    if selected_ids:
        return 0.15, []
    return 0.0, []


def _archived_subspace_rejection_reason(
    *,
    candidate: Mapping[str, Any],
    candidate_subspace_ids: list[str],
    subspace_state: Mapping[str, Any],
    include_archived: bool,
) -> str | None:
    if include_archived:
        return None
    if candidate.get("archived") is True:
        return "archived_subspace_excluded"
    lifecycle = _clean_text(candidate.get("subspace_lifecycle_status") or candidate.get("lifecycle_status"))
    if lifecycle == "archived":
        return "archived_subspace_excluded"
    archived_ids = set(subspace_state.get("archived_ids", set()))
    for subspace_id in candidate_subspace_ids:
        if subspace_id in archived_ids:
            return "archived_subspace_excluded"
    return None


def _why_selected_v2(
    *,
    component_scores: Mapping[str, float],
    final_score: float,
    project_scope: str | None,
    risk_level: str,
    subspace_matches: list[dict[str, str]],
    query_entity_ids: set[str],
) -> list[str]:
    reasons: list[str] = []
    for match in subspace_matches:
        subspace_id = _clean_text(match.get("subspace_id"))
        match_type = _clean_text(match.get("match_type"))
        if subspace_id and match_type:
            reasons.append(f"selected_subspace_{match_type}_match:{subspace_id}")
    if project_scope and component_scores.get("project_scope_score") == 1.0:
        reasons.append(f"project_scope_match:{project_scope}")
    if query_entity_ids and component_scores.get("entity_score", 0.0) > 0:
        reasons.append("entity_match")
    if component_scores.get("keyword_score", 0.0) > 0:
        reasons.append("keyword_overlap")
    if component_scores.get("semantic_score", 0.0) > 0:
        reasons.append("semantic_overlap")
    if component_scores.get("source_trust_score") == 1.0:
        reasons.append("trusted_provenance")
    if component_scores.get("governance_score") == 1.0:
        reasons.append("read_only_governance")
    if risk_level:
        reasons.append(f"risk_level:{risk_level}")
    reasons.append(f"final_score:{final_score:.4f}")
    return _dedupe_strings(reasons)


def _candidate_project_scope(candidate: Mapping[str, Any]) -> str:
    return _strip_scope_prefix_v2(
        _clean_text(candidate.get("project_id") or candidate.get("project_scope")),
        "project",
    )


def _candidate_agent_scope(candidate: Mapping[str, Any]) -> str:
    return _strip_scope_prefix_v2(
        _clean_text(candidate.get("agent_id") or candidate.get("agent_scope")),
        "agent",
    )


def _candidate_subspace_ids(candidate: Mapping[str, Any]) -> list[str]:
    values = []
    values.extend(_as_list(candidate.get("subspace_id")))
    values.extend(_as_list(candidate.get("subspace_ids")))
    return _dedupe_strings(_clean_text(value) for value in values if _clean_text(value))


def _candidate_risk_level(candidate: Mapping[str, Any]) -> str:
    return _clean_text(candidate.get("risk_level") or candidate.get("risk")).lower()


def _candidate_governance(candidate: Mapping[str, Any]) -> Any:
    governance = candidate.get("governance")
    policy = candidate.get("policy")
    if isinstance(governance, Mapping) and isinstance(policy, Mapping):
        merged = deepcopy(dict(policy))
        merged.update(deepcopy(dict(governance)))
        return merged
    if governance is not None:
        return governance
    return policy


def _risk_score(risk_level: str) -> float:
    return {
        "low": 1.0,
        "medium": 0.75,
        "high": 0.35,
        "critical": 0.15,
    }.get(risk_level, 0.5)


def _allowed_risk_levels_v2(value: Any) -> set[str]:
    if value is None:
        return set(DEFAULT_ALLOWED_RISK_LEVELS_V2)
    return {_clean_text(item).lower() for item in _as_list(value) if _clean_text(item)}


def _selection_limit(value: Any) -> int:
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return DEFAULT_LIMIT


def _subspace_project_scope_v2(subspace: Mapping[str, Any]) -> str:
    scope = subspace.get("scope")
    kind = _clean_text(subspace.get("subspace_kind"))
    if isinstance(scope, Mapping):
        for key in ("project_scope", "project_id"):
            value = _clean_text(scope.get(key))
            if value:
                return _strip_scope_prefix_v2(value, "project")
        if kind == "project":
            for key in ("scope_id", "id", "name"):
                value = _clean_text(scope.get(key))
                if value:
                    return _strip_scope_prefix_v2(value, "project")
    elif kind == "project":
        return _strip_scope_prefix_v2(_clean_text(scope), "project")
    return ""


def _subspace_agent_scope_v2(subspace: Mapping[str, Any]) -> str:
    scope = subspace.get("scope")
    kind = _clean_text(subspace.get("subspace_kind"))
    if isinstance(scope, Mapping):
        for key in ("agent_scope", "agent_id"):
            value = _clean_text(scope.get(key))
            if value:
                return _strip_scope_prefix_v2(value, "agent")
        if kind == "agent":
            for key in ("scope_id", "id", "name"):
                value = _clean_text(scope.get(key))
                if value:
                    return _strip_scope_prefix_v2(value, "agent")
    elif kind == "agent":
        return _strip_scope_prefix_v2(_clean_text(scope), "agent")
    return ""


def _mapping_of_lists(value: Any) -> dict[str, list[str]]:
    if not isinstance(value, Mapping):
        return {}
    return {
        _clean_text(key): [_clean_text(item) for item in _as_list(items) if _clean_text(item)]
        for key, items in value.items()
        if _clean_text(key)
    }


def _dedupe_matches(matches: Iterable[Mapping[str, str]]) -> list[dict[str, str]]:
    deduped: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for match in matches:
        subspace_id = _clean_text(match.get("subspace_id"))
        match_type = _clean_text(match.get("match_type"))
        key = (subspace_id, match_type)
        if subspace_id and match_type and key not in seen:
            seen.add(key)
            deduped.append({"subspace_id": subspace_id, "match_type": match_type})
    return deduped


def _dedupe_strings(values: Iterable[Any]) -> list[str]:
    deduped: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = _clean_text(value)
        if text and text not in seen:
            seen.add(text)
            deduped.append(text)
    return deduped


def _strip_scope_prefix_v2(value: str, prefix: str) -> str:
    prefix_text = f"{prefix}:"
    return value[len(prefix_text) :] if value.startswith(prefix_text) else value


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _as_mapping_copy(value: Any) -> dict[str, Any]:
    return deepcopy(dict(value)) if isinstance(value, Mapping) else {}


def _sort_reason_map_v2(value: Any) -> dict[str, list[str]]:
    if not isinstance(value, Mapping):
        return {}
    return {
        str(key): [str(reason) for reason in _as_list(value[key])]
        for key in sorted(value, key=lambda item: str(item))
    }


def _safe_policy_v2(policy: Any) -> dict[str, Any]:
    if not isinstance(policy, Mapping):
        return dict(FUSION_POLICY_V2)
    safe = dict(FUSION_POLICY_V2)
    for key, expected in FUSION_POLICY_V2.items():
        safe[key] = policy.get(key) if policy.get(key) is expected else expected
    return safe


def _tokens(text: str) -> set[str]:
    return {match.group(0).lower() for match in _TOKEN_RE.finditer(text or "")}


def _semantic_score(query_tokens: set[str], candidate_tokens: set[str]) -> float:
    if not query_tokens or not candidate_tokens:
        return 0.0
    overlap = len(query_tokens & candidate_tokens)
    return round(overlap / len(query_tokens | candidate_tokens), 4)


def _keyword_score(query: str, query_tokens: set[str], text: str, candidate_tokens: set[str]) -> float:
    if not query_tokens or not candidate_tokens:
        return 0.0
    exact_token_score = len(query_tokens & candidate_tokens) / len(query_tokens)
    normalized_query = " ".join(str(query).lower().split())
    normalized_text = " ".join(str(text).lower().split())
    phrase_score = 1.0 if normalized_query and normalized_query in normalized_text else 0.0
    return round((exact_token_score * 0.75) + (phrase_score * 0.25), 4)


def _entity_score(candidate_entity_ids: Any, query_entity_ids: set[str]) -> float:
    if not query_entity_ids:
        return 0.5
    candidate_set = {str(entity_id) for entity_id in _as_list(candidate_entity_ids) if str(entity_id)}
    if not candidate_set:
        return 0.0
    return round(len(candidate_set & query_entity_ids) / len(query_entity_ids), 4)


def _temporal_score(candidate: Mapping[str, Any], now: datetime) -> float:
    valid_from = _coerce_datetime(candidate.get("valid_from"))
    valid_until = _coerce_datetime(candidate.get("valid_until"))
    if valid_until and valid_until < now:
        return 0.05
    if valid_from and valid_from > now:
        return 0.2
    if valid_from or valid_until:
        return 1.0

    created_at = _coerce_datetime(candidate.get("created_at"))
    if not created_at:
        return 0.5
    age_days = max((now - created_at).total_seconds() / 86400, 0)
    if age_days <= 7:
        return 0.9
    if age_days <= 30:
        return 0.75
    if age_days <= 365:
        return 0.5
    return 0.25


def _project_scope_score(project_id: Any, project_scope: str | None) -> float:
    if not project_scope:
        return 0.5
    if project_id is None:
        return 0.25
    return 1.0 if str(project_id) == str(project_scope) else 0.0


def _source_trust_score(candidate: Mapping[str, Any]) -> float:
    if candidate.get("provenance"):
        return 1.0
    if candidate.get("source"):
        return 0.6
    return 0.25


def _governance_score(governance: Any) -> tuple[float, list[str]]:
    if governance is None:
        return 0.5, []
    if isinstance(governance, str):
        lowered = governance.lower()
        reasons = [marker for marker in _UNSAFE_TEXT_MARKERS if marker in lowered]
        if reasons:
            return 0.0, reasons
        if "read_only" in lowered or "proposal" in lowered or "governed" in lowered:
            return 1.0, []
        return 0.5, []
    if not isinstance(governance, Mapping):
        return 0.5, []

    reasons = [key for key in _UNSAFE_BOOL_KEYS if governance.get(key) is True]
    mode = str(governance.get("mode", "")).lower()
    if any(marker in mode for marker in ("write", "mutate", "modify")):
        reasons.append("mode")
    if reasons:
        return 0.0, reasons
    if governance.get("read_only") is True or governance.get("proposal_governed") is True:
        return 1.0, []
    return 0.5, []


def _coerce_datetime(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=UTC)
    if not value:
        return None
    text = str(value)
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return list(value)
    return [value]
