from __future__ import annotations

import argparse
import dataclasses
import io
import json
import tomllib
from pathlib import Path

import hermes_memory_fabric.p4_m0_subspace_operator as operator
from hermes_memory_fabric.p4_m0_subspace_operator import (
    build_parser,
    run_operator_command,
)
from hermes_memory_fabric.p4_m4_entry_gate_design_phase_terminal_closure_seal import (
    BOUNDARY_PHRASE_LINES,
    ENTRY_GATE_DESIGN_PHASE_TERMINAL_CLOSURE_SEAL_BOUNDARY,
    FALSE_STATUS_FLAGS,
    TRUE_STATUS_FLAGS,
    EntryGateDesignPhaseTerminalClosureSealField,
    entry_gate_design_phase_terminal_closure_seal_as_dicts,
    entry_gate_design_phase_terminal_closure_seal_field_ids,
    entry_gate_design_phase_terminal_closure_seal_report,
    list_entry_gate_design_phase_terminal_closure_seal_fields,
    render_entry_gate_design_phase_terminal_closure_seal_markdown,
)


FIELD_IDS = (
    "p4-m4-entry-gate-design-phase-terminal-closure-seal-id",
    "p4-m4-entry-gate-design-phase-terminal-closure-seal-phase",
    "p4-m4-entry-gate-design-phase-terminal-closure-seal-mode",
    "p4-m4-entry-gate-design-phase-terminal-closure-seal-direct-prior-final-phase-handoff-summary-reference",
    "p4-m4-entry-gate-design-phase-terminal-closure-seal-inherited-prior-phase-closure-review-reference",
    "p4-m4-entry-gate-design-phase-terminal-closure-seal-inherited-prior-closure-handoff-contract-reference",
    "p4-m4-entry-gate-design-phase-terminal-closure-seal-inherited-prior-final-non-validation-boundary-audit-reference",
    "p4-m4-entry-gate-design-phase-terminal-closure-seal-inherited-prior-declared-transition-package-assembly-envelope-reference",
    "p4-m4-entry-gate-design-phase-terminal-closure-seal-inherited-prior-declared-transition-safeguard-envelope-reference",
    "p4-m4-entry-gate-design-phase-terminal-closure-seal-inherited-prior-declared-transition-assumption-envelope-reference",
    "p4-m4-entry-gate-design-phase-terminal-closure-seal-inherited-prior-declared-transition-risk-envelope-reference",
    "p4-m4-entry-gate-design-phase-terminal-closure-seal-inherited-prior-declared-transition-impact-envelope-reference",
    "p4-m4-entry-gate-design-phase-terminal-closure-seal-inherited-prior-declared-transition-dependency-envelope-reference",
    "p4-m4-entry-gate-design-phase-terminal-closure-seal-inherited-prior-declared-transition-constraint-envelope-reference",
    "p4-m4-entry-gate-design-phase-terminal-closure-seal-inherited-prior-declared-transition-reason-envelope-reference",
    "p4-m4-entry-gate-design-phase-terminal-closure-seal-inherited-prior-target-phase-envelope-reference",
    "p4-m4-entry-gate-design-phase-terminal-closure-seal-inherited-prior-declared-human-context-envelope-reference",
    "p4-m4-entry-gate-design-phase-terminal-closure-seal-inherited-prior-evidence-reference-envelope-reference",
    "p4-m4-entry-gate-design-phase-terminal-closure-seal-inherited-prior-request-envelope-reference",
    "p4-m4-entry-gate-design-phase-terminal-closure-seal-inherited-prior-boundary-reference",
    "p4-m4-entry-gate-design-phase-terminal-closure-seal-static-seal-surface-definition",
    "p4-m4-entry-gate-design-phase-terminal-closure-seal-declaration-only-semantics-definition",
    "p4-m4-entry-gate-design-phase-terminal-closure-seal-validation-scoring-verdict-execution-record-mutation-p4-m5-start-semantics-disabled",
)

DATACLASS_FIELDS = {
    "field_order",
    "field_id",
    "field_name",
    "field_purpose",
    "p4_m4_entry_gate_design_phase_terminal_closure_seal_category",
    "p4_m4_entry_gate_design_phase_terminal_closure_seal_semantics_disabled",
}

