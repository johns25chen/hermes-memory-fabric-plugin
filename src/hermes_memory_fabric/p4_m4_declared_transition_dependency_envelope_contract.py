from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence

from .p4_m4_declared_transition_constraint_envelope_contract import (
    declared_transition_constraint_envelope_contract_field_ids,
)


P4_M4_7_PACKAGE_VERSION = "6.16.0"


@dataclass(frozen=True)
class DeclaredTransitionDependencyEnvelopeContractField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    p4_m4_declared_transition_dependency_envelope_contract_category: str
    p4_m4_declared_transition_dependency_envelope_contract_semantics_disabled: str


DIRECT_PRIOR_DEFINITION_LAYER_REFERENCES = (
    "P4-M4.6 Declared Transition Constraint Envelope Contract",
)

INHERITED_PRIOR_DEFINITION_LAYER_REFERENCES = (
    "P4-M4.5 Declared Transition Reason Envelope Contract",
    "P4-M4.4 Target Phase Envelope Contract",
    "P4-M4.3 Declared Human Context Envelope Contract",
    "P4-M4.2 Evidence Reference Envelope Contract",
    "P4-M4.1 Entry Gate Design Request Envelope Contract",
    "P4-M4.0 Entry Gate Design Boundary Contract",
    "P4-M3.16 Governed Transition Intake Final Phase Handoff Summary",
)


