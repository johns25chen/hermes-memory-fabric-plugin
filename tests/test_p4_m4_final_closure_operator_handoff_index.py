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
from hermes_memory_fabric.p4_m4_final_closure_operator_handoff_index import (
    BOUNDARY_PHRASE_LINES,
    FALSE_STATUS_FLAGS,
    P4_M4_FINAL_CLOSURE_OPERATOR_HANDOFF_INDEX_BOUNDARY,
    TRUE_STATUS_FLAGS,
    P4M4FinalClosureOperatorHandoffIndexField,
    list_p4_m4_final_closure_operator_handoff_index_fields,
    p4_m4_final_closure_operator_handoff_index_as_dicts,
    p4_m4_final_closure_operator_handoff_index_field_ids,
    p4_m4_final_closure_operator_handoff_index_report,
    render_p4_m4_final_closure_operator_handoff_index_markdown,
)


FIELD_IDS = (
    "p4-m4-final-closure-operator-handoff-index-id",
    "p4-m4-final-closure-operator-handoff-index-phase",
    "p4-m4-final-closure-operator-handoff-index-mode",
    "p4-m4-final-closure-operator-handoff-index-direct-prior-final-closure-evidence-index-reference",
    "p4-m4-final-closure-operator-handoff-index-inherited-prior-final-closure-index-entry-planning-gate-reference",
    "p4-m4-final-closure-operator-handoff-index-inherited-prior-terminal-closure-seal-reference",
    "p4-m4-final-closure-operator-handoff-index-inherited-prior-final-phase-handoff-summary-reference",
    "p4-m4-final-closure-operator-handoff-index-inherited-prior-phase-closure-review-reference",
    "p4-m4-final-closure-operator-handoff-index-inherited-prior-closure-handoff-contract-reference",
    "p4-m4-final-closure-operator-handoff-index-inherited-prior-final-non-validation-boundary-audit-reference",
    "p4-m4-final-closure-operator-handoff-index-inherited-prior-declared-transition-package-assembly-envelope-reference",
    "p4-m4-final-closure-operator-handoff-index-inherited-prior-declared-transition-safeguard-envelope-reference",
    "p4-m4-final-closure-operator-handoff-index-inherited-prior-declared-transition-assumption-envelope-reference",
    "p4-m4-final-closure-operator-handoff-index-inherited-prior-declared-transition-risk-envelope-reference",
    "p4-m4-final-closure-operator-handoff-index-inherited-prior-declared-transition-impact-envelope-reference",
    "p4-m4-final-closure-operator-handoff-index-inherited-prior-declared-transition-dependency-envelope-reference",
    "p4-m4-final-closure-operator-handoff-index-inherited-prior-declared-transition-constraint-envelope-reference",
    "p4-m4-final-closure-operator-handoff-index-inherited-prior-declared-transition-reason-envelope-reference",
    "p4-m4-final-closure-operator-handoff-index-inherited-prior-target-phase-envelope-reference",
    "p4-m4-final-closure-operator-handoff-index-inherited-prior-declared-human-context-envelope-reference",
    "p4-m4-final-closure-operator-handoff-index-inherited-prior-evidence-reference-envelope-reference",
    "p4-m4-final-closure-operator-handoff-index-inherited-prior-request-envelope-and-boundary-reference",
    "p4-m4-final-closure-operator-handoff-index-static-operator-handoff-and-validation-scoring-verdict-execution-record-mutation-semantics-disabled",
)

DATACLASS_FIELDS = {
    "field_order",
    "field_id",
    "field_name",
    "field_purpose",
    "p4_m4_final_closure_operator_handoff_index_category",
    "p4_m4_final_closure_operator_handoff_index_semantics_disabled",
}

