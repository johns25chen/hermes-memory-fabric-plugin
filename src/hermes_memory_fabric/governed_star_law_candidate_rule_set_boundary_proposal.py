"""Governed Star-Law candidate rule-set boundary proposal for v2.30 gates."""

from __future__ import annotations

import json
from typing import Any, Mapping


GOVERNED_STAR_LAW_CANDIDATE_RULE_SET_BOUNDARY_PROPOSAL_VERSION = "2.31.0"
SOURCE_REVIEW_GATE_VERSION = "2.30.0"

SOURCE_REVIEWED_CHAIN_VERSIONS = [
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
    "v2.28.0",
    "v2.29.0",
]

SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS = [
    "v2.19.0",
    "v2.20.0",
    "v2.21.0",
    "v2.22.0",
    "v2.23.0",
    "v2.24.0",
    "v2.25.0",
    "v2.26.0",
    "v2.27.0",
    "v2.28.0",
    "v2.29.0",
]

PROPOSED_CHAIN_VERSIONS = [
    *SOURCE_REVIEWED_CHAIN_VERSIONS,
    "v2.30.0",
]

PROPOSED_STAR_HUB_CHAIN_VERSIONS = [
    *SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS,
    "v2.30.0",
]

LAYER_MAPPING = {
    "primary_layer": "星律记忆",
    "primary_layer_status": "Star-Law candidate rule-set boundary proposal only, not rule creation, not rule activation, and not rule enforcement",
    "source_layer": "星律记忆",
    "source_layer_status": "Star-Law design boundary review gate complete for human review only",
    "supporting_layers": ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"],
    "direction": "Star-Law design boundary review gate -> Star-Law candidate rule-set boundary proposal",
}

READY_NEXT_ALLOWED_STEP = "v2.32.0 Star-Law candidate rule-set boundary review gate"
BLOCKED_NEXT_ALLOWED_STEP = (
    "resolve_v2_31_0_star_law_candidate_rule_set_boundary_proposal_blockers"
)

PROPOSAL_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "proposal_only": True,
    "candidate_rule_set_boundary_proposal_only": True,
    "star_law_candidate_rule_set_boundary_proposal_only": True,
    "star_law_candidate_rules_created": False,
    "star_law_rules_created": False,
    "star_law_rules_activated": False,
    "star_law_rules_enforced": False,
    "star_law_self_enforcing_law_created": False,
    "star_law_self_enforcing_law_active": False,
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
    "review_gate_only": True,
    "design_boundary_review_gate_only": True,
    "star_law_design_boundary_review_gate_only": True,
    "star_law_design_boundary_review_ready": True,
    "star_law_candidate_rule_set_boundary_proposal_ready_for_human_review_only": True,
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

SOURCE_REVIEW_GATE_BOUNDARY_REQUIRED_FLAGS = {
    "star_law_design_boundary_reviewed": True,
    "star_law_design_boundary_structurally_review_ready": True,
    "candidate_rule_set_boundary_proposal_ready_for_human_review_only": True,
    "source_star_law_design_boundary_proposal_valid": True,
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
}

