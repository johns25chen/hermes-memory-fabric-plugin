"""Governed approval request dry-run envelope for v2.12 preparation reports."""

from __future__ import annotations

import json
from typing import Any, Mapping


GOVERNED_APPROVAL_REQUEST_DRY_RUN_ENVELOPE_VERSION = "2.13.0"

EXPECTED_PREPARATION_VERSION = "2.12.0"

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
    "direction": "星穹 approval request 准备材料 -> 星穹 dry-run envelope",
}

SAFETY_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "dry_run_only": True,
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
    "would_execute_approval_request": False,
    "authorization_granted": False,
    "envelope_authorized": False,
    "approval_request_created": False,
    "approval_request_submitted": False,
    "approval_request_authorized": False,
    "approval_granted": False,
    "memory_write_authorized": False,
    "openclaw_execution_authorized": False,
}

REQUIRED_PREPARATION_FLAGS = {
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

GOVERNANCE_REQUIREMENTS = [
    "Envelope readiness is not authorization.",
    "Envelope readiness is not approval.",
    "Envelope readiness is not a real approval request.",
    "Envelope readiness is not approval request submission.",
    "Envelope readiness is not durable memory write permission.",
    "Envelope readiness is not Memory Graph mutation permission.",
    "Envelope readiness is not operation-ledger creation.",
    "Envelope readiness is not OpenClaw execution permission.",
    "Human Operator remains final authority.",
]


def build_governed_approval_request_dry_run_envelope(
    preparation_report: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a sanitized local-only dry-run envelope report."""

    if not isinstance(preparation_report, Mapping):
        return _base_report(
            status="blocked",
            envelope_checks=[_check("preparation_report_mapping", False)],
            candidate_ids_in_envelope=[],
            blocked_candidate_ids=[],
            blocking_reasons=["preparation_report_must_be_mapping"],
            sensitive_field_count=0,
        )

    sensitive_field_count = _count_sensitive_keys(preparation_report)
    envelope_checks, blocking_reasons = _envelope_checks(preparation_report)
    candidate_ids = _safe_candidate_ids(preparation_report.get("candidate_ids_for_human_review"))
    blocked_candidate_ids = _safe_candidate_ids(preparation_report.get("blocked_candidate_ids"))
    status = "envelope_ready" if not blocking_reasons else "blocked"

    return _base_report(
        status=status,
        envelope_checks=envelope_checks,
        candidate_ids_in_envelope=candidate_ids if status == "envelope_ready" else [],
        blocked_candidate_ids=blocked_candidate_ids,
        blocking_reasons=blocking_reasons,
        sensitive_field_count=sensitive_field_count,
    )


def governed_approval_request_dry_run_envelope_to_json(report: Mapping[str, Any]) -> str:
    """Serialize a governed approval request dry-run envelope deterministically."""

    return json.dumps(dict(report), ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def _base_report(
    *,
    status: str,
    envelope_checks: list[dict[str, Any]],
    candidate_ids_in_envelope: list[str],
    blocked_candidate_ids: list[str],
    blocking_reasons: list[str],
    sensitive_field_count: int,
) -> dict[str, Any]:
    return {
        "version": GOVERNED_APPROVAL_REQUEST_DRY_RUN_ENVELOPE_VERSION,
        "status": status,
        **SAFETY_FLAGS,
        "civilization_core_layer_mapping": dict(LAYER_MAPPING),
        "envelope_summary": (
            "Governed approval request dry-run envelope is prepared for a future human operator only."
            if status == "envelope_ready"
            else "Governed approval request dry-run envelope preparation is blocked."
        ),
        "envelope_checks": envelope_checks,
        "dry_run_envelope": _dry_run_envelope(status, candidate_ids_in_envelope),
        "candidate_ids_in_envelope": candidate_ids_in_envelope,
        "blocked_candidate_ids": blocked_candidate_ids,
        "scope_boundaries": [
            "Civilization Core is the total system; this dry-run envelope is only a Subspace Memory System governance checkpoint.",
            "Fifteen Memory Layers remain the highest memory coordinate system.",
            "Hermes, Codex CLI, OpenClaw, Terminal, and GitHub remain components, not the core.",
            "Envelope readiness is not authorization, approval, real approval request creation, submission, execution, or durable memory write permission.",
            "Human Operator remains final authority.",
        ],
        "risk_notes": [
            "Envelope-ready status must not be treated as authorization.",
            "No real approval request is created, submitted, approved, authorized, or executed.",
            "No durable memory write, Memory Graph mutation, operation-ledger entry, GitHub API call, merge, tag creation, or OpenClaw execution is authorized.",
            "Sensitive fields were omitted from dry-run envelope output when present in input.",
            "This dry-run envelope step does not claim Civilization Core completion.",
        ],
        "required_human_actions": _required_human_actions(status, blocking_reasons),
        "blocking_reasons": blocking_reasons,
        "sensitive_field_count": sensitive_field_count,
        "sensitive_fields_omitted": sensitive_field_count > 0,
    }


def _dry_run_envelope(status: str, candidate_ids: list[str]) -> dict[str, Any]:
    if status != "envelope_ready":
        return {
            "envelope_status": "not_prepared",
            "is_real_approval_request": False,
            "is_submittable": False,
            "candidate_ids": [],
            "source_preparation_version": EXPECTED_PREPARATION_VERSION,
            "envelope_type": "approval_request_dry_run",
            "governance_requirements": list(GOVERNANCE_REQUIREMENTS),
            "required_human_actions": _required_human_actions("blocked", []),
            "non_authorization_notice": "Blocked dry-run envelope is not authorization, approval, submission, or real approval request material.",
        }
    return {
        "envelope_status": "dry_run_prepared_for_human_operator_only",
        "is_real_approval_request": False,
        "is_submittable": False,
        "candidate_ids": list(candidate_ids),
        "source_preparation_version": EXPECTED_PREPARATION_VERSION,
        "envelope_type": "approval_request_dry_run",
        "governance_requirements": list(GOVERNANCE_REQUIREMENTS),
        "required_human_actions": _required_human_actions(status, []),
        "non_authorization_notice": "Envelope-ready material is structural only and grants no approval, submission, execution, or memory-write authority.",
    }


def _envelope_checks(
    preparation_report: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    blocking_reasons: list[str] = []

    _add_check(
        checks,
        blocking_reasons,
        "preparation_version",
        preparation_report.get("version") == EXPECTED_PREPARATION_VERSION,
        "preparation_version_must_be_2_12_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "preparation_status",
        preparation_report.get("status") == "preparation_ready",
        "preparation_status_must_be_preparation_ready",
    )
    for key, expected in REQUIRED_PREPARATION_FLAGS.items():
        _add_check(
            checks,
            blocking_reasons,
            f"preparation_flag_{key}",
            preparation_report.get(key) is expected,
            f"preparation_flag_{key}_must_be_{str(expected).lower()}",
        )

    mapping = preparation_report.get("civilization_core_layer_mapping")
    mapping_is_valid = isinstance(mapping, Mapping)
    _add_check(
        checks,
        blocking_reasons,
        "preparation_layer_mapping_present",
        mapping_is_valid,
        "preparation_layer_mapping_must_be_mapping",
    )
    if mapping_is_valid:
        _add_check(
            checks,
            blocking_reasons,
            "preparation_primary_layer",
            mapping.get("primary_layer") == LAYER_MAPPING["primary_layer"],
            "preparation_primary_layer_must_be_star_dome_memory",
        )
        supporting_layers = mapping.get("supporting_layers")
        _add_check(
            checks,
            blocking_reasons,
            "preparation_supporting_layers",
            isinstance(supporting_layers, list)
            and all(layer in supporting_layers for layer in LAYER_MAPPING["supporting_layers"]),
            "preparation_supporting_layers_must_include_required_layers",
        )

    candidate_ids = preparation_report.get("candidate_ids_for_human_review")
    candidate_ids_are_valid = (
        isinstance(candidate_ids, list)
        and bool(candidate_ids)
        and all(_safe_identifier(item) for item in candidate_ids)
    )
    _add_check(
        checks,
        blocking_reasons,
        "candidate_ids_for_human_review_non_empty_safe_list",
        candidate_ids_are_valid,
        "candidate_ids_for_human_review_must_be_non_empty_safe_string_list",
    )

    blocked_candidate_ids = preparation_report.get("blocked_candidate_ids")
    _add_check(
        checks,
        blocking_reasons,
        "blocked_candidate_ids_empty_list",
        blocked_candidate_ids == [],
        "blocked_candidate_ids_must_be_empty",
    )

    draft = preparation_report.get("approval_request_draft_material")
    draft_is_mapping = isinstance(draft, Mapping)
    _add_check(
        checks,
        blocking_reasons,
        "approval_request_draft_material_present",
        draft_is_mapping,
        "approval_request_draft_material_must_be_mapping",
    )
    if draft_is_mapping:
        _add_check(
            checks,
            blocking_reasons,
            "approval_request_draft_material_status",
            draft.get("draft_status") == "prepared_for_human_operator_only",
            "approval_request_draft_material_status_must_be_prepared_for_human_operator_only",
        )
        _add_check(
            checks,
            blocking_reasons,
            "approval_request_draft_material_not_real",
            draft.get("is_real_approval_request") is False,
            "approval_request_draft_material_must_not_be_real_approval_request",
        )
        _add_check(
            checks,
            blocking_reasons,
            "approval_request_draft_material_not_submittable",
            draft.get("is_submittable") is not True,
            "approval_request_draft_material_must_not_be_submittable",
        )

    return checks, list(dict.fromkeys(blocking_reasons))


def _required_human_actions(status: str, blocking_reasons: list[str]) -> list[str]:
    if status == "envelope_ready":
        return [
            "human_operator_must_review_dry_run_envelope_before_any_real_approval_request",
            "human_operator_must_confirm_envelope_ready_is_not_authorization",
            "human_operator_must_use_separate_governed_process_for_any_real_approval_request_submission",
        ]
    actions = [
        "repair_v2_12_preparation_report_before_dry_run_envelope_can_continue",
        "confirm_all_safety_flags_remain_non_authorizing",
        "provide_non_empty_candidate_ids_for_human_review_and_empty_blocked_candidate_ids",
        "ensure_draft_material_is_structural_and_not_a_real_approval_request",
    ]
    if blocking_reasons:
        actions.append("resolve_blocking_reasons_before_human_approval_request_dry_run_envelope")
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
    "GOVERNED_APPROVAL_REQUEST_DRY_RUN_ENVELOPE_VERSION",
    "build_governed_approval_request_dry_run_envelope",
    "governed_approval_request_dry_run_envelope_to_json",
]
