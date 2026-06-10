"""Governed Star-Law candidate rule violation response audit completion attestation completion finalization boundary review gate."""

from __future__ import annotations

import json
from typing import Any, Mapping

from .governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal import (
    PROPOSAL_FALSE_FLAGS as SOURCE_PROPOSAL_FALSE_FLAGS,
    PROPOSAL_OBJECT_FALSE_FLAGS as SOURCE_PROPOSAL_OBJECT_FALSE_FLAGS,
    PROPOSED_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_COMPLETION_ATTESTATION_COMPLETION_FINALIZATION_BOUNDARY_KEYS as SOURCE_PROPOSED_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_COMPLETION_ATTESTATION_COMPLETION_FINALIZATION_BOUNDARY_KEYS,
    PROPOSED_CHAIN_VERSIONS as SOURCE_PROPOSED_CHAIN_VERSIONS,
    PROPOSED_STAR_HUB_CHAIN_VERSIONS as SOURCE_PROPOSED_STAR_HUB_CHAIN_VERSIONS,
    SENSITIVE_KEYS,
)


GOVERNED_STAR_LAW_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_COMPLETION_ATTESTATION_COMPLETION_FINALIZATION_BOUNDARY_REVIEW_GATE_VERSION = (
    "2.60.0"
)
SOURCE_PROPOSAL_VERSION = "2.59.0"

REVIEWED_CHAIN_VERSIONS = [*SOURCE_PROPOSED_CHAIN_VERSIONS, "v2.59.0"]
REVIEWED_STAR_HUB_CHAIN_VERSIONS = [
    *SOURCE_PROPOSED_STAR_HUB_CHAIN_VERSIONS,
    "v2.59.0",
]

LAYER_MAPPING = {
    "primary_layer": "星律记忆",
    "primary_layer_status": "Star-Law candidate rule violation response audit completion attestation completion finalization boundary review gate only, not finalization execution, not finalization record creation, not finalization-ledger creation, not completion execution, not completion record creation, not completion-ledger creation, not closure execution, not closure record creation, not closure-ledger creation, not attestation execution, not attestation record creation, not attestation-ledger creation, not audit execution, not audit logging, not audit record creation, not audit-ledger creation, not violation response execution, not automated correction, not violation enforcement, not autonomous execution, and not Star-Soul transition execution",
    "source_layer": "星律记忆",
    "source_layer_status": "Star-Law candidate rule violation response audit completion attestation completion finalization boundary proposal complete for human review only",
    "supporting_layers": ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"],
    "direction": "Star-Law candidate rule violation response audit completion attestation completion finalization boundary proposal -> Star-Law candidate rule violation response audit completion attestation completion finalization boundary review gate",
    "hard_boundary": "v2.60.0 is the final v2.x Star-Law memory layer review gate before a later separate v3.0.0 Star-Soul Memory continuity boundary proposal",
}

READY_NEXT_ALLOWED_STEP = (
    "v3.0.0 Star-Soul Memory continuity boundary proposal"
)

REVIEW_GATE_FALSE_FLAGS = {
    **SOURCE_PROPOSAL_FALSE_FLAGS,
    "finalization_performed": False,
    "finalization_authorized": False,
    "finalization_executed": False,
    "finalization_record_written": False,
    "finalization_ledger_entry_written": False,
    "completion_performed": False,
    "completion_authorized": False,
    "completion_executed": False,
    "completion_record_written": False,
    "completion_ledger_entry_written": False,
    "closure_performed": False,
    "closure_authorized": False,
    "closure_executed": False,
    "closure_record_written": False,
    "closure_ledger_entry_written": False,
    "attestation_performed": False,
    "attestation_authorized": False,
    "attestation_executed": False,
    "attestation_record_written": False,
    "attestation_ledger_entry_written": False,
    "audit_log_written": False,
    "audit_record_written": False,
    "audit_ledger_entry_written": False,
    "violation_response_audit_performed": False,
    "violation_response_audit_authorized": False,
    "violation_response_audit_executed": False,
    "violation_response_audit_execution_authorized": False,
    "violation_response_audit_log_created": False,
    "violation_response_audit_record_created": False,
    "violation_response_audit_ledger_entry_created": False,
    "candidate_rules_created": False,
    "candidate_rules_activated": False,
    "candidate_rules_enforced": False,
    "star_hub_scheduling_authorized": False,
    "star_hub_scheduling_executed": False,
    "github_api_called": False,
    "openclaw_called": False,
    "operation_ledger_entry_created": False,
    "star_soul_transition_executed": False,
    "star_soul_transition_authorized": False,
    "enters_thirteenth_memory_layer": False,
    "thirteenth_memory_layer_transition_authorized": False,
    "v3_created": False,
    "v3_authorized": False,
}
REVIEW_OBJECT_FALSE_FLAGS = {
    **REVIEW_GATE_FALSE_FLAGS,
    "durable_memory_write_authorized": False,
    "memory_graph_mutation_authorized": False,
    "operation_ledger_creation_authorized": False,
    "approval_authorized": False,
    "real_human_decision_recorded": False,
}

