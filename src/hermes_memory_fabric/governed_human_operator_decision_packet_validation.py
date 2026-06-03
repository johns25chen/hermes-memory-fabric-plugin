"""Governed Human Operator decision packet validation gate for v2.15 reports."""

from __future__ import annotations

import json
from typing import Any, Mapping


GOVERNED_HUMAN_OPERATOR_DECISION_PACKET_VALIDATION_VERSION = "2.16.0"

EXPECTED_PACKET_REPORT_VERSION = "2.15.0"
EXPECTED_SOURCE_VALIDATION_VERSION = "2.14.0"
EXPECTED_SOURCE_ENVELOPE_VERSION = "2.13.0"
EXPECTED_SOURCE_PREPARATION_VERSION = "2.12.0"

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
    "direction": (
        "Human Operator decision packet dry-run -> "
        "Human Operator decision packet validation gate"
    ),
}

SAFETY_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "dry_run_only": True,
    "validation_only": True,
    "decision_packet_validation_only": True,
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
    "validation_authorized": False,
    "decision_packet_authorized": False,
    "human_decision_recorded": False,
    "approval_request_created": False,
    "approval_request_submitted": False,
    "approval_request_authorized": False,
    "approval_granted": False,
    "memory_write_authorized": False,
    "openclaw_execution_authorized": False,
}

