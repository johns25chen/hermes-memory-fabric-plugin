"""Governed Star-Law preflight boundary analysis for the v2.27 manifest."""

from __future__ import annotations

import json
from typing import Any, Mapping


GOVERNED_STAR_LAW_PREFLIGHT_BOUNDARY_ANALYSIS_VERSION = "2.28.0"
SOURCE_MANIFEST_VERSION = "2.27.0"

ANALYZED_CHAIN_VERSIONS = [
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
    "v2.19.0",
    "v2.20.0",
    "v2.21.0",
    "v2.22.0",
    "v2.23.0",
    "v2.24.0",
    "v2.25.0",
    "v2.26.0",
    "v2.27.0",
]

ANALYZED_STAR_HUB_CHAIN_VERSIONS = [
    "v2.19.0",
    "v2.20.0",
    "v2.21.0",
    "v2.22.0",
    "v2.23.0",
    "v2.24.0",
    "v2.25.0",
    "v2.26.0",
    "v2.27.0",
]

SOURCE_MANIFESTED_CHAIN_VERSIONS = ANALYZED_CHAIN_VERSIONS[:-1]
SOURCE_MANIFESTED_STAR_HUB_CHAIN_VERSIONS = ANALYZED_STAR_HUB_CHAIN_VERSIONS[:-1]

LAYER_MAPPING = {
    "primary_layer": "星律记忆",
    "primary_layer_status": "Star-Law preflight boundary analysis only, not self-enforcing law and not autonomous execution",
    "source_layer": "星枢记忆",
    "source_layer_status": "Star-Hub staged closure boundary manifest complete for human review only",
    "supporting_layers": ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"],
    "direction": "Star-Hub closure boundary manifest -> Star-Law preflight boundary analysis",
}

READY_NEXT_ALLOWED_STEP = "v2.29.0 Star-Law design boundary proposal"

PREFLIGHT_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "preflight_analysis_only": True,
    "star_law_preflight_boundary_analysis_only": True,
    "star_law_self_enforcing_law_created": False,
    "star_law_self_enforcing_law_active": False,
    "star_law_rules_activated": False,
    "star_law_rules_enforced": False,
    "autonomous_governance_created": False,
    "autonomous_execution_authorized": False,
    "self_executing_policy_created": False,
    "self_executing_policy_active": False,
    "enters_star_law_layer": False,
    "mature_star_law_claimed": False,
    "enters_star_soul_layer": False,
    "enters_star_cosmos_layer": False,
    "enters_star_source_layer": False,
    "civilization_core_complete_claimed": False,
    "handoff_authorized": False,
    "star_hub_handoff_authorized": False,
    "handoff_performed": False,
    "dry_run_performed": False,
    "dry_run_executed": False,
    "scheduling_performed": False,
    "would_schedule_anything": False,
    "would_execute_dry_run": False,
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
    "approval_request_created": False,
    "approval_request_submitted": False,
    "approval_request_authorized": False,
    "approval_granted": False,
    "human_decision_recorded": False,
    "memory_write_authorized": False,
    "openclaw_execution_authorized": False,
    "star_dome_final_closure_claimed": False,
}

SOURCE_REQUIRED_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "manifest_only": True,
    "closure_boundary_manifest_only": True,
    "star_hub_closure_boundary_manifest_only": True,
    "star_hub_staged_closure_boundary_ready": True,
    "star_hub_stage_sealed_for_human_review_only": True,
    "star_hub_final_closure_claimed": False,
    "civilization_core_complete_claimed": False,
    "handoff_authorized": False,
    "star_hub_handoff_authorized": False,
    "handoff_performed": False,
    "dry_run_performed": False,
    "dry_run_executed": False,
    "scheduling_performed": False,
    "would_schedule_anything": False,
    "would_execute_dry_run": False,
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
    "approval_request_created": False,
    "approval_request_submitted": False,
    "approval_request_authorized": False,
    "approval_granted": False,
    "human_decision_recorded": False,
    "memory_write_authorized": False,
    "openclaw_execution_authorized": False,
    "star_dome_final_closure_claimed": False,
    "enters_star_law_layer": False,
    "enters_star_soul_layer": False,
    "enters_star_cosmos_layer": False,
    "enters_star_source_layer": False,
}

