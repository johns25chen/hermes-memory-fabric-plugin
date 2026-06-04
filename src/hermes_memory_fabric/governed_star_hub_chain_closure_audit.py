"""Governed Star-Hub chain closure audit for the v2.19-v2.25 chain."""

from __future__ import annotations

import json
from typing import Any, Mapping


GOVERNED_STAR_HUB_CHAIN_CLOSURE_AUDIT_VERSION = "2.26.0"
SOURCE_REVIEW_GATE_VERSION = "2.25.0"

AUDITED_CHAIN_VERSIONS = [
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
]

AUDITED_STAR_HUB_CHAIN_VERSIONS = [
    "v2.19.0",
    "v2.20.0",
    "v2.21.0",
    "v2.22.0",
    "v2.23.0",
    "v2.24.0",
    "v2.25.0",
]

SOURCE_REVIEWED_CHAIN_VERSIONS = AUDITED_CHAIN_VERSIONS[:-1]

LAYER_MAPPING = {
    "primary_layer": "星枢记忆",
    "primary_layer_status": "Star-Hub chain closure audit only, not final closure and not handoff",
    "supporting_layers": ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"],
    "direction": "Star-Hub scheduling dry-run execution boundary review gate -> Star-Hub chain closure audit",
}

READY_NEXT_ALLOWED_STEP = "v2.27.0 Star-Hub closure boundary manifest"

AUDIT_FLAGS = {
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

SOURCE_REQUIRED_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "review_gate_only": True,
    "dry_run_execution_boundary_review_gate_only": True,
    "scheduling_dry_run_execution_boundary_review_gate_only": True,
    "star_hub_dry_run_execution_review_gate_only": True,
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
    "star_hub_closure_claimed": False,
    "star_dome_final_closure_claimed": False,
}

SOURCE_REVIEWED_BOUNDARY_REQUIRED_FLAGS = {
    "star_hub_dry_run_execution_boundary_reviewed": True,
    "dry_run_execution_boundary_review_authorized": False,
    "dry_run_execution_boundary_authorized": False,
    "dry_run_execution_authorized": False,
    "dry_run_performed": False,
    "dry_run_executed": False,
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
    "star_hub_closure_claimed": False,
    "star_dome_final_closure_claimed": False,
}