BOUNDARY_PHRASE_LINES = tuple(
    line
    for line in """
P4-M4.7
Declared Transition Dependency Envelope Contract
read-only
definition-only
declared-transition-dependency-envelope-design-only
declared-dependency-surface-only
dependency-non-validation-boundary-only
dependency-non-resolution-boundary-only
dependency-non-graph-boundary-only
declaration-only
inspection-only
P4-M4.7 Declared Transition Dependency Envelope Contract is definition only
P4-M4.7 is read-only
P4-M4.7 is declared-transition-dependency-envelope-design-only
P4-M4.7 is declared-dependency-surface-only
P4-M4.7 is dependency-non-validation-boundary-only
P4-M4.7 is dependency-non-resolution-boundary-only
P4-M4.7 is dependency-non-graph-boundary-only
P4-M4.7 is declaration-only
P4-M4.7 is inspection-only
P4-M4.6 Declared Transition Constraint Envelope Contract remains the direct prior declared transition constraint envelope reference
P4-M4.6 declared transition constraint remains only an inherited static declared constraint surface reference
P4-M4.5 Declared Transition Reason Envelope Contract remains the inherited prior declared transition reason envelope reference
P4-M4.5 declared transition reason remains only an inherited static declared reason surface reference
P4-M4.4 Target Phase Envelope Contract remains the inherited prior target phase envelope reference
P4-M4.3 Declared Human Context Envelope Contract remains the inherited prior declared human context envelope reference
P4-M4.2 Evidence Reference Envelope Contract remains the inherited prior evidence reference envelope reference
P4-M4.1 Entry Gate Design Request Envelope Contract remains the inherited prior request envelope reference
P4-M4.0 Entry Gate Design Boundary Contract remains the inherited prior design boundary reference
P4-M3.16 Governed Transition Intake Final Phase Handoff Summary remains the inherited prior closed-phase handoff reference
P4-M3 static definition chain remains closed
P4-M4 design layer remains design-boundary-only
P4-M4 declared transition dependency envelope design starts only as a static declared dependency description surface
P4-M4 transition dependency validation remains not implemented
P4-M4 transition dependency resolution remains not implemented
P4-M4 transition dependency solving remains not implemented
P4-M4 dependency graph construction remains not implemented
P4-M4 dependency satisfaction validation remains not implemented
P4-M4 dependency violation detection remains not implemented
P4-M4 dependency sufficiency validation remains not implemented
P4-M4 dependency consistency validation remains not implemented
P4-M4 dependency integrity validation remains not implemented
P4-M4 transition dependency acceptance remains not implemented
P4-M4 transition dependency rejection remains not implemented
P4-M4 transition dependency scoring remains not implemented
P4-M4 transition dependency ranking remains not implemented
P4-M4 transition dependency recommendation remains not implemented
P4-M4 transition dependency generation remains not implemented
P4-M4 transition dependency justification remains not implemented
P4-M4 transition dependency routing remains not implemented
P4-M4 transition dependency planning remains not implemented
P4-M4 transition dependency execution remains not implemented
P4-M4 transition dependency record creation remains not implemented
P4-M4 dependency validation record creation remains not implemented
P4-M4 dependency resolution record creation remains not implemented
P4-M4 dependency graph record creation remains not implemented
P4-M4 dependency solving record creation remains not implemented
P4-M4 dependency scoring record creation remains not implemented
P4-M4 dependency routing record creation remains not implemented
P4-M4 dependency planning record creation remains not implemented
P4-M4 dependency justification record creation remains not implemented
P4-M4 transition constraint validation remains not implemented
P4-M4 transition constraint enforcement remains not implemented
P4-M4 transition constraint solving remains not implemented
P4-M4 transition constraint routing remains not implemented
P4-M4 transition constraint planning remains not implemented
P4-M4 transition constraint execution remains not implemented
P4-M4 transition reason validation remains not implemented
P4-M4 transition reason routing remains not implemented
P4-M4 transition reason planning remains not implemented
P4-M4 transition reason execution remains not implemented
P4-M4 target phase validation remains not implemented
P4-M4 phase transition validation remains not implemented
P4-M4 readiness scoring remains not implemented
P4-M4 state-space graph remains not implemented
P4-M4 transition graph remains not implemented
P4-M4 constraint graph remains not implemented
P4-M4 dependency graph remains not implemented
P4-M4 transition constraint to transition dependency mapping remains not implemented
P4-M4 transition reason to transition dependency mapping remains not implemented
P4-M4 target phase to transition dependency mapping remains not implemented
P4-M4 human context to transition dependency mapping remains not implemented
P4-M4 evidence validation remains not implemented
P4-M4 reference resolution remains not implemented
P4-M4 reference validation remains not implemented
P4-M4 citation validation remains not implemented
P4-M4 source fetching remains not implemented
P4-M4 provenance writing remains not implemented
P4-M4 request intake remains not implemented
P4-M4 request validation remains not implemented
P4-M4 execution remains not implemented
P4-M4 entry gate remains not implemented
P4-M4 entry gate validation remains not implemented
P4-M4 readiness validation remains not implemented
P4-M4 verdict generation remains not implemented
P4-M4 approval remains not implemented
P4-M4 authorization remains not implemented
P4-M4 confirmation remains not implemented
P4-M4 transition execution remains not implemented
P4-M5 remains not started
v7 remains not started
productization remains not started
UI remains not started
Operator Console remains not started
P4-M4.7 is not transition dependency intake
P4-M4.7 is not live transition dependency parsing
P4-M4.7 is not transition dependency validation
P4-M4.7 is not transition dependency resolution
P4-M4.7 is not transition dependency solving
P4-M4.7 is not dependency graph construction
P4-M4.7 is not dependency satisfaction validation
P4-M4.7 is not dependency violation detection
P4-M4.7 is not dependency sufficiency validation
P4-M4.7 is not dependency consistency validation
P4-M4.7 is not dependency integrity validation
P4-M4.7 is not transition dependency acceptance
P4-M4.7 is not transition dependency rejection
P4-M4.7 is not transition dependency scoring
P4-M4.7 is not transition dependency ranking
P4-M4.7 is not transition dependency recommendation
P4-M4.7 is not transition dependency generation
P4-M4.7 is not transition dependency justification
P4-M4.7 is not transition dependency routing
P4-M4.7 is not transition dependency planning
P4-M4.7 is not transition dependency execution
P4-M4.7 is not transition dependency record creation
P4-M4.7 is not dependency validation record creation
P4-M4.7 is not dependency resolution record creation
P4-M4.7 is not dependency graph record creation
P4-M4.7 is not dependency solving record creation
P4-M4.7 is not dependency scoring record creation
P4-M4.7 is not dependency routing record creation
P4-M4.7 is not dependency planning record creation
P4-M4.7 is not dependency justification record creation
P4-M4.7 is not transition constraint validation
P4-M4.7 is not transition constraint enforcement
P4-M4.7 is not transition constraint solving
P4-M4.7 is not transition constraint routing
P4-M4.7 is not transition constraint planning
P4-M4.7 is not transition constraint execution
P4-M4.7 is not transition reason validation
P4-M4.7 is not transition reason routing
P4-M4.7 is not transition reason planning
P4-M4.7 is not transition reason execution
P4-M4.7 is not target phase validation
P4-M4.7 is not phase transition validation
P4-M4.7 is not readiness scoring
P4-M4.7 is not target phase routing
P4-M4.7 is not transition planning
P4-M4.7 is not path planning
P4-M4.7 is not state-space graph
P4-M4.7 is not transition graph
P4-M4.7 is not constraint graph
P4-M4.7 is not dependency graph
P4-M4.7 is not transition constraint to transition dependency mapping
P4-M4.7 is not transition reason to transition dependency mapping
P4-M4.7 is not target phase to transition dependency mapping
P4-M4.7 is not human context to transition dependency mapping
P4-M4.7 is not evidence validation
P4-M4.7 is not reference resolution
P4-M4.7 is not reference validation
P4-M4.7 is not citation validation
P4-M4.7 is not source fetching
P4-M4.7 is not provenance writing
P4-M4.7 is not request intake
P4-M4.7 is not request validation
P4-M4.7 is not entry gate validation
P4-M4.7 is not readiness validation
P4-M4.7 is not a working entry gate
P4-M4.7 is not gate activation
P4-M4.7 is not gate execution
P4-M4.7 is not readiness verdict
P4-M4.7 is not validation verdict
P4-M4.7 is not transition dependency verdict
P4-M4.7 is not transition verdict
P4-M4.7 is not approval
P4-M4.7 is not authorization
P4-M4.7 is not confirmation
P4-M4.7 is not recommendation
P4-M4.7 is not ranking
P4-M4.7 is not next action generation
P4-M4.7 is not transition execution
P4-M4.7 is not record creation
P4-M4.7 is not memory mutation
P4-M4.7 is not roadmap mutation
no transition dependency intake
no live transition dependency parsing
no transition dependency validation
no transition dependency resolution
no transition dependency solving
no dependency graph construction
no dependency satisfaction validation
no dependency violation detection
no dependency sufficiency validation
no dependency consistency validation
no dependency integrity validation
no transition dependency acceptance
no transition dependency rejection
no transition dependency scoring
no transition dependency ranking
no transition dependency recommendation
no transition dependency generation
no transition dependency justification
no transition dependency routing
no transition dependency planning
no transition dependency execution
no transition dependency record creation
no dependency validation record creation
no dependency resolution record creation
no dependency graph record creation
no dependency solving record creation
no dependency scoring record creation
no dependency routing record creation
no dependency planning record creation
no dependency justification record creation
no transition constraint validation
no transition constraint enforcement
no transition constraint solving
no transition constraint routing
no transition constraint planning
no transition constraint execution
no transition reason validation
no transition reason routing
no transition reason planning
no transition reason execution
no target phase validation
no phase transition validation
no readiness scoring
no target phase routing
no transition planning
no path planning
no state-space graph
no transition graph
no constraint graph
no dependency graph
no transition constraint to transition dependency mapping
no transition reason to transition dependency mapping
no target phase to transition dependency mapping
no human context to transition dependency mapping
no evidence validation
no reference resolution
no reference validation
no citation validation
no source fetching
no provenance writing
no request intake
no request validation
no entry gate validation
no readiness validation
no working entry gate
no gate activation
no gate execution
no readiness verdict
no validation verdict
no transition dependency verdict
no transition verdict
no approval
no authorization
no confirmation
no recommendation
no ranking
no next action generation
no transition execution
no record creation
no memory mutation
no roadmap mutation
no P4-M5
no v7
no productization
no UI
no Operator Console
no MVP
no deploy
no full Memory Graph
no version bump
no tag
""".splitlines()
    if line
)


