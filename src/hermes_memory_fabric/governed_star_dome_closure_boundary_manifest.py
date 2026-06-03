"""Governed Star-Dome closure boundary manifest for the v2.9-v2.17 chain."""

from __future__ import annotations

import json
from typing import Any, Mapping


GOVERNED_STAR_DOME_CLOSURE_BOUNDARY_MANIFEST_VERSION = "2.18.0"
SOURCE_AUDIT_VERSION = "2.17.0"

SOURCE_AUDITED_CHAIN_VERSIONS = [
    "v2.9.0",
    "v2.10.0",
    "v2.11.0",
    "v2.12.0",
    "v2.13.0",
    "v2.14.0",
    "v2.15.0",
    "v2.16.0",
]

MANIFESTED_CHAIN_VERSIONS = [
    *SOURCE_AUDITED_CHAIN_VERSIONS,
    "v2.17.0",
]

LAYER_MAPPING = {
    "primary_layer": "星穹记忆",
    "supporting_layers": ["星界记忆", "星辰记忆", "星域记忆"],
    "direction": "Star-Dome chain closure audit -> Star-Dome closure boundary manifest",
}

READY_NEXT_ALLOWED_STEP = "v2.19.0 Star-Hub preflight boundary analysis"

MANIFEST_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "manifest_only": True,
    "boundary_manifest_only": True,
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
    "boundary_manifest_authorized": False,
    "star_dome_final_closure_claimed": False,
    "star_hub_handoff_authorized": False,
    "star_hub_scheduling_authorized": False,
    "handoff_authorized": False,
    "closure_authorized": False,
    "human_decision_recorded": False,
    "approval_request_created": False,
    "approval_request_submitted": False,
    "approval_request_authorized": False,
    "approval_granted": False,
    "memory_write_authorized": False,
    "openclaw_execution_authorized": False,
}

SOURCE_REQUIRED_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "audit_only": True,
    "closure_audit_only": True,
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
    "closure_authorized": False,
    "star_dome_closed": False,
    "handoff_authorized": False,
    "human_decision_recorded": False,
    "approval_request_created": False,
    "approval_request_submitted": False,
    "approval_request_authorized": False,
    "approval_granted": False,
    "memory_write_authorized": False,
    "openclaw_execution_authorized": False,
}

UNSAFE_TRUE_FLAGS = {
    *(key for key, expected in SOURCE_REQUIRED_FLAGS.items() if expected is False),
    "boundary_manifest_authorized",
    "star_dome_final_closure_claimed",
    "star_hub_handoff_authorized",
    "star_hub_scheduling_authorized",
    "memory_write_authorized",
    "openclaw_execution_authorized",
}