SOURCE_MANIFEST_BOUNDARY_REQUIRED_FLAGS = {
    "star_hub_closure_boundary_manifested": True,
    "star_hub_staged_closure_boundary_ready": True,
    "star_hub_stage_sealed_for_human_review_only": True,
    "star_hub_final_closure_claimed": False,
    "civilization_core_complete_claimed": False,
    "handoff_authorized": False,
    "star_hub_handoff_authorized": False,
    "handoff_performed": False,
    "dry_run_execution_authorized": False,
    "dry_run_performed": False,
    "dry_run_executed": False,
    "star_hub_scheduling_authorized": False,
    "star_hub_scheduling_executed": False,
    "scheduling_performed": False,
    "durable_memory_write_authorized": False,
    "memory_graph_mutation_authorized": False,
    "operation_ledger_creation_authorized": False,
    "openclaw_execution_authorized": False,
    "approval_authorized": False,
    "real_human_decision_recorded": False,
    "star_dome_final_closure_claimed": False,
    "enters_star_law_layer": False,
    "enters_star_soul_layer": False,
    "enters_star_cosmos_layer": False,
    "enters_star_source_layer": False,
}

UNSAFE_TRUE_FIELDS = {
    "star_law_self_enforcing_law_created",
    "star_law_self_enforcing_law_active",
    "star_law_rules_activated",
    "star_law_rules_enforced",
    "autonomous_governance_created",
    "autonomous_execution_authorized",
    "self_executing_policy_created",
    "self_executing_policy_active",
    "enters_star_law_layer",
    "mature_star_law_claimed",
    "enters_star_soul_layer",
    "enters_star_cosmos_layer",
    "enters_star_source_layer",
    "civilization_core_complete_claimed",
    "handoff_authorized",
    "star_hub_handoff_authorized",
    "handoff_performed",
    "dry_run_execution_authorized",
    "dry_run_performed",
    "dry_run_executed",
    "star_hub_scheduling_authorized",
    "star_hub_scheduling_executed",
    "scheduling_performed",
    "would_schedule_anything",
    "would_execute_dry_run",
    "would_mutate_memory",
    "writes_files",
    "invokes_openclaw",
    "would_call_github_api",
    "would_merge_pr",
    "would_create_tag",
    "would_write_durable_memory",
    "would_mutate_memory_graph",
    "would_create_operation_ledger_entry",
    "would_create_approval_request",
    "would_submit_approval_request",
    "would_execute_approval_request",
    "would_record_human_decision",
    "would_grant_approval",
    "authorization_granted",
    "approval_request_created",
    "approval_request_submitted",
    "approval_request_authorized",
    "approval_granted",
    "approval_authorized",
    "human_decision_recorded",
    "real_human_decision_recorded",
    "memory_write_authorized",
    "durable_memory_write_authorized",
    "memory_graph_mutation_authorized",
    "operation_ledger_creation_authorized",
    "openclaw_execution_authorized",
    "star_dome_final_closure_claimed",
}

SENSITIVE_KEYS = {
    "approval_phrase",
    "stdout_tail",
    "stdout",
    "raw_logs",
    "token",
    "api_key",
    "secret",
    "password",
    "credential",
}