TRUE_STATUS_FLAGS = tuple(
    line
    for line in """
definition_only
declared_transition_dependency_envelope_design_only
declared_dependency_surface_only
dependency_non_validation_boundary_only
dependency_non_resolution_boundary_only
dependency_non_graph_boundary_only
declaration_only
inspection_only
p4_m4_7_declared_transition_dependency_envelope_contract_started
p4_m4_7_definition_only
p4_m4_7_declared_transition_dependency_envelope_design_only
p4_m4_7_declared_dependency_surface_only
p4_m4_7_dependency_non_validation_boundary_only
p4_m4_7_dependency_non_resolution_boundary_only
p4_m4_7_dependency_non_graph_boundary_only
p4_m4_7_declaration_only
p4_m4_6_declared_transition_constraint_envelope_contract_reference_defined
p4_m4_6_declared_transition_constraint_static_reference_defined
p4_m4_5_declared_transition_reason_envelope_contract_reference_defined
p4_m4_5_declared_transition_reason_static_reference_defined
p4_m4_4_target_phase_envelope_contract_reference_defined
p4_m4_3_declared_human_context_envelope_contract_reference_defined
p4_m4_2_evidence_reference_envelope_contract_reference_defined
p4_m4_1_entry_gate_design_request_envelope_contract_reference_defined
p4_m4_0_entry_gate_design_boundary_contract_reference_defined
p4_m3_16_final_phase_handoff_summary_reference_defined
p4_m3_static_definition_chain_closed_reference_defined
p4_m4_design_boundary_reference_defined
p4_m4_declared_transition_dependency_envelope_design_defined
p4_m4_declared_dependency_surface_defined
p4_m4_transition_dependency_non_validation_boundary_defined
p4_m4_transition_dependency_non_resolution_boundary_defined
p4_m4_transition_dependency_non_graph_boundary_defined
p4_m4_transition_dependency_non_solving_boundary_defined
p4_m4_transition_dependency_non_acceptance_boundary_defined
p4_m4_transition_dependency_non_rejection_boundary_defined
p4_m4_transition_dependency_non_scoring_boundary_defined
p4_m4_transition_dependency_non_routing_boundary_defined
p4_m4_transition_dependency_non_planning_boundary_defined
p4_m4_transition_dependency_non_execution_boundary_defined
p4_m4_transition_dependency_validation_semantics_prohibited
p4_m4_dependency_resolution_semantics_prohibited
p4_m4_dependency_graph_semantics_prohibited
p4_m4_dependency_solving_semantics_prohibited
p4_m4_dependency_satisfaction_validation_semantics_prohibited
p4_m4_dependency_violation_detection_semantics_prohibited
p4_m4_dependency_sufficiency_validation_semantics_prohibited
p4_m4_dependency_consistency_validation_semantics_prohibited
p4_m4_dependency_integrity_validation_semantics_prohibited
p4_m4_dependency_justification_semantics_prohibited
p4_m4_routing_semantics_prohibited
p4_m4_planning_semantics_prohibited
p4_m4_verdict_semantics_prohibited
p4_m4_execution_semantics_prohibited
p4_m4_record_creation_semantics_prohibited
p4_m4_mutation_semantics_prohibited
p4_m5_start_deferred
v7_start_deferred
productization_deferred
ui_deferred
operator_console_deferred
""".splitlines()
    if line
)


