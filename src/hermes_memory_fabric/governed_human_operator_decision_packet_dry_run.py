"""Governed Human Operator decision packet dry-run from v2.14 validation reports."""

from __future__ import annotations

import json
from typing import Any, Mapping


GOVERNED_HUMAN_OPERATOR_DECISION_PACKET_DRY_RUN_VERSION = "2.15.0"

EXPECTED_VALIDATION_VERSION = "2.14.0"
EXPECTED_ENVELOPE_VERSION = "2.13.0"
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
    "direction": "星穹 dry-run envelope validation gate -> Human Operator decision packet dry-run",
}

SAFETY_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "dry_run_only": True,
    "decision_packet_only": True,
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
    "would_record_human_decision": False,
    "would_grant_approval": False,
    "authorization_granted": False,
    "decision_packet_authorized": False,
    "human_decision_recorded": False,
    "approval_request_created": False,
    "approval_request_submitted": False,
    "approval_request_authorized": False,
    "approval_granted": False,
    "memory_write_authorized": False,
    "openclaw_execution_authorized": False,
}

REQUIRED_VALIDATION_FLAGS = {
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

DECISION_OPTIONS = [
    "request_changes",
    "reject",
    "prepare_separate_real_approval_process",
]

GOVERNANCE_REQUIREMENTS = [
    "Decision packet readiness is not authorization.",
    "Decision packet readiness is not approval.",
    "Decision packet readiness is not a real human decision.",
    "Decision packet readiness is not a real approval request.",
    "Decision packet readiness is not approval request submission.",
    "Decision packet readiness is not approval request execution.",
    "Decision packet readiness is not durable memory write permission.",
    "Decision packet readiness is not Memory Graph mutation permission.",
    "Decision packet readiness is not operation-ledger creation.",
    "Decision packet readiness is not OpenClaw execution permission.",
    "Human Operator remains final authority.",
]


def build_governed_human_operator_decision_packet_dry_run(
    validation_report: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a sanitized local-only decision packet dry-run report."""

    if not isinstance(validation_report, Mapping):
        return _base_report(
            status="blocked",
            decision_packet_checks=[_check("validation_report_mapping", False)],
            candidate_ids=[],
            blocked_candidate_ids=[],
            blocking_reasons=["validation_report_must_be_mapping"],
            sensitive_field_count=0,
            validation_report=None,
        )

    sensitive_field_count = _count_sensitive_keys(validation_report)
    decision_packet_checks, blocking_reasons = _decision_packet_checks(validation_report)
    candidate_ids = _safe_candidate_ids(validation_report.get("candidate_ids_validated"))
    blocked_candidate_ids = _safe_candidate_ids(validation_report.get("blocked_candidate_ids"))
    status = "decision_packet_ready" if not blocking_reasons else "blocked"

    return _base_report(
        status=status,
        decision_packet_checks=decision_packet_checks,
        candidate_ids=candidate_ids if status == "decision_packet_ready" else [],
        blocked_candidate_ids=blocked_candidate_ids,
        blocking_reasons=blocking_reasons,
        sensitive_field_count=sensitive_field_count,
        validation_report=validation_report,
    )


def governed_human_operator_decision_packet_dry_run_to_json(
    report: Mapping[str, Any],
) -> str:
    """Serialize a governed Human Operator decision packet dry-run deterministically."""

    return json.dumps(dict(report), ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def _base_report(
    *,
    status: str,
    decision_packet_checks: list[dict[str, Any]],
    candidate_ids: list[str],
    blocked_candidate_ids: list[str],
    blocking_reasons: list[str],
    sensitive_field_count: int,
    validation_report: Mapping[str, Any] | None,
) -> dict[str, Any]:
    return {
        "version": GOVERNED_HUMAN_OPERATOR_DECISION_PACKET_DRY_RUN_VERSION,
        "status": status,
        **SAFETY_FLAGS,
        "civilization_core_layer_mapping": dict(LAYER_MAPPING),
        "decision_packet_summary": (
            "Governed Human Operator decision packet dry-run is prepared for future review only."
            if status == "decision_packet_ready"
            else "Governed Human Operator decision packet dry-run is blocked."
        ),
        "decision_packet_checks": decision_packet_checks,
        "human_operator_decision_packet": _decision_packet(
            status,
            candidate_ids,
            validation_report,
        ),
        "candidate_ids_for_decision_review": candidate_ids,
        "blocked_candidate_ids": blocked_candidate_ids,
        "scope_boundaries": [
            "Civilization Core is the total system; this decision packet dry-run is only a Subspace Memory System governance checkpoint.",
            "Fifteen Memory Layers remain the highest memory coordinate system.",
            "Hermes, Codex CLI, OpenClaw, Terminal, and GitHub remain components, not the core.",
            "Decision packet readiness is not authorization, approval, real human decision recording, real approval request creation, submission, execution, or durable memory write permission.",
            "Human Operator remains final authority.",
        ],
        "risk_notes": [
            "Decision packet readiness must not be treated as authorization.",
            "No selected decision, approval grant, real approval request, submission, execution, or human decision record is produced.",
            "No durable memory write, Memory Graph mutation, operation-ledger entry, GitHub API call, merge, tag creation, or OpenClaw execution is authorized.",
            "Sensitive fields were omitted from decision packet output when present in input.",
            "This decision packet dry-run does not claim Civilization Core completion.",
        ],
        "required_human_actions": _required_human_actions(status, blocking_reasons),
        "blocking_reasons": blocking_reasons,
        "sensitive_field_count": sensitive_field_count,
        "sensitive_fields_omitted": sensitive_field_count > 0,
    }


def _decision_packet(
    status: str,
    candidate_ids: list[str],
    validation_report: Mapping[str, Any] | None,
) -> dict[str, Any]:
    if status != "decision_packet_ready" or validation_report is None:
        return {
            "packet_status": "blocked_not_prepared_for_review",
            "is_real_human_decision": False,
            "is_approval": False,
            "is_submittable": False,
            "is_executable": False,
            "candidate_ids": [],
            "source_validation_version": EXPECTED_VALIDATION_VERSION,
            "source_envelope_version": EXPECTED_ENVELOPE_VERSION,
            "source_preparation_version": EXPECTED_PREPARATION_VERSION,
            "packet_type": "human_operator_decision_packet_dry_run",
            "decision_options": [],
            "governance_requirements": list(GOVERNANCE_REQUIREMENTS),
            "required_human_actions": _required_human_actions("blocked", []),
            "non_authorization_notice": "Blocked decision packet dry-run is not decision material, authorization, approval, submission, execution, or memory-write permission.",
        }

    summary = validation_report.get("validated_dry_run_envelope_summary")
    source_envelope_version = (
        summary.get("source_envelope_version") if isinstance(summary, Mapping) else None
    )
    source_preparation_version = (
        summary.get("source_preparation_version") if isinstance(summary, Mapping) else None
    )
    return {
        "packet_status": "prepared_for_human_operator_review_only",
        "is_real_human_decision": False,
        "is_approval": False,
        "is_submittable": False,
        "is_executable": False,
        "candidate_ids": list(candidate_ids),
        "source_validation_version": EXPECTED_VALIDATION_VERSION,
        "source_envelope_version": source_envelope_version,
        "source_preparation_version": source_preparation_version,
        "packet_type": "human_operator_decision_packet_dry_run",
        "decision_options": list(DECISION_OPTIONS),
        "governance_requirements": list(GOVERNANCE_REQUIREMENTS),
        "required_human_actions": _required_human_actions(status, []),
        "non_authorization_notice": "Decision packet readiness is structural only and grants no human decision record, approval, request creation, submission, execution, or memory-write authority.",
    }


def _decision_packet_checks(
    validation_report: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    blocking_reasons: list[str] = []

    _add_check(
        checks,
        blocking_reasons,
        "validation_report_version",
        validation_report.get("version") == EXPECTED_VALIDATION_VERSION,
        "validation_report_version_must_be_2_14_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "validation_report_status",
        validation_report.get("status") == "validation_ready",
        "validation_report_status_must_be_validation_ready",
    )
    for key, expected in REQUIRED_VALIDATION_FLAGS.items():
        _add_check(
            checks,
            blocking_reasons,
            f"validation_flag_{key}",
            validation_report.get(key) is expected,
            f"validation_flag_{key}_must_be_{str(expected).lower()}",
        )

    mapping = validation_report.get("civilization_core_layer_mapping")
    mapping_is_valid = isinstance(mapping, Mapping)
    _add_check(
        checks,
        blocking_reasons,
        "validation_layer_mapping_present",
        mapping_is_valid,
        "validation_layer_mapping_must_be_mapping",
    )
    if mapping_is_valid:
        _add_check(
            checks,
            blocking_reasons,
            "validation_primary_layer",
            mapping.get("primary_layer") == LAYER_MAPPING["primary_layer"],
            "validation_primary_layer_must_be_star_dome_memory",
        )
        supporting_layers = mapping.get("supporting_layers")
        _add_check(
            checks,
            blocking_reasons,
            "validation_supporting_layers",
            isinstance(supporting_layers, list)
            and all(layer in supporting_layers for layer in LAYER_MAPPING["supporting_layers"]),
            "validation_supporting_layers_must_include_required_layers",
        )

    candidate_ids = validation_report.get("candidate_ids_validated")
    candidate_ids_are_valid = (
        isinstance(candidate_ids, list)
        and bool(candidate_ids)
        and all(_safe_identifier(item) for item in candidate_ids)
    )
    _add_check(
        checks,
        blocking_reasons,
        "candidate_ids_validated_non_empty_safe_list",
        candidate_ids_are_valid,
        "candidate_ids_validated_must_be_non_empty_safe_string_list",
    )

    _add_check(
        checks,
        blocking_reasons,
        "blocked_candidate_ids_empty_list",
        validation_report.get("blocked_candidate_ids") == [],
        "blocked_candidate_ids_must_be_empty",
    )

    summary = validation_report.get("validated_dry_run_envelope_summary")
    summary_is_mapping = isinstance(summary, Mapping)
    _add_check(
        checks,
        blocking_reasons,
        "validated_dry_run_envelope_summary_present",
        summary_is_mapping,
        "validated_dry_run_envelope_summary_must_be_mapping",
    )
    if summary_is_mapping:
        _add_check(
            checks,
            blocking_reasons,
            "validated_summary_status",
            summary.get("validation_status")
            == "dry_run_envelope_validated_for_human_review_only",
            "validated_summary_status_must_be_human_review_only",
        )
        _add_check(
            checks,
            blocking_reasons,
            "validated_summary_not_real",
            summary.get("is_real_approval_request") is False,
            "validated_summary_must_not_be_real_approval_request",
        )
        _add_check(
            checks,
            blocking_reasons,
            "validated_summary_not_submittable",
            summary.get("is_submittable") is False,
            "validated_summary_must_not_be_submittable",
        )
        _add_check(
            checks,
            blocking_reasons,
            "validated_summary_not_executable",
            summary.get("is_executable") is False,
            "validated_summary_must_not_be_executable",
        )
        _add_check(
            checks,
            blocking_reasons,
            "validated_summary_envelope_type",
            summary.get("envelope_type") == "approval_request_dry_run",
            "validated_summary_envelope_type_must_be_approval_request_dry_run",
        )
        _add_check(
            checks,
            blocking_reasons,
            "validated_summary_source_envelope_version",
            summary.get("source_envelope_version") == EXPECTED_ENVELOPE_VERSION,
            "validated_summary_source_envelope_version_must_be_2_13_0",
        )
        _add_check(
            checks,
            blocking_reasons,
            "validated_summary_source_preparation_version",
            summary.get("source_preparation_version") == EXPECTED_PREPARATION_VERSION,
            "validated_summary_source_preparation_version_must_be_2_12_0",
        )

    return checks, list(dict.fromkeys(blocking_reasons))


def _required_human_actions(status: str, blocking_reasons: list[str]) -> list[str]:
    if status == "decision_packet_ready":
        return [
            "human_operator_must_review_decision_packet_dry_run_before_any_real_process",
            "human_operator_must_confirm_decision_packet_ready_is_not_authorization",
            "human_operator_must_use_separate_governed_process_for_any_real_decision_approval_submission_or_execution",
        ]
    actions = [
        "repair_v2_14_validation_report_before_decision_packet_dry_run_can_continue",
        "confirm_all_safety_flags_remain_non_authorizing",
        "provide_non_empty_candidate_ids_validated_and_empty_blocked_candidate_ids",
        "ensure_validated_summary_is_structural_and_not_real_submittable_or_executable",
    ]
    if blocking_reasons:
        actions.append("resolve_blocking_reasons_before_decision_packet_dry_run")
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
    "GOVERNED_HUMAN_OPERATOR_DECISION_PACKET_DRY_RUN_VERSION",
    "build_governed_human_operator_decision_packet_dry_run",
    "governed_human_operator_decision_packet_dry_run_to_json",
]
