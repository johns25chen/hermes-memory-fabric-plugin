"""Governed Star-Hub scheduling dry-run execution boundary review gate for v2.24 proposals."""

from __future__ import annotations

import json
from typing import Any, Mapping


GOVERNED_STAR_HUB_SCHEDULING_DRY_RUN_EXECUTION_BOUNDARY_REVIEW_GATE_VERSION = "2.25.0"
SOURCE_PROPOSAL_VERSION = "2.24.0"

SOURCE_PROPOSED_CHAIN_VERSIONS = [
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
]

REVIEWED_CHAIN_VERSIONS = [
    *SOURCE_PROPOSED_CHAIN_VERSIONS,
    "v2.24.0",
]

LAYER_MAPPING = {
    "primary_layer": "星枢记忆",
    "primary_layer_status": "scheduling dry-run execution boundary review gate only, not scheduling and not dry-run execution",
    "supporting_layers": ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"],
    "direction": "Star-Hub scheduling dry-run execution boundary proposal -> Star-Hub scheduling dry-run execution boundary review gate",
}

READY_NEXT_ALLOWED_STEP = "v2.26.0 Star-Hub chain closure audit"

REVIEW_GATE_FLAGS = {
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

SOURCE_REQUIRED_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "proposal_only": True,
    "dry_run_execution_boundary_proposal_only": True,
    "scheduling_dry_run_execution_boundary_proposal_only": True,
    "star_hub_dry_run_execution_boundary_only": True,
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

SOURCE_PROPOSED_BOUNDARY_REQUIRED_FLAGS = {
    "star_hub_dry_run_execution_boundary_proposed": True,
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
    "star_dome_final_closure_claimed": False,
}

UNSAFE_TRUE_FIELDS = {
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
    "star_hub_closure_claimed",
    "star_dome_final_closure_claimed",
}


def build_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate(
    proposal_report: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a local-only, non-authorizing Star-Hub dry-run execution review gate."""

    checks, blocking_reasons = _review_gate_checks(proposal_report)
    sensitive_field_count = _count_sensitive_keys(proposal_report)
    blocking_reasons = list(dict.fromkeys(blocking_reasons))
    status = (
        "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready"
        if not blocking_reasons
        else "blocked"
    )
    ready = status == "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready"

    return {
        "version": GOVERNED_STAR_HUB_SCHEDULING_DRY_RUN_EXECUTION_BOUNDARY_REVIEW_GATE_VERSION,
        "status": status,
        **REVIEW_GATE_FLAGS,
        "civilization_core_layer_mapping": dict(LAYER_MAPPING),
        "source_proposal_version": SOURCE_PROPOSAL_VERSION,
        "reviewed_chain_versions": list(REVIEWED_CHAIN_VERSIONS),
        "star_hub_scheduling_dry_run_execution_boundary_review_summary": _review_summary(ready),
        "review_gate_checks": checks,
        "source_proposal_summary": _source_proposal_summary(ready),
        "reviewed_star_hub_dry_run_execution_boundary": (
            _reviewed_star_hub_dry_run_execution_boundary(ready)
        ),
        "non_authorization_boundary": _non_authorization_boundary(),
        "preserved_governance_boundaries": _preserved_governance_boundaries(),
        "future_closure_audit_constraints": _future_closure_audit_constraints(),
        "next_stage_constraints": _next_stage_constraints(),
        "scope_boundaries": _scope_boundaries(),
        "risk_notes": _risk_notes(sensitive_field_count),
        "required_human_actions": _required_human_actions(status, blocking_reasons),
        "blocking_reasons": blocking_reasons,
        "next_allowed_step": (
            READY_NEXT_ALLOWED_STEP
            if ready
            else "resolve_v2_25_0_star_hub_scheduling_dry_run_execution_boundary_review_gate_blockers"
        ),
        "sensitive_field_count": sensitive_field_count,
        "sensitive_fields_omitted": sensitive_field_count > 0,
    }


def governed_star_hub_scheduling_dry_run_execution_boundary_review_gate_to_json(
    report: Mapping[str, Any],
) -> str:
    """Serialize a Star-Hub dry-run execution boundary review gate deterministically."""

    return json.dumps(dict(report), ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def _review_gate_checks(report: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    blocking_reasons: list[str] = []

    if not isinstance(report, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_proposal_report_mapping",
            False,
            "source_proposal_report_must_be_mapping",
        )
        return checks, blocking_reasons

    _add_check(
        checks,
        blocking_reasons,
        "source_proposal_version",
        report.get("version") == SOURCE_PROPOSAL_VERSION,
        "source_proposal_version_must_be_2_24_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_proposal_status_ready",
        report.get("status")
        == "star_hub_scheduling_dry_run_execution_boundary_proposal_ready",
        "source_proposal_status_must_be_star_hub_scheduling_dry_run_execution_boundary_proposal_ready",
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
        "source_must_not_claim_scheduling_handoff_approval_write_execution_or_dry_run_execution",
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
            == "scheduling dry-run execution boundary proposal only, not scheduling and not dry-run execution",
            "source_primary_layer_status_must_be_execution_boundary_proposal_only_not_scheduling_not_dry_run_execution",
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
        "source_proposed_chain_versions",
        report.get("proposed_chain_versions") == SOURCE_PROPOSED_CHAIN_VERSIONS,
        "source_proposed_chain_versions_must_exactly_match_v2_9_0_through_v2_23_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_next_allowed_step",
        report.get("next_allowed_step")
        == "v2.25.0 Star-Hub scheduling dry-run execution boundary review gate",
        "source_next_allowed_step_must_be_v2_25_0_star_hub_scheduling_dry_run_execution_boundary_review_gate",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_blocking_reasons_empty",
        report.get("blocking_reasons") == [],
        "source_blocking_reasons_must_be_empty",
    )

    proposed = report.get("proposed_star_hub_dry_run_execution_boundary")
    _add_check(
        checks,
        blocking_reasons,
        "source_proposed_star_hub_dry_run_execution_boundary_shape",
        isinstance(proposed, Mapping),
        "source_proposed_star_hub_dry_run_execution_boundary_must_be_mapping",
    )
    if isinstance(proposed, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_proposed_boundary_status",
            proposed.get("proposal_status")
            == "star_hub_scheduling_dry_run_execution_boundary_proposed_for_human_review_only",
            "source_proposed_boundary_status_must_be_human_review_only",
        )
        for key, expected in SOURCE_PROPOSED_BOUNDARY_REQUIRED_FLAGS.items():
            _add_check(
                checks,
                blocking_reasons,
                f"source_proposed_boundary_{key}",
                proposed.get(key) is expected,
                f"source_proposed_boundary_{key}_must_be_{str(expected).lower()}",
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
            "star_hub_scheduling_dry_run_execution_boundary_proposal_ready_is_star_hub_scheduling",
            "star_hub_scheduling_dry_run_execution_boundary_proposal_ready_is_dry_run_execution",
            "star_hub_scheduling_dry_run_execution_boundary_proposal_ready_is_star_hub_handoff",
            "star_hub_scheduling_dry_run_execution_boundary_proposal_ready_is_authorization",
            "star_hub_scheduling_dry_run_execution_boundary_proposal_ready_is_civilization_core_completion",
        ]:
            _add_check(
                checks,
                blocking_reasons,
                f"source_non_authorization_{key}",
                boundary.get(key) is False,
                f"source_non_authorization_{key}_must_be_false",
            )

    return checks, blocking_reasons


def _review_summary(ready: bool) -> dict[str, Any]:
    return {
        "review_status": (
            "ready_for_later_star_hub_chain_closure_audit" if ready else "blocked"
        ),
        "source_proposal_version": SOURCE_PROPOSAL_VERSION,
        "source_proposal_ready": ready,
        "future_star_hub_scheduling_dry_run_execution_boundary_reviewed_for_human_review_only": ready,
        "chain_structurally_ready_for_later_star_hub_chain_closure_audit": ready,
        "non_authorizing": True,
        "non_scheduling": True,
        "non_dry_run_execution": True,
        "non_handoff": True,
        "non_writing": True,
        "non_executing": True,
        "dry_run_execution_boundary_review_authorized": False,
        "dry_run_execution_boundary_authorized": False,
        "dry_run_execution_authorized": False,
        "dry_run_performed": False,
        "dry_run_executed": False,
        "star_hub_scheduling_authorized": False,
        "star_hub_scheduling_executed": False,
        "star_hub_handoff_authorized": False,
        "civilization_core_complete_claimed": False,
        "star_hub_closure_claimed": False,
        "only_permits_later_star_hub_chain_closure_audit": ready,
    }


def _source_proposal_summary(ready: bool) -> dict[str, Any]:
    return {
        "source_proposal_version": SOURCE_PROPOSAL_VERSION,
        "source_proposal_status": (
            "star_hub_scheduling_dry_run_execution_boundary_proposal_ready"
            if ready
            else "blocked"
        ),
        "source_chain_versions": list(SOURCE_PROPOSED_CHAIN_VERSIONS),
        "source_dry_run_execution_boundary_proposal_ready": ready,
        "source_proposal_authorized_dry_run_execution_boundary": False,
        "source_proposal_authorized_dry_run_execution": False,
        "source_proposal_authorized_scheduling": False,
        "source_proposal_authorized_handoff": False,
        "source_proposal_authorized_approval": False,
        "source_proposal_authorized_memory_write": False,
        "source_proposal_authorized_openclaw_execution": False,
        "source_proposal_claimed_civilization_core_completion": False,
    }


def _reviewed_star_hub_dry_run_execution_boundary(ready: bool) -> dict[str, Any]:
    status = (
        "star_hub_scheduling_dry_run_execution_boundary_reviewed_for_human_review_only"
        if ready
        else "blocked_no_star_hub_scheduling_dry_run_execution_boundary_review_gate_readiness_claim"
    )
    return {
        "review_status": status,
        "boundary_type": "star_hub_scheduling_dry_run_execution_boundary_review_gate",
        "source_proposal_version": SOURCE_PROPOSAL_VERSION,
        "star_hub_dry_run_execution_boundary_reviewed": ready,
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
        "reviewed_chain_versions": list(REVIEWED_CHAIN_VERSIONS),
        "dry_run_execution_review_gate_components": {
            "dry_run_execution_scope_review": "future_dry_run_execution_scope_reviewed_for_human_review_only",
            "dry_run_execution_authorization_review": "dry_run_execution_and_boundary_review_authorization_remain_false",
            "scheduler_scope_review": "star_hub_scheduling_remains_unauthorized_and_unperformed",
            "no_real_execution_review": "no_dry_run_is_performed_or_executed_in_this_review_gate",
            "memory_write_boundary_review": "durable_memory_writes_remain_unauthorized",
            "operation_ledger_boundary_review": "operation_ledger_creation_remains_unauthorized",
            "openclaw_execution_boundary_review": "openclaw_execution_remains_unauthorized",
            "human_operator_boundary_review": "human_operator_remains_final_authority",
            "approval_boundary_review": "approval_requests_and_approvals_remain_unauthorized",
            "evidence_lineage_boundary_review": "use_sanitized_proposal_lineage_only",
            "fifteen_memory_layers_boundary_review": "fifteen_memory_layers_remain_highest_memory_coordinate_system",
        },
        "next_allowed_step": READY_NEXT_ALLOWED_STEP,
        "non_authorization_notice": (
            "The future Star-Hub scheduling dry-run execution boundary is reviewed for human review only and the chain is structurally ready for a later Star-Hub chain closure audit; Star-Hub scheduling, dry-run performance, dry-run execution, dry-run execution authorization, Star-Hub handoff, durable memory writing, Memory Graph mutation, operation-ledger creation, OpenClaw execution, approval, human decision recording, Civilization Core completion, Star-Hub closure, and Star-Dome final closure remain unauthorized, unperformed, and unclaimed."
        ),
    }


def _non_authorization_boundary() -> dict[str, Any]:
    return {
        "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready_is_authorization": False,
        "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready_is_star_hub_scheduling": False,
        "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready_is_dry_run_execution": False,
        "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready_is_star_hub_handoff": False,
        "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready_is_approval": False,
        "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready_is_human_decision": False,
        "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready_is_real_approval_request": False,
        "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready_is_request_submission": False,
        "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready_is_request_execution": False,
        "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready_is_memory_write_permission": False,
        "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready_is_memory_graph_mutation_permission": False,
        "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready_is_operation_ledger_creation": False,
        "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready_is_openclaw_execution_permission": False,
        "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready_is_civilization_core_completion": False,
        "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready_is_star_hub_closure": False,
        "only_permits_later_star_hub_chain_closure_audit": True,
        "human_operator_remains_final_authority": True,
    }


def _preserved_governance_boundaries() -> list[str]:
    return [
        "Star-Hub scheduling dry-run execution boundary review gate ready is not authorization.",
        "Star-Hub scheduling dry-run execution boundary review gate ready is not scheduling.",
        "Star-Hub scheduling dry-run execution boundary review gate ready is not dry-run execution.",
        "Star-Hub scheduling dry-run execution boundary review gate ready is not handoff.",
        "Star-Hub scheduling dry-run execution boundary review gate ready is not approval.",
        "Star-Hub scheduling dry-run execution boundary review gate ready is not a real human decision.",
        "Star-Hub scheduling dry-run execution boundary review gate ready is not a real approval request.",
        "Star-Hub scheduling dry-run execution boundary review gate ready is not approval request submission.",
        "Star-Hub scheduling dry-run execution boundary review gate ready is not approval request execution.",
        "Star-Hub scheduling dry-run execution boundary review gate ready is not durable memory write permission.",
        "Star-Hub scheduling dry-run execution boundary review gate ready is not Memory Graph mutation permission.",
        "Star-Hub scheduling dry-run execution boundary review gate ready is not operation-ledger creation.",
        "Star-Hub scheduling dry-run execution boundary review gate ready is not OpenClaw execution permission.",
        "Star-Hub scheduling dry-run execution boundary review gate ready is not Civilization Core completion.",
        "Star-Hub scheduling dry-run execution boundary review gate ready is not Star-Hub closure.",
        "Star-Hub scheduling dry-run execution boundary review gate ready only permits a later Star-Hub chain closure audit.",
        "Human Operator remains final authority.",
    ]


def _future_closure_audit_constraints() -> list[str]:
    return [
        "Future Star-Hub chain closure audit must remain governed and human-supervised.",
        "Future Star-Hub chain closure audit must not treat this review gate as scheduling authorization.",
        "Future Star-Hub chain closure audit must not treat this review gate as dry-run execution authorization.",
        "Future Star-Hub chain closure audit must not treat this review gate as Star-Hub handoff authorization.",
        "Future Star-Hub chain closure audit must not write durable memory without a separate governed process.",
        "Future Star-Hub chain closure audit must not mutate Memory Graph without a separate governed process.",
        "Future Star-Hub chain closure audit must not create operation-ledger entries from this review gate.",
        "Future Star-Hub chain closure audit must not call OpenClaw or GitHub APIs from this review gate.",
        "Future Star-Hub chain closure audit must preserve the Fifteen Memory Layers as the highest coordinate system.",
    ]


def _next_stage_constraints() -> list[str]:
    return [
        "The only next allowed step is v2.26.0 Star-Hub chain closure audit.",
        "v2.25.0 reviews a dry-run execution boundary only; it must not schedule anything.",
        "v2.25.0 must not perform or execute a dry-run.",
        "v2.25.0 must not authorize dry-run execution.",
        "v2.25.0 must not authorize Star-Hub scheduling or handoff.",
        "Star-Hub closure remains unclaimed.",
        "Mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, and 星源 self-evolution remain out of scope.",
        "Human Operator remains final authority for any future governed action.",
    ]


def _scope_boundaries() -> list[str]:
    return [
        "Civilization Core is the total system.",
        "Fifteen Memory Layers are the highest memory coordinate system.",
        "Subspace Memory System is the engineering carrier.",
        "Hermes, Codex CLI, OpenClaw, Terminal, and GitHub are components, not the core.",
        "This v2.25.0 step is limited to 星枢记忆 scheduling dry-run execution boundary review gate only, not scheduling and not dry-run execution.",
        "This review gate does not enter mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, or 星源 self-evolution.",
    ]


def _risk_notes(sensitive_field_count: int) -> list[str]:
    notes = [
        "Scheduling dry-run execution boundary review gate ready must not be treated as authorization.",
        "No dry-run performance, dry-run execution, durable memory write, Memory Graph mutation, operation-ledger entry, GitHub API write, merge, tag creation, approval, request creation, request submission, request execution, human decision record, handoff, scheduling, or OpenClaw execution is produced or authorized.",
        "Star-Hub scheduling, handoff, and closure are not authorized or claimed.",
        "Civilization Core completion and Star-Dome final closure are not claimed.",
    ]
    if sensitive_field_count:
        notes.append("Sensitive fields were omitted from review gate output.")
    return notes


def _required_human_actions(status: str, blocking_reasons: list[str]) -> list[str]:
    if status == "star_hub_scheduling_dry_run_execution_boundary_review_gate_ready":
        return [
            "human_operator_must_review_dry_run_execution_boundary_review_gate_before_any_later_chain_closure_audit",
            "human_operator_must_confirm_execution_boundary_review_gate_ready_is_not_authorization",
            "human_operator_must_use_separate_governed_process_for_any_real_approval_write_submission_execution_handoff_scheduling_dry_run_or_decision",
        ]
    actions = [
        "repair_source_star_hub_scheduling_dry_run_execution_boundary_proposal_before_review_gate_can_continue",
        "confirm_all_write_approval_execution_handoff_scheduling_dry_run_completion_and_final_closure_flags_remain_false",
        "rerun_local_dry_run_execution_boundary_review_gate_after_blocking_reasons_are_resolved",
    ]
    if blocking_reasons:
        actions.append(
            "resolve_blocking_reasons_before_dry_run_execution_boundary_review_gate_can_be_ready"
        )
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


def _unsafe_true_fields(value: Any) -> list[str]:
    fields: list[str] = []
    if isinstance(value, Mapping):
        for key, inner in value.items():
            key_text = str(key)
            if key_text in UNSAFE_TRUE_FIELDS and inner is True:
                fields.append(key_text)
            fields.extend(_unsafe_true_fields(inner))
    elif isinstance(value, list):
        for item in value:
            fields.extend(_unsafe_true_fields(item))
    return fields


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
    "GOVERNED_STAR_HUB_SCHEDULING_DRY_RUN_EXECUTION_BOUNDARY_REVIEW_GATE_VERSION",
    "build_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate",
    "governed_star_hub_scheduling_dry_run_execution_boundary_review_gate_to_json",
]