FALSE_STATUS_FLAGS = tuple(
    line
    for line in """
live_validation_enabled
transition_dependency_intake_enabled
live_transition_dependency_parsing_enabled
transition_dependency_validation_enabled
transition_dependency_resolution_enabled
transition_dependency_solving_enabled
dependency_graph_construction_enabled
dependency_satisfaction_validation_enabled
dependency_violation_detection_enabled
dependency_sufficiency_validation_enabled
dependency_consistency_validation_enabled
dependency_integrity_validation_enabled
transition_dependency_acceptance_enabled
transition_dependency_rejection_enabled
transition_dependency_scoring_enabled
transition_dependency_ranking_enabled
transition_dependency_recommendation_enabled
transition_dependency_generation_enabled
transition_dependency_justification_enabled
transition_dependency_routing_enabled
transition_dependency_planning_enabled
transition_dependency_execution_enabled
transition_dependency_record_creation_enabled
dependency_validation_record_creation_enabled
dependency_resolution_record_creation_enabled
dependency_graph_record_creation_enabled
dependency_solving_record_creation_enabled
dependency_scoring_record_creation_enabled
dependency_routing_record_creation_enabled
dependency_planning_record_creation_enabled
dependency_justification_record_creation_enabled
transition_constraint_validation_enabled
transition_constraint_enforcement_enabled
transition_constraint_solving_enabled
transition_constraint_routing_enabled
transition_constraint_planning_enabled
transition_constraint_execution_enabled
transition_reason_validation_enabled
transition_reason_routing_enabled
transition_reason_planning_enabled
transition_reason_execution_enabled
target_phase_validation_enabled
phase_transition_validation_enabled
phase_readiness_validation_enabled
target_phase_readiness_validation_enabled
readiness_scoring_enabled
target_phase_scoring_enabled
target_phase_routing_enabled
target_phase_execution_enabled
transition_planning_enabled
path_planning_enabled
state_space_graph_enabled
transition_graph_enabled
constraint_graph_enabled
dependency_graph_enabled
semantic_target_field_graph_enabled
transition_constraint_to_transition_dependency_mapping_enabled
transition_reason_to_transition_dependency_mapping_enabled
target_phase_to_transition_dependency_mapping_enabled
human_context_to_transition_dependency_mapping_enabled
human_context_intake_enabled
live_human_context_parsing_enabled
human_context_validation_enabled
identity_validation_enabled
actor_validation_enabled
user_validation_enabled
operator_validation_enabled
consent_validation_enabled
authority_validation_enabled
approval_validation_enabled
authorization_validation_enabled
confirmation_validation_enabled
human_context_record_creation_enabled
evidence_intake_enabled
live_evidence_parsing_enabled
evidence_validation_enabled
evidence_record_creation_enabled
reference_resolution_enabled
reference_validation_enabled
reference_integrity_validation_enabled
citation_validation_enabled
source_fetching_enabled
provenance_writing_enabled
request_intake_enabled
live_request_parsing_enabled
request_validation_enabled
request_acceptance_enabled
request_rejection_enabled
request_routing_enabled
request_execution_enabled
request_record_creation_enabled
boundary_validation_enabled
phase_validation_enabled
entry_gate_validation_enabled
entry_readiness_validation_enabled
readiness_validation_enabled
transition_readiness_validation_enabled
transition_validation_enabled
governed_transition_intake_validation_enabled
package_validation_enabled
closure_validation_enabled
handoff_validation_enabled
final_phase_handoff_validation_enabled
working_entry_gate_enabled
gate_activation_enabled
gate_execution_enabled
p4_m4_execution_enabled
operational_behavior_enabled
readiness_verdict_enabled
validation_verdict_enabled
transition_dependency_verdict_enabled
transition_verdict_enabled
human_context_verdict_enabled
evidence_verdict_enabled
reference_verdict_enabled
citation_verdict_enabled
entry_verdict_enabled
gate_verdict_enabled
approval_enabled
authorization_enabled
confirmation_enabled
recommendation_enabled
ranking_enabled
next_action_generation_enabled
transition_execution_enabled
command_execution_enabled
record_creation_enabled
persistence_enabled
storage_enabled
memory_mutation_enabled
roadmap_mutation_enabled
lifecycle_mutation_enabled
proposal_mutation_enabled
transition_dependency_mutation_enabled
transition_constraint_mutation_enabled
transition_reason_mutation_enabled
target_phase_mutation_enabled
phase_mutation_enabled
transition_mutation_enabled
human_context_mutation_enabled
evidence_mutation_enabled
api_enabled
mcp_enabled
connector_enabled
agent_call_enabled
p4_m5_started
v7_started
productization_started
ui_started
operator_console_started
mvp_started
deploy_started
full_memory_graph_started
version_bump_enabled
tag_creation_enabled
""".splitlines()
    if line
)


