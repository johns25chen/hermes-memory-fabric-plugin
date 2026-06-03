"""Governed approval request preparation for v2.11 review gate reports."""

from __future__ import annotations

import json
from typing import Any, Mapping


GOVERNED_APPROVAL_REQUEST_PREPARATION_VERSION = "2.12.0"

EXPECTED_REVIEW_GATE_VERSION = "2.11.0"

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
    "direction": "星穹治理评审闸门 -> 受治理 approval request 准备",
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
    "would_submit_approval_request": False,
    "authorization_granted": False,
    "preparation_authorized": False,
    "approval_request_created": False,
    "approval_request_authorized": False,
    "approval_granted": False,
    "memory_write_authorized": False,
    "openclaw_execution_authorized": False,
}

REQUIRED_REVIEW_GATE_FLAGS = {
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

GOVERNANCE_REQUIREMENTS = [
    "Preparation readiness is not authorization.",
    "Preparation readiness is not approval.",
    "Preparation readiness is not a real approval request.",
    "Preparation readiness is not durable memory write permission.",
    "Preparation readiness is not Memory Graph mutation permission.",
    "Preparation readiness is not operation-ledger creation.",
    "Preparation readiness is not OpenClaw execution permission.",
    "Human Operator remains final authority.",
]


def build_governed_approval_request_preparation(
    review_gate_report: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a sanitized local-only approval request preparation report."""

    if not isinstance(review_gate_report, Mapping):
        return _base_report(
            status="blocked",
            preparation_checks=[_check("review_gate_report_mapping", False)],
            candidate_ids_for_human_review=[],
            blocked_candidate_ids=[],
            blocking_reasons=["review_gate_report_must_be_mapping"],
            sensitive_field_count=0,
        )

    sensitive_field_count = _count_sensitive_keys(review_gate_report)
    preparation_checks, blocking_reasons = _preparation_checks(review_gate_report)
    accepted_candidate_ids = _safe_candidate_ids(review_gate_report.get("accepted_candidate_ids"))
    raw_blocked_candidate_ids = review_gate_report.get("blocked_candidate_ids")
    blocked_candidate_ids = _safe_candidate_ids(raw_blocked_candidate_ids)
    status = "preparation_ready" if not blocking_reasons else "blocked"

    return _base_report(
        status=status,
        preparation_checks=preparation_checks,
        candidate_ids_for_human_review=accepted_candidate_ids if status == "preparation_ready" else [],
        blocked_candidate_ids=blocked_candidate_ids,
        blocking_reasons=blocking_reasons,
        sensitive_field_count=sensitive_field_count,
    )


def governed_approval_request_preparation_to_json(report: Mapping[str, Any]) -> str:
    """Serialize a governed approval request preparation report deterministically."""

    return json.dumps(dict(report), ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def _base_report(
    *,
    status: str,
    preparation_checks: list[dict[str, Any]],
    candidate_ids_for_human_review: list[str],
    blocked_candidate_ids: list[str],
    blocking_reasons: list[str],
    sensitive_field_count: int,
) -> dict[str, Any]:
    return {
        "version": GOVERNED_APPROVAL_REQUEST_PREPARATION_VERSION,
        "status": status,
        **SAFETY_FLAGS,
        "civilization_core_layer_mapping": dict(LAYER_MAPPING),
        "preparation_summary": (
            "Governed approval request material is prepared for a future human operator only."
            if status == "preparation_ready"
            else "Governed approval request preparation is blocked."
        ),
        "preparation_checks": preparation_checks,
        "approval_request_draft_material": _approval_request_draft_material(
            status,
            candidate_ids_for_human_review,
        ),
        "candidate_ids_for_human_review": candidate_ids_for_human_review,
        "blocked_candidate_ids": blocked_candidate_ids,
        "scope_boundaries": [
            "Civilization Core is the total system; this preparation step is only a Subspace Memory System governance checkpoint.",
            "Fifteen Memory Layers remain the highest memory coordinate system.",
            "Hermes, Codex CLI, OpenClaw, Terminal, and GitHub remain components, not the core.",
            "Preparation readiness is not authorization, approval, approval request creation, execution, or durable memory write permission.",
            "Human Operator remains final authority.",
        ],
        "risk_notes": [
            "Preparation-ready status must not be treated as authorization.",
            "No real approval request is created or submitted.",
            "No durable memory write, Memory Graph mutation, operation-ledger entry, or OpenClaw execution is authorized.",
            "Sensitive fields were omitted from preparation output when present in input.",
            "This preparation step does not claim Civilization Core completion.",
        ],
        "required_human_actions": _required_human_actions(status, blocking_reasons),
        "blocking_reasons": blocking_reasons,
        "sensitive_field_count": sensitive_field_count,
        "sensitive_fields_omitted": sensitive_field_count > 0,
    }


def _approval_request_draft_material(status: str, candidate_ids: list[str]) -> dict[str, Any]:
    if status != "preparation_ready":
        return {
            "draft_status": "not_prepared",
            "is_real_approval_request": False,
            "candidate_ids": [],
            "source_review_gate_version": EXPECTED_REVIEW_GATE_VERSION,
            "governance_requirements": list(GOVERNANCE_REQUIREMENTS),
            "required_human_actions": _required_human_actions("blocked", []),
            "non_authorization_notice": "Blocked preparation is not authorization, approval, or real approval request material.",
        }
    return {
        "draft_status": "prepared_for_human_operator_only",
        "is_real_approval_request": False,
        "candidate_ids": list(candidate_ids),
        "source_review_gate_version": EXPECTED_REVIEW_GATE_VERSION,
        "governance_requirements": list(GOVERNANCE_REQUIREMENTS),
        "required_human_actions": _required_human_actions(status, []),
        "non_authorization_notice": "Preparation-ready material is structural only and grants no approval or execution authority.",
    }


def _preparation_checks(review_gate_report: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    blocking_reasons: list[str] = []

    _add_check(
        checks,
        blocking_reasons,
        "review_gate_version",
        review_gate_report.get("version") == EXPECTED_REVIEW_GATE_VERSION,
        "review_gate_version_must_be_2_11_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "review_gate_status",
        review_gate_report.get("status") == "review_ready",
        "review_gate_status_must_be_review_ready",
    )
    for key, expected in REQUIRED_REVIEW_GATE_FLAGS.items():
        _add_check(
            checks,
            blocking_reasons,
            f"review_gate_flag_{key}",
            review_gate_report.get(key) is expected,
            f"review_gate_flag_{key}_must_be_{str(expected).lower()}",
        )

    mapping = review_gate_report.get("civilization_core_layer_mapping")
    mapping_is_valid = isinstance(mapping, Mapping)
    _add_check(
        checks,
        blocking_reasons,
        "review_gate_layer_mapping_present",
        mapping_is_valid,
        "review_gate_layer_mapping_must_be_mapping",
    )
    if mapping_is_valid:
        _add_check(
            checks,
            blocking_reasons,
            "review_gate_primary_layer",
            mapping.get("primary_layer") == LAYER_MAPPING["primary_layer"],
            "review_gate_primary_layer_must_be_star_dome_memory",
        )
        supporting_layers = mapping.get("supporting_layers")
        _add_check(
            checks,
            blocking_reasons,
            "review_gate_supporting_layers",
            isinstance(supporting_layers, list)
            and all(layer in supporting_layers for layer in LAYER_MAPPING["supporting_layers"]),
            "review_gate_supporting_layers_must_include_required_layers",
        )

    accepted_candidate_ids = review_gate_report.get("accepted_candidate_ids")
    accepted_ids_are_valid = (
        isinstance(accepted_candidate_ids, list)
        and bool(accepted_candidate_ids)
        and all(_safe_identifier(item) for item in accepted_candidate_ids)
    )
    _add_check(
        checks,
        blocking_reasons,
        "accepted_candidate_ids_non_empty_safe_list",
        accepted_ids_are_valid,
        "accepted_candidate_ids_must_be_non_empty_safe_string_list",
    )

    blocked_candidate_ids = review_gate_report.get("blocked_candidate_ids")
    _add_check(
        checks,
        blocking_reasons,
        "blocked_candidate_ids_empty_list",
        blocked_candidate_ids == [],
        "blocked_candidate_ids_must_be_empty",
    )
    return checks, list(dict.fromkeys(blocking_reasons))


def _required_human_actions(status: str, blocking_reasons: list[str]) -> list[str]:
    if status == "preparation_ready":
        return [
            "human_operator_must_review_candidate_ids_before_any_real_approval_request",
            "human_operator_must_confirm_preparation_is_not_authorization",
            "human_operator_must_use_separate_governed_process_for_any_real_approval_request",
        ]
    actions = [
        "repair_v2_11_review_gate_report_before_preparation_can_continue",
        "confirm_all_safety_flags_remain_non_authorizing",
        "provide_non_empty_accepted_candidate_ids_and_empty_blocked_candidate_ids",
    ]
    if blocking_reasons:
        actions.append("resolve_blocking_reasons_before_human_approval_request_preparation")
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


def _safe_candidate_ids(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    safe_ids = []
    for item in value:
        safe = _safe_identifier(item)
        if safe:
            safe_ids.append(safe)
    return safe_ids


def _safe_identifier(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    if not stripped or _contains_sensitive_text(stripped):
        return None
    return stripped


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
    "GOVERNED_APPROVAL_REQUEST_PREPARATION_VERSION",
    "build_governed_approval_request_preparation",
    "governed_approval_request_preparation_to_json",
]
