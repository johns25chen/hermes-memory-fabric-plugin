"""Governed Star-Law candidate rule enforcement boundary proposal for v2.34 gates."""

from __future__ import annotations

import json
from typing import Any, Mapping

from .governed_star_law_candidate_rule_activation_boundary_review_gate import (
    REVIEWED_CHAIN_VERSIONS as SOURCE_REVIEWED_CHAIN_VERSIONS,
    REVIEWED_STAR_HUB_CHAIN_VERSIONS as SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS,
)


GOVERNED_STAR_LAW_CANDIDATE_RULE_ENFORCEMENT_BOUNDARY_PROPOSAL_VERSION = "2.35.0"
SOURCE_REVIEW_GATE_VERSION = "2.34.0"

PROPOSED_CHAIN_VERSIONS = [
    *SOURCE_REVIEWED_CHAIN_VERSIONS,
    "v2.34.0",
]

PROPOSED_STAR_HUB_CHAIN_VERSIONS = [
    *SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS,
    "v2.34.0",
]

LAYER_MAPPING = {
    "primary_layer": "星律记忆",
    "primary_layer_status": "Star-Law candidate rule enforcement boundary proposal only, not candidate rule enforcement, not rule enforcement, and not autonomous execution",
    "source_layer": "星律记忆",
    "source_layer_status": "Star-Law candidate rule activation boundary review gate complete for human review only",
    "supporting_layers": ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"],
    "direction": "Star-Law candidate rule activation boundary review gate -> Star-Law candidate rule enforcement boundary proposal",
}

READY_NEXT_ALLOWED_STEP = (
    "v2.36.0 Star-Law candidate rule enforcement boundary review gate"
)
BLOCKED_NEXT_ALLOWED_STEP = (
    "resolve_v2_35_0_star_law_candidate_rule_enforcement_boundary_proposal_blockers"
)

PROPOSAL_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "proposal_only": True,
    "candidate_rule_enforcement_boundary_proposal_only": True,
    "star_law_candidate_rule_enforcement_boundary_proposal_only": True,
    "candidate_rule_enforcement_performed": False,
    "candidate_rule_enforcement_authorized": False,
    "candidate_rule_activation_performed": False,
    "candidate_rule_activation_authorized": False,
    "star_law_candidate_rules_created": False,
    "star_law_candidate_rules_activated": False,
    "star_law_candidate_rules_enforced": False,
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
    "candidate_rule_activation_boundary_review_gate_only": True,
    "star_law_candidate_rule_activation_boundary_review_gate_only": True,
    "candidate_rule_activation_boundary_reviewed_for_human_review_only": True,
    "candidate_rule_enforcement_boundary_proposal_ready_for_human_review_only": True,
    "candidate_rule_activation_performed": False,
    "candidate_rule_activation_authorized": False,
    "star_law_candidate_rules_created": False,
    "star_law_candidate_rules_activated": False,
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

SOURCE_REVIEW_GATE_REQUIRED_FLAGS = {
    "candidate_rule_activation_boundary_reviewed": True,
    "candidate_rule_activation_boundary_structurally_review_ready": True,
    "candidate_rule_enforcement_boundary_proposal_ready_for_human_review_only": True,
    "source_star_law_candidate_rule_activation_boundary_proposal_valid": True,
    "candidate_rule_activation_performed": False,
    "candidate_rule_activation_authorized": False,
    "star_law_candidate_rules_created": False,
    "star_law_candidate_rules_activated": False,
    "star_law_candidate_rules_enforced": False,
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
}

