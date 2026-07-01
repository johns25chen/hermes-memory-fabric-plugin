from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence

from .p4_m2_closure_handoff_contract import closure_handoff_contract_field_ids
from .p4_m2_final_non_execution_boundary_audit import final_non_execution_boundary_audit_field_ids
from .p4_m3_governed_transition_intake_boundary_contract import governed_transition_intake_boundary_contract_field_ids
from .p4_m3_governed_transition_intake_declared_human_context_envelope_contract import governed_transition_intake_declared_human_context_envelope_contract_field_ids
from .p4_m3_governed_transition_intake_declared_transition_constraint_envelope_contract import governed_transition_intake_declared_transition_constraint_envelope_contract_field_ids
from .p4_m3_governed_transition_intake_declared_transition_dependency_envelope_contract import governed_transition_intake_declared_transition_dependency_envelope_contract_field_ids
from .p4_m3_governed_transition_intake_declared_transition_reason_envelope_contract import governed_transition_intake_declared_transition_reason_envelope_contract_field_ids
from .p4_m3_governed_transition_intake_evidence_reference_envelope_contract import governed_transition_intake_evidence_reference_envelope_contract_field_ids
from .p4_m3_governed_transition_intake_request_envelope_contract import governed_transition_intake_request_envelope_contract_field_ids
from .p4_m3_governed_transition_intake_target_phase_envelope_contract import governed_transition_intake_target_phase_envelope_contract_field_ids


P4_M3_8_PACKAGE_VERSION = "6.16.0"


@dataclass(frozen=True)
class GovernedTransitionIntakeDeclaredTransitionImpactEnvelopeContractField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    p4_m3_declared_transition_impact_envelope_contract_category: str
    p4_m3_declared_transition_impact_envelope_semantics_disabled: str


PRIOR_DEFINITION_LAYER_REFERENCES = (
    "P4-M3.7 Governed Transition Intake Declared Transition Dependency Envelope Contract",
    "P4-M3.6 Governed Transition Intake Declared Transition Constraint Envelope Contract",
    "P4-M3.5 Governed Transition Intake Declared Transition Reason Envelope Contract",
    "P4-M3.4 Governed Transition Intake Target Phase Envelope Contract",
    "P4-M3.3 Governed Transition Intake Declared Human Context Envelope Contract",
    "P4-M3.2 Governed Transition Intake Evidence Reference Envelope Contract",
    "P4-M3.1 Governed Transition Intake Request Envelope Contract",
    "P4-M3.0 Governed Transition Intake Boundary Contract",
    "P4-M2.17 P4-M2 Closure Handoff Contract",
    "P4-M2.16 Final Non-Execution Boundary Audit",
)

