from __future__ import annotations

import argparse
import io
import json
import tomllib
from pathlib import Path

from hermes_memory_fabric.p4_m0_subspace_operator import build_parser, run_operator_command
from hermes_memory_fabric.p4_m3_governed_transition_intake_final_phase_handoff_summary import (
    BOUNDARY_PHRASE_LINES,
    FALSE_STATUS_FLAGS,
    GOVERNED_TRANSITION_INTAKE_FINAL_PHASE_HANDOFF_SUMMARY_BOUNDARY,
    TRUE_STATUS_FLAGS,
    GovernedTransitionIntakeFinalPhaseHandoffSummaryField,
    governed_transition_intake_final_phase_handoff_summary_as_dicts,
    governed_transition_intake_final_phase_handoff_summary_field_ids,
    governed_transition_intake_final_phase_handoff_summary_report,
    list_governed_transition_intake_final_phase_handoff_summary_fields,
    render_governed_transition_intake_final_phase_handoff_summary_markdown,
)


FIELD_IDS = (
    "p4-m3-governed-transition-intake-final-phase-handoff-summary-id",
    "p4-m3-governed-transition-intake-phase-closure-review-reference",
    "p4-m3-governed-transition-intake-closure-handoff-contract-reference",
    "p4-m3-governed-transition-intake-final-non-validation-boundary-audit-reference",
    "p4-m3-governed-transition-intake-package-assembly-envelope-contract-reference",
    "p4-m3-governed-transition-intake-declared-transition-safeguard-envelope-contract-reference",
    "p4-m3-governed-transition-intake-declared-transition-assumption-envelope-contract-reference",
    "p4-m3-governed-transition-intake-declared-transition-risk-envelope-contract-reference",
    "p4-m3-governed-transition-intake-declared-transition-impact-envelope-contract-reference",
    "p4-m3-governed-transition-intake-declared-transition-dependency-envelope-contract-reference",
    "p4-m3-governed-transition-intake-declared-transition-constraint-envelope-contract-reference",
    "p4-m3-governed-transition-intake-declared-transition-reason-envelope-contract-reference",
    "p4-m3-governed-transition-intake-target-phase-envelope-contract-reference",
    "p4-m3-governed-transition-intake-declared-human-context-envelope-contract-reference",
    "p4-m3-governed-transition-intake-evidence-reference-envelope-contract-reference",
    "p4-m3-governed-transition-intake-request-envelope-contract-reference",
    "p4-m3-governed-transition-intake-boundary-contract-reference",
    "p4-m3-governed-transition-intake-final-phase-handoff-summary-scope",
    "p4-m3-governed-transition-intake-final-phase-handoff-summary-semantics-disabled",
    "p4-m3-governed-transition-intake-p4-m4-deferred-boundary-reference",
)

DATACLASS_FIELDS = {
    "field_order",
    "field_id",
    "field_name",
    "field_purpose",
    "p4_m3_final_phase_handoff_summary_category",
    "p4_m3_final_phase_handoff_summary_semantics_disabled",
}