REQUIRED_BOUNDARY_PHRASES = tuple(
    line
    for line in """
P4-M4-FC.2
P4-M4 Final Closure Operator Handoff Index
read-only
definition-only
p4-m4-final-closure-operator-handoff-index-only
operator-handoff-index-only
operator-handoff-non-validation-boundary-only
operator-handoff-non-scoring-boundary-only
operator-handoff-non-verdict-boundary-only
operator-handoff-non-execution-boundary-only
operator-handoff-non-record-boundary-only
operator-handoff-non-mutation-boundary-only
p4-m5-non-start-boundary-only
declaration-only
inspection-only
P4-M4-FC.2 is not P4-M4.18
P4-M4-FC.2 is not P4-M5
P4-M4-FC.2 P4-M4 Final Closure Operator Handoff Index is definition only
P4-M4-FC.2 is p4-m4-final-closure-operator-handoff-index-only
P4-M4-FC.2 is operator-handoff-index-only
P4-M4-FC.2 is operator-handoff-non-validation-boundary-only
P4-M4-FC.2 is operator-handoff-non-scoring-boundary-only
P4-M4-FC.2 is operator-handoff-non-verdict-boundary-only
P4-M4-FC.2 is operator-handoff-non-execution-boundary-only
P4-M4-FC.2 is operator-handoff-non-record-boundary-only
P4-M4-FC.2 is operator-handoff-non-mutation-boundary-only
P4-M4-FC.2 is p4-m5-non-start-boundary-only
P4-M4-FC.2 is declaration-only
P4-M4-FC.1 P4-M4 Final Closure Evidence Index remains the direct prior final closure evidence index reference
P4-M4-FC.1 remains only an inherited static final closure evidence index surface reference
P4-M4-FC.0 P4-M4 Final Closure Index / P4-M5 Entry Planning Gate remains the inherited prior final closure index and entry planning gate reference
P4-M4.17 Entry Gate Design Phase Terminal Closure Seal remains the inherited prior terminal closure seal reference
P4-M4.16 Entry Gate Design Final Phase Handoff Summary remains the inherited prior final phase handoff summary reference
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
P4-M3.16 Governed Transition Intake Final Phase Handoff Summary remains the inherited prior closed-phase handoff context reference
P4-M4 static definition chain remains closed
P4-M4 design layer remains terminally sealed
P4-M4 final closure operator handoff index starts only as a static declared operator handoff index surface
P4-M4 operator handoff references remain static reference-only entries
operator handoff validation remains not implemented
operator handoff scoring remains not implemented
operator handoff verdict remains not implemented
operator handoff execution remains not implemented
operator handoff record creation remains not implemented
operator handoff storage remains not implemented
operator handoff persistence remains not implemented
operator handoff mutation remains not implemented
P4-M4 evidence validation remains not implemented
P4-M5 entry validation remains not implemented
P4-M5 readiness validation remains not implemented
P4-M5 entry scoring remains not implemented
P4-M5 entry verdict remains not implemented
P4-M5 entry execution remains not implemented
P4-M5 start remains not implemented
P4-M4.18 remains not started
P4-M5 remains not started
v7 remains not started
productization remains not started
UI remains not started
Operator Console remains not started
no P4-M4.18
no P4-M5 implementation
no P4-M5 entry validation
no P4-M5 readiness validation
no P4-M5 entry scoring
no P4-M5 entry verdict
no P4-M5 entry execution
no P4-M5 start
no operator handoff validation
no operator handoff scoring
no operator handoff verdict
no operator handoff execution
no operator handoff record creation
no operator handoff storage
no operator handoff persistence
no operator handoff mutation
no evidence validation
no evidence scoring
no evidence verdict
no evidence execution
no validation
no scoring
no verdict
no approval
no authorization
no confirmation
no recommendation
no ranking
no routing
no executable planning
no execution
no record creation
no storage
no persistence
no mutation
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
    "P4-M4-FC.2 P4-M4 Final Closure Operator Handoff Index",
    "read-only",
    "definition-only",
    "p4-m4-final-closure-operator-handoff-index-only",
    "operator-handoff-index-only",
    "operator-handoff-non-validation-boundary-only",
    "operator-handoff-non-scoring-boundary-only",
    "operator-handoff-non-verdict-boundary-only",
    "operator-handoff-non-execution-boundary-only",
    "operator-handoff-non-record-boundary-only",
    "operator-handoff-non-mutation-boundary-only",
    "p4-m5-non-start-boundary-only",
    "declaration-only",
    "inspection-only",
    "P4-M4-FC.2 is not P4-M4.18",
    "P4-M4-FC.2 is not P4-M5",
    "P4-M4-FC.1 P4-M4 Final Closure Evidence Index remains the direct prior final closure evidence index reference",
    "P4-M4-FC.0 P4-M4 Final Closure Index / P4-M5 Entry Planning Gate remains the inherited prior final closure index and entry planning gate reference",
    "P4-M4.17 Entry Gate Design Phase Terminal Closure Seal remains the inherited prior terminal closure seal reference",
    "P4-M4 static definition chain remains closed",
    "P4-M4 design layer remains terminally sealed",
    "P4-M4 final closure operator handoff index starts only as a static declared operator handoff index surface",
    "P4-M4 operator handoff references remain static reference-only entries",
    "operator handoff validation remains not implemented",
    "P4-M5 entry validation remains not implemented",
    "P4-M5 readiness validation remains not implemented",
    "P4-M5 entry verdict remains not implemented",
    "P4-M5 start remains not implemented",
    "P4-M4.18 remains not started",
    "P4-M5 remains not started",
    "v7 remains not started",
    "no P4-M4.18",
    "no P4-M5 implementation",
    "no P4-M5 entry validation",
    "no P4-M5 readiness validation",
    "no P4-M5 entry scoring",
    "no P4-M5 entry verdict",
    "no P4-M5 entry execution",
    "no P4-M5 start",
    "no operator handoff validation",
    "no operator handoff scoring",
    "no operator handoff verdict",
    "no operator handoff execution",
    "no operator handoff record creation",
    "no operator handoff storage",
    "no operator handoff persistence",
    "no operator handoff mutation",
    "no evidence validation",
    "no evidence scoring",
    "no evidence verdict",
    "no evidence execution",
    "no validation",
    "no scoring",
    "no verdict",
    "no approval",
    "no authorization",
    "no confirmation",
    "no recommendation",
    "no ranking",
    "no routing",
    "no executable planning",
    "no execution",
    "no record creation",
    "no storage",
    "no persistence",
    "no mutation",
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
p4_m4_final_closure_operator_handoff_index_only
operator_handoff_index_only
operator_handoff_non_validation_boundary_only
operator_handoff_non_scoring_boundary_only
operator_handoff_non_verdict_boundary_only
operator_handoff_non_execution_boundary_only
operator_handoff_non_record_boundary_only
operator_handoff_non_mutation_boundary_only
p4_m5_non_start_boundary_only
declaration_only
inspection_only
p4_m4_fc_2_started
p4_m4_fc_2_definition_only
p4_m4_fc_2_final_closure_operator_handoff_index_only
p4_m4_fc_2_operator_handoff_index_only
p4_m4_fc_2_p4_m5_non_start_boundary_only
p4_m4_fc_1_final_closure_evidence_index_reference_defined
p4_m4_fc_1_static_reference_defined
p4_m4_fc_0_final_closure_index_entry_planning_gate_reference_defined
p4_m4_17_terminal_closure_seal_reference_defined
p4_m4_16_final_phase_handoff_summary_reference_defined
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
p4_m4_static_definition_chain_closed_reference_defined
p4_m4_design_layer_terminally_sealed_reference_defined
p4_m4_final_closure_operator_handoff_index_surface_defined
p4_m4_static_operator_handoff_references_defined
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
p4_m4_18_started
p4_m5_started
p4_m5_implementation_started
p4_m5_entry_validation_enabled
p4_m5_readiness_validation_enabled
p4_m5_entry_scoring_enabled
p4_m5_entry_verdict_enabled
p4_m5_entry_execution_enabled
p4_m5_start_enabled
operator_handoff_validation_enabled
operator_handoff_scoring_enabled
operator_handoff_verdict_enabled
operator_handoff_execution_enabled
operator_handoff_record_creation_enabled
operator_handoff_storage_enabled
operator_handoff_persistence_enabled
operator_handoff_mutation_enabled
final_closure_operator_handoff_index_validation_enabled
final_closure_operator_handoff_index_scoring_enabled
final_closure_operator_handoff_index_verdict_enabled
final_closure_operator_handoff_index_execution_enabled
evidence_validation_enabled
evidence_scoring_enabled
evidence_verdict_enabled
evidence_execution_enabled
final_closure_evidence_index_validation_enabled
final_closure_evidence_index_scoring_enabled
final_closure_evidence_index_verdict_enabled
final_closure_evidence_index_execution_enabled
final_closure_index_validation_enabled
final_closure_index_scoring_enabled
final_closure_index_verdict_enabled
final_closure_index_execution_enabled
entry_planning_gate_validation_enabled
entry_planning_gate_scoring_enabled
entry_planning_gate_verdict_enabled
entry_planning_gate_execution_enabled
p4_m4_closure_validation_enabled
p4_m4_closure_scoring_enabled
p4_m4_closure_verdict_enabled
p4_m4_closure_execution_enabled
terminal_closure_validation_enabled
terminal_closure_scoring_enabled
terminal_closure_verdict_enabled
terminal_closure_execution_enabled
final_phase_handoff_validation_enabled
final_phase_handoff_scoring_enabled
final_phase_handoff_verdict_enabled
final_phase_handoff_execution_enabled
phase_closure_validation_enabled
phase_closure_scoring_enabled
phase_closure_verdict_enabled
phase_closure_execution_enabled
closure_handoff_validation_enabled
closure_handoff_execution_enabled
final_audit_execution_enabled
live_audit_evaluation_enabled
entry_gate_validation_enabled
readiness_validation_enabled
transition_validation_enabled
package_validation_enabled
package_assembly_validation_enabled
gate_activation_enabled
verdict_generation_enabled
approval_enabled
authorization_enabled
confirmation_enabled
recommendation_enabled
ranking_enabled
routing_enabled
planning_enabled
executable_planning_enabled
next_action_generation_enabled
execution_enabled
command_execution_enabled
record_creation_enabled
storage_enabled
persistence_enabled
memory_mutation_enabled
api_enabled
mcp_enabled
connector_enabled
agent_call_enabled
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
}


def test_field_inventory_is_exact_and_ordered():
    fields = list_p4_m4_final_closure_operator_handoff_index_fields()

    assert len(fields) == 23
    assert p4_m4_final_closure_operator_handoff_index_field_ids() == FIELD_IDS
    assert tuple(field.field_order for field in fields) == tuple(range(1, 24))
    assert all(
        isinstance(field, P4M4FinalClosureOperatorHandoffIndexField)
        for field in fields
    )
    assert {
        field.name
        for field in dataclasses.fields(
            P4M4FinalClosureOperatorHandoffIndexField
        )
    } == DATACLASS_FIELDS


def test_boundary_phrase_inventory_is_required_contract():
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in BOUNDARY_PHRASE_LINES
        assert phrase in P4_M4_FINAL_CLOSURE_OPERATOR_HANDOFF_INDEX_BOUNDARY


def test_markdown_renders_static_boundary_and_field_ids():
    markdown = render_p4_m4_final_closure_operator_handoff_index_markdown()

    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in markdown
    for field_id in FIELD_IDS:
        assert field_id in markdown
    assert "## Status Report" in markdown
    assert "## P4-M4 Final Closure Operator Handoff Index Fields" in markdown
    assert "P4-M4-FC.2 P4-M4 Final Closure Operator Handoff Index" in markdown


def test_report_has_required_true_false_status_flags():
    status = p4_m4_final_closure_operator_handoff_index_report()

    assert status["phase"] == "P4-M4-FC.2"
    assert status["feature"] == "P4-M4 Final Closure Operator Handoff Index"
    assert status["mode"] == "read-only"
    assert status["package_version"] == "6.16.0"
    assert status["p4_m4_final_closure_operator_handoff_index_field_count"] == 23
    assert (
        status["referenced_p4_m4_fc_1_final_closure_evidence_index_field_count"]
        == 23
    )
    assert TRUE_STATUS_FLAGS == EXPECTED_TRUE_STATUS_FLAGS
    assert FALSE_STATUS_FLAGS == EXPECTED_FALSE_STATUS_FLAGS
    for flag in EXPECTED_TRUE_STATUS_FLAGS:
        assert status[flag] is True
    for flag in EXPECTED_FALSE_STATUS_FLAGS:
        assert status[flag] is False


def test_as_dicts_is_deterministic_and_read_only_shape():
    fields = p4_m4_final_closure_operator_handoff_index_as_dicts()

    assert len(fields) == 23
    assert tuple(field["field_id"] for field in fields) == FIELD_IDS
    assert fields == p4_m4_final_closure_operator_handoff_index_as_dicts()
    assert all(
        field["p4_m4_final_closure_operator_handoff_index_category"]
        == "p4-m4-final-closure-operator-handoff-index-category"
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
            "p4-m4-final-closure-operator-handoff-index",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith(
        "# P4-M4-FC.2 P4-M4 Final Closure Operator Handoff Index\n"
    )
    for phrase in OPERATOR_SMOKE_PHRASES:
        assert phrase in stdout
    assert not (tmp_path / ".local" / "subspace_memory").exists()


def test_operator_json_command_returns_required_report(tmp_path: Path):
    code, output, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "p4-m4-final-closure-operator-handoff-index",
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
    assert output["boundary"] == P4_M4_FINAL_CLOSURE_OPERATOR_HANDOFF_INDEX_BOUNDARY
    assert tuple(field["field_id"] for field in output["fields"]) == FIELD_IDS
    status = output["status"]
    assert status["phase"] == "P4-M4-FC.2"
    assert status["feature"] == "P4-M4 Final Closure Operator Handoff Index"
    assert status["mode"] == "read-only"
    for flag in EXPECTED_TRUE_STATUS_FLAGS:
        assert status[flag] is True
    for flag in EXPECTED_FALSE_STATUS_FLAGS:
        assert status[flag] is False
    assert not (tmp_path / ".local" / "subspace_memory").exists()


def test_parser_exposes_only_expected_memory_loop_command_surface():
    commands = _memory_loop_subcommands(build_parser())

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
    assert "p4-m4-final-closure-operator-handoff-index" in commands


def test_pyproject_entry_points_do_not_productize_command():
    pyproject = tomllib.loads(Path("pyproject.toml").read_text())
    entry_points = pyproject["project"]["entry-points"]

    assert "p4-m4-final-closure-operator-handoff-index" not in entry_points
    assert "p4-m4-final-closure-operator-handoff-index" not in str(entry_points)
    assert pyproject["project"]["version"] == "6.16.0"


def test_static_doc_contains_required_boundaries_and_fields():
    project_root = Path(__file__).resolve().parents[1]
    doc_path = (
        project_root
        / "docs"
        / "CIVILIZATION_CORE_P4_M4_FC_2_FINAL_CLOSURE_OPERATOR_HANDOFF_INDEX.md"
    )
    doc = doc_path.read_text(encoding="utf-8")

    assert doc.startswith(
        "# P4-M4-FC.2 P4-M4 Final Closure Operator Handoff Index\n"
    )
    for field_id in FIELD_IDS:
        assert field_id in doc
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in doc


def test_custom_field_rendering_remains_definition_only():
    field = P4M4FinalClosureOperatorHandoffIndexField(
        field_order=99,
        field_id="custom-final-closure-operator-handoff-index",
        field_name="Custom Final Closure Operator Handoff Index",
        field_purpose="custom read-only definition-only inspection-only field",
        p4_m4_final_closure_operator_handoff_index_category=(
            "custom-final-closure-operator-handoff-index-category"
        ),
        p4_m4_final_closure_operator_handoff_index_semantics_disabled=(
            "no operator handoff validation semantics; no execution semantics; no mutation semantics"
        ),
    )

    markdown = render_p4_m4_final_closure_operator_handoff_index_markdown((field,))

    assert "custom-final-closure-operator-handoff-index" in markdown
    assert "no operator handoff validation semantics; no execution semantics" in markdown
    assert "P4-M4-FC.2 P4-M4 Final Closure Operator Handoff Index" in markdown


def test_forbidden_stage_filenames_are_not_created():
    project_root = Path(__file__).resolve().parents[1]
    changed_names = (
        "src/hermes_memory_fabric/p4_m4_final_closure_operator_handoff_index.py",
        "tests/test_p4_m4_final_closure_operator_handoff_index.py",
        "docs/CIVILIZATION_CORE_P4_M4_FC_2_FINAL_CLOSURE_OPERATOR_HANDOFF_INDEX.md",
    )

    assert all("p4_m5" not in name and "P4_M5" not in name for name in changed_names)
    assert all(
        "p4_m4_18" not in name and "P4_M4_18" not in name for name in changed_names
    )
    assert not (project_root / "src" / "hermes_memory_fabric" / "p4_m5.py").exists()
    assert not (project_root / "src" / "hermes_memory_fabric" / "p4_m4_18.py").exists()


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
