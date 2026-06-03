"""Governed Star-Hub scheduling design boundary proposal for v2.19 preflight."""

from __future__ import annotations

import json
from typing import Any, Mapping


GOVERNED_STAR_HUB_SCHEDULING_DESIGN_BOUNDARY_PROPOSAL_VERSION = "2.20.0"
SOURCE_PREFLIGHT_VERSION = "2.19.0"

SOURCE_ANALYZED_CHAIN_VERSIONS = [
    "v2.9.0",
    "v2.10.0",
    "v2.11.0",
    "v2.12.0",
    "v2.13.0",
    "v2.14.0",
    "v2.15.0",
    "v2.16.0",
    "v2.17.0",
    "v2.18.0",
]

PROPOSED_CHAIN_VERSIONS = [
    *SOURCE_ANALYZED_CHAIN_VERSIONS,
    "v2.19.0",
]

LAYER_MAPPING = {
    "primary_layer": "星枢记忆",
    "primary_layer_status": "scheduling design boundary proposal only, not scheduling",
    "supporting_layers": ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"],
    "direction": "Star-Hub preflight boundary analysis -> Star-Hub scheduling design boundary proposal",
}

READY_NEXT_ALLOWED_STEP = "v2.21.0 Star-Hub scheduling design boundary review gate"

PROPOSAL_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "proposal_only": True,
    "design_boundary_proposal_only": True,
    "scheduling_design_boundary_proposal_only": True,
    "star_hub_design_boundary_only": True,
    "scheduling_performed": False,
    "would_schedule_anything": False,
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
    "design_boundary_authorized": False,
    "scheduling_design_authorized": False,
    "star_hub_scheduling_authorized": False,
    "star_hub_scheduling_executed": False,
    "star_hub_handoff_authorized": False,
    "handoff_authorized": False,
    "human_decision_recorded": False,
    "approval_request_created": False,
    "approval_request_submitted": False,
    "approval_request_authorized": False,
    "approval_granted": False,
    "memory_write_authorized": False,
    "openclaw_execution_authorized": False,
    "civilization_core_complete_claimed": False,
    "star_dome_final_closure_claimed": False,
}

SOURCE_REQUIRED_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "analysis_only": True,
    "preflight_only": True,
    "boundary_analysis_only": True,
    "star_hub_preflight_only": True,
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
    "preflight_analysis_authorized": False,
    "star_hub_design_authorized": False,
    "star_hub_handoff_authorized": False,
    "star_hub_scheduling_authorized": False,
    "scheduling_performed": False,
    "handoff_authorized": False,
    "human_decision_recorded": False,
    "approval_request_created": False,
    "approval_request_submitted": False,
    "approval_request_authorized": False,
    "approval_granted": False,
    "memory_write_authorized": False,
    "openclaw_execution_authorized": False,
    "civilization_core_complete_claimed": False,
    "star_dome_final_closure_claimed": False,
}

OPTIONAL_UNSAFE_TRUE_FLAGS = {
    "design_boundary_authorized",
    "scheduling_design_authorized",
    "star_hub_scheduling_executed",
    "would_schedule_anything",
    "durable_memory_write_authorized",
    "memory_graph_mutation_authorized",
    "operation_ledger_creation_authorized",
    "approval_authorized",
    "real_human_decision_recorded",
}