def build_governed_star_law_preflight_boundary_analysis(
    manifest_report: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a local-only, non-authorizing Star-Law preflight analysis."""

    checks, blocking_reasons = _preflight_checks(manifest_report)
    sensitive_field_count = _count_sensitive_keys(manifest_report)
    blocking_reasons = list(dict.fromkeys(blocking_reasons))
    status = (
        "star_law_preflight_boundary_analysis_ready"
        if not blocking_reasons
        else "blocked"
    )
    ready = status == "star_law_preflight_boundary_analysis_ready"

    return {
        "version": GOVERNED_STAR_LAW_PREFLIGHT_BOUNDARY_ANALYSIS_VERSION,
        "status": status,
        **PREFLIGHT_FLAGS,
        "civilization_core_layer_mapping": dict(LAYER_MAPPING),
        "source_manifest_version": SOURCE_MANIFEST_VERSION,
        "analyzed_chain_versions": list(ANALYZED_CHAIN_VERSIONS),
        "analyzed_star_hub_chain_versions": list(ANALYZED_STAR_HUB_CHAIN_VERSIONS),
        "star_law_preflight_boundary_analysis_summary": _analysis_summary(ready),
        "preflight_checks": checks,
        "source_manifest_summary": _source_manifest_summary(ready),
        "star_law_preflight_boundary": _star_law_preflight_boundary(ready),
        "non_authorization_boundary": _non_authorization_boundary(),
        "preserved_governance_boundaries": _preserved_governance_boundaries(),
        "future_star_law_design_constraints": _future_star_law_design_constraints(),
        "next_stage_constraints": _next_stage_constraints(),
        "scope_boundaries": _scope_boundaries(),
        "risk_notes": _risk_notes(sensitive_field_count),
        "required_human_actions": _required_human_actions(status, blocking_reasons),
        "blocking_reasons": blocking_reasons,
        "next_allowed_step": (
            READY_NEXT_ALLOWED_STEP
            if ready
            else "resolve_v2_28_0_star_law_preflight_boundary_analysis_blockers"
        ),
        "sensitive_field_count": sensitive_field_count,
        "sensitive_fields_omitted": sensitive_field_count > 0,
    }


def governed_star_law_preflight_boundary_analysis_to_json(
    report: Mapping[str, Any],
) -> str:
    """Serialize a Star-Law preflight boundary analysis deterministically."""

    return json.dumps(dict(report), ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def _preflight_checks(
    report: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[str]]:
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
        "source_manifest_version_must_be_2_27_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_manifest_status_ready",
        report.get("status") == "star_hub_closure_boundary_manifest_ready",
        "source_manifest_status_must_be_star_hub_closure_boundary_manifest_ready",
    )
    for key, expected in SOURCE_REQUIRED_FLAGS.items():
        _add_check(
            checks,
            blocking_reasons,
            f"source_flag_{key}",
            report.get(key) is expected,
            f"source_flag_{key}_must_be_{str(expected).lower()}",
        )
    _add_check(
        checks,
        blocking_reasons,
        "source_no_unsafe_true_claims",
        _unsafe_true_fields(report) == [],
        "source_must_not_claim_star_law_activation_autonomous_execution_handoff_scheduling_approval_write_execution_dry_run_or_civilization_core_completion",
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
            == "Star-Hub staged closure boundary manifest only, not handoff and not execution",
            "source_primary_layer_status_must_be_closure_boundary_manifest_only_not_handoff_not_execution",
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
        "source_manifested_chain_versions",
        report.get("manifested_chain_versions") == SOURCE_MANIFESTED_CHAIN_VERSIONS,
        "source_manifested_chain_versions_must_exactly_match_v2_9_0_through_v2_26_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_manifested_star_hub_chain_versions",
        report.get("manifested_star_hub_chain_versions")
        == SOURCE_MANIFESTED_STAR_HUB_CHAIN_VERSIONS,
        "source_manifested_star_hub_chain_versions_must_exactly_match_v2_19_0_through_v2_26_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_next_allowed_step",
        report.get("next_allowed_step")
        == "v2.28.0 Star-Law preflight boundary analysis",
        "source_next_allowed_step_must_be_v2_28_0_star_law_preflight_boundary_analysis",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_blocking_reasons_empty",
        report.get("blocking_reasons") == [],
        "source_blocking_reasons_must_be_empty",
    )

    manifest = report.get("star_hub_closure_boundary_manifest")
    _add_check(
        checks,
        blocking_reasons,
        "source_star_hub_closure_boundary_manifest_shape",
        isinstance(manifest, Mapping),
        "source_star_hub_closure_boundary_manifest_must_be_mapping",
    )
    if isinstance(manifest, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_manifest_boundary_status",
            manifest.get("manifest_status")
            == "star_hub_staged_closure_boundary_manifested_for_human_review_only",
            "source_manifest_boundary_status_must_be_human_review_only",
        )
        for key, expected in SOURCE_MANIFEST_BOUNDARY_REQUIRED_FLAGS.items():
            _add_check(
                checks,
                blocking_reasons,
                f"source_manifest_boundary_{key}",
                manifest.get(key) is expected,
                f"source_manifest_boundary_{key}_must_be_{str(expected).lower()}",
            )

    return checks, blocking_reasons


def _analysis_summary(ready: bool) -> dict[str, Any]:
    return {
        "preflight_status": (
            "star_law_preflight_boundary_analyzed_for_human_review_only"
            if ready
            else "blocked"
        ),
        "source_manifest_version": SOURCE_MANIFEST_VERSION,
        "source_star_hub_closure_boundary_manifest_valid": ready,
        "star_law_design_boundary_proposal_ready_for_human_review_only": ready,
        "star_law_self_enforcing_law_created": False,
        "star_law_rules_activated": False,
        "star_law_rules_enforced": False,
        "autonomous_governance_created": False,
        "autonomous_execution_authorized": False,
        "civilization_core_complete_claimed": False,
        "only_permits_later_star_law_design_boundary_proposal": ready,
    }


def _source_manifest_summary(ready: bool) -> dict[str, Any]:
    return {
        "source_manifest_version": SOURCE_MANIFEST_VERSION,
        "source_manifest_status": (
            "star_hub_closure_boundary_manifest_ready" if ready else "blocked"
        ),
        "source_manifest_non_authorizing": True,
        "source_manifest_star_hub_staged_closure_boundary_ready": ready,
        "source_manifest_authorized_handoff": False,
        "source_manifest_authorized_scheduling": False,
        "source_manifest_authorized_dry_run_execution": False,
        "source_manifest_authorized_approval": False,
        "source_manifest_authorized_memory_write": False,
        "source_manifest_authorized_openclaw_execution": False,
        "source_manifest_claimed_civilization_core_completion": False,
        "source_manifest_claimed_next_layer_entry": False,
    }


def _star_law_preflight_boundary(ready: bool) -> dict[str, Any]:
    return {
        "preflight_status": (
            "star_law_preflight_boundary_analyzed_for_human_review_only"
            if ready
            else "blocked_no_star_law_preflight_boundary_readiness_claim"
        ),
        "boundary_type": "star_law_preflight_boundary_analysis",
        "source_manifest_version": SOURCE_MANIFEST_VERSION,
        "star_law_preflight_boundary_analyzed": ready,
        "star_law_design_boundary_proposal_ready_for_human_review_only": ready,
        "source_star_hub_boundary_manifest_valid": ready,
        "star_law_self_enforcing_law_created": False,
        "star_law_self_enforcing_law_active": False,
        "star_law_rules_activated": False,
        "star_law_rules_enforced": False,
        "autonomous_governance_created": False,
        "autonomous_execution_authorized": False,
        "self_executing_policy_created": False,
        "self_executing_policy_active": False,
        "enters_star_law_layer": False,
        "mature_star_law_claimed": False,
        "enters_star_soul_layer": False,
        "enters_star_cosmos_layer": False,
        "enters_star_source_layer": False,
        "civilization_core_complete_claimed": False,
        "durable_memory_write_authorized": False,
        "memory_graph_mutation_authorized": False,
        "operation_ledger_creation_authorized": False,
        "openclaw_execution_authorized": False,
        "approval_authorized": False,
        "real_human_decision_recorded": False,
        "analyzed_chain_versions": list(ANALYZED_CHAIN_VERSIONS),
        "analyzed_star_hub_chain_versions": list(ANALYZED_STAR_HUB_CHAIN_VERSIONS),
        "star_law_preflight_boundary_components": {
            "source_star_hub_closure_boundary_manifest_analysis": "v2.27.0_structural_source_boundary_validated_for_human_review_only",
            "star_law_scope_preflight_analysis": "future_star_law_design_boundary_scope_identified_without_rule_creation",
            "self_enforcing_law_non_activation_analysis": "no_self_enforcing_memory_law_created_active_or_started",
            "autonomous_execution_non_authorization_analysis": "no_autonomous_governance_or_execution_authorized",
            "memory_write_boundary_analysis": "no_durable_memory_write_permission_created",
            "memory_graph_mutation_boundary_analysis": "no_memory_graph_mutation_permission_created",
            "operation_ledger_boundary_analysis": "no_operation_ledger_entry_creation_permission_created",
            "openclaw_execution_boundary_analysis": "no_openclaw_execution_permission_created",
            "approval_boundary_analysis": "no_approval_request_or_approval_created_submitted_executed_or_granted",
            "human_operator_boundary_analysis": "human_operator_remains_final_authority",
            "fifteen_memory_layers_boundary_analysis": "fifteen_memory_layers_remain_highest_memory_coordinate_system",
        },
        "next_allowed_step": READY_NEXT_ALLOWED_STEP,
        "non_authorization_notice": (
            "The Star-Law preflight boundary has been analyzed for human review only. The Star-Hub closure boundary manifest is a structurally valid source for a future Star-Law design boundary proposal. This analysis does not create, activate, or enforce Star-Law rules; does not create self-enforcing memory law, autonomous governance, autonomous execution, self-executing policy, approval, handoff, scheduling, dry-run execution, durable memory write permission, Memory Graph mutation permission, operation-ledger creation, OpenClaw execution permission, or Civilization Core completion; and does not start 星魂 continuity, 星宙 evolution, or 星源 self-evolution."
        ),
    }


def _non_authorization_boundary() -> dict[str, Any]:
    return {
        "star_law_preflight_boundary_analysis_ready_is_self_enforcing_memory_law": False,
        "star_law_preflight_boundary_analysis_ready_is_rule_activation": False,
        "star_law_preflight_boundary_analysis_ready_is_rule_enforcement": False,
        "star_law_preflight_boundary_analysis_ready_is_autonomous_governance": False,
        "star_law_preflight_boundary_analysis_ready_is_autonomous_execution": False,
        "star_law_preflight_boundary_analysis_ready_is_handoff": False,
        "star_law_preflight_boundary_analysis_ready_is_authorization": False,
        "star_law_preflight_boundary_analysis_ready_is_scheduling": False,
        "star_law_preflight_boundary_analysis_ready_is_dry_run_execution": False,
        "star_law_preflight_boundary_analysis_ready_is_approval": False,
        "star_law_preflight_boundary_analysis_ready_is_human_decision": False,
        "star_law_preflight_boundary_analysis_ready_is_memory_write_permission": False,
        "star_law_preflight_boundary_analysis_ready_is_memory_graph_mutation_permission": False,
        "star_law_preflight_boundary_analysis_ready_is_operation_ledger_creation": False,
        "star_law_preflight_boundary_analysis_ready_is_openclaw_execution_permission": False,
        "star_law_preflight_boundary_analysis_ready_is_civilization_core_completion": False,
        "only_permits_later_star_law_design_boundary_proposal": True,
        "human_operator_remains_final_authority": True,
    }


def _preserved_governance_boundaries() -> list[str]:
    return [
        "Star-Law preflight boundary analysis ready is not self-enforcing memory law.",
        "Star-Law preflight boundary analysis ready is not rule activation.",
        "Star-Law preflight boundary analysis ready is not rule enforcement.",
        "Star-Law preflight boundary analysis ready is not autonomous governance.",
        "Star-Law preflight boundary analysis ready is not autonomous execution.",
        "Star-Law preflight boundary analysis ready is not handoff.",
        "Star-Law preflight boundary analysis ready is not authorization.",
        "Star-Law preflight boundary analysis ready is not scheduling.",
        "Star-Law preflight boundary analysis ready is not dry-run execution.",
        "Star-Law preflight boundary analysis ready is not approval.",
        "Star-Law preflight boundary analysis ready is not a real human decision.",
        "Star-Law preflight boundary analysis ready is not durable memory write permission.",
        "Star-Law preflight boundary analysis ready is not Memory Graph mutation permission.",
        "Star-Law preflight boundary analysis ready is not operation-ledger creation.",
        "Star-Law preflight boundary analysis ready is not OpenClaw execution permission.",
        "Star-Law preflight boundary analysis ready is not Civilization Core completion.",
        "Star-Law preflight boundary analysis ready only permits a later Star-Law design boundary proposal.",
        "Human Operator remains final authority.",
    ]


def _future_star_law_design_constraints() -> list[str]:
    return [
        "A future Star-Law design boundary proposal may be prepared only through a separate governed process.",
        "A future proposal must remain non-executing until explicitly reviewed by the Human Operator.",
        "This preflight analysis must not be treated as Star-Law rule creation, activation, or enforcement.",
        "This preflight analysis must not be treated as self-enforcing policy or autonomous governance.",
    ]


def _next_stage_constraints() -> list[str]:
    return [
        "The only next allowed step is v2.29.0 Star-Law design boundary proposal.",
        "v2.28.0 is Star-Law preflight boundary analysis only, not self-enforcing law and not autonomous execution.",
        "v2.28.0 must not authorize Star-Hub handoff, scheduling, approval, dry-run execution, memory writing, Memory Graph mutation, operation-ledger creation, OpenClaw execution, or GitHub API actions.",
        "Mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, and 星源 self-evolution remain out of scope.",
        "Human Operator remains final authority for any future governed action.",
    ]


def _scope_boundaries() -> list[str]:
    return [
        "Civilization Core is the total system.",
        "Fifteen Memory Layers are the highest memory coordinate system.",
        "Subspace Memory System is the engineering carrier.",
        "Hermes, Codex CLI, OpenClaw, Terminal, and GitHub are components, not the core.",
        "This v2.28.0 step is limited to 星律记忆 Star-Law preflight boundary analysis only.",
        "This analysis does not enter mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, or 星源 self-evolution.",
    ]


def _risk_notes(sensitive_field_count: int) -> list[str]:
    notes = [
        "Star-Law preflight boundary analysis ready must not be treated as self-enforcing memory law, rule activation, rule enforcement, autonomous governance, autonomous execution, handoff, authorization, scheduling, approval, dry-run execution, or Civilization Core completion.",
        "No durable memory write, Memory Graph mutation, operation-ledger entry, GitHub API write, merge, tag creation, approval, request creation, request submission, request execution, human decision record, handoff, scheduling, dry-run performance, dry-run execution, or OpenClaw execution is produced or authorized.",
        "Mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, and 星源 self-evolution are not started.",
    ]
    if sensitive_field_count:
        notes.append("Sensitive fields were omitted from preflight boundary analysis output.")
    return notes


def _required_human_actions(status: str, blocking_reasons: list[str]) -> list[str]:
    if status == "star_law_preflight_boundary_analysis_ready":
        return [
            "human_operator_must_review_star_law_preflight_boundary_analysis_before_any_later_star_law_design_boundary_proposal",
            "human_operator_must_confirm_star_law_preflight_boundary_analysis_ready_is_not_self_enforcing_law_rule_activation_rule_enforcement_autonomous_execution_handoff_authorization_scheduling_approval_write_execution_or_civilization_core_completion",
            "human_operator_must_use_separate_governed_process_for_any_future_star_law_design_boundary_proposal_or_real_approval_write_submission_execution_handoff_scheduling_dry_run_decision_or_next_layer_work",
        ]
    actions = [
        "repair_source_star_hub_closure_boundary_manifest_before_star_law_preflight_boundary_analysis_can_continue",
        "confirm_all_star_law_activation_autonomous_execution_handoff_scheduling_dry_run_write_approval_execution_next_layer_and_civilization_core_completion_flags_remain_false",
        "rerun_local_star_law_preflight_boundary_analysis_after_blocking_reasons_are_resolved",
    ]
    if blocking_reasons:
        actions.append(
            "resolve_blocking_reasons_before_star_law_preflight_boundary_analysis_can_be_ready"
        )
    return actions


def _add_check(
    checks: list[dict[str, Any]],
    blocking_reasons: list[str],
    name: str,
    passed: bool,
    reason: str,
) -> None:
    checks.append({"name": name, "passed": passed})
    if not passed:
        blocking_reasons.append(reason)


def _unsafe_true_fields(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if key in UNSAFE_TRUE_FIELDS and nested is True:
                found.append(key)
            found.extend(_unsafe_true_fields(nested))
    elif isinstance(value, list):
        for nested in value:
            found.extend(_unsafe_true_fields(nested))
    return found


def _count_sensitive_keys(value: Any) -> int:
    if isinstance(value, Mapping):
        return sum(
            (1 if key in SENSITIVE_KEYS else 0) + _count_sensitive_keys(nested)
            for key, nested in value.items()
        )
    if isinstance(value, list):
        return sum(_count_sensitive_keys(nested) for nested in value)
    return 0


__all__ = [
    "GOVERNED_STAR_LAW_PREFLIGHT_BOUNDARY_ANALYSIS_VERSION",
    "ANALYZED_CHAIN_VERSIONS",
    "ANALYZED_STAR_HUB_CHAIN_VERSIONS",
    "build_governed_star_law_preflight_boundary_analysis",
    "governed_star_law_preflight_boundary_analysis_to_json",
]
