from __future__ import annotations

import argparse
import io
import json
import tomllib
from pathlib import Path

from hermes_memory_fabric.p4_m0_subspace_operator import build_parser, run_operator_command
from hermes_memory_fabric.p4_m4_declared_transition_impact_envelope_contract import (
    BOUNDARY_PHRASE_LINES,
    DECLARED_TRANSITION_IMPACT_ENVELOPE_CONTRACT_BOUNDARY,
    FALSE_STATUS_FLAGS,
    TRUE_STATUS_FLAGS,
    DeclaredTransitionImpactEnvelopeContractField,
    declared_transition_impact_envelope_contract_as_dicts,
    declared_transition_impact_envelope_contract_field_ids,
    declared_transition_impact_envelope_contract_report,
    list_declared_transition_impact_envelope_contract_fields,
    render_declared_transition_impact_envelope_contract_markdown,
)


FIELD_IDS = (
    "p4-m4-declared-transition-impact-envelope-contract-id",
    "p4-m4-declared-transition-impact-envelope-contract-phase",
    "p4-m4-declared-transition-impact-envelope-contract-mode",
    "p4-m4-declared-transition-impact-envelope-contract-direct-prior-declared-transition-dependency-envelope-reference",
    "p4-m4-declared-transition-impact-envelope-contract-inherited-prior-declared-transition-constraint-envelope-reference",
    "p4-m4-declared-transition-impact-envelope-contract-inherited-prior-declared-transition-reason-envelope-reference",
    "p4-m4-declared-transition-impact-envelope-contract-inherited-prior-target-phase-envelope-reference",
    "p4-m4-declared-transition-impact-envelope-contract-inherited-prior-declared-human-context-envelope-reference",
    "p4-m4-declared-transition-impact-envelope-contract-inherited-prior-evidence-reference-envelope-reference",
    "p4-m4-declared-transition-impact-envelope-contract-inherited-prior-request-envelope-reference",
    "p4-m4-declared-transition-impact-envelope-contract-inherited-prior-boundary-reference",
    "p4-m4-declared-transition-impact-envelope-contract-inherited-prior-handoff-reference",
    "p4-m4-declared-transition-impact-envelope-contract-scope",
    "p4-m4-declared-transition-impact-envelope-contract-declared-transition-impact-envelope-design-only",
    "p4-m4-declared-transition-impact-envelope-contract-declared-impact-surface-definition",
    "p4-m4-declared-transition-impact-envelope-contract-impact-non-analysis-boundary-definition",
    "p4-m4-declared-transition-impact-envelope-contract-impact-non-validation-boundary-definition",
    "p4-m4-declared-transition-impact-envelope-contract-impact-non-scoring-boundary-definition",
    "p4-m4-declared-transition-impact-envelope-contract-impact-non-graph-boundary-definition",
    "p4-m4-declared-transition-impact-envelope-contract-declaration-only-semantics-definition",
    "p4-m4-declared-transition-impact-envelope-contract-declared-transition-dependency-static-reference-definition",
    "p4-m4-declared-transition-impact-envelope-contract-impact-analysis-validation-scoring-graph-semantics-disabled",
    "p4-m4-declared-transition-impact-envelope-contract-p4-m5-v7-productization-ui-deferred",
)

DATACLASS_FIELDS = {
    "field_order",
    "field_id",
    "field_name",
    "field_purpose",
    "p4_m4_declared_transition_impact_envelope_contract_category",
    "p4_m4_declared_transition_impact_envelope_contract_semantics_disabled",
}

REQUIRED_BOUNDARY_PHRASES = BOUNDARY_PHRASE_LINES