UNSAFE_TRUE_FIELDS = {
    "star_law_candidate_rules_created",
    "star_law_candidate_rules_activated",
    "star_law_candidate_rules_enforced",
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
    "candidate_rule_set_boundary_proposal_authorized",
    "candidate_rule_set_boundary_review_gate_authorized",
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

BOUNDARY_ALLOWED_TRUE_KEYS = {
    "review_only",
}

FORBIDDEN_BOUNDARY_CLAIMS = (
    "star-law rules are created",
    "star-law rules are active",
    "star-law rules are enforced",
    "rules are created",
    "rules are active",
    "rules are enforced",
    "rules are authorized",
    "rule creation is authorized",
    "rule activation is authorized",
    "rule enforcement is authorized",
    "self-executing policy active",
    "self-executing policy is active",
    "autonomous governance is created",
    "autonomous execution is authorized",
    "durable memory writing is allowed",
    "memory graph mutation is allowed",
    "operation-ledger creation is allowed",
    "openclaw execution is allowed",
    "approval is granted",
    "real human decision has been recorded",
    "civilization core is complete",
    "mature 星律 self-enforcing memory law has started",
    "星魂 continuity has started",
    "星宙 evolution has started",
    "星源 self-evolution has started",
)

PROPOSED_CANDIDATE_RULE_SET_BOUNDARY_KEYS = {
    "candidate_rule_taxonomy_boundary",
    "candidate_rule_eligibility_boundary",
    "candidate_rule_input_scope_boundary",
    "candidate_rule_output_scope_boundary",
    "candidate_rule_non_creation_boundary",
    "candidate_rule_non_activation_boundary",
    "candidate_rule_non_enforcement_boundary",
    "candidate_rule_evidence_lineage_boundary",
    "human_operator_control_boundary",
    "non_authorization_boundary",
    "memory_write_boundary",
    "memory_graph_boundary",
    "operation_ledger_boundary",
    "openclaw_boundary",
    "approval_boundary",
    "auditability_boundary",
    "future_review_gate_boundary",
}


def build_governed_star_law_candidate_rule_set_boundary_proposal(
    review_gate_report: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a local-only, non-authorizing candidate rule-set proposal."""

    checks, blocking_reasons = _proposal_checks(review_gate_report)
    sensitive_field_count = _count_sensitive_keys(review_gate_report)
    blocking_reasons = list(dict.fromkeys(blocking_reasons))
    status = (
        "star_law_candidate_rule_set_boundary_proposal_ready"
        if not blocking_reasons
        else "blocked"
    )
    ready = status == "star_law_candidate_rule_set_boundary_proposal_ready"

    return {
        "version": GOVERNED_STAR_LAW_CANDIDATE_RULE_SET_BOUNDARY_PROPOSAL_VERSION,
        "status": status,
        **PROPOSAL_FLAGS,
        "candidate_rule_set_boundary_proposed_for_human_review_only": ready,
        "candidate_rule_set_review_gate_ready_for_human_review_only": ready,
        "civilization_core_layer_mapping": dict(LAYER_MAPPING),
        "source_review_gate_version": SOURCE_REVIEW_GATE_VERSION,
        "proposed_chain_versions": list(PROPOSED_CHAIN_VERSIONS),
        "proposed_star_hub_chain_versions": list(PROPOSED_STAR_HUB_CHAIN_VERSIONS),
        "star_law_candidate_rule_set_boundary_proposal_summary": (
            _proposal_summary(ready)
        ),
        "proposal_checks": checks,
        "source_review_gate_summary": _source_review_gate_summary(ready),
        "star_law_candidate_rule_set_boundary_proposal": (
            _star_law_candidate_rule_set_boundary_proposal(ready)
        ),
        "proposed_candidate_rule_set_boundaries": (
            _proposed_candidate_rule_set_boundaries(ready)
        ),
        "non_authorization_boundary": _non_authorization_boundary(),
        "preserved_governance_boundaries": _preserved_governance_boundaries(),
        "future_candidate_rule_set_review_gate_constraints": (
            _future_candidate_rule_set_review_gate_constraints()
        ),
        "next_stage_constraints": _next_stage_constraints(),
        "scope_boundaries": _scope_boundaries(),
        "risk_notes": _risk_notes(sensitive_field_count),
        "required_human_actions": _required_human_actions(
            status, blocking_reasons
        ),
        "blocking_reasons": blocking_reasons,
        "next_allowed_step": READY_NEXT_ALLOWED_STEP
        if ready
        else BLOCKED_NEXT_ALLOWED_STEP,
        "sensitive_field_count": sensitive_field_count,
        "sensitive_fields_omitted": sensitive_field_count > 0,
    }


def governed_star_law_candidate_rule_set_boundary_proposal_to_json(
    report: Mapping[str, Any],
) -> str:
    """Serialize a Star-Law candidate rule-set proposal deterministically."""

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
        "source_review_gate_version_must_be_2_30_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_review_gate_status_ready",
        report.get("status") == "star_law_design_boundary_review_gate_ready",
        "source_review_gate_status_must_be_star_law_design_boundary_review_gate_ready",
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
        "source_must_not_claim_star_law_candidate_rule_creation_rule_creation_activation_enforcement_self_enforcing_law_autonomous_execution_handoff_scheduling_approval_write_execution_dry_run_or_civilization_core_completion",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_no_unsafe_text_claims",
        _unsafe_text_claims(report) == [],
        "source_must_not_textually_claim_star_law_rule_creation_activation_enforcement_self_enforcing_law_autonomous_execution_write_approval_next_layer_or_civilization_core_completion",
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
            == "Star-Law design boundary review gate only, not rule activation and not rule enforcement",
            "source_primary_layer_status_must_be_design_boundary_review_gate_only_not_rule_activation_not_rule_enforcement",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_source_layer",
            mapping.get("source_layer") == "星律记忆",
            "source_source_layer_must_be_star_law_memory",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_source_layer_status",
            mapping.get("source_layer_status")
            == "Star-Law design boundary proposal complete for human review only",
            "source_source_layer_status_must_be_design_boundary_proposal_complete_for_human_review_only",
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
            "source_direction",
            mapping.get("direction")
            == "Star-Law design boundary proposal -> Star-Law design boundary review gate",
            "source_direction_must_be_design_boundary_proposal_to_design_boundary_review_gate",
        )

    _add_check(
        checks,
        blocking_reasons,
        "source_reviewed_chain_versions",
        report.get("reviewed_chain_versions") == SOURCE_REVIEWED_CHAIN_VERSIONS,
        "source_reviewed_chain_versions_must_exactly_match_v2_9_0_through_v2_29_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_reviewed_star_hub_chain_versions",
        report.get("reviewed_star_hub_chain_versions")
        == SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS,
        "source_reviewed_star_hub_chain_versions_must_exactly_match_v2_19_0_through_v2_29_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_next_allowed_step",
        report.get("next_allowed_step")
        == "v2.31.0 Star-Law candidate rule-set boundary proposal",
        "source_next_allowed_step_must_be_v2_31_0_star_law_candidate_rule_set_boundary_proposal",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_blocking_reasons_empty",
        report.get("blocking_reasons") == [],
        "source_blocking_reasons_must_be_empty",
    )

    review_gate = report.get("star_law_design_boundary_review_gate")
    _add_check(
        checks,
        blocking_reasons,
        "source_star_law_design_boundary_review_gate_shape",
        isinstance(review_gate, Mapping),
        "source_star_law_design_boundary_review_gate_must_be_mapping",
    )
    if isinstance(review_gate, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_review_gate_review_status",
            review_gate.get("review_status")
            == "star_law_design_boundary_reviewed_for_human_review_only",
            "source_review_gate_review_status_must_be_human_review_only",
        )
        for key, expected in SOURCE_REVIEW_GATE_BOUNDARY_REQUIRED_FLAGS.items():
            _add_check(
                checks,
                blocking_reasons,
                f"source_review_gate_{key}",
                review_gate.get(key) is expected,
                f"source_review_gate_{key}_must_be_{str(expected).lower()}",
            )

    boundaries = report.get("reviewed_star_law_design_boundaries")
    _add_check(
        checks,
        blocking_reasons,
        "source_reviewed_star_law_design_boundaries_shape",
        isinstance(boundaries, Mapping),
        "source_reviewed_star_law_design_boundaries_must_be_mapping",
    )
    if isinstance(boundaries, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_reviewed_star_law_design_boundaries_review_only",
            _reviewed_boundaries_remain_review_only(boundaries),
            "source_reviewed_star_law_design_boundaries_must_remain_review_only_and_non_authorizing",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_reviewed_star_law_design_boundaries_no_unsafe_claims",
            _unsafe_boundary_claims(boundaries) == [],
            "source_reviewed_star_law_design_boundaries_must_not_claim_rule_creation_activation_enforcement_authorization_self_execution_autonomous_execution_or_memory_writing",
        )

    return checks, blocking_reasons


def _proposal_summary(ready: bool) -> dict[str, Any]:
    return {
        "proposal_status": (
            "star_law_candidate_rule_set_boundary_proposed_for_human_review_only"
            if ready
            else "blocked"
        ),
        "source_review_gate_version": SOURCE_REVIEW_GATE_VERSION,
        "source_star_law_design_boundary_review_gate_valid": ready,
        "candidate_rule_set_boundary_review_gate_ready_for_human_review_only": ready,
        "star_law_candidate_rules_created": False,
        "star_law_rules_created": False,
        "star_law_rules_activated": False,
        "star_law_rules_enforced": False,
        "star_law_self_enforcing_law_created": False,
        "autonomous_governance_created": False,
        "autonomous_execution_authorized": False,
        "civilization_core_complete_claimed": False,
        "only_permits_later_star_law_candidate_rule_set_boundary_review_gate": ready,
    }


def _source_review_gate_summary(ready: bool) -> dict[str, Any]:
    return {
        "source_review_gate_version": SOURCE_REVIEW_GATE_VERSION,
        "source_review_gate_status": (
            "star_law_design_boundary_review_gate_ready" if ready else "blocked"
        ),
        "source_chain_versions": list(SOURCE_REVIEWED_CHAIN_VERSIONS),
        "source_star_hub_chain_versions": list(
            SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS
        ),
        "source_review_gate_non_authorizing": True,
        "source_review_gate_candidate_rule_set_boundary_proposal_ready_for_human_review_only": ready,
        "source_review_gate_authorized_candidate_rule_creation": False,
        "source_review_gate_authorized_rule_creation": False,
        "source_review_gate_authorized_rule_activation": False,
        "source_review_gate_authorized_rule_enforcement": False,
        "source_review_gate_authorized_autonomous_execution": False,
        "source_review_gate_authorized_handoff": False,
        "source_review_gate_authorized_scheduling": False,
        "source_review_gate_authorized_dry_run_execution": False,
        "source_review_gate_authorized_approval": False,
        "source_review_gate_authorized_memory_write": False,
        "source_review_gate_authorized_memory_graph_mutation": False,
        "source_review_gate_authorized_operation_ledger_creation": False,
        "source_review_gate_authorized_openclaw_execution": False,
        "source_review_gate_claimed_civilization_core_completion": False,
        "source_review_gate_claimed_next_layer_entry": False,
    }


def _star_law_candidate_rule_set_boundary_proposal(ready: bool) -> dict[str, Any]:
    return {
        "proposal_status": (
            "star_law_candidate_rule_set_boundary_proposed_for_human_review_only"
            if ready
            else "blocked_no_star_law_candidate_rule_set_boundary_readiness_claim"
        ),
        "boundary_type": "star_law_candidate_rule_set_boundary_proposal",
        "source_review_gate_version": SOURCE_REVIEW_GATE_VERSION,
        "candidate_rule_set_boundary_proposed": ready,
        "candidate_rule_set_boundary_review_gate_ready_for_human_review_only": ready,
        "source_star_law_design_boundary_review_gate_valid": ready,
        "star_law_candidate_rules_created": False,
        "star_law_rules_created": False,
        "star_law_rules_activated": False,
        "star_law_rules_enforced": False,
        "star_law_self_enforcing_law_created": False,
        "star_law_self_enforcing_law_active": False,
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
        "star_law_candidate_rule_set_boundary_components": {
            "source_star_law_design_boundary_review_gate": "v2.30.0_source_review_gate_structurally_valid_for_human_review_only",
            "candidate_rule_taxonomy_boundary": "candidate_taxonomy_boundary_described_without_rule_creation",
            "candidate_rule_eligibility_boundary": "candidate_eligibility_boundary_described_without_rule_creation",
            "candidate_rule_non_creation_boundary": "candidate_rule_creation_not_performed",
            "candidate_rule_non_activation_boundary": "candidate_rule_activation_not_performed",
            "candidate_rule_non_enforcement_boundary": "candidate_rule_enforcement_not_performed",
            "self_enforcing_law_non_activation_boundary": "self_enforcing_law_not_created_or_activated",
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
        "next_allowed_step": READY_NEXT_ALLOWED_STEP
        if ready
        else BLOCKED_NEXT_ALLOWED_STEP,
        "non_authorization_notice": (
            "The Star-Law candidate rule-set boundary has been proposed for human review only. "
            "It describes candidate rule taxonomy, eligibility, evidence-lineage, auditability, and Human Operator control boundaries for a future governed Star-Law system. "
            "It creates no candidate Star-Law rules, creates no Star-Law rules, activates none, enforces none, creates no self-enforcing memory law, creates no autonomous governance, authorizes no autonomous execution, creates no self-executing policy, grants no approval, records no real human decision, performs no handoff, schedules nothing, performs no dry-run, executes no dry-run plan, writes no durable memory, mutates no Memory Graph, creates no operation-ledger entry, calls no OpenClaw or GitHub API, claims no Civilization Core completion, starts no 星魂 continuity, starts no 星宙 evolution, and starts no 星源 self-evolution."
            if ready
            else "The Star-Law candidate rule-set boundary proposal is blocked; no readiness, authorization, rule creation, rule activation, rule enforcement, autonomous execution, handoff, scheduling, approval, write, execution, dry-run, next-layer, or Civilization Core completion claim is made."
        ),
    }


def _proposed_candidate_rule_set_boundaries(ready: bool) -> dict[str, Any]:
    status = "proposed_for_human_review_only" if ready else "blocked"
    return {
        "candidate_rule_taxonomy_boundary": {
            "proposal_only": True,
            "boundary_status": status,
            "description": "Candidate taxonomy categories may be described for later human review only: lineage, conflict handling, scope, escalation triggers, and audit checks.",
            "star_law_candidate_rules_created": False,
            "star_law_rules_created": False,
        },
        "candidate_rule_eligibility_boundary": {
            "proposal_only": True,
            "boundary_status": status,
            "description": "Candidate eligibility is limited to future review inputs with explicit source lineage, Human Operator context, and non-authorization evidence.",
            "candidate_rule_creation_performed": False,
            "authorization_granted": False,
        },
        "candidate_rule_input_scope_boundary": {
            "proposal_only": True,
            "boundary_status": status,
            "description": "Candidate inputs are limited to sanitized chain versions, structural review-gate status, and governance boundary summaries.",
            "raw_source_report_copied": False,
            "real_human_decision_recorded": False,
        },
        "candidate_rule_output_scope_boundary": {
            "proposal_only": True,
            "boundary_status": status,
            "description": "Candidate outputs are limited to boundary categories for later review and must not become executable policy.",
            "self_executing_policy_created": False,
            "self_executing_policy_active": False,
        },
        "candidate_rule_non_creation_boundary": {
            "proposal_only": True,
            "boundary_status": status,
            "description": "Candidate rule material remains descriptive boundary text for later review only.",
            "star_law_candidate_rules_created": False,
            "star_law_rules_created": False,
        },
        "candidate_rule_non_activation_boundary": {
            "proposal_only": True,
            "boundary_status": status,
            "description": "Candidate rule material cannot become active in this proposal step.",
            "star_law_rules_activated": False,
            "star_law_self_enforcing_law_active": False,
        },
        "candidate_rule_non_enforcement_boundary": {
            "proposal_only": True,
            "boundary_status": status,
            "description": "Candidate rule material cannot be enforced in this proposal step.",
            "star_law_rules_enforced": False,
            "autonomous_execution_authorized": False,
        },
        "candidate_rule_evidence_lineage_boundary": {
            "proposal_only": True,
            "boundary_status": status,
            "description": "Future review must preserve source review-gate version, expected chain versions, and sanitized governance-boundary evidence.",
            "would_create_operation_ledger_entry": False,
            "would_write_durable_memory": False,
        },
        "human_operator_control_boundary": {
            "proposal_only": True,
            "boundary_status": status,
            "description": "Human Operator remains final authority for any later review, approval, execution, handoff, scheduling, memory write, graph mutation, or next-layer work.",
            "autonomous_governance_created": False,
            "autonomous_execution_authorized": False,
        },
        "non_authorization_boundary": {
            "proposal_only": True,
            "boundary_status": status,
            "description": "This boundary grants no permission for execution, approval, handoff, scheduling, write, graph mutation, ledger entry creation, OpenClaw, GitHub API, or dry-run execution.",
            "authorization_granted": False,
            "approval_granted": False,
        },
        "memory_write_boundary": {
            "proposal_only": True,
            "boundary_status": status,
            "description": "Durable memory write paths remain outside this candidate rule-set boundary proposal.",
            "durable_memory_write_authorized": False,
            "would_write_durable_memory": False,
        },
        "memory_graph_boundary": {
            "proposal_only": True,
            "boundary_status": status,
            "description": "Memory Graph mutation paths remain outside this candidate rule-set boundary proposal.",
            "memory_graph_mutation_authorized": False,
            "would_mutate_memory_graph": False,
        },
        "operation_ledger_boundary": {
            "proposal_only": True,
            "boundary_status": status,
            "description": "Operation-ledger entry creation remains outside this candidate rule-set boundary proposal.",
            "operation_ledger_creation_authorized": False,
            "would_create_operation_ledger_entry": False,
        },
        "openclaw_boundary": {
            "proposal_only": True,
            "boundary_status": status,
            "description": "OpenClaw execution remains outside this candidate rule-set boundary proposal.",
            "openclaw_execution_authorized": False,
            "invokes_openclaw": False,
        },
        "approval_boundary": {
            "proposal_only": True,
            "boundary_status": status,
            "description": "Approval request creation, submission, execution, decision recording, and grant remain outside this candidate rule-set boundary proposal.",
            "approval_request_created": False,
            "approval_request_submitted": False,
            "approval_request_authorized": False,
            "approval_granted": False,
        },
        "auditability_boundary": {
            "proposal_only": True,
            "boundary_status": status,
            "description": "Auditability is limited to deterministic local report structure, expected chain-version traceability, and omitted sensitive source material.",
            "would_create_operation_ledger_entry": False,
            "human_decision_recorded": False,
        },
        "future_review_gate_boundary": {
            "proposal_only": True,
            "boundary_status": status,
            "description": (
                "The only later step described by this report is v2.32.0 Star-Law candidate rule-set boundary review gate."
                if ready
                else "A later Star-Law candidate rule-set boundary review gate is unavailable until blocking reasons are resolved."
            ),
            "review_gate_authorized": False,
            "approval_granted": False,
        },
    }


def _non_authorization_boundary() -> dict[str, Any]:
    return {
        "star_law_candidate_rule_set_boundary_proposal_ready_is_self_enforcing_memory_law": False,
        "star_law_candidate_rule_set_boundary_proposal_ready_is_rule_creation": False,
        "star_law_candidate_rule_set_boundary_proposal_ready_is_rule_activation": False,
        "star_law_candidate_rule_set_boundary_proposal_ready_is_rule_enforcement": False,
        "star_law_candidate_rule_set_boundary_proposal_ready_is_autonomous_governance": False,
        "star_law_candidate_rule_set_boundary_proposal_ready_is_autonomous_execution": False,
        "star_law_candidate_rule_set_boundary_proposal_ready_is_handoff": False,
        "star_law_candidate_rule_set_boundary_proposal_ready_is_authorization": False,
        "star_law_candidate_rule_set_boundary_proposal_ready_is_scheduling": False,
        "star_law_candidate_rule_set_boundary_proposal_ready_is_dry_run_execution": False,
        "star_law_candidate_rule_set_boundary_proposal_ready_is_approval": False,
        "star_law_candidate_rule_set_boundary_proposal_ready_is_human_decision": False,
        "star_law_candidate_rule_set_boundary_proposal_ready_is_memory_write_permission": False,
        "star_law_candidate_rule_set_boundary_proposal_ready_is_memory_graph_mutation_permission": False,
        "star_law_candidate_rule_set_boundary_proposal_ready_is_operation_ledger_creation": False,
        "star_law_candidate_rule_set_boundary_proposal_ready_is_openclaw_execution_permission": False,
        "star_law_candidate_rule_set_boundary_proposal_ready_is_civilization_core_completion": False,
        "only_permits_later_star_law_candidate_rule_set_boundary_review_gate": True,
        "human_operator_remains_final_authority": True,
    }


def _preserved_governance_boundaries() -> list[str]:
    return [
        "Star-Law candidate rule-set boundary proposal ready is not self-enforcing memory law.",
        "Star-Law candidate rule-set boundary proposal ready is not rule creation.",
        "Star-Law candidate rule-set boundary proposal ready is not rule activation.",
        "Star-Law candidate rule-set boundary proposal ready is not rule enforcement.",
        "Star-Law candidate rule-set boundary proposal ready is not autonomous governance.",
        "Star-Law candidate rule-set boundary proposal ready is not autonomous execution.",
        "Star-Law candidate rule-set boundary proposal ready is not handoff.",
        "Star-Law candidate rule-set boundary proposal ready is not authorization.",
        "Star-Law candidate rule-set boundary proposal ready is not scheduling.",
        "Star-Law candidate rule-set boundary proposal ready is not dry-run execution.",
        "Star-Law candidate rule-set boundary proposal ready is not approval.",
        "Star-Law candidate rule-set boundary proposal ready is not a real human decision.",
        "Star-Law candidate rule-set boundary proposal ready is not durable memory write permission.",
        "Star-Law candidate rule-set boundary proposal ready is not Memory Graph mutation permission.",
        "Star-Law candidate rule-set boundary proposal ready is not operation-ledger creation.",
        "Star-Law candidate rule-set boundary proposal ready is not OpenClaw execution permission.",
        "Star-Law candidate rule-set boundary proposal ready is not Civilization Core completion.",
        "Star-Law candidate rule-set boundary proposal ready only permits a later Star-Law candidate rule-set boundary review gate.",
        "Human Operator remains final authority.",
    ]


def _future_candidate_rule_set_review_gate_constraints() -> list[str]:
    return [
        "A later Star-Law candidate rule-set boundary review gate may inspect this proposal through a separate governed process.",
        "A later review gate must not be treated as automatic rule creation, activation, enforcement, approval, handoff, scheduling, memory writing, Memory Graph mutation, operation-ledger creation, OpenClaw execution, GitHub API action, dry-run execution, autonomous execution, or Civilization Core completion.",
        "Any future candidate rule taxonomy or eligibility category must remain inactive until a separate Human Operator governed process explicitly authorizes an applicable later stage.",
        "Human Operator remains final authority for all future Star-Law governance decisions.",
    ]


def _next_stage_constraints() -> list[str]:
    return [
        "The only next allowed step is v2.32.0 Star-Law candidate rule-set boundary review gate.",
        "v2.31.0 is Star-Law candidate rule-set boundary proposal only, not rule creation, not rule activation, and not rule enforcement.",
        "v2.31.0 must not create, activate, or enforce Star-Law rules.",
        "v2.31.0 must not authorize Star-Hub handoff, scheduling, approval, dry-run execution, memory writing, Memory Graph mutation, operation-ledger creation, OpenClaw execution, or GitHub API actions.",
        "Mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, and 星源 self-evolution remain out of scope.",
        "Human Operator remains final authority for any future governed action.",
    ]


def _scope_boundaries() -> list[str]:
    return [
        "Civilization Core is the total system.",
        "Fifteen Memory Layers are the highest memory coordinate system.",
        "Subspace Memory System is the engineering carrier.",
        "Hermes, Codex CLI, OpenClaw, Terminal, and GitHub are components, not the core.",
        "This v2.31.0 step is limited to 星律记忆 Star-Law candidate rule-set boundary proposal only.",
        "This proposal does not enter mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, or 星源 self-evolution.",
    ]


def _risk_notes(sensitive_field_count: int) -> list[str]:
    notes = [
        "Star-Law candidate rule-set boundary proposal ready must not be treated as self-enforcing memory law, rule creation, rule activation, rule enforcement, autonomous governance, autonomous execution, handoff, authorization, scheduling, approval, dry-run execution, or Civilization Core completion.",
        "No durable memory write, Memory Graph mutation, operation-ledger entry, GitHub API write, merge, tag creation, approval, request creation, request submission, request execution, human decision record, handoff, scheduling, dry-run performance, dry-run execution, or OpenClaw execution is produced or authorized.",
        "Mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, and 星源 self-evolution are not started.",
    ]
    if sensitive_field_count:
        notes.append(
            "Sensitive fields were omitted from candidate rule-set boundary proposal output."
        )
    return notes


def _required_human_actions(status: str, blocking_reasons: list[str]) -> list[str]:
    if status == "star_law_candidate_rule_set_boundary_proposal_ready":
        return [
            "human_operator_must_review_star_law_candidate_rule_set_boundary_proposal_before_any_later_candidate_rule_set_boundary_review_gate",
            "human_operator_must_confirm_candidate_rule_set_boundary_proposal_ready_is_not_self_enforcing_law_rule_creation_rule_activation_rule_enforcement_autonomous_execution_handoff_authorization_scheduling_approval_write_execution_or_civilization_core_completion",
            "human_operator_must_use_separate_governed_process_for_any_future_star_law_candidate_rule_set_boundary_review_gate_rule_activation_rule_enforcement_real_approval_write_submission_execution_handoff_scheduling_dry_run_decision_or_next_layer_work",
        ]
    actions = [
        "repair_source_v2_30_0_star_law_design_boundary_review_gate_before_candidate_rule_set_boundary_proposal_can_continue",
        "confirm_all_star_law_candidate_rule_creation_rule_creation_rule_activation_rule_enforcement_autonomous_execution_handoff_scheduling_dry_run_write_approval_execution_next_layer_and_civilization_core_completion_flags_remain_false",
        "rerun_local_star_law_candidate_rule_set_boundary_proposal_after_blocking_reasons_are_resolved",
    ]
    if blocking_reasons:
        actions.append(
            "resolve_blocking_reasons_before_star_law_candidate_rule_set_boundary_proposal_can_be_ready"
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


def _reviewed_boundaries_remain_review_only(value: Mapping[str, Any]) -> bool:
    for boundary in value.values():
        if not isinstance(boundary, Mapping):
            return False
        if boundary.get("review_only") is not True:
            return False
        for key, nested in boundary.items():
            if nested is True and key not in BOUNDARY_ALLOWED_TRUE_KEYS:
                return False
    return True


def _unsafe_boundary_claims(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if nested is True and key not in BOUNDARY_ALLOWED_TRUE_KEYS:
                found.append("unsafe_true_boundary_claim")
            if isinstance(nested, str) and _contains_forbidden_boundary_claim(nested):
                found.append("unsafe_text_boundary_claim")
            found.extend(_unsafe_boundary_claims(nested))
    elif isinstance(value, list):
        for nested in value:
            found.extend(_unsafe_boundary_claims(nested))
    elif isinstance(value, str) and _contains_forbidden_boundary_claim(value):
        found.append("unsafe_text_boundary_claim")
    return found


def _unsafe_text_claims(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, Mapping):
        for nested in value.values():
            found.extend(_unsafe_text_claims(nested))
    elif isinstance(value, list):
        for nested in value:
            found.extend(_unsafe_text_claims(nested))
    elif isinstance(value, str) and _contains_forbidden_boundary_claim(value):
        found.append("unsafe_text_claim")
    return found


def _contains_forbidden_boundary_claim(value: str) -> bool:
    lowered = value.lower()
    return any(claim in lowered for claim in FORBIDDEN_BOUNDARY_CLAIMS)


def _count_sensitive_keys(value: Any) -> int:
    if isinstance(value, Mapping):
        return sum(
            (
                1
                if isinstance(key, str) and key.lower() in SENSITIVE_KEYS
                else 0
            )
            + _count_sensitive_keys(nested)
            for key, nested in value.items()
        )
    if isinstance(value, list):
        return sum(_count_sensitive_keys(nested) for nested in value)
    return 0


__all__ = [
    "GOVERNED_STAR_LAW_CANDIDATE_RULE_SET_BOUNDARY_PROPOSAL_VERSION",
    "PROPOSED_CHAIN_VERSIONS",
    "PROPOSED_STAR_HUB_CHAIN_VERSIONS",
    "READY_NEXT_ALLOWED_STEP",
    "build_governed_star_law_candidate_rule_set_boundary_proposal",
    "governed_star_law_candidate_rule_set_boundary_proposal_to_json",
]
