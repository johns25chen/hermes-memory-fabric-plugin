"""Governed Star-Hub preflight boundary analysis for the v2.18 manifest."""

from __future__ import annotations

import json
from typing import Any, Mapping


GOVERNED_STAR_HUB_PREFLIGHT_BOUNDARY_ANALYSIS_VERSION = "2.19.0"
SOURCE_MANIFEST_VERSION = "2.18.0"

SOURCE_MANIFESTED_CHAIN_VERSIONS = [
    "v2.9.0",
    "v2.10.0",
    "v2.11.0",
    "v2.12.0",
    "v2.13.0",
    "v2.14.0",
    "v2.15.0",
    "v2.16.0",
    "v2.17.0",
]

ANALYZED_CHAIN_VERSIONS = [
    *SOURCE_MANIFESTED_CHAIN_VERSIONS,
    "v2.18.0",
]

LAYER_MAPPING = {
    "primary_layer": "星枢记忆",
    "primary_layer_status": "preflight boundary analysis only, not scheduling",
    "supporting_layers": ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"],
    "direction": "Star-Dome closure boundary manifest -> Star-Hub preflight boundary analysis",
}

READY_NEXT_ALLOWED_STEP = "v2.20.0 Star-Hub scheduling design boundary proposal"

PREFLIGHT_FLAGS = {
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
    "closure_authorized": False,
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
    "star_dome_stage_boundary_manifested": True,
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

OPTIONAL_UNSAFE_TRUE_FLAGS = {
    "civilization_core_complete_claimed",
    "scheduling_performed",
    "durable_memory_write_authorized",
    "memory_graph_mutation_authorized",
    "operation_ledger_creation_authorized",
    "approval_authorized",
    "real_human_decision_recorded",
}


def build_governed_star_hub_preflight_boundary_analysis(
    manifest_report: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a local-only, non-authorizing Star-Hub preflight analysis."""

    checks, blocking_reasons = _preflight_checks(manifest_report)
    sensitive_field_count = _count_sensitive_keys(manifest_report)
    blocking_reasons = list(dict.fromkeys(blocking_reasons))
    status = (
        "star_hub_preflight_boundary_analysis_ready"
        if not blocking_reasons
        else "blocked"
    )
    ready = status == "star_hub_preflight_boundary_analysis_ready"

    return {
        "version": GOVERNED_STAR_HUB_PREFLIGHT_BOUNDARY_ANALYSIS_VERSION,
        "status": status,
        **PREFLIGHT_FLAGS,
        "civilization_core_layer_mapping": dict(LAYER_MAPPING),
        "source_manifest_version": SOURCE_MANIFEST_VERSION,
        "analyzed_chain_versions": list(ANALYZED_CHAIN_VERSIONS),
        "star_hub_preflight_summary": _star_hub_preflight_summary(ready),
        "star_hub_preflight_checks": checks,
        "source_star_dome_boundary_summary": _source_star_dome_boundary_summary(ready),
        "future_star_hub_design_constraints": _future_star_hub_design_constraints(),
        "non_authorization_boundary": _non_authorization_boundary(),
        "preserved_governance_boundaries": _preserved_governance_boundaries(),
        "next_stage_constraints": _next_stage_constraints(),
        "scope_boundaries": _scope_boundaries(),
        "risk_notes": _risk_notes(sensitive_field_count),
        "required_human_actions": _required_human_actions(status, blocking_reasons),
        "blocking_reasons": blocking_reasons,
        "next_allowed_step": (
            READY_NEXT_ALLOWED_STEP
            if ready
            else "resolve_v2_19_0_star_hub_preflight_boundary_analysis_blockers"
        ),
        "sensitive_field_count": sensitive_field_count,
        "sensitive_fields_omitted": sensitive_field_count > 0,
    }


def governed_star_hub_preflight_boundary_analysis_to_json(
    report: Mapping[str, Any],
) -> str:
    """Serialize a Star-Hub preflight boundary analysis deterministically."""

    return json.dumps(dict(report), ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def _preflight_checks(report: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    blocking_reasons: list[str] = []

    if not isinstance(report, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_manifest_report_mapping",
            False,
            "source_manifest_report_must_be_mapping",
        )
        return checks, blocking_reasons

    _add_check(
        checks,
        blocking_reasons,
        "source_manifest_version",
        report.get("version") == SOURCE_MANIFEST_VERSION,
        "source_manifest_version_must_be_2_18_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_manifest_status_ready",
        report.get("status") == "boundary_manifest_ready",
        "source_manifest_status_must_be_boundary_manifest_ready",
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
            mapping.get("primary_layer") == "星穹记忆",
            "source_primary_layer_must_be_star_dome_memory",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_supporting_layers",
            isinstance(supporting_layers, list)
            and all(
                layer in supporting_layers
                for layer in ["星界记忆", "星辰记忆", "星域记忆"]
            ),
            "source_supporting_layers_must_include_star_boundary_star_memory_and_star_domain",
        )

    _add_check(
        checks,
        blocking_reasons,
        "source_manifested_chain_versions",
        report.get("manifested_chain_versions") == SOURCE_MANIFESTED_CHAIN_VERSIONS,
        "source_manifested_chain_versions_must_exactly_match_v2_9_0_through_v2_17_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_next_allowed_step",
        report.get("next_allowed_step") == "v2.19.0 Star-Hub preflight boundary analysis",
        "source_next_allowed_step_must_be_v2_19_0_star_hub_preflight_boundary_analysis",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_blocking_reasons_empty",
        report.get("blocking_reasons") == [],
        "source_blocking_reasons_must_be_empty",
    )

    statement = report.get("star_dome_stage_closure_statement")
    _add_check(
        checks,
        blocking_reasons,
        "source_star_dome_stage_closure_statement_shape",
        isinstance(statement, Mapping),
        "source_star_dome_stage_closure_statement_must_be_mapping",
    )
    if isinstance(statement, Mapping):
        required_statement = {
            "statement_status": "star_dome_stage_boundary_manifested_for_human_review_only",
            "star_dome_governance_chain_stage_ready_for_closure": True,
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
        }
        for key, expected in required_statement.items():
            _add_check(
                checks,
                blocking_reasons,
                f"source_statement_{key}",
                statement.get(key) is expected
                if isinstance(expected, bool)
                else statement.get(key) == expected,
                f"source_statement_{key}_must_be_{str(expected).lower()}",
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
            "boundary_manifest_ready_is_star_hub_scheduling_permission",
            "boundary_manifest_ready_is_star_hub_handoff_permission",
            "boundary_manifest_ready_is_civilization_core_completion",
        ]:
            _add_check(
                checks,
                blocking_reasons,
                f"source_non_authorization_{key}",
                boundary.get(key) is False,
                f"source_non_authorization_{key}_must_be_false",
            )

    return checks, blocking_reasons


def _star_hub_preflight_summary(ready: bool) -> dict[str, Any]:
    return {
        "preflight_status": (
            "ready_for_later_star_hub_scheduling_design_boundary_proposal"
            if ready
            else "blocked"
        ),
        "source_manifest_version": SOURCE_MANIFEST_VERSION,
        "source_boundary_manifest_ready": ready,
        "structurally_ready_for_future_design_boundary_proposal": ready,
        "non_authorizing": True,
        "non_writing": True,
        "non_executing": True,
        "star_hub_scheduling_authorized": False,
        "star_hub_handoff_authorized": False,
        "star_hub_design_authorized": False,
        "civilization_core_complete_claimed": False,
        "only_permits_later_star_hub_scheduling_design_boundary_proposal": ready,
    }


def _source_star_dome_boundary_summary(ready: bool) -> dict[str, Any]:
    return {
        "source_manifest_version": SOURCE_MANIFEST_VERSION,
        "source_boundary_status": "boundary_manifest_ready" if ready else "blocked",
        "star_dome_stage_boundary_manifested": ready,
        "star_dome_final_closure_claimed": False,
        "civilization_core_complete_claimed": False,
        "star_hub_handoff_authorized": False,
        "star_hub_scheduling_authorized": False,
        "scheduling_performed": False,
        "handoff_authorized": False,
        "durable_memory_write_authorized": False,
        "memory_graph_mutation_authorized": False,
        "operation_ledger_creation_authorized": False,
        "openclaw_execution_authorized": False,
        "approval_authorized": False,
        "real_human_decision_recorded": False,
        "analyzed_chain_versions": list(ANALYZED_CHAIN_VERSIONS),
        "source_boundary_type": "star_dome_closure_boundary_manifest",
        "next_allowed_step": READY_NEXT_ALLOWED_STEP if ready else "repair_source_boundary_manifest",
        "non_authorization_notice": (
            "Star-Dome boundary manifest readiness only supports a later governed Star-Hub scheduling design boundary proposal; it is not scheduling, handoff, approval, memory writing, graph mutation, operation-ledger creation, human decision recording, OpenClaw execution, or Civilization Core completion."
            if ready
            else "Source Star-Dome boundary manifest did not satisfy preflight analysis requirements and does not claim readiness."
        ),
    }


def _future_star_hub_design_constraints() -> list[str]:
    return [
        "Future design must remain governed.",
        "Future design must remain dry-run/proposal-only until a separate human-governed approval process exists.",
        "Future design must not schedule anything.",
        "Future design must not write durable memory.",
        "Future design must not mutate Memory Graph.",
        "Future design must not create operation-ledger entries.",
        "Future design must not call OpenClaw.",
        "Future design must not call GitHub APIs.",
        "Future design must not create, submit, or execute approval requests.",
        "Future design must not record human decisions.",
        "Future design must preserve the Fifteen Memory Layers as the highest coordinate system.",
    ]


def _non_authorization_boundary() -> dict[str, Any]:
    return {
        "star_hub_preflight_boundary_analysis_ready_is_authorization": False,
        "star_hub_preflight_boundary_analysis_ready_is_star_hub_scheduling": False,
        "star_hub_preflight_boundary_analysis_ready_is_star_hub_handoff": False,
        "star_hub_preflight_boundary_analysis_ready_is_approval": False,
        "star_hub_preflight_boundary_analysis_ready_is_human_decision": False,
        "star_hub_preflight_boundary_analysis_ready_is_real_approval_request": False,
        "star_hub_preflight_boundary_analysis_ready_is_request_submission": False,
        "star_hub_preflight_boundary_analysis_ready_is_request_execution": False,
        "star_hub_preflight_boundary_analysis_ready_is_memory_write_permission": False,
        "star_hub_preflight_boundary_analysis_ready_is_memory_graph_mutation_permission": False,
        "star_hub_preflight_boundary_analysis_ready_is_operation_ledger_creation": False,
        "star_hub_preflight_boundary_analysis_ready_is_openclaw_execution_permission": False,
        "star_hub_preflight_boundary_analysis_ready_is_civilization_core_completion": False,
        "only_permits_later_star_hub_scheduling_design_boundary_proposal": True,
        "human_operator_remains_final_authority": True,
    }


def _preserved_governance_boundaries() -> list[str]:
    return [
        "Star-Hub preflight boundary analysis ready is not authorization.",
        "Star-Hub preflight boundary analysis ready is not Star-Hub scheduling.",
        "Star-Hub preflight boundary analysis ready is not Star-Hub handoff.",
        "Star-Hub preflight boundary analysis ready is not approval.",
        "Star-Hub preflight boundary analysis ready is not a real human decision.",
        "Star-Hub preflight boundary analysis ready is not a real approval request, submission, or execution.",
        "Star-Hub preflight boundary analysis ready is not durable memory write permission.",
        "Star-Hub preflight boundary analysis ready is not Memory Graph mutation permission.",
        "Star-Hub preflight boundary analysis ready is not operation-ledger creation.",
        "Star-Hub preflight boundary analysis ready is not OpenClaw execution permission.",
        "Star-Hub preflight boundary analysis ready is not Civilization Core completion.",
    ]


def _next_stage_constraints() -> list[str]:
    return [
        "The only next allowed step is v2.20.0 Star-Hub scheduling design boundary proposal.",
        "v2.20.0 may propose a design boundary only; it must not schedule anything.",
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
        "This v2.19.0 step is limited to 星枢记忆 preflight boundary analysis only, not scheduling.",
        "This analysis does not enter mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, or 星源 self-evolution.",
    ]


def _risk_notes(sensitive_field_count: int) -> list[str]:
    notes = [
        "Preflight boundary analysis ready must not be treated as authorization.",
        "No durable memory write, Memory Graph mutation, operation-ledger entry, GitHub API write, merge, tag creation, approval, request creation, request submission, request execution, human decision record, handoff, scheduling, or OpenClaw execution is produced or authorized.",
        "Star-Hub scheduling and handoff are not authorized.",
        "Civilization Core completion is not claimed.",
    ]
    if sensitive_field_count:
        notes.append("Sensitive fields were omitted from analysis output.")
    return notes


def _required_human_actions(status: str, blocking_reasons: list[str]) -> list[str]:
    if status == "star_hub_preflight_boundary_analysis_ready":
        return [
            "human_operator_must_review_preflight_boundary_analysis_before_any_later_design_boundary_proposal",
            "human_operator_must_confirm_preflight_ready_is_not_authorization",
            "human_operator_must_use_separate_governed_process_for_any_real_approval_write_submission_execution_handoff_scheduling_or_decision",
        ]
    actions = [
        "repair_source_star_dome_boundary_manifest_before_preflight_analysis_can_continue",
        "confirm_all_write_approval_execution_handoff_scheduling_completion_and_final_closure_flags_remain_false",
        "rerun_local_preflight_boundary_analysis_after_blocking_reasons_are_resolved",
    ]
    if blocking_reasons:
        actions.append("resolve_blocking_reasons_before_preflight_boundary_analysis_can_be_ready")
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
    "GOVERNED_STAR_HUB_PREFLIGHT_BOUNDARY_ANALYSIS_VERSION",
    "build_governed_star_hub_preflight_boundary_analysis",
    "governed_star_hub_preflight_boundary_analysis_to_json",
]
