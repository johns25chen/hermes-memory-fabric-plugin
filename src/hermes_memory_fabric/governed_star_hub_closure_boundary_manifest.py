"""Governed Star-Hub closure boundary manifest for the v2.19-v2.26 chain."""

from __future__ import annotations

import json
from typing import Any, Mapping


GOVERNED_STAR_HUB_CLOSURE_BOUNDARY_MANIFEST_VERSION = "2.27.0"
SOURCE_AUDIT_VERSION = "2.26.0"

MANIFESTED_CHAIN_VERSIONS = [
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
]

MANIFESTED_STAR_HUB_CHAIN_VERSIONS = [
    "v2.19.0",
    "v2.20.0",
    "v2.21.0",
    "v2.22.0",
    "v2.23.0",
    "v2.24.0",
    "v2.25.0",
    "v2.26.0",
]

SOURCE_AUDITED_CHAIN_VERSIONS = MANIFESTED_CHAIN_VERSIONS[:-1]
SOURCE_AUDITED_STAR_HUB_CHAIN_VERSIONS = MANIFESTED_STAR_HUB_CHAIN_VERSIONS[:-1]

LAYER_MAPPING = {
    "primary_layer": "星枢记忆",
    "primary_layer_status": "Star-Hub staged closure boundary manifest only, not handoff and not execution",
    "supporting_layers": ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"],
    "direction": "Star-Hub chain closure audit -> Star-Hub closure boundary manifest",
}

READY_NEXT_ALLOWED_STEP = "v2.28.0 Star-Law preflight boundary analysis"

MANIFEST_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "manifest_only": True,
    "closure_boundary_manifest_only": True,
    "star_hub_closure_boundary_manifest_only": True,
    "star_hub_final_closure_claimed": False,
    "civilization_core_complete_claimed": False,
    "handoff_authorized": False,
    "star_hub_handoff_authorized": False,
    "handoff_performed": False,
    "closure_manifest_authorized_handoff": False,
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
    "dry_run_execution_boundary_review_authorized": False,
    "dry_run_execution_boundary_authorized": False,
    "dry_run_execution_authorized": False,
    "scheduling_dry_run_authorized": False,
    "star_hub_scheduling_authorized": False,
    "star_hub_scheduling_executed": False,
    "human_decision_recorded": False,
    "approval_request_created": False,
    "approval_request_submitted": False,
    "approval_request_authorized": False,
    "approval_granted": False,
    "memory_write_authorized": False,
    "openclaw_execution_authorized": False,
    "star_dome_final_closure_claimed": False,
    "enters_star_law_layer": False,
    "enters_star_soul_layer": False,
    "enters_star_cosmos_layer": False,
    "enters_star_source_layer": False,
}

SOURCE_REQUIRED_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "audit_only": True,
    "chain_closure_audit_only": True,
    "star_hub_chain_closure_audit_only": True,
    "closure_manifest_created": False,
    "star_hub_final_closure_claimed": False,
    "star_hub_closure_claimed": False,
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
    "dry_run_execution_boundary_review_authorized": False,
    "dry_run_execution_boundary_authorized": False,
    "dry_run_execution_authorized": False,
    "scheduling_dry_run_authorized": False,
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

SOURCE_AUDITED_BOUNDARY_REQUIRED_FLAGS = {
    "star_hub_chain_audited": True,
    "star_hub_chain_structurally_continuous": True,
    "star_hub_chain_closure_manifest_ready_for_human_review_only": True,
    "star_hub_final_closure_claimed": False,
    "star_hub_closure_claimed": False,
    "closure_manifest_created": False,
    "handoff_authorized": False,
    "star_hub_handoff_authorized": False,
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
    "civilization_core_complete_claimed": False,
    "star_dome_final_closure_claimed": False,
}

SOURCE_NON_AUTHORIZATION_KEYS = [
    "star_hub_chain_closure_audit_ready_is_star_hub_final_closure",
    "star_hub_chain_closure_audit_ready_is_star_hub_closure",
    "star_hub_chain_closure_audit_ready_is_closure_boundary_manifest",
    "star_hub_chain_closure_audit_ready_is_star_hub_handoff",
    "star_hub_chain_closure_audit_ready_is_authorization",
    "star_hub_chain_closure_audit_ready_is_scheduling",
    "star_hub_chain_closure_audit_ready_is_dry_run_execution",
    "star_hub_chain_closure_audit_ready_is_approval",
    "star_hub_chain_closure_audit_ready_is_civilization_core_completion",
]

