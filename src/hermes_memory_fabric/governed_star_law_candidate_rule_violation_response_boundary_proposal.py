"""Governed Star-Law candidate rule violation response boundary proposal."""

from __future__ import annotations

import json
from typing import Any, Mapping

from .governed_star_law_candidate_rule_violation_observation_boundary_proposal import (
    PROPOSED_CANDIDATE_RULE_VIOLATION_OBSERVATION_BOUNDARY_KEYS as SOURCE_REVIEWED_CANDIDATE_RULE_VIOLATION_OBSERVATION_BOUNDARY_KEYS,
)
from .governed_star_law_candidate_rule_violation_observation_boundary_review_gate import (
    REVIEWED_CHAIN_VERSIONS as SOURCE_REVIEWED_CHAIN_VERSIONS,
    REVIEWED_STAR_HUB_CHAIN_VERSIONS as SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS,
)


GOVERNED_STAR_LAW_CANDIDATE_RULE_VIOLATION_RESPONSE_BOUNDARY_PROPOSAL_VERSION = "2.39.0"
SOURCE_REVIEW_GATE_VERSION = "2.38.0"

PROPOSED_CHAIN_VERSIONS = [
    *SOURCE_REVIEWED_CHAIN_VERSIONS,
    "v2.38.0",
]

PROPOSED_STAR_HUB_CHAIN_VERSIONS = [
    *SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS,
    "v2.38.0",
]

LAYER_MAPPING = {
    "primary_layer": "星律记忆",
    "primary_layer_status": "Star-Law candidate rule violation response boundary proposal only, not violation response execution, not automated correction, not violation enforcement, and not autonomous execution",
    "source_layer": "星律记忆",
    "source_layer_status": "Star-Law candidate rule violation observation boundary review gate complete for human review only",
    "supporting_layers": ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"],
    "direction": "Star-Law candidate rule violation observation boundary review gate -> Star-Law candidate rule violation response boundary proposal",
}

READY_NEXT_ALLOWED_STEP = (
    "v2.40.0 Star-Law candidate rule violation response boundary review gate"
)
BLOCKED_NEXT_ALLOWED_STEP = (
    "resolve_v2_39_0_star_law_candidate_rule_violation_response_boundary_proposal_blockers"
)

PROPOSAL_FALSE_FLAGS = {
    "candidate_rule_violation_response_performed": False,
    "candidate_rule_violation_response_authorized": False,
    "candidate_rule_violation_response_executed": False,
    "candidate_rule_violation_response_execution_authorized": False,
    "candidate_rule_violation_response_record_created": False,
    "candidate_rule_violation_response_ledger_entry_created": False,
    "automated_correction_performed": False,
    "automated_correction_authorized": False,
    "automated_correction_executed": False,
    "automated_correction_execution_authorized": False,
    "candidate_rule_violation_observation_performed": False,
    "candidate_rule_violation_observation_authorized": False,
    "candidate_rule_violation_observation_executed": False,
    "candidate_rule_violation_observation_execution_authorized": False,
    "candidate_rule_violation_detected": False,
    "candidate_rule_violation_recorded": False,
    "candidate_rule_violation_enforced": False,
    "candidate_rule_violation_ledger_entry_created": False,
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

PROPOSAL_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "proposal_only": True,
    "candidate_rule_violation_response_boundary_proposal_only": True,
    "star_law_candidate_rule_violation_response_boundary_proposal_only": True,
    **PROPOSAL_FALSE_FLAGS,
}

SOURCE_REQUIRED_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "review_gate_only": True,
    "candidate_rule_violation_observation_boundary_review_gate_only": True,
    "star_law_candidate_rule_violation_observation_boundary_review_gate_only": True,
    "candidate_rule_violation_observation_boundary_reviewed_for_human_review_only": True,
    "candidate_rule_violation_response_boundary_proposal_ready_for_human_review_only": True,
    "candidate_rule_violation_observation_performed": False,
    "candidate_rule_violation_observation_authorized": False,
    "candidate_rule_violation_observation_executed": False,
    "candidate_rule_violation_observation_execution_authorized": False,
    "candidate_rule_violation_detected": False,
    "candidate_rule_violation_recorded": False,
    "candidate_rule_violation_enforced": False,
    "candidate_rule_violation_ledger_entry_created": False,
    "candidate_rule_violation_response_performed": False,
    "candidate_rule_violation_response_authorized": False,
    "automated_correction_performed": False,
    "automated_correction_authorized": False,
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

