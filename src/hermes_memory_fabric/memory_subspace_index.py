from __future__ import annotations

import json
from collections import Counter
from copy import deepcopy
from typing import Any, Iterable, Mapping


MEMORY_SUBSPACE_INDEX_VERSION = "0.1"
MEMORY_SUBSPACE_REGISTRY_TYPE = "memory_subspace_registry"
DEFAULT_TIMESTAMP = "1970-01-01T00:00:00Z"
DEFAULT_ACTIVE_CONTEXT_BUDGET = 5

SUPPORTED_SUBSPACE_KINDS = (
    "project",
    "agent",
    "risk",
    "archive",
    "global",
    "custom",
)
SUPPORTED_LIFECYCLE_STATUSES = (
    "active",
    "planned",
    "deprecated",
    "archived",
)
SUPPORTED_RISK_LEVELS = (
    "low",
    "medium",
    "high",
    "critical",
)
DEFAULT_ALLOWED_RISK_LEVELS = ("low", "medium")
HIGH_RISK_LEVELS = {"high", "critical"}

MEMORY_SUBSPACE_INDEX_POLICY = {
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

REQUIRED_SUBSPACE_DESCRIPTOR_FIELDS = (
    "subspace_id",
    "subspace_kind",
    "scope",
    "owner",
    "access_policy",
    "risk_level",
    "lifecycle_status",
    "active_summary",
    "source_index",
    "fact_graph_ref",
    "memory_blocks_ref",
    "tags",
    "priority",
    "created_at",
    "updated_at",
    "last_compacted_at",
    "governance_status",
    "policy",
)
REQUIRED_POLICY_FIELDS = tuple(MEMORY_SUBSPACE_INDEX_POLICY)

_LIFECYCLE_SCORE = {
    "active": 30.0,
    "planned": 12.0,
    "deprecated": -15.0,
    "archived": -30.0,
}
_LIFECYCLE_SORT_RANK = {
    "active": 0,
    "planned": 1,
    "deprecated": 2,
    "archived": 3,
}
_RISK_SORT_RANK = {
    "low": 0,
    "medium": 1,
    "high": 2,
    "critical": 3,
}


def create_subspace_descriptor(
    *,
    subspace_id: str,
    subspace_kind: str,
    scope: Mapping[str, Any] | str,
    owner: str,
    access_policy: Mapping[str, Any] | str | None = None,
    risk_level: str = "low",
    lifecycle_status: str = "active",
    active_summary: str = "",
    source_index: Mapping[str, Any] | None = None,
    fact_graph_ref: Mapping[str, Any] | str | None = None,
    memory_blocks_ref: Mapping[str, Any] | str | None = None,
    tags: Iterable[str] | None = None,
    priority: int | float = 0,
    created_at: str | None = None,
    updated_at: str | None = None,
    last_compacted_at: str | None = None,
    governance_status: str = "governed",
    policy: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a deterministic read-only subspace descriptor."""
    kind = _clean_text(subspace_kind)
    created = _clean_text(created_at) or DEFAULT_TIMESTAMP
    descriptor = {
        "subspace_id": _clean_text(subspace_id),
        "subspace_kind": kind,
        "scope": _normalize_scope(scope, kind),
        "owner": _clean_text(owner),
        "access_policy": _normalize_access_policy(access_policy),
        "risk_level": _clean_text(risk_level),
        "lifecycle_status": _clean_text(lifecycle_status),
        "active_summary": _clean_text(active_summary),
        "source_index": deepcopy(dict(source_index or {})),
        "fact_graph_ref": _normalize_ref(fact_graph_ref),
        "memory_blocks_ref": _normalize_ref(memory_blocks_ref),
        "tags": _sorted_strings(tags or []),
        "priority": _coerce_priority(priority),
        "created_at": created,
        "updated_at": _clean_text(updated_at) or created,
        "last_compacted_at": _clean_text(last_compacted_at) if last_compacted_at is not None else None,
        "governance_status": _clean_text(governance_status),
        "policy": _merge_policy(policy),
    }
    return descriptor


def validate_subspace_descriptor(subspace: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the v0.1 subspace descriptor contract without side effects."""
    if not isinstance(subspace, Mapping):
        return {"valid": False, "errors": ["descriptor_must_be_mapping"]}

    errors: list[str] = []
    for field in REQUIRED_SUBSPACE_DESCRIPTOR_FIELDS:
        if field not in subspace:
            errors.append(f"missing_{field}")

    subspace_id = _clean_text(subspace.get("subspace_id"))
    if "subspace_id" in subspace and not subspace_id:
        errors.append("subspace_id_must_be_non_empty")

    kind = _clean_text(subspace.get("subspace_kind"))
    if "subspace_kind" in subspace and kind not in SUPPORTED_SUBSPACE_KINDS:
        errors.append(f"unsupported_subspace_kind:{kind}")

    risk_level = _clean_text(subspace.get("risk_level"))
    if "risk_level" in subspace and risk_level not in SUPPORTED_RISK_LEVELS:
        errors.append(f"unsupported_risk_level:{risk_level}")

    lifecycle_status = _clean_text(subspace.get("lifecycle_status"))
    if "lifecycle_status" in subspace and lifecycle_status not in SUPPORTED_LIFECYCLE_STATUSES:
        errors.append(f"unsupported_lifecycle_status:{lifecycle_status}")

    tags = subspace.get("tags")
    if "tags" in subspace and not isinstance(tags, (list, tuple)):
        errors.append("tags_must_be_list")

    if "priority" in subspace and not isinstance(subspace.get("priority"), (int, float)):
        errors.append("priority_must_be_number")

    policy = subspace.get("policy")
    if not isinstance(policy, Mapping):
        errors.append("policy_must_be_mapping")
    else:
        for key, expected in MEMORY_SUBSPACE_INDEX_POLICY.items():
            if key not in policy:
                errors.append(f"missing_policy_{key}")
            elif policy.get(key) is not expected:
                expected_text = "true" if expected is True else "false"
                errors.append(f"policy_{key}_must_be_{expected_text}")

    return {"valid": not errors, "errors": _dedupe(errors)}


def explain_subspace_descriptor(subspace: Mapping[str, Any]) -> dict[str, Any]:
    """Return a stable explanation for a single subspace descriptor."""
    descriptor = deepcopy(dict(subspace)) if isinstance(subspace, Mapping) else {}
    validity = validate_subspace_descriptor(descriptor)
    return {
        "subspace_id": descriptor.get("subspace_id"),
        "subspace_kind": descriptor.get("subspace_kind"),
        "scope": deepcopy(descriptor.get("scope")),
        "scope_key": _scope_key(descriptor),
        "owner": descriptor.get("owner"),
        "risk_level": descriptor.get("risk_level"),
        "lifecycle_status": descriptor.get("lifecycle_status"),
        "governance_status": descriptor.get("governance_status"),
        "tags": _sorted_strings(descriptor.get("tags", [])),
        "priority": descriptor.get("priority"),
        "read_only": _as_mapping(descriptor.get("policy")).get("read_only") is True,
        "validity": validity,
        "policy": _safe_policy_from(descriptor.get("policy")),
    }


def create_subspace_registry(subspaces: Iterable[Mapping[str, Any]] | None = None) -> dict[str, Any]:
    """Create a deterministic read-only subspace registry."""
    return {
        "registry_type": MEMORY_SUBSPACE_REGISTRY_TYPE,
        "version": MEMORY_SUBSPACE_INDEX_VERSION,
        "subspaces": _copy_subspaces(subspaces or []),
        "policy": dict(MEMORY_SUBSPACE_INDEX_POLICY),
    }


def validate_subspace_registry(registry: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a subspace registry and all contained descriptors."""
    if not isinstance(registry, Mapping):
        return {"valid": False, "errors": ["registry_must_be_mapping"]}

    errors: list[str] = []
    if registry.get("registry_type") != MEMORY_SUBSPACE_REGISTRY_TYPE:
        errors.append("registry_type_must_be_memory_subspace_registry")
    if registry.get("version") != MEMORY_SUBSPACE_INDEX_VERSION:
        errors.append("version_must_be_0.1")

    policy = registry.get("policy")
    if not isinstance(policy, Mapping):
        errors.append("policy_must_be_mapping")
    else:
        for key, expected in MEMORY_SUBSPACE_INDEX_POLICY.items():
            if policy.get(key) is not expected:
                expected_text = "true" if expected is True else "false"
                errors.append(f"policy_{key}_must_be_{expected_text}")

    raw_subspaces = registry.get("subspaces")
    if not isinstance(raw_subspaces, (list, tuple)):
        errors.append("subspaces_must_be_list")
        raw_subspaces = []

    seen: set[str] = set()
    for index, subspace in enumerate(raw_subspaces):
        validity = validate_subspace_descriptor(subspace)
        subspace_id = _clean_text(subspace.get("subspace_id")) if isinstance(subspace, Mapping) else ""
        label = subspace_id or f"index_{index}"
        for error in validity["errors"]:
            errors.append(f"subspace_{label}_{error}")
        if subspace_id:
            if subspace_id in seen:
                errors.append(f"duplicate_subspace_id:{subspace_id}")
            seen.add(subspace_id)

    return {"valid": not errors, "errors": _dedupe(errors)}


def add_subspace_to_registry(
    registry: Mapping[str, Any],
    subspace: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a new registry with one appended subspace; never mutate the input."""
    next_registry = deepcopy(dict(registry)) if isinstance(registry, Mapping) else create_subspace_registry()
    next_registry["registry_type"] = next_registry.get("registry_type", MEMORY_SUBSPACE_REGISTRY_TYPE)
    next_registry["version"] = next_registry.get("version", MEMORY_SUBSPACE_INDEX_VERSION)
    next_registry["policy"] = _merge_policy(next_registry.get("policy"))
    next_registry["subspaces"] = _copy_subspaces(next_registry.get("subspaces", []))
    next_registry["subspaces"].append(deepcopy(dict(subspace)))
    return next_registry


def resolve_subspace(registry: Mapping[str, Any], subspace_id: str) -> dict[str, Any] | None:
    """Resolve one descriptor by id and return a copy."""
    target = _clean_text(subspace_id)
    for subspace in _registry_subspaces(registry):
        if _clean_text(subspace.get("subspace_id")) == target:
            return deepcopy(subspace)
    return None


def select_subspaces_for_context(
    registry: Mapping[str, Any],
    context: Mapping[str, Any],
) -> dict[str, Any]:
    """Select relevant subspaces for a context without mutating registry state."""
    context_map = _as_mapping(context)
    project_scope = _clean_text(context_map.get("project_scope"))
    agent_scope = _clean_text(context_map.get("agent_scope"))
    include_archived = bool(context_map.get("include_archived", False))
    required_tags = set(_sorted_strings(context_map.get("required_tags", [])))
    allowed_risk_levels = _allowed_risk_levels(context_map.get("allowed_risk_levels"))
    budget = _active_context_budget(context_map.get("max_active_subspaces"))
    query_tokens = set(_sorted_strings(_tokenize(context_map.get("query", ""))))

    eligible: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    selection_reasons: dict[str, list[str]] = {}
    rejected_reasons: dict[str, list[str]] = {}

    for index, raw_subspace in enumerate(_registry_subspaces(registry)):
        subspace = deepcopy(raw_subspace)
        subspace_id = _subspace_id_for_output(subspace, index)
        validity = validate_subspace_descriptor(subspace)
        reasons: list[str] = []
        score = 0.0

        if not validity["valid"]:
            _reject(subspace, subspace_id, ["invalid_descriptor"], rejected, rejected_reasons)
            continue

        lifecycle_status = _clean_text(subspace.get("lifecycle_status"))
        risk_level = _clean_text(subspace.get("risk_level"))
        tags = set(_sorted_strings(subspace.get("tags", [])))
        project_match = _matches_project_scope(subspace, project_scope)
        agent_match = _matches_agent_scope(subspace, agent_scope)

        if lifecycle_status == "archived" and not include_archived:
            _reject(subspace, subspace_id, ["archived_excluded"], rejected, rejected_reasons)
            continue
        if risk_level in HIGH_RISK_LEVELS and risk_level not in allowed_risk_levels:
            _reject(subspace, subspace_id, [f"risk_level_not_allowed:{risk_level}"], rejected, rejected_reasons)
            continue
        missing_tags = sorted(required_tags - tags)
        if missing_tags:
            _reject(
                subspace,
                subspace_id,
                [f"missing_required_tags:{','.join(missing_tags)}"],
                rejected,
                rejected_reasons,
            )
            continue
        if project_scope and project_match is False:
            _reject(subspace, subspace_id, ["project_scope_mismatch"], rejected, rejected_reasons)
            continue
        if agent_scope and agent_match is False:
            _reject(subspace, subspace_id, ["agent_scope_mismatch"], rejected, rejected_reasons)
            continue

        if project_match is True:
            score += 100.0
            reasons.append("project_scope_exact_match")
        elif project_scope:
            reasons.append("project_scope_not_declared")

        if agent_match is True:
            score += 50.0
            reasons.append("agent_scope_exact_match")
        elif agent_scope:
            reasons.append("agent_scope_not_declared")

        lifecycle_score = _LIFECYCLE_SCORE.get(lifecycle_status, 0.0)
        score += lifecycle_score
        reasons.append(f"lifecycle:{lifecycle_status}")

        risk_score = {"low": 10.0, "medium": 5.0, "high": -8.0, "critical": -16.0}.get(risk_level, 0.0)
        score += risk_score
        reasons.append(f"risk_level:{risk_level}")

        if required_tags:
            score += len(required_tags) * 8.0
            reasons.append("required_tags_matched")

        tag_overlap = sorted(query_tokens & tags)
        if tag_overlap:
            score += len(tag_overlap) * 3.0
            reasons.append("query_tag_overlap:" + ",".join(tag_overlap))

        kind = _clean_text(subspace.get("subspace_kind"))
        if kind == "global":
            score += 3.0
            reasons.append("global_subspace")
        if kind == "archive":
            score -= 10.0
            reasons.append("archive_subspace")

        priority = _coerce_priority(subspace.get("priority", 0))
        score += priority
        reasons.append(f"priority:{_format_number(priority)}")

        eligible.append(
            {
                "subspace": subspace,
                "subspace_id": subspace_id,
                "score": round(score, 4),
                "priority": priority,
                "reasons": reasons,
            }
        )

    eligible.sort(key=_selection_sort_key)
    selected_items = eligible[:budget]
    overflow_items = eligible[budget:]

    selected_subspaces: list[dict[str, Any]] = []
    for item in selected_items:
        subspace = deepcopy(item["subspace"])
        selected_subspaces.append(subspace)
        selection_reasons[item["subspace_id"]] = list(item["reasons"]) + [f"score:{_format_number(item['score'])}"]

    for item in overflow_items:
        _reject(
            item["subspace"],
            item["subspace_id"],
            ["ranked_below_active_context_budget", f"score:{_format_number(item['score'])}"],
            rejected,
            rejected_reasons,
        )

    return {
        "selected_subspaces": selected_subspaces,
        "rejected_subspaces": rejected,
        "selection_reasons": _sort_reason_map(selection_reasons),
        "rejected_reasons": _sort_reason_map(rejected_reasons),
        "active_context_budget": {
            "max_active_subspaces": budget,
            "eligible_subspace_count": len(eligible),
            "selected_subspace_count": len(selected_subspaces),
            "rejected_subspace_count": len(rejected),
        },
        "policy": dict(MEMORY_SUBSPACE_INDEX_POLICY),
    }


def explain_subspace_selection(selection: Mapping[str, Any]) -> dict[str, Any]:
    """Return a deterministic explanation for a selection result."""
    selection_map = _as_mapping(selection)
    selected_ids = [_clean_text(item.get("subspace_id")) for item in _as_list(selection_map.get("selected_subspaces"))]
    rejected_ids = [_clean_text(item.get("subspace_id")) for item in _as_list(selection_map.get("rejected_subspaces"))]
    return {
        "selected_subspace_ids": [item for item in selected_ids if item],
        "rejected_subspace_ids": [item for item in rejected_ids if item],
        "selection_reasons": _sort_reason_map(selection_map.get("selection_reasons")),
        "rejected_reasons": _sort_reason_map(selection_map.get("rejected_reasons")),
        "active_context_budget": deepcopy(dict(selection_map.get("active_context_budget", {}))),
        "rules": [
            "Exact project scope matches outrank global and custom domains.",
            "Exact agent scope matches are preferred when an agent scope is provided.",
            "Archived subspaces are excluded unless include_archived is true.",
            "High and critical risk subspaces require explicit allowed_risk_levels.",
            "Required tags are hard filters.",
            "Selection is deterministic and read-only.",
        ],
        "policy": _safe_policy_from(selection_map.get("policy")),
    }


def summarize_subspace_registry(registry: Mapping[str, Any]) -> dict[str, Any]:
    """Summarize registry distribution by scope, lifecycle, risk, and governance."""
    subspaces = _registry_subspaces(registry)
    return {
        "total": len(subspaces),
        "by_scope": _count(_scope_key(subspace) for subspace in subspaces),
        "by_lifecycle_status": _count(_clean_text(subspace.get("lifecycle_status")) for subspace in subspaces),
        "by_risk_level": _count(_clean_text(subspace.get("risk_level")) for subspace in subspaces),
        "by_governance_status": _count(_clean_text(subspace.get("governance_status")) for subspace in subspaces),
        "validity": validate_subspace_registry(registry),
        "policy": dict(MEMORY_SUBSPACE_INDEX_POLICY),
    }


def _normalize_scope(scope: Mapping[str, Any] | str, kind: str) -> dict[str, Any]:
    if isinstance(scope, Mapping):
        return deepcopy(dict(scope))
    scope_text = _clean_text(scope)
    if kind == "project":
        return {"project_scope": scope_text}
    if kind == "agent":
        return {"agent_scope": scope_text}
    if kind == "risk":
        return {"risk_scope": scope_text}
    if kind == "archive":
        return {"archive_scope": scope_text}
    if kind == "global":
        return {"scope_type": "global", "scope_id": scope_text or "global"}
    return {"custom_scope": scope_text}


def _normalize_access_policy(access_policy: Mapping[str, Any] | str | None) -> dict[str, Any] | str:
    if isinstance(access_policy, Mapping):
        return deepcopy(dict(access_policy))
    if access_policy is not None:
        return _clean_text(access_policy)
    return {
        "read": "allowed",
        "write": "forbidden",
        "proposal_required_for_writes": True,
    }


def _normalize_ref(value: Mapping[str, Any] | str | None) -> dict[str, Any] | str:
    if isinstance(value, Mapping):
        return deepcopy(dict(value))
    if value is None:
        return {}
    return _clean_text(value)


def _merge_policy(policy: Mapping[str, Any] | None) -> dict[str, Any]:
    merged = dict(MEMORY_SUBSPACE_INDEX_POLICY)
    if isinstance(policy, Mapping):
        for key, value in policy.items():
            if key not in MEMORY_SUBSPACE_INDEX_POLICY:
                merged[str(key)] = deepcopy(value)
    return merged


def _safe_policy_from(policy: Any) -> dict[str, Any]:
    if isinstance(policy, Mapping):
        return deepcopy(dict(policy))
    return dict(MEMORY_SUBSPACE_INDEX_POLICY)


def _copy_subspaces(subspaces: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    if isinstance(subspaces, (str, bytes, bytearray, Mapping)):
        return []
    copied: list[dict[str, Any]] = []
    for subspace in subspaces:
        if isinstance(subspace, Mapping):
            copied.append(deepcopy(dict(subspace)))
    return copied


def _registry_subspaces(registry: Mapping[str, Any]) -> list[dict[str, Any]]:
    if not isinstance(registry, Mapping):
        return []
    return _copy_subspaces(registry.get("subspaces", []))


def _matches_project_scope(subspace: Mapping[str, Any], project_scope: str) -> bool | None:
    declared = _project_scope(subspace)
    if not project_scope:
        return None
    if declared:
        return declared == project_scope
    if _clean_text(subspace.get("subspace_kind")) == "project":
        return False
    return None


def _matches_agent_scope(subspace: Mapping[str, Any], agent_scope: str) -> bool | None:
    declared = _agent_scope(subspace)
    if not agent_scope:
        return None
    if declared:
        return declared == agent_scope
    if _clean_text(subspace.get("subspace_kind")) == "agent":
        return False
    return None


def _project_scope(subspace: Mapping[str, Any]) -> str:
    kind = _clean_text(subspace.get("subspace_kind"))
    scope = subspace.get("scope")
    if isinstance(scope, Mapping):
        for key in ("project_scope", "project_id"):
            value = _clean_text(scope.get(key))
            if value:
                return _strip_scope_prefix(value, "project")
        if kind == "project":
            for key in ("scope_id", "id", "name"):
                value = _clean_text(scope.get(key))
                if value:
                    return _strip_scope_prefix(value, "project")
    elif kind == "project":
        return _strip_scope_prefix(_clean_text(scope), "project")
    return ""


def _agent_scope(subspace: Mapping[str, Any]) -> str:
    kind = _clean_text(subspace.get("subspace_kind"))
    scope = subspace.get("scope")
    if isinstance(scope, Mapping):
        for key in ("agent_scope", "agent_id"):
            value = _clean_text(scope.get(key))
            if value:
                return _strip_scope_prefix(value, "agent")
        if kind == "agent":
            for key in ("scope_id", "id", "name"):
                value = _clean_text(scope.get(key))
                if value:
                    return _strip_scope_prefix(value, "agent")
    elif kind == "agent":
        return _strip_scope_prefix(_clean_text(scope), "agent")
    return ""


def _scope_key(subspace: Mapping[str, Any]) -> str:
    kind = _clean_text(subspace.get("subspace_kind")) or "unknown"
    scope = subspace.get("scope")
    project_scope = _project_scope(subspace)
    agent_scope = _agent_scope(subspace)
    if project_scope:
        return f"project:{project_scope}"
    if agent_scope:
        return f"agent:{agent_scope}"
    if kind == "global":
        return "global"
    if isinstance(scope, Mapping):
        for key in ("risk_scope", "archive_scope", "custom_scope", "scope_id", "id", "name"):
            value = _clean_text(scope.get(key))
            if value:
                return f"{kind}:{_strip_scope_prefix(value, kind)}"
        encoded = json.dumps(scope, sort_keys=True, separators=(",", ":"), default=str)
        return f"{kind}:{encoded}"
    scope_text = _clean_text(scope)
    if not scope_text:
        return kind
    return f"{kind}:{_strip_scope_prefix(scope_text, kind)}"


def _selection_sort_key(item: Mapping[str, Any]) -> tuple[float, float, int, int, str]:
    subspace = item["subspace"]
    lifecycle = _clean_text(subspace.get("lifecycle_status"))
    risk = _clean_text(subspace.get("risk_level"))
    return (
        -float(item["score"]),
        -float(item["priority"]),
        _LIFECYCLE_SORT_RANK.get(lifecycle, 99),
        _RISK_SORT_RANK.get(risk, 99),
        _clean_text(item["subspace_id"]),
    )


def _reject(
    subspace: Mapping[str, Any],
    subspace_id: str,
    reasons: list[str],
    rejected: list[dict[str, Any]],
    rejected_reasons: dict[str, list[str]],
) -> None:
    rejected.append(deepcopy(dict(subspace)))
    rejected_reasons[subspace_id] = list(reasons)


def _allowed_risk_levels(value: Any) -> set[str]:
    if value is None:
        return set(DEFAULT_ALLOWED_RISK_LEVELS)
    return {item for item in _sorted_strings(value) if item}


def _active_context_budget(value: Any) -> int:
    if value is None:
        return DEFAULT_ACTIVE_CONTEXT_BUDGET
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return DEFAULT_ACTIVE_CONTEXT_BUDGET


def _as_mapping(value: Any) -> dict[str, Any]:
    return deepcopy(dict(value)) if isinstance(value, Mapping) else {}


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, (list, tuple)):
        return deepcopy(list(value))
    return []


def _sorted_strings(value: Iterable[Any]) -> list[str]:
    if isinstance(value, str):
        items = [value]
    else:
        try:
            items = list(value)
        except TypeError:
            items = []
    return sorted({_clean_text(item) for item in items if _clean_text(item)})


def _tokenize(value: Any) -> list[str]:
    return str(value or "").replace(":", " ").replace("/", " ").replace(",", " ").split()


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _strip_scope_prefix(value: str, prefix: str) -> str:
    text = _clean_text(value)
    prefix_text = f"{prefix}:"
    if text.startswith(prefix_text):
        return text[len(prefix_text) :]
    return text


def _coerce_priority(value: Any) -> int | float:
    if isinstance(value, bool):
        return 0
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return value
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return 0
    return int(numeric) if numeric.is_integer() else numeric


def _format_number(value: Any) -> str:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return "0"
    if numeric.is_integer():
        return str(int(numeric))
    return f"{numeric:.4f}".rstrip("0").rstrip(".")


def _subspace_id_for_output(subspace: Mapping[str, Any], index: int) -> str:
    subspace_id = _clean_text(subspace.get("subspace_id"))
    return subspace_id or f"index_{index}"


def _sort_reason_map(value: Any) -> dict[str, list[str]]:
    if not isinstance(value, Mapping):
        return {}
    return {
        str(key): [str(reason) for reason in _as_list(value[key])]
        for key in sorted(value, key=lambda item: str(item))
    }


def _count(values: Iterable[str]) -> dict[str, int]:
    return dict(sorted(Counter(value or "unknown" for value in values).items()))


def _dedupe(errors: Iterable[str]) -> list[str]:
    deduped: list[str] = []
    seen: set[str] = set()
    for error in errors:
        if error not in seen:
            seen.add(error)
            deduped.append(error)
    return deduped


__all__ = [
    "MEMORY_SUBSPACE_INDEX_POLICY",
    "REQUIRED_SUBSPACE_DESCRIPTOR_FIELDS",
    "REQUIRED_POLICY_FIELDS",
    "SUPPORTED_SUBSPACE_KINDS",
    "create_subspace_descriptor",
    "validate_subspace_descriptor",
    "explain_subspace_descriptor",
    "create_subspace_registry",
    "validate_subspace_registry",
    "add_subspace_to_registry",
    "resolve_subspace",
    "select_subspaces_for_context",
    "explain_subspace_selection",
    "summarize_subspace_registry",
]