REVIEW_GATE_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "review_gate_only": True,
    "candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate_only": True,
    "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate_only": True,
    **REVIEW_GATE_FALSE_FLAGS,
}

SOURCE_REQUIRED_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "proposal_only": True,
    "candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal_only": True,
    "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal_only": True,
    "candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposed_for_human_review_only": True,
    "candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate_ready_for_human_review_only": True,
    **SOURCE_PROPOSAL_FALSE_FLAGS,
}

SOURCE_PROPOSAL_OBJECT_REQUIRED_FLAGS = {
    "candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposed": True,
    "candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate_ready_for_human_review_only": True,
    "source_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate_valid": True,
    **SOURCE_PROPOSAL_OBJECT_FALSE_FLAGS,
}

UNSAFE_TRUE_FIELDS = {
    *REVIEW_GATE_FALSE_FLAGS,
    *REVIEW_OBJECT_FALSE_FLAGS,
    "attestation_performed",
    "attestation_authorized",
    "attestation_executed",
    "attestation_record_written",
    "attestation_ledger_entry_written",
    "completion_performed",
    "completion_authorized",
    "completion_executed",
    "completion_record_written",
    "completion_ledger_entry_written",
    "finalization_performed",
    "finalization_authorized",
    "finalization_executed",
    "finalization_record_written",
    "finalization_ledger_entry_written",
    "closure_performed",
    "closure_authorized",
    "closure_executed",
    "closure_record_written",
    "closure_ledger_entry_written",
    "audit_log_written",
    "audit_record_written",
    "audit_ledger_entry_written",
    "violation_response_audit_performed",
    "violation_response_audit_authorized",
    "violation_response_audit_executed",
    "violation_response_audit_execution_authorized",
    "violation_response_audit_log_created",
    "violation_response_audit_record_created",
    "violation_response_audit_ledger_entry_created",
    "candidate_rules_created",
    "candidate_rules_activated",
    "candidate_rules_enforced",
    "candidate_rule_enforcement_boundary_proposal_authorized",
    "candidate_rule_enforcement_boundary_review_gate_authorized",
    "candidate_rule_activation_boundary_proposal_authorized",
    "candidate_rule_activation_boundary_review_gate_authorized",
    "star_hub_scheduling_authorized",
    "star_hub_scheduling_executed",
    "candidate_rule_violation_response_audit_boundary_attestation_executed",
    "candidate_rule_violation_response_audit_boundary_completion_executed",
    "candidate_rule_violation_response_audit_boundary_closure_executed",
    "candidate_rule_violation_response_audit_boundary_finalization_executed",
    "star_soul_transition_executed",
    "star_soul_transition_authorized",
    "v3_created",
    "v3_authorized",
    "civilization_core_completed",
    "enters_thirteenth_memory_layer",
    "thirteenth_memory_layer_transition_authorized",
}

FORBIDDEN_BOUNDARY_CLAIMS = (
    "attestation execution is performed",
    "attestation execution is authorized",
    "attestation is performed",
    "attestation is authorized",
    "attestation is executed",
    "attestation record is created",
    "attestation records are created",
    "attestation ledger entry is created",
    "attestation-ledger entries are created",
    "attestation ledger entries are created",
    "completion execution is performed",
    "completion execution is authorized",
    "completion is performed",
    "completion is authorized",
    "completion is executed",
    "completion record is created",
    "completion records are created",
    "completion ledger entry is created",
    "completion-ledger entries are created",
    "completion ledger entries are created",
    "finalization execution is performed",
    "finalization execution is authorized",
    "finalization is performed",
    "finalization is authorized",
    "finalization is executed",
    "finalization record is created",
    "finalization records are created",
    "finalization ledger entry is created",
    "finalization-ledger entries are created",
    "finalization ledger entries are created",
    "closure execution is performed",
    "closure execution is authorized",
    "closure is performed",
    "closure is authorized",
    "closure is executed",
    "closure record is created",
    "closure records are created",
    "closure ledger entry is created",
    "closure-ledger entries are created",
    "closure ledger entries are created",
    "audit execution is performed",
    "audit execution is authorized",
    "audit logging is performed",
    "audit log is created",
    "audit logs are created",
    "audit record is created",
    "audit records are created",
    "audit-ledger entries are created",
    "audit ledger entries are created",
    "violation response audit records are created",
    "violation response audit ledger entries are created",
    "violation response is performed",
    "violation response is authorized",
    "violation response is executed",
    "violation response records are created",
    "violation response ledger entries are created",
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
    "star-soul transition is executed",
    "star-soul transition is authorized",
    "v3 is created",
    "v3 is authorized",
    "the thirteenth memory layer has been entered",
)

