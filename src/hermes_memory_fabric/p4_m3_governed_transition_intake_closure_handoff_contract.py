from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence

from .p4_m2_closure_handoff_contract import closure_handoff_contract_field_ids
from .p4_m3_governed_transition_intake_boundary_contract import governed_transition_intake_boundary_contract_field_ids
from .p4_m3_governed_transition_intake_declared_human_context_envelope_contract import governed_transition_intake_declared_human_context_envelope_contract_field_ids
from .p4_m3_governed_transition_intake_declared_transition_assumption_envelope_contract import governed_transition_intake_declared_transition_assumption_envelope_contract_field_ids
from .p4_m3_governed_transition_intake_declared_transition_constraint_envelope_contract import governed_transition_intake_declared_transition_constraint_envelope_contract_field_ids
from .p4_m3_governed_transition_intake_declared_transition_dependency_envelope_contract import governed_transition_intake_declared_transition_dependency_envelope_contract_field_ids
from .p4_m3_governed_transition_intake_declared_transition_impact_envelope_contract import governed_transition_intake_declared_transition_impact_envelope_contract_field_ids
from .p4_m3_governed_transition_intake_declared_transition_reason_envelope_contract import governed_transition_intake_declared_transition_reason_envelope_contract_field_ids
from .p4_m3_governed_transition_intake_declared_transition_risk_envelope_contract import governed_transition_intake_declared_transition_risk_envelope_contract_field_ids
from .p4_m3_governed_transition_intake_declared_transition_safeguard_envelope_contract import governed_transition_intake_declared_transition_safeguard_envelope_contract_field_ids
from .p4_m3_governed_transition_intake_evidence_reference_envelope_contract import governed_transition_intake_evidence_reference_envelope_contract_field_ids
from .p4_m3_governed_transition_intake_final_non_validation_boundary_audit import governed_transition_intake_final_non_validation_boundary_audit_field_ids
from .p4_m3_governed_transition_intake_package_assembly_envelope_contract import governed_transition_intake_package_assembly_envelope_contract_field_ids
from .p4_m3_governed_transition_intake_request_envelope_contract import governed_transition_intake_request_envelope_contract_field_ids
from .p4_m3_governed_transition_intake_target_phase_envelope_contract import governed_transition_intake_target_phase_envelope_contract_field_ids


P4_M3_14_PACKAGE_VERSION = "6.16.0"


@dataclass(frozen=True)
class GovernedTransitionIntakeClosureHandoffContractField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    p4_m3_closure_handoff_contract_category: str
    p4_m3_closure_handoff_semantics_disabled: str


PRIOR_DEFINITION_LAYER_REFERENCES = (
    "P4-M3.13 Governed Transition Intake Final Non-Validation Boundary Audit",
    "P4-M3.12 Governed Transition Intake Package Assembly Envelope Contract",
    "P4-M3.11 Governed Transition Intake Declared Transition Safeguard Envelope Contract",
    "P4-M3.10 Governed Transition Intake Declared Transition Assumption Envelope Contract",
    "P4-M3.9 Governed Transition Intake Declared Transition Risk Envelope Contract",
    "P4-M3.8 Governed Transition Intake Declared Transition Impact Envelope Contract",
    "P4-M3.7 Governed Transition Intake Declared Transition Dependency Envelope Contract",
    "P4-M3.6 Governed Transition Intake Declared Transition Constraint Envelope Contract",
    "P4-M3.5 Governed Transition Intake Declared Transition Reason Envelope Contract",
    "P4-M3.4 Governed Transition Intake Target Phase Envelope Contract",
    "P4-M3.3 Governed Transition Intake Declared Human Context Envelope Contract",
    "P4-M3.2 Governed Transition Intake Evidence Reference Envelope Contract",
    "P4-M3.1 Governed Transition Intake Request Envelope Contract",
    "P4-M3.0 Governed Transition Intake Boundary Contract",
    "P4-M2.17 P4-M2 Closure Handoff Contract",
)

