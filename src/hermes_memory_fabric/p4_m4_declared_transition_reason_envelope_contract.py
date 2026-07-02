from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence

from .p4_m4_target_phase_envelope_contract import (
    target_phase_envelope_contract_field_ids,
)


P4_M4_5_PACKAGE_VERSION = "6.16.0"


@dataclass(frozen=True)
class DeclaredTransitionReasonEnvelopeContractField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    p4_m4_declared_transition_reason_envelope_contract_category: str
    p4_m4_declared_transition_reason_envelope_contract_semantics_disabled: str


DIRECT_PRIOR_DEFINITION_LAYER_REFERENCES = (
    "P4-M4.4 Target Phase Envelope Contract",
)

INHERITED_PRIOR_DEFINITION_LAYER_REFERENCES = (
    "P4-M4.3 Declared Human Context Envelope Contract",
    "P4-M4.2 Evidence Reference Envelope Contract",
    "P4-M4.1 Entry Gate Design Request Envelope Contract",
    "P4-M4.0 Entry Gate Design Boundary Contract",
    "P4-M3.16 Governed Transition Intake Final Phase Handoff Summary",
)


BOUNDARY_PHRASE_LINES = (
    "P4-M4.5",
    "Declared Transition Reason Envelope Contract",
    "read-only",
    "definition-only",
    "declared-transition-reason-envelope-design-only",
    "declared-reason-surface-only",
    "reason-non-validation-boundary-only",
    "declaration-only",
    "inspection-only",
    "P4-M4.5 Declared Transition Reason Envelope Contract is definition only",
    "P4-M4.5 is declared-transition-reason-envelope-design-only",
    "P4-M4.5 is declared-reason-surface-only",
    "P4-M4.5 is reason-non-validation-boundary-only",
    "P4-M4.5 is declaration-only",
    "P4-M4.4 Target Phase Envelope Contract remains the direct prior target phase envelope reference",
    "P4-M4.4 target phase remains only an inherited static target phase projection reference",
    "P4-M4.3 Declared Human Context Envelope Contract remains the inherited prior declared human context envelope reference",
    "P4-M4.2 Evidence Reference Envelope Contract remains the inherited prior evidence reference envelope reference",
    "P4-M4.1 Entry Gate Design Request Envelope Contract remains the inherited prior request envelope reference",
    "P4-M4.0 Entry Gate Design Boundary Contract remains the inherited prior design boundary reference",
    "P4-M3.16 Governed Transition Intake Final Phase Handoff Summary remains the inherited prior closed-phase handoff reference",
    "P4-M3 static definition chain remains closed",
    "P4-M4 design layer remains design-boundary-only",
    "P4-M4 declared transition reason envelope design starts only as a static declared reason description surface",
    "P4-M4 transition reason validation remains not implemented",
    "P4-M4 reason sufficiency validation remains not implemented",
    "P4-M4 reason consistency validation remains not implemented",
    "P4-M4 reason integrity validation remains not implemented",
    "P4-M4 transition reason acceptance remains not implemented",
    "P4-M4 transition reason rejection remains not implemented",
    "P4-M4 transition reason scoring remains not implemented",
    "P4-M4 transition reason ranking remains not implemented",
    "P4-M4 transition reason recommendation remains not implemented",
    "P4-M4 transition reason generation remains not implemented",
    "P4-M4 transition reason justification remains not implemented",
    "P4-M4 transition reason routing remains not implemented",
    "P4-M4 transition reason planning remains not implemented",
    "P4-M4 transition reason execution remains not implemented",
    "P4-M4 transition reason record creation remains not implemented",
    "P4-M4 reason validation record creation remains not implemented",
    "P4-M4 reason scoring record creation remains not implemented",
    "P4-M4 reason routing record creation remains not implemented",
    "P4-M4 reason planning record creation remains not implemented",
    "P4-M4 reason justification record creation remains not implemented",
    "P4-M4 target phase validation remains not implemented",
    "P4-M4 phase transition validation remains not implemented",
    "P4-M4 readiness scoring remains not implemented",
    "P4-M4 state-space graph remains not implemented",
    "P4-M4 transition graph remains not implemented",
    "P4-M4 constraint graph remains not implemented",
    "P4-M4 target phase to transition reason mapping remains not implemented",
    "P4-M4 human context to transition reason mapping remains not implemented",
    "P4-M4 evidence validation remains not implemented",
    "P4-M4 reference resolution remains not implemented",
    "P4-M4 reference validation remains not implemented",
    "P4-M4 citation validation remains not implemented",
    "P4-M4 source fetching remains not implemented",
    "P4-M4 provenance writing remains not implemented",
    "P4-M4 request intake remains not implemented",
    "P4-M4 request validation remains not implemented",
    "P4-M4 execution remains not implemented",
    "P4-M4 entry gate remains not implemented",
    "P4-M4 entry gate validation remains not implemented",
    "P4-M4 readiness validation remains not implemented",
    "P4-M4 verdict generation remains not implemented",
    "P4-M4 approval remains not implemented",
    "P4-M4 authorization remains not implemented",
    "P4-M4 confirmation remains not implemented",
    "P4-M4 transition execution remains not implemented",
    "P4-M5 remains not started",
    "v7 remains not started",
    "productization remains not started",
    "UI remains not started",
    "Operator Console remains not started",
    "P4-M4.5 is not transition reason intake",
    "P4-M4.5 is not live transition reason parsing",
    "P4-M4.5 is not transition reason validation",
    "P4-M4.5 is not reason sufficiency validation",
    "P4-M4.5 is not reason consistency validation",
    "P4-M4.5 is not reason integrity validation",
    "P4-M4.5 is not transition reason acceptance",
    "P4-M4.5 is not transition reason rejection",
    "P4-M4.5 is not transition reason scoring",
    "P4-M4.5 is not transition reason ranking",
    "P4-M4.5 is not transition reason recommendation",
    "P4-M4.5 is not transition reason generation",
    "P4-M4.5 is not transition reason justification",
    "P4-M4.5 is not transition reason routing",
    "P4-M4.5 is not transition reason planning",
    "P4-M4.5 is not transition reason execution",
    "P4-M4.5 is not transition reason record creation",
    "P4-M4.5 is not reason validation record creation",
    "P4-M4.5 is not reason scoring record creation",
    "P4-M4.5 is not reason routing record creation",
    "P4-M4.5 is not reason planning record creation",
    "P4-M4.5 is not reason justification record creation",
    "P4-M4.5 is not target phase validation",
    "P4-M4.5 is not phase transition validation",
    "P4-M4.5 is not readiness scoring",
    "P4-M4.5 is not target phase routing",
    "P4-M4.5 is not transition planning",
    "P4-M4.5 is not path planning",
    "P4-M4.5 is not state-space graph",
    "P4-M4.5 is not transition graph",
    "P4-M4.5 is not constraint graph",
    "P4-M4.5 is not target phase to transition reason mapping",
    "P4-M4.5 is not human context to transition reason mapping",
    "P4-M4.5 is not evidence validation",
    "P4-M4.5 is not reference resolution",
    "P4-M4.5 is not reference validation",
    "P4-M4.5 is not citation validation",
    "P4-M4.5 is not source fetching",
    "P4-M4.5 is not provenance writing",
    "P4-M4.5 is not request intake",
    "P4-M4.5 is not request validation",
    "P4-M4.5 is not entry gate validation",
    "P4-M4.5 is not readiness validation",
    "P4-M4.5 is not a working entry gate",
    "P4-M4.5 is not gate activation",
    "P4-M4.5 is not gate execution",
    "P4-M4.5 is not readiness verdict",
    "P4-M4.5 is not validation verdict",
    "P4-M4.5 is not transition reason verdict",
    "P4-M4.5 is not transition verdict",
    "P4-M4.5 is not approval",
    "P4-M4.5 is not authorization",
    "P4-M4.5 is not confirmation",
    "P4-M4.5 is not recommendation",
    "P4-M4.5 is not ranking",
    "P4-M4.5 is not next action generation",
    "P4-M4.5 is not transition execution",
    "P4-M4.5 is not record creation",
    "P4-M4.5 is not memory mutation",
    "P4-M4.5 is not roadmap mutation",
    "no transition reason intake",
    "no live transition reason parsing",
    "no transition reason validation",
    "no reason sufficiency validation",
    "no reason consistency validation",
    "no reason integrity validation",
    "no transition reason acceptance",
    "no transition reason rejection",
    "no transition reason scoring",
    "no transition reason ranking",
    "no transition reason recommendation",
    "no transition reason generation",
    "no transition reason justification",
    "no transition reason routing",
    "no transition reason planning",
    "no transition reason execution",
    "no transition reason record creation",
    "no reason validation record creation",
    "no reason scoring record creation",
    "no reason routing record creation",
    "no reason planning record creation",
    "no reason justification record creation",
    "no target phase validation",
    "no phase transition validation",
    "no readiness scoring",
    "no target phase routing",
    "no transition planning",
    "no path planning",
    "no state-space graph",
    "no transition graph",
    "no constraint graph",
    "no target phase to transition reason mapping",
    "no human context to transition reason mapping",
    "no evidence validation",
    "no reference resolution",
    "no reference validation",
    "no citation validation",
    "no source fetching",
    "no provenance writing",
    "no request intake",
    "no request validation",
    "no entry gate validation",
    "no readiness validation",
    "no working entry gate",
    "no gate activation",
    "no gate execution",
    "no readiness verdict",
    "no validation verdict",
    "no transition reason verdict",
    "no transition verdict",
    "no approval",
    "no authorization",
    "no confirmation",
    "no recommendation",
    "no ranking",
    "no next action generation",
    "no transition execution",
    "no record creation",
    "no memory mutation",
    "no roadmap mutation",
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
    "declared_transition_reason_envelope_design_only",
    "declared_reason_surface_only",
    "reason_non_validation_boundary_only",
    "declaration_only",
    "inspection_only",
    "p4_m4_5_declared_transition_reason_envelope_contract_started",
    "p4_m4_5_definition_only",
    "p4_m4_5_declared_transition_reason_envelope_design_only",
    "p4_m4_5_declared_reason_surface_only",
    "p4_m4_5_reason_non_validation_boundary_only",
    "p4_m4_5_declaration_only",
    "p4_m4_4_target_phase_envelope_contract_reference_defined",
    "p4_m4_4_target_phase_static_projection_reference_defined",
    "p4_m4_3_declared_human_context_envelope_contract_reference_defined",
    "p4_m4_2_evidence_reference_envelope_contract_reference_defined",
    "p4_m4_1_entry_gate_design_request_envelope_contract_reference_defined",
    "p4_m4_0_entry_gate_design_boundary_contract_reference_defined",
    "p4_m3_16_final_phase_handoff_summary_reference_defined",
    "p4_m3_static_definition_chain_closed_reference_defined",
    "p4_m4_design_boundary_reference_defined",
    "p4_m4_declared_transition_reason_envelope_design_defined",
    "p4_m4_declared_reason_surface_defined",
    "p4_m4_transition_reason_non_validation_boundary_defined",
    "p4_m4_transition_reason_non_acceptance_boundary_defined",
    "p4_m4_transition_reason_non_rejection_boundary_defined",
    "p4_m4_transition_reason_non_scoring_boundary_defined",
    "p4_m4_transition_reason_non_routing_boundary_defined",
    "p4_m4_transition_reason_non_planning_boundary_defined",
    "p4_m4_transition_reason_non_execution_boundary_defined",
    "p4_m4_transition_reason_validation_semantics_prohibited",
    "p4_m4_reason_sufficiency_validation_semantics_prohibited",
    "p4_m4_reason_consistency_validation_semantics_prohibited",
    "p4_m4_reason_integrity_validation_semantics_prohibited",
    "p4_m4_reason_justification_semantics_prohibited",
    "p4_m4_routing_semantics_prohibited",
    "p4_m4_planning_semantics_prohibited",
    "p4_m4_verdict_semantics_prohibited",
    "p4_m4_execution_semantics_prohibited",
    "p4_m4_record_creation_semantics_prohibited",
    "p4_m4_mutation_semantics_prohibited",
    "p4_m5_start_deferred",
    "v7_start_deferred",
    "productization_deferred",
    "ui_deferred",
    "operator_console_deferred",
)