OPERATOR_SMOKE_PHRASES = (
    "P4-M4.8 Declared Transition Impact Envelope Contract",
    "read-only",
    "definition-only",
    "declared-transition-impact-envelope-design-only",
    "declared-impact-surface-only",
    "impact-non-analysis-boundary-only",
    "impact-non-validation-boundary-only",
    "impact-non-scoring-boundary-only",
    "impact-non-graph-boundary-only",
    "declaration-only",
    "inspection-only",
    "P4-M4.7 Declared Transition Dependency Envelope Contract remains the direct prior declared transition dependency envelope reference",
    "P4-M4.7 declared transition dependency remains only an inherited static declared dependency surface reference",
    "P4-M4 transition impact analysis remains not implemented",
    "P4-M4 transition impact validation remains not implemented",
    "P4-M4 transition impact scoring remains not implemented",
    "P4-M4 impact graph construction remains not implemented",
    "P4-M4 transition impact acceptance remains not implemented",
    "P4-M4 transition impact rejection remains not implemented",
    "P4-M4 transition impact routing remains not implemented",
    "P4-M4 transition impact planning remains not implemented",
    "P4-M4 transition impact execution remains not implemented",
    "P4-M4 transition dependency to transition impact mapping remains not implemented",
    "P4-M4 transition constraint to transition impact mapping remains not implemented",
    "P4-M4 transition reason to transition impact mapping remains not implemented",
    "P4-M4 target phase to transition impact mapping remains not implemented",
    "P4-M4 human context to transition impact mapping remains not implemented",
    "no transition impact analysis",
    "no transition impact validation",
    "no transition impact scoring",
    "no impact graph construction",
    "no transition impact acceptance",
    "no transition impact rejection",
    "no transition impact routing",
    "no transition impact planning",
    "no transition impact execution",
    "no transition dependency to transition impact mapping",
    "no transition constraint to transition impact mapping",
    "no transition reason to transition impact mapping",
    "no target phase to transition impact mapping",
    "no human context to transition impact mapping",
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
declared_transition_impact_envelope_design_only
declared_impact_surface_only
impact_non_analysis_boundary_only
impact_non_validation_boundary_only
impact_non_scoring_boundary_only
impact_non_graph_boundary_only
declaration_only
inspection_only
p4_m4_8_declared_transition_impact_envelope_contract_started
p4_m4_8_definition_only
p4_m4_8_declared_transition_impact_envelope_design_only
p4_m4_8_declared_impact_surface_only
p4_m4_8_impact_non_analysis_boundary_only
p4_m4_8_impact_non_validation_boundary_only
p4_m4_8_impact_non_scoring_boundary_only
p4_m4_8_impact_non_graph_boundary_only
p4_m4_8_declaration_only
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
p4_m4_declared_transition_impact_envelope_design_defined
p4_m4_declared_impact_surface_defined
p4_m4_transition_impact_non_analysis_boundary_defined
p4_m4_transition_impact_non_validation_boundary_defined
p4_m4_transition_impact_non_scoring_boundary_defined
p4_m4_transition_impact_non_graph_boundary_defined
p4_m4_transition_impact_non_acceptance_boundary_defined
p4_m4_transition_impact_non_rejection_boundary_defined
p4_m4_transition_impact_non_ranking_boundary_defined
p4_m4_transition_impact_non_routing_boundary_defined
p4_m4_transition_impact_non_planning_boundary_defined
p4_m4_transition_impact_non_execution_boundary_defined
p4_m4_transition_impact_analysis_semantics_prohibited
p4_m4_transition_impact_validation_semantics_prohibited
p4_m4_transition_impact_scoring_semantics_prohibited
p4_m4_impact_graph_semantics_prohibited
p4_m4_impact_propagation_semantics_prohibited
p4_m4_impact_simulation_semantics_prohibited
p4_m4_impact_severity_semantics_prohibited
p4_m4_impact_justification_semantics_prohibited
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
transition_impact_intake_enabled
live_transition_impact_parsing_enabled
transition_impact_analysis_enabled
transition_impact_validation_enabled
transition_impact_scoring_enabled
impact_graph_construction_enabled
impact_propagation_enabled
impact_simulation_enabled
impact_severity_evaluation_enabled
impact_sufficiency_validation_enabled
impact_consistency_validation_enabled
impact_integrity_validation_enabled
transition_impact_acceptance_enabled
transition_impact_rejection_enabled
transition_impact_ranking_enabled
transition_impact_recommendation_enabled
transition_impact_generation_enabled
transition_impact_justification_enabled
transition_impact_routing_enabled
transition_impact_planning_enabled
transition_impact_execution_enabled
transition_impact_record_creation_enabled
impact_analysis_record_creation_enabled
impact_validation_record_creation_enabled
impact_scoring_record_creation_enabled
impact_graph_record_creation_enabled
impact_propagation_record_creation_enabled
impact_simulation_record_creation_enabled
impact_severity_record_creation_enabled
impact_routing_record_creation_enabled
impact_planning_record_creation_enabled
impact_justification_record_creation_enabled
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
semantic_target_field_graph_enabled
transition_dependency_to_transition_impact_mapping_enabled
transition_constraint_to_transition_impact_mapping_enabled
transition_reason_to_transition_impact_mapping_enabled
target_phase_to_transition_impact_mapping_enabled
human_context_to_transition_impact_mapping_enabled
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
transition_impact_verdict_enabled
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
}