BOUNDARY_PHRASE_LINES = (
    "P4-M3.14",
    "Governed Transition Intake Closure Handoff Contract",
    "read-only",
    "definition-only",
    "inspection-only",
    "P4-M3.14 closure handoff contract definition only",
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
    "P4-M2.17 P4-M2 Closure Handoff Contract remains the prior closure handoff reference",
    "P4-M3.14 is not live validation",
    "P4-M3.14 is not transition intake validation",
    "P4-M3.14 is not package validation",
    "P4-M3.14 is not final audit validation",
    "P4-M3.14 is not closure validation",
    "P4-M3.14 is not handoff validation",
    "P4-M3.14 is not closure execution",
    "P4-M3.14 is not handoff execution",
    "P4-M3.14 is not package correctness validation",
    "P4-M3.14 is not package completeness validation",
    "P4-M3.14 is not package consistency validation",
    "P4-M3.14 is not package integrity validation",
    "P4-M3.14 is not package readiness validation",
    "P4-M3.14 is not package readiness verdict",
    "P4-M3.14 is not package validation verdict",
    "P4-M3.14 is not reference resolution",
    "P4-M3.14 is not reference integrity validation",
    "P4-M3.14 is not reference completeness validation",
    "P4-M3.14 is not transition safeguard validation",
    "P4-M3.14 is not transition assumption validation",
    "P4-M3.14 is not transition risk validation",
    "P4-M3.14 is not transition impact validation",
    "P4-M3.14 is not transition dependency validation",
    "P4-M3.14 is not transition constraint validation",
    "P4-M3.14 is not transition reason validation",
    "P4-M3.14 is not target phase validation",
    "P4-M3.14 is not target phase selection",
    "P4-M3.14 is not transition readiness validation",
    "P4-M3.14 is not readiness verdict",
    "P4-M3.14 is not validation verdict",
    "P4-M3.14 is not closure verdict",
    "P4-M3.14 is not handoff verdict",
    "P4-M3.14 is not boundary certification",
    "P4-M3.14 is not approval",
    "P4-M3.14 is not authorization",
    "P4-M3.14 is not confirmation",
    "P4-M3.14 is not recommendation",
    "P4-M3.14 is not ranking",
    "P4-M3.14 is not next action generation",
    "P4-M3.14 is not transition execution",
    "P4-M3.14 is not request validation",
    "P4-M3.14 is not evidence validation",
    "P4-M3.14 is not human context validation",
    "P4-M3.14 is not source validation",
    "P4-M3.14 is not citation validation",
    "P4-M3.14 is not transition record creation",
    "P4-M3.14 is not request record creation",
    "P4-M3.14 is not package record creation",
    "P4-M3.14 is not closure record creation",
    "P4-M3.14 is not handoff record creation",
    "P4-M3.14 is not memory mutation",
    "P4-M3.14 is not roadmap mutation",
    "P4-M3.14 is not lifecycle mutation",
    "P4-M3.14 is not proposal mutation",
    "P4-M3.14 is not evidence mutation",
    "P4-M3.14 is not human context mutation",
    "P4-M3.14 is not target phase mutation",
    "P4-M3.14 is not transition reason mutation",
    "P4-M3.14 is not transition constraint mutation",
    "P4-M3.14 is not transition dependency mutation",
    "P4-M3.14 is not transition impact mutation",
    "P4-M3.14 is not transition risk mutation",
    "P4-M3.14 is not transition assumption mutation",
    "P4-M3.14 is not transition safeguard mutation",
    "P4-M3.14 is not package mutation",
    "P4-M3.14 is not closure mutation",
    "P4-M3.14 is not handoff mutation",
    "P4-M3.14 is not source fetching",
    "P4-M3.14 is not provenance writing",
    "P4-M3.14 is not citation mutation",
    "P4-M4 remains not started",
    "P4-M5 remains not started",
    "v7 remains not started",
    "productization remains not started",
    "UI remains not started",
    "Operator Console remains not started",
    "no live validation",
    "no transition intake validation",
    "no package validation",
    "no final audit validation",
    "no closure validation",
    "no handoff validation",
    "no closure execution",
    "no handoff execution",
    "no package correctness validation",
    "no package completeness validation",
    "no package consistency validation",
    "no package integrity validation",
    "no package readiness validation",
    "no package readiness verdict",
    "no package validation verdict",
    "no reference resolution",
    "no reference integrity validation",
    "no reference completeness validation",
    "no transition safeguard validation",
    "no transition assumption validation",
    "no transition risk validation",
    "no transition impact validation",
    "no transition dependency validation",
    "no transition constraint validation",
    "no transition reason validation",
    "no target phase validation",
    "no target phase selection",
    "no readiness validation",
    "no readiness verdict",
    "no validation verdict",
    "no closure verdict",
    "no handoff verdict",
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
    "no source validation",
    "no citation validation",
    "no memory mutation",
    "no roadmap mutation",
    "no closure record creation",
    "no handoff record creation",
    "no closure mutation",
    "no handoff mutation",
    "no source fetching",
    "no provenance writing",
    "no citation mutation",
    "no P4-M4",
    "no P4-M5",
    "no v7",
    "no productization",
    "no UI",
    "no Operator Console",
    "no MVP",
    "no deploy",
    "no full Memory Graph",
    "no version bump",
    "no tag",
)

