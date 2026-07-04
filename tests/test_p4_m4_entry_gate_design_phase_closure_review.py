from __future__ import annotations

import argparse
import io
import json
import tomllib
from pathlib import Path

from hermes_memory_fabric.p4_m0_subspace_operator import build_parser, run_operator_command
from hermes_memory_fabric.p4_m4_entry_gate_design_phase_closure_review import (
    BOUNDARY_PHRASE_LINES,
    ENTRY_GATE_DESIGN_PHASE_CLOSURE_REVIEW_BOUNDARY,
    FALSE_STATUS_FLAGS,
    TRUE_STATUS_FLAGS,
    EntryGateDesignPhaseClosureReviewField,
    entry_gate_design_phase_closure_review_as_dicts,
    entry_gate_design_phase_closure_review_field_ids,
    entry_gate_design_phase_closure_review_report,
    list_entry_gate_design_phase_closure_review_fields,
    render_entry_gate_design_phase_closure_review_markdown,
)


FIELD_IDS = (
    "p4-m4-entry-gate-design-phase-closure-review-id",
    "p4-m4-entry-gate-design-phase-closure-review-phase",
    "p4-m4-entry-gate-design-phase-closure-review-mode",
    "p4-m4-entry-gate-design-phase-closure-review-direct-prior-closure-handoff-contract-reference",
    "p4-m4-entry-gate-design-phase-closure-review-inherited-prior-final-non-validation-boundary-audit-reference",
    "p4-m4-entry-gate-design-phase-closure-review-inherited-prior-declared-transition-package-assembly-envelope-reference",
    "p4-m4-entry-gate-design-phase-closure-review-inherited-prior-declared-transition-safeguard-envelope-reference",
    "p4-m4-entry-gate-design-phase-closure-review-inherited-prior-declared-transition-assumption-envelope-reference",
    "p4-m4-entry-gate-design-phase-closure-review-inherited-prior-declared-transition-risk-envelope-reference",
    "p4-m4-entry-gate-design-phase-closure-review-inherited-prior-declared-transition-impact-envelope-reference",
    "p4-m4-entry-gate-design-phase-closure-review-inherited-prior-declared-transition-dependency-envelope-reference",
    "p4-m4-entry-gate-design-phase-closure-review-inherited-prior-declared-transition-constraint-envelope-reference",
    "p4-m4-entry-gate-design-phase-closure-review-inherited-prior-declared-transition-reason-envelope-reference",
    "p4-m4-entry-gate-design-phase-closure-review-inherited-prior-target-phase-envelope-reference",
    "p4-m4-entry-gate-design-phase-closure-review-inherited-prior-declared-human-context-envelope-reference",
    "p4-m4-entry-gate-design-phase-closure-review-inherited-prior-evidence-reference-envelope-reference",
    "p4-m4-entry-gate-design-phase-closure-review-inherited-prior-request-envelope-reference",
    "p4-m4-entry-gate-design-phase-closure-review-inherited-prior-boundary-reference",
    "p4-m4-entry-gate-design-phase-closure-review-inherited-prior-closed-phase-handoff-reference",
    "p4-m4-entry-gate-design-phase-closure-review-scope",
    "p4-m4-entry-gate-design-phase-closure-review-static-review-surface-definition",
    "p4-m4-entry-gate-design-phase-closure-review-declaration-only-semantics-definition",
    "p4-m4-entry-gate-design-phase-closure-review-validation-scoring-verdict-execution-record-mutation-p4-m5-start-semantics-disabled",
)

DATACLASS_FIELDS = {
    "field_order",
    "field_id",
    "field_name",
    "field_purpose",
    "p4_m4_entry_gate_design_phase_closure_review_category",
    "p4_m4_entry_gate_design_phase_closure_review_semantics_disabled",
}