PROHIBITED_MEMORY_LOOP_COMMANDS = {
    "transition-impact-intake",
    "parse-transition-impact",
    "analyze-transition-impact",
    "validate-transition-impact",
    "score-transition-impact",
    "build-impact-graph",
    "propagate-impact",
    "simulate-impact",
    "evaluate-impact-severity",
    "accept-transition-impact",
    "reject-transition-impact",
    "rank-transition-impact",
    "recommend-transition-impact",
    "generate-transition-impact",
    "justify-transition-impact",
    "route-transition-impact",
    "plan-transition-impact",
    "execute-transition-impact",
    "create-transition-impact-record",
    "map-transition-dependency-to-transition-impact",
    "map-transition-constraint-to-transition-impact",
    "map-transition-reason-to-transition-impact",
    "map-target-phase-to-transition-impact",
    "map-human-context-to-transition-impact",
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
    "transition-impact-verdict",
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


def test_declared_transition_impact_envelope_contract_field_order_count_and_ids_are_stable():
    fields = list_declared_transition_impact_envelope_contract_fields()

    assert [field.field_order for field in fields] == list(range(1, 24))
    assert len(fields) == 23
    assert declared_transition_impact_envelope_contract_field_ids() == FIELD_IDS


def test_every_declared_transition_impact_envelope_contract_field_has_required_values():
    for field in list_declared_transition_impact_envelope_contract_fields():
        assert field.field_name.strip()
        assert field.field_purpose.strip()
        assert field.p4_m4_declared_transition_impact_envelope_contract_category.strip()
        assert (
            field.p4_m4_declared_transition_impact_envelope_contract_semantics_disabled.strip()
        )


def test_required_boundary_phrase_contract_contains_all_required_phrases():
    assert len(REQUIRED_BOUNDARY_PHRASES) >= 230
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in BOUNDARY_PHRASE_LINES
    for phrase in OPERATOR_SMOKE_PHRASES:
        assert (
            phrase in BOUNDARY_PHRASE_LINES
            or phrase in DECLARED_TRANSITION_IMPACT_ENVELOPE_CONTRACT_BOUNDARY
        )


def test_required_status_flag_contract_is_literal_and_complete():
    assert TRUE_STATUS_FLAGS == EXPECTED_TRUE_STATUS_FLAGS
    assert FALSE_STATUS_FLAGS == EXPECTED_FALSE_STATUS_FLAGS


def test_markdown_output_is_stable_and_contains_required_boundaries():
    first = render_declared_transition_impact_envelope_contract_markdown()
    second = render_declared_transition_impact_envelope_contract_markdown()

    assert first == second
    assert first.startswith("# P4-M4.8 Declared Transition Impact Envelope Contract\n")
    assert DECLARED_TRANSITION_IMPACT_ENVELOPE_CONTRACT_BOUNDARY in first
    for field_id in FIELD_IDS:
        assert field_id in first
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in first


def test_json_output_is_stable_and_contains_required_boundaries(tmp_path):
    args = [
        "memory-loop",
        "declared-transition-impact-envelope-contract",
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
        == DECLARED_TRANSITION_IMPACT_ENVELOPE_CONTRACT_BOUNDARY
    )
    assert first_payload["count"] == 23
    assert first_payload["status"]["phase"] == "P4-M4.8"
    assert first_payload["status"]["feature"] == "Declared Transition Impact Envelope Contract"
    assert first_payload["status"]["mode"] == "read-only"
    assert first_payload["status"] == declared_transition_impact_envelope_contract_report()
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
    first_fields = declared_transition_impact_envelope_contract_as_dicts()
    second_fields = declared_transition_impact_envelope_contract_as_dicts()
    first_status = declared_transition_impact_envelope_contract_report()
    second_status = declared_transition_impact_envelope_contract_report()

    assert first_fields == second_fields
    assert [field["field_id"] for field in first_fields] == list(FIELD_IDS)
    assert first_status == second_status
    assert first_status["phase"] == "P4-M4.8"
    assert first_status["feature"] == "Declared Transition Impact Envelope Contract"
    assert first_status["mode"] == "read-only"
    assert first_status["declared_transition_impact_envelope_contract_field_count"] == 23
    assert (
        first_status[
            "referenced_p4_m4_7_declared_transition_dependency_envelope_contract_field_count"
        ]
        == 22
    )
    assert first_status["boundary"] == DECLARED_TRANSITION_IMPACT_ENVELOPE_CONTRACT_BOUNDARY


def test_status_report_locks_true_and_disabled_flags():
    status = declared_transition_impact_envelope_contract_report()

    for flag in EXPECTED_TRUE_STATUS_FLAGS:
        assert status[flag] is True
    for flag in EXPECTED_FALSE_STATUS_FLAGS:
        assert status[flag] is False


def test_operator_markdown_default_is_read_only_and_creates_no_local_storage(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "declared-transition-impact-envelope-contract",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M4.8 Declared Transition Impact Envelope Contract\n")
    assert "## Status Report" in stdout
    assert DECLARED_TRANSITION_IMPACT_ENVELOPE_CONTRACT_BOUNDARY in stdout
    for phrase in OPERATOR_SMOKE_PHRASES:
        assert phrase in stdout
    assert not (tmp_path / ".local").exists()


def test_operator_markdown_format_is_explicit_and_stable(tmp_path):
    args = [
        "memory-loop",
        "declared-transition-impact-envelope-contract",
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
    assert first_stdout.startswith("# P4-M4.8")
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
            "declared-transition-impact-envelope-contract",
            "--workspace-root",
            str(tmp_path),
        ]
    )
    json_code, json_payload, json_stderr, _ = _run_operator(
        [
            "memory-loop",
            "declared-transition-impact-envelope-contract",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert markdown_code == 0
    assert markdown_stderr == ""
    assert markdown_stdout.startswith("# P4-M4.8")
    assert json_code == 0
    assert json_stderr == ""
    assert json_payload["count"] == 23
    assert not (tmp_path / ".local").exists()


def test_command_creates_no_storage_files_or_state_changes(tmp_path):
    _run_operator(
        [
            "memory-loop",
            "declared-transition-impact-envelope-contract",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    storage_root = tmp_path / ".local" / "subspace_memory"
    for filename in (
        "declared_transition_impact_envelope_contract.jsonl",
        "transition_impact_intake.jsonl",
        "transition_impact_parsing.jsonl",
        "transition_impact_analysis.jsonl",
        "transition_impact_validation.jsonl",
        "transition_impact_scoring.jsonl",
        "impact_graph_construction.jsonl",
        "impact_propagation.jsonl",
        "impact_simulation.jsonl",
        "impact_severity_evaluation.jsonl",
        "transition_impact_acceptance.jsonl",
        "transition_impact_rejection.jsonl",
        "transition_impact_routing.jsonl",
        "transition_impact_planning.jsonl",
        "transition_impact_execution.jsonl",
        "transition_impact_record_creation.jsonl",
        "impact_analysis_record_creation.jsonl",
        "impact_validation_record_creation.jsonl",
        "impact_scoring_record_creation.jsonl",
        "impact_graph_record_creation.jsonl",
        "impact_routing_record_creation.jsonl",
        "impact_planning_record_creation.jsonl",
        "impact_justification_record_creation.jsonl",
        "transition_dependency_to_transition_impact_mapping.jsonl",
        "transition_constraint_to_transition_impact_mapping.jsonl",
        "transition_reason_to_transition_impact_mapping.jsonl",
        "target_phase_to_transition_impact_mapping.jsonl",
        "human_context_to_transition_impact_mapping.jsonl",
    ):
        assert not (storage_root / filename).exists()
    assert not storage_root.exists()


def test_parser_exposes_only_expected_memory_loop_command_surface():
    commands = _memory_loop_subcommands(build_parser())

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
    assert "declared-transition-impact-envelope-contract" in commands
    assert not (commands & PROHIBITED_MEMORY_LOOP_COMMANDS)


def test_command_is_not_packaged_as_top_level_entry_point():
    entry_points = _project_entry_points()

    assert "declared-transition-impact-envelope-contract" not in entry_points
    assert "declared-transition-impact-envelope-contract" not in str(entry_points)


def test_custom_field_rendering_remains_definition_only():
    custom = DeclaredTransitionImpactEnvelopeContractField(
        field_order=24,
        field_id="custom-declared-transition-impact-envelope-contract",
        field_name="Custom Declared Transition Impact Envelope Contract Field",
        field_purpose="Custom read-only declared impact surface field.",
        p4_m4_declared_transition_impact_envelope_contract_category=(
            "custom-declared-transition-impact-envelope-contract-category"
        ),
        p4_m4_declared_transition_impact_envelope_contract_semantics_disabled=(
            "no transition impact analysis semantics"
        ),
    )

    markdown = render_declared_transition_impact_envelope_contract_markdown([custom])

    assert "custom-declared-transition-impact-envelope-contract" in markdown
    assert "Custom read-only declared impact surface field." in markdown
    assert DECLARED_TRANSITION_IMPACT_ENVELOPE_CONTRACT_BOUNDARY in markdown


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