UNSAFE_TRUE_FIELDS = {
    "closure_manifest_created",
    "star_hub_final_closure_claimed",
    "star_hub_closure_claimed",
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
    "star_hub_handoff_authorized",
    "handoff_authorized",
    "approval_request_created",
    "approval_request_submitted",
    "approval_request_authorized",
    "approval_granted",
    "approval_authorized",
    "authorization_granted",
    "human_decision_recorded",
    "real_human_decision_recorded",
    "memory_write_authorized",
    "durable_memory_write_authorized",
    "memory_graph_mutation_authorized",
    "operation_ledger_creation_authorized",
    "openclaw_execution_authorized",
    "civilization_core_complete_claimed",
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


def build_governed_star_hub_chain_closure_audit(
    review_gate_report: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a local-only, non-authorizing Star-Hub chain closure audit."""

    checks, blocking_reasons = _audit_checks(review_gate_report)
    sensitive_field_count = _count_sensitive_keys(review_gate_report)
    blocking_reasons = list(dict.fromkeys(blocking_reasons))
    status = "star_hub_chain_closure_audit_ready" if not blocking_reasons else "blocked"
    ready = status == "star_hub_chain_closure_audit_ready"

    return {
        "version": GOVERNED_STAR_HUB_CHAIN_CLOSURE_AUDIT_VERSION,
        "status": status,
        **AUDIT_FLAGS,
        "civilization_core_layer_mapping": dict(LAYER_MAPPING),
        "source_review_gate_version": SOURCE_REVIEW_GATE_VERSION,
        "audited_chain_versions": list(AUDITED_CHAIN_VERSIONS),
        "audited_star_hub_chain_versions": list(AUDITED_STAR_HUB_CHAIN_VERSIONS),
        "star_hub_chain_closure_audit_summary": _audit_summary(ready),
        "audit_checks": checks,
        "source_review_gate_summary": _source_review_gate_summary(ready),
        "audited_star_hub_chain_boundary": _audited_star_hub_chain_boundary(ready),
        "non_authorization_boundary": _non_authorization_boundary(),
        "preserved_governance_boundaries": _preserved_governance_boundaries(),
        "future_closure_manifest_constraints": _future_closure_manifest_constraints(),
        "next_stage_constraints": _next_stage_constraints(),
        "scope_boundaries": _scope_boundaries(),
        "risk_notes": _risk_notes(sensitive_field_count),
        "required_human_actions": _required_human_actions(status, blocking_reasons),
        "blocking_reasons": blocking_reasons,
        "next_allowed_step": (
            READY_NEXT_ALLOWED_STEP
            if ready
            else "resolve_v2_26_0_star_hub_chain_closure_audit_blockers"
        ),
        "sensitive_field_count": sensitive_field_count,
        "sensitive_fields_omitted": sensitive_field_count > 0,
    }


def governed_star_hub_chain_closure_audit_to_json(report: Mapping[str, Any]) -> str:
    """Serialize a Star-Hub chain closure audit report deterministically."""

    return json.dumps(dict(report), ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def _audit_checks(report: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    blocking_reasons: list[str] = []

    if not isinstance(report, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_review_gate_report_mapping",
            False,
            "source_review_gate_report_must_be_mapping",
        )
        return checks, blocking_reasons

    _add_check(
        checks,
        blocking_reasons,
        "source_review_gate_version",
        report.get("version") == SOURCE_REVIEW_GATE_VERSION,
        "source_review_gate_version_must_be_2_25_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_review_gate_status_ready",
        report.get("status")
        == "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready",
        "source_review_gate_status_must_be_star_hub_scheduling_dry_run_execution_boundary_review_gate_ready",
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
        "source_must_not_claim_closure_manifest_scheduling_handoff_approval_write_execution_or_dry_run_execution",
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
            == "scheduling dry-run execution boundary review gate only, not scheduling and not dry-run execution",
            "source_primary_layer_status_must_be_execution_boundary_review_gate_only_not_scheduling_not_dry_run_execution",
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
        "source_reviewed_chain_versions",
        report.get("reviewed_chain_versions") == SOURCE_REVIEWED_CHAIN_VERSIONS,
        "source_reviewed_chain_versions_must_exactly_match_v2_9_0_through_v2_24_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_next_allowed_step",
        report.get("next_allowed_step") == "v2.26.0 Star-Hub chain closure audit",
        "source_next_allowed_step_must_be_v2_26_0_star_hub_chain_closure_audit",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_blocking_reasons_empty",
        report.get("blocking_reasons") == [],
        "source_blocking_reasons_must_be_empty",
    )

    reviewed = report.get("reviewed_star_hub_dry_run_execution_boundary")
    _add_check(
        checks,
        blocking_reasons,
        "source_reviewed_star_hub_dry_run_execution_boundary_shape",
        isinstance(reviewed, Mapping),
        "source_reviewed_star_hub_dry_run_execution_boundary_must_be_mapping",
    )
    if isinstance(reviewed, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_reviewed_boundary_status",
            reviewed.get("review_status")
            == "star_hub_scheduling_dry_run_execution_boundary_reviewed_for_human_review_only",
            "source_reviewed_boundary_status_must_be_human_review_only",
        )
        for key, expected in SOURCE_REVIEWED_BOUNDARY_REQUIRED_FLAGS.items():
            _add_check(
                checks,
                blocking_reasons,
                f"source_reviewed_boundary_{key}",
                reviewed.get(key) is expected,
                f"source_reviewed_boundary_{key}_must_be_{str(expected).lower()}",
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
            "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready_is_star_hub_scheduling",
            "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready_is_dry_run_execution",
            "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready_is_star_hub_handoff",
            "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready_is_authorization",
            "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready_is_star_hub_closure",
            "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready_is_civilization_core_completion",
        ]:
            _add_check(
                checks,
                blocking_reasons,
                f"source_non_authorization_{key}",
                boundary.get(key) is False,
                f"source_non_authorization_{key}_must_be_false",
            )

    return checks, blocking_reasons


def _audit_summary(ready: bool) -> dict[str, Any]:
    return {
        "audit_status": (
            "audited_for_later_star_hub_closure_boundary_manifest_readiness_only"
            if ready
            else "blocked"
        ),
        "source_review_gate_version": SOURCE_REVIEW_GATE_VERSION,
        "source_review_gate_ready": ready,
        "star_hub_governance_chain_structurally_continuous": ready,
        "ready_for_later_star_hub_closure_boundary_manifest": ready,
        "closure_manifest_created": False,
        "star_hub_final_closure_claimed": False,
        "star_hub_closure_claimed": False,
        "star_hub_handoff_authorized": False,
        "star_hub_scheduling_authorized": False,
        "dry_run_execution_authorized": False,
        "dry_run_performed": False,
        "dry_run_executed": False,
        "durable_memory_write_authorized": False,
        "memory_graph_mutation_authorized": False,
        "operation_ledger_creation_authorized": False,
        "openclaw_execution_authorized": False,
        "civilization_core_complete_claimed": False,
        "only_permits_later_star_hub_closure_boundary_manifest": ready,
    }


def _source_review_gate_summary(ready: bool) -> dict[str, Any]:
    return {
        "source_review_gate_version": SOURCE_REVIEW_GATE_VERSION,
        "source_review_gate_status": (
            "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready"
            if ready
            else "blocked"
        ),
        "source_reviewed_chain_versions": list(SOURCE_REVIEWED_CHAIN_VERSIONS),
        "source_review_gate_non_authorizing": True,
        "source_review_gate_authorized_dry_run_execution": False,
        "source_review_gate_authorized_scheduling": False,
        "source_review_gate_authorized_handoff": False,
        "source_review_gate_authorized_approval": False,
        "source_review_gate_authorized_memory_write": False,
        "source_review_gate_authorized_openclaw_execution": False,
        "source_review_gate_claimed_star_hub_closure": False,
        "source_review_gate_claimed_civilization_core_completion": False,
    }


def _audited_star_hub_chain_boundary(ready: bool) -> dict[str, Any]:
    status = (
        "star_hub_chain_audited_for_closure_boundary_manifest_readiness_only"
        if ready
        else "blocked_no_star_hub_chain_closure_boundary_manifest_readiness_claim"
    )
    return {
        "audit_status": status,
        "boundary_type": "star_hub_chain_closure_audit",
        "source_review_gate_version": SOURCE_REVIEW_GATE_VERSION,
        "star_hub_chain_audited": ready,
        "star_hub_chain_structurally_continuous": ready,
        "star_hub_chain_closure_manifest_ready_for_human_review_only": ready,
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
        "audited_chain_versions": list(AUDITED_CHAIN_VERSIONS),
        "audited_star_hub_chain_versions": list(AUDITED_STAR_HUB_CHAIN_VERSIONS),
        "star_hub_chain_audit_components": {
            "preflight_boundary_analysis_audit": "v2.19.0_checked_for_chain_continuity",
            "scheduling_design_boundary_proposal_audit": "v2.20.0_checked_for_chain_continuity",
            "scheduling_design_boundary_review_gate_audit": "v2.21.0_checked_for_chain_continuity",
            "scheduling_dry_run_plan_boundary_proposal_audit": "v2.22.0_checked_for_chain_continuity",
            "scheduling_dry_run_plan_boundary_review_gate_audit": "v2.23.0_checked_for_chain_continuity",
            "scheduling_dry_run_execution_boundary_proposal_audit": "v2.24.0_checked_for_chain_continuity",
            "scheduling_dry_run_execution_boundary_review_gate_audit": "v2.25.0_checked_for_chain_continuity",
            "non_authorization_boundary_audit": "all_authorization_execution_write_handoff_scheduling_and_closure_flags_remain_false",
            "evidence_lineage_boundary_audit": "sanitized_structural_lineage_only",
            "fifteen_memory_layers_boundary_audit": "fifteen_memory_layers_remain_highest_memory_coordinate_system",
        },
        "next_allowed_step": READY_NEXT_ALLOWED_STEP,
        "non_authorization_notice": (
            "The Star-Hub governance chain is audited for closure boundary manifest readiness only; it is structurally continuous and ready for a later closure boundary manifest step, while Star-Hub final closure, Star-Hub closure completion, closure manifest creation, Star-Hub handoff, Star-Hub scheduling, dry-run performance, dry-run execution, dry-run execution authorization, durable memory writing, Memory Graph mutation, operation-ledger creation, OpenClaw execution, approval, human decision recording, Civilization Core completion, and Star-Dome final closure remain unauthorized, unperformed, and unclaimed."
        ),
    }


def _non_authorization_boundary() -> dict[str, Any]:
    return {
        "star_hub_chain_closure_audit_ready_is_star_hub_final_closure": False,
        "star_hub_chain_closure_audit_ready_is_star_hub_closure": False,
        "star_hub_chain_closure_audit_ready_is_closure_boundary_manifest": False,
        "star_hub_chain_closure_audit_ready_is_star_hub_handoff": False,
        "star_hub_chain_closure_audit_ready_is_authorization": False,
        "star_hub_chain_closure_audit_ready_is_scheduling": False,
        "star_hub_chain_closure_audit_ready_is_dry_run_execution": False,
        "star_hub_chain_closure_audit_ready_is_approval": False,
        "star_hub_chain_closure_audit_ready_is_human_decision": False,
        "star_hub_chain_closure_audit_ready_is_real_approval_request": False,
        "star_hub_chain_closure_audit_ready_is_request_submission": False,
        "star_hub_chain_closure_audit_ready_is_request_execution": False,
        "star_hub_chain_closure_audit_ready_is_memory_write_permission": False,
        "star_hub_chain_closure_audit_ready_is_memory_graph_mutation_permission": False,
        "star_hub_chain_closure_audit_ready_is_operation_ledger_creation": False,
        "star_hub_chain_closure_audit_ready_is_openclaw_execution_permission": False,
        "star_hub_chain_closure_audit_ready_is_civilization_core_completion": False,
        "only_permits_later_star_hub_closure_boundary_manifest": True,
        "human_operator_remains_final_authority": True,
    }


def _preserved_governance_boundaries() -> list[str]:
    return [
        "Star-Hub chain closure audit ready is not final Star-Hub closure.",
        "Star-Hub chain closure audit ready is not a closure boundary manifest.",
        "Star-Hub chain closure audit ready is not handoff.",
        "Star-Hub chain closure audit ready is not authorization.",
        "Star-Hub chain closure audit ready is not scheduling.",
        "Star-Hub chain closure audit ready is not dry-run execution.",
        "Star-Hub chain closure audit ready is not approval.",
        "Star-Hub chain closure audit ready is not a real human decision.",
        "Star-Hub chain closure audit ready is not a real approval request.",
        "Star-Hub chain closure audit ready is not approval request submission.",
        "Star-Hub chain closure audit ready is not approval request execution.",
        "Star-Hub chain closure audit ready is not durable memory write permission.",
        "Star-Hub chain closure audit ready is not Memory Graph mutation permission.",
        "Star-Hub chain closure audit ready is not operation-ledger creation.",
        "Star-Hub chain closure audit ready is not OpenClaw execution permission.",
        "Star-Hub chain closure audit ready is not Civilization Core completion.",
        "Star-Hub chain closure audit ready only permits a later Star-Hub closure boundary manifest.",
        "Human Operator remains final authority.",
    ]


def _future_closure_manifest_constraints() -> list[str]:
    return [
        "Future Star-Hub closure boundary manifest must remain governed and human-supervised.",
        "Future Star-Hub closure boundary manifest must not treat this audit as final Star-Hub closure.",
        "Future Star-Hub closure boundary manifest must not treat this audit as Star-Hub handoff authorization.",
        "Future Star-Hub closure boundary manifest must not treat this audit as Star-Hub scheduling authorization.",
        "Future Star-Hub closure boundary manifest must not treat this audit as dry-run execution authorization.",
        "Future Star-Hub closure boundary manifest must not write durable memory without a separate governed process.",
        "Future Star-Hub closure boundary manifest must not mutate Memory Graph without a separate governed process.",
        "Future Star-Hub closure boundary manifest must not create operation-ledger entries from this audit.",
        "Future Star-Hub closure boundary manifest must not call OpenClaw or GitHub APIs from this audit.",
    ]


def _next_stage_constraints() -> list[str]:
    return [
        "The only next allowed step is v2.27.0 Star-Hub closure boundary manifest.",
        "v2.26.0 is chain closure audit only; it must not create a Star-Hub closure boundary manifest.",
        "v2.26.0 must not claim final Star-Hub closure.",
        "v2.26.0 must not authorize Star-Hub scheduling, handoff, approval, dry-run execution, memory writing, Memory Graph mutation, operation-ledger creation, OpenClaw execution, or GitHub API actions.",
        "Mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, and 星源 self-evolution remain out of scope.",
        "Human Operator remains final authority for any future governed action.",
    ]


def _scope_boundaries() -> list[str]:
    return [
        "Civilization Core is the total system.",
        "Fifteen Memory Layers are the highest memory coordinate system.",
        "Subspace Memory System is the engineering carrier.",
        "Hermes, Codex CLI, OpenClaw, Terminal, and GitHub are components, not the core.",
        "This v2.26.0 step is limited to 星枢记忆 Star-Hub chain closure audit only, not final closure and not handoff.",
        "This audit does not enter mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, or 星源 self-evolution.",
    ]


def _risk_notes(sensitive_field_count: int) -> list[str]:
    notes = [
        "Star-Hub chain closure audit ready must not be treated as final closure, closure manifest creation, authorization, scheduling, handoff, approval, or dry-run execution.",
        "No dry-run performance, dry-run execution, durable memory write, Memory Graph mutation, operation-ledger entry, GitHub API write, merge, tag creation, approval, request creation, request submission, request execution, human decision record, handoff, scheduling, or OpenClaw execution is produced or authorized.",
        "Star-Hub scheduling, handoff, and final closure are not authorized or claimed.",
        "Civilization Core completion and Star-Dome final closure are not claimed.",
    ]
    if sensitive_field_count:
        notes.append("Sensitive fields were omitted from chain closure audit output.")
    return notes


def _required_human_actions(status: str, blocking_reasons: list[str]) -> list[str]:
    if status == "star_hub_chain_closure_audit_ready":
        return [
            "human_operator_must_review_star_hub_chain_closure_audit_before_any_later_closure_boundary_manifest",
            "human_operator_must_confirm_chain_closure_audit_ready_is_not_final_closure_or_handoff",
            "human_operator_must_use_separate_governed_process_for_any_real_approval_write_submission_execution_handoff_scheduling_dry_run_decision_or_closure_manifest",
        ]
    actions = [
        "repair_source_star_hub_scheduling_dry_run_execution_boundary_review_gate_before_chain_closure_audit_can_continue",
        "confirm_all_closure_write_approval_execution_handoff_scheduling_dry_run_completion_and_final_closure_flags_remain_false",
        "rerun_local_chain_closure_audit_after_blocking_reasons_are_resolved",
    ]
    if blocking_reasons:
        actions.append(
            "resolve_blocking_reasons_before_star_hub_chain_closure_audit_can_be_ready"
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
    "GOVERNED_STAR_HUB_CHAIN_CLOSURE_AUDIT_VERSION",
    "AUDITED_CHAIN_VERSIONS",
    "AUDITED_STAR_HUB_CHAIN_VERSIONS",
    "build_governed_star_hub_chain_closure_audit",
    "governed_star_hub_chain_closure_audit_to_json",
]