REQUIRED_BOUNDARY_PHRASES = tuple(
    line
    for line in """
P4-M4.17
Entry Gate Design Phase Terminal Closure Seal
read-only
definition-only
entry-gate-design-phase-terminal-closure-seal-only
phase-terminal-closure-seal-surface-only
phase-terminal-closure-non-validation-boundary-only
phase-terminal-closure-non-scoring-boundary-only
phase-terminal-closure-non-verdict-boundary-only
phase-terminal-closure-non-execution-boundary-only
phase-terminal-closure-non-record-boundary-only
phase-terminal-closure-non-mutation-boundary-only
p4-m5-non-start-boundary-only
declaration-only
inspection-only
P4-M4.17 Entry Gate Design Phase Terminal Closure Seal is definition only
P4-M4.17 is entry-gate-design-phase-terminal-closure-seal-only
P4-M4.17 is phase-terminal-closure-seal-surface-only
P4-M4.17 is phase-terminal-closure-non-validation-boundary-only
P4-M4.17 is phase-terminal-closure-non-scoring-boundary-only
P4-M4.17 is phase-terminal-closure-non-verdict-boundary-only
P4-M4.17 is phase-terminal-closure-non-execution-boundary-only
P4-M4.17 is phase-terminal-closure-non-record-boundary-only
P4-M4.17 is phase-terminal-closure-non-mutation-boundary-only
P4-M4.17 is p4-m5-non-start-boundary-only
P4-M4.17 is declaration-only
P4-M4.16 Entry Gate Design Final Phase Handoff Summary remains the direct prior final phase handoff summary reference
P4-M4.16 final phase handoff summary remains only an inherited static final phase handoff summary surface reference
P4-M4.15 Entry Gate Design Phase Closure Review remains the inherited prior phase closure review reference
P4-M4.14 Entry Gate Design Closure Handoff Contract remains the inherited prior closure handoff contract reference
P4-M4.13 Entry Gate Design Final Non-Validation Boundary Audit remains the inherited prior final non-validation boundary audit reference
P4-M4.12 Declared Transition Package Assembly Envelope Contract remains the inherited prior declared transition package assembly envelope reference
P4-M4.11 Declared Transition Safeguard Envelope Contract remains the inherited prior declared transition safeguard envelope reference
P4-M4.10 Declared Transition Assumption Envelope Contract remains the inherited prior declared transition assumption envelope reference
P4-M4.9 Declared Transition Risk Envelope Contract remains the inherited prior declared transition risk envelope reference
P4-M4.8 Declared Transition Impact Envelope Contract remains the inherited prior declared transition impact envelope reference
P4-M4.7 Declared Transition Dependency Envelope Contract remains the inherited prior declared transition dependency envelope reference
P4-M4.6 Declared Transition Constraint Envelope Contract remains the inherited prior declared transition constraint envelope reference
P4-M4.5 Declared Transition Reason Envelope Contract remains the inherited prior declared transition reason envelope reference
P4-M4.4 Target Phase Envelope Contract remains the inherited prior target phase envelope reference
P4-M4.3 Declared Human Context Envelope Contract remains the inherited prior declared human context envelope reference
P4-M4.2 Evidence Reference Envelope Contract remains the inherited prior evidence reference envelope reference
P4-M4.1 Entry Gate Design Request Envelope Contract remains the inherited prior request envelope reference
P4-M4.0 Entry Gate Design Boundary Contract remains the inherited prior design boundary reference
P4-M3.16 Governed Transition Intake Final Phase Handoff Summary remains the inherited prior closed-phase handoff reference
P4-M3 static definition chain remains closed
P4-M4 design layer remains design-boundary-only
P4-M4 phase terminal closure seal starts only as a static declared seal surface
P4-M4 terminal closure validation remains not implemented
P4-M4 terminal closure scoring remains not implemented
P4-M4 terminal closure verdict remains not implemented
P4-M4 terminal closure execution remains not implemented
P4-M4 terminal closure record creation remains not implemented
P4-M4 terminal closure storage remains not implemented
P4-M4 terminal closure persistence remains not implemented
P4-M4 terminal closure mutation remains not implemented
P4-M4 final phase handoff validation remains not implemented
P4-M4 final phase handoff scoring remains not implemented
P4-M4 final phase handoff verdict remains not implemented
P4-M4 final phase handoff execution remains not implemented
P4-M4 phase closure validation remains not implemented
P4-M4 phase closure scoring remains not implemented
P4-M4 phase closure verdict remains not implemented
P4-M4 phase closure execution remains not implemented
P4-M4 closure handoff validation remains not implemented
P4-M4 closure handoff execution remains not implemented
P4-M4 final non-validation audit execution remains not implemented
P4-M4 entry gate validation remains not implemented
P4-M4 readiness validation remains not implemented
P4-M4 transition validation remains not implemented
P4-M4 package validation remains not implemented
P4-M4 package assembly validation remains not implemented
P4-M4 gate activation remains not implemented
P4-M4 verdict generation remains not implemented
P4-M4 approval remains not implemented
P4-M4 authorization remains not implemented
P4-M4 confirmation remains not implemented
P4-M4 recommendation remains not implemented
P4-M4 ranking remains not implemented
P4-M4 routing remains not implemented
P4-M4 planning remains not implemented
P4-M4 execution remains not implemented
P4-M4 record creation remains not implemented
P4-M4 storage remains not implemented
P4-M4 persistence remains not implemented
P4-M4 mutation remains not implemented
P4-M5 remains not started
v7 remains not started
productization remains not started
UI remains not started
Operator Console remains not started
no terminal closure validation
no terminal closure scoring
no terminal closure verdict
no terminal closure execution
no terminal closure record creation
no terminal closure storage
no terminal closure persistence
no terminal closure mutation
no final phase handoff validation
no final phase handoff scoring
no final phase handoff verdict
no final phase handoff execution
no phase closure validation
no phase closure scoring
no phase closure verdict
no phase closure execution
no closure handoff validation
no closure handoff execution
no final audit execution
no entry gate validation
no readiness validation
no transition validation
no package validation
no package assembly validation
no gate activation
no verdict generation
no approval
no authorization
no confirmation
no recommendation
no ranking
no routing
no planning
no execution
no record creation
no storage
no persistence
no mutation
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
    "P4-M4.17 Entry Gate Design Phase Terminal Closure Seal",
    "read-only",
    "definition-only",
    "entry-gate-design-phase-terminal-closure-seal-only",
    "phase-terminal-closure-seal-surface-only",
    "phase-terminal-closure-non-validation-boundary-only",
    "phase-terminal-closure-non-scoring-boundary-only",
    "phase-terminal-closure-non-verdict-boundary-only",
    "phase-terminal-closure-non-execution-boundary-only",
    "phase-terminal-closure-non-record-boundary-only",
    "phase-terminal-closure-non-mutation-boundary-only",
    "p4-m5-non-start-boundary-only",
    "declaration-only",
    "inspection-only",
    "P4-M4.16 Entry Gate Design Final Phase Handoff Summary remains the direct prior final phase handoff summary reference",
    "P4-M4.16 final phase handoff summary remains only an inherited static final phase handoff summary surface reference",
    "P4-M4 phase terminal closure seal starts only as a static declared seal surface",
    "P4-M4 terminal closure validation remains not implemented",
    "P4-M4 terminal closure scoring remains not implemented",
    "P4-M4 terminal closure verdict remains not implemented",
    "P4-M4 terminal closure execution remains not implemented",
    "P4-M5 remains not started",
    "no terminal closure validation",
    "no terminal closure scoring",
    "no terminal closure verdict",
    "no terminal closure execution",
    "no terminal closure record creation",
    "no gate activation",
    "no verdict generation",
    "no approval",
    "no authorization",
    "no confirmation",
    "no routing",
    "no planning",
    "no execution",
    "no record creation",
    "no storage",
    "no persistence",
    "no mutation",
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
entry_gate_design_phase_terminal_closure_seal_only
phase_terminal_closure_seal_surface_only
phase_terminal_closure_non_validation_boundary_only
phase_terminal_closure_non_scoring_boundary_only
phase_terminal_closure_non_verdict_boundary_only
phase_terminal_closure_non_execution_boundary_only
phase_terminal_closure_non_record_boundary_only
phase_terminal_closure_non_mutation_boundary_only
p4_m5_non_start_boundary_only
declaration_only
inspection_only
p4_m4_17_entry_gate_design_phase_terminal_closure_seal_started
p4_m4_17_definition_only
p4_m4_17_entry_gate_design_phase_terminal_closure_seal_only
p4_m4_17_phase_terminal_closure_seal_surface_only
p4_m4_17_phase_terminal_closure_non_validation_boundary_only
p4_m4_17_phase_terminal_closure_non_scoring_boundary_only
p4_m4_17_phase_terminal_closure_non_verdict_boundary_only
p4_m4_17_phase_terminal_closure_non_execution_boundary_only
p4_m4_17_phase_terminal_closure_non_record_boundary_only
p4_m4_17_phase_terminal_closure_non_mutation_boundary_only
p4_m4_17_p4_m5_non_start_boundary_only
p4_m4_17_declaration_only
p4_m4_16_final_phase_handoff_summary_reference_defined
p4_m4_16_final_phase_handoff_summary_static_reference_defined
p4_m4_15_phase_closure_review_reference_defined
p4_m4_14_closure_handoff_contract_reference_defined
p4_m4_13_final_non_validation_boundary_audit_reference_defined
p4_m4_12_declared_transition_package_assembly_envelope_contract_reference_defined
p4_m4_11_declared_transition_safeguard_envelope_contract_reference_defined
p4_m4_10_declared_transition_assumption_envelope_contract_reference_defined
p4_m4_9_declared_transition_risk_envelope_contract_reference_defined
p4_m4_8_declared_transition_impact_envelope_contract_reference_defined
p4_m4_7_declared_transition_dependency_envelope_contract_reference_defined
p4_m4_6_declared_transition_constraint_envelope_contract_reference_defined
p4_m4_5_declared_transition_reason_envelope_contract_reference_defined
p4_m4_4_target_phase_envelope_contract_reference_defined
p4_m4_3_declared_human_context_envelope_contract_reference_defined
p4_m4_2_evidence_reference_envelope_contract_reference_defined
p4_m4_1_entry_gate_design_request_envelope_contract_reference_defined
p4_m4_0_entry_gate_design_boundary_contract_reference_defined
p4_m3_16_final_phase_handoff_summary_reference_defined
p4_m3_static_definition_chain_closed_reference_defined
p4_m4_design_boundary_reference_defined
p4_m4_phase_terminal_closure_seal_surface_defined
p4_m4_phase_terminal_closure_non_validation_boundary_defined
p4_m4_phase_terminal_closure_non_scoring_boundary_defined
p4_m4_phase_terminal_closure_non_verdict_boundary_defined
p4_m4_phase_terminal_closure_non_execution_boundary_defined
p4_m4_phase_terminal_closure_non_record_boundary_defined
p4_m4_phase_terminal_closure_non_mutation_boundary_defined
p4_m4_p4_m5_non_start_boundary_defined
p4_m4_validation_semantics_prohibited
p4_m4_scoring_semantics_prohibited
p4_m4_verdict_semantics_prohibited
p4_m4_execution_semantics_prohibited
p4_m4_record_creation_semantics_prohibited
p4_m4_storage_semantics_prohibited
p4_m4_persistence_semantics_prohibited
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
terminal_closure_validation_enabled
terminal_closure_scoring_enabled
terminal_closure_verdict_enabled
terminal_closure_execution_enabled
terminal_closure_record_creation_enabled
terminal_closure_storage_enabled
terminal_closure_persistence_enabled
terminal_closure_mutation_enabled
final_phase_handoff_validation_enabled
final_phase_handoff_scoring_enabled
final_phase_handoff_verdict_enabled
final_phase_handoff_execution_enabled
final_phase_handoff_record_creation_enabled
final_phase_handoff_storage_enabled
final_phase_handoff_persistence_enabled
final_phase_handoff_mutation_enabled
phase_closure_validation_enabled
phase_closure_scoring_enabled
phase_closure_verdict_enabled
phase_closure_execution_enabled
phase_closure_record_creation_enabled
phase_closure_storage_enabled
phase_closure_persistence_enabled
phase_closure_mutation_enabled
closure_handoff_validation_enabled
closure_handoff_execution_enabled
closure_handoff_record_creation_enabled
closure_handoff_storage_enabled
closure_handoff_persistence_enabled
closure_handoff_mutation_enabled
final_audit_execution_enabled
live_audit_evaluation_enabled
entry_gate_validation_enabled
entry_readiness_validation_enabled
readiness_validation_enabled
transition_readiness_validation_enabled
transition_validation_enabled
package_validation_enabled
package_assembly_validation_enabled
package_assembly_enabled
package_composition_enabled
package_execution_enabled
package_assembly_scoring_enabled
package_assembly_routing_enabled
package_assembly_planning_enabled
package_assembly_graph_enabled
package_assembly_graph_construction_enabled
transition_package_assembly_validation_enabled
transition_package_assembly_composition_enabled
transition_package_assembly_execution_enabled
transition_package_assembly_scoring_enabled
transition_package_assembly_routing_enabled
transition_package_assembly_planning_enabled
transition_safeguard_validation_enabled
transition_safeguard_enforcement_enabled
transition_safeguard_execution_enabled
transition_safeguard_mitigation_enabled
transition_assumption_validation_enabled
transition_risk_validation_enabled
transition_impact_validation_enabled
transition_dependency_validation_enabled
transition_constraint_validation_enabled
transition_reason_validation_enabled
target_phase_validation_enabled
phase_transition_validation_enabled
readiness_scoring_enabled
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
semantic_target_field_graph_enabled
human_context_validation_enabled
identity_validation_enabled
consent_validation_enabled
authority_validation_enabled
approval_validation_enabled
authorization_validation_enabled
confirmation_validation_enabled
evidence_validation_enabled
reference_resolution_enabled
reference_validation_enabled
citation_validation_enabled
source_fetching_enabled
provenance_writing_enabled
request_intake_enabled
request_validation_enabled
boundary_validation_enabled
phase_validation_enabled
governed_transition_intake_validation_enabled
closure_validation_enabled
handoff_validation_enabled
working_entry_gate_enabled
gate_activation_enabled
gate_execution_enabled
p4_m4_execution_enabled
operational_behavior_enabled
readiness_verdict_enabled
validation_verdict_enabled
audit_verdict_enabled
closure_handoff_verdict_enabled
transition_verdict_enabled
entry_verdict_enabled
gate_verdict_enabled
approval_enabled
authorization_enabled
confirmation_enabled
recommendation_enabled
ranking_enabled
routing_enabled
planning_enabled
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
terminal_closure_state_mutation_enabled
final_phase_handoff_state_mutation_enabled
phase_closure_state_mutation_enabled
closure_handoff_state_mutation_enabled
final_non_validation_audit_mutation_enabled
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
    "p4-m6-4-entry-rejection-non-execution-surface",
    "p4-m6-5-entry-escalation-non-routing-surface",
    "p4-m6-6-entry-exception-non-override-surface",
    "p4-m6-7-entry-conflict-non-resolution-surface",
    "p4-m6-8-entry-ambiguity-non-inference-surface",
    "p4-m6-9-entry-dependency-non-activation-surface",
    "p4-m6-10-entry-constraint-non-enforcement-surface",
    "p4-m6-11-entry-risk-non-mitigation-surface",
    "p4-m6-12-entry-safeguard-non-activation-surface",
}


def test_field_inventory_is_exact_and_ordered():
    fields = list_entry_gate_design_phase_terminal_closure_seal_fields()

    assert len(fields) == 23
    assert entry_gate_design_phase_terminal_closure_seal_field_ids() == FIELD_IDS
    assert tuple(field.field_order for field in fields) == tuple(range(1, 24))
    assert all(
        isinstance(field, EntryGateDesignPhaseTerminalClosureSealField)
        for field in fields
    )
    assert {
        field.name
        for field in dataclasses.fields(EntryGateDesignPhaseTerminalClosureSealField)
    } == DATACLASS_FIELDS


def test_boundary_phrase_inventory_is_required_contract():
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in BOUNDARY_PHRASE_LINES
        assert phrase in ENTRY_GATE_DESIGN_PHASE_TERMINAL_CLOSURE_SEAL_BOUNDARY


def test_markdown_renders_static_boundary_and_field_ids():
    markdown = render_entry_gate_design_phase_terminal_closure_seal_markdown()

    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in markdown
    for field_id in FIELD_IDS:
        assert field_id in markdown
    assert "## Status Report" in markdown
    assert "## Entry Gate Design Phase Terminal Closure Seal Fields" in markdown
    assert "P4-M4.17 Entry Gate Design Phase Terminal Closure Seal" in markdown


def test_report_has_required_true_false_status_flags():
    status = entry_gate_design_phase_terminal_closure_seal_report()

    assert status["phase"] == "P4-M4.17"
    assert status["feature"] == "Entry Gate Design Phase Terminal Closure Seal"
    assert status["mode"] == "read-only"
    assert status["package_version"] == "6.16.0"
    assert status["entry_gate_design_phase_terminal_closure_seal_field_count"] == 23
    assert (
        status[
            "referenced_p4_m4_16_entry_gate_design_final_phase_handoff_summary_field_count"
        ]
        == 23
    )
    assert TRUE_STATUS_FLAGS == EXPECTED_TRUE_STATUS_FLAGS
    assert FALSE_STATUS_FLAGS == EXPECTED_FALSE_STATUS_FLAGS
    for flag in EXPECTED_TRUE_STATUS_FLAGS:
        assert status[flag] is True
    for flag in EXPECTED_FALSE_STATUS_FLAGS:
        assert status[flag] is False


def test_as_dicts_is_deterministic_and_read_only_shape():
    fields = entry_gate_design_phase_terminal_closure_seal_as_dicts()

    assert len(fields) == 23
    assert tuple(field["field_id"] for field in fields) == FIELD_IDS
    assert fields == entry_gate_design_phase_terminal_closure_seal_as_dicts()
    assert all(
        field["p4_m4_entry_gate_design_phase_terminal_closure_seal_category"]
        == "p4-m4-entry-gate-design-phase-terminal-closure-seal-category"
        for field in fields
    )


def test_operator_markdown_command_is_read_only_and_pre_store(
    monkeypatch, tmp_path: Path
):
    def fail_store_creation(*_args, **_kwargs):
        raise AssertionError("workspace store must not be created")

    monkeypatch.setattr(
        operator,
        "create_workspace_subspace_memory_store",
        fail_store_creation,
    )

    code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "entry-gate-design-phase-terminal-closure-seal",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith(
        "# P4-M4.17 Entry Gate Design Phase Terminal Closure Seal\n"
    )
    for phrase in OPERATOR_SMOKE_PHRASES:
        assert phrase in stdout
    assert not (tmp_path / ".local" / "subspace_memory").exists()


def test_operator_json_command_returns_required_report(tmp_path: Path):
    code, output, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "entry-gate-design-phase-terminal-closure-seal",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert code == 0
    assert stderr == ""
    assert stdout.startswith("{")
    assert output["count"] == 23
    assert output["boundary"] == ENTRY_GATE_DESIGN_PHASE_TERMINAL_CLOSURE_SEAL_BOUNDARY
    assert tuple(field["field_id"] for field in output["fields"]) == FIELD_IDS
    status = output["status"]
    assert status["phase"] == "P4-M4.17"
    assert status["feature"] == "Entry Gate Design Phase Terminal Closure Seal"
    assert status["mode"] == "read-only"
    for flag in EXPECTED_TRUE_STATUS_FLAGS:
        assert status[flag] is True
    for flag in EXPECTED_FALSE_STATUS_FLAGS:
        assert status[flag] is False
    assert not (tmp_path / ".local" / "subspace_memory").exists()


def test_parser_exposes_only_expected_memory_loop_command_surface():
    commands = _memory_loop_subcommands(build_parser())

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
    assert "entry-gate-design-phase-terminal-closure-seal" in commands


def test_pyproject_entry_points_do_not_productize_command():
    pyproject = tomllib.loads(Path("pyproject.toml").read_text())
    entry_points = pyproject["project"]["entry-points"]

    assert "entry-gate-design-phase-terminal-closure-seal" not in entry_points
    assert "entry-gate-design-phase-terminal-closure-seal" not in str(entry_points)
    assert pyproject["project"]["version"] == "6.16.0"


def test_static_doc_contains_required_boundaries_and_fields():
    project_root = Path(__file__).resolve().parents[1]
    doc_path = (
        project_root
        / "docs"
        / "CIVILIZATION_CORE_P4_M4_17_ENTRY_GATE_DESIGN_PHASE_TERMINAL_CLOSURE_SEAL.md"
    )
    doc = doc_path.read_text(encoding="utf-8")

    assert doc.startswith(
        "# P4-M4.17 Entry Gate Design Phase Terminal Closure Seal\n"
    )
    for field_id in FIELD_IDS:
        assert field_id in doc
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in doc


def test_custom_field_rendering_remains_definition_only():
    field = EntryGateDesignPhaseTerminalClosureSealField(
        field_order=99,
        field_id="custom-entry-gate-design-phase-terminal-closure-seal",
        field_name="Custom Entry Gate Design Phase Terminal Closure Seal",
        field_purpose="custom read-only definition-only inspection-only field",
        p4_m4_entry_gate_design_phase_terminal_closure_seal_category=(
            "custom-entry-gate-design-phase-terminal-closure-seal-category"
        ),
        p4_m4_entry_gate_design_phase_terminal_closure_seal_semantics_disabled=(
            "no validation semantics; no execution semantics; no mutation semantics"
        ),
    )

    markdown = render_entry_gate_design_phase_terminal_closure_seal_markdown((field,))

    assert "custom-entry-gate-design-phase-terminal-closure-seal" in markdown
    assert "no validation semantics; no execution semantics" in markdown
    assert "P4-M4.17 Entry Gate Design Phase Terminal Closure Seal" in markdown


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