DECLARED_TRANSITION_DEPENDENCY_ENVELOPE_CONTRACT_BOUNDARY = (
    "P4-M4.7 Declared Transition Dependency Envelope Contract read-only "
    "definition-only declared-transition-dependency-envelope-design-only "
    "declared-dependency-surface-only dependency-non-validation-boundary-only "
    "dependency-non-resolution-boundary-only dependency-non-graph-boundary-only "
    "declaration-only inspection-only. P4-M4.7 Declared Transition Dependency "
    "Envelope Contract is definition only. "
    + " ".join(f"{phrase}." for phrase in BOUNDARY_PHRASE_LINES)
)


_FIELD_IDS = (
    "p4-m4-declared-transition-dependency-envelope-contract-id",
    "p4-m4-declared-transition-dependency-envelope-contract-phase",
    "p4-m4-declared-transition-dependency-envelope-contract-mode",
    "p4-m4-declared-transition-dependency-envelope-contract-direct-prior-declared-transition-constraint-envelope-reference",
    "p4-m4-declared-transition-dependency-envelope-contract-inherited-prior-declared-transition-reason-envelope-reference",
    "p4-m4-declared-transition-dependency-envelope-contract-inherited-prior-target-phase-envelope-reference",
    "p4-m4-declared-transition-dependency-envelope-contract-inherited-prior-declared-human-context-envelope-reference",
    "p4-m4-declared-transition-dependency-envelope-contract-inherited-prior-evidence-reference-envelope-reference",
    "p4-m4-declared-transition-dependency-envelope-contract-inherited-prior-request-envelope-reference",
    "p4-m4-declared-transition-dependency-envelope-contract-inherited-prior-boundary-reference",
    "p4-m4-declared-transition-dependency-envelope-contract-inherited-prior-handoff-reference",
    "p4-m4-declared-transition-dependency-envelope-contract-scope",
    "p4-m4-declared-transition-dependency-envelope-contract-declared-transition-dependency-envelope-design-only",
    "p4-m4-declared-transition-dependency-envelope-contract-declared-dependency-surface-definition",
    "p4-m4-declared-transition-dependency-envelope-contract-dependency-non-validation-boundary-definition",
    "p4-m4-declared-transition-dependency-envelope-contract-dependency-non-resolution-boundary-definition",
    "p4-m4-declared-transition-dependency-envelope-contract-dependency-non-graph-boundary-definition",
    "p4-m4-declared-transition-dependency-envelope-contract-declaration-only-semantics-definition",
    "p4-m4-declared-transition-dependency-envelope-contract-declared-transition-constraint-static-reference-definition",
    "p4-m4-declared-transition-dependency-envelope-contract-dependency-validation-resolution-graph-semantics-disabled",
    "p4-m4-declared-transition-dependency-envelope-contract-routing-planning-execution-scoring-justification-semantics-disabled",
    "p4-m4-declared-transition-dependency-envelope-contract-p4-m5-v7-productization-ui-deferred",
)


