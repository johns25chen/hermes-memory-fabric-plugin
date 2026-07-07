from __future__ import annotations

import argparse
import io
import json
import tomllib
from pathlib import Path

from hermes_memory_fabric.p4_m0_subspace_operator import build_parser, run_operator_command
from hermes_memory_fabric.p4_m4_declared_transition_package_assembly_envelope_contract import (
    BOUNDARY_PHRASE_LINES,
    DECLARED_TRANSITION_PACKAGE_ASSEMBLY_ENVELOPE_CONTRACT_BOUNDARY,
    FALSE_STATUS_FLAGS,
    TRUE_STATUS_FLAGS,
    DeclaredTransitionPackageAssemblyEnvelopeContractField,
    declared_transition_package_assembly_envelope_contract_as_dicts,
    declared_transition_package_assembly_envelope_contract_field_ids,
    declared_transition_package_assembly_envelope_contract_report,
    list_declared_transition_package_assembly_envelope_contract_fields,
    render_declared_transition_package_assembly_envelope_contract_markdown,
)


FIELD_IDS = (
    "p4-m4-declared-transition-package-assembly-envelope-contract-id",
    "p4-m4-declared-transition-package-assembly-envelope-contract-phase",
    "p4-m4-declared-transition-package-assembly-envelope-contract-mode",
    "p4-m4-declared-transition-package-assembly-envelope-contract-direct-prior-declared-transition-safeguard-envelope-reference",
    "p4-m4-declared-transition-package-assembly-envelope-contract-inherited-prior-declared-transition-assumption-envelope-reference",
    "p4-m4-declared-transition-package-assembly-envelope-contract-inherited-prior-declared-transition-risk-envelope-reference",
    "p4-m4-declared-transition-package-assembly-envelope-contract-inherited-prior-declared-transition-impact-envelope-reference",
    "p4-m4-declared-transition-package-assembly-envelope-contract-inherited-prior-declared-transition-dependency-envelope-reference",
    "p4-m4-declared-transition-package-assembly-envelope-contract-inherited-prior-declared-transition-constraint-envelope-reference",
    "p4-m4-declared-transition-package-assembly-envelope-contract-inherited-prior-declared-transition-reason-envelope-reference",
    "p4-m4-declared-transition-package-assembly-envelope-contract-inherited-prior-target-phase-envelope-reference",
    "p4-m4-declared-transition-package-assembly-envelope-contract-inherited-prior-declared-human-context-envelope-reference",
    "p4-m4-declared-transition-package-assembly-envelope-contract-inherited-prior-evidence-reference-envelope-reference",
    "p4-m4-declared-transition-package-assembly-envelope-contract-inherited-prior-request-envelope-reference",
    "p4-m4-declared-transition-package-assembly-envelope-contract-inherited-prior-boundary-reference",
    "p4-m4-declared-transition-package-assembly-envelope-contract-inherited-prior-handoff-reference",
    "p4-m4-declared-transition-package-assembly-envelope-contract-scope",
    "p4-m4-declared-transition-package-assembly-envelope-contract-declared-transition-package-assembly-envelope-design-only",
    "p4-m4-declared-transition-package-assembly-envelope-contract-declared-package-assembly-surface-definition",
    "p4-m4-declared-transition-package-assembly-envelope-contract-package-assembly-non-validation-boundary-definition",
    "p4-m4-declared-transition-package-assembly-envelope-contract-package-assembly-non-composition-execution-routing-boundary-definition",
    "p4-m4-declared-transition-package-assembly-envelope-contract-declaration-only-semantics-definition",
    "p4-m4-declared-transition-package-assembly-envelope-contract-package-assembly-validation-composition-execution-routing-scoring-graph-semantics-disabled",
)

DATACLASS_FIELDS = {
    "field_order",
    "field_id",
    "field_name",
    "field_purpose",
    "p4_m4_declared_transition_package_assembly_envelope_contract_category",
    "p4_m4_declared_transition_package_assembly_envelope_contract_semantics_disabled",
}

