"""Governed memory proposal review gate for v2.10 proposal reports."""

from __future__ import annotations

import json
from typing import Any, Mapping


GOVERNED_MEMORY_PROPOSAL_REVIEW_GATE_VERSION = "2.11.0"

EXPECTED_PROPOSAL_VERSION = "2.10.0"

SENSITIVE_EXACT_KEYS = {
    "approval_phrase",
    "stdout",
    "stdout_tail",
    "raw_logs",
}
SENSITIVE_KEY_FRAGMENTS = (
    "token",
    "secret",
    "password",
    "credential",
    "api_key",
    "apikey",
)

LAYER_MAPPING = {
    "primary_layer": "星穹记忆",
    "supporting_layers": ["星辰记忆", "星域记忆", "星界记忆"],
    "direction": "星辰候选记忆提案 -> 星穹治理评审闸门",
}

EXPECTED_PROPOSAL_LAYER_MAPPING = {
    "primary_layer": "星辰记忆",
    "supporting_layers": ["星域记忆", "星穹记忆", "星界记忆"],
}

SAFETY_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "would_mutate_memory": False,
    "writes_files": False,
    "invokes_openclaw": False,
    "would_call_github_api": False,
    "would_merge_pr": False,
    "would_create_tag": False,
    "would_write_durable_memory": False,
    "would_mutate_memory_graph": False,
    "would_create_operation_ledger_entry": False,
    "would_create_approval_request": False,
    "authorization_granted": False,
    "review_gate_authorized": False,
    "approval_request_authorized": False,
    "memory_write_authorized": False,
    "openclaw_execution_authorized": False,
}

REQUIRED_PROPOSAL_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "would_mutate_memory": False,
    "writes_files": False,
    "invokes_openclaw": False,
    "would_call_github_api": False,
    "would_merge_pr": False,
    "would_create_tag": False,
    "would_write_durable_memory": False,
    "would_mutate_memory_graph": False,
    "would_create_operation_ledger_entry": False,
    "authorization_granted": False,
    "memory_write_authorized": False,
    "openclaw_execution_authorized": False,
}

REQUIRED_CANDIDATE_FIELDS = (
    "candidate_id",
    "memory_layer",
    "title",
    "summary",
    "evidence_basis",
    "scope",
    "risks",
    "required_review",
)