def build_governed_star_hub_scheduling_design_boundary_proposal(
    preflight_report: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a local-only, non-authorizing Star-Hub design boundary proposal."""

    checks, blocking_reasons = _proposal_checks(preflight_report)
    sensitive_field_count = _count_sensitive_keys(preflight_report)
    blocking_reasons = list(dict.fromkeys(blocking_reasons))
    status = (
        "star_hub_scheduling_design_boundary_proposal_ready"
        if not blocking_reasons
        else "blocked"
    )
    ready = status == "star_hub_scheduling_design_boundary_proposal_ready"

    return {
        "version": GOVERNED_STAR_HUB_SCHEDULING_DESIGN_BOUNDARY_PROPOSAL_VERSION,
        "status": status,
        **PROPOSAL_FLAGS,
        "civilization_core_layer_mapping": dict(LAYER_MAPPING),
        "source_preflight_version": SOURCE_PREFLIGHT_VERSION,
        "proposed_chain_versions": list(PROPOSED_CHAIN_VERSIONS),
        "star_hub_scheduling_design_boundary_summary": _proposal_summary(ready),
        "proposal_checks": checks,
        "source_preflight_summary": _source_preflight_summary(ready),
        "proposed_star_hub_design_boundary": _proposed_star_hub_design_boundary(ready),
        "non_authorization_boundary": _non_authorization_boundary(),
        "preserved_governance_boundaries": _preserved_governance_boundaries(),
        "future_design_constraints": _future_design_constraints(),
        "next_stage_constraints": _next_stage_constraints(),
        "scope_boundaries": _scope_boundaries(),
        "risk_notes": _risk_notes(sensitive_field_count),
        "required_human_actions": _required_human_actions(status, blocking_reasons),
        "blocking_reasons": blocking_reasons,
        "next_allowed_step": (
            READY_NEXT_ALLOWED_STEP
            if ready
            else "resolve_v2_20_0_star_hub_scheduling_design_boundary_proposal_blockers"
        ),
        "sensitive_field_count": sensitive_field_count,
        "sensitive_fields_omitted": sensitive_field_count > 0,
    }


def governed_star_hub_scheduling_design_boundary_proposal_to_json(
    report: Mapping[str, Any],
) -> str:
    """Serialize a Star-Hub scheduling design boundary proposal deterministically."""

    return json.dumps(dict(report), ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def _proposal_checks(report: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    blocking_reasons: list[str] = []

    if not isinstance(report, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_preflight_report_mapping",
            False,
            "source_preflight_report_must_be_mapping",
        )
        return checks, blocking_reasons

    _add_check(
        checks,
        blocking_reasons,
        "source_preflight_version",
        report.get("version") == SOURCE_PREFLIGHT_VERSION,
        "source_preflight_version_must_be_2_19_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_preflight_status_ready",
        report.get("status") == "star_hub_preflight_boundary_analysis_ready",
        "source_preflight_status_must_be_star_hub_preflight_boundary_analysis_ready",
    )
    for key, expected in SOURCE_REQUIRED_FLAGS.items():
        _add_check(
            checks,
            blocking_reasons,
            f"source_flag_{key}",
            report.get(key) is expected,
            f"source_flag_{key}_must_be_{str(expected).lower()}",
        )
    for key in sorted(OPTIONAL_UNSAFE_TRUE_FLAGS):
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
            mapping.get("primary_layer") == "星枢记忆",
            "source_primary_layer_must_be_star_hub_memory",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_primary_layer_status",
            mapping.get("primary_layer_status")
            == "preflight boundary analysis only, not scheduling",
            "source_primary_layer_status_must_be_preflight_boundary_analysis_only_not_scheduling",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_supporting_layers",
            isinstance(supporting_layers, list)
            and all(
                layer in supporting_layers
                for layer in ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"]
            ),
            "source_supporting_layers_must_include_required_layers",
        )

    _add_check(
        checks,
        blocking_reasons,
        "source_analyzed_chain_versions",
        report.get("analyzed_chain_versions") == SOURCE_ANALYZED_CHAIN_VERSIONS,
        "source_analyzed_chain_versions_must_exactly_match_v2_9_0_through_v2_18_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_next_allowed_step",
        report.get("next_allowed_step")
        == "v2.20.0 Star-Hub scheduling design boundary proposal",
        "source_next_allowed_step_must_be_v2_20_0_star_hub_scheduling_design_boundary_proposal",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_blocking_reasons_empty",
        report.get("blocking_reasons") == [],
        "source_blocking_reasons_must_be_empty",
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
        for key in [
            "star_hub_preflight_boundary_analysis_ready_is_star_hub_scheduling",
            "star_hub_preflight_boundary_analysis_ready_is_star_hub_handoff",
            "star_hub_preflight_boundary_analysis_ready_is_authorization",
            "star_hub_preflight_boundary_analysis_ready_is_civilization_core_completion",
        ]:
            _add_check(
                checks,
                blocking_reasons,
                f"source_non_authorization_{key}",
                boundary.get(key) is False,
                f"source_non_authorization_{key}_must_be_false",
            )

    return checks, blocking_reasons


def _proposal_summary(ready: bool) -> dict[str, Any]:
    return {
        "proposal_status": (
            "ready_for_later_star_hub_scheduling_design_boundary_review_gate"
            if ready
            else "blocked"
        ),
        "source_preflight_version": SOURCE_PREFLIGHT_VERSION,
        "source_preflight_ready": ready,
        "future_star_hub_scheduling_design_boundary_proposed_for_review": ready,
        "non_authorizing": True,
        "non_scheduling": True,
        "non_handoff": True,
        "non_writing": True,
        "non_executing": True,
        "star_hub_design_authorized": False,
        "star_hub_scheduling_authorized": False,
        "star_hub_scheduling_executed": False,
        "star_hub_handoff_authorized": False,
        "civilization_core_complete_claimed": False,
        "only_permits_later_review_gate": ready,
    }


def _source_preflight_summary(ready: bool) -> dict[str, Any]:
    return {
        "source_preflight_version": SOURCE_PREFLIGHT_VERSION,
        "source_preflight_status": (
            "star_hub_preflight_boundary_analysis_ready" if ready else "blocked"
        ),
        "source_chain_versions": list(SOURCE_ANALYZED_CHAIN_VERSIONS),
        "source_preflight_boundary_analysis_ready": ready,
        "source_preflight_authorized_scheduling": False,
        "source_preflight_authorized_handoff": False,
        "source_preflight_authorized_approval": False,
        "source_preflight_authorized_memory_write": False,
        "source_preflight_authorized_openclaw_execution": False,
        "source_preflight_claimed_civilization_core_completion": False,
    }


def _proposed_star_hub_design_boundary(ready: bool) -> dict[str, Any]:
    status = (
        "star_hub_scheduling_design_boundary_proposed_for_human_review_only"
        if ready
        else "blocked_no_star_hub_scheduling_design_boundary_readiness_claim"
    )
    return {
        "proposal_status": status,
        "boundary_type": "star_hub_scheduling_design_boundary_proposal",
        "source_preflight_version": SOURCE_PREFLIGHT_VERSION,
        "star_hub_design_boundary_proposed": ready,
        "star_hub_design_authorized": False,
        "star_hub_scheduling_authorized": False,
        "star_hub_scheduling_executed": False,
        "scheduling_performed": False,
        "star_hub_handoff_authorized": False,
        "handoff_authorized": False,
        "durable_memory_write_authorized": False,
        "memory_graph_mutation_authorized": False,
        "operation_ledger_creation_authorized": False,
        "openclaw_execution_authorized": False,
        "approval_authorized": False,
        "real_human_decision_recorded": False,
        "civilization_core_complete_claimed": False,
        "star_dome_final_closure_claimed": False,
        "proposed_chain_versions": list(PROPOSED_CHAIN_VERSIONS),
        "design_boundary_components": {
            "scheduler_scope_boundary": "describe_future_scheduler_scope_without_scheduling",
            "memory_write_boundary": "durable_memory_writes_remain_unauthorized",
            "operation_ledger_boundary": "operation_ledger_creation_remains_unauthorized",
            "openclaw_execution_boundary": "openclaw_execution_remains_unauthorized",
            "human_operator_boundary": "human_operator_remains_final_authority",
            "approval_boundary": "approval_requests_and_approvals_remain_unauthorized",
            "evidence_lineage_boundary": "use_sanitized_preflight_lineage_only",
            "fifteen_memory_layers_boundary": "fifteen_memory_layers_remain_highest_memory_coordinate_system",
        },
        "next_allowed_step": READY_NEXT_ALLOWED_STEP,
        "non_authorization_notice": (
            "A future Star-Hub scheduling design boundary is proposed for human review only; Star-Hub scheduling, Star-Hub handoff, durable memory writing, Memory Graph mutation, operation-ledger creation, OpenClaw execution, approval, human decision recording, and Civilization Core completion remain unauthorized and unperformed."
        ),
    }


def _non_authorization_boundary() -> dict[str, Any]:
    return {
        "star_hub_scheduling_design_boundary_proposal_ready_is_authorization": False,
        "star_hub_scheduling_design_boundary_proposal_ready_is_star_hub_scheduling": False,
        "star_hub_scheduling_design_boundary_proposal_ready_is_star_hub_handoff": False,
        "star_hub_scheduling_design_boundary_proposal_ready_is_approval": False,
        "star_hub_scheduling_design_boundary_proposal_ready_is_human_decision": False,
        "star_hub_scheduling_design_boundary_proposal_ready_is_real_approval_request": False,
        "star_hub_scheduling_design_boundary_proposal_ready_is_request_submission": False,
        "star_hub_scheduling_design_boundary_proposal_ready_is_request_execution": False,
        "star_hub_scheduling_design_boundary_proposal_ready_is_memory_write_permission": False,
        "star_hub_scheduling_design_boundary_proposal_ready_is_memory_graph_mutation_permission": False,
        "star_hub_scheduling_design_boundary_proposal_ready_is_operation_ledger_creation": False,
        "star_hub_scheduling_design_boundary_proposal_ready_is_openclaw_execution_permission": False,
        "star_hub_scheduling_design_boundary_proposal_ready_is_civilization_core_completion": False,
        "only_permits_later_star_hub_scheduling_design_boundary_review_gate": True,
        "human_operator_remains_final_authority": True,
    }


def _preserved_governance_boundaries() -> list[str]:
    return [
        "Star-Hub scheduling design boundary proposal ready is not authorization.",
        "Star-Hub scheduling design boundary proposal ready is not scheduling.",
        "Star-Hub scheduling design boundary proposal ready is not handoff.",
        "Star-Hub scheduling design boundary proposal ready is not approval.",
        "Star-Hub scheduling design boundary proposal ready is not a real human decision.",
        "Star-Hub scheduling design boundary proposal ready is not a real approval request.",
        "Star-Hub scheduling design boundary proposal ready is not approval request submission.",
        "Star-Hub scheduling design boundary proposal ready is not approval request execution.",
        "Star-Hub scheduling design boundary proposal ready is not durable memory write permission.",
        "Star-Hub scheduling design boundary proposal ready is not Memory Graph mutation permission.",
        "Star-Hub scheduling design boundary proposal ready is not operation-ledger creation.",
        "Star-Hub scheduling design boundary proposal ready is not OpenClaw execution permission.",
        "Star-Hub scheduling design boundary proposal ready is not Civilization Core completion.",
        "Star-Hub scheduling design boundary proposal ready only permits a later Star-Hub scheduling design boundary review gate.",
        "Human Operator remains final authority.",
    ]


def _future_design_constraints() -> list[str]:
    return [
        "Future review must remain governed and human-supervised.",
        "Future scheduling design must remain non-executing unless a separate authorized process exists.",
        "Future scheduling design must not schedule anything in this proposal stage.",
        "Future scheduling design must not write durable memory.",
        "Future scheduling design must not mutate Memory Graph.",
        "Future scheduling design must not create operation-ledger entries.",
        "Future scheduling design must not call OpenClaw.",
        "Future scheduling design must not call GitHub APIs.",
        "Future scheduling design must not create, submit, or execute approval requests.",
        "Future scheduling design must not record human decisions.",
        "Future scheduling design must preserve the Fifteen Memory Layers as the highest coordinate system.",
    ]


def _next_stage_constraints() -> list[str]:
    return [
        "The only next allowed step is v2.21.0 Star-Hub scheduling design boundary review gate.",
        "v2.21.0 may review this design boundary proposal only; it must not schedule anything unless separately authorized by a later governed process.",
        "Star-Hub scheduling remains unauthorized.",
        "Star-Hub handoff remains unauthorized.",
        "Mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, and 星源 self-evolution remain out of scope.",
        "Human Operator remains final authority for any future governed action.",
    ]


def _scope_boundaries() -> list[str]:
    return [
        "Civilization Core is the total system.",
        "Fifteen Memory Layers are the highest memory coordinate system.",
        "Subspace Memory System is the engineering carrier.",
        "Hermes, Codex CLI, OpenClaw, Terminal, and GitHub are components, not the core.",
        "This v2.20.0 step is limited to 星枢记忆 scheduling design boundary proposal only, not scheduling.",
        "This proposal does not enter mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, or 星源 self-evolution.",
    ]


def _risk_notes(sensitive_field_count: int) -> list[str]:
    notes = [
        "Scheduling design boundary proposal ready must not be treated as authorization.",
        "No durable memory write, Memory Graph mutation, operation-ledger entry, GitHub API write, merge, tag creation, approval, request creation, request submission, request execution, human decision record, handoff, scheduling, or OpenClaw execution is produced or authorized.",
        "Star-Hub scheduling and handoff are not authorized.",
        "Civilization Core completion is not claimed.",
    ]
    if sensitive_field_count:
        notes.append("Sensitive fields were omitted from proposal output.")
    return notes


def _required_human_actions(status: str, blocking_reasons: list[str]) -> list[str]:
    if status == "star_hub_scheduling_design_boundary_proposal_ready":
        return [
            "human_operator_must_review_design_boundary_proposal_before_any_later_review_gate",
            "human_operator_must_confirm_design_boundary_proposal_ready_is_not_authorization",
            "human_operator_must_use_separate_governed_process_for_any_real_approval_write_submission_execution_handoff_scheduling_or_decision",
        ]
    actions = [
        "repair_source_star_hub_preflight_boundary_analysis_before_design_boundary_proposal_can_continue",
        "confirm_all_write_approval_execution_handoff_scheduling_completion_and_final_closure_flags_remain_false",
        "rerun_local_design_boundary_proposal_after_blocking_reasons_are_resolved",
    ]
    if blocking_reasons:
        actions.append("resolve_blocking_reasons_before_design_boundary_proposal_can_be_ready")
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
    "GOVERNED_STAR_HUB_SCHEDULING_DESIGN_BOUNDARY_PROPOSAL_VERSION",
    "build_governed_star_hub_scheduling_design_boundary_proposal",
    "governed_star_hub_scheduling_design_boundary_proposal_to_json",
]