REQUIRED_BOUNDARY_PHRASES = (
    "P4-M3.16",
    "Governed Transition Intake Final Phase Handoff Summary",
    "read-only",
    "definition-only",
    "inspection-only",
    "P4-M3.16 final phase handoff summary definition only",
    "P4-M3.15 Governed Transition Intake Phase Closure Review remains the source phase closure review",
    "P4-M3.14 Governed Transition Intake Closure Handoff Contract remains the source closure handoff contract",
    "P4-M3.13 Governed Transition Intake Final Non-Validation Boundary Audit remains the source final non-validation boundary audit",
    "P4-M3.12 Governed Transition Intake Package Assembly Envelope Contract remains the source package assembly envelope boundary",
    "P4-M3.11 Governed Transition Intake Declared Transition Safeguard Envelope Contract remains the source declared transition safeguard envelope boundary",
    "P4-M3.10 Governed Transition Intake Declared Transition Assumption Envelope Contract remains the source declared transition assumption envelope boundary",
    "P4-M3.9 Governed Transition Intake Declared Transition Risk Envelope Contract remains the source declared transition risk envelope boundary",
    "P4-M3.8 Governed Transition Intake Declared Transition Impact Envelope Contract remains the source declared transition impact envelope boundary",
    "P4-M3.7 Governed Transition Intake Declared Transition Dependency Envelope Contract remains the source declared transition dependency envelope boundary",
    "P4-M3.6 Governed Transition Intake Declared Transition Constraint Envelope Contract remains the source declared transition constraint envelope boundary",
    "P4-M3.5 Governed Transition Intake Declared Transition Reason Envelope Contract remains the source declared transition reason envelope boundary",
    "P4-M3.4 Governed Transition Intake Target Phase Envelope Contract remains the source target phase envelope boundary",
    "P4-M3.3 Governed Transition Intake Declared Human Context Envelope Contract remains the source declared human context envelope boundary",
    "P4-M3.2 Governed Transition Intake Evidence Reference Envelope Contract remains the source evidence reference envelope boundary",
    "P4-M3.1 Governed Transition Intake Request Envelope Contract remains the source request envelope boundary",
    "P4-M3.0 Governed Transition Intake Boundary Contract remains the source intake boundary",
    "P4-M3 static definition chain remains closed",
    "P4-M4 remains deferred",
    "P4-M4 entry gate remains not implemented",
    "P4-M3.16 is not live validation",
    "P4-M3.16 is not phase validation",
    "P4-M3.16 is not final phase validation",
    "P4-M3.16 is not transition intake validation",
    "P4-M3.16 is not package validation",
    "P4-M3.16 is not final audit validation",
    "P4-M3.16 is not closure validation",
    "P4-M3.16 is not handoff validation",
    "P4-M3.16 is not phase closure validation",
    "P4-M3.16 is not final phase handoff validation",
    "P4-M3.16 is not entry gate validation",
    "P4-M3.16 is not P4-M4 entry gate implementation",
    "P4-M3.16 is not P4-M4 activation",
    "P4-M3.16 is not P4-M4 execution",
    "P4-M3.16 is not closure execution",
    "P4-M3.16 is not handoff execution",
    "P4-M3.16 is not phase closure execution",
    "P4-M3.16 is not final phase handoff execution",
    "P4-M3.16 is not readiness verdict",
    "P4-M3.16 is not validation verdict",
    "P4-M3.16 is not closure verdict",
    "P4-M3.16 is not handoff verdict",
    "P4-M3.16 is not phase closure verdict",
    "P4-M3.16 is not final phase handoff verdict",
    "P4-M3.16 is not P4-M4 entry verdict",
    "P4-M3.16 is not boundary certification",
    "P4-M3.16 is not approval",
    "P4-M3.16 is not authorization",
    "P4-M3.16 is not confirmation",
    "P4-M3.16 is not recommendation",
    "P4-M3.16 is not ranking",
    "P4-M3.16 is not next action generation",
    "P4-M3.16 is not transition execution",
    "P4-M3.16 is not request validation",
    "P4-M3.16 is not evidence validation",
    "P4-M3.16 is not human context validation",
    "P4-M3.16 is not source validation",
    "P4-M3.16 is not citation validation",
    "P4-M3.16 is not transition record creation",
    "P4-M3.16 is not request record creation",
    "P4-M3.16 is not package record creation",
    "P4-M3.16 is not closure record creation",
    "P4-M3.16 is not handoff record creation",
    "P4-M3.16 is not phase closure record creation",
    "P4-M3.16 is not final phase handoff record creation",
    "P4-M3.16 is not P4-M4 entry record creation",
    "P4-M3.16 is not memory mutation",
    "P4-M3.16 is not roadmap mutation",
    "P4-M3.16 is not lifecycle mutation",
    "P4-M3.16 is not proposal mutation",
    "P4-M3.16 is not source fetching",
    "P4-M3.16 is not provenance writing",
    "P4-M3.16 is not citation mutation",
    "no live validation",
    "no phase validation",
    "no final phase validation",
    "no transition intake validation",
    "no package validation",
    "no final audit validation",
    "no closure validation",
    "no handoff validation",
    "no phase closure validation",
    "no final phase handoff validation",
    "no entry gate validation",
    "no P4-M4 entry gate implementation",
    "no P4-M4 activation",
    "no P4-M4 execution",
    "no closure execution",
    "no handoff execution",
    "no phase closure execution",
    "no final phase handoff execution",
    "no readiness verdict",
    "no validation verdict",
    "no closure verdict",
    "no handoff verdict",
    "no phase closure verdict",
    "no final phase handoff verdict",
    "no P4-M4 entry verdict",
    "no boundary certification",
    "no approval",
    "no authorization",
    "no confirmation",
    "no recommendation",
    "no ranking",
    "no next action generation",
    "no transition execution",
    "no request validation",
    "no evidence validation",
    "no memory mutation",
    "no roadmap mutation",
    "no phase closure record creation",
    "no final phase handoff record creation",
    "no P4-M4 entry record creation",
    "no phase closure mutation",
    "no final phase handoff mutation",
    "no P4-M4",
    "no P4-M5",
    "no v7",
    "no productization",
    "no UI",
    "no Operator Console",
    "no version bump",
    "no tag",
)