SOURCE_REVIEW_GATE_REQUIRED_FLAGS = {
    "candidate_rule_violation_observation_boundary_reviewed": True,
    "candidate_rule_violation_observation_boundary_structurally_review_ready": True,
    "candidate_rule_violation_response_boundary_proposal_ready_for_human_review_only": True,
    "source_star_law_candidate_rule_violation_observation_boundary_proposal_valid": True,
    "candidate_rule_violation_observation_performed": False,
    "candidate_rule_violation_observation_authorized": False,
    "candidate_rule_violation_observation_executed": False,
    "candidate_rule_violation_observation_execution_authorized": False,
    "candidate_rule_violation_detected": False,
    "candidate_rule_violation_recorded": False,
    "candidate_rule_violation_enforced": False,
    "candidate_rule_violation_ledger_entry_created": False,
    "candidate_rule_violation_response_performed": False,
    "candidate_rule_violation_response_authorized": False,
    "automated_correction_performed": False,
    "automated_correction_authorized": False,
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
}

UNSAFE_TRUE_FIELDS = {
    "candidate_rule_violation_response_performed",
    "candidate_rule_violation_response_authorized",
    "candidate_rule_violation_response_executed",
    "candidate_rule_violation_response_execution_authorized",
    "candidate_rule_violation_response_record_created",
    "candidate_rule_violation_response_ledger_entry_created",
    "violation_response_performed",
    "violation_response_authorized",
    "violation_response_executed",
    "violation_response_record_created",
    "violation_response_ledger_entry_created",
    "automated_correction_performed",
    "automated_correction_authorized",
    "automated_correction_executed",
    "automated_correction_execution_authorized",
    "candidate_rule_violation_observation_performed",
    "candidate_rule_violation_observation_authorized",
    "candidate_rule_violation_observation_executed",
    "candidate_rule_violation_observation_execution_authorized",
    "candidate_rule_violation_detected",
    "candidate_rule_violation_recorded",
    "candidate_rule_violation_enforced",
    "candidate_rule_violation_ledger_entry_created",
    "violation_observation_performed",
    "violation_observation_authorized",
    "violation_observation_executed",
    "violation_observation_execution_authorized",
    "violation_detected",
    "violation_recorded",
    "violation_enforced",
    "violation_record_created",
    "violation_ledger_entry_created",
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

PROPOSED_BOUNDARY_ALLOWED_TRUE_KEYS = {"proposal_only"}
REVIEWED_BOUNDARY_ALLOWED_TRUE_KEYS = {"review_only"}

FORBIDDEN_BOUNDARY_CLAIMS = (
    "violation response is performed",
    "violation response is authorized",
    "violation response is executed",
    "violation response records are created",
    "violation response ledger entries are created",
    "violation responses are performed",
    "violation responses are authorized",
    "automated correction is performed",
    "automated correction is authorized",
    "automated correction is executed",
    "violations are observed",
    "violations are detected",
    "violations are recorded",
    "violations are enforced",
    "violation records are created",
    "violation-ledger entries are created",
    "operation-ledger entries are created",
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

PROPOSED_CANDIDATE_RULE_VIOLATION_RESPONSE_BOUNDARY_KEYS = {
    "violation_response_eligibility_boundary",
    "violation_response_input_scope_boundary",
    "violation_response_output_scope_boundary",
    "violation_response_non_execution_boundary",
    "violation_response_non_authorization_boundary",
    "automated_correction_non_execution_boundary",
    "automated_correction_non_authorization_boundary",
    "violation_enforcement_non_execution_boundary",
    "candidate_rule_enforcement_non_authorization_boundary",
    "human_operator_review_boundary",
    "escalation_review_boundary",
    "false_positive_response_prevention_boundary",
    "rollback_boundary",
    "suspension_boundary",
    "evidence_lineage_boundary",
    "auditability_boundary",
    "non_authorization_boundary",
    "memory_write_boundary",
    "memory_graph_boundary",
    "operation_ledger_boundary",
    "violation_response_ledger_boundary",
    "openclaw_boundary",
    "approval_boundary",
    "future_review_gate_boundary",
}

PROPOSAL_COMPONENTS = {
    "source_candidate_rule_violation_observation_boundary_review_gate",
    "violation_response_eligibility_boundary",
    "violation_response_input_boundary",
    "violation_response_output_boundary",
    "violation_response_non_execution_boundary",
    "violation_response_non_authorization_boundary",
    "automated_correction_non_execution_boundary",
    "automated_correction_non_authorization_boundary",
    "violation_enforcement_non_execution_boundary",
    "candidate_rule_enforcement_non_authorization_boundary",
    "human_operator_review_boundary",
    "escalation_review_boundary",
    "false_positive_response_prevention_boundary",
    "rollback_boundary",
    "suspension_boundary",
    "evidence_lineage_boundary",
    "auditability_boundary",
    "memory_write_non_authorization_boundary",
    "memory_graph_mutation_non_authorization_boundary",
    "operation_ledger_non_creation_boundary",
    "violation_response_ledger_non_creation_boundary",
    "openclaw_execution_non_authorization_boundary",
    "approval_non_authorization_boundary",
    "human_operator_final_authority_boundary",
    "fifteen_memory_layers_boundary",
}


def build_governed_star_law_candidate_rule_violation_response_boundary_proposal(
    review_gate_report: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a local-only, non-authorizing candidate rule violation response boundary proposal."""

    checks, blocking_reasons = _proposal_checks(review_gate_report)
    sensitive_field_count = _count_sensitive_keys(review_gate_report)
    blocking_reasons = list(dict.fromkeys(blocking_reasons))
    status = (
        "star_law_candidate_rule_violation_response_boundary_proposal_ready"
        if not blocking_reasons
        else "blocked"
    )
    ready = (
        status
        == "star_law_candidate_rule_violation_response_boundary_proposal_ready"
    )

    return {
        "version": GOVERNED_STAR_LAW_CANDIDATE_RULE_VIOLATION_RESPONSE_BOUNDARY_PROPOSAL_VERSION,
        "status": status,
        **PROPOSAL_FLAGS,
        "candidate_rule_violation_response_boundary_proposed_for_human_review_only": ready,
        "candidate_rule_violation_response_boundary_review_gate_ready_for_human_review_only": ready,
        "civilization_core_layer_mapping": dict(LAYER_MAPPING),
        "source_review_gate_version": SOURCE_REVIEW_GATE_VERSION,
        "proposed_chain_versions": list(PROPOSED_CHAIN_VERSIONS),
        "proposed_star_hub_chain_versions": list(PROPOSED_STAR_HUB_CHAIN_VERSIONS),
        "star_law_candidate_rule_violation_response_boundary_proposal_summary": (
            _proposal_summary(ready)
        ),
        "proposal_checks": checks,
        "source_review_gate_summary": _source_review_gate_summary(ready),
        "star_law_candidate_rule_violation_response_boundary_proposal": (
            _star_law_candidate_rule_violation_response_boundary_proposal(ready)
        ),
        "proposed_candidate_rule_violation_response_boundaries": (
            _proposed_candidate_rule_violation_response_boundaries(ready)
        ),
        "non_authorization_boundary": _non_authorization_boundary(ready),
        "preserved_governance_boundaries": _preserved_governance_boundaries(),
        "future_candidate_rule_violation_response_review_gate_constraints": (
            _future_candidate_rule_violation_response_review_gate_constraints()
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


def governed_star_law_candidate_rule_violation_response_boundary_proposal_to_json(
    report: Mapping[str, Any],
) -> str:
    """Serialize a Star-Law candidate rule violation response boundary proposal deterministically."""

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
        "source_review_gate_version_must_be_2_38_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_review_gate_status_ready",
        report.get("status")
        == "star_law_candidate_rule_violation_observation_boundary_review_gate_ready",
        "source_review_gate_status_must_be_star_law_candidate_rule_violation_observation_boundary_review_gate_ready",
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
        "source_must_not_claim_violation_response_response_authorization_response_execution_response_record_response_ledger_automated_correction_violation_observation_violation_detection_violation_recording_violation_enforcement_violation_ledger_candidate_rule_enforcement_candidate_rule_activation_candidate_rule_creation_star_law_rule_creation_activation_enforcement_self_enforcing_law_autonomous_execution_handoff_scheduling_approval_write_execution_dry_run_or_civilization_core_completion",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_no_unsafe_text_claims",
        _unsafe_text_claims(report) == [],
        "source_must_not_textually_claim_violation_response_automated_correction_violation_observation_detection_recording_enforcement_violation_ledger_candidate_rule_enforcement_candidate_rule_activation_candidate_rule_creation_star_law_rule_creation_activation_enforcement_self_enforcing_law_autonomous_execution_write_approval_next_layer_or_civilization_core_completion",
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
            == "Star-Law candidate rule violation observation boundary review gate only, not violation observation execution, not violation detection, not violation recording, not violation enforcement, and not autonomous execution",
            "source_primary_layer_status_must_be_candidate_rule_violation_observation_boundary_review_gate_only_not_violation_observation_execution_detection_recording_enforcement_or_autonomous_execution",
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
            == "Star-Law candidate rule violation observation boundary proposal complete for human review only",
            "source_source_layer_status_must_be_candidate_rule_violation_observation_boundary_proposal_complete_for_human_review_only",
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
            == "Star-Law candidate rule violation observation boundary proposal -> Star-Law candidate rule violation observation boundary review gate",
            "source_direction_must_be_candidate_rule_violation_observation_boundary_proposal_to_candidate_rule_violation_observation_boundary_review_gate",
        )

    _add_check(
        checks,
        blocking_reasons,
        "source_reviewed_chain_versions",
        report.get("reviewed_chain_versions") == SOURCE_REVIEWED_CHAIN_VERSIONS,
        "source_reviewed_chain_versions_must_exactly_match_v2_9_0_through_v2_37_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_reviewed_star_hub_chain_versions",
        report.get("reviewed_star_hub_chain_versions")
        == SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS,
        "source_reviewed_star_hub_chain_versions_must_exactly_match_v2_19_0_through_v2_37_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_next_allowed_step",
        report.get("next_allowed_step")
        == "v2.39.0 Star-Law candidate rule violation response boundary proposal",
        "source_next_allowed_step_must_be_v2_39_0_star_law_candidate_rule_violation_response_boundary_proposal",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_blocking_reasons_empty",
        report.get("blocking_reasons") == [],
        "source_blocking_reasons_must_be_empty",
    )

    review_gate = report.get(
        "star_law_candidate_rule_violation_observation_boundary_review_gate"
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_star_law_candidate_rule_violation_observation_boundary_review_gate_shape",
        isinstance(review_gate, Mapping),
        "source_star_law_candidate_rule_violation_observation_boundary_review_gate_must_be_mapping",
    )
    if isinstance(review_gate, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_candidate_rule_violation_observation_boundary_review_gate_status",
            review_gate.get("review_status")
            == "star_law_candidate_rule_violation_observation_boundary_reviewed_for_human_review_only",
            "source_candidate_rule_violation_observation_boundary_review_gate_status_must_be_human_review_only",
        )
        for key, expected in SOURCE_REVIEW_GATE_REQUIRED_FLAGS.items():
            _add_check(
                checks,
                blocking_reasons,
                f"source_candidate_rule_violation_observation_boundary_review_gate_{key}",
                review_gate.get(key) is expected,
                f"source_candidate_rule_violation_observation_boundary_review_gate_{key}_must_be_{str(expected).lower()}",
            )

    reviewed_boundaries = report.get(
        "reviewed_candidate_rule_violation_observation_boundaries"
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_reviewed_candidate_rule_violation_observation_boundaries_shape",
        isinstance(reviewed_boundaries, Mapping),
        "source_reviewed_candidate_rule_violation_observation_boundaries_must_be_mapping",
    )
    if isinstance(reviewed_boundaries, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_reviewed_candidate_rule_violation_observation_boundaries_required_keys",
            set(reviewed_boundaries)
            == SOURCE_REVIEWED_CANDIDATE_RULE_VIOLATION_OBSERVATION_BOUNDARY_KEYS,
            "source_reviewed_candidate_rule_violation_observation_boundaries_must_exactly_match_required_boundaries",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_reviewed_candidate_rule_violation_observation_boundaries_review_only",
            _reviewed_boundaries_remain_review_only(reviewed_boundaries),
            "source_reviewed_candidate_rule_violation_observation_boundaries_must_remain_review_only_and_non_authorizing",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_reviewed_candidate_rule_violation_observation_boundaries_no_unsafe_claims",
            _unsafe_boundary_claims(
                reviewed_boundaries, REVIEWED_BOUNDARY_ALLOWED_TRUE_KEYS
            )
            == [],
            "source_reviewed_candidate_rule_violation_observation_boundaries_must_not_claim_violation_response_automated_correction_violation_observation_detection_recording_enforcement_violation_ledger_candidate_rule_enforcement_candidate_rule_activation_candidate_rule_creation_rule_creation_activation_enforcement_authorization_self_execution_autonomous_execution_or_memory_writing",
        )

    return checks, blocking_reasons


def _proposal_summary(ready: bool) -> dict[str, Any]:
    return {
        "proposal_status": (
            "star_law_candidate_rule_violation_response_boundary_proposed_for_human_review_only"
            if ready
            else "blocked"
        ),
        "source_review_gate_version": SOURCE_REVIEW_GATE_VERSION,
        "source_star_law_candidate_rule_violation_observation_boundary_review_gate_valid": ready,
        "candidate_rule_violation_response_boundary_proposed_for_human_review_only": ready,
        "candidate_rule_violation_response_boundary_review_gate_ready_for_human_review_only": ready,
        "non_violation_response_performing": True,
        "non_violation_response_authorizing": True,
        "non_violation_response_executing": True,
        "non_violation_response_record_creating": True,
        "non_violation_response_ledger_creating": True,
        "non_automated_correction": True,
        "non_violation_observing": True,
        "non_violation_detecting": True,
        "non_violation_recording": True,
        "non_violation_enforcing": True,
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
        "only_permits_later_star_law_candidate_rule_violation_response_boundary_review_gate": ready,
    }


def _source_review_gate_summary(ready: bool) -> dict[str, Any]:
    return {
        "source_review_gate_version": SOURCE_REVIEW_GATE_VERSION,
        "source_review_gate_status": (
            "star_law_candidate_rule_violation_observation_boundary_review_gate_ready"
            if ready
            else "blocked"
        ),
        "source_chain_versions": list(SOURCE_REVIEWED_CHAIN_VERSIONS),
        "source_star_hub_chain_versions": list(
            SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS
        ),
        "source_candidate_rule_violation_observation_boundary_review_gate_ready": ready,
        "source_review_gate_authorized_violation_response": False,
        "source_review_gate_executed_violation_response": False,
        "source_review_gate_created_violation_response_record": False,
        "source_review_gate_created_violation_response_ledger_entry": False,
        "source_review_gate_authorized_automated_correction": False,
        "source_review_gate_executed_automated_correction": False,
        "source_review_gate_authorized_violation_observation": False,
        "source_review_gate_authorized_violation_detection": False,
        "source_review_gate_authorized_violation_recording": False,
        "source_review_gate_authorized_violation_enforcement": False,
        "source_review_gate_created_violation_ledger_entry": False,
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


def _star_law_candidate_rule_violation_response_boundary_proposal(
    ready: bool,
) -> dict[str, Any]:
    return {
        "proposal_status": (
            "star_law_candidate_rule_violation_response_boundary_proposed_for_human_review_only"
            if ready
            else "blocked_no_star_law_candidate_rule_violation_response_boundary_proposal_readiness_claim"
        ),
        "boundary_type": "star_law_candidate_rule_violation_response_boundary_proposal",
        "source_review_gate_version": SOURCE_REVIEW_GATE_VERSION,
        "candidate_rule_violation_response_boundary_proposed": ready,
        "candidate_rule_violation_response_boundary_review_gate_ready_for_human_review_only": ready,
        "source_star_law_candidate_rule_violation_observation_boundary_review_gate_valid": ready,
        "candidate_rule_violation_response_performed": False,
        "candidate_rule_violation_response_authorized": False,
        "candidate_rule_violation_response_executed": False,
        "candidate_rule_violation_response_execution_authorized": False,
        "candidate_rule_violation_response_record_created": False,
        "candidate_rule_violation_response_ledger_entry_created": False,
        "automated_correction_performed": False,
        "automated_correction_authorized": False,
        "automated_correction_executed": False,
        "automated_correction_execution_authorized": False,
        "candidate_rule_violation_observation_performed": False,
        "candidate_rule_violation_observation_authorized": False,
        "candidate_rule_violation_observation_executed": False,
        "candidate_rule_violation_observation_execution_authorized": False,
        "candidate_rule_violation_detected": False,
        "candidate_rule_violation_recorded": False,
        "candidate_rule_violation_enforced": False,
        "candidate_rule_violation_ledger_entry_created": False,
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
        "star_law_candidate_rule_violation_response_boundary_components": (
            _proposal_components(ready)
        ),
        "next_allowed_step": READY_NEXT_ALLOWED_STEP
        if ready
        else BLOCKED_NEXT_ALLOWED_STEP,
        "non_authorization_notice": (
            "The Star-Law candidate rule violation response boundary has been proposed for human review only. "
            "A later response boundary review gate is structurally allowed as the next governed step. "
            "This proposal performs no candidate-rule violation response, authorizes no candidate-rule violation response, executes no candidate-rule violation response, authorizes no candidate-rule violation response execution, creates no candidate-rule violation response record, creates no candidate-rule violation response ledger entry, performs no automated correction, authorizes no automated correction, executes no automated correction, authorizes no automated correction execution, performs no candidate-rule violation observation, authorizes no candidate-rule violation observation, executes no candidate-rule violation observation, authorizes no candidate-rule violation observation execution, performs no violation detection, records no violation artifact, performs no violation enforcement, creates no violation ledger artifact, performs no candidate rule enforcement, authorizes no candidate rule enforcement, performs no candidate rule activation, authorizes no candidate rule activation, creates no candidate Star-Law rules, activates no candidate Star-Law rules, enforces no candidate Star-Law rules, creates no Star-Law rules, activates no rules, enforces no rules, creates no self-enforcing memory law, creates no autonomous governance, authorizes no autonomous execution, creates no self-executing policy, grants no approval, records no real human decision, performs no handoff, schedules nothing, performs no dry-run, executes no dry-run plan, writes no durable memory, mutates no Memory Graph, creates no operation-ledger entry, calls no OpenClaw or GitHub API, claims no Civilization Core completion, starts no 星魂 continuity, starts no 星宙 evolution, and starts no 星源 self-evolution."
            if ready
            else "The Star-Law candidate rule violation response boundary proposal is blocked; no readiness, response, automated correction, observation, detection, recording, enforcement, ledger, authorization, candidate rule enforcement, candidate rule activation, candidate rule creation, rule creation, rule activation, rule enforcement, autonomous execution, handoff, scheduling, approval, write, execution, dry-run, next-layer, or Civilization Core completion claim is made."
        ),
    }


def _proposal_components(ready: bool) -> dict[str, str]:
    status = "proposed_for_human_review_only" if ready else "blocked"
    return {component: status for component in sorted(PROPOSAL_COMPONENTS)}


def _proposed_candidate_rule_violation_response_boundaries(
    ready: bool,
) -> dict[str, dict[str, Any]]:
    status = "proposed_for_human_review_only" if ready else "blocked"
    summaries = {
        "violation_response_eligibility_boundary": "Defines future eligibility categories before any later human-operated review-gate work.",
        "violation_response_input_scope_boundary": "Limits future inputs to sanitized source review-gate status, chain versions, and governance flags.",
        "violation_response_output_scope_boundary": "Limits future outputs to non-authorizing boundary status and explanatory categories.",
        "violation_response_non_execution_boundary": "Prevents any response execution in this proposal stage.",
        "violation_response_non_authorization_boundary": "Prevents any response authority from this proposal stage.",
        "automated_correction_non_execution_boundary": "Prevents automated correction execution in this proposal stage.",
        "automated_correction_non_authorization_boundary": "Prevents automated correction authority from this proposal stage.",
        "violation_enforcement_non_execution_boundary": "Prevents any violation enforcement action in this proposal stage.",
        "candidate_rule_enforcement_non_authorization_boundary": "Prevents candidate rule enforcement authority from this proposal stage.",
        "human_operator_review_boundary": "Requires Human Operator review before any later governed stage.",
        "escalation_review_boundary": "Keeps escalation review as a later human-operated review concern only.",
        "false_positive_response_prevention_boundary": "Requires later human review of false-positive handling before any operational use.",
        "rollback_boundary": "Defines rollback category review for a future system without performing rollback.",
        "suspension_boundary": "Defines suspension category review for a future system without performing suspension.",
        "evidence_lineage_boundary": "Keeps evidence lineage limited to source version, chain versions, and structural gate status.",
        "auditability_boundary": "Keeps auditability deterministic, local-only, and limited to sanitized structural output.",
        "non_authorization_boundary": "States this proposal grants no authority for response, correction, enforcement, writes, execution, or approvals.",
        "memory_write_boundary": "Prevents durable memory write permission in this proposal stage.",
        "memory_graph_boundary": "Prevents Memory Graph mutation permission in this proposal stage.",
        "operation_ledger_boundary": "Prevents operation-ledger creation permission in this proposal stage.",
        "violation_response_ledger_boundary": "Prevents response-ledger artifact creation in this proposal stage.",
        "openclaw_boundary": "Prevents OpenClaw execution permission in this proposal stage.",
        "approval_boundary": "Prevents approval request creation, submission, execution, or grant in this proposal stage.",
        "future_review_gate_boundary": "Allows only a later governed Star-Law candidate rule violation response boundary review gate.",
    }
    return {
        key: _proposed_boundary(status, summaries[key])
        for key in sorted(PROPOSED_CANDIDATE_RULE_VIOLATION_RESPONSE_BOUNDARY_KEYS)
    }


def _proposed_boundary(status: str, summary: str) -> dict[str, Any]:
    return {
        "proposal_only": True,
        "boundary_status": status,
        "summary": summary,
        "raw_source_boundary_copied": False,
        "candidate_rule_violation_response_performed": False,
        "candidate_rule_violation_response_authorized": False,
        "candidate_rule_violation_response_executed": False,
        "candidate_rule_violation_response_execution_authorized": False,
        "candidate_rule_violation_response_record_created": False,
        "candidate_rule_violation_response_ledger_entry_created": False,
        "automated_correction_performed": False,
        "automated_correction_authorized": False,
        "automated_correction_executed": False,
        "automated_correction_execution_authorized": False,
        "candidate_rule_violation_observation_performed": False,
        "candidate_rule_violation_observation_authorized": False,
        "candidate_rule_violation_observation_executed": False,
        "candidate_rule_violation_observation_execution_authorized": False,
        "candidate_rule_violation_detected": False,
        "candidate_rule_violation_recorded": False,
        "candidate_rule_violation_enforced": False,
        "candidate_rule_violation_ledger_entry_created": False,
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
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_self_enforcing_memory_law": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_violation_response_execution": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_violation_response_authorization": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_violation_response_record_creation": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_violation_response_ledger_creation": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_automated_correction": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_automated_correction_authorization": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_violation_observation_execution": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_violation_detection": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_violation_recording": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_violation_enforcement": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_violation_ledger_creation": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_candidate_rule_enforcement": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_candidate_rule_enforcement_authorization": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_candidate_rule_activation": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_candidate_rule_creation": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_rule_creation": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_rule_activation": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_rule_enforcement": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_autonomous_governance": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_autonomous_execution": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_handoff": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_authorization": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_scheduling": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_dry_run_execution": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_approval": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_human_decision": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_memory_write_permission": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_memory_graph_mutation_permission": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_operation_ledger_creation": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_openclaw_execution_permission": False,
        "star_law_candidate_rule_violation_response_boundary_proposal_ready_is_civilization_core_completion": False,
        "only_permits_later_star_law_candidate_rule_violation_response_boundary_review_gate": ready,
        "human_operator_remains_final_authority": True,
    }


def _preserved_governance_boundaries() -> list[str]:
    return [
        "Star-Law candidate rule violation response boundary proposal ready is not self-enforcing memory law.",
        "Star-Law candidate rule violation response boundary proposal ready is not violation response execution.",
        "Star-Law candidate rule violation response boundary proposal ready is not violation response authorization.",
        "Star-Law candidate rule violation response boundary proposal ready is not automated correction.",
        "Star-Law candidate rule violation response boundary proposal ready is not automated correction authorization.",
        "Star-Law candidate rule violation response boundary proposal ready is not violation observation execution.",
        "Star-Law candidate rule violation response boundary proposal ready is not violation detection.",
        "Star-Law candidate rule violation response boundary proposal ready is not violation recording.",
        "Star-Law candidate rule violation response boundary proposal ready is not violation enforcement.",
        "Star-Law candidate rule violation response boundary proposal ready is not violation-ledger creation.",
        "Star-Law candidate rule violation response boundary proposal ready is not candidate rule enforcement.",
        "Star-Law candidate rule violation response boundary proposal ready is not candidate rule enforcement authorization.",
        "Star-Law candidate rule violation response boundary proposal ready is not candidate rule activation.",
        "Star-Law candidate rule violation response boundary proposal ready is not candidate rule creation.",
        "Star-Law candidate rule violation response boundary proposal ready is not Star-Law rule creation.",
        "Star-Law candidate rule violation response boundary proposal ready is not rule activation.",
        "Star-Law candidate rule violation response boundary proposal ready is not rule enforcement.",
        "Star-Law candidate rule violation response boundary proposal ready is not autonomous governance.",
        "Star-Law candidate rule violation response boundary proposal ready is not autonomous execution.",
        "Star-Law candidate rule violation response boundary proposal ready is not handoff.",
        "Star-Law candidate rule violation response boundary proposal ready is not authorization.",
        "Star-Law candidate rule violation response boundary proposal ready is not scheduling.",
        "Star-Law candidate rule violation response boundary proposal ready is not dry-run execution.",
        "Star-Law candidate rule violation response boundary proposal ready is not approval.",
        "Star-Law candidate rule violation response boundary proposal ready is not a real human decision.",
        "Star-Law candidate rule violation response boundary proposal ready is not durable memory write permission.",
        "Star-Law candidate rule violation response boundary proposal ready is not Memory Graph mutation permission.",
        "Star-Law candidate rule violation response boundary proposal ready is not operation-ledger creation.",
        "Star-Law candidate rule violation response boundary proposal ready is not OpenClaw execution permission.",
        "Star-Law candidate rule violation response boundary proposal ready is not Civilization Core completion.",
        "Star-Law candidate rule violation response boundary proposal ready only permits a later Star-Law candidate rule violation response boundary review gate.",
        "Human Operator remains final authority.",
    ]


def _future_candidate_rule_violation_response_review_gate_constraints() -> list[str]:
    return [
        "A later Star-Law candidate rule violation response boundary review gate may structurally review this proposal through a separate governed process.",
        "A later review gate must not be treated as violation response execution, violation response authorization, response record creation, response ledger creation, automated correction, automated correction authorization, violation observation execution, violation detection, violation recording, violation enforcement, candidate rule enforcement, candidate rule activation, candidate rule creation, Star-Law rule creation, rule activation, rule enforcement, approval, handoff, scheduling, memory writing, Memory Graph mutation, operation-ledger creation, OpenClaw execution, GitHub API action, dry-run execution, autonomous execution, or Civilization Core completion.",
        "Any future Star-Law candidate rule violation response boundary remains inactive until a separate Human Operator governed process reviews an applicable later stage.",
        "Human Operator remains final authority for all future Star-Law governance decisions.",
    ]


def _next_stage_constraints() -> list[str]:
    return [
        "The only next allowed step is v2.40.0 Star-Law candidate rule violation response boundary review gate.",
        "v2.39.0 is Star-Law candidate rule violation response boundary proposal only, not violation response execution, not automated correction, not violation enforcement, and not autonomous execution.",
        "v2.39.0 must not create candidate rules, create Star-Law rules, activate rules, or enforce rules.",
        "v2.39.0 must not authorize Star-Hub handoff, scheduling, approval, dry-run execution, memory writing, Memory Graph mutation, operation-ledger creation, OpenClaw execution, or GitHub API actions.",
        "Mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, and 星源 self-evolution remain out of scope.",
        "Human Operator remains final authority for any future governed action.",
    ]


def _scope_boundaries() -> list[str]:
    return [
        "Civilization Core is the total system.",
        "Fifteen Memory Layers are the highest memory coordinate system.",
        "Subspace Memory System is the engineering carrier.",
        "Hermes, Codex CLI, OpenClaw, Terminal, and GitHub are components, not the core.",
        "This v2.39.0 step is limited to 星律记忆 Star-Law candidate rule violation response boundary proposal only.",
        "This proposal does not enter mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, or 星源 self-evolution.",
    ]


def _risk_notes(sensitive_field_count: int) -> list[str]:
    notes = [
        "Star-Law candidate rule violation response boundary proposal ready must not be treated as self-enforcing memory law, violation response execution, violation response authorization, response record creation, response ledger creation, automated correction, automated correction authorization, violation observation execution, violation detection, violation recording, violation enforcement, violation-ledger creation, candidate rule enforcement, candidate rule enforcement authorization, candidate rule activation, candidate rule creation, rule creation, rule activation, rule enforcement, autonomous governance, autonomous execution, handoff, authorization, scheduling, approval, dry-run execution, or Civilization Core completion.",
        "No durable memory write, Memory Graph mutation, operation-ledger entry, GitHub API write, merge, tag creation, approval, request creation, request submission, request execution, human decision record, handoff, scheduling, dry-run performance, dry-run execution, or OpenClaw execution is produced or authorized.",
        "Mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, and 星源 self-evolution are not started.",
    ]
    if sensitive_field_count:
        notes.append(
            "Sensitive fields were omitted from candidate rule violation response boundary proposal output."
        )
    return notes


def _required_human_actions(status: str, blocking_reasons: list[str]) -> list[str]:
    if (
        status
        == "star_law_candidate_rule_violation_response_boundary_proposal_ready"
    ):
        return [
            "human_operator_must_review_star_law_candidate_rule_violation_response_boundary_proposal_before_any_later_candidate_rule_violation_response_boundary_review_gate",
            "human_operator_must_confirm_candidate_rule_violation_response_boundary_proposal_ready_is_not_self_enforcing_law_violation_response_violation_response_authorization_violation_response_execution_response_record_response_ledger_automated_correction_violation_observation_violation_detection_violation_recording_violation_enforcement_candidate_rule_enforcement_candidate_rule_enforcement_authorization_candidate_rule_activation_candidate_rule_creation_rule_creation_rule_activation_rule_enforcement_autonomous_execution_handoff_authorization_scheduling_approval_write_execution_or_civilization_core_completion",
            "human_operator_must_use_separate_governed_process_for_any_future_star_law_violation_response_automated_correction_violation_observation_violation_detection_violation_recording_violation_enforcement_candidate_rule_enforcement_rule_activation_rule_enforcement_real_approval_write_submission_execution_handoff_scheduling_dry_run_decision_or_next_layer_work",
        ]
    actions = [
        "repair_source_v2_38_0_star_law_candidate_rule_violation_observation_boundary_review_gate_before_proposal_can_continue",
        "confirm_all_violation_response_response_authorization_response_execution_response_record_response_ledger_automated_correction_violation_observation_violation_detection_violation_recording_violation_enforcement_candidate_rule_enforcement_candidate_rule_activation_candidate_rule_creation_star_law_rule_creation_rule_activation_rule_enforcement_autonomous_execution_handoff_scheduling_dry_run_write_approval_execution_next_layer_and_civilization_core_completion_flags_remain_false",
        "rerun_local_star_law_candidate_rule_violation_response_boundary_proposal_after_blocking_reasons_are_resolved",
    ]
    if blocking_reasons:
        actions.append(
            "resolve_blocking_reasons_before_star_law_candidate_rule_violation_response_boundary_proposal_can_be_ready"
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
            if nested is True and key not in PROPOSED_BOUNDARY_ALLOWED_TRUE_KEYS:
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
            (1 if str(key).lower() in SENSITIVE_KEYS else 0)
            + _count_sensitive_keys(nested)
            for key, nested in value.items()
        )
    if isinstance(value, list):
        return sum(_count_sensitive_keys(nested) for nested in value)
    return 0


__all__ = [
    "GOVERNED_STAR_LAW_CANDIDATE_RULE_VIOLATION_RESPONSE_BOUNDARY_PROPOSAL_VERSION",
    "PROPOSED_CANDIDATE_RULE_VIOLATION_RESPONSE_BOUNDARY_KEYS",
    "PROPOSED_CHAIN_VERSIONS",
    "PROPOSED_STAR_HUB_CHAIN_VERSIONS",
    "READY_NEXT_ALLOWED_STEP",
    "build_governed_star_law_candidate_rule_violation_response_boundary_proposal",
    "governed_star_law_candidate_rule_violation_response_boundary_proposal_to_json",
]