REQUIRED_BOUNDARY_PHRASES = tuple(
    line
    for line in """
P4-M4.15
Entry Gate Design Phase Closure Review
read-only
definition-only
entry-gate-design-phase-closure-review-only
phase-closure-review-surface-only
phase-closure-non-validation-boundary-only
phase-closure-non-scoring-boundary-only
phase-closure-non-verdict-boundary-only
phase-closure-non-execution-boundary-only
phase-closure-non-record-boundary-only
phase-closure-non-mutation-boundary-only
p4-m5-non-start-boundary-only
declaration-only
inspection-only
P4-M4.15 Entry Gate Design Phase Closure Review is definition only
P4-M4.15 is entry-gate-design-phase-closure-review-only
P4-M4.15 is phase-closure-review-surface-only
P4-M4.15 is phase-closure-non-validation-boundary-only
P4-M4.15 is phase-closure-non-scoring-boundary-only
P4-M4.15 is phase-closure-non-verdict-boundary-only
P4-M4.15 is phase-closure-non-execution-boundary-only
P4-M4.15 is phase-closure-non-record-boundary-only
P4-M4.15 is phase-closure-non-mutation-boundary-only
P4-M4.15 is p4-m5-non-start-boundary-only
P4-M4.15 is declaration-only
P4-M4.14 Entry Gate Design Closure Handoff Contract remains the direct prior closure handoff contract reference
P4-M4.14 closure handoff contract remains only an inherited static closure handoff surface reference
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
P4-M4 phase closure review starts only as a static declared review surface
P4-M4 phase closure validation remains not implemented
P4-M4 phase closure scoring remains not implemented
P4-M4 phase closure verdict remains not implemented
P4-M4 phase closure execution remains not implemented
P4-M4 phase closure record creation remains not implemented
P4-M4 phase closure storage remains not implemented
P4-M4 phase closure persistence remains not implemented
P4-M4 phase closure mutation remains not implemented
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
no phase closure validation
no phase closure scoring
no phase closure verdict
no phase closure execution
no phase closure record creation
no phase closure storage
no phase closure persistence
no phase closure mutation
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
    "P4-M4.15 Entry Gate Design Phase Closure Review",
    "read-only",
    "definition-only",
    "entry-gate-design-phase-closure-review-only",
    "phase-closure-review-surface-only",
    "phase-closure-non-validation-boundary-only",
    "phase-closure-non-scoring-boundary-only",
    "phase-closure-non-verdict-boundary-only",
    "phase-closure-non-execution-boundary-only",
    "phase-closure-non-record-boundary-only",
    "phase-closure-non-mutation-boundary-only",
    "p4-m5-non-start-boundary-only",
    "declaration-only",
    "inspection-only",
    "P4-M4.14 Entry Gate Design Closure Handoff Contract remains the direct prior closure handoff contract reference",
    "P4-M4.14 closure handoff contract remains only an inherited static closure handoff surface reference",
    "P4-M4 phase closure review starts only as a static declared review surface",
    "P4-M4 phase closure validation remains not implemented",
    "P4-M4 phase closure scoring remains not implemented",
    "P4-M4 phase closure verdict remains not implemented",
    "P4-M4 phase closure execution remains not implemented",
    "P4-M5 remains not started",
    "no phase closure validation",
    "no phase closure scoring",
    "no phase closure verdict",
    "no phase closure execution",
    "no phase closure record creation",
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
entry_gate_design_phase_closure_review_only
phase_closure_review_surface_only
phase_closure_non_validation_boundary_only
phase_closure_non_scoring_boundary_only
phase_closure_non_verdict_boundary_only
phase_closure_non_execution_boundary_only
phase_closure_non_record_boundary_only
phase_closure_non_mutation_boundary_only
p4_m5_non_start_boundary_only
declaration_only
inspection_only
p4_m4_15_entry_gate_design_phase_closure_review_started
p4_m4_15_definition_only
p4_m4_15_entry_gate_design_phase_closure_review_only
p4_m4_15_phase_closure_review_surface_only
p4_m4_15_phase_closure_non_validation_boundary_only
p4_m4_15_phase_closure_non_scoring_boundary_only
p4_m4_15_phase_closure_non_verdict_boundary_only
p4_m4_15_phase_closure_non_execution_boundary_only
p4_m4_15_phase_closure_non_record_boundary_only
p4_m4_15_phase_closure_non_mutation_boundary_only
p4_m4_15_p4_m5_non_start_boundary_only
p4_m4_15_declaration_only
p4_m4_14_closure_handoff_contract_reference_defined
p4_m4_14_closure_handoff_contract_static_reference_defined
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
p4_m4_phase_closure_review_surface_defined
p4_m4_phase_closure_non_validation_boundary_defined
p4_m4_phase_closure_non_scoring_boundary_defined
p4_m4_phase_closure_non_verdict_boundary_defined
p4_m4_phase_closure_non_execution_boundary_defined
p4_m4_phase_closure_non_record_boundary_defined
p4_m4_phase_closure_non_mutation_boundary_defined
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
final_phase_handoff_validation_enabled
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
}

PROHIBITED_MEMORY_LOOP_COMMANDS = {
    "validate-phase-closure",
    "score-phase-closure",
    "generate-closure-verdict",
    "execute-closure",
    "validate-entry-gate",
    "validate-readiness",
    "validate-transition",
    "validate-package",
    "validate-package-assembly",
    "execute-handoff",
    "activate-gate",
    "start-p4-m5",
    "start-v7",
    "final-audit-execution",
    "live-audit-evaluation",
    "generate-verdict",
    "approve",
    "authorize",
    "confirm",
    "recommend",
    "rank",
    "route",
    "plan",
    "next-action",
    "execute-transition",
    "create-record",
    "write-memory",
    "productize",
    "operator-console",
    "ui",
}


def test_entry_gate_design_phase_closure_review_field_order_count_and_ids_are_stable():
    fields = list_entry_gate_design_phase_closure_review_fields()

    assert [field.field_order for field in fields] == list(range(1, 24))
    assert len(fields) == 23
    assert entry_gate_design_phase_closure_review_field_ids() == FIELD_IDS


def test_every_entry_gate_design_phase_closure_review_field_has_required_values():
    for field in list_entry_gate_design_phase_closure_review_fields():
        assert field.field_name.strip()
        assert field.field_purpose.strip()
        assert field.p4_m4_entry_gate_design_phase_closure_review_category.strip()
        assert (
            field.p4_m4_entry_gate_design_phase_closure_review_semantics_disabled.strip()
        )


def test_required_boundary_phrase_contract_contains_all_required_phrases():
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in BOUNDARY_PHRASE_LINES
        assert phrase in ENTRY_GATE_DESIGN_PHASE_CLOSURE_REVIEW_BOUNDARY
    for phrase in OPERATOR_SMOKE_PHRASES:
        assert (
            phrase in BOUNDARY_PHRASE_LINES
            or phrase in ENTRY_GATE_DESIGN_PHASE_CLOSURE_REVIEW_BOUNDARY
        )


def test_status_flag_contract_contains_exact_required_keys():
    assert TRUE_STATUS_FLAGS == EXPECTED_TRUE_STATUS_FLAGS
    assert FALSE_STATUS_FLAGS == EXPECTED_FALSE_STATUS_FLAGS


def test_markdown_output_is_stable_and_contains_required_boundaries():
    first = render_entry_gate_design_phase_closure_review_markdown()
    second = render_entry_gate_design_phase_closure_review_markdown()

    assert first == second
    assert first.startswith("# P4-M4.15 Entry Gate Design Phase Closure Review\n")
    assert ENTRY_GATE_DESIGN_PHASE_CLOSURE_REVIEW_BOUNDARY in first
    for field_id in FIELD_IDS:
        assert field_id in first
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in first


def test_json_output_is_stable_and_contains_required_boundaries(tmp_path):
    args = [
        "memory-loop",
        "entry-gate-design-phase-closure-review",
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
    assert first_payload["boundary"] == ENTRY_GATE_DESIGN_PHASE_CLOSURE_REVIEW_BOUNDARY
    assert first_payload["count"] == 23
    assert first_payload["status"]["phase"] == "P4-M4.15"
    assert first_payload["status"]["feature"] == "Entry Gate Design Phase Closure Review"
    assert first_payload["status"]["mode"] == "read-only"
    assert first_payload["status"] == entry_gate_design_phase_closure_review_report()
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
    first_fields = entry_gate_design_phase_closure_review_as_dicts()
    second_fields = entry_gate_design_phase_closure_review_as_dicts()
    first_status = entry_gate_design_phase_closure_review_report()
    second_status = entry_gate_design_phase_closure_review_report()

    assert first_fields == second_fields
    assert [field["field_id"] for field in first_fields] == list(FIELD_IDS)
    assert first_status == second_status
    assert first_status["phase"] == "P4-M4.15"
    assert first_status["feature"] == "Entry Gate Design Phase Closure Review"
    assert first_status["mode"] == "read-only"
    assert first_status["entry_gate_design_phase_closure_review_field_count"] == 23
    assert (
        first_status[
            "referenced_p4_m4_14_entry_gate_design_closure_handoff_contract_field_count"
        ]
        == 23
    )


def test_status_report_locks_true_and_disabled_flags():
    status = entry_gate_design_phase_closure_review_report()

    for flag in EXPECTED_TRUE_STATUS_FLAGS:
        assert status[flag] is True
    for flag in EXPECTED_FALSE_STATUS_FLAGS:
        assert status[flag] is False


def test_operator_markdown_default_is_read_only_and_creates_no_local_storage(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "entry-gate-design-phase-closure-review",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M4.15 Entry Gate Design Phase Closure Review\n")
    assert "## Status Report" in stdout
    assert ENTRY_GATE_DESIGN_PHASE_CLOSURE_REVIEW_BOUNDARY in stdout
    for phrase in OPERATOR_SMOKE_PHRASES:
        assert phrase in stdout
    assert not (tmp_path / ".local").exists()


def test_operator_markdown_format_is_explicit_and_stable(tmp_path):
    args = [
        "memory-loop",
        "entry-gate-design-phase-closure-review",
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
    assert first_stdout.startswith("# P4-M4.15")
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
            "entry-gate-design-phase-closure-review",
            "--workspace-root",
            str(tmp_path),
        ]
    )
    json_code, json_payload, json_stderr, _ = _run_operator(
        [
            "memory-loop",
            "entry-gate-design-phase-closure-review",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert markdown_code == 0
    assert markdown_stderr == ""
    assert markdown_stdout.startswith("# P4-M4.15")
    assert json_code == 0
    assert json_stderr == ""
    assert json_payload["count"] == 23
    assert not (tmp_path / ".local").exists()


def test_command_creates_no_storage_files_or_state_changes(tmp_path):
    _run_operator(
        [
            "memory-loop",
            "entry-gate-design-phase-closure-review",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    storage_root = tmp_path / ".local" / "subspace_memory"
    for filename in (
        "entry_gate_design_phase_closure_review.jsonl",
        "phase_closure_validation.jsonl",
        "phase_closure_scoring.jsonl",
        "phase_closure_verdict.jsonl",
        "phase_closure_execution.jsonl",
        "phase_closure_record_creation.jsonl",
        "phase_closure_storage.jsonl",
        "phase_closure_persistence.jsonl",
        "phase_closure_mutation.jsonl",
        "closure_handoff_validation.jsonl",
        "closure_handoff_execution.jsonl",
        "final_non_validation_audit_execution.jsonl",
        "entry_gate_validation.jsonl",
        "readiness_validation.jsonl",
        "transition_validation.jsonl",
        "package_validation.jsonl",
        "package_assembly_validation.jsonl",
        "gate_activation.jsonl",
        "verdict_generation.jsonl",
        "approval.jsonl",
        "authorization.jsonl",
        "confirmation.jsonl",
        "routing.jsonl",
        "planning.jsonl",
        "execution.jsonl",
        "record_creation.jsonl",
        "storage.jsonl",
        "persistence.jsonl",
        "mutation.jsonl",
    ):
        assert not (storage_root / filename).exists()
    assert not storage_root.exists()


def test_parser_exposes_only_expected_memory_loop_command_surface():
    commands = _memory_loop_subcommands(build_parser())

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
    assert "entry-gate-design-phase-closure-review" in commands
    assert not (commands & PROHIBITED_MEMORY_LOOP_COMMANDS)


def test_command_is_not_packaged_as_top_level_entry_point():
    entry_points = _project_entry_points()

    assert "entry-gate-design-phase-closure-review" not in entry_points
    assert "entry-gate-design-phase-closure-review" not in str(entry_points)


def test_static_doc_contains_required_boundaries_and_fields():
    project_root = Path(__file__).resolve().parents[1]
    doc_path = (
        project_root
        / "docs"
        / "CIVILIZATION_CORE_P4_M4_15_ENTRY_GATE_DESIGN_PHASE_CLOSURE_REVIEW.md"
    )
    doc = doc_path.read_text(encoding="utf-8")

    assert doc.startswith("# P4-M4.15 Entry Gate Design Phase Closure Review\n")
    for field_id in FIELD_IDS:
        assert field_id in doc
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in doc


def test_custom_field_rendering_remains_definition_only():
    custom = EntryGateDesignPhaseClosureReviewField(
        field_order=24,
        field_id="custom-entry-gate-design-phase-closure-review",
        field_name="Custom Entry Gate Design Phase Closure Review Field",
        field_purpose="Custom read-only phase closure review surface field.",
        p4_m4_entry_gate_design_phase_closure_review_category=(
            "custom-entry-gate-design-phase-closure-review-category"
        ),
        p4_m4_entry_gate_design_phase_closure_review_semantics_disabled=(
            "no validation semantics"
        ),
    )

    markdown = render_entry_gate_design_phase_closure_review_markdown([custom])

    assert "custom-entry-gate-design-phase-closure-review" in markdown
    assert "Custom read-only phase closure review surface field." in markdown
    assert ENTRY_GATE_DESIGN_PHASE_CLOSURE_REVIEW_BOUNDARY in markdown


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