PROPOSED_BOUNDARY_ALLOWED_TRUE_KEYS = {"proposal_only"}

REVIEW_COMPONENTS = {
    "source_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal_review",
    "response_audit_completion_attestation_completion_finalization_eligibility_boundary_review",
    "response_audit_completion_attestation_completion_finalization_input_boundary_review",
    "response_audit_completion_attestation_completion_finalization_output_boundary_review",
    "response_audit_completion_attestation_completion_finalization_non_execution_boundary_review",
    "response_audit_completion_attestation_completion_finalization_non_recording_boundary_review",
    "response_audit_completion_attestation_completion_finalization_non_ledger_boundary_review",
    "response_audit_completion_attestation_completion_finalization_non_authorization_boundary_review",
    "attestation_execution_non_authorization_boundary_review",
    "attestation_record_non_creation_boundary_review",
    "attestation_ledger_non_creation_boundary_review",
    "completion_execution_non_authorization_boundary_review",
    "completion_record_non_creation_boundary_review",
    "completion_ledger_non_creation_boundary_review",
    "finalization_execution_non_authorization_boundary_review",
    "finalization_record_non_creation_boundary_review",
    "finalization_ledger_non_creation_boundary_review",
    "closure_execution_non_authorization_boundary_review",
    "closure_record_non_creation_boundary_review",
    "closure_ledger_non_creation_boundary_review",
    "audit_execution_non_authorization_boundary_review",
    "audit_logging_non_execution_boundary_review",
    "audit_record_non_creation_boundary_review",
    "audit_ledger_non_creation_boundary_review",
    "violation_response_non_execution_boundary_review",
    "automated_correction_non_execution_boundary_review",
    "violation_enforcement_non_execution_boundary_review",
    "candidate_rule_enforcement_non_authorization_boundary_review",
    "human_operator_finalization_review_boundary_review",
    "evidence_lineage_finalization_boundary_review",
    "auditability_finalization_design_boundary_review",
    "false_positive_finalization_prevention_boundary_review",
    "rollback_finalization_boundary_review",
    "suspension_finalization_boundary_review",
    "memory_write_non_authorization_boundary_review",
    "memory_graph_mutation_non_authorization_boundary_review",
    "operation_ledger_non_creation_boundary_review",
    "openclaw_execution_non_authorization_boundary_review",
    "approval_non_authorization_boundary_review",
    "human_operator_final_authority_boundary_review",
    "fifteen_memory_layers_boundary_review",
    "twelfth_memory_layer_final_star_law_boundary_review",
    "future_star_soul_memory_continuity_boundary_proposal_review",
}