EXPECTED_TRUE_STATUS_FLAGS = (
    "definition_only",
    "inspection_only",
    "p4_m3_final_phase_handoff_summary_definition_started",
    "p4_m3_16_governed_transition_intake_final_phase_handoff_summary_started",
    "p4_m3_16_definition_only",
    "p4_m3_15_phase_closure_review_reference_defined",
    "p4_m3_14_closure_handoff_contract_reference_defined",
    "p4_m3_13_final_non_validation_boundary_audit_reference_defined",
    "p4_m3_12_package_assembly_envelope_contract_reference_defined",
    "p4_m3_11_declared_transition_safeguard_envelope_contract_reference_defined",
    "p4_m3_10_declared_transition_assumption_envelope_contract_reference_defined",
    "p4_m3_9_declared_transition_risk_envelope_contract_reference_defined",
    "p4_m3_8_declared_transition_impact_envelope_contract_reference_defined",
    "p4_m3_7_declared_transition_dependency_envelope_contract_reference_defined",
    "p4_m3_6_declared_transition_constraint_envelope_contract_reference_defined",
    "p4_m3_5_declared_transition_reason_envelope_contract_reference_defined",
    "p4_m3_4_target_phase_envelope_contract_reference_defined",
    "p4_m3_3_declared_human_context_envelope_contract_reference_defined",
    "p4_m3_2_evidence_reference_envelope_contract_reference_defined",
    "p4_m3_1_request_envelope_contract_reference_defined",
    "p4_m3_0_intake_boundary_contract_reference_defined",
    "p4_m3_final_phase_handoff_summary_defined",
    "p4_m3_final_phase_handoff_summary_scope_defined",
    "p4_m3_final_phase_handoff_summary_field_shape_defined",
    "p4_m3_governed_transition_intake_static_definition_chain_reviewed_for_final_handoff",
    "p4_m3_static_definition_chain_closed_before_p4_m4_entry_gate_design_boundary",
    "p4_m3_static_definition_chain_final_handoff_summary_defined",
    "p4_m4_entry_gate_deferred",
    "p4_m4_start_deferred",
    "p4_m4_entry_gate_design_boundary_deferred_to_future_work",
    "p4_m3_live_validation_semantics_prohibited",
    "p4_m3_phase_validation_semantics_prohibited",
    "p4_m3_final_phase_validation_semantics_prohibited",
    "p4_m3_transition_intake_validation_semantics_prohibited",
    "p4_m3_transition_intake_package_validation_semantics_prohibited",
    "p4_m3_final_audit_validation_semantics_prohibited",
    "p4_m3_closure_validation_semantics_prohibited",
    "p4_m3_handoff_validation_semantics_prohibited",
    "p4_m3_phase_closure_validation_semantics_prohibited",
    "p4_m3_final_phase_handoff_validation_semantics_prohibited",
    "p4_m3_entry_gate_validation_semantics_prohibited",
    "p4_m4_entry_gate_implementation_semantics_prohibited",
    "p4_m4_activation_semantics_prohibited",
    "p4_m4_execution_semantics_prohibited",
    "p4_m3_closure_execution_semantics_prohibited",
    "p4_m3_handoff_execution_semantics_prohibited",
    "p4_m3_phase_closure_execution_semantics_prohibited",
    "p4_m3_final_phase_handoff_execution_semantics_prohibited",
    "p4_m3_transition_readiness_verdict_semantics_prohibited",
    "p4_m3_transition_validation_verdict_semantics_prohibited",
    "p4_m3_closure_verdict_semantics_prohibited",
    "p4_m3_handoff_verdict_semantics_prohibited",
    "p4_m3_phase_closure_verdict_semantics_prohibited",
    "p4_m3_final_phase_handoff_verdict_semantics_prohibited",
    "p4_m4_entry_verdict_semantics_prohibited",
    "p4_m3_boundary_certification_semantics_prohibited",
    "p4_m3_transition_execution_semantics_prohibited",
    "p4_m3_transition_authorization_semantics_prohibited",
    "p4_m3_transition_approval_semantics_prohibited",
    "p4_m3_transition_confirmation_semantics_prohibited",
    "p4_m3_transition_recommendation_semantics_prohibited",
    "p4_m3_transition_ranking_semantics_prohibited",
    "p4_m3_transition_next_action_semantics_prohibited",
    "p4_m3_request_validation_semantics_prohibited",
    "p4_m3_evidence_validation_semantics_prohibited",
    "p4_m3_human_context_validation_semantics_prohibited",
    "p4_m3_transition_mutation_semantics_prohibited",
    "p4_m3_closure_mutation_semantics_prohibited",
    "p4_m3_handoff_mutation_semantics_prohibited",
    "p4_m3_phase_closure_mutation_semantics_prohibited",
    "p4_m3_final_phase_handoff_mutation_semantics_prohibited",
)