FALSE_STATUS_FLAGS = (
    "live_validation_enabled",
    "transition_reason_intake_enabled",
    "live_transition_reason_parsing_enabled",
    "transition_reason_validation_enabled",
    "reason_sufficiency_validation_enabled",
    "reason_consistency_validation_enabled",
    "reason_integrity_validation_enabled",
    "transition_reason_acceptance_enabled",
    "transition_reason_rejection_enabled",
    "transition_reason_scoring_enabled",
    "transition_reason_ranking_enabled",
    "transition_reason_recommendation_enabled",
    "transition_reason_generation_enabled",
    "transition_reason_justification_enabled",
    "transition_reason_routing_enabled",
    "transition_reason_planning_enabled",
    "transition_reason_execution_enabled",
    "transition_reason_record_creation_enabled",
    "reason_validation_record_creation_enabled",
    "reason_scoring_record_creation_enabled",
    "reason_routing_record_creation_enabled",
    "reason_planning_record_creation_enabled",
    "reason_justification_record_creation_enabled",
    "target_phase_validation_enabled",
    "phase_transition_validation_enabled",
    "phase_readiness_validation_enabled",
    "target_phase_readiness_validation_enabled",
    "readiness_scoring_enabled",
    "target_phase_scoring_enabled",
    "target_phase_routing_enabled",
    "target_phase_execution_enabled",
    "transition_planning_enabled",
    "path_planning_enabled",
    "state_space_graph_enabled",
    "transition_graph_enabled",
    "constraint_graph_enabled",
    "semantic_target_field_graph_enabled",
    "target_phase_to_transition_reason_mapping_enabled",
    "human_context_to_transition_reason_mapping_enabled",
    "human_context_intake_enabled",
    "live_human_context_parsing_enabled",
    "human_context_validation_enabled",
    "identity_validation_enabled",
    "actor_validation_enabled",
    "user_validation_enabled",
    "operator_validation_enabled",
    "consent_validation_enabled",
    "authority_validation_enabled",
    "approval_validation_enabled",
    "authorization_validation_enabled",
    "confirmation_validation_enabled",
    "human_context_record_creation_enabled",
    "evidence_intake_enabled",
    "live_evidence_parsing_enabled",
    "evidence_validation_enabled",
    "evidence_record_creation_enabled",
    "reference_resolution_enabled",
    "reference_validation_enabled",
    "reference_integrity_validation_enabled",
    "citation_validation_enabled",
    "source_fetching_enabled",
    "provenance_writing_enabled",
    "request_intake_enabled",
    "live_request_parsing_enabled",
    "request_validation_enabled",
    "request_acceptance_enabled",
    "request_rejection_enabled",
    "request_routing_enabled",
    "request_execution_enabled",
    "request_record_creation_enabled",
    "boundary_validation_enabled",
    "phase_validation_enabled",
    "entry_gate_validation_enabled",
    "entry_readiness_validation_enabled",
    "readiness_validation_enabled",
    "transition_readiness_validation_enabled",
    "transition_validation_enabled",
    "governed_transition_intake_validation_enabled",
    "package_validation_enabled",
    "closure_validation_enabled",
    "handoff_validation_enabled",
    "final_phase_handoff_validation_enabled",
    "working_entry_gate_enabled",
    "gate_activation_enabled",
    "gate_execution_enabled",
    "p4_m4_execution_enabled",
    "operational_behavior_enabled",
    "readiness_verdict_enabled",
    "validation_verdict_enabled",
    "transition_reason_verdict_enabled",
    "transition_verdict_enabled",
    "human_context_verdict_enabled",
    "evidence_verdict_enabled",
    "reference_verdict_enabled",
    "citation_verdict_enabled",
    "entry_verdict_enabled",
    "gate_verdict_enabled",
    "approval_enabled",
    "authorization_enabled",
    "confirmation_enabled",
    "recommendation_enabled",
    "ranking_enabled",
    "next_action_generation_enabled",
    "transition_execution_enabled",
    "command_execution_enabled",
    "record_creation_enabled",
    "persistence_enabled",
    "storage_enabled",
    "memory_mutation_enabled",
    "roadmap_mutation_enabled",
    "lifecycle_mutation_enabled",
    "proposal_mutation_enabled",
    "transition_reason_mutation_enabled",
    "target_phase_mutation_enabled",
    "phase_mutation_enabled",
    "transition_mutation_enabled",
    "human_context_mutation_enabled",
    "evidence_mutation_enabled",
    "api_enabled",
    "mcp_enabled",
    "connector_enabled",
    "agent_call_enabled",
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


DECLARED_TRANSITION_REASON_ENVELOPE_CONTRACT_BOUNDARY = (
    "P4-M4.5 Declared Transition Reason Envelope Contract read-only "
    "definition-only declared-transition-reason-envelope-design-only "
    "declared-reason-surface-only reason-non-validation-boundary-only "
    "declaration-only inspection-only. P4-M4.5 Declared Transition Reason "
    "Envelope Contract is definition only. "
    + " ".join(f"{phrase}." for phrase in BOUNDARY_PHRASE_LINES)
)


_FIELD_IDS = (
    "p4-m4-declared-transition-reason-envelope-contract-id",
    "p4-m4-declared-transition-reason-envelope-contract-phase",
    "p4-m4-declared-transition-reason-envelope-contract-mode",
    "p4-m4-declared-transition-reason-envelope-contract-direct-prior-target-phase-envelope-reference",
    "p4-m4-declared-transition-reason-envelope-contract-inherited-prior-declared-human-context-envelope-reference",
    "p4-m4-declared-transition-reason-envelope-contract-inherited-prior-evidence-reference-envelope-reference",
    "p4-m4-declared-transition-reason-envelope-contract-inherited-prior-request-envelope-reference",
    "p4-m4-declared-transition-reason-envelope-contract-inherited-prior-boundary-reference",
    "p4-m4-declared-transition-reason-envelope-contract-inherited-prior-handoff-reference",
    "p4-m4-declared-transition-reason-envelope-contract-scope",
    "p4-m4-declared-transition-reason-envelope-contract-declared-transition-reason-envelope-design-only",
    "p4-m4-declared-transition-reason-envelope-contract-declared-reason-surface-definition",
    "p4-m4-declared-transition-reason-envelope-contract-reason-non-validation-boundary-definition",
    "p4-m4-declared-transition-reason-envelope-contract-declaration-only-semantics-definition",
    "p4-m4-declared-transition-reason-envelope-contract-target-phase-static-projection-reference-definition",
    "p4-m4-declared-transition-reason-envelope-contract-transition-reason-validation-semantics-disabled",
    "p4-m4-declared-transition-reason-envelope-contract-routing-planning-execution-scoring-justification-semantics-disabled",
    "p4-m4-declared-transition-reason-envelope-contract-p4-m5-v7-productization-ui-deferred",
)


_FIELD_NAMES = (
    "P4-M4 Declared Transition Reason Envelope Contract Id",
    "P4-M4 Declared Transition Reason Envelope Contract Phase",
    "P4-M4 Declared Transition Reason Envelope Contract Mode",
    "P4-M4 Declared Transition Reason Envelope Contract Direct Prior Target Phase Envelope Reference",
    "P4-M4 Declared Transition Reason Envelope Contract Inherited Prior Declared Human Context Envelope Reference",
    "P4-M4 Declared Transition Reason Envelope Contract Inherited Prior Evidence Reference Envelope Reference",
    "P4-M4 Declared Transition Reason Envelope Contract Inherited Prior Request Envelope Reference",
    "P4-M4 Declared Transition Reason Envelope Contract Inherited Prior Boundary Reference",
    "P4-M4 Declared Transition Reason Envelope Contract Inherited Prior Handoff Reference",
    "P4-M4 Declared Transition Reason Envelope Contract Scope",
    "P4-M4 Declared Transition Reason Envelope Contract Declared Transition Reason Envelope Design Only",
    "P4-M4 Declared Transition Reason Envelope Contract Declared Reason Surface Definition",
    "P4-M4 Declared Transition Reason Envelope Contract Reason Non-Validation Boundary Definition",
    "P4-M4 Declared Transition Reason Envelope Contract Declaration Only Semantics Definition",
    "P4-M4 Declared Transition Reason Envelope Contract Target Phase Static Projection Reference Definition",
    "P4-M4 Declared Transition Reason Envelope Contract Transition Reason Validation Semantics Disabled",
    "P4-M4 Declared Transition Reason Envelope Contract Routing Planning Execution Scoring Justification Semantics Disabled",
    "P4-M4 Declared Transition Reason Envelope Contract P4-M5 V7 Productization UI Deferred",
)


def _field_purpose(field_id: str) -> str:
    return (
        f"Defines {field_id} as read-only definition-only "
        "declared-transition-reason-envelope-design-only "
        "declared-reason-surface-only reason-non-validation-boundary-only "
        "declaration-only inspection-only P4-M4.5 Declared Transition Reason "
        "Envelope Contract context; P4-M4.4 Target Phase Envelope Contract "
        "remains the direct prior target phase envelope reference; P4-M4.4 "
        "target phase remains only an inherited static target phase projection "
        "reference; P4-M4 declared transition reason envelope design starts "
        "only as a static declared reason description surface; no transition "
        "reason intake; no live transition reason parsing; no transition "
        "reason validation; no reason sufficiency validation; no reason "
        "consistency validation; no reason integrity validation; no transition "
        "reason acceptance; no transition reason rejection; no transition "
        "reason scoring; no transition reason ranking; no transition reason "
        "recommendation; no transition reason generation; no transition reason "
        "justification; no transition reason routing; no transition reason "
        "planning; no transition reason execution; no transition reason record "
        "creation; no reason validation record creation; no reason scoring "
        "record creation; no reason routing record creation; no reason "
        "planning record creation; no reason justification record creation; "
        "no target phase validation; no phase transition validation; no "
        "readiness scoring; no target phase routing; no transition planning; "
        "no path planning; no state-space graph; no transition graph; no "
        "constraint graph; no target phase to transition reason mapping; no "
        "human context to transition reason mapping; no evidence validation; "
        "no reference resolution; no reference validation; no citation "
        "validation; no source fetching; no provenance writing; no request "
        "intake; no request validation; no entry gate validation; no readiness "
        "validation; no working entry gate; no gate activation; no gate "
        "execution; no readiness verdict; no validation verdict; no "
        "transition reason verdict; no transition verdict; no approval; no "
        "authorization; no confirmation; no recommendation; no ranking; no "
        "next action generation; no transition execution; no record creation; "
        "no memory mutation; no roadmap mutation; no P4-M5; no v7; no "
        "productization; no UI; no Operator Console; no version bump; no tag."
    )


_DECLARED_TRANSITION_REASON_ENVELOPE_CONTRACT_FIELDS = tuple(
    DeclaredTransitionReasonEnvelopeContractField(
        index,
        field_id,
        _FIELD_NAMES[index - 1],
        _field_purpose(field_id),
        "p4-m4-declared-transition-reason-envelope-contract-category",
        (
            "no transition reason intake semantics; no live transition reason "
            "parsing semantics; no transition reason validation semantics; no "
            "reason sufficiency validation semantics; no reason consistency "
            "validation semantics; no reason integrity validation semantics; "
            "no transition reason acceptance semantics; no transition reason "
            "rejection semantics; no transition reason scoring semantics; no "
            "transition reason ranking semantics; no transition reason "
            "recommendation semantics; no transition reason generation "
            "semantics; no transition reason justification semantics; no "
            "transition reason routing semantics; no transition reason planning "
            "semantics; no transition reason execution semantics; no target "
            "phase to transition reason mapping semantics; no human context to "
            "transition reason mapping semantics; no evidence validation "
            "semantics; no reference resolution semantics; no reference "
            "validation semantics; no citation validation semantics; no source "
            "fetching semantics; no provenance writing semantics; no request "
            "intake semantics; no request validation semantics; no verdict "
            "semantics; no approval semantics; no authorization semantics; no "
            "confirmation semantics; no recommendation semantics; no ranking "
            "semantics; no next-action semantics; no transition execution "
            "semantics; no record creation semantics; no mutation semantics"
        ),
    )
    for index, field_id in enumerate(_FIELD_IDS, start=1)
)


def list_declared_transition_reason_envelope_contract_fields() -> tuple[
    DeclaredTransitionReasonEnvelopeContractField, ...
]:
    return _DECLARED_TRANSITION_REASON_ENVELOPE_CONTRACT_FIELDS


def declared_transition_reason_envelope_contract_field_ids() -> tuple[str, ...]:
    return tuple(
        field.field_id
        for field in list_declared_transition_reason_envelope_contract_fields()
    )


def render_declared_transition_reason_envelope_contract_markdown(
    fields: Sequence[DeclaredTransitionReasonEnvelopeContractField] | None = None,
) -> str:
    field_values = (
        tuple(fields)
        if fields is not None
        else list_declared_transition_reason_envelope_contract_fields()
    )
    status = declared_transition_reason_envelope_contract_report()
    lines = [
        "# P4-M4.5 Declared Transition Reason Envelope Contract",
        "",
        "P4-M4.5 Declared Transition Reason Envelope Contract.",
        "",
        "read-only.",
        "",
        "definition-only.",
        "",
        "declared-transition-reason-envelope-design-only.",
        "",
        "declared-reason-surface-only.",
        "",
        "reason-non-validation-boundary-only.",
        "",
        "declaration-only.",
        "",
        "inspection-only.",
        "",
        "P4-M4.5 Declared Transition Reason Envelope Contract is definition only.",
        "",
        "P4-M4.5 is declared-transition-reason-envelope-design-only.",
        "",
        "P4-M4.5 is declared-reason-surface-only.",
        "",
        "P4-M4.5 is reason-non-validation-boundary-only.",
        "",
        "P4-M4.5 is declaration-only.",
        "",
        "P4-M4.4 Target Phase Envelope Contract remains the direct prior target phase envelope reference.",
        "",
        "P4-M4.4 target phase remains only an inherited static target phase projection reference.",
        "",
    ]
    for prior_layer in DIRECT_PRIOR_DEFINITION_LAYER_REFERENCES:
        lines.extend([f"{prior_layer} remains a referenced definition layer.", ""])
    for prior_layer in INHERITED_PRIOR_DEFINITION_LAYER_REFERENCES:
        lines.extend([f"{prior_layer} remains an inherited referenced definition layer.", ""])
    for phrase in BOUNDARY_PHRASE_LINES:
        lines.extend([f"{phrase}.", ""])
    lines.extend([
        DECLARED_TRANSITION_REASON_ENVELOPE_CONTRACT_BOUNDARY,
        "",
        "## Status Report",
        "",
    ])
    for key, value in status.items():
        lines.append(f"- {key}: {value}")
    lines.extend([
        "",
        "## Declared Transition Reason Envelope Contract Fields",
        "",
    ])
    for field in field_values:
        lines.extend([
            f"### {field.field_order}. {field.field_id}",
            "",
            f"- Field name: {field.field_name}",
            f"- Field purpose: {field.field_purpose}",
            "- P4-M4 declared transition reason envelope contract category: "
            f"{field.p4_m4_declared_transition_reason_envelope_contract_category}",
            "- P4-M4 declared transition reason envelope contract semantics disabled: "
            f"{field.p4_m4_declared_transition_reason_envelope_contract_semantics_disabled}",
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def declared_transition_reason_envelope_contract_as_dicts() -> tuple[
    dict[str, object], ...
]:
    return tuple(
        asdict(field)
        for field in list_declared_transition_reason_envelope_contract_fields()
    )


def declared_transition_reason_envelope_contract_report() -> dict[str, object]:
    status: dict[str, object] = {
        "phase": "P4-M4.5",
        "feature": "Declared Transition Reason Envelope Contract",
        "mode": "read-only",
        "boundary": DECLARED_TRANSITION_REASON_ENVELOPE_CONTRACT_BOUNDARY,
        "package_version": P4_M4_5_PACKAGE_VERSION,
        "declared_transition_reason_envelope_contract_field_count": len(_FIELD_IDS),
        "referenced_p4_m4_4_target_phase_envelope_contract_field_count": len(
            target_phase_envelope_contract_field_ids()
        ),
    }
    status.update({flag: True for flag in TRUE_STATUS_FLAGS})
    status.update({flag: False for flag in FALSE_STATUS_FLAGS})
    return status