def build_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate(
    proposal_report: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a local-only, non-authorizing completion finalization review gate."""

    checks, blocking_reasons = _review_gate_checks(proposal_report)
    sensitive_field_count = _count_sensitive_keys(proposal_report)
    blocking_reasons = list(dict.fromkeys(blocking_reasons))
    ready = not blocking_reasons
    status = (
        "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate_ready"
        if ready
        else "blocked"
    )

    return {
        "version": GOVERNED_STAR_LAW_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_COMPLETION_ATTESTATION_COMPLETION_FINALIZATION_BOUNDARY_REVIEW_GATE_VERSION,
        "status": status,
        **REVIEW_GATE_FLAGS,
        "candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_reviewed_for_human_review_only": ready,
        "twelfth_memory_layer_final_star_law_boundary_review_gate_only": True,
        "twelfth_memory_layer_final_star_law_boundary_reviewed_for_human_review_only": ready,
        "star_soul_memory_continuity_boundary_proposal_ready_for_human_review_only": ready,
        "civilization_core_layer_mapping": dict(LAYER_MAPPING),
        "source_proposal_version": SOURCE_PROPOSAL_VERSION,
        "reviewed_chain_versions": list(REVIEWED_CHAIN_VERSIONS),
        "reviewed_star_hub_chain_versions": list(REVIEWED_STAR_HUB_CHAIN_VERSIONS),
        "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate_summary": _review_gate_summary(
            ready
        ),
        "review_gate_checks": checks,
        "source_proposal_summary": _source_proposal_summary(ready),
        "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate": _review_gate(
            ready
        ),
        "reviewed_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundaries": _reviewed_boundaries(
            ready
        ),
        "non_authorization_boundary": _non_authorization_boundary(ready),
        "preserved_governance_boundaries": _preserved_governance_boundaries(),
        "twelfth_memory_layer_hard_boundary": _twelfth_memory_layer_hard_boundary(
            ready
        ),
        "future_star_soul_memory_continuity_boundary_constraints": _future_star_soul_memory_continuity_boundary_constraints(),
        "next_stage_constraints": _next_stage_constraints(),
        "scope_boundaries": _scope_boundaries(),
        "risk_notes": _risk_notes(sensitive_field_count),
        "required_human_actions": _required_human_actions(ready, blocking_reasons),
        "blocking_reasons": blocking_reasons,
        "next_allowed_step": READY_NEXT_ALLOWED_STEP,
        "sensitive_field_count": sensitive_field_count,
        "sensitive_fields_omitted": sensitive_field_count > 0,
    }


def governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate_to_json(
    report: Mapping[str, Any],
) -> str:
    """Serialize the audit completion attestation completion finalization boundary review gate deterministically."""

    return json.dumps(dict(report), ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def _review_gate_checks(
    report: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[str]]:
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
        "source_proposal_version_must_be_2_59_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_proposal_status_ready",
        report.get("status")
        == "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal_ready",
        "source_proposal_status_must_be_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal_ready",
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
        "source_must_not_claim_attestation_completion_finalization_closure_audit_response_correction_violation_rule_autonomous_handoff_scheduling_approval_write_execution_dry_run_or_civilization_core_actions",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_no_unsafe_text_claims",
        _unsafe_text_claims(report) == [],
        "source_must_not_textually_claim_attestation_completion_finalization_closure_audit_response_correction_violation_rule_autonomous_write_approval_next_layer_or_civilization_core_actions",
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
        layer_checks = {
            "source_primary_layer": (
                mapping.get("primary_layer") == "星律记忆",
                "source_primary_layer_must_be_star_law_memory",
            ),
            "source_primary_layer_status": (
                mapping.get("primary_layer_status")
                == "Star-Law candidate rule violation response audit completion attestation completion finalization boundary proposal only, not finalization execution, not finalization record creation, not finalization-ledger creation, not completion execution, not completion record creation, not completion-ledger creation, not closure execution, not closure record creation, not closure-ledger creation, not attestation execution, not attestation record creation, not attestation-ledger creation, not audit execution, not audit logging, not audit record creation, not audit-ledger creation, not violation response execution, not automated correction, not violation enforcement, and not autonomous execution",
                "source_primary_layer_status_must_be_audit_completion_attestation_completion_finalization_boundary_proposal_only",
            ),
            "source_source_layer": (
                mapping.get("source_layer") == "星律记忆",
                "source_source_layer_must_be_star_law_memory",
            ),
            "source_source_layer_status": (
                mapping.get("source_layer_status")
                == "Star-Law candidate rule violation response audit completion attestation completion closure boundary review gate complete for human review only",
                "source_source_layer_status_must_be_audit_completion_attestation_completion_closure_boundary_review_gate_complete_for_human_review_only",
            ),
            "source_supporting_layers": (
                isinstance(supporting_layers, list)
                and all(
                    layer in supporting_layers
                    for layer in ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"]
                ),
                "source_supporting_layers_must_include_required_layers",
            ),
            "source_direction": (
                mapping.get("direction")
                == "Star-Law candidate rule violation response audit completion attestation completion closure boundary review gate -> Star-Law candidate rule violation response audit completion attestation completion finalization boundary proposal",
                "source_direction_must_match_audit_completion_attestation_completion_closure_review_gate_to_audit_completion_attestation_completion_finalization_boundary_proposal",
            ),
        }
        for name, (passed, reason) in layer_checks.items():
            _add_check(checks, blocking_reasons, name, passed, reason)

    _add_check(
        checks,
        blocking_reasons,
        "source_proposed_chain_versions",
        report.get("proposed_chain_versions") == SOURCE_PROPOSED_CHAIN_VERSIONS,
        "source_proposed_chain_versions_must_exactly_match_v2_9_0_through_v2_58_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_proposed_star_hub_chain_versions",
        report.get("proposed_star_hub_chain_versions")
        == SOURCE_PROPOSED_STAR_HUB_CHAIN_VERSIONS,
        "source_proposed_star_hub_chain_versions_must_exactly_match_v2_19_0_through_v2_58_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_next_allowed_step",
        report.get("next_allowed_step")
        == "v2.60.0 Star-Law candidate rule violation response audit completion attestation completion finalization boundary review gate",
        "source_next_allowed_step_must_be_v2_60_0_audit_completion_attestation_completion_finalization_boundary_review_gate",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_blocking_reasons_empty",
        report.get("blocking_reasons") == [],
        "source_blocking_reasons_must_be_empty",
    )

    proposal = report.get(
        "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal"
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_audit_completion_attestation_completion_finalization_boundary_proposal_shape",
        isinstance(proposal, Mapping),
        "source_audit_completion_attestation_completion_finalization_boundary_proposal_must_be_mapping",
    )
    if isinstance(proposal, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_audit_completion_attestation_completion_finalization_boundary_proposal_status",
            proposal.get("proposal_status")
            == "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposed_for_human_review_only",
            "source_audit_completion_attestation_completion_finalization_boundary_proposal_status_must_be_human_review_only",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_audit_completion_attestation_completion_finalization_boundary_proposal_type",
            proposal.get("boundary_type")
            == "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal",
            "source_audit_completion_attestation_completion_finalization_boundary_proposal_type_must_match",
        )
        for key, expected in SOURCE_PROPOSAL_OBJECT_REQUIRED_FLAGS.items():
            _add_check(
                checks,
                blocking_reasons,
                f"source_audit_completion_attestation_completion_finalization_boundary_proposal_{key}",
                proposal.get(key) is expected,
                f"source_audit_completion_attestation_completion_finalization_boundary_proposal_{key}_must_be_{str(expected).lower()}",
            )
        _add_check(
            checks,
            blocking_reasons,
            "source_audit_completion_attestation_completion_finalization_boundary_proposal_chain_versions",
            proposal.get("proposed_chain_versions")
            == SOURCE_PROPOSED_CHAIN_VERSIONS,
            "source_audit_completion_attestation_completion_finalization_boundary_proposal_chain_versions_must_match",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_audit_completion_attestation_completion_finalization_boundary_proposal_star_hub_chain_versions",
            proposal.get("proposed_star_hub_chain_versions")
            == SOURCE_PROPOSED_STAR_HUB_CHAIN_VERSIONS,
            "source_audit_completion_attestation_completion_finalization_boundary_proposal_star_hub_chain_versions_must_match",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_audit_completion_attestation_completion_finalization_boundary_proposal_next_allowed_step",
            proposal.get("next_allowed_step")
            == "v2.60.0 Star-Law candidate rule violation response audit completion attestation completion finalization boundary review gate",
            "source_audit_completion_attestation_completion_finalization_boundary_proposal_next_allowed_step_must_match",
        )

    boundaries = report.get(
        "proposed_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundaries"
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_proposed_audit_completion_attestation_completion_finalization_boundaries_shape",
        isinstance(boundaries, Mapping),
        "source_proposed_audit_completion_attestation_completion_finalization_boundaries_must_be_mapping",
    )
    if isinstance(boundaries, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_proposed_audit_completion_attestation_completion_finalization_boundaries_required_keys",
            set(boundaries)
            == SOURCE_PROPOSED_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_COMPLETION_ATTESTATION_COMPLETION_FINALIZATION_BOUNDARY_KEYS,
            "source_proposed_audit_completion_attestation_completion_finalization_boundaries_must_exactly_match_required_boundaries",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_proposed_audit_completion_attestation_completion_finalization_boundaries_proposal_only",
            _proposed_boundaries_remain_proposal_only(boundaries),
            "source_proposed_audit_completion_attestation_completion_finalization_boundaries_must_remain_proposal_only_and_non_authorizing",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_proposed_audit_completion_attestation_completion_finalization_boundaries_no_unsafe_claims",
            _unsafe_boundary_claims(
                boundaries, PROPOSED_BOUNDARY_ALLOWED_TRUE_KEYS
            )
            == [],
            "source_proposed_audit_completion_attestation_completion_finalization_boundaries_must_not_claim_execution_authorization_recording_enforcement_or_write_actions",
        )

    return checks, blocking_reasons


def _review_gate_summary(ready: bool) -> dict[str, Any]:
    return {
        "review_status": (
            "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_reviewed_for_human_review_only"
            if ready
            else "blocked"
        ),
        "source_proposal_version": SOURCE_PROPOSAL_VERSION,
        "source_proposal_valid": ready,
        "candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_reviewed_for_human_review_only": ready,
        "twelfth_memory_layer_final_star_law_boundary_reviewed_for_human_review_only": ready,
        "star_soul_memory_continuity_boundary_proposal_ready_for_human_review_only": ready,
        "review_only": True,
        "non_authorizing": True,
        "non_executing": True,
        "non_recording": True,
        "non_ledger_creating": True,
        "non_memory_writing": True,
        "civilization_core_complete_claimed": False,
    }


def _source_proposal_summary(ready: bool) -> dict[str, Any]:
    return {
        "source_proposal_version": SOURCE_PROPOSAL_VERSION,
        "source_proposal_status": (
            "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal_ready"
            if ready
            else "blocked"
        ),
        "source_chain_versions": list(SOURCE_PROPOSED_CHAIN_VERSIONS),
        "source_star_hub_chain_versions": list(
            SOURCE_PROPOSED_STAR_HUB_CHAIN_VERSIONS
        ),
        "source_audit_completion_attestation_completion_finalization_boundary_proposal_valid": ready,
        "source_proposal_authorized_attestation_execution": False,
        "source_proposal_created_attestation_record": False,
        "source_proposal_created_attestation_ledger_entry": False,
        "source_proposal_authorized_completion_execution": False,
        "source_proposal_created_completion_record": False,
        "source_proposal_created_completion_ledger_entry": False,
        "source_proposal_authorized_finalization_execution": False,
        "source_proposal_created_finalization_record": False,
        "source_proposal_created_finalization_ledger_entry": False,
        "source_proposal_authorized_closure_execution": False,
        "source_proposal_created_closure_record": False,
        "source_proposal_created_closure_ledger_entry": False,
        "source_proposal_authorized_audit_execution": False,
        "source_proposal_created_audit_artifact": False,
        "source_proposal_authorized_violation_response": False,
        "source_proposal_authorized_automated_correction": False,
        "source_proposal_authorized_violation_enforcement": False,
        "source_proposal_authorized_candidate_rule_enforcement": False,
        "source_proposal_authorized_autonomous_execution": False,
        "source_proposal_authorized_memory_write": False,
        "source_proposal_authorized_openclaw_execution": False,
        "source_proposal_claimed_civilization_core_completion": False,
        "raw_source_proposal_copied": False,
    }


def _review_gate(ready: bool) -> dict[str, Any]:
    return {
        "review_status": (
            "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_reviewed_for_human_review_only"
            if ready
            else "blocked_no_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_readiness_claim"
        ),
        "boundary_type": "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate",
        "source_proposal_version": SOURCE_PROPOSAL_VERSION,
        "candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_reviewed": ready,
        "candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_structurally_review_ready": ready,
        "star_soul_memory_continuity_boundary_proposal_ready_for_human_review_only": ready,
        "source_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal_valid": ready,
        "twelfth_memory_layer_final_star_law_boundary_reviewed_for_human_review_only": ready,
        **REVIEW_OBJECT_FALSE_FLAGS,
        "reviewed_chain_versions": list(REVIEWED_CHAIN_VERSIONS),
        "reviewed_star_hub_chain_versions": list(REVIEWED_STAR_HUB_CHAIN_VERSIONS),
        "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_components": _review_components(
            ready
        ),
        "next_allowed_step": READY_NEXT_ALLOWED_STEP,
        "non_authorization_notice": (
            "The v2.59.0 Star-Law candidate rule violation response audit completion attestation completion finalization boundary proposal has been structurally reviewed for human review only. A later separate v3.0.0 Star-Soul Memory continuity boundary proposal may be considered, but this review grants no transition, execution, authorization, recording, ledger, write, approval, handoff, scheduling, or autonomous authority."
            if ready
            else "The Star-Law candidate rule violation response audit completion attestation completion finalization boundary review gate is blocked and makes no readiness, execution, authorization, recording, ledger, enforcement, write, approval, handoff, scheduling, next-layer, or Civilization Core completion claim."
        ),
    }


def _review_components(ready: bool) -> dict[str, str]:
    status = "reviewed_for_human_review_only" if ready else "blocked"
    return {component: status for component in sorted(REVIEW_COMPONENTS)}


def _reviewed_boundaries(ready: bool) -> dict[str, dict[str, Any]]:
    status = "reviewed_for_human_review_only" if ready else "blocked"
    return {
        key: {
            "review_only": True,
            "boundary_status": status,
            "summary": "The source boundary was structurally reviewed from sanitized v2.59.0 proposal metadata only; no raw proposal data or authority was copied.",
            "raw_source_boundary_copied": False,
            **REVIEW_OBJECT_FALSE_FLAGS,
        }
        for key in sorted(
            SOURCE_PROPOSED_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_COMPLETION_ATTESTATION_COMPLETION_FINALIZATION_BOUNDARY_KEYS
        )
    }


def _non_authorization_boundary(ready: bool) -> dict[str, Any]:
    return {
        "review_gate_ready_is_attestation_execution": False,
        "review_gate_ready_is_attestation_authorization": False,
        "review_gate_ready_is_attestation_record_creation": False,
        "review_gate_ready_is_attestation_ledger_creation": False,
        "review_gate_ready_is_completion_execution": False,
        "review_gate_ready_is_completion_authorization": False,
        "review_gate_ready_is_completion_record_creation": False,
        "review_gate_ready_is_completion_ledger_creation": False,
        "review_gate_ready_is_finalization_execution": False,
        "review_gate_ready_is_finalization_authorization": False,
        "review_gate_ready_is_finalization_record_creation": False,
        "review_gate_ready_is_finalization_ledger_creation": False,
        "review_gate_ready_is_closure_execution": False,
        "review_gate_ready_is_closure_authorization": False,
        "review_gate_ready_is_closure_record_creation": False,
        "review_gate_ready_is_closure_ledger_creation": False,
        "review_gate_ready_is_audit_execution": False,
        "review_gate_ready_is_audit_authorization": False,
        "review_gate_ready_is_audit_logging": False,
        "review_gate_ready_is_audit_artifact_creation": False,
        "review_gate_ready_is_violation_response": False,
        "review_gate_ready_is_automated_correction": False,
        "review_gate_ready_is_violation_enforcement": False,
        "review_gate_ready_is_candidate_rule_enforcement": False,
        "review_gate_ready_is_rule_creation_activation_or_enforcement": False,
        "review_gate_ready_is_autonomous_governance_or_execution": False,
        "review_gate_ready_is_memory_write_or_graph_mutation": False,
        "review_gate_ready_is_operation_ledger_creation": False,
        "review_gate_ready_is_openclaw_execution": False,
        "review_gate_ready_is_approval_or_human_decision": False,
        "review_gate_ready_is_handoff_scheduling_or_dry_run": False,
        "review_gate_ready_is_civilization_core_completion": False,
        "review_gate_ready_is_star_soul_transition": False,
        "review_gate_ready_is_v3_creation_or_authorization": False,
        "only_permits_later_star_soul_memory_continuity_boundary_proposal": ready,
        "human_operator_remains_final_authority": True,
    }


def _preserved_governance_boundaries() -> list[str]:
    return [
        "This review gate does not perform or authorize attestation execution.",
        "This review gate does not create attestation records or attestation-ledger entries.",
        "This review gate does not perform or authorize completion execution.",
        "This review gate does not create completion records or completion-ledger entries.",
        "This review gate does not perform or authorize finalization execution.",
        "This review gate does not create finalization records or finalization-ledger entries.",
        "This review gate does not perform or authorize closure execution.",
        "This review gate does not create closure records or closure-ledger entries.",
        "This review gate does not perform or authorize audit execution or audit logging.",
        "This review gate does not create audit logs, audit records, or audit-ledger entries.",
        "This review gate does not perform or authorize violation response or automated correction.",
        "This review gate does not observe, detect, record, or enforce violations.",
        "This review gate does not enforce candidate rules or create, activate, or enforce Star-Law rules.",
        "This review gate does not authorize autonomous execution, handoff, scheduling, approval, or dry-run execution.",
        "This review gate does not write durable memory, mutate Memory Graph, create operation-ledger entries, or call OpenClaw or GitHub APIs.",
        "This review gate does not claim Civilization Core completion or entry into mature 星律, 星魂, 星宙, or 星源 stages.",
        "This review gate does not execute or authorize Star-Soul transition and does not create or authorize v3.0.0.",
        "This review gate does not authorize transition into the 13th memory layer.",
        "Human Operator remains final authority.",
    ]


def _twelfth_memory_layer_hard_boundary(ready: bool) -> dict[str, Any]:
    return {
        "memory_layer": "星律记忆",
        "memory_layer_number": 12,
        "final_v2_x_star_law_boundary": True,
        "review_gate_only": True,
        "reviewed_for_human_review_only": ready,
        "enters_thirteenth_memory_layer": False,
        "thirteenth_memory_layer_transition_authorized": False,
        "star_soul_transition_executed": False,
        "star_soul_transition_authorized": False,
        "v3_created": False,
        "v3_authorized": False,
        "boundary_notice": "This is the final v2.x Star-Law review gate. Any later v3.0.0 Star-Soul Memory continuity boundary proposal must be separate and human-reviewed.",
    }


def _future_star_soul_memory_continuity_boundary_constraints() -> list[str]:
    return [
        "A later separate v3.0.0 Star-Soul Memory continuity boundary proposal may consume this sanitized review report through a separate governed process.",
        "A later Star-Soul Memory continuity boundary proposal remains proposal-only and cannot execute finalization, completion, closure, attestation, audit, response, correction, enforcement, writes, approvals, handoffs, scheduling, transitions, or autonomous actions.",
        "This review gate does not create, authorize, or enter v3.0.0 or the 13th memory layer.",
        "No future stage may infer real Human Operator approval from this review gate.",
        "Human Operator remains final authority for all future Star-Law and Star-Soul boundary decisions.",
    ]


def _next_stage_constraints() -> list[str]:
    return [
        f"The only next allowed step is {READY_NEXT_ALLOWED_STEP}.",
        "v2.60.0 is the final v2.x Star-Law candidate rule violation response audit completion attestation completion finalization boundary review gate only.",
        "All closure, attestation, completion, finalization, audit, response, correction, violation, enforcement, rule, write, approval, handoff, scheduling, and dry-run execution boundaries remain inactive.",
        "No Star-Soul transition, v3 creation, 13th-memory-layer entry, mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, or 星源 self-evolution occurs.",
    ]


def _scope_boundaries() -> list[str]:
    return [
        "Civilization Core is the total system.",
        "Fifteen Memory Layers are the highest memory coordinate system.",
        "Subspace Memory System is the engineering carrier.",
        "Hermes, Codex CLI, OpenClaw, Terminal, and GitHub are components, not the core.",
        "This v2.60.0 step is limited to the final v2.x 星律记忆 audit completion attestation completion finalization boundary review gate.",
    ]


def _risk_notes(sensitive_field_count: int) -> list[str]:
    notes = [
        "Review readiness must not be interpreted as closure, attestation, completion, finalization, audit, response, correction, enforcement, write, approval, handoff, scheduling, or autonomous authority.",
        "The report is deterministic, local-only, read-only, and contains sanitized structural summaries rather than raw source proposal data.",
        "Civilization Core completion and later memory-layer entry are not claimed.",
    ]
    if sensitive_field_count:
        notes.append("Sensitive fields were omitted from review gate output.")
    return notes


def _required_human_actions(
    ready: bool, blocking_reasons: list[str]
) -> list[str]:
    if ready:
        return [
            "human_operator_must_review_v2_60_0_final_star_law_boundary_review_gate_before_any_separate_v3_0_0_star_soul_memory_continuity_boundary_proposal",
            "human_operator_must_confirm_review_readiness_grants_no_execution_authorization_recording_ledger_enforcement_write_approval_handoff_scheduling_or_autonomous_authority",
            "human_operator_must_use_a_separate_governed_process_for_any_v3_0_0_star_soul_memory_continuity_boundary_proposal",
        ]
    actions = [
        "repair_source_v2_59_0_audit_completion_attestation_completion_finalization_boundary_proposal_before_review_gate_can_continue",
        "confirm_all_unsafe_attestation_completion_finalization_closure_audit_response_correction_violation_enforcement_rule_execution_authorization_recording_ledger_write_approval_handoff_and_scheduling_flags_remain_false",
        "rerun_local_v2_60_0_audit_completion_attestation_completion_finalization_boundary_review_gate_after_blockers_are_resolved",
    ]
    if blocking_reasons:
        actions.append(
            "resolve_blocking_reasons_before_audit_completion_attestation_completion_finalization_boundary_review_gate_can_be_ready"
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


def _unsafe_boundary_claims(
    value: Any, allowed_true_keys: set[str]
) -> list[str]:
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
    "GOVERNED_STAR_LAW_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_COMPLETION_ATTESTATION_COMPLETION_FINALIZATION_BOUNDARY_REVIEW_GATE_VERSION",
    "READY_NEXT_ALLOWED_STEP",
    "REVIEWED_CHAIN_VERSIONS",
    "REVIEWED_STAR_HUB_CHAIN_VERSIONS",
    "SOURCE_PROPOSED_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_COMPLETION_ATTESTATION_COMPLETION_FINALIZATION_BOUNDARY_KEYS",
    "REVIEW_GATE_FALSE_FLAGS",
    "REVIEW_OBJECT_FALSE_FLAGS",
    "REVIEW_COMPONENTS",
    "SENSITIVE_KEYS",
    "build_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate",
    "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate_to_json",
]