EXPECTED_FALSE_STATUS_FLAGS = (
    "live_validation_enabled",
    "boundary_validation_enabled",
    "phase_validation_enabled",
    "final_phase_validation_enabled",
    "transition_intake_validation_enabled",
    "transition_intake_package_validation_enabled",
    "final_audit_validation_enabled",
    "closure_validation_enabled",
    "handoff_validation_enabled",
    "phase_closure_validation_enabled",
    "final_phase_handoff_validation_enabled",
    "entry_gate_validation_enabled",
    "p4_m4_entry_gate_implementation_enabled",
    "p4_m4_activation_enabled",
    "p4_m4_execution_enabled",
    "closure_execution_enabled",
    "handoff_execution_enabled",
    "phase_closure_execution_enabled",
    "final_phase_handoff_execution_enabled",
    "package_correctness_validation_enabled",
    "package_completeness_validation_enabled",
    "package_consistency_validation_enabled",
    "package_integrity_validation_enabled",
    "package_readiness_validation_enabled",
    "package_readiness_verdict_enabled",
    "package_validation_verdict_enabled",
    "reference_resolution_enabled",
    "reference_integrity_validation_enabled",
    "reference_completeness_validation_enabled",
    "boundary_certification_enabled",
    "package_assembly_execution_enabled",
    "package_persistence_enabled",
    "package_storage_enabled",
    "package_mutation_enabled",
    "closure_persistence_enabled",
    "closure_storage_enabled",
    "closure_mutation_enabled",
    "handoff_persistence_enabled",
    "handoff_storage_enabled",
    "handoff_mutation_enabled",
    "phase_closure_persistence_enabled",
    "phase_closure_storage_enabled",
    "phase_closure_mutation_enabled",
    "final_phase_handoff_persistence_enabled",
    "final_phase_handoff_storage_enabled",
    "final_phase_handoff_mutation_enabled",
    "transition_intake_package_record_creation_enabled",
    "transition_intake_package_record_update_enabled",
    "transition_intake_package_record_deletion_enabled",
    "closure_record_creation_enabled",
    "closure_record_update_enabled",
    "closure_record_deletion_enabled",
    "handoff_record_creation_enabled",
    "handoff_record_update_enabled",
    "handoff_record_deletion_enabled",
    "phase_closure_record_creation_enabled",
    "phase_closure_record_update_enabled",
    "phase_closure_record_deletion_enabled",
    "final_phase_handoff_record_creation_enabled",
    "final_phase_handoff_record_update_enabled",
    "final_phase_handoff_record_deletion_enabled",
    "p4_m4_entry_record_creation_enabled",
    "p4_m4_entry_record_update_enabled",
    "p4_m4_entry_record_deletion_enabled",
    "transition_safeguard_validation_enabled",
    "transition_assumption_validation_enabled",
    "transition_risk_validation_enabled",
    "transition_impact_validation_enabled",
    "transition_dependency_validation_enabled",
    "transition_constraint_validation_enabled",
    "transition_reason_validation_enabled",
    "target_phase_validation_enabled",
    "target_phase_selection_enabled",
    "transition_readiness_validation_enabled",
    "live_transition_readiness_validation_enabled",
    "readiness_verdict_enabled",
    "transition_readiness_verdict_enabled",
    "validation_verdict_enabled",
    "transition_validation_verdict_enabled",
    "closure_verdict_enabled",
    "handoff_verdict_enabled",
    "phase_closure_verdict_enabled",
    "final_phase_handoff_verdict_enabled",
    "p4_m4_entry_verdict_enabled",
    "execution_enabled",
    "decision_execution_enabled",
    "transition_execution_enabled",
    "transition_command_execution_enabled",
    "authorization_enabled",
    "transition_authorization_enabled",
    "approval_enabled",
    "transition_approval_enabled",
    "confirmation_enabled",
    "transition_confirmation_enabled",
    "recommendation_enabled",
    "transition_recommendation_enabled",
    "ranking_enabled",
    "transition_ranking_enabled",
    "suggested_next_action_enabled",
    "next_action_generation_enabled",
    "transition_record_creation_enabled",
    "request_record_creation_enabled",
    "package_record_creation_enabled",
    "transition_readiness_record_creation_enabled",
    "transition_validation_record_creation_enabled",
    "transition_approval_record_creation_enabled",
    "transition_authorization_record_creation_enabled",
    "transition_confirmation_record_creation_enabled",
    "transition_execution_record_creation_enabled",
    "transition_recommendation_record_creation_enabled",
    "transition_ranking_record_creation_enabled",
    "transition_next_action_record_creation_enabled",
    "live_request_intake_enabled",
    "request_acceptance_enabled",
    "request_rejection_enabled",
    "request_validation_enabled",
    "request_schema_validation_enabled",
    "request_content_validation_enabled",
    "request_completeness_validation_enabled",
    "request_eligibility_validation_enabled",
    "request_persistence_enabled",
    "request_storage_enabled",
    "request_mutation_enabled",
    "request_record_update_enabled",
    "request_record_deletion_enabled",
    "evidence_validation_enabled",
    "evidence_scoring_enabled",
    "evidence_ranking_enabled",
    "evidence_precedence_enabled",
    "evidence_arbitration_enabled",
    "evidence_winner_selection_enabled",
    "evidence_record_creation_enabled",
    "human_context_validation_enabled",
    "human_context_mutation_enabled",
    "human_context_record_creation_enabled",
    "human_confirmation_enabled",
    "human_approval_enabled",
    "human_authorization_enabled",
    "consent_validation_enabled",
    "identity_verification_enabled",
    "source_validation_enabled",
    "citation_validation_enabled",
    "source_fetching_enabled",
    "provenance_writing_enabled",
    "citation_mutation_enabled",
    "input_validation_enabled",
    "record_validation_enabled",
    "memory_mutation_enabled",
    "memory_record_creation_enabled",
    "memory_record_update_enabled",
    "memory_record_deletion_enabled",
    "proposal_mutation_enabled",
    "lifecycle_mutation_enabled",
    "retry_policy_mutation_enabled",
    "evidence_mutation_enabled",
    "roadmap_mutation_enabled",
    "api_enabled",
    "mcp_enabled",
    "connector_enabled",
    "agent_call_enabled",
    "codex_hermes_chatgpt_product_code_auto_call_enabled",
    "p4_m4_started",
    "p4_m4_command_enabled",
    "p4_m4_activation_enabled",
    "p4_m4_implementation_enabled",
    "p4_m4_entry_gate_design_boundary_contract_enabled",
    "p4_m5_started",
    "v7_started",
    "productization_started",
    "ui_started",
    "operator_console_started",
    "mvp_started",
    "deploy_started",
    "full_memory_graph_started",
    "version_bump_enabled",
    "tag_creation_enabled",
)

