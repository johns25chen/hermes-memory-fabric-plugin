"""Governed Star-Law design boundary proposal for v2.28 preflight reports."""

from __future__ import annotations

import json
from typing import Any, Mapping


GOVERNED_STAR_LAW_DESIGN_BOUNDARY_PROPOSAL_VERSION = "2.29.0"
SOURCE_PREFLIGHT_VERSION = "2.28.0"

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

SOURCE_ANALYZED_STAR_HUB_CHAIN_VERSIONS = [
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

PROPOSED_CHAIN_VERSIONS = [
    *SOURCE_ANALYZED_CHAIN_VERSIONS,
    "v2.28.0",
]

PROPOSED_STAR_HUB_CHAIN_VERSIONS = [
    *SOURCE_ANALYZED_STAR_HUB_CHAIN_VERSIONS,
    "v2.28.0",
]

LAYER_MAPPING = {
    "primary_layer": "星律记忆",
    "primary_layer_status": "Star-Law design boundary proposal only, not rule activation and not rule enforcement",
    "source_layer": "星律记忆",
    "source_layer_status": "Star-Law preflight boundary analysis complete for human review only",
    "supporting_layers": ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"],
    "direction": "Star-Law preflight boundary analysis -> Star-Law design boundary proposal",
}

READY_NEXT_ALLOWED_STEP = "v2.30.0 Star-Law design boundary review gate"

PROPOSAL_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "proposal_only": True,
    "design_boundary_proposal_only": True,
    "star_law_design_boundary_proposal_only": True,
    "star_law_self_enforcing_law_created": False,
    "star_law_self_enforcing_law_active": False,
    "star_law_rules_created": False,
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

SOURCE_PREFLIGHT_BOUNDARY_REQUIRED_FLAGS = {
    "star_law_preflight_boundary_analyzed": True,
    "star_law_design_boundary_proposal_ready_for_human_review_only": True,
    "source_star_hub_boundary_manifest_valid": True,
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
}

UNSAFE_TRUE_FIELDS = {
    "star_law_self_enforcing_law_created",
    "star_law_self_enforcing_law_active",
    "star_law_rules_created",
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
    "scheduling_authorized",
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
    "approval_request_executed",
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


def build_governed_star_law_design_boundary_proposal(
    preflight_report: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a local-only, non-authorizing Star-Law design boundary proposal."""

    checks, blocking_reasons = _proposal_checks(preflight_report)
    sensitive_field_count = _count_sensitive_keys(preflight_report)
    blocking_reasons = list(dict.fromkeys(blocking_reasons))
    status = (
        "star_law_design_boundary_proposal_ready"
        if not blocking_reasons
        else "blocked"
    )
    ready = status == "star_law_design_boundary_proposal_ready"

    return {
        "version": GOVERNED_STAR_LAW_DESIGN_BOUNDARY_PROPOSAL_VERSION,
        "status": status,
        **PROPOSAL_FLAGS,
        "civilization_core_layer_mapping": dict(LAYER_MAPPING),
        "source_preflight_version": SOURCE_PREFLIGHT_VERSION,
        "proposed_chain_versions": list(PROPOSED_CHAIN_VERSIONS),
        "proposed_star_hub_chain_versions": list(PROPOSED_STAR_HUB_CHAIN_VERSIONS),
        "star_law_design_boundary_proposal_summary": _proposal_summary(ready),
        "proposal_checks": checks,
        "source_preflight_summary": _source_preflight_summary(ready),
        "star_law_design_boundary_proposal": _star_law_design_boundary_proposal(ready),
        "proposed_star_law_design_boundaries": _proposed_star_law_design_boundaries(
            ready
        ),
        "non_authorization_boundary": _non_authorization_boundary(),
        "preserved_governance_boundaries": _preserved_governance_boundaries(),
        "future_star_law_review_gate_constraints": _future_star_law_review_gate_constraints(),
        "next_stage_constraints": _next_stage_constraints(),
        "scope_boundaries": _scope_boundaries(),
        "risk_notes": _risk_notes(sensitive_field_count),
        "required_human_actions": _required_human_actions(status, blocking_reasons),
        "blocking_reasons": blocking_reasons,
        "next_allowed_step": (
            READY_NEXT_ALLOWED_STEP
            if ready
            else "resolve_v2_29_0_star_law_design_boundary_proposal_blockers"
        ),
        "sensitive_field_count": sensitive_field_count,
        "sensitive_fields_omitted": sensitive_field_count > 0,
    }


def governed_star_law_design_boundary_proposal_to_json(
    report: Mapping[str, Any],
) -> str:
    """Serialize a Star-Law design boundary proposal deterministically."""

    return json.dumps(dict(report), ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def _proposal_checks(
    report: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[str]]:
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
        "source_preflight_version_must_be_2_28_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_preflight_status_ready",
        report.get("status") == "star_law_preflight_boundary_analysis_ready",
        "source_preflight_status_must_be_star_law_preflight_boundary_analysis_ready",
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
        "source_must_not_claim_star_law_activation_rule_creation_rule_enforcement_autonomous_execution_handoff_scheduling_approval_write_execution_dry_run_or_civilization_core_completion",
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
            mapping.get("primary_layer") == "星律记忆",
            "source_primary_layer_must_be_star_law_memory",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_primary_layer_status",
            mapping.get("primary_layer_status")
            == "Star-Law preflight boundary analysis only, not self-enforcing law and not autonomous execution",
            "source_primary_layer_status_must_be_preflight_boundary_analysis_only_not_self_enforcing_law_not_autonomous_execution",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_source_layer",
            mapping.get("source_layer") == "星枢记忆",
            "source_source_layer_must_be_star_hub_memory",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_source_layer_status",
            mapping.get("source_layer_status")
            == "Star-Hub staged closure boundary manifest complete for human review only",
            "source_source_layer_status_must_be_star_hub_closure_boundary_manifest_complete_for_human_review_only",
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
        "source_analyzed_chain_versions_must_exactly_match_v2_9_0_through_v2_27_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_analyzed_star_hub_chain_versions",
        report.get("analyzed_star_hub_chain_versions")
        == SOURCE_ANALYZED_STAR_HUB_CHAIN_VERSIONS,
        "source_analyzed_star_hub_chain_versions_must_exactly_match_v2_19_0_through_v2_27_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_next_allowed_step",
        report.get("next_allowed_step")
        == "v2.29.0 Star-Law design boundary proposal",
        "source_next_allowed_step_must_be_v2_29_0_star_law_design_boundary_proposal",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_blocking_reasons_empty",
        report.get("blocking_reasons") == [],
        "source_blocking_reasons_must_be_empty",
    )

    preflight_boundary = report.get("star_law_preflight_boundary")
    _add_check(
        checks,
        blocking_reasons,
        "source_star_law_preflight_boundary_shape",
        isinstance(preflight_boundary, Mapping),
        "source_star_law_preflight_boundary_must_be_mapping",
    )
    if isinstance(preflight_boundary, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_preflight_boundary_status",
            preflight_boundary.get("preflight_status")
            == "star_law_preflight_boundary_analyzed_for_human_review_only",
            "source_preflight_boundary_status_must_be_human_review_only",
        )
        for key, expected in SOURCE_PREFLIGHT_BOUNDARY_REQUIRED_FLAGS.items():
            _add_check(
                checks,
                blocking_reasons,
                f"source_preflight_boundary_{key}",
                preflight_boundary.get(key) is expected,
                f"source_preflight_boundary_{key}_must_be_{str(expected).lower()}",
            )

    return checks, blocking_reasons


def _proposal_summary(ready: bool) -> dict[str, Any]:
    return {
        "proposal_status": (
            "star_law_design_boundary_proposed_for_human_review_only"
            if ready
            else "blocked"
        ),
        "source_preflight_version": SOURCE_PREFLIGHT_VERSION,
        "source_star_law_preflight_boundary_valid": ready,
        "star_law_design_boundary_review_gate_ready_for_human_review_only": ready,
        "star_law_self_enforcing_law_created": False,
        "star_law_rules_created": False,
        "star_law_rules_activated": False,
        "star_law_rules_enforced": False,
        "autonomous_governance_created": False,
        "autonomous_execution_authorized": False,
        "civilization_core_complete_claimed": False,
        "only_permits_later_star_law_design_boundary_review_gate": ready,
    }


def _source_preflight_summary(ready: bool) -> dict[str, Any]:
    return {
        "source_preflight_version": SOURCE_PREFLIGHT_VERSION,
        "source_preflight_status": (
            "star_law_preflight_boundary_analysis_ready" if ready else "blocked"
        ),
        "source_preflight_non_authorizing": True,
        "source_preflight_star_law_design_boundary_proposal_ready_for_human_review_only": ready,
        "source_preflight_authorized_rule_creation": False,
        "source_preflight_authorized_rule_activation": False,
        "source_preflight_authorized_rule_enforcement": False,
        "source_preflight_authorized_autonomous_execution": False,
        "source_preflight_authorized_handoff": False,
        "source_preflight_authorized_scheduling": False,
        "source_preflight_authorized_dry_run_execution": False,
        "source_preflight_authorized_approval": False,
        "source_preflight_authorized_memory_write": False,
        "source_preflight_authorized_openclaw_execution": False,
        "source_preflight_claimed_civilization_core_completion": False,
        "source_preflight_claimed_next_layer_entry": False,
    }


def _star_law_design_boundary_proposal(ready: bool) -> dict[str, Any]:
    return {
        "proposal_status": (
            "star_law_design_boundary_proposed_for_human_review_only"
            if ready
            else "blocked_no_star_law_design_boundary_readiness_claim"
        ),
        "boundary_type": "star_law_design_boundary_proposal",
        "source_preflight_version": SOURCE_PREFLIGHT_VERSION,
        "star_law_design_boundary_proposed": ready,
        "star_law_design_boundary_review_gate_ready_for_human_review_only": ready,
        "source_star_law_preflight_valid": ready,
        "star_law_self_enforcing_law_created": False,
        "star_law_self_enforcing_law_active": False,
        "star_law_rules_created": False,
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
        "proposed_chain_versions": list(PROPOSED_CHAIN_VERSIONS),
        "proposed_star_hub_chain_versions": list(PROPOSED_STAR_HUB_CHAIN_VERSIONS),
        "star_law_design_boundary_components": {
            "source_star_law_preflight_boundary_analysis": "v2.28.0_structural_source_boundary_validated_for_human_review_only",
            "candidate_rule_taxonomy_boundary": "candidate_categories_described_for_later_review_only_without_rule_creation",
            "rule_activation_non_authorization_boundary": "rule_activation_permission_not_created",
            "rule_enforcement_non_authorization_boundary": "rule_enforcement_permission_not_created",
            "autonomous_governance_non_creation_boundary": "autonomous_governance_not_created",
            "autonomous_execution_non_authorization_boundary": "autonomous_execution_permission_not_created",
            "memory_write_non_authorization_boundary": "durable_memory_write_permission_not_created",
            "memory_graph_mutation_non_authorization_boundary": "memory_graph_mutation_permission_not_created",
            "operation_ledger_non_creation_boundary": "operation_ledger_entry_creation_permission_not_created",
            "openclaw_execution_non_authorization_boundary": "openclaw_execution_permission_not_created",
            "approval_non_authorization_boundary": "approval_request_and_approval_permission_not_created",
            "human_operator_final_authority_boundary": "human_operator_remains_final_authority",
            "fifteen_memory_layers_boundary": "fifteen_memory_layers_remain_highest_memory_coordinate_system",
        },
        "next_allowed_step": READY_NEXT_ALLOWED_STEP,
        "non_authorization_notice": (
            "The Star-Law design boundary has been proposed for human review only. "
            "It describes candidate taxonomy and control boundaries for a later governed review gate. "
            "It performs no rule creation, rule activation, rule enforcement, autonomous governance creation, autonomous execution authorization, self-executing policy creation, approval, handoff, scheduling, dry-run execution, durable memory write, Memory Graph mutation, operation-ledger entry creation, OpenClaw execution, GitHub API action, human decision record, Civilization Core completion claim, 星魂 continuity start, 星宙 evolution start, or 星源 self-evolution start."
        ),
    }


def _proposed_star_law_design_boundaries(ready: bool) -> dict[str, Any]:
    return {
        "candidate_rule_taxonomy_boundary": {
            "proposal_only": True,
            "description": "Candidate categories may be described for later human review: evidence lineage, conflict handling, write gating, routing constraints, escalation triggers, and audit checks.",
            "rule_creation_performed": False,
            "rule_activation_performed": False,
            "rule_enforcement_performed": False,
        },
        "human_operator_control_boundary": {
            "proposal_only": True,
            "description": "Human Operator retains final authority over any later review, approval, execution, handoff, scheduling, memory write, graph mutation, or next-layer work.",
            "autonomous_governance_created": False,
            "autonomous_execution_authorized": False,
        },
        "non_authorization_boundary": {
            "proposal_only": True,
            "description": "This boundary grants no permission for execution, approval, handoff, scheduling, write, graph mutation, ledger entry creation, OpenClaw, GitHub API, or dry-run execution.",
            "authorization_granted": False,
            "approval_granted": False,
        },
        "evidence_lineage_boundary": {
            "proposal_only": True,
            "description": "Future rule candidates would require source preflight lineage, explicit scope, and separate review-gate evidence before any governed action could be considered.",
            "real_human_decision_recorded": False,
        },
        "memory_write_boundary": {
            "proposal_only": True,
            "description": "Durable memory write paths remain out of scope for this design boundary proposal.",
            "durable_memory_write_authorized": False,
        },
        "memory_graph_boundary": {
            "proposal_only": True,
            "description": "Memory Graph mutation paths remain out of scope for this design boundary proposal.",
            "memory_graph_mutation_authorized": False,
        },
        "operation_ledger_boundary": {
            "proposal_only": True,
            "description": "Operation-ledger entry creation remains out of scope for this design boundary proposal.",
            "operation_ledger_creation_authorized": False,
        },
        "openclaw_boundary": {
            "proposal_only": True,
            "description": "OpenClaw execution remains out of scope for this design boundary proposal.",
            "openclaw_execution_authorized": False,
        },
        "approval_boundary": {
            "proposal_only": True,
            "description": "Approval request creation, submission, execution, and grant remain out of scope for this design boundary proposal.",
            "approval_request_created": False,
            "approval_request_submitted": False,
            "approval_request_authorized": False,
            "approval_granted": False,
        },
        "auditability_boundary": {
            "proposal_only": True,
            "description": "Auditability is limited to deterministic local report structure and expected chain-version traceability.",
            "would_create_operation_ledger_entry": False,
        },
        "future_review_gate_boundary": {
            "proposal_only": True,
            "description": (
                "The only later step allowed by this report is v2.30.0 Star-Law design boundary review gate."
                if ready
                else "A later Star-Law design boundary review gate is unavailable until blocking reasons are resolved."
            ),
            "review_gate_ready_for_human_review_only": ready,
            "review_gate_authorized": False,
        },
    }


def _non_authorization_boundary() -> dict[str, Any]:
    return {
        "star_law_design_boundary_proposal_ready_is_self_enforcing_memory_law": False,
        "star_law_design_boundary_proposal_ready_is_rule_creation": False,
        "star_law_design_boundary_proposal_ready_is_rule_activation": False,
        "star_law_design_boundary_proposal_ready_is_rule_enforcement": False,
        "star_law_design_boundary_proposal_ready_is_autonomous_governance": False,
        "star_law_design_boundary_proposal_ready_is_autonomous_execution": False,
        "star_law_design_boundary_proposal_ready_is_handoff": False,
        "star_law_design_boundary_proposal_ready_is_authorization": False,
        "star_law_design_boundary_proposal_ready_is_scheduling": False,
        "star_law_design_boundary_proposal_ready_is_dry_run_execution": False,
        "star_law_design_boundary_proposal_ready_is_approval": False,
        "star_law_design_boundary_proposal_ready_is_human_decision": False,
        "star_law_design_boundary_proposal_ready_is_memory_write_permission": False,
        "star_law_design_boundary_proposal_ready_is_memory_graph_mutation_permission": False,
        "star_law_design_boundary_proposal_ready_is_operation_ledger_creation": False,
        "star_law_design_boundary_proposal_ready_is_openclaw_execution_permission": False,
        "star_law_design_boundary_proposal_ready_is_civilization_core_completion": False,
        "only_permits_later_star_law_design_boundary_review_gate": True,
        "human_operator_remains_final_authority": True,
    }


def _preserved_governance_boundaries() -> list[str]:
    return [
        "Star-Law design boundary proposal ready is not self-enforcing memory law.",
        "Star-Law design boundary proposal ready is not rule creation.",
        "Star-Law design boundary proposal ready is not rule activation.",
        "Star-Law design boundary proposal ready is not rule enforcement.",
        "Star-Law design boundary proposal ready is not autonomous governance.",
        "Star-Law design boundary proposal ready is not autonomous execution.",
        "Star-Law design boundary proposal ready is not handoff.",
        "Star-Law design boundary proposal ready is not authorization.",
        "Star-Law design boundary proposal ready is not scheduling.",
        "Star-Law design boundary proposal ready is not dry-run execution.",
        "Star-Law design boundary proposal ready is not approval.",
        "Star-Law design boundary proposal ready is not a real human decision.",
        "Star-Law design boundary proposal ready is not durable memory write permission.",
        "Star-Law design boundary proposal ready is not Memory Graph mutation permission.",
        "Star-Law design boundary proposal ready is not operation-ledger creation.",
        "Star-Law design boundary proposal ready is not OpenClaw execution permission.",
        "Star-Law design boundary proposal ready is not Civilization Core completion.",
        "Star-Law design boundary proposal ready only permits a later Star-Law design boundary review gate.",
        "Human Operator remains final authority.",
    ]


def _future_star_law_review_gate_constraints() -> list[str]:
    return [
        "A later Star-Law design boundary review gate may inspect this proposal through a separate governed process.",
        "A later review gate must not be treated as automatic rule creation, activation, enforcement, approval, handoff, scheduling, memory writing, Memory Graph mutation, operation-ledger creation, OpenClaw execution, GitHub API action, dry-run execution, or Civilization Core completion.",
        "Any future rule taxonomy must remain inactive until a separate Human Operator governed process explicitly authorizes an applicable later stage.",
        "Human Operator remains final authority for all future Star-Law governance decisions.",
    ]


def _next_stage_constraints() -> list[str]:
    return [
        "The only next allowed step is v2.30.0 Star-Law design boundary review gate.",
        "v2.29.0 is Star-Law design boundary proposal only, not rule activation and not rule enforcement.",
        "v2.29.0 must not authorize Star-Hub handoff, scheduling, approval, dry-run execution, memory writing, Memory Graph mutation, operation-ledger creation, OpenClaw execution, or GitHub API actions.",
        "Mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, and 星源 self-evolution remain out of scope.",
        "Human Operator remains final authority for any future governed action.",
    ]


def _scope_boundaries() -> list[str]:
    return [
        "Civilization Core is the total system.",
        "Fifteen Memory Layers are the highest memory coordinate system.",
        "Subspace Memory System is the engineering carrier.",
        "Hermes, Codex CLI, OpenClaw, Terminal, and GitHub are components, not the core.",
        "This v2.29.0 step is limited to 星律记忆 Star-Law design boundary proposal only.",
        "This proposal does not enter mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, or 星源 self-evolution.",
    ]


def _risk_notes(sensitive_field_count: int) -> list[str]:
    notes = [
        "Star-Law design boundary proposal ready must not be treated as self-enforcing memory law, rule creation, rule activation, rule enforcement, autonomous governance, autonomous execution, handoff, authorization, scheduling, approval, dry-run execution, or Civilization Core completion.",
        "No durable memory write, Memory Graph mutation, operation-ledger entry, GitHub API write, merge, tag creation, approval, request creation, request submission, request execution, human decision record, handoff, scheduling, dry-run performance, dry-run execution, or OpenClaw execution is produced or authorized.",
        "Mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, and 星源 self-evolution are not started.",
    ]
    if sensitive_field_count:
        notes.append("Sensitive fields were omitted from design boundary proposal output.")
    return notes


def _required_human_actions(status: str, blocking_reasons: list[str]) -> list[str]:
    if status == "star_law_design_boundary_proposal_ready":
        return [
            "human_operator_must_review_star_law_design_boundary_proposal_before_any_later_star_law_design_boundary_review_gate",
            "human_operator_must_confirm_star_law_design_boundary_proposal_ready_is_not_self_enforcing_law_rule_creation_rule_activation_rule_enforcement_autonomous_execution_handoff_authorization_scheduling_approval_write_execution_or_civilization_core_completion",
            "human_operator_must_use_separate_governed_process_for_any_future_star_law_review_gate_rule_activation_rule_enforcement_real_approval_write_submission_execution_handoff_scheduling_dry_run_decision_or_next_layer_work",
        ]
    actions = [
        "repair_source_star_law_preflight_boundary_analysis_before_star_law_design_boundary_proposal_can_continue",
        "confirm_all_star_law_rule_creation_rule_activation_rule_enforcement_autonomous_execution_handoff_scheduling_dry_run_write_approval_execution_next_layer_and_civilization_core_completion_flags_remain_false",
        "rerun_local_star_law_design_boundary_proposal_after_blocking_reasons_are_resolved",
    ]
    if blocking_reasons:
        actions.append(
            "resolve_blocking_reasons_before_star_law_design_boundary_proposal_can_be_ready"
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
    "GOVERNED_STAR_LAW_DESIGN_BOUNDARY_PROPOSAL_VERSION",
    "PROPOSED_CHAIN_VERSIONS",
    "PROPOSED_STAR_HUB_CHAIN_VERSIONS",
    "build_governed_star_law_design_boundary_proposal",
    "governed_star_law_design_boundary_proposal_to_json",
]
