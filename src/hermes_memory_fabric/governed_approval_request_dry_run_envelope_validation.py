"""Governed validation gate for v2.13 approval request dry-run envelopes."""

from __future__ import annotations

import json
from typing import Any, Mapping


GOVERNED_APPROVAL_REQUEST_DRY_RUN_ENVELOPE_VALIDATION_VERSION = "2.14.0"

EXPECTED_ENVELOPE_REPORT_VERSION = "2.13.0"
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
    "direction": "星穹 dry-run envelope -> 星穹 dry-run envelope validation gate",
}

SAFETY_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "validation_only": True,
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
    "validation_authorized": False,
    "envelope_authorized": False,
    "approval_request_created": False,
    "approval_request_submitted": False,
    "approval_request_authorized": False,
    "approval_granted": False,
    "memory_write_authorized": False,
    "openclaw_execution_authorized": False,
}

REQUIRED_ENVELOPE_FLAGS = {
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

GOVERNANCE_REQUIREMENTS = [
    "Validation readiness is not authorization.",
    "Validation readiness is not approval.",
    "Validation readiness is not a real approval request.",
    "Validation readiness is not approval request submission.",
    "Validation readiness is not approval request execution.",
    "Validation readiness is not durable memory write permission.",
    "Validation readiness is not Memory Graph mutation permission.",
    "Validation readiness is not operation-ledger creation.",
    "Validation readiness is not OpenClaw execution permission.",
    "Human Operator remains final authority.",
]


def build_governed_approval_request_dry_run_envelope_validation(
    envelope_report: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a sanitized local-only validation report for a v2.13 dry-run envelope."""

    if not isinstance(envelope_report, Mapping):
        return _base_report(
            status="blocked",
            validation_checks=[_check("envelope_report_mapping", False)],
            candidate_ids_validated=[],
            blocked_candidate_ids=[],
            blocking_reasons=["envelope_report_must_be_mapping"],
            sensitive_field_count=0,
            envelope_report=None,
        )

    sensitive_field_count = _count_sensitive_keys(envelope_report)
    validation_checks, blocking_reasons = _validation_checks(envelope_report)
    candidate_ids = _safe_candidate_ids(envelope_report.get("candidate_ids_in_envelope"))
    blocked_candidate_ids = _safe_candidate_ids(envelope_report.get("blocked_candidate_ids"))
    status = "validation_ready" if not blocking_reasons else "blocked"

    return _base_report(
        status=status,
        validation_checks=validation_checks,
        candidate_ids_validated=candidate_ids if status == "validation_ready" else [],
        blocked_candidate_ids=blocked_candidate_ids,
        blocking_reasons=blocking_reasons,
        sensitive_field_count=sensitive_field_count,
        envelope_report=envelope_report,
    )


def governed_approval_request_dry_run_envelope_validation_to_json(
    report: Mapping[str, Any],
) -> str:
    """Serialize a governed dry-run envelope validation report deterministically."""

    return json.dumps(dict(report), ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def _base_report(
    *,
    status: str,
    validation_checks: list[dict[str, Any]],
    candidate_ids_validated: list[str],
    blocked_candidate_ids: list[str],
    blocking_reasons: list[str],
    sensitive_field_count: int,
    envelope_report: Mapping[str, Any] | None,
) -> dict[str, Any]:
    return {
        "version": GOVERNED_APPROVAL_REQUEST_DRY_RUN_ENVELOPE_VALIDATION_VERSION,
        "status": status,
        **SAFETY_FLAGS,
        "civilization_core_layer_mapping": dict(LAYER_MAPPING),
        "validation_summary": (
            "Governed dry-run envelope is structurally valid for future human review only."
            if status == "validation_ready"
            else "Governed dry-run envelope validation is blocked."
        ),
        "validation_checks": validation_checks,
        "validated_dry_run_envelope_summary": _validated_summary(
            status,
            candidate_ids_validated,
            envelope_report,
        ),
        "candidate_ids_validated": candidate_ids_validated,
        "blocked_candidate_ids": blocked_candidate_ids,
        "scope_boundaries": [
            "Civilization Core is the total system; this validation gate is only a Subspace Memory System governance checkpoint.",
            "Fifteen Memory Layers remain the highest memory coordinate system.",
            "Hermes, Codex CLI, OpenClaw, Terminal, and GitHub remain components, not the core.",
            "Validation readiness is not authorization, approval, real approval request creation, submission, execution, or durable memory write permission.",
            "Human Operator remains final authority.",
        ],
        "risk_notes": [
            "Validation-ready status must not be treated as authorization.",
            "No real approval request is created, submitted, approved, authorized, or executed.",
            "No durable memory write, Memory Graph mutation, operation-ledger entry, GitHub API call, merge, tag creation, or OpenClaw execution is authorized.",
            "Sensitive fields were omitted from validation output when present in input.",
            "This validation gate does not claim Civilization Core completion.",
        ],
        "required_human_actions": _required_human_actions(status, blocking_reasons),
        "blocking_reasons": blocking_reasons,
        "sensitive_field_count": sensitive_field_count,
        "sensitive_fields_omitted": sensitive_field_count > 0,
    }


def _validated_summary(
    status: str,
    candidate_ids: list[str],
    envelope_report: Mapping[str, Any] | None,
) -> dict[str, Any]:
    if status != "validation_ready" or envelope_report is None:
        return {
            "validation_status": "dry_run_envelope_validation_blocked",
            "is_real_approval_request": False,
            "is_submittable": False,
            "is_executable": False,
            "candidate_ids": [],
            "source_envelope_version": EXPECTED_ENVELOPE_REPORT_VERSION,
            "source_preparation_version": EXPECTED_PREPARATION_VERSION,
            "envelope_type": "approval_request_dry_run",
            "governance_requirements": list(GOVERNANCE_REQUIREMENTS),
            "required_human_actions": _required_human_actions("blocked", []),
            "non_authorization_notice": "Blocked validation is not authorization, approval, submission, execution, or real approval request material.",
        }

    envelope = envelope_report.get("dry_run_envelope")
    source_preparation_version = (
        envelope.get("source_preparation_version") if isinstance(envelope, Mapping) else None
    )
    return {
        "validation_status": "dry_run_envelope_validated_for_human_review_only",
        "is_real_approval_request": False,
        "is_submittable": False,
        "is_executable": False,
        "candidate_ids": list(candidate_ids),
        "source_envelope_version": EXPECTED_ENVELOPE_REPORT_VERSION,
        "source_preparation_version": source_preparation_version,
        "envelope_type": "approval_request_dry_run",
        "governance_requirements": list(GOVERNANCE_REQUIREMENTS),
        "required_human_actions": _required_human_actions(status, []),
        "non_authorization_notice": "Validation-ready material is structural only and grants no approval, submission, execution, or memory-write authority.",
    }


def _validation_checks(
    envelope_report: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    blocking_reasons: list[str] = []

    _add_check(
        checks,
        blocking_reasons,
        "envelope_report_version",
        envelope_report.get("version") == EXPECTED_ENVELOPE_REPORT_VERSION,
        "envelope_report_version_must_be_2_13_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "envelope_report_status",
        envelope_report.get("status") == "envelope_ready",
        "envelope_report_status_must_be_envelope_ready",
    )
    for key, expected in REQUIRED_ENVELOPE_FLAGS.items():
        _add_check(
            checks,
            blocking_reasons,
            f"envelope_flag_{key}",
            envelope_report.get(key) is expected,
            f"envelope_flag_{key}_must_be_{str(expected).lower()}",
        )

    mapping = envelope_report.get("civilization_core_layer_mapping")
    mapping_is_valid = isinstance(mapping, Mapping)
    _add_check(
        checks,
        blocking_reasons,
        "envelope_layer_mapping_present",
        mapping_is_valid,
        "envelope_layer_mapping_must_be_mapping",
    )
    if mapping_is_valid:
        _add_check(
            checks,
            blocking_reasons,
            "envelope_primary_layer",
            mapping.get("primary_layer") == LAYER_MAPPING["primary_layer"],
            "envelope_primary_layer_must_be_star_dome_memory",
        )
        supporting_layers = mapping.get("supporting_layers")
        _add_check(
            checks,
            blocking_reasons,
            "envelope_supporting_layers",
            isinstance(supporting_layers, list)
            and all(layer in supporting_layers for layer in LAYER_MAPPING["supporting_layers"]),
            "envelope_supporting_layers_must_include_required_layers",
        )

    candidate_ids = envelope_report.get("candidate_ids_in_envelope")
    candidate_ids_are_valid = (
        isinstance(candidate_ids, list)
        and bool(candidate_ids)
        and all(_safe_identifier(item) for item in candidate_ids)
    )
    _add_check(
        checks,
        blocking_reasons,
        "candidate_ids_in_envelope_non_empty_safe_list",
        candidate_ids_are_valid,
        "candidate_ids_in_envelope_must_be_non_empty_safe_string_list",
    )

    blocked_candidate_ids = envelope_report.get("blocked_candidate_ids")
    _add_check(
        checks,
        blocking_reasons,
        "blocked_candidate_ids_empty_list",
        blocked_candidate_ids == [],
        "blocked_candidate_ids_must_be_empty",
    )

    envelope = envelope_report.get("dry_run_envelope")
    envelope_is_mapping = isinstance(envelope, Mapping)
    _add_check(
        checks,
        blocking_reasons,
        "dry_run_envelope_present",
        envelope_is_mapping,
        "dry_run_envelope_must_be_mapping",
    )
    if envelope_is_mapping:
        _add_check(
            checks,
            blocking_reasons,
            "dry_run_envelope_status",
            envelope.get("envelope_status") == "dry_run_prepared_for_human_operator_only",
            "dry_run_envelope_status_must_be_prepared_for_human_operator_only",
        )
        _add_check(
            checks,
            blocking_reasons,
            "dry_run_envelope_not_real",
            envelope.get("is_real_approval_request") is False,
            "dry_run_envelope_must_not_be_real_approval_request",
        )
        _add_check(
            checks,
            blocking_reasons,
            "dry_run_envelope_not_submittable",
            envelope.get("is_submittable") is False,
            "dry_run_envelope_must_not_be_submittable",
        )
        _add_check(
            checks,
            blocking_reasons,
            "dry_run_envelope_not_executable",
            envelope.get("is_executable") is not True,
            "dry_run_envelope_must_not_be_executable",
        )
        _add_check(
            checks,
            blocking_reasons,
            "dry_run_envelope_type",
            envelope.get("envelope_type") == "approval_request_dry_run",
            "dry_run_envelope_type_must_be_approval_request_dry_run",
        )
        _add_check(
            checks,
            blocking_reasons,
            "dry_run_envelope_source_preparation_version",
            envelope.get("source_preparation_version") == EXPECTED_PREPARATION_VERSION,
            "dry_run_envelope_source_preparation_version_must_be_2_12_0",
        )

    return checks, list(dict.fromkeys(blocking_reasons))


def _required_human_actions(status: str, blocking_reasons: list[str]) -> list[str]:
    if status == "validation_ready":
        return [
            "human_operator_must_review_validated_dry_run_envelope_before_any_real_approval_request",
            "human_operator_must_confirm_validation_ready_is_not_authorization",
            "human_operator_must_use_separate_governed_process_for_any_real_approval_request_submission_or_execution",
        ]
    actions = [
        "repair_v2_13_dry_run_envelope_report_before_validation_can_continue",
        "confirm_all_safety_flags_remain_non_authorizing",
        "provide_non_empty_candidate_ids_in_envelope_and_empty_blocked_candidate_ids",
        "ensure_dry_run_envelope_is_structural_and_not_real_submittable_or_executable",
    ]
    if blocking_reasons:
        actions.append("resolve_blocking_reasons_before_dry_run_envelope_validation")
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
    "GOVERNED_APPROVAL_REQUEST_DRY_RUN_ENVELOPE_VALIDATION_VERSION",
    "build_governed_approval_request_dry_run_envelope_validation",
    "governed_approval_request_dry_run_envelope_validation_to_json",
]