EXPECTED_MEMORY_LOOP_COMMANDS = {
    "checklist",
    "review-status",
    "recall-verification-status",
    "lifecycle-verification-status",
    "do-not-retry-verification-status",
    "source-provenance-verification-status",
    "decision-readiness-status",
    "manual-decision-preview",
    "governance-pack-export",
    "final-boundary-audit",
    "manual-execution-hardening",
    "execution-surface-contract",
    "execution-contract-validation-matrix",
    "manual-authorization-evidence-envelope",
    "human-confirmation-snapshot-contract",
    "execution-preconditions-snapshot-map",
    "execution-risk-acknowledgement-map",
    "execution-risk-acceptance-prohibition-map",
    "execution-risk-waiver-prohibition-map",
    "execution-decision-non-equivalence-map",
    "execution-decision-recommendation-prohibition-map",
    "execution-decision-default-denial-boundary-map",
    "execution-decision-silence-non-consent-map",
    "execution-decision-negative-evidence-non-override-map",
    "execution-decision-conflicting-evidence-isolation-map",
    "execution-decision-evidence-precedence-prohibition-map",
    "final-non-execution-boundary-audit",
    "p4-m2-closure-handoff-contract",
    "governed-transition-intake-boundary-contract",
    "governed-transition-intake-request-envelope-contract",
    "governed-transition-intake-evidence-reference-envelope-contract",
    "governed-transition-intake-declared-human-context-envelope-contract",
    "governed-transition-intake-target-phase-envelope-contract",
    "governed-transition-intake-declared-transition-reason-envelope-contract",
    "governed-transition-intake-declared-transition-constraint-envelope-contract",
    "governed-transition-intake-declared-transition-dependency-envelope-contract",
    "governed-transition-intake-declared-transition-impact-envelope-contract",
    "governed-transition-intake-declared-transition-risk-envelope-contract",
    "governed-transition-intake-declared-transition-assumption-envelope-contract",
    "governed-transition-intake-declared-transition-safeguard-envelope-contract",
    "governed-transition-intake-package-assembly-envelope-contract",
    "governed-transition-intake-final-non-validation-boundary-audit",
    "governed-transition-intake-closure-handoff-contract",
    "governed-transition-intake-phase-closure-review",
    "governed-transition-intake-final-phase-handoff-summary",
    "entry-gate-design-boundary-contract",
    "entry-gate-design-request-envelope-contract",
    "evidence-reference-envelope-contract",
    "declared-human-context-envelope-contract",
    "target-phase-envelope-contract",
    "declared-transition-reason-envelope-contract",
    "declared-transition-constraint-envelope-contract",
    "declared-transition-dependency-envelope-contract",
    "declared-transition-impact-envelope-contract",
    "declared-transition-risk-envelope-contract",
    "declared-transition-assumption-envelope-contract",
    "declared-transition-safeguard-envelope-contract",
}