UNSAFE_TRUE_FIELDS = {
    "closure_manifest_created",
    "star_hub_final_closure_claimed",
    "star_hub_closure_claimed",
    "civilization_core_complete_claimed",
    "handoff_authorized",
    "star_hub_handoff_authorized",
    "handoff_performed",
    "dry_run_performed",
    "dry_run_executed",
    "would_execute_dry_run",
    "dry_run_execution_boundary_review_authorized",
    "dry_run_execution_boundary_authorized",
    "dry_run_execution_authorized",
    "scheduling_dry_run_authorized",
    "star_hub_scheduling_authorized",
    "star_hub_scheduling_executed",
    "scheduling_performed",
    "would_schedule_anything",
    "approval_request_created",
    "approval_request_submitted",
    "approval_request_authorized",
    "approval_granted",
    "approval_authorized",
    "authorization_granted",
    "human_decision_recorded",
    "real_human_decision_recorded",
    "would_create_approval_request",
    "would_submit_approval_request",
    "would_execute_approval_request",
    "would_record_human_decision",
    "would_grant_approval",
    "memory_write_authorized",
    "durable_memory_write_authorized",
    "would_write_durable_memory",
    "memory_graph_mutation_authorized",
    "would_mutate_memory_graph",
    "operation_ledger_creation_authorized",
    "would_create_operation_ledger_entry",
    "openclaw_execution_authorized",
    "openclaw_execution_allowed",
    "would_call_github_api",
    "would_merge_pr",
    "would_create_tag",
    "would_mutate_memory",
    "writes_files",
    "invokes_openclaw",
    "star_dome_final_closure_claimed",
    "enters_star_law_layer",
    "enters_star_soul_layer",
    "enters_star_cosmos_layer",
    "enters_star_source_layer",
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


def build_governed_star_hub_closure_boundary_manifest(
    audit_report: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a local-only, non-authorizing Star-Hub closure boundary manifest."""

    checks, blocking_reasons = _manifest_checks(audit_report)
    sensitive_field_count = _count_sensitive_keys(audit_report)
    blocking_reasons = list(dict.fromkeys(blocking_reasons))
    status = (
        "star_hub_closure_boundary_manifest_ready"
        if not blocking_reasons
        else "blocked"
    )
    ready = status == "star_hub_closure_boundary_manifest_ready"

    return {
        "version": GOVERNED_STAR_HUB_CLOSURE_BOUNDARY_MANIFEST_VERSION,
        "status": status,
        **MANIFEST_FLAGS,
        "star_hub_staged_closure_boundary_ready": ready,
        "star_hub_stage_sealed_for_human_review_only": ready,
        "civilization_core_layer_mapping": dict(LAYER_MAPPING),
        "source_audit_version": SOURCE_AUDIT_VERSION,
        "manifested_chain_versions": list(MANIFESTED_CHAIN_VERSIONS),
        "manifested_star_hub_chain_versions": list(MANIFESTED_STAR_HUB_CHAIN_VERSIONS),
        "star_hub_closure_boundary_manifest_summary": _manifest_summary(ready),
        "manifest_checks": checks,
        "source_audit_summary": _source_audit_summary(ready),
        "star_hub_closure_boundary_manifest": _star_hub_closure_boundary_manifest(ready),
        "non_authorization_boundary": _non_authorization_boundary(),
        "preserved_governance_boundaries": _preserved_governance_boundaries(),
        "post_closure_constraints": _post_closure_constraints(),
        "next_stage_constraints": _next_stage_constraints(),
        "scope_boundaries": _scope_boundaries(),
        "risk_notes": _risk_notes(sensitive_field_count),
        "required_human_actions": _required_human_actions(status, blocking_reasons),
        "blocking_reasons": blocking_reasons,
        "next_allowed_step": (
            READY_NEXT_ALLOWED_STEP
            if ready
            else "resolve_v2_27_0_star_hub_closure_boundary_manifest_blockers"
        ),
        "sensitive_field_count": sensitive_field_count,
        "sensitive_fields_omitted": sensitive_field_count > 0,
    }


def governed_star_hub_closure_boundary_manifest_to_json(
    report: Mapping[str, Any],
) -> str:
    """Serialize a Star-Hub closure boundary manifest report deterministically."""

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
        "source_audit_version_must_be_2_26_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_audit_status_ready",
        report.get("status") == "star_hub_chain_closure_audit_ready",
        "source_audit_status_must_be_star_hub_chain_closure_audit_ready",
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
        "source_must_not_claim_final_closure_handoff_scheduling_approval_write_execution_dry_run_or_next_layer_entry",
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
            == "Star-Hub chain closure audit only, not final closure and not handoff",
            "source_primary_layer_status_must_be_chain_closure_audit_only_not_final_closure_not_handoff",
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
        "source_audited_chain_versions",
        report.get("audited_chain_versions") == SOURCE_AUDITED_CHAIN_VERSIONS,
        "source_audited_chain_versions_must_exactly_match_v2_9_0_through_v2_25_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_audited_star_hub_chain_versions",
        report.get("audited_star_hub_chain_versions")
        == SOURCE_AUDITED_STAR_HUB_CHAIN_VERSIONS,
        "source_audited_star_hub_chain_versions_must_exactly_match_v2_19_0_through_v2_25_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_next_allowed_step",
        report.get("next_allowed_step") == "v2.27.0 Star-Hub closure boundary manifest",
        "source_next_allowed_step_must_be_v2_27_0_star_hub_closure_boundary_manifest",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_blocking_reasons_empty",
        report.get("blocking_reasons") == [],
        "source_blocking_reasons_must_be_empty",
    )

    audited = report.get("audited_star_hub_chain_boundary")
    _add_check(
        checks,
        blocking_reasons,
        "source_audited_star_hub_chain_boundary_shape",
        isinstance(audited, Mapping),
        "source_audited_star_hub_chain_boundary_must_be_mapping",
    )
    if isinstance(audited, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_audited_boundary_status",
            audited.get("audit_status")
            == "star_hub_chain_audited_for_closure_boundary_manifest_readiness_only",
            "source_audited_boundary_status_must_be_closure_boundary_manifest_readiness_only",
        )
        for key, expected in SOURCE_AUDITED_BOUNDARY_REQUIRED_FLAGS.items():
            _add_check(
                checks,
                blocking_reasons,
                f"source_audited_boundary_{key}",
                audited.get(key) is expected,
                f"source_audited_boundary_{key}_must_be_{str(expected).lower()}",
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
        for key in SOURCE_NON_AUTHORIZATION_KEYS:
            _add_check(
                checks,
                blocking_reasons,
                f"source_non_authorization_{key}",
                boundary.get(key) is False,
                f"source_non_authorization_{key}_must_be_false",
            )

    return checks, blocking_reasons


def _manifest_summary(ready: bool) -> dict[str, Any]:
    return {
        "manifest_status": (
            "star_hub_staged_closure_boundary_readiness_manifested_for_human_review_only"
            if ready
            else "blocked"
        ),
        "source_audit_version": SOURCE_AUDIT_VERSION,
        "source_audit_ready": ready,
        "star_hub_staged_closure_boundary_ready": ready,
        "star_hub_boundary_milestone_structurally_sealed_for_human_review_only": ready,
        "civilization_core_complete_claimed": False,
        "star_hub_final_closure_claimed": False,
        "star_hub_handoff_authorized": False,
        "handoff_performed": False,
        "star_hub_scheduling_authorized": False,
        "star_hub_scheduling_executed": False,
        "dry_run_execution_authorized": False,
        "dry_run_performed": False,
        "dry_run_executed": False,
        "approval_granted": False,
        "real_human_decision_recorded": False,
        "only_permits_later_star_law_preflight_boundary_analysis": ready,
    }


def _source_audit_summary(ready: bool) -> dict[str, Any]:
    return {
        "source_audit_version": SOURCE_AUDIT_VERSION,
        "source_audit_status": (
            "star_hub_chain_closure_audit_ready" if ready else "blocked"
        ),
        "source_audited_chain_versions": list(SOURCE_AUDITED_CHAIN_VERSIONS),
        "source_audited_star_hub_chain_versions": list(
            SOURCE_AUDITED_STAR_HUB_CHAIN_VERSIONS
        ),
        "source_audit_non_authorizing": True,
        "source_audit_created_closure_manifest": False,
        "source_audit_authorized_handoff": False,
        "source_audit_authorized_scheduling": False,
        "source_audit_authorized_dry_run_execution": False,
        "source_audit_authorized_approval": False,
        "source_audit_authorized_memory_write": False,
        "source_audit_authorized_openclaw_execution": False,
        "source_audit_claimed_star_hub_final_closure": False,
        "source_audit_claimed_civilization_core_completion": False,
    }


def _star_hub_closure_boundary_manifest(ready: bool) -> dict[str, Any]:
    return {
        "manifest_status": (
            "star_hub_staged_closure_boundary_manifested_for_human_review_only"
            if ready
            else "blocked_no_star_hub_closure_boundary_readiness_claim"
        ),
        "boundary_type": "star_hub_closure_boundary_manifest",
        "source_audit_version": SOURCE_AUDIT_VERSION,
        "star_hub_closure_boundary_manifested": ready,
        "star_hub_staged_closure_boundary_ready": ready,
        "star_hub_stage_sealed_for_human_review_only": ready,
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
        "manifested_chain_versions": list(MANIFESTED_CHAIN_VERSIONS),
        "manifested_star_hub_chain_versions": list(MANIFESTED_STAR_HUB_CHAIN_VERSIONS),
        "star_hub_closure_boundary_manifest_components": {
            "star_hub_preflight_boundary_analysis_manifest": "v2.19.0_structural_lineage_preserved",
            "star_hub_scheduling_design_boundary_manifest": "v2.20.0_v2.21.0_structural_lineage_preserved",
            "star_hub_scheduling_dry_run_plan_boundary_manifest": "v2.22.0_v2.23.0_structural_lineage_preserved",
            "star_hub_scheduling_dry_run_execution_boundary_manifest": "v2.24.0_v2.25.0_structural_lineage_preserved",
            "star_hub_chain_closure_audit_manifest": "v2.26.0_structural_audit_lineage_preserved",
            "non_authorization_boundary_manifest": "all_authorization_execution_write_handoff_scheduling_approval_and_dry_run_flags_remain_false",
            "evidence_lineage_boundary_manifest": "sanitized_structural_lineage_only",
            "fifteen_memory_layers_boundary_manifest": "fifteen_memory_layers_remain_highest_memory_coordinate_system",
            "post_star_hub_next_layer_boundary_manifest": "only_v2_28_0_star_law_preflight_boundary_analysis_is_next_allowed_step",
        },
        "next_allowed_step": READY_NEXT_ALLOWED_STEP,
        "non_authorization_notice": (
            "This is the formal Star-Hub closure boundary manifest: the Star-Hub stage has reached staged closure boundary readiness for human review and the Star-Hub boundary milestone is structurally sealed for human review only. It does not complete Civilization Core, authorize or perform Star-Hub handoff, authorize or perform Star-Hub scheduling, perform or execute a dry-run, authorize dry-run execution, permit durable memory writing, permit Memory Graph mutation, create operation-ledger entries, permit OpenClaw execution, grant approval, record a real human decision, or start mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, or 星源 self-evolution."
        ),
    }


def _non_authorization_boundary() -> dict[str, Any]:
    return {
        "star_hub_closure_boundary_manifest_ready_is_civilization_core_completion": False,
        "star_hub_closure_boundary_manifest_ready_is_star_hub_handoff": False,
        "star_hub_closure_boundary_manifest_ready_is_handoff_authorization": False,
        "star_hub_closure_boundary_manifest_ready_is_handoff_performance": False,
        "star_hub_closure_boundary_manifest_ready_is_scheduling_authorization": False,
        "star_hub_closure_boundary_manifest_ready_is_scheduling": False,
        "star_hub_closure_boundary_manifest_ready_is_dry_run_execution": False,
        "star_hub_closure_boundary_manifest_ready_is_dry_run_execution_authorization": False,
        "star_hub_closure_boundary_manifest_ready_is_approval": False,
        "star_hub_closure_boundary_manifest_ready_is_human_decision": False,
        "star_hub_closure_boundary_manifest_ready_is_real_approval_request": False,
        "star_hub_closure_boundary_manifest_ready_is_request_submission": False,
        "star_hub_closure_boundary_manifest_ready_is_request_execution": False,
        "star_hub_closure_boundary_manifest_ready_is_memory_write_permission": False,
        "star_hub_closure_boundary_manifest_ready_is_memory_graph_mutation_permission": False,
        "star_hub_closure_boundary_manifest_ready_is_operation_ledger_creation": False,
        "star_hub_closure_boundary_manifest_ready_is_openclaw_execution_permission": False,
        "only_permits_later_star_law_preflight_boundary_analysis": True,
        "human_operator_remains_final_authority": True,
    }


def _preserved_governance_boundaries() -> list[str]:
    return [
        "Star-Hub closure boundary manifest ready is not Civilization Core completion.",
        "Star-Hub closure boundary manifest ready is not handoff.",
        "Star-Hub closure boundary manifest ready is not authorization.",
        "Star-Hub closure boundary manifest ready is not scheduling.",
        "Star-Hub closure boundary manifest ready is not dry-run execution.",
        "Star-Hub closure boundary manifest ready is not approval.",
        "Star-Hub closure boundary manifest ready is not a real human decision.",
        "Star-Hub closure boundary manifest ready is not a real approval request.",
        "Star-Hub closure boundary manifest ready is not approval request submission.",
        "Star-Hub closure boundary manifest ready is not approval request execution.",
        "Star-Hub closure boundary manifest ready is not durable memory write permission.",
        "Star-Hub closure boundary manifest ready is not Memory Graph mutation permission.",
        "Star-Hub closure boundary manifest ready is not operation-ledger creation.",
        "Star-Hub closure boundary manifest ready is not OpenClaw execution permission.",
        "Star-Hub closure boundary manifest ready only permits a later Star-Law preflight boundary analysis.",
        "Human Operator remains final authority.",
    ]


def _post_closure_constraints() -> list[str]:
    return [
        "Star-Hub staged closure boundary readiness requires human review before any later stage action.",
        "This manifest must not be used as Star-Hub handoff authorization.",
        "This manifest must not be used as Star-Hub scheduling authorization.",
        "This manifest must not be used as dry-run execution authorization.",
        "This manifest must not be used to write durable memory, mutate Memory Graph, or create operation-ledger entries.",
        "This manifest must not call OpenClaw or GitHub APIs.",
    ]


def _next_stage_constraints() -> list[str]:
    return [
        "The only next allowed step is v2.28.0 Star-Law preflight boundary analysis.",
        "v2.27.0 is Star-Hub closure boundary manifest only, not Star-Hub handoff and not execution.",
        "v2.27.0 must not claim Civilization Core completion or Star-Dome final closure.",
        "v2.27.0 must not authorize Star-Hub scheduling, handoff, approval, dry-run execution, memory writing, Memory Graph mutation, operation-ledger creation, OpenClaw execution, or GitHub API actions.",
        "Mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, and 星源 self-evolution remain out of scope.",
        "Human Operator remains final authority for any future governed action.",
    ]


def _scope_boundaries() -> list[str]:
    return [
        "Civilization Core is the total system.",
        "Fifteen Memory Layers are the highest memory coordinate system.",
        "Subspace Memory System is the engineering carrier.",
        "Hermes, Codex CLI, OpenClaw, Terminal, and GitHub are components, not the core.",
        "This v2.27.0 step is limited to 星枢记忆 Star-Hub staged closure boundary manifest only, not handoff and not execution.",
        "This manifest does not enter mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, or 星源 self-evolution.",
    ]


def _risk_notes(sensitive_field_count: int) -> list[str]:
    notes = [
        "Star-Hub closure boundary manifest ready must not be treated as Civilization Core completion, final Star-Hub closure, authorization, scheduling, handoff, approval, or dry-run execution.",
        "No dry-run performance, dry-run execution, durable memory write, Memory Graph mutation, operation-ledger entry, GitHub API write, merge, tag creation, approval, request creation, request submission, request execution, human decision record, handoff, scheduling, or OpenClaw execution is produced or authorized.",
        "Star-Hub scheduling, handoff, and final closure are not authorized or performed.",
        "Civilization Core completion and Star-Dome final closure are not claimed.",
        "Star-Law, Star-Soul, Star-Cosmos, and Star-Source layer entry is not claimed.",
    ]
    if sensitive_field_count:
        notes.append("Sensitive fields were omitted from closure boundary manifest output.")
    return notes


def _required_human_actions(status: str, blocking_reasons: list[str]) -> list[str]:
    if status == "star_hub_closure_boundary_manifest_ready":
        return [
            "human_operator_must_review_star_hub_closure_boundary_manifest_before_any_later_star_law_preflight_boundary_analysis",
            "human_operator_must_confirm_star_hub_closure_boundary_manifest_ready_is_not_civilization_core_completion_handoff_authorization_scheduling_approval_write_execution_or_dry_run_execution",
            "human_operator_must_use_separate_governed_process_for_any_real_approval_write_submission_execution_handoff_scheduling_dry_run_decision_or_next_layer_work",
        ]
    actions = [
        "repair_source_star_hub_chain_closure_audit_before_closure_boundary_manifest_can_continue",
        "confirm_all_closure_write_approval_execution_handoff_scheduling_dry_run_completion_next_layer_and_civilization_core_completion_flags_remain_false",
        "rerun_local_closure_boundary_manifest_after_blocking_reasons_are_resolved",
    ]
    if blocking_reasons:
        actions.append(
            "resolve_blocking_reasons_before_star_hub_closure_boundary_manifest_can_be_ready"
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
    "GOVERNED_STAR_HUB_CLOSURE_BOUNDARY_MANIFEST_VERSION",
    "MANIFESTED_CHAIN_VERSIONS",
    "MANIFESTED_STAR_HUB_CHAIN_VERSIONS",
    "build_governed_star_hub_closure_boundary_manifest",
    "governed_star_hub_closure_boundary_manifest_to_json",
]