UNSAFE_TRUE_FIELDS = {
    "candidate_rules_created",
    "candidate_rules_activated",
    "candidate_rule_enforcement_performed",
    "candidate_rule_enforcement_authorized",
    "candidate_rule_enforcement_boundary_proposal_authorized",
    "candidate_rule_enforcement_boundary_review_gate_authorized",
    "candidate_rule_activation_performed",
    "candidate_rule_activation_authorized",
    "candidate_rule_activation_boundary_proposal_authorized",
    "candidate_rule_activation_boundary_review_gate_authorized",
    "star_law_candidate_rules_created",
    "star_law_candidate_rules_activated",
    "star_law_candidate_rules_enforced",
    "star_law_rules_created",
    "star_law_rules_activated",
    "star_law_rules_enforced",
    "star_law_self_enforcing_law_created",
    "star_law_self_enforcing_law_active",
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

BOUNDARY_ALLOWED_TRUE_KEYS = {"proposal_only"}
REVIEWED_BOUNDARY_ALLOWED_TRUE_KEYS = {"review_only"}

FORBIDDEN_BOUNDARY_CLAIMS = (
    "candidate rules are enforced",
    "candidate rules are activated",
    "candidate rules are created",
    "star-law candidate rules are enforced",
    "star-law candidate rules are activated",
    "star-law candidate rules are created",
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
    "self-enforcing memory law has started",
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

PROPOSAL_COMPONENTS = {
    "source_candidate_rule_activation_boundary_review_gate",
    "candidate_rule_enforcement_eligibility_boundary",
    "candidate_rule_enforcement_precondition_boundary",
    "candidate_rule_non_enforcement_boundary",
    "candidate_rule_non_autonomous_execution_boundary",
    "enforcement_human_operator_control_boundary",
    "enforcement_evidence_lineage_boundary",
    "enforcement_auditability_boundary",
    "enforcement_rollback_boundary",
    "enforcement_suspension_boundary",
    "enforcement_violation_observation_boundary",
    "self_enforcing_law_non_activation_boundary",
    "autonomous_governance_non_creation_boundary",
    "autonomous_execution_non_authorization_boundary",
    "memory_write_non_authorization_boundary",
    "memory_graph_mutation_non_authorization_boundary",
    "operation_ledger_non_creation_boundary",
    "openclaw_execution_non_authorization_boundary",
    "approval_non_authorization_boundary",
    "human_operator_final_authority_boundary",
    "fifteen_memory_layers_boundary",
}

PROPOSED_CANDIDATE_RULE_ENFORCEMENT_BOUNDARY_KEYS = {
    "candidate_rule_enforcement_eligibility_boundary",
    "candidate_rule_enforcement_precondition_boundary",
    "candidate_rule_enforcement_input_scope_boundary",
    "candidate_rule_enforcement_output_scope_boundary",
    "candidate_rule_non_enforcement_boundary",
    "candidate_rule_non_autonomous_execution_boundary",
    "candidate_rule_enforcement_evidence_lineage_boundary",
    "human_operator_control_boundary",
    "non_authorization_boundary",
    "memory_write_boundary",
    "memory_graph_boundary",
    "operation_ledger_boundary",
    "openclaw_boundary",
    "approval_boundary",
    "auditability_boundary",
    "rollback_boundary",
    "suspension_boundary",
    "violation_observation_boundary",
    "future_review_gate_boundary",
}


def build_governed_star_law_candidate_rule_enforcement_boundary_proposal(
    review_gate_report: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a local-only, non-authorizing candidate rule enforcement proposal."""

    checks, blocking_reasons = _proposal_checks(review_gate_report)
    sensitive_field_count = _count_sensitive_keys(review_gate_report)
    blocking_reasons = list(dict.fromkeys(blocking_reasons))
    status = (
        "star_law_candidate_rule_enforcement_boundary_proposal_ready"
        if not blocking_reasons
        else "blocked"
    )
    ready = (
        status
        == "star_law_candidate_rule_enforcement_boundary_proposal_ready"
    )

    return {
        "version": GOVERNED_STAR_LAW_CANDIDATE_RULE_ENFORCEMENT_BOUNDARY_PROPOSAL_VERSION,
        "status": status,
        **PROPOSAL_FLAGS,
        "candidate_rule_enforcement_boundary_proposed_for_human_review_only": ready,
        "candidate_rule_enforcement_boundary_review_gate_ready_for_human_review_only": ready,
        "civilization_core_layer_mapping": dict(LAYER_MAPPING),
        "source_review_gate_version": SOURCE_REVIEW_GATE_VERSION,
        "proposed_chain_versions": list(PROPOSED_CHAIN_VERSIONS),
        "proposed_star_hub_chain_versions": list(PROPOSED_STAR_HUB_CHAIN_VERSIONS),
        "star_law_candidate_rule_enforcement_boundary_proposal_summary": (
            _proposal_summary(ready)
        ),
        "proposal_checks": checks,
        "source_review_gate_summary": _source_review_gate_summary(ready),
        "star_law_candidate_rule_enforcement_boundary_proposal": (
            _star_law_candidate_rule_enforcement_boundary_proposal(ready)
        ),
        "proposed_candidate_rule_enforcement_boundaries": (
            _proposed_candidate_rule_enforcement_boundaries(ready)
        ),
        "non_authorization_boundary": _non_authorization_boundary(ready),
        "preserved_governance_boundaries": _preserved_governance_boundaries(),
        "future_candidate_rule_enforcement_review_gate_constraints": (
            _future_candidate_rule_enforcement_review_gate_constraints()
        ),
        "next_stage_constraints": _next_stage_constraints(),
        "scope_boundaries": _scope_boundaries(),
        "risk_notes": _risk_notes(sensitive_field_count),
        "required_human_actions": _required_human_actions(status, blocking_reasons),
        "blocking_reasons": blocking_reasons,
        "next_allowed_step": READY_NEXT_ALLOWED_STEP
        if ready
        else BLOCKED_NEXT_ALLOWED_STEP,
        "sensitive_field_count": sensitive_field_count,
        "sensitive_fields_omitted": sensitive_field_count > 0,
    }


def governed_star_law_candidate_rule_enforcement_boundary_proposal_to_json(
    report: Mapping[str, Any],
) -> str:
    """Serialize a Star-Law candidate rule enforcement boundary proposal deterministically."""

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
        "source_review_gate_version_must_be_2_34_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_review_gate_status_ready",
        report.get("status")
        == "star_law_candidate_rule_activation_boundary_review_gate_ready",
        "source_review_gate_status_must_be_star_law_candidate_rule_activation_boundary_review_gate_ready",
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
        "source_must_not_claim_candidate_rule_enforcement_candidate_rule_activation_candidate_rule_creation_star_law_rule_creation_activation_enforcement_self_enforcing_law_autonomous_execution_handoff_scheduling_approval_write_execution_dry_run_or_civilization_core_completion",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_no_unsafe_text_claims",
        _unsafe_text_claims(report) == [],
        "source_must_not_textually_claim_candidate_rule_enforcement_candidate_rule_activation_candidate_rule_creation_star_law_rule_creation_activation_enforcement_self_enforcing_law_autonomous_execution_write_approval_next_layer_or_civilization_core_completion",
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
            == "Star-Law candidate rule activation boundary review gate only, not candidate rule activation, not rule activation, and not rule enforcement",
            "source_primary_layer_status_must_be_candidate_rule_activation_boundary_review_gate_only_not_candidate_rule_activation_rule_activation_or_rule_enforcement",
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
            == "Star-Law candidate rule activation boundary proposal complete for human review only",
            "source_source_layer_status_must_be_candidate_rule_activation_boundary_proposal_complete_for_human_review_only",
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
            == "Star-Law candidate rule activation boundary proposal -> Star-Law candidate rule activation boundary review gate",
            "source_direction_must_be_candidate_rule_activation_boundary_proposal_to_candidate_rule_activation_boundary_review_gate",
        )

    _add_check(
        checks,
        blocking_reasons,
        "source_reviewed_chain_versions",
        report.get("reviewed_chain_versions") == SOURCE_REVIEWED_CHAIN_VERSIONS,
        "source_reviewed_chain_versions_must_exactly_match_v2_9_0_through_v2_33_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_reviewed_star_hub_chain_versions",
        report.get("reviewed_star_hub_chain_versions")
        == SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS,
        "source_reviewed_star_hub_chain_versions_must_exactly_match_v2_19_0_through_v2_33_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_next_allowed_step",
        report.get("next_allowed_step")
        == "v2.35.0 Star-Law candidate rule enforcement boundary proposal",
        "source_next_allowed_step_must_be_v2_35_0_star_law_candidate_rule_enforcement_boundary_proposal",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_blocking_reasons_empty",
        report.get("blocking_reasons") == [],
        "source_blocking_reasons_must_be_empty",
    )

    review_gate = report.get("star_law_candidate_rule_activation_boundary_review_gate")
    _add_check(
        checks,
        blocking_reasons,
        "source_star_law_candidate_rule_activation_boundary_review_gate_shape",
        isinstance(review_gate, Mapping),
        "source_star_law_candidate_rule_activation_boundary_review_gate_must_be_mapping",
    )
    if isinstance(review_gate, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_candidate_rule_activation_boundary_review_gate_status",
            review_gate.get("review_status")
            == "star_law_candidate_rule_activation_boundary_reviewed_for_human_review_only",
            "source_candidate_rule_activation_boundary_review_gate_status_must_be_human_review_only",
        )
        for key, expected in SOURCE_REVIEW_GATE_REQUIRED_FLAGS.items():
            _add_check(
                checks,
                blocking_reasons,
                f"source_candidate_rule_activation_boundary_review_gate_{key}",
                _source_review_gate_flag_matches(review_gate, key, expected),
                f"source_candidate_rule_activation_boundary_review_gate_{key}_must_be_{str(expected).lower()}",
            )

    boundaries = report.get("reviewed_candidate_rule_activation_boundaries")
    _add_check(
        checks,
        blocking_reasons,
        "source_reviewed_candidate_rule_activation_boundaries_shape",
        isinstance(boundaries, Mapping),
        "source_reviewed_candidate_rule_activation_boundaries_must_be_mapping",
    )
    if isinstance(boundaries, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_reviewed_candidate_rule_activation_boundaries_review_only",
            _reviewed_boundaries_remain_review_only(boundaries),
            "source_reviewed_candidate_rule_activation_boundaries_must_remain_review_only_and_non_authorizing",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_reviewed_candidate_rule_activation_boundaries_no_unsafe_claims",
            _unsafe_boundary_claims(boundaries, REVIEWED_BOUNDARY_ALLOWED_TRUE_KEYS)
            == [],
            "source_reviewed_candidate_rule_activation_boundaries_must_not_claim_candidate_rule_enforcement_candidate_rule_activation_candidate_rule_creation_rule_creation_activation_enforcement_authorization_self_execution_autonomous_execution_or_memory_writing",
        )

    return checks, blocking_reasons


def _source_review_gate_flag_matches(
    review_gate: Mapping[str, Any], key: str, expected: bool
) -> bool:
    if key == "star_law_candidate_rules_enforced" and key not in review_gate:
        return expected is False
    return review_gate.get(key) is expected


def _proposal_summary(ready: bool) -> dict[str, Any]:
    return {
        "proposal_status": (
            "star_law_candidate_rule_enforcement_boundary_proposed_for_human_review_only"
            if ready
            else "blocked"
        ),
        "source_review_gate_version": SOURCE_REVIEW_GATE_VERSION,
        "source_star_law_candidate_rule_activation_boundary_review_gate_valid": ready,
        "candidate_rule_enforcement_boundary_proposed_for_human_review_only": ready,
        "candidate_rule_enforcement_boundary_review_gate_ready_for_human_review_only": ready,
        "non_authorizing": True,
        "non_candidate_rule_enforcing": True,
        "non_candidate_rule_activating": True,
        "non_candidate_rule_creating": True,
        "non_rule_creating": True,
        "non_rule_activating": True,
        "non_rule_enforcing": True,
        "non_autonomous_governance": True,
        "non_autonomous_execution": True,
        "non_handoff": True,
        "non_scheduling": True,
        "non_dry_run_execution": True,
        "non_memory_writing": True,
        "non_memory_graph_mutating": True,
        "non_operation_ledger_creating": True,
        "non_openclaw_executing": True,
        "non_approval_granting": True,
        "non_human_decision_recording": True,
        "civilization_core_complete_claimed": False,
        "only_permits_later_star_law_candidate_rule_enforcement_boundary_review_gate": ready,
    }


def _source_review_gate_summary(ready: bool) -> dict[str, Any]:
    return {
        "source_review_gate_version": SOURCE_REVIEW_GATE_VERSION,
        "source_review_gate_status": (
            "star_law_candidate_rule_activation_boundary_review_gate_ready"
            if ready
            else "blocked"
        ),
        "source_chain_versions": list(SOURCE_REVIEWED_CHAIN_VERSIONS),
        "source_star_hub_chain_versions": list(
            SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS
        ),
        "source_candidate_rule_activation_boundary_review_gate_ready": ready,
        "source_review_gate_authorized_candidate_rule_enforcement": False,
        "source_review_gate_authorized_candidate_rule_activation": False,
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
        "raw_source_review_gate_copied": False,
    }


def _star_law_candidate_rule_enforcement_boundary_proposal(
    ready: bool,
) -> dict[str, Any]:
    return {
        "proposal_status": (
            "star_law_candidate_rule_enforcement_boundary_proposed_for_human_review_only"
            if ready
            else "blocked_no_star_law_candidate_rule_enforcement_boundary_proposal_readiness_claim"
        ),
        "boundary_type": "star_law_candidate_rule_enforcement_boundary_proposal",
        "source_review_gate_version": SOURCE_REVIEW_GATE_VERSION,
        "candidate_rule_enforcement_boundary_proposed": ready,
        "candidate_rule_enforcement_boundary_review_gate_ready_for_human_review_only": ready,
        "source_star_law_candidate_rule_activation_boundary_review_gate_valid": ready,
        "candidate_rule_enforcement_performed": False,
        "candidate_rule_enforcement_authorized": False,
        "candidate_rule_activation_performed": False,
        "candidate_rule_activation_authorized": False,
        "star_law_candidate_rules_created": False,
        "star_law_candidate_rules_activated": False,
        "star_law_candidate_rules_enforced": False,
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
        "star_law_candidate_rule_enforcement_boundary_components": (
            _proposal_components(ready)
        ),
        "next_allowed_step": READY_NEXT_ALLOWED_STEP
        if ready
        else BLOCKED_NEXT_ALLOWED_STEP,
        "non_authorization_notice": (
            "The Star-Law candidate rule enforcement boundary has been proposed for human review only. "
            "A later candidate rule enforcement boundary review gate is the only next governed step. "
            "This proposal performs no candidate rule enforcement, authorizes no candidate rule enforcement, performs no candidate rule activation, authorizes no candidate rule activation, creates no candidate Star-Law rules, activates no candidate Star-Law rules, enforces no candidate Star-Law rules, creates no Star-Law rules, activates no rules, enforces no rules, creates no self-enforcing memory law, creates no autonomous governance, authorizes no autonomous execution, creates no self-executing policy, grants no approval, records no real human decision, performs no handoff, schedules nothing, performs no dry-run, executes no dry-run plan, writes no durable memory, mutates no Memory Graph, creates no operation-ledger entry, calls no OpenClaw or GitHub API, claims no Civilization Core completion, starts no 星魂 continuity, starts no 星宙 evolution, and starts no 星源 self-evolution."
            if ready
            else "The Star-Law candidate rule enforcement boundary proposal is blocked; no readiness, authorization, candidate rule enforcement, candidate rule activation, candidate rule creation, rule creation, rule activation, rule enforcement, autonomous execution, handoff, scheduling, approval, write, execution, dry-run, next-layer, or Civilization Core completion claim is made."
        ),
    }


def _proposal_components(ready: bool) -> dict[str, str]:
    status = "proposed_for_human_review_only" if ready else "blocked"
    return {component: status for component in sorted(PROPOSAL_COMPONENTS)}


def _proposed_candidate_rule_enforcement_boundaries(
    ready: bool,
) -> dict[str, dict[str, Any]]:
    status = "proposed_for_human_review_only" if ready else "blocked"
    summaries = {
        "candidate_rule_enforcement_eligibility_boundary": "Defines future eligibility criteria as human-review proposal material only.",
        "candidate_rule_enforcement_precondition_boundary": "Defines future preconditions as inactive proposal material only.",
        "candidate_rule_enforcement_input_scope_boundary": "Limits future inputs to sanitized chain and governance status evidence.",
        "candidate_rule_enforcement_output_scope_boundary": "Limits future outputs to reviewable boundary reports with no executable policy.",
        "candidate_rule_non_enforcement_boundary": "Preserves the rule that this proposal performs no candidate rule enforcement.",
        "candidate_rule_non_autonomous_execution_boundary": "Preserves Human Operator control and excludes autonomous execution.",
        "candidate_rule_enforcement_evidence_lineage_boundary": "Requires later review to trace evidence lineage without creating ledger records here.",
        "human_operator_control_boundary": "States that the Human Operator remains final authority for any later governed action.",
        "non_authorization_boundary": "States that this proposal grants no authorization or approval.",
        "memory_write_boundary": "States that durable memory writes are outside this proposal.",
        "memory_graph_boundary": "States that Memory Graph mutation is outside this proposal.",
        "operation_ledger_boundary": "States that operation-ledger creation is outside this proposal.",
        "openclaw_boundary": "States that OpenClaw execution is outside this proposal.",
        "approval_boundary": "States that approval creation, submission, execution, and granting are outside this proposal.",
        "auditability_boundary": "Defines auditability requirements for a later review gate using deterministic local report fields.",
        "rollback_boundary": "Defines rollback and reversal categories for later review without performing rollback.",
        "suspension_boundary": "Defines suspension categories for later review without enforcing suspension.",
        "violation_observation_boundary": "Defines violation-observation categories for later review without taking enforcement action.",
        "future_review_gate_boundary": "Allows only a later governed Star-Law candidate rule enforcement boundary review gate.",
    }
    return {
        key: _proposed_boundary(status, summaries[key])
        for key in sorted(PROPOSED_CANDIDATE_RULE_ENFORCEMENT_BOUNDARY_KEYS)
    }


def _proposed_boundary(status: str, summary: str) -> dict[str, Any]:
    return {
        "proposal_only": True,
        "boundary_status": status,
        "summary": summary,
        "raw_source_boundary_copied": False,
        "candidate_rule_enforcement_performed": False,
        "candidate_rule_enforcement_authorized": False,
        "candidate_rule_activation_performed": False,
        "candidate_rule_activation_authorized": False,
        "star_law_candidate_rules_created": False,
        "star_law_candidate_rules_activated": False,
        "star_law_candidate_rules_enforced": False,
        "star_law_rules_created": False,
        "star_law_rules_activated": False,
        "star_law_rules_enforced": False,
        "authorization_granted": False,
        "handoff_authorized": False,
        "scheduling_performed": False,
        "dry_run_performed": False,
        "dry_run_executed": False,
        "durable_memory_write_authorized": False,
        "memory_graph_mutation_authorized": False,
        "operation_ledger_creation_authorized": False,
        "openclaw_execution_authorized": False,
        "approval_granted": False,
        "real_human_decision_recorded": False,
        "civilization_core_complete_claimed": False,
    }


def _non_authorization_boundary(ready: bool) -> dict[str, Any]:
    return {
        "star_law_candidate_rule_enforcement_boundary_proposal_ready_is_self_enforcing_memory_law": False,
        "star_law_candidate_rule_enforcement_boundary_proposal_ready_is_candidate_rule_enforcement": False,
        "star_law_candidate_rule_enforcement_boundary_proposal_ready_is_candidate_rule_activation": False,
        "star_law_candidate_rule_enforcement_boundary_proposal_ready_is_candidate_rule_creation": False,
        "star_law_candidate_rule_enforcement_boundary_proposal_ready_is_rule_creation": False,
        "star_law_candidate_rule_enforcement_boundary_proposal_ready_is_rule_activation": False,
        "star_law_candidate_rule_enforcement_boundary_proposal_ready_is_rule_enforcement": False,
        "star_law_candidate_rule_enforcement_boundary_proposal_ready_is_autonomous_governance": False,
        "star_law_candidate_rule_enforcement_boundary_proposal_ready_is_autonomous_execution": False,
        "star_law_candidate_rule_enforcement_boundary_proposal_ready_is_handoff": False,
        "star_law_candidate_rule_enforcement_boundary_proposal_ready_is_authorization": False,
        "star_law_candidate_rule_enforcement_boundary_proposal_ready_is_scheduling": False,
        "star_law_candidate_rule_enforcement_boundary_proposal_ready_is_dry_run_execution": False,
        "star_law_candidate_rule_enforcement_boundary_proposal_ready_is_approval": False,
        "star_law_candidate_rule_enforcement_boundary_proposal_ready_is_human_decision": False,
        "star_law_candidate_rule_enforcement_boundary_proposal_ready_is_memory_write_permission": False,
        "star_law_candidate_rule_enforcement_boundary_proposal_ready_is_memory_graph_mutation_permission": False,
        "star_law_candidate_rule_enforcement_boundary_proposal_ready_is_operation_ledger_creation": False,
        "star_law_candidate_rule_enforcement_boundary_proposal_ready_is_openclaw_execution_permission": False,
        "star_law_candidate_rule_enforcement_boundary_proposal_ready_is_civilization_core_completion": False,
        "only_permits_later_star_law_candidate_rule_enforcement_boundary_review_gate": ready,
        "human_operator_remains_final_authority": True,
    }


def _preserved_governance_boundaries() -> list[str]:
    return [
        "Star-Law candidate rule enforcement boundary proposal ready is not self-enforcing memory law.",
        "Star-Law candidate rule enforcement boundary proposal ready is not candidate rule enforcement.",
        "Star-Law candidate rule enforcement boundary proposal ready is not candidate rule activation.",
        "Star-Law candidate rule enforcement boundary proposal ready is not candidate rule creation.",
        "Star-Law candidate rule enforcement boundary proposal ready is not Star-Law rule creation.",
        "Star-Law candidate rule enforcement boundary proposal ready is not rule activation.",
        "Star-Law candidate rule enforcement boundary proposal ready is not rule enforcement.",
        "Star-Law candidate rule enforcement boundary proposal ready is not autonomous governance.",
        "Star-Law candidate rule enforcement boundary proposal ready is not autonomous execution.",
        "Star-Law candidate rule enforcement boundary proposal ready is not handoff.",
        "Star-Law candidate rule enforcement boundary proposal ready is not authorization.",
        "Star-Law candidate rule enforcement boundary proposal ready is not scheduling.",
        "Star-Law candidate rule enforcement boundary proposal ready is not dry-run execution.",
        "Star-Law candidate rule enforcement boundary proposal ready is not approval.",
        "Star-Law candidate rule enforcement boundary proposal ready is not a real human decision.",
        "Star-Law candidate rule enforcement boundary proposal ready is not durable memory write permission.",
        "Star-Law candidate rule enforcement boundary proposal ready is not Memory Graph mutation permission.",
        "Star-Law candidate rule enforcement boundary proposal ready is not operation-ledger creation.",
        "Star-Law candidate rule enforcement boundary proposal ready is not OpenClaw execution permission.",
        "Star-Law candidate rule enforcement boundary proposal ready is not Civilization Core completion.",
        "Star-Law candidate rule enforcement boundary proposal ready only permits a later Star-Law candidate rule enforcement boundary review gate.",
        "Human Operator remains final authority.",
    ]


def _future_candidate_rule_enforcement_review_gate_constraints() -> list[str]:
    return [
        "A later Star-Law candidate rule enforcement boundary review gate may inspect this proposal through a separate governed process.",
        "A later candidate rule enforcement boundary review gate must not be treated as automatic candidate rule enforcement, candidate rule activation, candidate rule creation, Star-Law rule creation, rule activation, rule enforcement, approval, handoff, scheduling, memory writing, Memory Graph mutation, operation-ledger creation, OpenClaw execution, GitHub API action, dry-run execution, autonomous execution, or Civilization Core completion.",
        "Any future Star-Law candidate rule enforcement boundary remains inactive until a separate Human Operator governed process reviews an applicable later stage.",
        "Human Operator remains final authority for all future Star-Law governance decisions.",
    ]


def _next_stage_constraints() -> list[str]:
    return [
        "The only next allowed step is v2.36.0 Star-Law candidate rule enforcement boundary review gate.",
        "v2.35.0 is Star-Law candidate rule enforcement boundary proposal only, not candidate rule enforcement, not rule enforcement, and not autonomous execution.",
        "v2.35.0 must not create candidate rules, create Star-Law rules, activate rules, or enforce rules.",
        "v2.35.0 must not authorize Star-Hub handoff, scheduling, approval, dry-run execution, memory writing, Memory Graph mutation, operation-ledger creation, OpenClaw execution, or GitHub API actions.",
        "Mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, and 星源 self-evolution remain out of scope.",
        "Human Operator remains final authority for any future governed action.",
    ]


def _scope_boundaries() -> list[str]:
    return [
        "Civilization Core is the total system.",
        "Fifteen Memory Layers are the highest memory coordinate system.",
        "Subspace Memory System is the engineering carrier.",
        "Hermes, Codex CLI, OpenClaw, Terminal, and GitHub are components, not the core.",
        "This v2.35.0 step is limited to 星律记忆 Star-Law candidate rule enforcement boundary proposal only.",
        "This proposal does not enter mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, or 星源 self-evolution.",
    ]


def _risk_notes(sensitive_field_count: int) -> list[str]:
    notes = [
        "Star-Law candidate rule enforcement boundary proposal ready must not be treated as self-enforcing memory law, candidate rule enforcement, candidate rule activation, candidate rule creation, rule creation, rule activation, rule enforcement, autonomous governance, autonomous execution, handoff, authorization, scheduling, approval, dry-run execution, or Civilization Core completion.",
        "No durable memory write, Memory Graph mutation, operation-ledger entry, GitHub API write, merge, tag creation, approval, request creation, request submission, request execution, human decision record, handoff, scheduling, dry-run performance, dry-run execution, or OpenClaw execution is produced or authorized.",
        "Mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, and 星源 self-evolution are not started.",
    ]
    if sensitive_field_count:
        notes.append(
            "Sensitive fields were omitted from candidate rule enforcement boundary proposal output."
        )
    return notes


def _required_human_actions(status: str, blocking_reasons: list[str]) -> list[str]:
    if status == "star_law_candidate_rule_enforcement_boundary_proposal_ready":
        return [
            "human_operator_must_review_star_law_candidate_rule_enforcement_boundary_proposal_before_any_later_candidate_rule_enforcement_boundary_review_gate",
            "human_operator_must_confirm_candidate_rule_enforcement_boundary_proposal_ready_is_not_self_enforcing_law_candidate_rule_enforcement_candidate_rule_activation_candidate_rule_creation_rule_creation_rule_activation_rule_enforcement_autonomous_execution_handoff_authorization_scheduling_approval_write_execution_or_civilization_core_completion",
            "human_operator_must_use_separate_governed_process_for_any_future_star_law_candidate_rule_enforcement_rule_activation_rule_enforcement_real_approval_write_submission_execution_handoff_scheduling_dry_run_decision_or_next_layer_work",
        ]
    actions = [
        "repair_source_v2_34_0_star_law_candidate_rule_activation_boundary_review_gate_before_proposal_can_continue",
        "confirm_all_candidate_rule_enforcement_candidate_rule_activation_candidate_rule_creation_star_law_rule_creation_rule_activation_rule_enforcement_autonomous_execution_handoff_scheduling_dry_run_write_approval_execution_next_layer_and_civilization_core_completion_flags_remain_false",
        "rerun_local_star_law_candidate_rule_enforcement_boundary_proposal_after_blocking_reasons_are_resolved",
    ]
    if blocking_reasons:
        actions.append(
            "resolve_blocking_reasons_before_star_law_candidate_rule_enforcement_boundary_proposal_can_be_ready"
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
            if nested is True and key not in REVIEWED_BOUNDARY_ALLOWED_TRUE_KEYS:
                return False
    return True


def _proposed_boundaries_remain_proposal_only(value: Mapping[str, Any]) -> bool:
    for boundary in value.values():
        if not isinstance(boundary, Mapping):
            return False
        if boundary.get("proposal_only") is not True:
            return False
        for key, nested in boundary.items():
            if nested is True and key not in BOUNDARY_ALLOWED_TRUE_KEYS:
                return False
    return True


def _unsafe_boundary_claims(value: Any, allowed_true_keys: set[str]) -> list[str]:
    found: list[str] = []
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if nested is True and key not in allowed_true_keys:
                found.append("unsafe_true_boundary_claim")
            if isinstance(nested, str) and _contains_forbidden_boundary_claim(nested):
                found.append("unsafe_text_boundary_claim")
            found.extend(_unsafe_boundary_claims(nested, allowed_true_keys))
    elif isinstance(value, list):
        for nested in value:
            found.extend(_unsafe_boundary_claims(nested, allowed_true_keys))
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
                if str(key).lower() in SENSITIVE_KEYS
                else 0
            )
            + _count_sensitive_keys(nested)
            for key, nested in value.items()
        )
    if isinstance(value, list):
        return sum(_count_sensitive_keys(nested) for nested in value)
    return 0


__all__ = [
    "GOVERNED_STAR_LAW_CANDIDATE_RULE_ENFORCEMENT_BOUNDARY_PROPOSAL_VERSION",
    "PROPOSED_CANDIDATE_RULE_ENFORCEMENT_BOUNDARY_KEYS",
    "PROPOSED_CHAIN_VERSIONS",
    "PROPOSED_STAR_HUB_CHAIN_VERSIONS",
    "READY_NEXT_ALLOWED_STEP",
    "build_governed_star_law_candidate_rule_enforcement_boundary_proposal",
    "governed_star_law_candidate_rule_enforcement_boundary_proposal_to_json",
]