PREVIOUS_P4_M3_15_READ_ONLY_COMMANDS = EXPECTED_MEMORY_LOOP_COMMANDS - {
    "governed-transition-intake-final-phase-handoff-summary"
}

PROHIBITED_MEMORY_LOOP_COMMANDS = {
    "validate-transition-intake",
    "validate-package",
    "validate-final-audit",
    "validate-closure",
    "validate-handoff",
    "validate-phase-closure",
    "validate-final-phase-handoff",
    "validate-entry-gate",
    "implement-p4-m4-entry-gate",
    "activate-p4-m4",
    "execute-p4-m4",
    "execute-closure",
    "execute-handoff",
    "execute-phase-closure",
    "execute-final-phase-handoff",
    "readiness-verdict",
    "validation-verdict",
    "closure-verdict",
    "handoff-verdict",
    "phase-closure-verdict",
    "final-phase-handoff-verdict",
    "p4-m4-entry-verdict",
    "certify-boundaries",
    "execute-transition",
    "authorize-transition",
    "approve-transition",
    "confirm-transition",
    "recommend-transition",
    "rank-transition",
    "suggest-next-action",
    "create-transition-record",
    "create-request-record",
    "create-package-record",
    "create-closure-record",
    "create-handoff-record",
    "create-phase-closure-record",
    "create-final-phase-handoff-record",
    "create-p4-m4-entry-record",
    "validate-request",
    "validate-evidence",
    "validate-human-context",
    "fetch-source",
    "write-provenance",
    "mutate-citation",
    "write-memory",
    "start-p4-m4",
    "start-p4-m5",
    "start-v7",
    "productize",
    "operator-console",
    "ui",
    "deploy",
}


def test_final_phase_handoff_summary_field_order_count_and_ids_are_stable():
    fields = list_governed_transition_intake_final_phase_handoff_summary_fields()

    assert [field.field_order for field in fields] == list(range(1, 21))
    assert len(fields) == 20
    assert governed_transition_intake_final_phase_handoff_summary_field_ids() == FIELD_IDS


def test_every_final_phase_handoff_summary_field_has_required_values():
    for field in list_governed_transition_intake_final_phase_handoff_summary_fields():
        assert field.field_name.strip()
        assert field.field_purpose.strip()
        assert field.p4_m3_final_phase_handoff_summary_category.strip()
        assert field.p4_m3_final_phase_handoff_summary_semantics_disabled.strip()


def test_required_boundary_phrase_contract_contains_all_required_phrases():
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in BOUNDARY_PHRASE_LINES


def test_required_status_flag_contract_is_literal_and_complete():
    assert TRUE_STATUS_FLAGS == EXPECTED_TRUE_STATUS_FLAGS
    assert FALSE_STATUS_FLAGS == EXPECTED_FALSE_STATUS_FLAGS


def test_markdown_output_is_stable_and_contains_required_boundaries():
    first = render_governed_transition_intake_final_phase_handoff_summary_markdown()
    second = render_governed_transition_intake_final_phase_handoff_summary_markdown()

    assert first == second
    assert first.startswith(
        "# P4-M3.16 Governed Transition Intake Final Phase Handoff Summary\n"
    )
    assert GOVERNED_TRANSITION_INTAKE_FINAL_PHASE_HANDOFF_SUMMARY_BOUNDARY in first
    for field_id in FIELD_IDS:
        assert field_id in first
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in first


def test_json_output_is_stable_and_contains_required_boundaries(tmp_path):
    args = [
        "memory-loop",
        "governed-transition-intake-final-phase-handoff-summary",
        "--workspace-root",
        str(tmp_path),
        "--format",
        "json",
    ]
    first_code, first_payload, first_stderr, first_stdout = _run_operator(args)
    second_code, second_payload, second_stderr, second_stdout = _run_operator(args)

    assert first_code == 0
    assert second_code == 0
    assert first_stderr == ""
    assert second_stderr == ""
    assert first_stdout == second_stdout
    assert first_payload == second_payload
    assert first_payload["boundary"] == GOVERNED_TRANSITION_INTAKE_FINAL_PHASE_HANDOFF_SUMMARY_BOUNDARY
    assert first_payload["count"] == 20
    assert first_payload["status"]["phase"] == "P4-M3.16"
    assert (
        first_payload["status"]["feature"]
        == "Governed Transition Intake Final Phase Handoff Summary"
    )
    assert first_payload["status"]["mode"] == "read-only"
    assert first_payload["status"] == governed_transition_intake_final_phase_handoff_summary_report()
    assert [item["field_id"] for item in first_payload["fields"]] == list(FIELD_IDS)
    assert set(first_payload["fields"][0]) == DATACLASS_FIELDS
    for flag in EXPECTED_TRUE_STATUS_FLAGS:
        assert first_payload["status"][flag] is True
    for flag in EXPECTED_FALSE_STATUS_FLAGS:
        assert first_payload["status"][flag] is False
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in first_stdout
    assert not (tmp_path / ".local").exists()