REQUIRED_BOUNDARY_PHRASES = tuple(
    line
    for line in """
P4-M4.12
Declared Transition Package Assembly Envelope Contract
read-only
definition-only
declared-transition-package-assembly-envelope-design-only
declared-package-assembly-surface-only
package-assembly-non-validation-boundary-only
package-assembly-non-composition-boundary-only
package-assembly-non-execution-boundary-only
package-assembly-non-routing-boundary-only
package-assembly-non-graph-boundary-only
declaration-only
inspection-only
P4-M4.12 Declared Transition Package Assembly Envelope Contract is definition only
P4-M4.12 is declared-transition-package-assembly-envelope-design-only
P4-M4.12 is declared-package-assembly-surface-only
P4-M4.12 is package-assembly-non-validation-boundary-only
P4-M4.12 is package-assembly-non-composition-boundary-only
P4-M4.12 is package-assembly-non-execution-boundary-only
P4-M4.12 is package-assembly-non-routing-boundary-only
P4-M4.12 is package-assembly-non-graph-boundary-only
P4-M4.12 is declaration-only
P4-M4.11 Declared Transition Safeguard Envelope Contract remains the direct prior declared transition safeguard envelope reference
P4-M4.11 declared transition safeguard remains only an inherited static declared safeguard surface reference
P4-M4.10 Declared Transition Assumption Envelope Contract remains the inherited prior declared transition assumption envelope reference
P4-M4.10 declared transition assumption remains only an inherited static declared assumption surface reference
P4-M4.9 Declared Transition Risk Envelope Contract remains the inherited prior declared transition risk envelope reference
P4-M4.9 declared transition risk remains only an inherited static declared risk surface reference
P4-M4.8 Declared Transition Impact Envelope Contract remains the inherited prior declared transition impact envelope reference
P4-M4.8 declared transition impact remains only an inherited static declared impact surface reference
P4-M4.7 Declared Transition Dependency Envelope Contract remains the inherited prior declared transition dependency envelope reference
P4-M4.7 declared transition dependency remains only an inherited static declared dependency surface reference
P4-M4.6 Declared Transition Constraint Envelope Contract remains the inherited prior declared transition constraint envelope reference
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
P4-M4 declared transition package assembly envelope design starts only as a static declared package assembly description surface
P4-M4 transition package assembly validation remains not implemented
P4-M4 transition package assembly composition remains not implemented
P4-M4 transition package assembly execution remains not implemented
P4-M4 transition package assembly scoring remains not implemented
P4-M4 transition package assembly routing remains not implemented
P4-M4 transition package assembly planning remains not implemented
P4-M4 package assembly graph construction remains not implemented
P4-M4 package assembly dependency solving remains not implemented
P4-M4 package assembly consistency checking remains not implemented
P4-M4 package assembly sufficiency checking remains not implemented
P4-M4 package assembly integrity checking remains not implemented
P4-M4 transition package assembly acceptance remains not implemented
P4-M4 transition package assembly rejection remains not implemented
P4-M4 transition package assembly ranking remains not implemented
P4-M4 transition package assembly recommendation remains not implemented
P4-M4 transition package assembly generation remains not implemented
P4-M4 transition package assembly justification remains not implemented
P4-M4 transition package assembly record creation remains not implemented
P4-M4 package assembly validation record creation remains not implemented
P4-M4 package assembly composition record creation remains not implemented
P4-M4 package assembly execution record creation remains not implemented
P4-M4 package assembly scoring record creation remains not implemented
P4-M4 package assembly graph record creation remains not implemented
P4-M4 package assembly consistency record creation remains not implemented
P4-M4 package assembly sufficiency record creation remains not implemented
P4-M4 package assembly integrity record creation remains not implemented
P4-M4 package assembly routing record creation remains not implemented
P4-M4 package assembly planning record creation remains not implemented
P4-M4 package assembly justification record creation remains not implemented
P4-M4 transition safeguard validation remains not implemented
P4-M4 transition safeguard enforcement remains not implemented
P4-M4 transition safeguard execution remains not implemented
P4-M4 transition safeguard mitigation remains not implemented
P4-M4 transition safeguard scoring remains not implemented
P4-M4 safeguard graph construction remains not implemented
P4-M4 transition safeguard to transition package assembly mapping remains not implemented
P4-M4 transition assumption to transition package assembly mapping remains not implemented
P4-M4 transition risk to transition package assembly mapping remains not implemented
P4-M4 transition impact to transition package assembly mapping remains not implemented
P4-M4 transition dependency to transition package assembly mapping remains not implemented
P4-M4 transition constraint to transition package assembly mapping remains not implemented
P4-M4 transition reason to transition package assembly mapping remains not implemented
P4-M4 target phase to transition package assembly mapping remains not implemented
P4-M4 human context to transition package assembly mapping remains not implemented
P4-M4 risk mitigation remains not implemented
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
no transition package assembly intake
no live transition package assembly parsing
no transition package assembly validation
no transition package assembly composition
no transition package assembly execution
no transition package assembly scoring
no transition package assembly routing
no transition package assembly planning
no package assembly graph construction
no package assembly dependency solving
no package assembly consistency checking
no package assembly sufficiency checking
no package assembly integrity checking
no transition package assembly acceptance
no transition package assembly rejection
no transition package assembly routing
no transition package assembly planning
no transition safeguard to transition package assembly mapping
no transition assumption to transition package assembly mapping
no transition risk to transition package assembly mapping
no transition impact to transition package assembly mapping
no transition dependency to transition package assembly mapping
no transition constraint to transition package assembly mapping
no transition reason to transition package assembly mapping
no target phase to transition package assembly mapping
no human context to transition package assembly mapping
no risk mitigation
no P4-M5
no v7
no productization
no UI
no Operator Console
no version bump
no tag
""".splitlines()
    if line
)