def build_governed_memory_proposal_review_gate(
    proposal_report: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a local read-only review gate report for a governed proposal report."""

    if not isinstance(proposal_report, Mapping):
        return _base_report(
            status="blocked",
            review_summary="Governed memory proposal review gate is blocked.",
            gate_checks=[
                _check("proposal_report_mapping", False),
            ],
            candidate_review_results=[],
            accepted_candidate_ids=[],
            blocked_candidate_ids=[],
            blocking_reasons=["proposal_report_must_be_mapping"],
            required_review_actions=["provide_v2_10_governed_memory_proposal_report"],
            sensitive_field_count=0,
        )

    sensitive_field_count = _count_sensitive_keys(proposal_report)
    gate_checks, global_blocking_reasons = _global_gate_checks(proposal_report)
    candidate_memories = proposal_report.get("candidate_memories")
    candidate_results = _candidate_review_results(candidate_memories)
    candidate_blocking_reasons = [
        reason
        for result in candidate_results
        for reason in result["blocking_reasons"]
    ]
    blocked_candidate_ids = [
        result["candidate_id"]
        for result in candidate_results
        if result["review_status"] == "blocked" and result["candidate_id"]
    ]
    all_candidates_accepted = bool(candidate_results) and all(
        result["review_status"] == "accepted_for_review" for result in candidate_results
    )
    status = "review_ready" if not global_blocking_reasons and all_candidates_accepted else "blocked"
    accepted_candidate_ids = [
        result["candidate_id"]
        for result in candidate_results
        if status == "review_ready" and result["review_status"] == "accepted_for_review"
    ]
    blocking_reasons = list(dict.fromkeys(global_blocking_reasons + candidate_blocking_reasons))

    return _base_report(
        status=status,
        review_summary=(
            "Governed proposal is structurally ready for future human-governed approval "
            "request preparation only."
            if status == "review_ready"
            else "Governed memory proposal review gate is blocked."
        ),
        gate_checks=gate_checks,
        candidate_review_results=candidate_results,
        accepted_candidate_ids=accepted_candidate_ids,
        blocked_candidate_ids=blocked_candidate_ids,
        blocking_reasons=blocking_reasons,
        required_review_actions=_required_review_actions(status, blocking_reasons),
        sensitive_field_count=sensitive_field_count,
    )


def governed_memory_proposal_review_gate_to_json(report: Mapping[str, Any]) -> str:
    """Serialize a governed memory proposal review gate report deterministically."""

    return json.dumps(dict(report), ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def _base_report(
    *,
    status: str,
    review_summary: str,
    gate_checks: list[dict[str, Any]],
    candidate_review_results: list[dict[str, Any]],
    accepted_candidate_ids: list[str],
    blocked_candidate_ids: list[str],
    blocking_reasons: list[str],
    required_review_actions: list[str],
    sensitive_field_count: int,
) -> dict[str, Any]:
    return {
        "version": GOVERNED_MEMORY_PROPOSAL_REVIEW_GATE_VERSION,
        "status": status,
        **SAFETY_FLAGS,
        "civilization_core_layer_mapping": dict(LAYER_MAPPING),
        "review_summary": review_summary,
        "gate_checks": gate_checks,
        "candidate_review_results": candidate_review_results,
        "accepted_candidate_ids": accepted_candidate_ids,
        "blocked_candidate_ids": blocked_candidate_ids,
        "scope_boundaries": [
            "Civilization Core is the total system; this gate is only a Subspace Memory System review checkpoint.",
            "Fifteen Memory Layers remain the highest memory coordinate system.",
            "Hermes, Codex CLI, OpenClaw, Terminal, and GitHub remain components, not the core.",
            "Review gate readiness is not authorization, approval, approval request creation, execution, or durable memory write permission.",
            "Human Operator remains final authority.",
        ],
        "risk_notes": [
            "Review-ready status must not be treated as authorization.",
            "No durable memory write, Memory Graph mutation, operation-ledger entry, approval request, or OpenClaw execution is authorized.",
            "Sensitive fields were omitted from review output when present in input.",
            "This gate does not claim Civilization Core completion.",
        ],
        "required_review_actions": required_review_actions,
        "blocking_reasons": blocking_reasons,
        "sensitive_field_count": sensitive_field_count,
        "sensitive_fields_omitted": sensitive_field_count > 0,
    }


def _global_gate_checks(proposal_report: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    blocking_reasons: list[str] = []

    _add_check(
        checks,
        blocking_reasons,
        "proposal_version",
        proposal_report.get("version") == EXPECTED_PROPOSAL_VERSION,
        "proposal_version_must_be_2_10_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "proposal_status",
        proposal_report.get("status") == "proposal_ready",
        "proposal_status_must_be_proposal_ready",
    )
    for key, expected in REQUIRED_PROPOSAL_FLAGS.items():
        _add_check(
            checks,
            blocking_reasons,
            f"proposal_flag_{key}",
            proposal_report.get(key) is expected,
            f"proposal_flag_{key}_must_be_{str(expected).lower()}",
        )

    mapping = proposal_report.get("civilization_core_layer_mapping")
    mapping_is_valid = isinstance(mapping, Mapping)
    _add_check(
        checks,
        blocking_reasons,
        "proposal_layer_mapping_present",
        mapping_is_valid,
        "proposal_layer_mapping_must_be_mapping",
    )
    if mapping_is_valid:
        _add_check(
            checks,
            blocking_reasons,
            "proposal_primary_layer",
            mapping.get("primary_layer") == EXPECTED_PROPOSAL_LAYER_MAPPING["primary_layer"],
            "proposal_primary_layer_must_be_star_memory",
        )
        supporting_layers = mapping.get("supporting_layers")
        _add_check(
            checks,
            blocking_reasons,
            "proposal_supporting_layers",
            isinstance(supporting_layers, list)
            and all(
                layer in supporting_layers
                for layer in EXPECTED_PROPOSAL_LAYER_MAPPING["supporting_layers"]
            ),
            "proposal_supporting_layers_must_include_required_layers",
        )

    candidate_memories = proposal_report.get("candidate_memories")
    _add_check(
        checks,
        blocking_reasons,
        "candidate_memories_non_empty_list",
        isinstance(candidate_memories, list) and bool(candidate_memories),
        "candidate_memories_must_be_non_empty_list",
    )
    return checks, blocking_reasons


def _candidate_review_results(candidate_memories: Any) -> list[dict[str, Any]]:
    if not isinstance(candidate_memories, list):
        return []
    return [_candidate_review_result(candidate, index) for index, candidate in enumerate(candidate_memories)]


def _candidate_review_result(candidate: Any, index: int) -> dict[str, Any]:
    candidate_id = _safe_candidate_id(candidate, index)
    checks: list[dict[str, Any]] = []
    blocking_reasons: list[str] = []

    if not isinstance(candidate, Mapping):
        return {
            "candidate_id": candidate_id,
            "review_status": "blocked",
            "checks": [_check("candidate_mapping", False)],
            "blocking_reasons": ["candidate_must_be_mapping"],
            "required_review_actions": ["replace_malformed_candidate_memory"],
        }

    for field in REQUIRED_CANDIDATE_FIELDS:
        _add_check(
            checks,
            blocking_reasons,
            f"candidate_{field}_present",
            field in candidate,
            f"candidate_{field}_missing",
        )

    _add_check(
        checks,
        blocking_reasons,
        "candidate_memory_layer",
        candidate.get("memory_layer") == "星辰记忆",
        "candidate_memory_layer_must_be_star_memory",
    )
    for field in ("candidate_id", "title", "summary", "evidence_basis", "scope", "risks", "required_review"):
        _add_check(
            checks,
            blocking_reasons,
            f"candidate_{field}_non_empty",
            _non_empty(candidate.get(field)),
            f"candidate_{field}_must_be_non_empty",
        )

    return {
        "candidate_id": candidate_id,
        "review_status": "blocked" if blocking_reasons else "accepted_for_review",
        "checks": checks,
        "blocking_reasons": blocking_reasons,
        "required_review_actions": _candidate_required_review_actions(blocking_reasons),
    }


def _candidate_required_review_actions(blocking_reasons: list[str]) -> list[str]:
    if not blocking_reasons:
        return ["human_operator_review_required_before_approval_request_preparation"]
    return [
        "repair_candidate_structure_before_review_gate_can_continue",
        "confirm_candidate_remains_read_only_and_non_authorizing",
    ]


def _required_review_actions(status: str, blocking_reasons: list[str]) -> list[str]:
    if status == "review_ready":
        return [
            "human_operator_review_required_before_any_approval_request_preparation",
            "confirm_review_ready_status_is_not_authorization",
            "confirm_no_memory_write_or_openclaw_execution_is_authorized",
        ]
    actions = [
        "repair_governed_memory_proposal_report_before_review_can_continue",
        "confirm_all_safety_flags_remain_non_authorizing",
        "provide_complete_structural_candidate_memory_fields",
    ]
    if blocking_reasons:
        actions.append("resolve_blocking_reasons_before_human_review_preparation")
    return actions


def _add_check(
    checks: list[dict[str, Any]],
    blocking_reasons: list[str],
    name: str,
    passed: bool,
    reason: str,
) -> None:
    checks.append(_check(name, passed))
    if not passed:
        blocking_reasons.append(reason)


def _check(name: str, passed: bool) -> dict[str, Any]:
    return {"check": name, "passed": passed}


def _safe_candidate_id(candidate: Any, index: int) -> str:
    if not isinstance(candidate, Mapping):
        return f"candidate_index_{index}"
    candidate_id = candidate.get("candidate_id")
    if isinstance(candidate_id, str) and candidate_id.strip() and not _contains_sensitive_text(candidate_id):
        return candidate_id.strip()
    return f"candidate_index_{index}"


def _non_empty(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip()) and not _contains_sensitive_text(value)
    if isinstance(value, Mapping):
        return bool(value)
    if isinstance(value, list):
        return bool(value)
    return value is not None


def _count_sensitive_keys(value: Any) -> int:
    if isinstance(value, Mapping):
        count = 0
        for key, inner in value.items():
            key_text = str(key).lower()
            if _is_sensitive_key(key_text):
                count += 1
            count += _count_sensitive_keys(inner)
        return count
    if isinstance(value, list):
        return sum(_count_sensitive_keys(item) for item in value)
    return 0


def _contains_sensitive_text(value: str) -> bool:
    return _is_sensitive_key(value.lower())


def _is_sensitive_key(key_text: str) -> bool:
    return key_text in SENSITIVE_EXACT_KEYS or any(
        fragment in key_text for fragment in SENSITIVE_KEY_FRAGMENTS
    )


__all__ = [
    "GOVERNED_MEMORY_PROPOSAL_REVIEW_GATE_VERSION",
    "build_governed_memory_proposal_review_gate",
    "governed_memory_proposal_review_gate_to_json",
]
