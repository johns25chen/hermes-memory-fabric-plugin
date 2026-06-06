"""Governed Star-Law audit completion attestation boundary proposal."""

from __future__ import annotations

import json
from typing import Any, Mapping

from .governed_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate import (
    REVIEWED_CHAIN_VERSIONS as SOURCE_REVIEWED_CHAIN_VERSIONS,
    REVIEWED_STAR_HUB_CHAIN_VERSIONS as SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS,
    REVIEW_GATE_FALSE_FLAGS as SOURCE_REVIEW_GATE_FALSE_FLAGS,
    REVIEW_OBJECT_FALSE_FLAGS as SOURCE_REVIEW_OBJECT_FALSE_FLAGS,
    SENSITIVE_KEYS,
    SOURCE_PROPOSED_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_COMPLETION_BOUNDARY_KEYS,
)


GOVERNED_STAR_LAW_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_COMPLETION_ATTESTATION_BOUNDARY_PROPOSAL_VERSION = (
    "2.49.0"
)
SOURCE_REVIEW_GATE_VERSION = "2.48.0"

PROPOSED_CHAIN_VERSIONS = [*SOURCE_REVIEWED_CHAIN_VERSIONS, "v2.48.0"]
PROPOSED_STAR_HUB_CHAIN_VERSIONS = [
    *SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS,
    "v2.48.0",
]

LAYER_MAPPING = {
    "primary_layer": "星律记忆",
    "primary_layer_status": "Star-Law candidate rule violation response audit completion attestation boundary proposal only, not attestation execution, not attestation record creation, not attestation-ledger creation, not completion execution, not finalization execution, not closure execution, not audit execution, not audit logging, not audit record creation, not audit-ledger creation, not violation response execution, not automated correction, not violation enforcement, and not autonomous execution",
    "source_layer": "星律记忆",
    "source_layer_status": "Star-Law candidate rule violation response audit completion boundary review gate complete for human review only",
    "supporting_layers": ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"],
    "direction": "Star-Law candidate rule violation response audit completion boundary review gate -> Star-Law candidate rule violation response audit completion attestation boundary proposal",
}

READY_NEXT_ALLOWED_STEP = (
    "v2.50.0 Star-Law candidate rule violation response audit completion attestation boundary review gate"
)

ATTESTATION_FALSE_FLAGS = {
    "candidate_rule_violation_response_audit_completion_attestation_performed": False,
    "candidate_rule_violation_response_audit_completion_attestation_authorized": False,
    "candidate_rule_violation_response_audit_completion_attestation_executed": False,
    "candidate_rule_violation_response_audit_completion_attestation_execution_authorized": False,
    "candidate_rule_violation_response_audit_completion_attestation_record_created": False,
    "candidate_rule_violation_response_audit_completion_attestation_ledger_entry_created": False,
    "attestation_execution_performed": False,
    "attestation_execution_authorized": False,
    "attestation_record_created": False,
    "attestation_ledger_entry_created": False,
}

PROPOSAL_FALSE_FLAGS = {
    **SOURCE_REVIEW_GATE_FALSE_FLAGS,
    **ATTESTATION_FALSE_FLAGS,
}

PROPOSAL_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "proposal_only": True,
    "candidate_rule_violation_response_audit_completion_attestation_boundary_proposal_only": True,
    "star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal_only": True,
    **PROPOSAL_FALSE_FLAGS,
}

SOURCE_REQUIRED_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "review_gate_only": True,
    "candidate_rule_violation_response_audit_completion_boundary_review_gate_only": True,
    "star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate_only": True,
    "candidate_rule_violation_response_audit_completion_boundary_reviewed_for_human_review_only": True,
    "candidate_rule_violation_response_audit_completion_attestation_boundary_proposal_ready_for_human_review_only": True,
    **SOURCE_REVIEW_GATE_FALSE_FLAGS,
}

SOURCE_REVIEW_GATE_REQUIRED_FLAGS = {
    "candidate_rule_violation_response_audit_completion_boundary_reviewed": True,
    "candidate_rule_violation_response_audit_completion_boundary_structurally_review_ready": True,
    "candidate_rule_violation_response_audit_completion_attestation_boundary_proposal_ready_for_human_review_only": True,
    "source_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal_valid": True,
    **SOURCE_REVIEW_OBJECT_FALSE_FLAGS,
}