OPERATOR_SMOKE_PHRASES = (
    "P4-M4.12 Declared Transition Package Assembly Envelope Contract",
    "read-only",
    "definition-only",
    "declared-transition-package-assembly-envelope-design-only",
    "declared-package-assembly-surface-only",
    "package-assembly-non-validation-boundary-only",
    "package-assembly-non-composition-boundary-only",
    "package-assembly-non-execution-boundary-only",
    "package-assembly-non-routing-boundary-only",
    "package-assembly-non-graph-boundary-only",
    "declaration-only",
    "inspection-only",
    "P4-M4.11 Declared Transition Safeguard Envelope Contract remains the direct prior declared transition safeguard envelope reference",
    "P4-M4.11 declared transition safeguard remains only an inherited static declared safeguard surface reference",
    "P4-M4 transition package assembly validation remains not implemented",
    "P4-M4 transition package assembly composition remains not implemented",
    "P4-M4 transition package assembly execution remains not implemented",
    "P4-M4 transition package assembly scoring remains not implemented",
    "P4-M4 transition package assembly routing remains not implemented",
    "P4-M4 transition package assembly planning remains not implemented",
    "P4-M4 package assembly graph construction remains not implemented",
    "P4-M4 transition package assembly acceptance remains not implemented",
    "P4-M4 transition package assembly rejection remains not implemented",
    "P4-M4 transition safeguard to transition package assembly mapping remains not implemented",
    "P4-M4 transition assumption to transition package assembly mapping remains not implemented",
    "P4-M4 transition risk to transition package assembly mapping remains not implemented",
    "P4-M4 transition impact to transition package assembly mapping remains not implemented",
    "P4-M4 transition dependency to transition package assembly mapping remains not implemented",
    "P4-M4 transition constraint to transition package assembly mapping remains not implemented",
    "P4-M4 transition reason to transition package assembly mapping remains not implemented",
    "P4-M4 target phase to transition package assembly mapping remains not implemented",
    "P4-M4 human context to transition package assembly mapping remains not implemented",
    "no transition package assembly validation",
    "no transition package assembly composition",
    "no transition package assembly execution",
    "no transition package assembly scoring",
    "no transition package assembly routing",
    "no transition package assembly planning",
    "no package assembly graph construction",
    "no transition package assembly acceptance",
    "no transition package assembly rejection",
    "no transition safeguard to transition package assembly mapping",
    "no transition assumption to transition package assembly mapping",
    "no transition risk to transition package assembly mapping",
    "no transition impact to transition package assembly mapping",
    "no transition dependency to transition package assembly mapping",
    "no transition constraint to transition package assembly mapping",
    "no transition reason to transition package assembly mapping",
    "no target phase to transition package assembly mapping",
    "no human context to transition package assembly mapping",
    "no risk mitigation",
    "no P4-M5",
    "no v7",
    "no productization",
    "no UI",
    "no Operator Console",
    "no version bump",
    "no tag",
)

