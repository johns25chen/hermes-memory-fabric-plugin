from __future__ import annotations

import argparse
import io
import json
import tomllib
from pathlib import Path

from hermes_memory_fabric.p4_m0_subspace_operator import build_parser, run_operator_command
from hermes_memory_fabric.p4_m4_declared_transition_constraint_envelope_contract import (
    BOUNDARY_PHRASE_LINES,
    DECLARED_TRANSITION_CONSTRAINT_ENVELOPE_CONTRACT_BOUNDARY,
    FALSE_STATUS_FLAGS,
    TRUE_STATUS_FLAGS,
    DeclaredTransitionConstraintEnvelopeContractField,
    declared_transition_constraint_envelope_contract_as_dicts,
    declared_transition_constraint_envelope_contract_field_ids,
    declared_transition_constraint_envelope_contract_report,
    list_declared_transition_constraint_envelope_contract_fields,
    render_declared_transition_constraint_envelope_contract_markdown,
)


FIELD_IDS = (
    "p4-m4-declared-transition-constraint-envelope-contract-id",
    "p4-m4-declared-transition-constraint-envelope-contract-phase",
    "p4-m4-declared-transition-constraint-envelope-contract-mode",
    "p4-m4-declared-transition-constraint-envelope-contract-direct-prior-declared-transition-reason-envelope-reference",
    "p4-m4-declared-transition-constraint-envelope-contract-inherited-prior-target-phase-envelope-reference",
    "p4-m4-declared-transition-constraint-envelope-contract-inherited-prior-declared-human-context-envelope-reference",
    "p4-m4-declared-transition-constraint-envelope-contract-inherited-prior-evidence-reference-envelope-reference",
    "p4-m4-declared-transition-constraint-envelope-contract-inherited-prior-request-envelope-reference",
    "p4-m4-declared-transition-constraint-envelope-contract-inherited-prior-boundary-reference",
    "p4-m4-declared-transition-constraint-envelope-contract-inherited-prior-handoff-reference",
    "p4-m4-declared-transition-constraint-envelope-contract-scope",
    "p4-m4-declared-transition-constraint-envelope-contract-declared-transition-constraint-envelope-design-only",
    "p4-m4-declared-transition-constraint-envelope-contract-declared-constraint-surface-definition",
    "p4-m4-declared-transition-constraint-envelope-contract-constraint-non-validation-boundary-definition",
    "p4-m4-declared-transition-constraint-envelope-contract-constraint-non-enforcement-boundary-definition",
    "p4-m4-declared-transition-constraint-envelope-contract-declaration-only-semantics-definition",
    "p4-m4-declared-transition-constraint-envelope-contract-declared-transition-reason-static-reference-definition",
    "p4-m4-declared-transition-constraint-envelope-contract-constraint-validation-enforcement-solving-semantics-disabled",
    "p4-m4-declared-transition-constraint-envelope-contract-routing-planning-execution-scoring-justification-semantics-disabled",
    "p4-m4-declared-transition-constraint-envelope-contract-p4-m5-v7-productization-ui-deferred",
)

DATACLASS_FIELDS = {
    "field_order",
    "field_id",
    "field_name",
    "field_purpose",
    "p4_m4_declared_transition_constraint_envelope_contract_category",
    "p4_m4_declared_transition_constraint_envelope_contract_semantics_disabled",
}