TRUE_STATUS_FLAGS = (
    "definition_only",
    "inspection_only",
    "p4_m3_closure_handoff_contract_definition_started",
    "p4_m3_14_governed_transition_intake_closure_handoff_contract_started",
    "p4_m3_14_definition_only",
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
    "p4_m2_17_closure_handoff_contract_reference_defined",
    "p4_m3_closure_handoff_contract_defined",
    "p4_m3_closure_handoff_scope_defined",
    "p4_m3_closure_handoff_field_shape_defined",
    "p4_m3_governed_transition_intake_static_definition_chain_closed_for_handoff",
    "p4_m3_live_validation_semantics_prohibited",
    "p4_m3_transition_intake_validation_semantics_prohibited",
    "p4_m3_transition_intake_package_validation_semantics_prohibited",
    "p4_m3_final_audit_validation_semantics_prohibited",
    "p4_m3_closure_validation_semantics_prohibited",
    "p4_m3_handoff_validation_semantics_prohibited",
    "p4_m3_closure_execution_semantics_prohibited",
    "p4_m3_handoff_execution_semantics_prohibited",
    "p4_m3_package_correctness_validation_semantics_prohibited",
    "p4_m3_package_completeness_validation_semantics_prohibited",
    "p4_m3_package_consistency_validation_semantics_prohibited",
    "p4_m3_package_integrity_validation_semantics_prohibited",
    "p4_m3_package_readiness_validation_semantics_prohibited",
    "p4_m3_package_readiness_verdict_semantics_prohibited",
    "p4_m3_package_validation_verdict_semantics_prohibited",
    "p4_m3_reference_resolution_semantics_prohibited",
    "p4_m3_reference_integrity_validation_semantics_prohibited",
    "p4_m3_reference_completeness_validation_semantics_prohibited",
    "p4_m3_boundary_certification_semantics_prohibited",
    "p4_m3_transition_safeguard_validation_semantics_prohibited",
    "p4_m3_transition_assumption_validation_semantics_prohibited",
    "p4_m3_transition_risk_validation_semantics_prohibited",
    "p4_m3_transition_impact_validation_semantics_prohibited",
    "p4_m3_transition_dependency_validation_semantics_prohibited",
    "p4_m3_transition_constraint_validation_semantics_prohibited",
    "p4_m3_transition_reason_validation_semantics_prohibited",
    "p4_m3_target_phase_validation_semantics_prohibited",
    "p4_m3_target_phase_selection_semantics_prohibited",
    "p4_m3_transition_readiness_validation_semantics_prohibited",
    "p4_m3_transition_readiness_verdict_semantics_prohibited",
    "p4_m3_transition_validation_verdict_semantics_prohibited",
    "p4_m3_closure_verdict_semantics_prohibited",
    "p4_m3_handoff_verdict_semantics_prohibited",
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
    "p4_m4_start_deferred",
)