def _field_purpose(field_id: str) -> str:
    return (
        f"Defines {field_id} as read-only definition-only "
        "declared-transition-dependency-envelope-design-only "
        "declared-dependency-surface-only dependency-non-validation-boundary-only "
        "dependency-non-resolution-boundary-only dependency-non-graph-boundary-only "
        "declaration-only inspection-only P4-M4.7 Declared Transition Dependency "
        "Envelope Contract context; P4-M4.6 Declared Transition Constraint "
        "Envelope Contract remains the direct prior declared transition constraint "
        "envelope reference; P4-M4.6 declared transition constraint remains only "
        "an inherited static declared constraint surface reference; P4-M4.5 "
        "declared transition reason remains only an inherited static declared "
        "reason surface reference; P4-M4 declared transition dependency envelope "
        "design starts only as a static declared dependency description surface; "
        "no transition dependency intake; no live transition dependency parsing; "
        "no transition dependency validation; no transition dependency resolution; "
        "no transition dependency solving; no dependency graph construction; no "
        "dependency satisfaction validation; no dependency violation detection; "
        "no dependency sufficiency validation; no dependency consistency "
        "validation; no dependency integrity validation; no transition dependency "
        "acceptance; no transition dependency rejection; no transition dependency "
        "scoring; no transition dependency ranking; no transition dependency "
        "recommendation; no transition dependency generation; no transition "
        "dependency justification; no transition dependency routing; no "
        "transition dependency planning; no transition dependency execution; no "
        "transition constraint to transition dependency mapping; no transition "
        "reason to transition dependency mapping; no target phase to transition "
        "dependency mapping; no human context to transition dependency mapping; "
        "no evidence validation; no reference resolution; no reference validation; "
        "no citation validation; no source fetching; no provenance writing; no "
        "request intake; no request validation; no working entry gate; no "
        "transition execution; no record creation; no memory mutation; no roadmap "
        "mutation; no P4-M5; no v7; no productization; no UI; no Operator "
        "Console; no version bump; no tag."
    )