REQUIRED_BOUNDARY_PHRASES = tuple(
    line
    for line in """
P4-M4.6
Declared Transition Constraint Envelope Contract
read-only
definition-only
declared-transition-constraint-envelope-design-only
declared-constraint-surface-only
constraint-non-validation-boundary-only
constraint-non-enforcement-boundary-only
declaration-only
inspection-only
P4-M4.6 Declared Transition Constraint Envelope Contract is definition only
P4-M4.6 is declared-transition-constraint-envelope-design-only
P4-M4.6 is declared-constraint-surface-only
P4-M4.6 is constraint-non-validation-boundary-only
P4-M4.6 is constraint-non-enforcement-boundary-only
P4-M4.6 is declaration-only
P4-M4.5 Declared Transition Reason Envelope Contract remains the direct prior declared transition reason envelope reference
P4-M4.5 declared transition reason remains only an inherited static declared reason surface reference
P4-M4.4 Target Phase Envelope Contract remains the inherited prior target phase envelope reference
P4-M4.3 Declared Human Context Envelope Contract remains the inherited prior declared human context envelope reference
P4-M4.2 Evidence Reference Envelope Contract remains the inherited prior evidence reference envelope reference
P4-M4.1 Entry Gate Design Request Envelope Contract remains the inherited prior request envelope reference
P4-M4.0 Entry Gate Design Boundary Contract remains the inherited prior design boundary reference
P4-M3.16 Governed Transition Intake Final Phase Handoff Summary remains the inherited prior closed-phase handoff reference
P4-M3 static definition chain remains closed
P4-M4 design layer remains design-boundary-only
P4-M4 declared transition constraint envelope design starts only as a static declared constraint description surface
P4-M4 transition constraint validation remains not implemented
P4-M4 transition constraint enforcement remains not implemented
P4-M4 transition constraint solving remains not implemented
P4-M4 constraint satisfaction validation remains not implemented
P4-M4 constraint violation detection remains not implemented
P4-M4 constraint sufficiency validation remains not implemented
P4-M4 constraint consistency validation remains not implemented
P4-M4 constraint integrity validation remains not implemented
P4-M4 transition constraint acceptance remains not implemented
P4-M4 transition constraint rejection remains not implemented
P4-M4 transition constraint scoring remains not implemented
P4-M4 transition constraint ranking remains not implemented
P4-M4 transition constraint recommendation remains not implemented
P4-M4 transition constraint generation remains not implemented
P4-M4 transition constraint justification remains not implemented
P4-M4 transition constraint routing remains not implemented
P4-M4 transition constraint planning remains not implemented
P4-M4 transition constraint execution remains not implemented
P4-M4 transition constraint record creation remains not implemented
P4-M4 constraint validation record creation remains not implemented
P4-M4 constraint enforcement record creation remains not implemented
P4-M4 constraint solving record creation remains not implemented
P4-M4 constraint scoring record creation remains not implemented
P4-M4 constraint routing record creation remains not implemented
P4-M4 constraint planning record creation remains not implemented
P4-M4 constraint justification record creation remains not implemented
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
P4-M4 transition reason to transition constraint mapping remains not implemented
P4-M4 target phase to transition constraint mapping remains not implemented
P4-M4 human context to transition constraint mapping remains not implemented
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
P4-M4.6 is not transition constraint intake
P4-M4.6 is not live transition constraint parsing
P4-M4.6 is not transition constraint validation
P4-M4.6 is not transition constraint enforcement
P4-M4.6 is not transition constraint solving
P4-M4.6 is not constraint satisfaction validation
P4-M4.6 is not constraint violation detection
P4-M4.6 is not constraint sufficiency validation
P4-M4.6 is not constraint consistency validation
P4-M4.6 is not constraint integrity validation
P4-M4.6 is not transition constraint acceptance
P4-M4.6 is not transition constraint rejection
P4-M4.6 is not transition constraint scoring
P4-M4.6 is not transition constraint ranking
P4-M4.6 is not transition constraint recommendation
P4-M4.6 is not transition constraint generation
P4-M4.6 is not transition constraint justification
P4-M4.6 is not transition constraint routing
P4-M4.6 is not transition constraint planning
P4-M4.6 is not transition constraint execution
P4-M4.6 is not transition constraint record creation
P4-M4.6 is not constraint validation record creation
P4-M4.6 is not constraint enforcement record creation
P4-M4.6 is not constraint solving record creation
P4-M4.6 is not constraint scoring record creation
P4-M4.6 is not constraint routing record creation
P4-M4.6 is not constraint planning record creation
P4-M4.6 is not constraint justification record creation
P4-M4.6 is not transition reason validation
P4-M4.6 is not transition reason routing
P4-M4.6 is not transition reason planning
P4-M4.6 is not transition reason execution
P4-M4.6 is not target phase validation
P4-M4.6 is not phase transition validation
P4-M4.6 is not readiness scoring
P4-M4.6 is not target phase routing
P4-M4.6 is not transition planning
P4-M4.6 is not path planning
P4-M4.6 is not state-space graph
P4-M4.6 is not transition graph
P4-M4.6 is not constraint graph
P4-M4.6 is not transition reason to transition constraint mapping
P4-M4.6 is not target phase to transition constraint mapping
P4-M4.6 is not human context to transition constraint mapping
P4-M4.6 is not evidence validation
P4-M4.6 is not reference resolution
P4-M4.6 is not reference validation
P4-M4.6 is not citation validation
P4-M4.6 is not source fetching
P4-M4.6 is not provenance writing
P4-M4.6 is not request intake
P4-M4.6 is not request validation
P4-M4.6 is not entry gate validation
P4-M4.6 is not readiness validation
P4-M4.6 is not a working entry gate
P4-M4.6 is not gate activation
P4-M4.6 is not gate execution
P4-M4.6 is not readiness verdict
P4-M4.6 is not validation verdict
P4-M4.6 is not transition constraint verdict
P4-M4.6 is not transition verdict
P4-M4.6 is not approval
P4-M4.6 is not authorization
P4-M4.6 is not confirmation
P4-M4.6 is not recommendation
P4-M4.6 is not ranking
P4-M4.6 is not next action generation
P4-M4.6 is not transition execution
P4-M4.6 is not record creation
P4-M4.6 is not memory mutation
P4-M4.6 is not roadmap mutation
no transition constraint intake
no live transition constraint parsing
no transition constraint validation
no transition constraint enforcement
no transition constraint solving
no constraint satisfaction validation
no constraint violation detection
no constraint sufficiency validation
no constraint consistency validation
no constraint integrity validation
no transition constraint acceptance
no transition constraint rejection
no transition constraint scoring
no transition constraint ranking
no transition constraint recommendation
no transition constraint generation
no transition constraint justification
no transition constraint routing
no transition constraint planning
no transition constraint execution
no transition constraint record creation
no constraint validation record creation
no constraint enforcement record creation
no constraint solving record creation
no constraint scoring record creation
no constraint routing record creation
no constraint planning record creation
no constraint justification record creation
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
no transition reason to transition constraint mapping
no target phase to transition constraint mapping
no human context to transition constraint mapping
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
no transition constraint verdict
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

EXPECTED_TRUE_STATUS_FLAGS = tuple(
    line
    for line in """
definition_only
declared_transition_constraint_envelope_design_only
declared_constraint_surface_only
constraint_non_validation_boundary_only
constraint_non_enforcement_boundary_only
declaration_only
inspection_only
p4_m4_6_declared_transition_constraint_envelope_contract_started
p4_m4_6_definition_only
p4_m4_6_declared_transition_constraint_envelope_design_only
p4_m4_6_declared_constraint_surface_only
p4_m4_6_constraint_non_validation_boundary_only
p4_m4_6_constraint_non_enforcement_boundary_only
p4_m4_6_declaration_only
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
p4_m4_declared_transition_constraint_envelope_design_defined
p4_m4_declared_constraint_surface_defined
p4_m4_transition_constraint_non_validation_boundary_defined
p4_m4_transition_constraint_non_enforcement_boundary_defined
p4_m4_transition_constraint_non_solving_boundary_defined
p4_m4_transition_constraint_non_acceptance_boundary_defined
p4_m4_transition_constraint_non_rejection_boundary_defined
p4_m4_transition_constraint_non_scoring_boundary_defined
p4_m4_transition_constraint_non_routing_boundary_defined
p4_m4_transition_constraint_non_planning_boundary_defined
p4_m4_transition_constraint_non_execution_boundary_defined
p4_m4_transition_constraint_validation_semantics_prohibited
p4_m4_constraint_enforcement_semantics_prohibited
p4_m4_constraint_solving_semantics_prohibited
p4_m4_constraint_satisfaction_validation_semantics_prohibited
p4_m4_constraint_violation_detection_semantics_prohibited
p4_m4_constraint_sufficiency_validation_semantics_prohibited
p4_m4_constraint_consistency_validation_semantics_prohibited
p4_m4_constraint_integrity_validation_semantics_prohibited
p4_m4_constraint_justification_semantics_prohibited
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

EXPECTED_FALSE_STATUS_FLAGS = tuple(
    line
    for line in """
live_validation_enabled
transition_constraint_intake_enabled
live_transition_constraint_parsing_enabled
transition_constraint_validation_enabled
transition_constraint_enforcement_enabled
transition_constraint_solving_enabled
constraint_satisfaction_validation_enabled
constraint_violation_detection_enabled
constraint_sufficiency_validation_enabled
constraint_consistency_validation_enabled
constraint_integrity_validation_enabled
transition_constraint_acceptance_enabled
transition_constraint_rejection_enabled
transition_constraint_scoring_enabled
transition_constraint_ranking_enabled
transition_constraint_recommendation_enabled
transition_constraint_generation_enabled
transition_constraint_justification_enabled
transition_constraint_routing_enabled
transition_constraint_planning_enabled
transition_constraint_execution_enabled
transition_constraint_record_creation_enabled
constraint_validation_record_creation_enabled
constraint_enforcement_record_creation_enabled
constraint_solving_record_creation_enabled
constraint_scoring_record_creation_enabled
constraint_routing_record_creation_enabled
constraint_planning_record_creation_enabled
constraint_justification_record_creation_enabled
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
semantic_target_field_graph_enabled
transition_reason_to_transition_constraint_mapping_enabled
target_phase_to_transition_constraint_mapping_enabled
human_context_to_transition_constraint_mapping_enabled
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
transition_constraint_verdict_enabled
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
    "declared-transition-package-assembly-envelope-contract",
    "entry-gate-design-final-non-validation-boundary-audit",
    "entry-gate-design-closure-handoff-contract",
    "entry-gate-design-phase-closure-review",
    "entry-gate-design-final-phase-handoff-summary",
    "entry-gate-design-phase-terminal-closure-seal",
    "p4-m4-final-closure-index-entry-planning-gate",
    "p4-m4-final-closure-evidence-index",
    "p4-m4-final-closure-operator-handoff-index",
    "p4-m4-final-closure-transition-readiness-non-start-index",
    "p4-m4-final-closure-non-start-bridge-index",
    "p4-m4-final-closure-boundary-freeze-index",
    "p4-m4-final-closure-roadmap-alignment-snapshot",
    "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract",
    "p4-m5-1-api-readiness-audit-surface-map",
    "p4-m5-2-mcp-readiness-audit-surface-map",
    "p4-m5-3-connector-readiness-audit-surface-map",
    "p4-m5-4-cross-surface-alignment-map",
    "p4-m5-5-readiness-audit-closure-non-start-boundary-seal",
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index",
    "p4-m6-0-next-corridor-entry-boundary-contract",
    "p4-m6-1-entry-preconditions-definition-surface",
}

PREVIOUS_P4_M4_5_READ_ONLY_COMMANDS = EXPECTED_MEMORY_LOOP_COMMANDS - {
    "declared-transition-constraint-envelope-contract"
}

PROHIBITED_MEMORY_LOOP_COMMANDS = {
    "transition-constraint-intake",
    "parse-transition-constraint",
    "validate-transition-constraint",
    "enforce-transition-constraint",
    "solve-transition-constraint",
    "validate-constraint-satisfaction",
    "detect-constraint-violation",
    "accept-transition-constraint",
    "reject-transition-constraint",
    "score-transition-constraint",
    "rank-transition-constraint",
    "recommend-transition-constraint",
    "generate-transition-constraint",
    "justify-transition-constraint",
    "route-transition-constraint",
    "plan-transition-constraint",
    "execute-transition-constraint",
    "create-transition-constraint-record",
    "create-constraint-validation-record",
    "create-constraint-enforcement-record",
    "create-constraint-solving-record",
    "create-constraint-scoring-record",
    "create-constraint-routing-record",
    "create-constraint-planning-record",
    "create-constraint-justification-record",
    "validate-transition-reason",
    "route-transition-reason",
    "plan-transition-reason",
    "execute-transition-reason",
    "validate-target-phase",
    "validate-phase-transition",
    "score-readiness",
    "route-target-phase",
    "plan-transition",
    "plan-path",
    "state-space-graph",
    "transition-graph",
    "constraint-graph",
    "map-transition-reason-to-transition-constraint",
    "map-target-phase-to-transition-constraint",
    "map-human-context-to-transition-constraint",
    "validate-evidence",
    "resolve-references",
    "validate-references",
    "validate-citations",
    "fetch-sources",
    "write-provenance",
    "request-intake",
    "validate-request",
    "validate-entry-gate",
    "validate-readiness",
    "working-entry-gate",
    "activate-gate",
    "execute-gate",
    "transition-constraint-verdict",
    "approve",
    "authorize",
    "confirm",
    "recommend",
    "rank",
    "next-action",
    "execute-transition",
    "create-record",
    "write-memory",
    "start-p4-m5",
    "start-v7",
    "productize",
    "operator-console",
    "ui",
    "mvp",
    "deploy",
}


def test_declared_transition_constraint_envelope_contract_field_order_count_and_ids_are_stable():
    fields = list_declared_transition_constraint_envelope_contract_fields()

    assert [field.field_order for field in fields] == list(range(1, 21))
    assert len(fields) == 20
    assert declared_transition_constraint_envelope_contract_field_ids() == FIELD_IDS


def test_every_declared_transition_constraint_envelope_contract_field_has_required_values():
    for field in list_declared_transition_constraint_envelope_contract_fields():
        assert field.field_name.strip()
        assert field.field_purpose.strip()
        assert field.p4_m4_declared_transition_constraint_envelope_contract_category.strip()
        assert (
            field.p4_m4_declared_transition_constraint_envelope_contract_semantics_disabled.strip()
        )


def test_required_boundary_phrase_contract_contains_all_required_phrases():
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in BOUNDARY_PHRASE_LINES


def test_required_status_flag_contract_is_literal_and_complete():
    assert TRUE_STATUS_FLAGS == EXPECTED_TRUE_STATUS_FLAGS
    assert FALSE_STATUS_FLAGS == EXPECTED_FALSE_STATUS_FLAGS


def test_markdown_output_is_stable_and_contains_required_boundaries():
    first = render_declared_transition_constraint_envelope_contract_markdown()
    second = render_declared_transition_constraint_envelope_contract_markdown()

    assert first == second
    assert first.startswith(
        "# P4-M4.6 Declared Transition Constraint Envelope Contract\n"
    )
    assert DECLARED_TRANSITION_CONSTRAINT_ENVELOPE_CONTRACT_BOUNDARY in first
    for field_id in FIELD_IDS:
        assert field_id in first
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in first


def test_json_output_is_stable_and_contains_required_boundaries(tmp_path):
    args = [
        "memory-loop",
        "declared-transition-constraint-envelope-contract",
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
    assert (
        first_payload["boundary"]
        == DECLARED_TRANSITION_CONSTRAINT_ENVELOPE_CONTRACT_BOUNDARY
    )
    assert first_payload["count"] == 20
    assert first_payload["status"]["phase"] == "P4-M4.6"
    assert (
        first_payload["status"]["feature"]
        == "Declared Transition Constraint Envelope Contract"
    )
    assert first_payload["status"]["mode"] == "read-only"
    assert first_payload["status"] == declared_transition_constraint_envelope_contract_report()
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
    first_fields = declared_transition_constraint_envelope_contract_as_dicts()
    second_fields = declared_transition_constraint_envelope_contract_as_dicts()
    first_status = declared_transition_constraint_envelope_contract_report()
    second_status = declared_transition_constraint_envelope_contract_report()

    assert first_fields == second_fields
    assert [field["field_id"] for field in first_fields] == list(FIELD_IDS)
    assert first_status == second_status
    assert first_status["phase"] == "P4-M4.6"
    assert first_status["feature"] == "Declared Transition Constraint Envelope Contract"
    assert first_status["mode"] == "read-only"
    assert first_status["declared_transition_constraint_envelope_contract_field_count"] == 20
    assert (
        first_status[
            "referenced_p4_m4_5_declared_transition_reason_envelope_contract_field_count"
        ]
        == 18
    )
    assert first_status["boundary"] == DECLARED_TRANSITION_CONSTRAINT_ENVELOPE_CONTRACT_BOUNDARY


def test_status_report_locks_true_and_disabled_flags():
    status = declared_transition_constraint_envelope_contract_report()

    for flag in EXPECTED_TRUE_STATUS_FLAGS:
        assert status[flag] is True
    for flag in EXPECTED_FALSE_STATUS_FLAGS:
        assert status[flag] is False


def test_operator_markdown_default_is_read_only_and_creates_no_local_storage(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "declared-transition-constraint-envelope-contract",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M4.6 Declared Transition Constraint Envelope Contract\n")
    assert "## Status Report" in stdout
    assert DECLARED_TRANSITION_CONSTRAINT_ENVELOPE_CONTRACT_BOUNDARY in stdout
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in stdout
    assert not (tmp_path / ".local").exists()


def test_operator_markdown_format_is_explicit_and_stable(tmp_path):
    args = [
        "memory-loop",
        "declared-transition-constraint-envelope-contract",
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
    assert first_stdout.startswith("# P4-M4.6")
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
            "declared-transition-constraint-envelope-contract",
            "--workspace-root",
            str(tmp_path),
        ]
    )
    json_code, json_payload, json_stderr, _ = _run_operator(
        [
            "memory-loop",
            "declared-transition-constraint-envelope-contract",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert markdown_code == 0
    assert markdown_stderr == ""
    assert markdown_stdout.startswith("# P4-M4.6")
    assert json_code == 0
    assert json_stderr == ""
    assert json_payload["count"] == 20
    assert not (tmp_path / ".local").exists()


def test_command_creates_no_storage_files_or_state_changes(tmp_path):
    _run_operator(
        [
            "memory-loop",
            "declared-transition-constraint-envelope-contract",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    storage_root = tmp_path / ".local" / "subspace_memory"
    for filename in (
        "declared_transition_constraint_envelope_contract.jsonl",
        "transition_constraint_intake.jsonl",
        "transition_constraint_parsing.jsonl",
        "transition_constraint_validation.jsonl",
        "transition_constraint_enforcement.jsonl",
        "transition_constraint_solving.jsonl",
        "constraint_satisfaction_validation.jsonl",
        "constraint_violation_detection.jsonl",
        "constraint_sufficiency_validation.jsonl",
        "constraint_consistency_validation.jsonl",
        "constraint_integrity_validation.jsonl",
        "transition_constraint_acceptance.jsonl",
        "transition_constraint_rejection.jsonl",
        "transition_constraint_scoring.jsonl",
        "transition_constraint_ranking.jsonl",
        "transition_constraint_recommendation.jsonl",
        "transition_constraint_generation.jsonl",
        "transition_constraint_justification.jsonl",
        "transition_constraint_routing.jsonl",
        "transition_constraint_planning.jsonl",
        "transition_constraint_execution.jsonl",
        "transition_constraint_records.jsonl",
        "constraint_validation_records.jsonl",
        "constraint_enforcement_records.jsonl",
        "constraint_solving_records.jsonl",
        "constraint_scoring_records.jsonl",
        "constraint_routing_records.jsonl",
        "constraint_planning_records.jsonl",
        "constraint_justification_records.jsonl",
        "transition_reason_validation.jsonl",
        "transition_reason_routing.jsonl",
        "transition_reason_planning.jsonl",
        "transition_reason_execution.jsonl",
        "target_phase_validation.jsonl",
        "phase_transition_validation.jsonl",
        "readiness_scoring.jsonl",
        "target_phase_routing.jsonl",
        "transition_planning.jsonl",
        "path_planning.jsonl",
        "state_space_graph.jsonl",
        "transition_graph.jsonl",
        "constraint_graph.jsonl",
        "semantic_target_field_graph.jsonl",
        "transition_reason_to_transition_constraint_mapping.jsonl",
        "target_phase_to_transition_constraint_mapping.jsonl",
        "human_context_to_transition_constraint_mapping.jsonl",
        "evidence_validation.jsonl",
        "reference_resolution.jsonl",
        "reference_validation.jsonl",
        "citation_validation.jsonl",
        "source_fetching.jsonl",
        "provenance_writing.jsonl",
        "request_intake.jsonl",
        "request_validation.jsonl",
        "entry_gate_validation.jsonl",
        "readiness_validation.jsonl",
        "validation.jsonl",
        "memories.jsonl",
        "proposals.jsonl",
        "lifecycle.jsonl",
        "roadmap.jsonl",
        "audit.jsonl",
    ):
        assert not (storage_root / filename).exists()
    assert not (tmp_path / ".local").exists()


def test_read_only_allowlist_includes_new_command_and_preserves_previous_commands():
    commands = _memory_loop_commands()

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
    assert "declared-transition-constraint-envelope-contract" in commands
    assert PREVIOUS_P4_M4_5_READ_ONLY_COMMANDS.issubset(commands)
    assert commands.isdisjoint(PROHIBITED_MEMORY_LOOP_COMMANDS)


def test_doc_contains_required_boundaries():
    doc = Path(
        "docs/CIVILIZATION_CORE_P4_M4_6_DECLARED_TRANSITION_CONSTRAINT_ENVELOPE_CONTRACT.md"
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
    assert "p4_m4_declared_transition_constraint_envelope_contract" not in entry_points
    assert "declared-transition-constraint-envelope-contract" not in entry_points


def test_no_uv_lock_is_created():
    assert not Path("uv.lock").exists()


def test_custom_markdown_render_accepts_read_only_fields():
    field = DeclaredTransitionConstraintEnvelopeContractField(
        field_order=1,
        field_id="custom-declared-transition-constraint-envelope-contract",
        field_name="Custom Declared Transition Constraint Envelope Contract Field",
        field_purpose="Custom inspection-only purpose.",
        p4_m4_declared_transition_constraint_envelope_contract_category=(
            "custom-declared-transition-constraint-envelope-contract-category"
        ),
        p4_m4_declared_transition_constraint_envelope_contract_semantics_disabled=(
            "Custom declared transition constraint envelope semantics are disabled."
        ),
    )

    markdown = render_declared_transition_constraint_envelope_contract_markdown([field])

    assert "custom-declared-transition-constraint-envelope-contract" in markdown
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