PROPOSAL_OBJECT_FALSE_FLAGS = {
    **PROPOSAL_FALSE_FLAGS,
    "durable_memory_write_authorized": False,
    "memory_graph_mutation_authorized": False,
    "operation_ledger_creation_authorized": False,
    "approval_authorized": False,
    "real_human_decision_recorded": False,
}

UNSAFE_TRUE_FIELDS = {
    *PROPOSAL_FALSE_FLAGS,
    *PROPOSAL_OBJECT_FALSE_FLAGS,
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
    "candidate_rule_violation_response_audit_boundary_finalization_executed",
    "candidate_rule_violation_response_audit_boundary_closure_executed",
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
    "self-enforcing memory law has started",
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

PROPOSED_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_COMPLETION_ATTESTATION_BOUNDARY_KEYS = {
    "response_audit_completion_attestation_eligibility_boundary",
    "response_audit_completion_attestation_input_boundary",
    "response_audit_completion_attestation_output_boundary",
    "response_audit_completion_attestation_non_execution_boundary",
    "response_audit_completion_attestation_non_recording_boundary",
    "response_audit_completion_attestation_non_ledger_boundary",
    "response_audit_completion_attestation_non_authorization_boundary",
    "attestation_execution_non_authorization_boundary",
    "attestation_record_non_creation_boundary",
    "attestation_ledger_non_creation_boundary",
    "completion_execution_non_authorization_boundary",
    "completion_record_non_creation_boundary",
    "completion_ledger_non_creation_boundary",
    "finalization_execution_non_authorization_boundary",
    "finalization_record_non_creation_boundary",
    "finalization_ledger_non_creation_boundary",
    "closure_execution_non_authorization_boundary",
    "closure_record_non_creation_boundary",
    "closure_ledger_non_creation_boundary",
    "audit_execution_non_authorization_boundary",
    "audit_logging_non_execution_boundary",
    "audit_record_non_creation_boundary",
    "audit_ledger_non_creation_boundary",
    "violation_response_non_execution_boundary",
    "automated_correction_non_execution_boundary",
    "violation_enforcement_non_execution_boundary",
    "candidate_rule_enforcement_non_authorization_boundary",
    "human_operator_attestation_review_boundary",
    "evidence_lineage_attestation_boundary",
    "auditability_attestation_design_boundary",
    "false_positive_attestation_prevention_boundary",
    "rollback_attestation_boundary",
    "suspension_attestation_boundary",
    "memory_write_non_authorization_boundary",
    "memory_graph_mutation_non_authorization_boundary",
    "operation_ledger_non_creation_boundary",
    "openclaw_execution_non_authorization_boundary",
    "approval_non_authorization_boundary",
    "human_operator_final_authority_boundary",
    "fifteen_memory_layers_boundary",
}

PROPOSAL_COMPONENTS = {
    "source_candidate_rule_violation_response_audit_completion_boundary_review_gate",
    *PROPOSED_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_COMPLETION_ATTESTATION_BOUNDARY_KEYS,
}


def build_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal(
    review_gate_report: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a local-only, non-authorizing attestation boundary proposal."""

    checks, blocking_reasons = _proposal_checks(review_gate_report)
    sensitive_field_count = _count_sensitive_keys(review_gate_report)
    blocking_reasons = list(dict.fromkeys(blocking_reasons))
    ready = not blocking_reasons
    status = (
        "star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal_ready"
        if ready
        else "blocked"
    )

    return {
        "version": GOVERNED_STAR_LAW_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_COMPLETION_ATTESTATION_BOUNDARY_PROPOSAL_VERSION,
        "status": status,
        **PROPOSAL_FLAGS,
        "candidate_rule_violation_response_audit_completion_attestation_boundary_proposed_for_human_review_only": ready,
        "candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate_ready_for_human_review_only": ready,
        "civilization_core_layer_mapping": dict(LAYER_MAPPING),
        "source_review_gate_version": SOURCE_REVIEW_GATE_VERSION,
        "proposed_chain_versions": list(PROPOSED_CHAIN_VERSIONS),
        "proposed_star_hub_chain_versions": list(PROPOSED_STAR_HUB_CHAIN_VERSIONS),
        "star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal_summary": _proposal_summary(
            ready
        ),
        "proposal_checks": checks,
        "source_review_gate_summary": _source_review_gate_summary(ready),
        "star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal": _attestation_boundary_proposal(
            ready
        ),
        "proposed_candidate_rule_violation_response_audit_completion_attestation_boundaries": _proposed_attestation_boundaries(
            ready
        ),
        "non_authorization_boundary": _non_authorization_boundary(ready),
        "preserved_governance_boundaries": _preserved_governance_boundaries(),
        "future_candidate_rule_violation_response_audit_completion_attestation_review_gate_constraints": _future_review_gate_constraints(),
        "next_stage_constraints": _next_stage_constraints(),
        "scope_boundaries": _scope_boundaries(),
        "risk_notes": _risk_notes(sensitive_field_count),
        "required_human_actions": _required_human_actions(
            ready, blocking_reasons
        ),
        "blocking_reasons": blocking_reasons,
        "next_allowed_step": READY_NEXT_ALLOWED_STEP,
        "sensitive_field_count": sensitive_field_count,
        "sensitive_fields_omitted": sensitive_field_count > 0,
    }


def governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal_to_json(
    report: Mapping[str, Any],
) -> str:
    """Serialize an attestation boundary proposal deterministically."""

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
        "source_review_gate_version_must_be_2_48_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_review_gate_status_ready",
        report.get("status")
        == "star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate_ready",
        "source_review_gate_status_must_be_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate_ready",
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
                == "Star-Law candidate rule violation response audit completion boundary review gate only, not completion execution, not completion record creation, not completion-ledger creation, not finalization execution, not closure execution, not audit execution, not audit logging, not audit record creation, not audit-ledger creation, not violation response execution, not automated correction, not violation enforcement, and not autonomous execution",
                "source_primary_layer_status_must_be_audit_completion_boundary_review_gate_only",
            ),
            "source_source_layer": (
                mapping.get("source_layer") == "星律记忆",
                "source_source_layer_must_be_star_law_memory",
            ),
            "source_source_layer_status": (
                mapping.get("source_layer_status")
                == "Star-Law candidate rule violation response audit completion boundary proposal complete for human review only",
                "source_source_layer_status_must_be_audit_completion_boundary_proposal_complete_for_human_review_only",
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
                == "Star-Law candidate rule violation response audit completion boundary proposal -> Star-Law candidate rule violation response audit completion boundary review gate",
                "source_direction_must_match_audit_completion_proposal_to_review_gate",
            ),
        }
        for name, (passed, reason) in layer_checks.items():
            _add_check(checks, blocking_reasons, name, passed, reason)

    _add_check(
        checks,
        blocking_reasons,
        "source_reviewed_chain_versions",
        report.get("reviewed_chain_versions") == SOURCE_REVIEWED_CHAIN_VERSIONS,
        "source_reviewed_chain_versions_must_exactly_match_v2_9_0_through_v2_47_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_reviewed_star_hub_chain_versions",
        report.get("reviewed_star_hub_chain_versions")
        == SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS,
        "source_reviewed_star_hub_chain_versions_must_exactly_match_v2_19_0_through_v2_47_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_next_allowed_step",
        report.get("next_allowed_step")
        == "v2.49.0 Star-Law candidate rule violation response audit completion attestation boundary proposal",
        "source_next_allowed_step_must_be_v2_49_0_audit_completion_attestation_boundary_proposal",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_blocking_reasons_empty",
        report.get("blocking_reasons") == [],
        "source_blocking_reasons_must_be_empty",
    )

    review_gate = report.get(
        "star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate"
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_audit_completion_boundary_review_gate_shape",
        isinstance(review_gate, Mapping),
        "source_audit_completion_boundary_review_gate_must_be_mapping",
    )
    if isinstance(review_gate, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_audit_completion_boundary_review_gate_status",
            review_gate.get("review_status")
            == "star_law_candidate_rule_violation_response_audit_completion_boundary_reviewed_for_human_review_only",
            "source_audit_completion_boundary_review_gate_status_must_be_human_review_only",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_audit_completion_boundary_review_gate_type",
            review_gate.get("boundary_type")
            == "star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate",
            "source_audit_completion_boundary_review_gate_type_must_match",
        )
        for key, expected in SOURCE_REVIEW_GATE_REQUIRED_FLAGS.items():
            _add_check(
                checks,
                blocking_reasons,
                f"source_audit_completion_boundary_review_gate_{key}",
                review_gate.get(key) is expected,
                f"source_audit_completion_boundary_review_gate_{key}_must_be_{str(expected).lower()}",
            )
        _add_check(
            checks,
            blocking_reasons,
            "source_audit_completion_boundary_review_gate_chain_versions",
            review_gate.get("reviewed_chain_versions")
            == SOURCE_REVIEWED_CHAIN_VERSIONS,
            "source_audit_completion_boundary_review_gate_chain_versions_must_match",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_audit_completion_boundary_review_gate_star_hub_chain_versions",
            review_gate.get("reviewed_star_hub_chain_versions")
            == SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS,
            "source_audit_completion_boundary_review_gate_star_hub_chain_versions_must_match",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_audit_completion_boundary_review_gate_next_allowed_step",
            review_gate.get("next_allowed_step")
            == "v2.49.0 Star-Law candidate rule violation response audit completion attestation boundary proposal",
            "source_audit_completion_boundary_review_gate_next_allowed_step_must_match",
        )

    boundaries = report.get(
        "reviewed_candidate_rule_violation_response_audit_completion_boundaries"
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_reviewed_audit_completion_boundaries_shape",
        isinstance(boundaries, Mapping),
        "source_reviewed_audit_completion_boundaries_must_be_mapping",
    )
    if isinstance(boundaries, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_reviewed_audit_completion_boundaries_required_keys",
            set(boundaries)
            == SOURCE_PROPOSED_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_COMPLETION_BOUNDARY_KEYS,
            "source_reviewed_audit_completion_boundaries_must_exactly_match_required_boundaries",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_reviewed_audit_completion_boundaries_review_only",
            _reviewed_boundaries_remain_review_only(boundaries),
            "source_reviewed_audit_completion_boundaries_must_remain_review_only_and_non_authorizing",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_reviewed_audit_completion_boundaries_no_unsafe_claims",
            _unsafe_boundary_claims(boundaries, {"review_only"}) == [],
            "source_reviewed_audit_completion_boundaries_must_not_claim_attestation_completion_finalization_closure_audit_response_correction_violation_rule_autonomous_or_memory_write_actions",
        )

    return checks, blocking_reasons


def _proposal_summary(ready: bool) -> dict[str, Any]:
    return {
        "proposal_status": (
            "star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposed_for_human_review_only"
            if ready
            else "blocked"
        ),
        "source_review_gate_version": SOURCE_REVIEW_GATE_VERSION,
        "source_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate_valid": ready,
        "candidate_rule_violation_response_audit_completion_attestation_boundary_proposed_for_human_review_only": ready,
        "candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate_ready_for_human_review_only": ready,
        "proposal_only": True,
        "non_attestation_executing": True,
        "non_attestation_authorizing": True,
        "non_attestation_record_creating": True,
        "non_attestation_ledger_creating": True,
        "non_completion_executing": True,
        "non_finalization_executing": True,
        "non_closure_executing": True,
        "non_audit_executing": True,
        "non_audit_logging": True,
        "non_violation_response_performing": True,
        "non_automated_correction": True,
        "non_violation_enforcing": True,
        "non_candidate_rule_enforcing": True,
        "non_rule_creating": True,
        "non_autonomous_execution": True,
        "civilization_core_complete_claimed": False,
    }


def _source_review_gate_summary(ready: bool) -> dict[str, Any]:
    return {
        "source_review_gate_version": SOURCE_REVIEW_GATE_VERSION,
        "source_review_gate_status": (
            "star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate_ready"
            if ready
            else "blocked"
        ),
        "source_chain_versions": list(SOURCE_REVIEWED_CHAIN_VERSIONS),
        "source_star_hub_chain_versions": list(
            SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS
        ),
        "source_audit_completion_boundary_review_gate_valid": ready,
        "source_review_gate_authorized_attestation_execution": False,
        "source_review_gate_created_attestation_record": False,
        "source_review_gate_created_attestation_ledger_entry": False,
        "source_review_gate_authorized_completion_execution": False,
        "source_review_gate_authorized_finalization_execution": False,
        "source_review_gate_authorized_closure_execution": False,
        "source_review_gate_authorized_audit_execution": False,
        "source_review_gate_authorized_violation_response": False,
        "source_review_gate_authorized_automated_correction": False,
        "source_review_gate_authorized_violation_enforcement": False,
        "source_review_gate_authorized_candidate_rule_enforcement": False,
        "source_review_gate_authorized_autonomous_execution": False,
        "source_review_gate_authorized_memory_write": False,
        "source_review_gate_authorized_openclaw_execution": False,
        "source_review_gate_claimed_civilization_core_completion": False,
        "raw_source_review_gate_copied": False,
    }


def _attestation_boundary_proposal(ready: bool) -> dict[str, Any]:
    return {
        "proposal_status": (
            "star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposed_for_human_review_only"
            if ready
            else "blocked_no_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_readiness_claim"
        ),
        "boundary_type": "star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal",
        "source_review_gate_version": SOURCE_REVIEW_GATE_VERSION,
        "candidate_rule_violation_response_audit_completion_attestation_boundary_proposed": ready,
        "candidate_rule_violation_response_audit_completion_attestation_boundary_review_gate_ready_for_human_review_only": ready,
        "source_star_law_candidate_rule_violation_response_audit_completion_boundary_review_gate_valid": ready,
        **PROPOSAL_OBJECT_FALSE_FLAGS,
        "proposed_chain_versions": list(PROPOSED_CHAIN_VERSIONS),
        "proposed_star_hub_chain_versions": list(
            PROPOSED_STAR_HUB_CHAIN_VERSIONS
        ),
        "star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_components": _proposal_components(
            ready
        ),
        "next_allowed_step": READY_NEXT_ALLOWED_STEP,
        "non_authorization_notice": (
            "This proposal describes candidate audit completion attestation boundaries for Human Operator review only. It performs no attestation, completion, finalization, closure, audit, response, correction, enforcement, record creation, ledger creation, write, approval, handoff, scheduling, dry-run, or autonomous action."
            if ready
            else "The attestation boundary proposal is blocked and makes no readiness, execution, authorization, recording, ledger, enforcement, write, approval, handoff, scheduling, next-layer, or Civilization Core completion claim."
        ),
    }


def _proposal_components(ready: bool) -> dict[str, str]:
    status = "proposed_for_human_review_only" if ready else "blocked"
    return {component: status for component in sorted(PROPOSAL_COMPONENTS)}


def _proposed_attestation_boundaries(
    ready: bool,
) -> dict[str, dict[str, Any]]:
    status = "proposed_for_human_review_only" if ready else "blocked"
    summaries = {
        "response_audit_completion_attestation_eligibility_boundary": "Eligibility is limited to a valid sanitized v2.48 review gate and exact chain traceability.",
        "response_audit_completion_attestation_input_boundary": "Inputs are limited to structural review status, chain metadata, layer mapping, and review-only boundary shape.",
        "response_audit_completion_attestation_output_boundary": "Outputs are limited to sanitized proposal categories for a later governed review gate.",
        "response_audit_completion_attestation_non_execution_boundary": "Attestation execution remains outside this proposal.",
        "response_audit_completion_attestation_non_recording_boundary": "Attestation record creation remains outside this proposal.",
        "response_audit_completion_attestation_non_ledger_boundary": "Attestation-ledger creation remains outside this proposal.",
        "response_audit_completion_attestation_non_authorization_boundary": "Attestation authority remains outside this proposal.",
        "attestation_execution_non_authorization_boundary": "Attestation execution authority remains outside this proposal.",
        "attestation_record_non_creation_boundary": "Attestation record creation remains outside this proposal.",
        "attestation_ledger_non_creation_boundary": "Attestation-ledger creation remains outside this proposal.",
        "completion_execution_non_authorization_boundary": "Completion execution authority remains outside this proposal.",
        "completion_record_non_creation_boundary": "Completion record creation remains outside this proposal.",
        "completion_ledger_non_creation_boundary": "Completion-ledger creation remains outside this proposal.",
        "finalization_execution_non_authorization_boundary": "Finalization execution authority remains outside this proposal.",
        "finalization_record_non_creation_boundary": "Finalization record creation remains outside this proposal.",
        "finalization_ledger_non_creation_boundary": "Finalization-ledger creation remains outside this proposal.",
        "closure_execution_non_authorization_boundary": "Closure execution authority remains outside this proposal.",
        "closure_record_non_creation_boundary": "Closure record creation remains outside this proposal.",
        "closure_ledger_non_creation_boundary": "Closure-ledger creation remains outside this proposal.",
        "audit_execution_non_authorization_boundary": "Audit execution authority remains outside this proposal.",
        "audit_logging_non_execution_boundary": "Audit logging remains outside this proposal.",
        "audit_record_non_creation_boundary": "Audit record creation remains outside this proposal.",
        "audit_ledger_non_creation_boundary": "Audit-ledger creation remains outside this proposal.",
        "violation_response_non_execution_boundary": "Violation response remains outside this proposal.",
        "automated_correction_non_execution_boundary": "Automated correction remains outside this proposal.",
        "violation_enforcement_non_execution_boundary": "Violation enforcement remains outside this proposal.",
        "candidate_rule_enforcement_non_authorization_boundary": "Candidate-rule enforcement authority remains outside this proposal.",
        "human_operator_attestation_review_boundary": "Human Operator review is required before any later governed stage.",
        "evidence_lineage_attestation_boundary": "Evidence lineage is limited to source version and exact chain metadata.",
        "auditability_attestation_design_boundary": "Auditability is limited to deterministic local report structure.",
        "false_positive_attestation_prevention_boundary": "False-positive prevention remains a required later Human Operator review concern.",
        "rollback_attestation_boundary": "Rollback is a proposal category without rollback action.",
        "suspension_attestation_boundary": "Suspension is a proposal category without suspension action.",
        "memory_write_non_authorization_boundary": "Durable memory write authority remains outside this proposal.",
        "memory_graph_mutation_non_authorization_boundary": "Memory Graph mutation authority remains outside this proposal.",
        "operation_ledger_non_creation_boundary": "Operation-ledger creation remains outside this proposal.",
        "openclaw_execution_non_authorization_boundary": "OpenClaw execution remains outside this proposal.",
        "approval_non_authorization_boundary": "Approval request and approval actions remain outside this proposal.",
        "human_operator_final_authority_boundary": "Human Operator remains final authority.",
        "fifteen_memory_layers_boundary": "Fifteen Memory Layers remain the highest memory coordinate system.",
    }
    return {
        key: {
            "proposal_only": True,
            "boundary_status": status,
            "summary": summaries[key],
            "raw_source_boundary_copied": False,
            **PROPOSAL_OBJECT_FALSE_FLAGS,
        }
        for key in sorted(
            PROPOSED_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_COMPLETION_ATTESTATION_BOUNDARY_KEYS
        )
    }


def _non_authorization_boundary(ready: bool) -> dict[str, Any]:
    return {
        "proposal_ready_is_attestation_execution": False,
        "proposal_ready_is_attestation_authorization": False,
        "proposal_ready_is_attestation_record_creation": False,
        "proposal_ready_is_attestation_ledger_creation": False,
        "proposal_ready_is_completion_execution": False,
        "proposal_ready_is_completion_authorization": False,
        "proposal_ready_is_completion_record_creation": False,
        "proposal_ready_is_completion_ledger_creation": False,
        "proposal_ready_is_finalization_execution": False,
        "proposal_ready_is_closure_execution": False,
        "proposal_ready_is_audit_execution_or_logging": False,
        "proposal_ready_is_violation_response_or_correction": False,
        "proposal_ready_is_violation_or_rule_enforcement": False,
        "proposal_ready_is_autonomous_governance_or_execution": False,
        "proposal_ready_is_memory_write_or_graph_mutation": False,
        "proposal_ready_is_operation_ledger_creation": False,
        "proposal_ready_is_openclaw_execution": False,
        "proposal_ready_is_approval_or_human_decision": False,
        "proposal_ready_is_handoff_scheduling_or_dry_run": False,
        "proposal_ready_is_civilization_core_completion": False,
        "only_permits_later_attestation_boundary_review_gate": ready,
        "human_operator_remains_final_authority": True,
    }


def _preserved_governance_boundaries() -> list[str]:
    return [
        "This proposal does not perform or authorize attestation execution.",
        "This proposal does not create attestation records or attestation-ledger entries.",
        "This proposal does not perform or authorize completion, finalization, or closure execution.",
        "This proposal does not create completion, finalization, or closure records or ledger entries.",
        "This proposal does not perform or authorize audit execution or audit logging.",
        "This proposal does not create audit logs, audit records, or audit-ledger entries.",
        "This proposal does not perform or authorize violation response or automated correction.",
        "This proposal does not observe, detect, record, or enforce violations.",
        "This proposal does not enforce candidate rules or create, activate, or enforce Star-Law rules.",
        "This proposal does not authorize autonomous execution, handoff, scheduling, approval, or dry-run execution.",
        "This proposal does not write durable memory, mutate Memory Graph, create operation-ledger entries, or call OpenClaw or GitHub APIs.",
        "This proposal does not claim Civilization Core completion or entry into mature 星律, 星魂, 星宙, or 星源 stages.",
        "Human Operator remains final authority.",
    ]


def _future_review_gate_constraints() -> list[str]:
    return [
        "A later v2.50.0 attestation boundary review gate may consume this sanitized proposal through a separate governed process.",
        "A later review gate remains review-only and cannot execute attestation, completion, finalization, closure, audit, response, correction, enforcement, writes, approvals, handoffs, scheduling, or autonomous actions.",
        "No future stage may infer real Human Operator approval from this proposal.",
        "Human Operator remains final authority for all future Star-Law governance decisions.",
    ]


def _next_stage_constraints() -> list[str]:
    return [
        f"The only next allowed step is {READY_NEXT_ALLOWED_STEP}.",
        "v2.49.0 is an audit completion attestation boundary proposal only.",
        "All attestation, completion, finalization, closure, audit, response, correction, violation, enforcement, rule, write, approval, handoff, scheduling, and dry-run execution boundaries remain inactive.",
        "Mature 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, and 星源 self-evolution remain out of scope.",
    ]


def _scope_boundaries() -> list[str]:
    return [
        "Civilization Core is the total system.",
        "Fifteen Memory Layers are the highest memory coordinate system.",
        "Subspace Memory System is the engineering carrier.",
        "Hermes, Codex CLI, OpenClaw, Terminal, and GitHub are components, not the core.",
        "This v2.49.0 step is limited to 星律记忆 audit completion attestation boundary proposal only.",
    ]


def _risk_notes(sensitive_field_count: int) -> list[str]:
    notes = [
        "Proposal readiness must not be interpreted as attestation, completion, finalization, closure, audit, response, correction, enforcement, write, approval, handoff, scheduling, or autonomous authority.",
        "The report is deterministic, local-only, read-only, and contains sanitized structural summaries rather than raw source review-gate data.",
        "Civilization Core completion and later memory-layer entry are not claimed.",
    ]
    if sensitive_field_count:
        notes.append("Sensitive fields were omitted from proposal output.")
    return notes


def _required_human_actions(
    ready: bool, blocking_reasons: list[str]
) -> list[str]:
    if ready:
        return [
            "human_operator_must_review_v2_49_0_audit_completion_attestation_boundary_proposal_before_any_v2_50_0_review_gate",
            "human_operator_must_confirm_proposal_readiness_grants_no_execution_authorization_recording_ledger_enforcement_write_approval_handoff_scheduling_or_autonomous_authority",
            "human_operator_must_use_a_separate_governed_process_for_any_later_stage",
        ]
    actions = [
        "repair_source_v2_48_0_audit_completion_boundary_review_gate_before_attestation_boundary_proposal_can_continue",
        "confirm_all_unsafe_attestation_completion_finalization_closure_audit_response_correction_violation_enforcement_rule_execution_authorization_recording_ledger_write_approval_handoff_and_scheduling_flags_remain_false",
        "rerun_local_v2_49_0_audit_completion_attestation_boundary_proposal_after_blockers_are_resolved",
    ]
    if blocking_reasons:
        actions.append(
            "resolve_blocking_reasons_before_audit_completion_attestation_boundary_proposal_can_be_ready"
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


def _reviewed_boundaries_remain_review_only(
    value: Mapping[str, Any],
) -> bool:
    for boundary in value.values():
        if not isinstance(boundary, Mapping):
            return False
        if boundary.get("review_only") is not True:
            return False
        for key, nested in boundary.items():
            if nested is True and key != "review_only":
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
    "GOVERNED_STAR_LAW_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_COMPLETION_ATTESTATION_BOUNDARY_PROPOSAL_VERSION",
    "READY_NEXT_ALLOWED_STEP",
    "PROPOSED_CHAIN_VERSIONS",
    "PROPOSED_STAR_HUB_CHAIN_VERSIONS",
    "PROPOSED_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_COMPLETION_ATTESTATION_BOUNDARY_KEYS",
    "PROPOSAL_FALSE_FLAGS",
    "PROPOSAL_OBJECT_FALSE_FLAGS",
    "PROPOSAL_COMPONENTS",
    "SENSITIVE_KEYS",
    "build_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal",
    "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_boundary_proposal_to_json",
]
