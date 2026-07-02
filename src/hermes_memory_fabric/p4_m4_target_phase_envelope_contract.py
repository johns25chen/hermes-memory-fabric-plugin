from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence

from .p4_m4_declared_human_context_envelope_contract import (
    declared_human_context_envelope_contract_field_ids,
)


P4_M4_4_PACKAGE_VERSION = "6.16.0"


@dataclass(frozen=True)
class TargetPhaseEnvelopeContractField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    p4_m4_target_phase_envelope_contract_category: str
    p4_m4_target_phase_envelope_contract_semantics_disabled: str


DIRECT_PRIOR_DEFINITION_LAYER_REFERENCES = (
    "P4-M4.3 Declared Human Context Envelope Contract",
)

INHERITED_PRIOR_DEFINITION_LAYER_REFERENCES = (
    "P4-M4.2 Evidence Reference Envelope Contract",
    "P4-M4.1 Entry Gate Design Request Envelope Contract",
    "P4-M4.0 Entry Gate Design Boundary Contract",
    "P4-M3.16 Governed Transition Intake Final Phase Handoff Summary",
)


BOUNDARY_PHRASE_LINES = (
    "P4-M4.4",
    "Target Phase Envelope Contract",
    "read-only",
    "definition-only",
    "target-phase-envelope-design-only",
    "projection-surface-only",
    "constraint-field-only",
    "converging-layer-only",
    "inspection-only",
    "P4-M4.4 Target Phase Envelope Contract is definition only",
    "P4-M4.4 is target-phase-envelope-design-only",
    "P4-M4.4 is projection-surface-only",
    "P4-M4.4 is constraint-field-only",
    "P4-M4.4 is converging-layer-only",
    "P4-M4.3 Declared Human Context Envelope Contract remains the direct prior declared human context envelope reference",
    "P4-M4.3 declared human context remains only an inherited weak prior reference",
    "P4-M4.2 Evidence Reference Envelope Contract remains the inherited prior evidence reference envelope reference",
    "P4-M4.1 Entry Gate Design Request Envelope Contract remains the inherited prior request envelope reference",
    "P4-M4.0 Entry Gate Design Boundary Contract remains the inherited prior design boundary reference",
    "P4-M3.16 Governed Transition Intake Final Phase Handoff Summary remains the inherited prior closed-phase handoff reference",
    "P4-M3 static definition chain remains closed",
    "P4-M4 design layer remains design-boundary-only",
    "P4-M4 target phase envelope design starts only as a static future-state projection surface",
    "P4-M4 target phase constraint field remains static definition only",
    "P4-M4 target phase intake remains not implemented",
    "P4-M4 target phase parsing remains not implemented",
    "P4-M4 target phase validation remains not implemented",
    "P4-M4 phase transition validation remains not implemented",
    "P4-M4 target phase readiness validation remains not implemented",
    "P4-M4 readiness scoring remains not implemented",
    "P4-M4 target phase routing remains not implemented",
    "P4-M4 transition planning remains not implemented",
    "P4-M4 path planning remains not implemented",
    "P4-M4 target phase generation remains not implemented",
    "P4-M4 target phase recommendation remains not implemented",
    "P4-M4 target phase ranking remains not implemented",
    "P4-M4 target phase execution remains not implemented",
    "P4-M4 state-space graph remains not implemented",
    "P4-M4 transition graph remains not implemented",
    "P4-M4 constraint graph remains not implemented",
    "P4-M4 human context to target phase mapping remains not implemented",
    "P4-M4 target phase record creation remains not implemented",
    "P4-M4 phase record creation remains not implemented",
    "P4-M4 transition record creation remains not implemented",
    "P4-M4 readiness record creation remains not implemented",
    "P4-M4 scoring record creation remains not implemented",
    "P4-M4 graph record creation remains not implemented",
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
    "P4-M4.4 is not target phase intake",
    "P4-M4.4 is not live target phase parsing",
    "P4-M4.4 is not target phase validation",
    "P4-M4.4 is not phase transition validation",
    "P4-M4.4 is not target phase readiness validation",
    "P4-M4.4 is not readiness scoring",
    "P4-M4.4 is not target phase scoring",
    "P4-M4.4 is not target phase routing",
    "P4-M4.4 is not transition planning",
    "P4-M4.4 is not path planning",
    "P4-M4.4 is not target phase generation",
    "P4-M4.4 is not target phase recommendation",
    "P4-M4.4 is not target phase ranking",
    "P4-M4.4 is not target phase execution",
    "P4-M4.4 is not state-space graph",
    "P4-M4.4 is not transition graph",
    "P4-M4.4 is not constraint graph",
    "P4-M4.4 is not human context to target phase mapping",
    "P4-M4.4 is not target phase record creation",
    "P4-M4.4 is not phase record creation",
    "P4-M4.4 is not transition record creation",
    "P4-M4.4 is not readiness record creation",
    "P4-M4.4 is not scoring record creation",
    "P4-M4.4 is not graph record creation",
    "P4-M4.4 is not evidence validation",
    "P4-M4.4 is not reference resolution",
    "P4-M4.4 is not reference validation",
    "P4-M4.4 is not citation validation",
    "P4-M4.4 is not source fetching",
    "P4-M4.4 is not provenance writing",
    "P4-M4.4 is not request intake",
    "P4-M4.4 is not request validation",
    "P4-M4.4 is not entry gate validation",
    "P4-M4.4 is not readiness validation",
    "P4-M4.4 is not a working entry gate",
    "P4-M4.4 is not gate activation",
    "P4-M4.4 is not gate execution",
    "P4-M4.4 is not readiness verdict",
    "P4-M4.4 is not validation verdict",
    "P4-M4.4 is not target phase verdict",
    "P4-M4.4 is not phase verdict",
    "P4-M4.4 is not transition verdict",
    "P4-M4.4 is not approval",
    "P4-M4.4 is not authorization",
    "P4-M4.4 is not confirmation",
    "P4-M4.4 is not recommendation",
    "P4-M4.4 is not ranking",
    "P4-M4.4 is not next action generation",
    "P4-M4.4 is not transition execution",
    "P4-M4.4 is not record creation",
    "P4-M4.4 is not memory mutation",
    "P4-M4.4 is not roadmap mutation",
    "no target phase intake",
    "no live target phase parsing",
    "no target phase validation",
    "no phase transition validation",
    "no target phase readiness validation",
    "no readiness scoring",
    "no target phase scoring",
    "no target phase routing",
    "no transition planning",
    "no path planning",
    "no target phase generation",
    "no target phase recommendation",
    "no target phase ranking",
    "no target phase execution",
    "no state-space graph",
    "no transition graph",
    "no constraint graph",
    "no human context to target phase mapping",
    "no target phase record creation",
    "no phase record creation",
    "no transition record creation",
    "no readiness record creation",
    "no scoring record creation",
    "no graph record creation",
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
    "no target phase verdict",
    "no phase verdict",
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
    "target_phase_envelope_design_only",
    "projection_surface_only",
    "constraint_field_only",
    "converging_layer_only",
    "inspection_only",
    "p4_m4_4_target_phase_envelope_contract_started",
    "p4_m4_4_definition_only",
    "p4_m4_4_target_phase_envelope_design_only",
    "p4_m4_4_projection_surface_only",
    "p4_m4_4_constraint_field_only",
    "p4_m4_4_converging_layer_only",
    "p4_m4_3_declared_human_context_envelope_contract_reference_defined",
    "p4_m4_3_declared_human_context_weak_prior_reference_defined",
    "p4_m4_2_evidence_reference_envelope_contract_reference_defined",
    "p4_m4_1_entry_gate_design_request_envelope_contract_reference_defined",
    "p4_m4_0_entry_gate_design_boundary_contract_reference_defined",
    "p4_m3_16_final_phase_handoff_summary_reference_defined",
    "p4_m3_static_definition_chain_closed_reference_defined",
    "p4_m4_design_boundary_reference_defined",
    "p4_m4_target_phase_envelope_design_defined",
    "p4_m4_target_phase_projection_surface_defined",
    "p4_m4_target_phase_constraint_field_defined",
    "p4_m4_target_phase_non_validation_boundary_defined",
    "p4_m4_target_phase_non_routing_boundary_defined",
    "p4_m4_target_phase_non_planning_boundary_defined",
    "p4_m4_target_phase_non_scoring_boundary_defined",
    "p4_m4_target_phase_non_execution_boundary_defined",
    "p4_m4_target_phase_non_graph_boundary_defined",
    "p4_m4_target_phase_validation_semantics_prohibited",
    "p4_m4_phase_transition_validation_semantics_prohibited",
    "p4_m4_readiness_scoring_semantics_prohibited",
    "p4_m4_routing_semantics_prohibited",
    "p4_m4_planning_semantics_prohibited",
    "p4_m4_graph_semantics_prohibited",
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
    "target_phase_intake_enabled",
    "live_target_phase_parsing_enabled",
    "target_phase_validation_enabled",
    "target_phase_acceptance_enabled",
    "target_phase_rejection_enabled",
    "target_phase_routing_enabled",
    "target_phase_execution_enabled",
    "target_phase_record_creation_enabled",
    "phase_transition_validation_enabled",
    "phase_readiness_validation_enabled",
    "target_phase_readiness_validation_enabled",
    "readiness_scoring_enabled",
    "target_phase_scoring_enabled",
    "target_phase_recommendation_enabled",
    "target_phase_ranking_enabled",
    "target_phase_generation_enabled",
    "transition_planning_enabled",
    "path_planning_enabled",
    "state_space_graph_enabled",
    "transition_graph_enabled",
    "constraint_graph_enabled",
    "semantic_target_field_graph_enabled",
    "human_context_to_target_phase_mapping_enabled",
    "phase_record_creation_enabled",
    "transition_record_creation_enabled",
    "scoring_record_creation_enabled",
    "routing_record_creation_enabled",
    "planning_record_creation_enabled",
    "graph_record_creation_enabled",
    "state_graph_record_creation_enabled",
    "transition_graph_record_creation_enabled",
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
    "identity_record_creation_enabled",
    "actor_record_creation_enabled",
    "consent_record_creation_enabled",
    "evidence_intake_enabled",
    "live_evidence_parsing_enabled",
    "evidence_validation_enabled",
    "evidence_record_creation_enabled",
    "reference_resolution_enabled",
    "reference_validation_enabled",
    "reference_integrity_validation_enabled",
    "citation_validation_enabled",
    "citation_mutation_enabled",
    "source_validation_enabled",
    "source_fetching_enabled",
    "provenance_writing_enabled",
    "provenance_mutation_enabled",
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
    "package_completeness_validation_enabled",
    "package_consistency_validation_enabled",
    "package_integrity_validation_enabled",
    "package_readiness_validation_enabled",
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
    "target_phase_verdict_enabled",
    "phase_verdict_enabled",
    "transition_verdict_enabled",
    "human_context_verdict_enabled",
    "identity_verdict_enabled",
    "approval_verdict_enabled",
    "authorization_verdict_enabled",
    "confirmation_verdict_enabled",
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
    "reference_record_creation_enabled",
    "citation_record_creation_enabled",
    "provenance_record_creation_enabled",
    "request_envelope_record_creation_enabled",
    "entry_record_creation_enabled",
    "gate_record_creation_enabled",
    "readiness_record_creation_enabled",
    "validation_record_creation_enabled",
    "approval_record_creation_enabled",
    "authorization_record_creation_enabled",
    "confirmation_record_creation_enabled",
    "recommendation_record_creation_enabled",
    "ranking_record_creation_enabled",
    "next_action_record_creation_enabled",
    "persistence_enabled",
    "storage_enabled",
    "memory_mutation_enabled",
    "roadmap_mutation_enabled",
    "lifecycle_mutation_enabled",
    "proposal_mutation_enabled",
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


TARGET_PHASE_ENVELOPE_CONTRACT_BOUNDARY = (
    "P4-M4.4 Target Phase Envelope Contract read-only definition-only "
    "target-phase-envelope-design-only projection-surface-only "
    "constraint-field-only converging-layer-only inspection-only. "
    "P4-M4.4 Target Phase Envelope Contract is definition only. "
    + " ".join(f"{phrase}." for phrase in BOUNDARY_PHRASE_LINES)
)


_FIELD_IDS = (
    "p4-m4-target-phase-envelope-contract-id",
    "p4-m4-target-phase-envelope-contract-phase",
    "p4-m4-target-phase-envelope-contract-mode",
    "p4-m4-target-phase-envelope-contract-direct-prior-declared-human-context-envelope-reference",
    "p4-m4-target-phase-envelope-contract-inherited-prior-evidence-reference-envelope-reference",
    "p4-m4-target-phase-envelope-contract-inherited-prior-request-envelope-reference",
    "p4-m4-target-phase-envelope-contract-inherited-prior-boundary-reference",
    "p4-m4-target-phase-envelope-contract-inherited-prior-handoff-reference",
    "p4-m4-target-phase-envelope-contract-scope",
    "p4-m4-target-phase-envelope-contract-target-phase-envelope-design-only",
    "p4-m4-target-phase-envelope-contract-target-phase-projection-surface-definition",
    "p4-m4-target-phase-envelope-contract-target-phase-constraint-field-definition",
    "p4-m4-target-phase-envelope-contract-converging-layer-semantics-definition",
    "p4-m4-target-phase-envelope-contract-human-context-weak-prior-semantics-definition",
    "p4-m4-target-phase-envelope-contract-target-phase-validation-semantics-disabled",
    "p4-m4-target-phase-envelope-contract-routing-planning-execution-scoring-graph-semantics-disabled",
    "p4-m4-target-phase-envelope-contract-p4-m5-v7-productization-ui-deferred",
)


_FIELD_NAMES = (
    "P4-M4 Target Phase Envelope Contract Id",
    "P4-M4 Target Phase Envelope Contract Phase",
    "P4-M4 Target Phase Envelope Contract Mode",
    "P4-M4 Target Phase Envelope Contract Direct Prior Declared Human Context Envelope Reference",
    "P4-M4 Target Phase Envelope Contract Inherited Prior Evidence Reference Envelope Reference",
    "P4-M4 Target Phase Envelope Contract Inherited Prior Request Envelope Reference",
    "P4-M4 Target Phase Envelope Contract Inherited Prior Boundary Reference",
    "P4-M4 Target Phase Envelope Contract Inherited Prior Handoff Reference",
    "P4-M4 Target Phase Envelope Contract Scope",
    "P4-M4 Target Phase Envelope Contract Target Phase Envelope Design Only",
    "P4-M4 Target Phase Envelope Contract Target Phase Projection Surface Definition",
    "P4-M4 Target Phase Envelope Contract Target Phase Constraint Field Definition",
    "P4-M4 Target Phase Envelope Contract Converging Layer Semantics Definition",
    "P4-M4 Target Phase Envelope Contract Human Context Weak Prior Semantics Definition",
    "P4-M4 Target Phase Envelope Contract Target Phase Validation Semantics Disabled",
    "P4-M4 Target Phase Envelope Contract Routing Planning Execution Scoring Graph Semantics Disabled",
    "P4-M4 Target Phase Envelope Contract P4-M5 V7 Productization UI Deferred",
)


def _field_purpose(field_id: str) -> str:
    return (
        f"Defines {field_id} as read-only definition-only "
        "target-phase-envelope-design-only projection-surface-only "
        "constraint-field-only converging-layer-only inspection-only P4-M4.4 "
        "Target Phase Envelope Contract context; P4-M4.3 Declared Human "
        "Context Envelope Contract remains the direct prior declared human "
        "context envelope reference; P4-M4.3 declared human context remains "
        "only an inherited weak prior reference; P4-M4.2 Evidence Reference "
        "Envelope Contract remains the inherited prior evidence reference "
        "envelope reference; P4-M4.1 Entry Gate Design Request Envelope "
        "Contract remains the inherited prior request envelope reference; "
        "P4-M4.0 Entry Gate Design Boundary Contract remains the inherited "
        "prior design boundary reference; P4-M3.16 Governed Transition Intake "
        "Final Phase Handoff Summary remains the inherited prior closed-phase "
        "handoff reference; P4-M3 static definition chain remains closed; "
        "P4-M4 target phase envelope design starts only as a static "
        "future-state projection surface; P4-M4 target phase constraint field "
        "remains static definition only; no target phase intake; no live "
        "target phase parsing; no target phase validation; no phase "
        "transition validation; no target phase readiness validation; no "
        "readiness scoring; no target phase scoring; no target phase routing; "
        "no transition planning; no path planning; no target phase generation; "
        "no target phase recommendation; no target phase ranking; no target "
        "phase execution; no state-space graph; no transition graph; no "
        "constraint graph; no human context to target phase mapping; no "
        "target phase record creation; no phase record creation; no transition "
        "record creation; no readiness record creation; no scoring record "
        "creation; no graph record creation; no evidence validation; no "
        "reference resolution; no reference validation; no citation "
        "validation; no source fetching; no provenance writing; no request "
        "intake; no request validation; no entry gate validation; no readiness "
        "validation; no working entry gate; no gate activation; no gate "
        "execution; no readiness verdict; no validation verdict; no target "
        "phase verdict; no phase verdict; no transition verdict; no approval; "
        "no authorization; no confirmation; no recommendation; no ranking; "
        "no next action generation; no transition execution; no record "
        "creation; no memory mutation; no roadmap mutation; no P4-M5; no v7; "
        "no productization; no UI; no Operator Console; no version bump; no tag."
    )


_TARGET_PHASE_ENVELOPE_CONTRACT_FIELDS = tuple(
    TargetPhaseEnvelopeContractField(
        index,
        field_id,
        _FIELD_NAMES[index - 1],
        _field_purpose(field_id),
        "p4-m4-target-phase-envelope-contract-category",
        (
            "no target phase intake semantics; no live target phase parsing "
            "semantics; no target phase validation semantics; no phase "
            "transition validation semantics; no target phase readiness "
            "validation semantics; no readiness scoring semantics; no target "
            "phase scoring semantics; no target phase routing semantics; no "
            "transition planning semantics; no path planning semantics; no "
            "target phase generation semantics; no target phase recommendation "
            "semantics; no target phase ranking semantics; no target phase "
            "execution semantics; no state-space graph semantics; no transition "
            "graph semantics; no constraint graph semantics; no human context "
            "to target phase mapping semantics; no evidence validation "
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


def list_target_phase_envelope_contract_fields() -> tuple[TargetPhaseEnvelopeContractField, ...]:
    return _TARGET_PHASE_ENVELOPE_CONTRACT_FIELDS


def target_phase_envelope_contract_field_ids() -> tuple[str, ...]:
    return tuple(field.field_id for field in list_target_phase_envelope_contract_fields())


def render_target_phase_envelope_contract_markdown(
    fields: Sequence[TargetPhaseEnvelopeContractField] | None = None,
) -> str:
    field_values = (
        tuple(fields)
        if fields is not None
        else list_target_phase_envelope_contract_fields()
    )
    status = target_phase_envelope_contract_report()
    lines = [
        "# P4-M4.4 Target Phase Envelope Contract",
        "",
        "P4-M4.4 Target Phase Envelope Contract.",
        "",
        "read-only.",
        "",
        "definition-only.",
        "",
        "target-phase-envelope-design-only.",
        "",
        "projection-surface-only.",
        "",
        "constraint-field-only.",
        "",
        "converging-layer-only.",
        "",
        "inspection-only.",
        "",
        "P4-M4.4 Target Phase Envelope Contract is definition only.",
        "",
        "P4-M4.4 is target-phase-envelope-design-only.",
        "",
        "P4-M4.4 is projection-surface-only.",
        "",
        "P4-M4.4 is constraint-field-only.",
        "",
        "P4-M4.4 is converging-layer-only.",
        "",
        "P4-M4.3 Declared Human Context Envelope Contract remains the direct prior declared human context envelope reference.",
        "",
        "P4-M4.3 declared human context remains only an inherited weak prior reference.",
        "",
        "P4-M4.2 Evidence Reference Envelope Contract remains the inherited prior evidence reference envelope reference.",
        "",
        "P4-M4.1 Entry Gate Design Request Envelope Contract remains the inherited prior request envelope reference.",
        "",
        "P4-M4.0 Entry Gate Design Boundary Contract remains the inherited prior design boundary reference.",
        "",
        "P4-M3.16 Governed Transition Intake Final Phase Handoff Summary remains the inherited prior closed-phase handoff reference.",
        "",
        "P4-M3 static definition chain remains closed.",
        "",
        "P4-M4 design layer remains design-boundary-only.",
        "",
        "P4-M4 target phase envelope design starts only as a static future-state projection surface.",
        "",
        "P4-M4 target phase constraint field remains static definition only.",
        "",
    ]
    for prior_layer in DIRECT_PRIOR_DEFINITION_LAYER_REFERENCES:
        lines.extend([f"{prior_layer} remains a referenced definition layer.", ""])
    for prior_layer in INHERITED_PRIOR_DEFINITION_LAYER_REFERENCES:
        lines.extend([f"{prior_layer} remains an inherited referenced definition layer.", ""])
    for phrase in BOUNDARY_PHRASE_LINES:
        lines.extend([f"{phrase}.", ""])
    lines.extend([
        TARGET_PHASE_ENVELOPE_CONTRACT_BOUNDARY,
        "",
        "## Status Report",
        "",
    ])
    for key, value in status.items():
        lines.append(f"- {key}: {value}")
    lines.extend([
        "",
        "## Target Phase Envelope Contract Fields",
        "",
    ])
    for field in field_values:
        lines.extend([
            f"### {field.field_order}. {field.field_id}",
            "",
            f"- Field name: {field.field_name}",
            f"- Field purpose: {field.field_purpose}",
            "- P4-M4 target phase envelope contract category: "
            f"{field.p4_m4_target_phase_envelope_contract_category}",
            "- P4-M4 target phase envelope contract semantics disabled: "
            f"{field.p4_m4_target_phase_envelope_contract_semantics_disabled}",
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def target_phase_envelope_contract_as_dicts() -> tuple[dict[str, object], ...]:
    return tuple(asdict(field) for field in list_target_phase_envelope_contract_fields())


def target_phase_envelope_contract_report() -> dict[str, object]:
    status: dict[str, object] = {
        "phase": "P4-M4.4",
        "feature": "Target Phase Envelope Contract",
        "mode": "read-only",
        "boundary": TARGET_PHASE_ENVELOPE_CONTRACT_BOUNDARY,
        "package_version": P4_M4_4_PACKAGE_VERSION,
        "target_phase_envelope_contract_field_count": len(_FIELD_IDS),
        "referenced_p4_m4_3_declared_human_context_envelope_contract_field_count": len(
            declared_human_context_envelope_contract_field_ids()
        ),
    }
    status.update({flag: True for flag in TRUE_STATUS_FLAGS})
    status.update({flag: False for flag in FALSE_STATUS_FLAGS})
    return status