REQUIRED_PACKET_REPORT_FLAGS = {
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

OPTIONAL_UNSAFE_FALSE_FLAGS = (
    "validation_authorized",
    "approval_request_authorized",
    "memory_write_authorized",
    "openclaw_execution_authorized",
)

DECISION_OPTIONS = [
    "request_changes",
    "reject",
    "prepare_separate_real_approval_process",
]

GOVERNANCE_REQUIREMENTS = [
    "Decision packet validation readiness is not authorization.",
    "Decision packet validation readiness is not approval.",
    "Decision packet validation readiness is not a real human decision.",
    "Decision packet validation readiness is not a real approval request.",
    "Decision packet validation readiness is not approval request submission.",
    "Decision packet validation readiness is not approval request execution.",
    "Decision packet validation readiness is not durable memory write permission.",
    "Decision packet validation readiness is not Memory Graph mutation permission.",
    "Decision packet validation readiness is not operation-ledger creation.",
    "Decision packet validation readiness is not OpenClaw execution permission.",
    "Human Operator remains final authority.",
]


def build_governed_human_operator_decision_packet_validation(
    packet_report: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a sanitized local-only validation report for a v2.15 packet dry-run."""

    if not isinstance(packet_report, Mapping):
        return _base_report(
            status="blocked",
            validation_checks=[_check("packet_report_mapping", False)],
            candidate_ids=[],
            blocked_candidate_ids=[],
            blocking_reasons=["packet_report_must_be_mapping"],
            sensitive_field_count=0,
            packet_report=None,
        )

    sensitive_field_count = _count_sensitive_keys(packet_report)
    validation_checks, blocking_reasons = _validation_checks(packet_report)
    candidate_ids = _safe_candidate_ids(packet_report.get("candidate_ids_for_decision_review"))
    blocked_candidate_ids = _safe_candidate_ids(packet_report.get("blocked_candidate_ids"))
    status = "decision_packet_validation_ready" if not blocking_reasons else "blocked"

    return _base_report(
        status=status,
        validation_checks=validation_checks,
        candidate_ids=(
            candidate_ids if status == "decision_packet_validation_ready" else []
        ),
        blocked_candidate_ids=blocked_candidate_ids,
        blocking_reasons=blocking_reasons,
        sensitive_field_count=sensitive_field_count,
        packet_report=packet_report,
    )


def governed_human_operator_decision_packet_validation_to_json(
    report: Mapping[str, Any],
) -> str:
    """Serialize a governed Human Operator decision packet validation deterministically."""

    return json.dumps(dict(report), ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def _base_report(
    *,
    status: str,
    validation_checks: list[dict[str, Any]],
    candidate_ids: list[str],
    blocked_candidate_ids: list[str],
    blocking_reasons: list[str],
    sensitive_field_count: int,
    packet_report: Mapping[str, Any] | None,
) -> dict[str, Any]:
    return {
        "version": GOVERNED_HUMAN_OPERATOR_DECISION_PACKET_VALIDATION_VERSION,
        "status": status,
        **SAFETY_FLAGS,
        "civilization_core_layer_mapping": dict(LAYER_MAPPING),
        "validation_summary": (
            "Governed Human Operator decision packet dry-run is structurally valid for future Human Operator review only."
            if status == "decision_packet_validation_ready"
            else "Governed Human Operator decision packet validation is blocked."
        ),
        "validation_checks": validation_checks,
        "validated_human_operator_decision_packet_summary": _validated_summary(
            status,
            candidate_ids,
            packet_report,
        ),
        "candidate_ids_validated_for_decision_review": candidate_ids,
        "blocked_candidate_ids": blocked_candidate_ids,
        "scope_boundaries": [
            "Civilization Core is the total system; this validation gate is only a Subspace Memory System governance checkpoint.",
            "Fifteen Memory Layers remain the highest memory coordinate system.",
            "Hermes, Codex CLI, OpenClaw, Terminal, and GitHub remain components, not the core.",
            "Decision packet validation readiness is structural only and grants no authorization, approval, human decision record, approval request, submission, execution, or durable memory write permission.",
            "Human Operator remains final authority.",
        ],
        "risk_notes": [
            "Decision packet validation readiness must not be treated as authorization.",
            "No selected decision, approval grant, real approval request, submission, execution, or human decision record is produced.",
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
    packet_report: Mapping[str, Any] | None,
) -> dict[str, Any]:
    if status != "decision_packet_validation_ready" or packet_report is None:
        return {
            "validation_status": "blocked_not_validated_for_review",
            "is_real_human_decision": False,
            "is_approval": False,
            "is_submittable": False,
            "is_executable": False,
            "candidate_ids": [],
            "source_packet_version": EXPECTED_PACKET_REPORT_VERSION,
            "source_validation_version": EXPECTED_SOURCE_VALIDATION_VERSION,
            "source_envelope_version": EXPECTED_SOURCE_ENVELOPE_VERSION,
            "source_preparation_version": EXPECTED_SOURCE_PREPARATION_VERSION,
            "packet_type": "human_operator_decision_packet_dry_run",
            "governance_requirements": list(GOVERNANCE_REQUIREMENTS),
            "required_human_actions": _required_human_actions("blocked", []),
            "non_authorization_notice": "Blocked validation is not decision material, authorization, approval, request creation, submission, execution, or memory-write permission.",
        }

    packet = packet_report.get("human_operator_decision_packet")
    packet_mapping = packet if isinstance(packet, Mapping) else {}
    return {
        "validation_status": "human_operator_decision_packet_validated_for_review_only",
        "is_real_human_decision": False,
        "is_approval": False,
        "is_submittable": False,
        "is_executable": False,
        "candidate_ids": list(candidate_ids),
        "source_packet_version": EXPECTED_PACKET_REPORT_VERSION,
        "source_validation_version": packet_mapping.get("source_validation_version"),
        "source_envelope_version": packet_mapping.get("source_envelope_version"),
        "source_preparation_version": packet_mapping.get("source_preparation_version"),
        "packet_type": packet_mapping.get("packet_type"),
        "governance_requirements": list(GOVERNANCE_REQUIREMENTS),
        "required_human_actions": _required_human_actions(status, []),
        "non_authorization_notice": "Decision packet validation readiness is structural only and grants no human decision record, approval, request creation, submission, execution, or memory-write authority.",
    }


def _validation_checks(
    packet_report: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    blocking_reasons: list[str] = []

    _add_check(
        checks,
        blocking_reasons,
        "packet_report_version",
        packet_report.get("version") == EXPECTED_PACKET_REPORT_VERSION,
        "packet_report_version_must_be_2_15_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "packet_report_status",
        packet_report.get("status") == "decision_packet_ready",
        "packet_report_status_must_be_decision_packet_ready",
    )
    for key, expected in REQUIRED_PACKET_REPORT_FLAGS.items():
        _add_check(
            checks,
            blocking_reasons,
            f"packet_report_flag_{key}",
            packet_report.get(key) is expected,
            f"packet_report_flag_{key}_must_be_{str(expected).lower()}",
        )
    for key in OPTIONAL_UNSAFE_FALSE_FLAGS:
        if key in packet_report:
            _add_check(
                checks,
                blocking_reasons,
                f"packet_report_flag_{key}",
                packet_report.get(key) is False,
                f"packet_report_flag_{key}_must_be_false",
            )

    mapping = packet_report.get("civilization_core_layer_mapping")
    mapping_is_valid = isinstance(mapping, Mapping)
    _add_check(
        checks,
        blocking_reasons,
        "packet_report_layer_mapping_present",
        mapping_is_valid,
        "packet_report_layer_mapping_must_be_mapping",
    )
    if mapping_is_valid:
        _add_check(
            checks,
            blocking_reasons,
            "packet_report_primary_layer",
            mapping.get("primary_layer") == LAYER_MAPPING["primary_layer"],
            "packet_report_primary_layer_must_be_star_dome_memory",
        )
        supporting_layers = mapping.get("supporting_layers")
        _add_check(
            checks,
            blocking_reasons,
            "packet_report_supporting_layers",
            isinstance(supporting_layers, list)
            and all(layer in supporting_layers for layer in LAYER_MAPPING["supporting_layers"]),
            "packet_report_supporting_layers_must_include_required_layers",
        )

    candidate_ids = packet_report.get("candidate_ids_for_decision_review")
    candidate_ids_are_valid = (
        isinstance(candidate_ids, list)
        and bool(candidate_ids)
        and all(_safe_identifier(item) for item in candidate_ids)
    )
    _add_check(
        checks,
        blocking_reasons,
        "candidate_ids_for_decision_review_non_empty_safe_list",
        candidate_ids_are_valid,
        "candidate_ids_for_decision_review_must_be_non_empty_safe_string_list",
    )

    _add_check(
        checks,
        blocking_reasons,
        "blocked_candidate_ids_empty_list",
        packet_report.get("blocked_candidate_ids") == [],
        "blocked_candidate_ids_must_be_empty",
    )

    packet = packet_report.get("human_operator_decision_packet")
    packet_is_mapping = isinstance(packet, Mapping)
    _add_check(
        checks,
        blocking_reasons,
        "human_operator_decision_packet_present",
        packet_is_mapping,
        "human_operator_decision_packet_must_be_mapping",
    )
    if packet_is_mapping:
        _add_packet_checks(checks, blocking_reasons, packet)

    return checks, list(dict.fromkeys(blocking_reasons))


def _add_packet_checks(
    checks: list[dict[str, Any]],
    blocking_reasons: list[str],
    packet: Mapping[str, Any],
) -> None:
    _add_check(
        checks,
        blocking_reasons,
        "packet_status_review_only",
        packet.get("packet_status") == "prepared_for_human_operator_review_only",
        "packet_status_must_be_prepared_for_human_operator_review_only",
    )
    for key in ("is_real_human_decision", "is_approval", "is_submittable", "is_executable"):
        _add_check(
            checks,
            blocking_reasons,
            f"packet_{key}",
            packet.get(key) is False,
            f"packet_{key}_must_be_false",
        )
    _add_check(
        checks,
        blocking_reasons,
        "packet_type",
        packet.get("packet_type") == "human_operator_decision_packet_dry_run",
        "packet_type_must_be_human_operator_decision_packet_dry_run",
    )
    _add_check(
        checks,
        blocking_reasons,
        "packet_source_validation_version",
        packet.get("source_validation_version") == EXPECTED_SOURCE_VALIDATION_VERSION,
        "packet_source_validation_version_must_be_2_14_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "packet_source_envelope_version",
        packet.get("source_envelope_version") == EXPECTED_SOURCE_ENVELOPE_VERSION,
        "packet_source_envelope_version_must_be_2_13_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "packet_source_preparation_version",
        packet.get("source_preparation_version") == EXPECTED_SOURCE_PREPARATION_VERSION,
        "packet_source_preparation_version_must_be_2_12_0",
    )
    decision_options = packet.get("decision_options")
    _add_check(
        checks,
        blocking_reasons,
        "packet_decision_options_exact",
        isinstance(decision_options, list) and decision_options == DECISION_OPTIONS,
        "packet_decision_options_must_match_required_review_only_options",
    )
    _add_check(
        checks,
        blocking_reasons,
        "packet_no_selected_decision",
        "selected_decision" not in packet,
        "packet_must_not_contain_selected_decision",
    )
    _add_check(
        checks,
        blocking_reasons,
        "packet_no_approval_granted",
        "approval_granted" not in packet,
        "packet_must_not_contain_approval_granted",
    )


def _required_human_actions(status: str, blocking_reasons: list[str]) -> list[str]:
    if status == "decision_packet_validation_ready":
        return [
            "human_operator_must_review_validated_decision_packet_before_any_real_process",
            "human_operator_must_confirm_validation_readiness_is_not_authorization",
            "human_operator_must_use_separate_governed_process_for_any_real_decision_approval_submission_or_execution",
        ]
    actions = [
        "repair_v2_15_decision_packet_dry_run_before_validation_can_continue",
        "confirm_all_safety_flags_remain_non_authorizing",
        "provide_non_empty_candidate_ids_for_decision_review_and_empty_blocked_candidate_ids",
        "ensure_decision_packet_is_structural_and_not_real_approved_submittable_executable_or_selected",
    ]
    if blocking_reasons:
        actions.append("resolve_blocking_reasons_before_decision_packet_validation")
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
    "GOVERNED_HUMAN_OPERATOR_DECISION_PACKET_VALIDATION_VERSION",
    "build_governed_human_operator_decision_packet_validation",
    "governed_human_operator_decision_packet_validation_to_json",
]