BOUNDARY_PHRASE_LINES = (
    "P4-M3.8",
    "Governed Transition Intake Declared Transition Impact Envelope Contract",
    "read-only",
    "definition-only",
    "inspection-only",
    "P4-M3.8 declared transition impact envelope definition only",
    "P4-M3.7 Governed Transition Intake Declared Transition Dependency Envelope Contract remains the source declared transition dependency envelope boundary",
    "P4-M3.6 Governed Transition Intake Declared Transition Constraint Envelope Contract remains the source declared transition constraint envelope boundary",
    "P4-M3.5 Governed Transition Intake Declared Transition Reason Envelope Contract remains the source declared transition reason envelope boundary",
    "P4-M3.4 Governed Transition Intake Target Phase Envelope Contract remains the source target phase envelope boundary",
    "P4-M3.3 Governed Transition Intake Declared Human Context Envelope Contract remains the source declared human context envelope boundary",
    "P4-M3.2 Governed Transition Intake Evidence Reference Envelope Contract remains the source evidence reference envelope boundary",
    "P4-M3.1 Governed Transition Intake Request Envelope Contract remains the source request envelope boundary",
    "P4-M3.0 Governed Transition Intake Boundary Contract remains the source intake boundary",
    "P4-M3.8 is not transition impact validation",
    "P4-M3.8 is not impact correctness validation",
    "P4-M3.8 is not impact assessment",
    "P4-M3.8 is not impact severity assessment",
    "P4-M3.8 is not impact scoring",
    "P4-M3.8 is not impact ranking",
    "P4-M3.8 is not affected-surface validation",
    "P4-M3.8 is not affected-surface selection",
    "P4-M3.8 is not transition dependency validation",
    "P4-M3.8 is not dependency correctness validation",
    "P4-M3.8 is not dependency satisfaction validation",
    "P4-M3.8 is not prerequisite validation",
    "P4-M3.8 is not transition constraint validation",
    "P4-M3.8 is not transition reason validation",
    "P4-M3.8 is not target phase validation",
    "P4-M3.8 is not target phase selection",
    "P4-M3.8 is not transition readiness validation",
    "P4-M3.8 is not readiness verdict",
    "P4-M3.8 is not validation verdict",
    "P4-M3.8 is not approval",
    "P4-M3.8 is not authorization",
    "P4-M3.8 is not confirmation",
    "P4-M3.8 is not recommendation",
    "P4-M3.8 is not ranking",
    "P4-M3.8 is not next action generation",
    "P4-M3.8 is not transition execution",
    "P4-M3.8 is not request validation",
    "P4-M3.8 is not evidence validation",
    "P4-M3.8 is not human context validation",
    "P4-M3.8 is not source validation",
    "P4-M3.8 is not citation validation",
    "P4-M3.8 is not transition record creation",
    "P4-M3.8 is not request record creation",
    "P4-M3.8 is not target-phase record creation",
    "P4-M3.8 is not transition-reason record creation",
    "P4-M3.8 is not transition-constraint record creation",
    "P4-M3.8 is not transition-dependency record creation",
    "P4-M3.8 is not transition-impact record creation",
    "P4-M3.8 is not memory mutation",
    "P4-M3.8 is not roadmap mutation",
    "P4-M3.8 is not lifecycle mutation",
    "P4-M3.8 is not proposal mutation",
    "P4-M3.8 is not evidence mutation",
    "P4-M3.8 is not human context mutation",
    "P4-M3.8 is not target phase mutation",
    "P4-M3.8 is not transition reason mutation",
    "P4-M3.8 is not transition constraint mutation",
    "P4-M3.8 is not transition dependency mutation",
    "P4-M3.8 is not transition impact mutation",
    "P4-M3.8 is not source fetching",
    "P4-M3.8 is not provenance writing",
    "P4-M3.8 is not citation mutation",
    "no transition impact validation",
    "no impact correctness validation",
    "no impact assessment",
    "no impact severity assessment",
    "no impact scoring",
    "no impact ranking",
    "no impact precedence",
    "no impact arbitration",
    "no impact winner selection",
    "no declared impact acceptance",
    "no declared impact rejection",
    "no affected-surface validation",
    "no affected-surface selection",
    "no affected-surface scoring",
    "no affected-surface ranking",
    "no transition impact persistence",
    "no transition impact storage",
    "no transition impact mutation",
    "no transition-impact record creation",
    "no transition-impact record update",
    "no transition-impact record deletion",
    "no transition dependency validation",
    "no dependency correctness validation",
    "no dependency satisfaction validation",
    "no prerequisite validation",
    "no dependency scoring",
    "no dependency ranking",
    "no transition dependency mutation",
    "no transition-dependency record creation",
    "no transition constraint validation",
    "no constraint correctness validation",
    "no constraint feasibility validation",
    "no transition reason validation",
    "no reason correctness validation",
    "no target phase validation",
    "no target phase selection",
    "no phase eligibility validation",
    "no phase compatibility validation",
    "no readiness validation",
    "no transition readiness validation",
    "no readiness verdict",
    "no validation verdict",
    "no approval",
    "no authorization",
    "no confirmation",
    "no recommendation",
    "no ranking",
    "no suggested next action",
    "no next action generation",
    "no transition execution",
    "no transition authorization",
    "no transition approval",
    "no transition confirmation",
    "no transition recommendation",
    "no transition ranking",
    "no transition record creation",
    "no target-phase record creation",
    "no transition-reason record creation",
    "no transition-constraint record creation",
    "no transition-dependency record creation",
    "no request validation",
    "no request acceptance",
    "no request rejection",
    "no request persistence",
    "no request storage",
    "no request mutation",
    "no request record creation",
    "no evidence validation",
    "no evidence scoring",
    "no evidence ranking",
    "no evidence precedence",
    "no evidence arbitration",
    "no evidence winner selection",
    "no human context validation",
    "no human confirmation",
    "no human approval",
    "no human authorization",
    "no consent validation",
    "no identity verification",
    "no source validation",
    "no citation validation",
    "no source fetching",
    "no provenance writing",
    "no citation mutation",
    "no memory mutation",
    "no memory record creation",
    "no memory record update",
    "no memory record deletion",
    "no roadmap mutation",
    "no lifecycle mutation",
    "no proposal mutation",
    "no evidence mutation",
    "no human context mutation",
    "no target phase mutation",
    "no transition reason mutation",
    "no transition constraint mutation",
    "no transition dependency mutation",
    "no transition impact semantics",
    "no impact correctness semantics",
    "no impact assessment semantics",
    "no impact severity semantics",
    "no affected-surface semantics",
    "no affected-surface selection semantics",
    "no dependency semantics",
    "no transition constraint semantics",
    "no transition reason semantics",
    "no target phase semantics",
    "no target selection semantics",
    "no route selection semantics",
    "no phase eligibility semantics",
    "no phase compatibility semantics",
    "no transition execution semantics",
    "no transition readiness semantics",
    "no transition validation semantics",
    "no validation semantics",
    "no readiness semantics",
    "no approval semantics",
    "no authorization semantics",
    "no confirmation semantics",
    "no recommendation semantics",
    "no ranking semantics",
    "no next-action semantics",
    "no mutation semantics",
    "no API",
    "no MCP",
    "no connector",
    "no agent call",
    "no Codex/Hermes/ChatGPT product-code auto-call",
    "no P4-M3.9",
    "no P4-M3.9 command",
    "no P4-M3.9 activation",
    "no P4-M3.9 implementation",
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
    "p4_m3_declared_transition_impact_envelope_definition_started",
    "p4_m3_8_governed_transition_intake_declared_transition_impact_envelope_contract_started",
    "p4_m3_8_definition_only",
    "p4_m3_7_declared_transition_dependency_envelope_contract_reference_defined",
    "p4_m3_6_declared_transition_constraint_envelope_contract_reference_defined",
    "p4_m3_5_declared_transition_reason_envelope_contract_reference_defined",
    "p4_m3_4_target_phase_envelope_contract_reference_defined",
    "p4_m3_3_declared_human_context_envelope_contract_reference_defined",
    "p4_m3_2_evidence_reference_envelope_contract_reference_defined",
    "p4_m3_1_request_envelope_contract_reference_defined",
    "p4_m3_0_intake_boundary_contract_reference_defined",
    "p4_m2_17_closure_handoff_contract_reference_defined",
    "p4_m2_final_non_execution_boundary_reference_defined",
    "p4_m3_declared_transition_impact_envelope_contract_defined",
    "p4_m3_declared_transition_impact_envelope_scope_defined",
    "p4_m3_declared_transition_impact_envelope_field_shape_defined",
    "p4_m3_transition_impact_validation_semantics_prohibited",
    "p4_m3_impact_correctness_validation_semantics_prohibited",
    "p4_m3_impact_assessment_semantics_prohibited",
    "p4_m3_impact_severity_assessment_semantics_prohibited",
    "p4_m3_impact_scoring_semantics_prohibited",
    "p4_m3_impact_ranking_semantics_prohibited",
    "p4_m3_affected_surface_validation_semantics_prohibited",
    "p4_m3_affected_surface_selection_semantics_prohibited",
    "p4_m3_transition_impact_record_semantics_prohibited",
    "p4_m3_transition_impact_mutation_semantics_prohibited",
    "p4_m3_transition_dependency_validation_semantics_prohibited",
    "p4_m3_dependency_correctness_validation_semantics_prohibited",
    "p4_m3_dependency_satisfaction_validation_semantics_prohibited",
    "p4_m3_prerequisite_validation_semantics_prohibited",
    "p4_m3_transition_constraint_validation_semantics_prohibited",
    "p4_m3_transition_reason_validation_semantics_prohibited",
    "p4_m3_target_phase_validation_semantics_prohibited",
    "p4_m3_target_phase_selection_semantics_prohibited",
    "p4_m3_transition_readiness_validation_semantics_prohibited",
    "p4_m3_transition_readiness_verdict_semantics_prohibited",
    "p4_m3_transition_validation_verdict_semantics_prohibited",
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
    "p4_m3_9_start_deferred",
)