def build_governed_star_dome_closure_boundary_manifest(
    audit_report: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a local-only, non-authorizing Star-Dome boundary manifest."""

    checks, blocking_reasons = _manifest_checks(audit_report)
    sensitive_field_count = _count_sensitive_keys(audit_report)
    blocking_reasons = list(dict.fromkeys(blocking_reasons))
    status = "boundary_manifest_ready" if not blocking_reasons else "blocked"
    ready = status == "boundary_manifest_ready"

    return {
        "version": GOVERNED_STAR_DOME_CLOSURE_BOUNDARY_MANIFEST_VERSION,
        "status": status,
        **MANIFEST_FLAGS,
        "star_dome_stage_boundary_manifested": ready,
        "civilization_core_layer_mapping": dict(LAYER_MAPPING),
        "source_audit_version": SOURCE_AUDIT_VERSION,
        "manifested_chain_versions": list(MANIFESTED_CHAIN_VERSIONS),
        "boundary_manifest_summary": _boundary_manifest_summary(status),
        "boundary_manifest_checks": checks,
        "star_dome_stage_closure_statement": _star_dome_stage_closure_statement(ready),
        "non_authorization_boundary": _non_authorization_boundary(),
        "preserved_governance_boundaries": _preserved_governance_boundaries(),
        "next_stage_constraints": _next_stage_constraints(),
        "scope_boundaries": _scope_boundaries(),
        "risk_notes": _risk_notes(sensitive_field_count),
        "required_human_actions": _required_human_actions(status, blocking_reasons),
        "blocking_reasons": blocking_reasons,
        "next_allowed_step": READY_NEXT_ALLOWED_STEP if ready else "resolve_v2_18_0_boundary_manifest_blockers",
        "sensitive_field_count": sensitive_field_count,
        "sensitive_fields_omitted": sensitive_field_count > 0,
    }


def governed_star_dome_closure_boundary_manifest_to_json(
    report: Mapping[str, Any],
) -> str:
    """Serialize a Star-Dome boundary manifest deterministically."""

    return json.dumps(dict(report), ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def _manifest_checks(report: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    blocking_reasons: list[str] = []

    if not isinstance(report, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_audit_report_mapping",
            False,
            "source_audit_report_must_be_mapping",
        )
        return checks, blocking_reasons

    _add_check(
        checks,
        blocking_reasons,
        "source_audit_version",
        report.get("version") == SOURCE_AUDIT_VERSION,
        "source_audit_version_must_be_2_17_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_audit_status_passed",
        report.get("status") == "chain_closure_audit_passed",
        "source_audit_status_must_be_chain_closure_audit_passed",
    )
    for key, expected in SOURCE_REQUIRED_FLAGS.items():
        _add_check(
            checks,
            blocking_reasons,
            f"source_flag_{key}",
            report.get(key) is expected,
            f"source_flag_{key}_must_be_{str(expected).lower()}",
        )
    for key in sorted(UNSAFE_TRUE_FLAGS):
        if key in report:
            _add_check(
                checks,
                blocking_reasons,
                f"source_no_unsafe_true_{key}",
                report.get(key) is not True,
                f"source_must_not_claim_{key}",
            )

    mapping = report.get("civilization_core_layer_mapping")
    _add_check(
        checks,
        blocking_reasons,
        "source_layer_mapping_shape",
        isinstance(mapping, Mapping),
        "source_layer_mapping_must_be_mapping",
    )
    if isinstance(mapping, Mapping):
        supporting_layers = mapping.get("supporting_layers")
        _add_check(
            checks,
            blocking_reasons,
            "source_primary_layer",
            mapping.get("primary_layer") == "星穹记忆",
            "source_primary_layer_must_be_star_dome_memory",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_supporting_layers",
            isinstance(supporting_layers, list)
            and all(layer in supporting_layers for layer in LAYER_MAPPING["supporting_layers"]),
            "source_supporting_layers_must_include_star_boundary_star_memory_and_star_domain",
        )

    _add_check(
        checks,
        blocking_reasons,
        "source_audited_chain_versions",
        report.get("audited_chain_versions") == SOURCE_AUDITED_CHAIN_VERSIONS,
        "source_audited_chain_versions_must_exactly_match_v2_9_0_through_v2_16_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_next_allowed_step",
        report.get("next_allowed_step") == "v2.18.0 Star-Dome closure boundary manifest",
        "source_next_allowed_step_must_be_v2_18_0_boundary_manifest",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_blocking_reasons_empty",
        report.get("blocking_reasons") == [],
        "source_blocking_reasons_must_be_empty",
    )

    summary = report.get("chain_closure_summary")
    _add_check(
        checks,
        blocking_reasons,
        "source_chain_closure_summary_shape",
        isinstance(summary, Mapping),
        "source_chain_closure_summary_must_be_mapping",
    )
    if isinstance(summary, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_star_dome_final_closure_not_claimed",
            summary.get("star_dome_final_closure_claimed") is False,
            "source_chain_closure_summary_must_not_claim_star_dome_final_closure",
        )

    boundary = report.get("non_authorization_boundary")
    _add_check(
        checks,
        blocking_reasons,
        "source_non_authorization_boundary_shape",
        isinstance(boundary, Mapping),
        "source_non_authorization_boundary_must_be_mapping",
    )
    if isinstance(boundary, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_chain_closure_not_final_closure",
            boundary.get("chain_closure_audit_passed_is_star_dome_final_closure") is False,
            "source_non_authorization_boundary_must_not_treat_audit_as_final_closure",
        )

    return checks, blocking_reasons


def _boundary_manifest_summary(status: str) -> dict[str, Any]:
    ready = status == "boundary_manifest_ready"
    return {
        "manifest_status": status,
        "source_audit_version": SOURCE_AUDIT_VERSION,
        "source_audit_passed": ready,
        "stage_boundary_ready_for_human_review": ready,
        "non_authorizing": True,
        "non_writing": True,
        "non_executing": True,
        "star_dome_final_closure_claimed": False,
        "civilization_core_complete_claimed": False,
        "only_permits_later_star_hub_preflight_boundary_analysis": ready,
    }


def _star_dome_stage_closure_statement(ready: bool) -> dict[str, Any]:
    return {
        "statement_status": (
            "star_dome_stage_boundary_manifested_for_human_review_only"
            if ready
            else "blocked"
        ),
        "star_dome_governance_chain_stage_ready_for_closure": ready,
        "star_dome_final_closure_claimed": False,
        "civilization_core_complete_claimed": False,
        "star_hub_handoff_authorized": False,
        "star_hub_scheduling_authorized": False,
        "durable_memory_write_authorized": False,
        "memory_graph_mutation_authorized": False,
        "operation_ledger_creation_authorized": False,
        "openclaw_execution_authorized": False,
        "approval_authorized": False,
        "real_human_decision_recorded": False,
        "source_audit_version": SOURCE_AUDIT_VERSION,
        "manifested_chain_versions": list(MANIFESTED_CHAIN_VERSIONS),
        "boundary_type": "star_dome_closure_boundary_manifest",
        "next_allowed_step": READY_NEXT_ALLOWED_STEP if ready else "resolve_v2_18_0_boundary_manifest_blockers",
        "required_human_actions": _required_human_actions(
            "boundary_manifest_ready" if ready else "blocked",
            [] if ready else ["source_audit_report_must_be_repaired"],
        ),
        "non_authorization_notice": (
            "Star-Dome governance chain stage boundary is manifested for human review only; this is not Civilization Core completion, final Star-Dome closure, Star-Hub scheduling, handoff, approval, memory writing, graph mutation, operation-ledger creation, real human decision recording, or execution authorization."
            if ready
            else "Boundary manifest is blocked and does not claim readiness or authorize any later action."
        ),
    }


def _non_authorization_boundary() -> dict[str, Any]:
    return {
        "boundary_manifest_ready_is_authorization": False,
        "boundary_manifest_ready_is_approval": False,
        "boundary_manifest_ready_is_human_decision": False,
        "boundary_manifest_ready_is_real_approval_request": False,
        "boundary_manifest_ready_is_request_submission": False,
        "boundary_manifest_ready_is_request_execution": False,
        "boundary_manifest_ready_is_memory_write_permission": False,
        "boundary_manifest_ready_is_memory_graph_mutation_permission": False,
        "boundary_manifest_ready_is_operation_ledger_creation": False,
        "boundary_manifest_ready_is_openclaw_execution_permission": False,
        "boundary_manifest_ready_is_star_hub_scheduling_permission": False,
        "boundary_manifest_ready_is_star_hub_handoff_permission": False,
        "boundary_manifest_ready_is_civilization_core_completion": False,
        "only_permits_later_star_hub_preflight_boundary_analysis": True,
        "human_operator_remains_final_authority": True,
    }


def _preserved_governance_boundaries() -> list[str]:
    return [
        "Boundary manifest ready is not authorization.",
        "Boundary manifest ready is not approval.",
        "Boundary manifest ready is not a real human decision.",
        "Boundary manifest ready is not a real approval request, submission, or execution.",
        "Boundary manifest ready is not durable memory write permission.",
        "Boundary manifest ready is not Memory Graph mutation permission.",
        "Boundary manifest ready is not operation-ledger creation.",
        "Boundary manifest ready is not OpenClaw execution permission.",
        "Boundary manifest ready is not Star-Hub scheduling or handoff permission.",
        "Boundary manifest ready is not Civilization Core completion.",
    ]


def _next_stage_constraints() -> list[str]:
    return [
        "The only next allowed step is v2.19.0 Star-Hub preflight boundary analysis.",
        "Star-Hub scheduling remains unauthorized.",
        "Star-Hub handoff remains unauthorized.",
        "星枢 scheduling, mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, and 星源 self-evolution remain out of scope.",
        "Human Operator remains final authority for any future governed action.",
    ]


def _scope_boundaries() -> list[str]:
    return [
        "Civilization Core is the total system.",
        "Fifteen Memory Layers are the highest memory coordinate system.",
        "Subspace Memory System is the engineering carrier.",
        "Hermes, Codex CLI, OpenClaw, Terminal, and GitHub are components, not the core.",
        "This v2.18.0 step is limited to 星穹记忆 closure boundary manifest readiness.",
        "This manifest does not enter 星枢 scheduling, mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, or 星源 self-evolution.",
    ]


def _risk_notes(sensitive_field_count: int) -> list[str]:
    notes = [
        "Boundary manifest ready must not be treated as authorization.",
        "No durable memory write, Memory Graph mutation, operation-ledger entry, GitHub API write, merge, tag creation, approval, request creation, request submission, request execution, human decision record, handoff, scheduling, or OpenClaw execution is produced or authorized.",
        "Star-Dome final closure is not claimed in the global or final sense.",
        "Civilization Core completion is not claimed.",
    ]
    if sensitive_field_count:
        notes.append("Sensitive fields were omitted from manifest output.")
    return notes


def _required_human_actions(status: str, blocking_reasons: list[str]) -> list[str]:
    if status == "boundary_manifest_ready":
        return [
            "human_operator_must_review_boundary_manifest_before_any_later_preflight",
            "human_operator_must_confirm_boundary_manifest_ready_is_not_authorization",
            "human_operator_must_use_separate_governed_process_for_any_real_approval_write_submission_execution_handoff_scheduling_or_decision",
        ]
    actions = [
        "repair_source_star_dome_chain_closure_audit_before_boundary_manifest_can_continue",
        "confirm_all_write_approval_execution_handoff_scheduling_and_final_closure_flags_remain_false",
        "rerun_local_boundary_manifest_after_blocking_reasons_are_resolved",
    ]
    if blocking_reasons:
        actions.append("resolve_blocking_reasons_before_boundary_manifest_can_be_ready")
    return actions


def _add_check(
    checks: list[dict[str, Any]],
    blocking_reasons: list[str],
    name: str,
    passed: bool,
    reason: str,
) -> None:
    checks.append({"check": name, "passed": passed})
    if not passed:
        blocking_reasons.append(reason)


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


def _is_sensitive_key(key_text: str) -> bool:
    return key_text in {
        "approval_phrase",
        "stdout",
        "stdout_tail",
        "raw_logs",
        "token",
        "api_key",
        "secret",
        "password",
        "credential",
    }


__all__ = [
    "GOVERNED_STAR_DOME_CLOSURE_BOUNDARY_MANIFEST_VERSION",
    "build_governed_star_dome_closure_boundary_manifest",
    "governed_star_dome_closure_boundary_manifest_to_json",
]