_DECLARED_TRANSITION_DEPENDENCY_ENVELOPE_CONTRACT_FIELDS = tuple(
    DeclaredTransitionDependencyEnvelopeContractField(
        index,
        field_id,
        f"P4-M4 Declared Transition Dependency Envelope Contract Field {index}",
        _field_purpose(field_id),
        "p4-m4-declared-transition-dependency-envelope-contract-category",
        (
            "no transition dependency intake semantics; no live transition "
            "dependency parsing semantics; no transition dependency validation "
            "semantics; no transition dependency resolution semantics; no "
            "transition dependency solving semantics; no dependency graph "
            "construction semantics; no dependency satisfaction validation "
            "semantics; no dependency violation detection semantics; no "
            "transition dependency acceptance semantics; no transition dependency "
            "rejection semantics; no transition dependency scoring semantics; no "
            "transition dependency routing semantics; no transition dependency "
            "planning semantics; no transition dependency execution semantics; no "
            "transition constraint to transition dependency mapping semantics; no "
            "transition reason to transition dependency mapping semantics; no "
            "target phase to transition dependency mapping semantics; no human "
            "context to transition dependency mapping semantics; no evidence "
            "validation semantics; no reference resolution semantics; no reference "
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


def list_declared_transition_dependency_envelope_contract_fields() -> tuple[
    DeclaredTransitionDependencyEnvelopeContractField, ...
]:
    return _DECLARED_TRANSITION_DEPENDENCY_ENVELOPE_CONTRACT_FIELDS


def declared_transition_dependency_envelope_contract_field_ids() -> tuple[str, ...]:
    return tuple(
        field.field_id
        for field in list_declared_transition_dependency_envelope_contract_fields()
    )


def render_declared_transition_dependency_envelope_contract_markdown(
    fields: Sequence[DeclaredTransitionDependencyEnvelopeContractField] | None = None,
) -> str:
    field_values = (
        tuple(fields)
        if fields is not None
        else list_declared_transition_dependency_envelope_contract_fields()
    )
    status = declared_transition_dependency_envelope_contract_report()
    lines = [
        "# P4-M4.7 Declared Transition Dependency Envelope Contract",
        "",
        "P4-M4.7 Declared Transition Dependency Envelope Contract.",
        "",
        "read-only.",
        "",
        "definition-only.",
        "",
        "declared-transition-dependency-envelope-design-only.",
        "",
        "declared-dependency-surface-only.",
        "",
        "dependency-non-validation-boundary-only.",
        "",
        "dependency-non-resolution-boundary-only.",
        "",
        "dependency-non-graph-boundary-only.",
        "",
        "declaration-only.",
        "",
        "inspection-only.",
        "",
        "P4-M4.7 Declared Transition Dependency Envelope Contract is definition only.",
        "",
        "P4-M4.7 is declared-transition-dependency-envelope-design-only.",
        "",
        "P4-M4.7 is declared-dependency-surface-only.",
        "",
        "P4-M4.7 is dependency-non-validation-boundary-only.",
        "",
        "P4-M4.7 is dependency-non-resolution-boundary-only.",
        "",
        "P4-M4.7 is dependency-non-graph-boundary-only.",
        "",
        "P4-M4.7 is declaration-only.",
        "",
        "P4-M4.6 Declared Transition Constraint Envelope Contract remains the direct prior declared transition constraint envelope reference.",
        "",
        "P4-M4.6 declared transition constraint remains only an inherited static declared constraint surface reference.",
        "",
    ]
    for prior_layer in DIRECT_PRIOR_DEFINITION_LAYER_REFERENCES:
        lines.extend([f"{prior_layer} remains a referenced definition layer.", ""])
    for prior_layer in INHERITED_PRIOR_DEFINITION_LAYER_REFERENCES:
        lines.extend([f"{prior_layer} remains an inherited referenced definition layer.", ""])
    for phrase in BOUNDARY_PHRASE_LINES:
        lines.extend([f"{phrase}.", ""])
    lines.extend([
        DECLARED_TRANSITION_DEPENDENCY_ENVELOPE_CONTRACT_BOUNDARY,
        "",
        "## Status Report",
        "",
    ])
    for key, value in status.items():
        lines.append(f"- {key}: {value}")
    lines.extend([
        "",
        "## Declared Transition Dependency Envelope Contract Fields",
        "",
    ])
    for field in field_values:
        lines.extend([
            f"### {field.field_order}. {field.field_id}",
            "",
            f"- Field name: {field.field_name}",
            f"- Field purpose: {field.field_purpose}",
            "- P4-M4 declared transition dependency envelope contract category: "
            f"{field.p4_m4_declared_transition_dependency_envelope_contract_category}",
            "- P4-M4 declared transition dependency envelope contract semantics disabled: "
            f"{field.p4_m4_declared_transition_dependency_envelope_contract_semantics_disabled}",
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def declared_transition_dependency_envelope_contract_as_dicts() -> tuple[
    dict[str, object], ...
]:
    return tuple(
        asdict(field)
        for field in list_declared_transition_dependency_envelope_contract_fields()
    )


def declared_transition_dependency_envelope_contract_report() -> dict[str, object]:
    status: dict[str, object] = {
        "phase": "P4-M4.7",
        "feature": "Declared Transition Dependency Envelope Contract",
        "mode": "read-only",
        "boundary": DECLARED_TRANSITION_DEPENDENCY_ENVELOPE_CONTRACT_BOUNDARY,
        "package_version": P4_M4_7_PACKAGE_VERSION,
        "declared_transition_dependency_envelope_contract_field_count": len(_FIELD_IDS),
        "referenced_p4_m4_6_declared_transition_constraint_envelope_contract_field_count": len(
            declared_transition_constraint_envelope_contract_field_ids()
        ),
    }
    status.update({flag: True for flag in TRUE_STATUS_FLAGS})
    status.update({flag: False for flag in FALSE_STATUS_FLAGS})
    return status