def test_dict_conversion_and_status_report_are_deterministic():
    first_fields = governed_transition_intake_final_phase_handoff_summary_as_dicts()
    second_fields = governed_transition_intake_final_phase_handoff_summary_as_dicts()
    first_status = governed_transition_intake_final_phase_handoff_summary_report()
    second_status = governed_transition_intake_final_phase_handoff_summary_report()

    assert first_fields == second_fields
    assert [field["field_id"] for field in first_fields] == list(FIELD_IDS)
    assert first_status == second_status
    assert first_status["phase"] == "P4-M3.16"
    assert (
        first_status["feature"]
        == "Governed Transition Intake Final Phase Handoff Summary"
    )
    assert first_status["mode"] == "read-only"
    assert (
        first_status["governed_transition_intake_final_phase_handoff_summary_field_count"]
        == 20
    )
    assert first_status["boundary"] == GOVERNED_TRANSITION_INTAKE_FINAL_PHASE_HANDOFF_SUMMARY_BOUNDARY


def test_status_report_locks_true_and_disabled_flags():
    status = governed_transition_intake_final_phase_handoff_summary_report()

    for flag in EXPECTED_TRUE_STATUS_FLAGS:
        assert status[flag] is True
    for flag in EXPECTED_FALSE_STATUS_FLAGS:
        assert status[flag] is False