FALSE_STATUS_FLAGS = (
    "live_validation_enabled",
    "boundary_validation_enabled",
    "transition_intake_validation_enabled",
    "transition_intake_package_validation_enabled",
    "final_audit_validation_enabled",
    "closure_validation_enabled",
    "handoff_validation_enabled",
    "closure_execution_enabled",
    "handoff_execution_enabled",
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
    "transition_intake_package_record_creation_enabled",
    "transition_intake_package_record_update_enabled",
    "transition_intake_package_record_deletion_enabled",
    "closure_record_creation_enabled",
    "closure_record_update_enabled",
    "closure_record_deletion_enabled",
    "handoff_record_creation_enabled",
    "handoff_record_update_enabled",
    "handoff_record_deletion_enabled",
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

GOVERNED_TRANSITION_INTAKE_CLOSURE_HANDOFF_CONTRACT_BOUNDARY = (
    "P4-M3.14 Governed Transition Intake Closure Handoff Contract "
    "read-only definition-only inspection-only. P4-M3.14 closure handoff "
    "contract definition only. "
    + " ".join(f"{phrase}." for phrase in BOUNDARY_PHRASE_LINES)
)

_FIELD_IDS = (
    "p4-m3-governed-transition-intake-closure-handoff-contract-id",
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
    "p4-m2-closure-handoff-contract-reference",
    "p4-m3-governed-transition-intake-closure-handoff-scope",
    "p4-m3-governed-transition-intake-closure-handoff-semantics-disabled",
)

_FIELD_NAMES = (
    "P4-M3 Governed Transition Intake Closure Handoff Contract Id",
    "P4-M3 Governed Transition Intake Final Non Validation Boundary Audit Reference",
    "P4-M3 Governed Transition Intake Package Assembly Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Declared Transition Safeguard Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Declared Transition Assumption Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Declared Transition Risk Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Declared Transition Impact Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Declared Transition Dependency Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Declared Transition Constraint Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Declared Transition Reason Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Target Phase Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Declared Human Context Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Evidence Reference Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Request Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Boundary Contract Reference",
    "P4-M2 Closure Handoff Contract Reference",
    "P4-M3 Governed Transition Intake Closure Handoff Scope",
    "P4-M3 Governed Transition Intake Closure Handoff Semantics Disabled",
)


def _field_purpose(field_id: str) -> str:
    return (
        f"Defines {field_id} as read-only definition-only inspection-only "
        "P4-M3.14 closure handoff contract definition only context; "
        "P4-M3.13 Governed Transition Intake Final Non-Validation Boundary "
        "Audit remains the source final non-validation boundary audit; "
        "P4-M2.17 P4-M2 Closure Handoff Contract remains the prior closure "
        "handoff reference; no live validation; no transition intake "
        "validation; no package validation; no final audit validation; no "
        "closure validation; no handoff validation; no closure execution; no "
        "handoff execution; no package correctness validation; no package "
        "completeness validation; no package consistency validation; no package "
        "integrity validation; no package readiness validation; no package "
        "readiness verdict; no package validation verdict; no reference "
        "resolution; no reference integrity validation; no reference "
        "completeness validation; no transition safeguard validation; no "
        "transition assumption validation; no transition risk validation; no "
        "transition impact validation; no transition dependency validation; no "
        "transition constraint validation; no transition reason validation; no "
        "target phase validation; no target phase selection; no readiness "
        "validation; no readiness verdict; no validation verdict; no closure "
        "verdict; no handoff verdict; no boundary certification; no approval; "
        "no authorization; no confirmation; no recommendation; no ranking; no "
        "next action generation; no transition execution; no request "
        "validation; no evidence validation; no memory mutation; no roadmap "
        "mutation; no closure record creation; no handoff record creation; no "
        "closure mutation; no handoff mutation; no P4-M4; no P4-M5; no v7; no "
        "productization; no UI; no Operator Console; no version bump; no tag."
    )


_GOVERNED_TRANSITION_INTAKE_CLOSURE_HANDOFF_CONTRACT_FIELDS = tuple(
    GovernedTransitionIntakeClosureHandoffContractField(
        index,
        field_id,
        _FIELD_NAMES[index - 1],
        _field_purpose(field_id),
        "p4-m3-governed-transition-intake-closure-handoff-contract-category",
        (
            "no live validation semantics; no transition intake validation "
            "semantics; no package validation semantics; no final audit "
            "validation semantics; no closure validation semantics; no handoff "
            "validation semantics; no closure execution semantics; no handoff "
            "execution semantics; no reference resolution semantics; no verdict "
            "semantics; no boundary certification semantics; no approval "
            "semantics; no authorization semantics; no confirmation semantics; "
            "no recommendation semantics; no ranking semantics; no next-action "
            "semantics; no transition execution semantics; no record creation "
            "semantics; no mutation semantics; no source fetching semantics; no "
            "provenance writing semantics; no citation mutation semantics"
        ),
    )
    for index, field_id in enumerate(_FIELD_IDS, start=1)
)


def list_governed_transition_intake_closure_handoff_contract_fields() -> tuple[GovernedTransitionIntakeClosureHandoffContractField, ...]:
    return _GOVERNED_TRANSITION_INTAKE_CLOSURE_HANDOFF_CONTRACT_FIELDS


def governed_transition_intake_closure_handoff_contract_field_ids() -> tuple[str, ...]:
    return tuple(
        field.field_id
        for field in list_governed_transition_intake_closure_handoff_contract_fields()
    )


def render_governed_transition_intake_closure_handoff_contract_markdown(
    fields: Sequence[GovernedTransitionIntakeClosureHandoffContractField] | None = None,
) -> str:
    field_values = tuple(fields) if fields is not None else list_governed_transition_intake_closure_handoff_contract_fields()
    status = governed_transition_intake_closure_handoff_contract_report()
    lines = [
        "# P4-M3.14 Governed Transition Intake Closure Handoff Contract",
        "",
        "P4-M3.14 Governed Transition Intake Closure Handoff Contract.",
        "",
        "read-only.",
        "",
        "definition-only.",
        "",
        "inspection-only.",
        "",
        "P4-M3.14 closure handoff contract definition only.",
        "",
        "P4-M3.13 Governed Transition Intake Final Non-Validation Boundary Audit remains the source final non-validation boundary audit.",
        "",
        "P4-M3.12 Governed Transition Intake Package Assembly Envelope Contract remains the source package assembly envelope boundary.",
        "",
        "P4-M3.11 Governed Transition Intake Declared Transition Safeguard Envelope Contract remains the source declared transition safeguard envelope boundary.",
        "",
        "P4-M3.10 Governed Transition Intake Declared Transition Assumption Envelope Contract remains the source declared transition assumption envelope boundary.",
        "",
        "P4-M3.9 Governed Transition Intake Declared Transition Risk Envelope Contract remains the source declared transition risk envelope boundary.",
        "",
        "P4-M3.8 Governed Transition Intake Declared Transition Impact Envelope Contract remains the source declared transition impact envelope boundary.",
        "",
        "P4-M3.7 Governed Transition Intake Declared Transition Dependency Envelope Contract remains the source declared transition dependency envelope boundary.",
        "",
        "P4-M3.6 Governed Transition Intake Declared Transition Constraint Envelope Contract remains the source declared transition constraint envelope boundary.",
        "",
        "P4-M3.5 Governed Transition Intake Declared Transition Reason Envelope Contract remains the source declared transition reason envelope boundary.",
        "",
        "P4-M3.4 Governed Transition Intake Target Phase Envelope Contract remains the source target phase envelope boundary.",
        "",
        "P4-M3.3 Governed Transition Intake Declared Human Context Envelope Contract remains the source declared human context envelope boundary.",
        "",
        "P4-M3.2 Governed Transition Intake Evidence Reference Envelope Contract remains the source evidence reference envelope boundary.",
        "",
        "P4-M3.1 Governed Transition Intake Request Envelope Contract remains the source request envelope boundary.",
        "",
        "P4-M3.0 Governed Transition Intake Boundary Contract remains the source intake boundary.",
        "",
        "P4-M2.17 P4-M2 Closure Handoff Contract remains the prior closure handoff reference.",
        "",
    ]
    for prior_layer in PRIOR_DEFINITION_LAYER_REFERENCES:
        lines.extend([f"{prior_layer} remains a referenced definition layer.", ""])
    for phrase in BOUNDARY_PHRASE_LINES:
        lines.extend([f"{phrase}.", ""])
    lines.extend([
        GOVERNED_TRANSITION_INTAKE_CLOSURE_HANDOFF_CONTRACT_BOUNDARY,
        "",
        "## Status Report",
        "",
    ])
    for key, value in status.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Governed Transition Intake Closure Handoff Contract Fields", ""])
    for field in field_values:
        lines.extend([
            f"### {field.field_order}. {field.field_id}",
            "",
            f"- Field name: {field.field_name}",
            f"- Field purpose: {field.field_purpose}",
            "- P4-M3 closure handoff contract category: "
            f"{field.p4_m3_closure_handoff_contract_category}",
            "- P4-M3 closure handoff semantics disabled: "
            f"{field.p4_m3_closure_handoff_semantics_disabled}",
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def governed_transition_intake_closure_handoff_contract_as_dicts() -> tuple[dict[str, object], ...]:
    return tuple(
        asdict(field)
        for field in list_governed_transition_intake_closure_handoff_contract_fields()
    )


def governed_transition_intake_closure_handoff_contract_report() -> dict[str, object]:
    status: dict[str, object] = {
        "phase": "P4-M3.14",
        "feature": "Governed Transition Intake Closure Handoff Contract",
        "mode": "read-only",
        "boundary": GOVERNED_TRANSITION_INTAKE_CLOSURE_HANDOFF_CONTRACT_BOUNDARY,
        "package_version": P4_M3_14_PACKAGE_VERSION,
        "governed_transition_intake_closure_handoff_contract_field_count": len(
            _FIELD_IDS
        ),
        "referenced_p4_m3_13_final_non_validation_boundary_audit_field_count": len(
            governed_transition_intake_final_non_validation_boundary_audit_field_ids()
        ),
        "referenced_p4_m3_12_package_assembly_envelope_contract_field_count": len(
            governed_transition_intake_package_assembly_envelope_contract_field_ids()
        ),
        "referenced_p4_m3_11_declared_transition_safeguard_envelope_contract_field_count": len(
            governed_transition_intake_declared_transition_safeguard_envelope_contract_field_ids()
        ),
        "referenced_p4_m3_10_declared_transition_assumption_envelope_contract_field_count": len(
            governed_transition_intake_declared_transition_assumption_envelope_contract_field_ids()
        ),
        "referenced_p4_m3_9_declared_transition_risk_envelope_contract_field_count": len(
            governed_transition_intake_declared_transition_risk_envelope_contract_field_ids()
        ),
        "referenced_p4_m3_8_declared_transition_impact_envelope_contract_field_count": len(
            governed_transition_intake_declared_transition_impact_envelope_contract_field_ids()
        ),
        "referenced_p4_m3_7_declared_transition_dependency_envelope_contract_field_count": len(
            governed_transition_intake_declared_transition_dependency_envelope_contract_field_ids()
        ),
        "referenced_p4_m3_6_declared_transition_constraint_envelope_contract_field_count": len(
            governed_transition_intake_declared_transition_constraint_envelope_contract_field_ids()
        ),
        "referenced_p4_m3_5_declared_transition_reason_envelope_contract_field_count": len(
            governed_transition_intake_declared_transition_reason_envelope_contract_field_ids()
        ),
        "referenced_p4_m3_4_target_phase_envelope_contract_field_count": len(
            governed_transition_intake_target_phase_envelope_contract_field_ids()
        ),
        "referenced_p4_m3_3_declared_human_context_envelope_contract_field_count": len(
            governed_transition_intake_declared_human_context_envelope_contract_field_ids()
        ),
        "referenced_p4_m3_2_evidence_reference_envelope_contract_field_count": len(
            governed_transition_intake_evidence_reference_envelope_contract_field_ids()
        ),
        "referenced_p4_m3_1_request_envelope_contract_field_count": len(
            governed_transition_intake_request_envelope_contract_field_ids()
        ),
        "referenced_p4_m3_0_intake_boundary_contract_field_count": len(
            governed_transition_intake_boundary_contract_field_ids()
        ),
        "referenced_p4_m2_17_closure_handoff_contract_field_count": len(
            closure_handoff_contract_field_ids()
        ),
    }
    status.update({flag: True for flag in TRUE_STATUS_FLAGS})
    status.update({flag: False for flag in FALSE_STATUS_FLAGS})
    return status