FALSE_STATUS_FLAGS = (
    "transition_impact_validation_enabled",
    "impact_correctness_validation_enabled",
    "impact_assessment_enabled",
    "impact_severity_assessment_enabled",
    "impact_scoring_enabled",
    "impact_ranking_enabled",
    "impact_precedence_enabled",
    "impact_arbitration_enabled",
    "impact_winner_selection_enabled",
    "declared_impact_acceptance_enabled",
    "declared_impact_rejection_enabled",
    "affected_surface_validation_enabled",
    "affected_surface_selection_enabled",
    "affected_surface_scoring_enabled",
    "affected_surface_ranking_enabled",
    "transition_impact_persistence_enabled",
    "transition_impact_storage_enabled",
    "transition_impact_mutation_enabled",
    "transition_impact_record_creation_enabled",
    "transition_impact_record_update_enabled",
    "transition_impact_record_deletion_enabled",
    "transition_dependency_validation_enabled",
    "dependency_correctness_validation_enabled",
    "dependency_satisfaction_validation_enabled",
    "prerequisite_validation_enabled",
    "transition_dependency_scoring_enabled",
    "transition_dependency_ranking_enabled",
    "transition_dependency_precedence_enabled",
    "transition_dependency_arbitration_enabled",
    "transition_dependency_winner_selection_enabled",
    "declared_dependency_acceptance_enabled",
    "declared_dependency_rejection_enabled",
    "transition_dependency_persistence_enabled",
    "transition_dependency_storage_enabled",
    "transition_dependency_mutation_enabled",
    "transition_dependency_record_creation_enabled",
    "transition_dependency_record_update_enabled",
    "transition_dependency_record_deletion_enabled",
    "transition_constraint_validation_enabled",
    "constraint_correctness_validation_enabled",
    "constraint_feasibility_validation_enabled",
    "feasibility_validation_enabled",
    "transition_reason_validation_enabled",
    "reason_correctness_validation_enabled",
    "justification_validation_enabled",
    "rationale_validation_enabled",
    "target_phase_validation_enabled",
    "target_phase_selection_enabled",
    "phase_eligibility_validation_enabled",
    "phase_compatibility_validation_enabled",
    "phase_transition_execution_enabled",
    "phase_transition_authorization_enabled",
    "target_selection_enabled",
    "route_selection_enabled",
    "lifecycle_transition_enabled",
    "roadmap_transition_enabled",
    "transition_readiness_validation_enabled",
    "live_transition_readiness_validation_enabled",
    "readiness_verdict_enabled",
    "transition_readiness_verdict_enabled",
    "validation_verdict_enabled",
    "transition_validation_verdict_enabled",
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
    "request_record_creation_enabled",
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
    "p4_m3_9_started",
    "p4_m3_9_command_enabled",
    "p4_m3_9_activation_enabled",
    "p4_m3_9_implementation_enabled",
    "p4_m4_started",
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

GOVERNED_TRANSITION_INTAKE_DECLARED_TRANSITION_IMPACT_ENVELOPE_CONTRACT_BOUNDARY = (
    "P4-M3.8 Governed Transition Intake Declared Transition Impact Envelope "
    "Contract read-only definition-only inspection-only. P4-M3.8 declared "
    "transition impact envelope definition only. "
    + " ".join(f"{phrase}." for phrase in BOUNDARY_PHRASE_LINES)
)

_FIELD_IDS = (
    "p4-m3-governed-transition-intake-declared-transition-impact-envelope-contract-id",
    "p4-m3-governed-transition-intake-declared-transition-dependency-envelope-contract-reference",
    "p4-m3-governed-transition-intake-declared-transition-constraint-envelope-contract-reference",
    "p4-m3-governed-transition-intake-declared-transition-reason-envelope-contract-reference",
    "p4-m3-governed-transition-intake-target-phase-envelope-contract-reference",
    "p4-m3-governed-transition-intake-declared-human-context-envelope-contract-reference",
    "p4-m3-governed-transition-intake-evidence-reference-envelope-contract-reference",
    "p4-m3-governed-transition-intake-request-envelope-contract-reference",
    "p4-m3-governed-transition-intake-boundary-contract-reference",
    "p4-m2-closure-handoff-contract-reference",
    "p4-m2-final-non-execution-boundary-audit-reference",
    "p4-m3-declared-transition-impact-envelope-source-reference",
    "p4-m3-declared-transition-impact-envelope-scope",
    "p4-m3-declared-transition-impact-envelope-request-reference-field",
    "p4-m3-declared-transition-impact-envelope-target-phase-reference-field",
    "p4-m3-declared-transition-impact-envelope-dependency-reference-field",
    "p4-m3-declared-transition-impact-envelope-affected-surface-reference-field",
    "p4-m3-declared-transition-impact-envelope-semantics-disabled",
)

_FIELD_NAMES = (
    "P4-M3 Governed Transition Intake Declared Transition Impact Envelope Contract Id",
    "P4-M3 Governed Transition Intake Declared Transition Dependency Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Declared Transition Constraint Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Declared Transition Reason Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Target Phase Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Declared Human Context Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Evidence Reference Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Request Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Boundary Contract Reference",
    "P4-M2 Closure Handoff Contract Reference",
    "P4-M2 Final Non Execution Boundary Audit Reference",
    "P4-M3 Declared Transition Impact Envelope Source Reference",
    "P4-M3 Declared Transition Impact Envelope Scope",
    "P4-M3 Declared Transition Impact Envelope Request Reference Field",
    "P4-M3 Declared Transition Impact Envelope Target Phase Reference Field",
    "P4-M3 Declared Transition Impact Envelope Dependency Reference Field",
    "P4-M3 Declared Transition Impact Envelope Affected Surface Reference Field",
    "P4-M3 Declared Transition Impact Envelope Semantics Disabled",
)


def _field_purpose(field_id: str) -> str:
    return (
        f"Defines {field_id} as read-only definition-only inspection-only "
        "P4-M3.8 declared transition impact envelope definition only context; "
        "P4-M3.7 Governed Transition Intake Declared Transition Dependency "
        "Envelope Contract remains the source declared transition dependency "
        "envelope boundary; no transition impact validation; no impact "
        "correctness validation; no impact assessment; no impact severity "
        "assessment; no impact scoring; no impact ranking; no affected-surface "
        "validation; no affected-surface selection; no transition dependency "
        "validation; no transition constraint validation; no transition reason "
        "validation; no target phase validation; no transition readiness "
        "validation; no readiness verdict; no validation verdict; no approval; "
        "no authorization; no confirmation; no recommendation; no ranking; "
        "no next action generation; no transition execution; no record "
        "creation; no transition impact mutation; no memory mutation; no "
        "P4-M3.9; no P4-M4; no P4-M5; no v7; no productization; no UI; no "
        "Operator Console; no version bump; no tag."
    )


_GOVERNED_TRANSITION_INTAKE_DECLARED_TRANSITION_IMPACT_ENVELOPE_CONTRACT_FIELDS = tuple(
    GovernedTransitionIntakeDeclaredTransitionImpactEnvelopeContractField(
        index,
        field_id,
        _FIELD_NAMES[index - 1],
        _field_purpose(field_id),
        "p4-m3-declared-transition-impact-envelope-contract-category",
        (
            "no transition impact semantics; no impact correctness semantics; "
            "no impact assessment semantics; no impact severity semantics; "
            "no affected-surface semantics; no affected-surface selection "
            "semantics; no validation semantics; no mutation semantics"
        ),
    )
    for index, field_id in enumerate(_FIELD_IDS, start=1)
)


def list_governed_transition_intake_declared_transition_impact_envelope_contract_fields() -> tuple[GovernedTransitionIntakeDeclaredTransitionImpactEnvelopeContractField, ...]:
    return _GOVERNED_TRANSITION_INTAKE_DECLARED_TRANSITION_IMPACT_ENVELOPE_CONTRACT_FIELDS


def governed_transition_intake_declared_transition_impact_envelope_contract_field_ids() -> tuple[str, ...]:
    return tuple(
        field.field_id
        for field in list_governed_transition_intake_declared_transition_impact_envelope_contract_fields()
    )


def render_governed_transition_intake_declared_transition_impact_envelope_contract_markdown(
    fields: Sequence[GovernedTransitionIntakeDeclaredTransitionImpactEnvelopeContractField] | None = None,
) -> str:
    field_values = tuple(fields) if fields is not None else list_governed_transition_intake_declared_transition_impact_envelope_contract_fields()
    status = governed_transition_intake_declared_transition_impact_envelope_contract_report()
    lines = [
        "# P4-M3.8 Governed Transition Intake Declared Transition Impact Envelope Contract",
        "",
        "P4-M3.8 Governed Transition Intake Declared Transition Impact Envelope Contract.",
        "",
        "read-only.",
        "",
        "definition-only.",
        "",
        "inspection-only.",
        "",
        "P4-M3.8 declared transition impact envelope definition only.",
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
    ]
    for prior_layer in PRIOR_DEFINITION_LAYER_REFERENCES:
        lines.extend([f"{prior_layer} remains a referenced definition layer.", ""])
    for phrase in BOUNDARY_PHRASE_LINES:
        lines.extend([f"{phrase}.", ""])
    lines.extend([
        GOVERNED_TRANSITION_INTAKE_DECLARED_TRANSITION_IMPACT_ENVELOPE_CONTRACT_BOUNDARY,
        "",
        "## Status Report",
        "",
    ])
    for key, value in status.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Governed Transition Intake Declared Transition Impact Envelope Contract Fields", ""])
    for field in field_values:
        lines.extend([
            f"### {field.field_order}. {field.field_id}",
            "",
            f"- Field name: {field.field_name}",
            f"- Field purpose: {field.field_purpose}",
            "- P4-M3 declared transition impact envelope contract category: "
            f"{field.p4_m3_declared_transition_impact_envelope_contract_category}",
            "- P4-M3 declared transition impact envelope semantics disabled: "
            f"{field.p4_m3_declared_transition_impact_envelope_semantics_disabled}",
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def governed_transition_intake_declared_transition_impact_envelope_contract_as_dicts() -> tuple[dict[str, object], ...]:
    return tuple(
        asdict(field)
        for field in list_governed_transition_intake_declared_transition_impact_envelope_contract_fields()
    )


def governed_transition_intake_declared_transition_impact_envelope_contract_report() -> dict[str, object]:
    status: dict[str, object] = {
        "phase": "P4-M3.8",
        "feature": "Governed Transition Intake Declared Transition Impact Envelope Contract",
        "mode": "read-only",
        "package_version": P4_M3_8_PACKAGE_VERSION,
        "governed_transition_intake_declared_transition_impact_envelope_contract_field_count": 18,
        "prior_definition_layer_references": list(PRIOR_DEFINITION_LAYER_REFERENCES),
        "declared_transition_dependency_envelope_contract_field_ids": list(governed_transition_intake_declared_transition_dependency_envelope_contract_field_ids()),
        "declared_transition_constraint_envelope_contract_field_ids": list(governed_transition_intake_declared_transition_constraint_envelope_contract_field_ids()),
        "declared_transition_reason_envelope_contract_field_ids": list(governed_transition_intake_declared_transition_reason_envelope_contract_field_ids()),
        "target_phase_envelope_contract_field_ids": list(governed_transition_intake_target_phase_envelope_contract_field_ids()),
        "declared_human_context_envelope_contract_field_ids": list(governed_transition_intake_declared_human_context_envelope_contract_field_ids()),
        "evidence_reference_envelope_contract_field_ids": list(governed_transition_intake_evidence_reference_envelope_contract_field_ids()),
        "request_envelope_contract_field_ids": list(governed_transition_intake_request_envelope_contract_field_ids()),
        "intake_boundary_contract_field_ids": list(governed_transition_intake_boundary_contract_field_ids()),
        "closure_handoff_contract_field_ids": list(closure_handoff_contract_field_ids()),
        "final_non_execution_boundary_audit_field_ids": list(final_non_execution_boundary_audit_field_ids()),
        "boundary": GOVERNED_TRANSITION_INTAKE_DECLARED_TRANSITION_IMPACT_ENVELOPE_CONTRACT_BOUNDARY,
    }
    status.update({flag: True for flag in TRUE_STATUS_FLAGS})
    status.update({flag: False for flag in FALSE_STATUS_FLAGS})
    return status