def test_operator_markdown_default_is_read_only_and_creates_no_local_storage(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "governed-transition-intake-final-phase-handoff-summary",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith(
        "# P4-M3.16 Governed Transition Intake Final Phase Handoff Summary\n"
    )
    assert "## Status Report" in stdout
    assert GOVERNED_TRANSITION_INTAKE_FINAL_PHASE_HANDOFF_SUMMARY_BOUNDARY in stdout
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in stdout
    assert not (tmp_path / ".local").exists()


def test_operator_markdown_format_is_explicit_and_stable(tmp_path):
    args = [
        "memory-loop",
        "governed-transition-intake-final-phase-handoff-summary",
        "--workspace-root",
        str(tmp_path),
        "--format",
        "markdown",
    ]
    first_code, first_payload, first_stderr, first_stdout = _run_operator(args)
    second_code, second_payload, second_stderr, second_stdout = _run_operator(args)

    assert first_code == 0
    assert second_code == 0
    assert first_payload == {}
    assert second_payload == {}
    assert first_stderr == ""
    assert second_stderr == ""
    assert first_stdout == second_stdout
    assert first_stdout.startswith("# P4-M3.16")
    assert not (tmp_path / ".local").exists()


def test_command_does_not_instantiate_writable_store(monkeypatch, tmp_path):
    def fail_store_creation(*_args, **_kwargs):
        raise AssertionError("writable store must not be instantiated")

    monkeypatch.setattr(
        "hermes_memory_fabric.p4_m0_subspace_operator.create_workspace_subspace_memory_store",
        fail_store_creation,
    )

    markdown_code, _, markdown_stderr, markdown_stdout = _run_operator(
        [
            "memory-loop",
            "governed-transition-intake-final-phase-handoff-summary",
            "--workspace-root",
            str(tmp_path),
        ]
    )
    json_code, json_payload, json_stderr, _ = _run_operator(
        [
            "memory-loop",
            "governed-transition-intake-final-phase-handoff-summary",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert markdown_code == 0
    assert markdown_stderr == ""
    assert markdown_stdout.startswith("# P4-M3.16")
    assert json_code == 0
    assert json_stderr == ""
    assert json_payload["count"] == 20
    assert not (tmp_path / ".local").exists()


def test_command_creates_no_storage_files_or_state_changes(tmp_path):
    _run_operator(
        [
            "memory-loop",
            "governed-transition-intake-final-phase-handoff-summary",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    storage_root = tmp_path / ".local" / "subspace_memory"
    for filename in (
        "transition_intake_final_phase_handoff_summary.jsonl",
        "final_phase_handoff_summary.jsonl",
        "final_phase_handoff_records.jsonl",
        "final_phase_handoff_validation.jsonl",
        "final_phase_handoff_execution.jsonl",
        "transition_intake_phase_closure_review.jsonl",
        "phase_closure_review.jsonl",
        "phase_closure_records.jsonl",
        "phase_closure_validation.jsonl",
        "phase_closure_execution.jsonl",
        "p4_m4_entry_gate.jsonl",
        "p4_m4_entry_records.jsonl",
        "p4_m4_entry_validation.jsonl",
        "transition_intake_closure_handoff_contract.jsonl",
        "closure_handoff_contract.jsonl",
        "closure_records.jsonl",
        "handoff_records.jsonl",
        "closure_validation.jsonl",
        "handoff_validation.jsonl",
        "closure_execution.jsonl",
        "handoff_execution.jsonl",
        "transition_intake_final_non_validation_boundary_audit.jsonl",
        "final_non_validation_boundary_audit.jsonl",
        "transition_intake_validation.jsonl",
        "transition_intake_package_validation.jsonl",
        "transition_intake_package_records.jsonl",
        "transition_intake_packages.jsonl",
        "package_assembly.jsonl",
        "package_validation.jsonl",
        "reference_resolution.jsonl",
        "reference_validation.jsonl",
        "request_records.jsonl",
        "package_records.jsonl",
        "transition_records.jsonl",
        "transition_readiness_records.jsonl",
        "transition_validation_records.jsonl",
        "transition_approval_records.jsonl",
        "transition_authorization_records.jsonl",
        "transition_confirmation_records.jsonl",
        "transition_execution_records.jsonl",
        "transition_recommendation_records.jsonl",
        "transition_ranking_records.jsonl",
        "transition_next_action_records.jsonl",
        "human_context_records.jsonl",
        "evidence_records.jsonl",
        "execution.jsonl",
        "authorization.jsonl",
        "confirmation.jsonl",
        "approvals.jsonl",
        "recommendations.jsonl",
        "rankings.jsonl",
        "next_actions.jsonl",
        "validation.jsonl",
        "readiness.jsonl",
        "memories.jsonl",
        "proposals.jsonl",
        "lifecycle.jsonl",
        "sources.jsonl",
        "provenance.jsonl",
        "evidence.jsonl",
        "citations.jsonl",
        "roadmap.jsonl",
        "audit.jsonl",
    ):
        assert not (storage_root / filename).exists()
    assert not (tmp_path / ".local").exists()


def test_read_only_allowlist_includes_new_command_and_preserves_previous_commands():
    commands = _memory_loop_commands()

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
    assert "governed-transition-intake-final-phase-handoff-summary" in commands
    assert PREVIOUS_P4_M3_15_READ_ONLY_COMMANDS.issubset(commands)
    assert commands.isdisjoint(PROHIBITED_MEMORY_LOOP_COMMANDS)


def test_doc_contains_required_boundaries():
    doc = Path(
        "docs/CIVILIZATION_CORE_P4_M3_16_GOVERNED_TRANSITION_INTAKE_FINAL_PHASE_HANDOFF_SUMMARY.md"
    ).read_text()

    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in doc
    for field_id in FIELD_IDS:
        assert field_id in doc


def test_package_version_lock_and_no_entry_point():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert pyproject["project"]["version"] == "6.16.0"
    assert "scripts" not in pyproject["project"]
    assert "gui-scripts" not in pyproject["project"]
    assert "console_scripts" not in pyproject["project"].get("entry-points", {})
    entry_points = json.dumps(pyproject["project"].get("entry-points", {}), sort_keys=True)
    assert "p4_m3_governed_transition_intake_final_phase_handoff_summary" not in entry_points
    assert "governed-transition-intake-final-phase-handoff-summary" not in entry_points


def test_no_uv_lock_is_created():
    assert not Path("uv.lock").exists()


def test_custom_markdown_render_accepts_read_only_fields():
    field = GovernedTransitionIntakeFinalPhaseHandoffSummaryField(
        field_order=1,
        field_id="custom-governed-transition-intake-final-phase-handoff-summary",
        field_name="Custom Governed Transition Intake Final Phase Handoff Summary Field",
        field_purpose="Custom inspection-only purpose.",
        p4_m3_final_phase_handoff_summary_category=(
            "custom-governed-transition-intake-final-phase-handoff-summary-category"
        ),
        p4_m3_final_phase_handoff_summary_semantics_disabled=(
            "Custom governed transition intake final phase handoff summary semantics are disabled."
        ),
    )

    markdown = render_governed_transition_intake_final_phase_handoff_summary_markdown(
        [field]
    )

    assert "custom-governed-transition-intake-final-phase-handoff-summary" in markdown
    assert "Custom inspection-only purpose." in markdown


def _run_operator(argv: list[str]) -> tuple[int, dict[str, object], str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_operator_command(argv, stdout=stdout, stderr=stderr)

    stdout_value = stdout.getvalue()
    payload = json.loads(stdout_value) if stdout_value.startswith("{") else {}
    return exit_code, payload, stderr.getvalue(), stdout_value


def _memory_loop_commands() -> set[str]:
    parser = build_parser()
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            memory_loop_parser = action.choices["memory-loop"]
            break
    else:
        raise AssertionError("memory-loop parser not found")

    for action in memory_loop_parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            return set(action.choices)
    raise AssertionError("memory-loop subcommands not found")