EXPECTED_TRUE_STATUS_FLAGS = tuple(
    line
    for line in """
definition_only
declared_transition_package_assembly_envelope_design_only
declared_package_assembly_surface_only
package_assembly_non_validation_boundary_only
package_assembly_non_composition_boundary_only
package_assembly_non_execution_boundary_only
package_assembly_non_routing_boundary_only
package_assembly_non_graph_boundary_only
declaration_only
inspection_only
p4_m4_12_declared_transition_package_assembly_envelope_contract_started
p4_m4_12_definition_only
p4_m4_12_declared_transition_package_assembly_envelope_design_only
p4_m4_12_declared_package_assembly_surface_only
p4_m4_12_package_assembly_non_validation_boundary_only
p4_m4_12_package_assembly_non_composition_boundary_only
p4_m4_12_package_assembly_non_execution_boundary_only
p4_m4_12_package_assembly_non_routing_boundary_only
p4_m4_12_package_assembly_non_graph_boundary_only
p4_m4_12_declaration_only
p4_m4_11_declared_transition_safeguard_envelope_contract_reference_defined
p4_m4_11_declared_transition_safeguard_static_reference_defined
p4_m4_10_declared_transition_assumption_envelope_contract_reference_defined
p4_m4_10_declared_transition_assumption_static_reference_defined
p4_m4_9_declared_transition_risk_envelope_contract_reference_defined
p4_m4_9_declared_transition_risk_static_reference_defined
p4_m4_8_declared_transition_impact_envelope_contract_reference_defined
p4_m4_8_declared_transition_impact_static_reference_defined
p4_m4_7_declared_transition_dependency_envelope_contract_reference_defined
p4_m4_7_declared_transition_dependency_static_reference_defined
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
p4_m4_declared_transition_package_assembly_envelope_design_defined
p4_m4_declared_package_assembly_surface_defined
p4_m4_transition_package_assembly_non_validation_boundary_defined
p4_m4_transition_package_assembly_non_composition_boundary_defined
p4_m4_transition_package_assembly_non_execution_boundary_defined
p4_m4_transition_package_assembly_non_routing_boundary_defined
p4_m4_transition_package_assembly_non_graph_boundary_defined
p4_m4_transition_package_assembly_non_acceptance_boundary_defined
p4_m4_transition_package_assembly_non_rejection_boundary_defined
p4_m4_transition_package_assembly_non_ranking_boundary_defined
p4_m4_transition_package_assembly_non_recommendation_boundary_defined
p4_m4_transition_package_assembly_non_generation_boundary_defined
p4_m4_transition_package_assembly_non_justification_boundary_defined
p4_m4_transition_package_assembly_validation_semantics_prohibited
p4_m4_transition_package_assembly_composition_semantics_prohibited
p4_m4_transition_package_assembly_execution_semantics_prohibited
p4_m4_transition_package_assembly_scoring_semantics_prohibited
p4_m4_transition_package_assembly_routing_semantics_prohibited
p4_m4_transition_package_assembly_planning_semantics_prohibited
p4_m4_package_assembly_graph_semantics_prohibited
p4_m4_package_assembly_dependency_solving_semantics_prohibited
p4_m4_package_assembly_consistency_semantics_prohibited
p4_m4_package_assembly_sufficiency_semantics_prohibited
p4_m4_package_assembly_integrity_semantics_prohibited
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
transition_package_assembly_intake_enabled
live_transition_package_assembly_parsing_enabled
transition_package_assembly_validation_enabled
transition_package_assembly_composition_enabled
transition_package_assembly_execution_enabled
transition_package_assembly_scoring_enabled
transition_package_assembly_routing_enabled
transition_package_assembly_planning_enabled
package_assembly_graph_construction_enabled
package_assembly_dependency_solving_enabled
package_assembly_consistency_checking_enabled
package_assembly_sufficiency_checking_enabled
package_assembly_integrity_checking_enabled
transition_package_assembly_acceptance_enabled
transition_package_assembly_rejection_enabled
transition_package_assembly_ranking_enabled
transition_package_assembly_recommendation_enabled
transition_package_assembly_generation_enabled
transition_package_assembly_justification_enabled
transition_package_assembly_record_creation_enabled
package_assembly_validation_record_creation_enabled
package_assembly_composition_record_creation_enabled
package_assembly_execution_record_creation_enabled
package_assembly_scoring_record_creation_enabled
package_assembly_graph_record_creation_enabled
package_assembly_consistency_record_creation_enabled
package_assembly_sufficiency_record_creation_enabled
package_assembly_integrity_record_creation_enabled
package_assembly_routing_record_creation_enabled
package_assembly_planning_record_creation_enabled
package_assembly_justification_record_creation_enabled
transition_safeguard_validation_enabled
transition_safeguard_enforcement_enabled
transition_safeguard_execution_enabled
transition_safeguard_mitigation_enabled
transition_safeguard_scoring_enabled
safeguard_graph_construction_enabled
transition_safeguard_routing_enabled
transition_safeguard_planning_enabled
transition_safeguard_to_transition_package_assembly_mapping_enabled
transition_assumption_to_transition_package_assembly_mapping_enabled
transition_risk_to_transition_package_assembly_mapping_enabled
transition_impact_to_transition_package_assembly_mapping_enabled
transition_dependency_to_transition_package_assembly_mapping_enabled
transition_constraint_to_transition_package_assembly_mapping_enabled
transition_reason_to_transition_package_assembly_mapping_enabled
target_phase_to_transition_package_assembly_mapping_enabled
human_context_to_transition_package_assembly_mapping_enabled
transition_assumption_validation_enabled
transition_assumption_resolution_enabled
transition_assumption_scoring_enabled
assumption_graph_construction_enabled
transition_assumption_routing_enabled
transition_assumption_planning_enabled
transition_assumption_execution_enabled
transition_risk_analysis_enabled
transition_risk_validation_enabled
transition_risk_scoring_enabled
risk_graph_construction_enabled
risk_mitigation_enabled
transition_risk_routing_enabled
transition_risk_planning_enabled
transition_risk_execution_enabled
transition_impact_analysis_enabled
transition_impact_validation_enabled
transition_impact_scoring_enabled
impact_graph_construction_enabled
transition_impact_routing_enabled
transition_impact_planning_enabled
transition_impact_execution_enabled
transition_dependency_validation_enabled
transition_dependency_resolution_enabled
transition_dependency_solving_enabled
transition_dependency_graph_construction_enabled
transition_dependency_routing_enabled
transition_dependency_planning_enabled
transition_dependency_execution_enabled
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
impact_graph_enabled
risk_graph_enabled
assumption_graph_enabled
safeguard_graph_enabled
package_assembly_graph_enabled
semantic_target_field_graph_enabled
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
package_assembly_enabled
package_composition_enabled
package_execution_enabled
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
transition_package_assembly_verdict_enabled
transition_safeguard_verdict_enabled
transition_assumption_verdict_enabled
transition_risk_verdict_enabled
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
transition_package_assembly_mutation_enabled
transition_safeguard_mutation_enabled
transition_assumption_mutation_enabled
transition_risk_mutation_enabled
transition_impact_mutation_enabled
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
    "p4-m6-2-entry-acceptance-non-evidence-surface",
    "p4-m6-3-entry-deferral-non-execution-surface",
}

PROHIBITED_MEMORY_LOOP_COMMANDS = {
    "transition-package-assembly-intake",
    "parse-transition-package-assembly",
    "assemble-transition-package",
    "compose-transition-package",
    "validate-transition-package-assembly",
    "score-transition-package-assembly",
    "route-transition-package-assembly",
    "plan-transition-package-assembly",
    "execute-transition-package-assembly",
    "build-package-assembly-graph",
    "solve-package-assembly-dependency",
    "check-package-assembly-consistency",
    "check-package-assembly-sufficiency",
    "check-package-assembly-integrity",
    "accept-transition-package-assembly",
    "reject-transition-package-assembly",
    "rank-transition-package-assembly",
    "recommend-transition-package-assembly",
    "generate-transition-package-assembly",
    "justify-transition-package-assembly",
    "create-transition-package-assembly-record",
    "map-transition-safeguard-to-transition-package-assembly",
    "map-transition-assumption-to-transition-package-assembly",
    "map-transition-risk-to-transition-package-assembly",
    "map-transition-impact-to-transition-package-assembly",
    "map-transition-dependency-to-transition-package-assembly",
    "map-transition-constraint-to-transition-package-assembly",
    "map-transition-reason-to-transition-package-assembly",
    "map-target-phase-to-transition-package-assembly",
    "map-human-context-to-transition-package-assembly",
    "mitigate-risk",
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
    "transition-package-assembly-verdict",
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


def test_declared_transition_package_assembly_envelope_contract_field_order_count_and_ids_are_stable():
    fields = list_declared_transition_package_assembly_envelope_contract_fields()

    assert [field.field_order for field in fields] == list(range(1, 24))
    assert len(fields) == 23
    assert declared_transition_package_assembly_envelope_contract_field_ids() == FIELD_IDS


def test_every_declared_transition_package_assembly_envelope_contract_field_has_required_values():
    for field in list_declared_transition_package_assembly_envelope_contract_fields():
        assert field.field_name.strip()
        assert field.field_purpose.strip()
        assert (
            field.p4_m4_declared_transition_package_assembly_envelope_contract_category.strip()
        )
        assert (
            field.p4_m4_declared_transition_package_assembly_envelope_contract_semantics_disabled.strip()
        )


def test_required_boundary_phrase_contract_contains_all_required_phrases():
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in BOUNDARY_PHRASE_LINES
    for phrase in OPERATOR_SMOKE_PHRASES:
        assert (
            phrase in BOUNDARY_PHRASE_LINES
            or phrase in DECLARED_TRANSITION_PACKAGE_ASSEMBLY_ENVELOPE_CONTRACT_BOUNDARY
        )


def test_required_status_flag_contract_is_literal_and_complete():
    assert TRUE_STATUS_FLAGS == EXPECTED_TRUE_STATUS_FLAGS
    assert FALSE_STATUS_FLAGS == EXPECTED_FALSE_STATUS_FLAGS


def test_markdown_output_is_stable_and_contains_required_boundaries():
    first = render_declared_transition_package_assembly_envelope_contract_markdown()
    second = render_declared_transition_package_assembly_envelope_contract_markdown()

    assert first == second
    assert first.startswith(
        "# P4-M4.12 Declared Transition Package Assembly Envelope Contract\n"
    )
    assert DECLARED_TRANSITION_PACKAGE_ASSEMBLY_ENVELOPE_CONTRACT_BOUNDARY in first
    for field_id in FIELD_IDS:
        assert field_id in first
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in first


def test_json_output_is_stable_and_contains_required_boundaries(tmp_path):
    args = [
        "memory-loop",
        "declared-transition-package-assembly-envelope-contract",
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
        == DECLARED_TRANSITION_PACKAGE_ASSEMBLY_ENVELOPE_CONTRACT_BOUNDARY
    )
    assert first_payload["count"] == 23
    assert first_payload["status"]["phase"] == "P4-M4.12"
    assert (
        first_payload["status"]["feature"]
        == "Declared Transition Package Assembly Envelope Contract"
    )
    assert first_payload["status"]["mode"] == "read-only"
    assert (
        first_payload["status"]
        == declared_transition_package_assembly_envelope_contract_report()
    )
    assert [item["field_id"] for item in first_payload["fields"]] == list(FIELD_IDS)
    assert set(first_payload["fields"][0]) == DATACLASS_FIELDS
    for flag in EXPECTED_TRUE_STATUS_FLAGS:
        assert first_payload["status"][flag] is True
    for flag in EXPECTED_FALSE_STATUS_FLAGS:
        assert first_payload["status"][flag] is False
    for phrase in OPERATOR_SMOKE_PHRASES:
        assert phrase in first_stdout
    assert not (tmp_path / ".local").exists()


def test_dict_conversion_and_status_report_are_deterministic():
    first_fields = declared_transition_package_assembly_envelope_contract_as_dicts()
    second_fields = declared_transition_package_assembly_envelope_contract_as_dicts()
    first_status = declared_transition_package_assembly_envelope_contract_report()
    second_status = declared_transition_package_assembly_envelope_contract_report()

    assert first_fields == second_fields
    assert [field["field_id"] for field in first_fields] == list(FIELD_IDS)
    assert first_status == second_status
    assert first_status["phase"] == "P4-M4.12"
    assert first_status["feature"] == "Declared Transition Package Assembly Envelope Contract"
    assert first_status["mode"] == "read-only"
    assert (
        first_status[
            "declared_transition_package_assembly_envelope_contract_field_count"
        ]
        == 23
    )
    assert (
        first_status[
            "referenced_p4_m4_11_declared_transition_safeguard_envelope_contract_field_count"
        ]
        == 23
    )
    assert (
        first_status["boundary"]
        == DECLARED_TRANSITION_PACKAGE_ASSEMBLY_ENVELOPE_CONTRACT_BOUNDARY
    )


def test_status_report_locks_true_and_disabled_flags():
    status = declared_transition_package_assembly_envelope_contract_report()

    for flag in EXPECTED_TRUE_STATUS_FLAGS:
        assert status[flag] is True
    for flag in EXPECTED_FALSE_STATUS_FLAGS:
        assert status[flag] is False


def test_operator_markdown_default_is_read_only_and_creates_no_local_storage(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "declared-transition-package-assembly-envelope-contract",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith(
        "# P4-M4.12 Declared Transition Package Assembly Envelope Contract\n"
    )
    assert "## Status Report" in stdout
    assert DECLARED_TRANSITION_PACKAGE_ASSEMBLY_ENVELOPE_CONTRACT_BOUNDARY in stdout
    for phrase in OPERATOR_SMOKE_PHRASES:
        assert phrase in stdout
    assert not (tmp_path / ".local").exists()


def test_operator_markdown_format_is_explicit_and_stable(tmp_path):
    args = [
        "memory-loop",
        "declared-transition-package-assembly-envelope-contract",
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
    assert first_stdout.startswith("# P4-M4.12")
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
            "declared-transition-package-assembly-envelope-contract",
            "--workspace-root",
            str(tmp_path),
        ]
    )
    json_code, json_payload, json_stderr, _ = _run_operator(
        [
            "memory-loop",
            "declared-transition-package-assembly-envelope-contract",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert markdown_code == 0
    assert markdown_stderr == ""
    assert markdown_stdout.startswith("# P4-M4.12")
    assert json_code == 0
    assert json_stderr == ""
    assert json_payload["count"] == 23
    assert not (tmp_path / ".local").exists()


def test_command_creates_no_storage_files_or_state_changes(tmp_path):
    _run_operator(
        [
            "memory-loop",
            "declared-transition-package-assembly-envelope-contract",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    storage_root = tmp_path / ".local" / "subspace_memory"
    for filename in (
        "declared_transition_package_assembly_envelope_contract.jsonl",
        "transition_package_assembly_intake.jsonl",
        "transition_package_assembly_parsing.jsonl",
        "transition_package_assembly_validation.jsonl",
        "transition_package_assembly_composition.jsonl",
        "transition_package_assembly_execution.jsonl",
        "transition_package_assembly_scoring.jsonl",
        "transition_package_assembly_routing.jsonl",
        "transition_package_assembly_planning.jsonl",
        "package_assembly_graph_construction.jsonl",
        "package_assembly_dependency_solving.jsonl",
        "package_assembly_consistency_checking.jsonl",
        "package_assembly_sufficiency_checking.jsonl",
        "package_assembly_integrity_checking.jsonl",
        "transition_package_assembly_acceptance.jsonl",
        "transition_package_assembly_rejection.jsonl",
        "transition_package_assembly_ranking.jsonl",
        "transition_package_assembly_recommendation.jsonl",
        "transition_package_assembly_generation.jsonl",
        "transition_package_assembly_justification.jsonl",
        "transition_package_assembly_record_creation.jsonl",
        "package_assembly_validation_record_creation.jsonl",
        "package_assembly_composition_record_creation.jsonl",
        "package_assembly_execution_record_creation.jsonl",
        "package_assembly_scoring_record_creation.jsonl",
        "package_assembly_graph_record_creation.jsonl",
        "package_assembly_routing_record_creation.jsonl",
        "package_assembly_planning_record_creation.jsonl",
        "package_assembly_justification_record_creation.jsonl",
        "transition_safeguard_to_transition_package_assembly_mapping.jsonl",
        "transition_assumption_to_transition_package_assembly_mapping.jsonl",
        "transition_risk_to_transition_package_assembly_mapping.jsonl",
        "transition_impact_to_transition_package_assembly_mapping.jsonl",
        "transition_dependency_to_transition_package_assembly_mapping.jsonl",
        "transition_constraint_to_transition_package_assembly_mapping.jsonl",
        "transition_reason_to_transition_package_assembly_mapping.jsonl",
        "target_phase_to_transition_package_assembly_mapping.jsonl",
        "human_context_to_transition_package_assembly_mapping.jsonl",
        "risk_mitigation.jsonl",
    ):
        assert not (storage_root / filename).exists()
    assert not storage_root.exists()


def test_parser_exposes_only_expected_memory_loop_command_surface():
    commands = _memory_loop_subcommands(build_parser())

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
    assert "declared-transition-package-assembly-envelope-contract" in commands
    assert not (commands & PROHIBITED_MEMORY_LOOP_COMMANDS)


def test_command_is_not_packaged_as_top_level_entry_point():
    entry_points = _project_entry_points()

    assert "declared-transition-package-assembly-envelope-contract" not in entry_points
    assert "declared-transition-package-assembly-envelope-contract" not in str(
        entry_points
    )


def test_static_doc_contains_required_boundaries_and_fields():
    project_root = Path(__file__).resolve().parents[1]
    doc_path = (
        project_root
        / "docs"
        / "CIVILIZATION_CORE_P4_M4_12_DECLARED_TRANSITION_PACKAGE_ASSEMBLY_ENVELOPE_CONTRACT.md"
    )
    doc = doc_path.read_text(encoding="utf-8")

    assert doc.startswith(
        "# P4-M4.12 Declared Transition Package Assembly Envelope Contract\n"
    )
    for field_id in FIELD_IDS:
        assert field_id in doc
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in doc


def test_custom_field_rendering_remains_definition_only():
    custom = DeclaredTransitionPackageAssemblyEnvelopeContractField(
        field_order=24,
        field_id="custom-declared-transition-package-assembly-envelope-contract",
        field_name="Custom Declared Transition Package Assembly Envelope Contract Field",
        field_purpose="Custom read-only declared package assembly surface field.",
        p4_m4_declared_transition_package_assembly_envelope_contract_category=(
            "custom-declared-transition-package-assembly-envelope-contract-category"
        ),
        p4_m4_declared_transition_package_assembly_envelope_contract_semantics_disabled=(
            "no transition package assembly validation semantics"
        ),
    )

    markdown = render_declared_transition_package_assembly_envelope_contract_markdown(
        [custom]
    )

    assert "custom-declared-transition-package-assembly-envelope-contract" in markdown
    assert "Custom read-only declared package assembly surface field." in markdown
    assert DECLARED_TRANSITION_PACKAGE_ASSEMBLY_ENVELOPE_CONTRACT_BOUNDARY in markdown


def _run_operator(args: list[str]) -> tuple[int, dict[str, object], str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    code = run_operator_command(args, stdout=stdout, stderr=stderr)
    stdout_value = stdout.getvalue()
    payload = json.loads(stdout_value) if stdout_value.startswith("{") else {}
    return code, payload, stderr.getvalue(), stdout_value


def _memory_loop_subcommands(parser: argparse.ArgumentParser) -> set[str]:
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


def _project_entry_points() -> dict[str, dict[str, str]]:
    project_root = Path(__file__).resolve().parents[1]
    with (project_root / "pyproject.toml").open("rb") as handle:
        return tomllib.load(handle)["project"]["entry-points"]
