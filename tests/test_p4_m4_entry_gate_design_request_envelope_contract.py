from __future__ import annotations

import argparse
import io
import json
import tomllib
from pathlib import Path

from hermes_memory_fabric.p4_m0_subspace_operator import build_parser, run_operator_command
from hermes_memory_fabric.p4_m4_entry_gate_design_request_envelope_contract import (
    BOUNDARY_PHRASE_LINES,
    ENTRY_GATE_DESIGN_REQUEST_ENVELOPE_CONTRACT_BOUNDARY,
    FALSE_STATUS_FLAGS,
    TRUE_STATUS_FLAGS,
    EntryGateDesignRequestEnvelopeContractField,
    entry_gate_design_request_envelope_contract_as_dicts,
    entry_gate_design_request_envelope_contract_field_ids,
    entry_gate_design_request_envelope_contract_report,
    list_entry_gate_design_request_envelope_contract_fields,
    render_entry_gate_design_request_envelope_contract_markdown,
)


FIELD_IDS = (
    "p4-m4-entry-gate-design-request-envelope-contract-id",
    "p4-m4-entry-gate-design-request-envelope-contract-phase",
    "p4-m4-entry-gate-design-request-envelope-contract-mode",
    "p4-m4-entry-gate-design-request-envelope-contract-direct-prior-boundary-reference",
    "p4-m4-entry-gate-design-request-envelope-contract-inherited-prior-handoff-reference",
    "p4-m4-entry-gate-design-request-envelope-contract-scope",
    "p4-m4-entry-gate-design-request-envelope-contract-request-envelope-design-only",
    "p4-m4-entry-gate-design-request-envelope-contract-request-shape-definition",
    "p4-m4-entry-gate-design-request-envelope-contract-request-intake-non-implementation",
    "p4-m4-entry-gate-design-request-envelope-contract-request-validation-semantics-disabled",
    "p4-m4-entry-gate-design-request-envelope-contract-verdict-semantics-disabled",
    "p4-m4-entry-gate-design-request-envelope-contract-execution-semantics-disabled",
    "p4-m4-entry-gate-design-request-envelope-contract-mutation-semantics-disabled",
    "p4-m4-entry-gate-design-request-envelope-contract-p4-m5-v7-productization-ui-deferred",
)

DATACLASS_FIELDS = {
    "field_order",
    "field_id",
    "field_name",
    "field_purpose",
    "p4_m4_entry_gate_design_request_envelope_contract_category",
    "p4_m4_entry_gate_design_request_envelope_contract_semantics_disabled",
}

REQUIRED_BOUNDARY_PHRASES = (
    "P4-M4.1",
    "Entry Gate Design Request Envelope Contract",
    "read-only",
    "definition-only",
    "request-envelope-design-only",
    "inspection-only",
    "P4-M4.1 Entry Gate Design Request Envelope Contract is definition only",
    "P4-M4.1 is request-envelope-design-only",
    "P4-M4.0 Entry Gate Design Boundary Contract remains the direct prior design boundary reference",
    "P4-M3.16 Governed Transition Intake Final Phase Handoff Summary remains the inherited prior closed-phase handoff reference",
    "P4-M3 static definition chain remains closed",
    "P4-M4 design layer remains design-boundary-only",
    "P4-M4 request envelope design starts only as a static envelope definition",
    "P4-M4 live request intake remains not implemented",
    "P4-M4 request parsing remains not implemented",
    "P4-M4 request validation remains not implemented",
    "P4-M4 request acceptance remains not implemented",
    "P4-M4 request rejection remains not implemented",
    "P4-M4 request routing remains not implemented",
    "P4-M4 request execution remains not implemented",
    "P4-M4 request record creation remains not implemented",
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
    "P4-M4.1 is not live validation",
    "P4-M4.1 is not request intake",
    "P4-M4.1 is not live request parsing",
    "P4-M4.1 is not request validation",
    "P4-M4.1 is not request acceptance",
    "P4-M4.1 is not request rejection",
    "P4-M4.1 is not request routing",
    "P4-M4.1 is not request execution",
    "P4-M4.1 is not request record creation",
    "P4-M4.1 is not boundary validation",
    "P4-M4.1 is not phase validation",
    "P4-M4.1 is not entry gate validation",
    "P4-M4.1 is not readiness validation",
    "P4-M4.1 is not transition validation",
    "P4-M4.1 is not package validation",
    "P4-M4.1 is not closure validation",
    "P4-M4.1 is not handoff validation",
    "P4-M4.1 is not final phase handoff validation",
    "P4-M4.1 is not a working entry gate",
    "P4-M4.1 is not gate activation",
    "P4-M4.1 is not gate execution",
    "P4-M4.1 is not transition execution",
    "P4-M4.1 is not command execution",
    "P4-M4.1 is not readiness verdict",
    "P4-M4.1 is not validation verdict",
    "P4-M4.1 is not entry verdict",
    "P4-M4.1 is not gate verdict",
    "P4-M4.1 is not transition verdict",
    "P4-M4.1 is not approval",
    "P4-M4.1 is not authorization",
    "P4-M4.1 is not confirmation",
    "P4-M4.1 is not recommendation",
    "P4-M4.1 is not ranking",
    "P4-M4.1 is not next action generation",
    "P4-M4.1 is not evidence intake",
    "P4-M4.1 is not human context intake",
    "P4-M4.1 is not evidence validation",
    "P4-M4.1 is not human context validation",
    "P4-M4.1 is not source validation",
    "P4-M4.1 is not citation validation",
    "P4-M4.1 is not reference resolution",
    "P4-M4.1 is not reference validation",
    "P4-M4.1 is not package completeness validation",
    "P4-M4.1 is not package consistency validation",
    "P4-M4.1 is not package integrity validation",
    "P4-M4.1 is not package readiness validation",
    "P4-M4.1 is not record creation",
    "P4-M4.1 is not request envelope record creation",
    "P4-M4.1 is not entry record creation",
    "P4-M4.1 is not gate record creation",
    "P4-M4.1 is not readiness record creation",
    "P4-M4.1 is not validation record creation",
    "P4-M4.1 is not transition record creation",
    "P4-M4.1 is not approval record creation",
    "P4-M4.1 is not authorization record creation",
    "P4-M4.1 is not confirmation record creation",
    "P4-M4.1 is not recommendation record creation",
    "P4-M4.1 is not ranking record creation",
    "P4-M4.1 is not next action record creation",
    "P4-M4.1 is not memory mutation",
    "P4-M4.1 is not roadmap mutation",
    "P4-M4.1 is not lifecycle mutation",
    "P4-M4.1 is not proposal mutation",
    "P4-M4.1 is not source fetching",
    "P4-M4.1 is not provenance writing",
    "P4-M4.1 is not citation mutation",
    "no live validation",
    "no request intake",
    "no live request parsing",
    "no request validation",
    "no request acceptance",
    "no request rejection",
    "no request routing",
    "no request execution",
    "no request record creation",
    "no boundary validation",
    "no phase validation",
    "no entry gate validation",
    "no readiness validation",
    "no transition validation",
    "no package validation",
    "no closure validation",
    "no handoff validation",
    "no final phase handoff validation",
    "no working entry gate",
    "no gate activation",
    "no gate execution",
    "no transition execution",
    "no command execution",
    "no readiness verdict",
    "no validation verdict",
    "no entry verdict",
    "no gate verdict",
    "no transition verdict",
    "no approval",
    "no authorization",
    "no confirmation",
    "no recommendation",
    "no ranking",
    "no next action generation",
    "no evidence intake",
    "no human context intake",
    "no evidence validation",
    "no human context validation",
    "no source validation",
    "no citation validation",
    "no reference resolution",
    "no reference validation",
    "no package completeness validation",
    "no package consistency validation",
    "no package integrity validation",
    "no package readiness validation",
    "no record creation",
    "no entry record creation",
    "no gate record creation",
    "no readiness record creation",
    "no validation record creation",
    "no transition record creation",
    "no approval record creation",
    "no authorization record creation",
    "no confirmation record creation",
    "no recommendation record creation",
    "no ranking record creation",
    "no next action record creation",
    "no memory mutation",
    "no roadmap mutation",
    "no lifecycle mutation",
    "no proposal mutation",
    "no source fetching",
    "no provenance writing",
    "no citation mutation",
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

EXPECTED_TRUE_STATUS_FLAGS = (
    "definition_only",
    "request_envelope_design_only",
    "inspection_only",
    "p4_m4_1_entry_gate_design_request_envelope_contract_started",
    "p4_m4_1_definition_only",
    "p4_m4_1_request_envelope_design_only",
    "p4_m4_0_entry_gate_design_boundary_contract_reference_defined",
    "p4_m3_16_final_phase_handoff_summary_reference_defined",
    "p4_m3_static_definition_chain_closed_reference_defined",
    "p4_m4_design_boundary_reference_defined",
    "p4_m4_request_envelope_design_defined",
    "p4_m4_request_shape_defined",
    "p4_m4_request_intake_non_implementation_boundary_defined",
    "p4_m4_request_validation_semantics_prohibited",
    "p4_m4_validation_semantics_prohibited",
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

EXPECTED_FALSE_STATUS_FLAGS = (
    "live_validation_enabled",
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
    "reference_resolution_enabled",
    "reference_validation_enabled",
    "reference_integrity_validation_enabled",
    "working_entry_gate_enabled",
    "gate_activation_enabled",
    "gate_execution_enabled",
    "p4_m4_execution_enabled",
    "operational_behavior_enabled",
    "readiness_verdict_enabled",
    "validation_verdict_enabled",
    "entry_verdict_enabled",
    "gate_verdict_enabled",
    "transition_verdict_enabled",
    "approval_enabled",
    "authorization_enabled",
    "confirmation_enabled",
    "recommendation_enabled",
    "ranking_enabled",
    "next_action_generation_enabled",
    "transition_execution_enabled",
    "command_execution_enabled",
    "evidence_intake_enabled",
    "human_context_intake_enabled",
    "evidence_validation_enabled",
    "human_context_validation_enabled",
    "source_validation_enabled",
    "citation_validation_enabled",
    "record_creation_enabled",
    "request_envelope_record_creation_enabled",
    "entry_record_creation_enabled",
    "gate_record_creation_enabled",
    "readiness_record_creation_enabled",
    "validation_record_creation_enabled",
    "transition_record_creation_enabled",
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
    "evidence_mutation_enabled",
    "human_context_mutation_enabled",
    "source_fetching_enabled",
    "provenance_writing_enabled",
    "citation_mutation_enabled",
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
}

PREVIOUS_P4_M4_0_READ_ONLY_COMMANDS = EXPECTED_MEMORY_LOOP_COMMANDS - {
    "entry-gate-design-request-envelope-contract"
}

PROHIBITED_MEMORY_LOOP_COMMANDS = {
    "request-intake",
    "parse-request",
    "validate-request",
    "accept-request",
    "reject-request",
    "route-request",
    "execute-request",
    "create-request-record",
    "validate-entry-gate",
    "validate-entry-readiness",
    "validate-readiness",
    "validate-transition-readiness",
    "validate-transition",
    "validate-package",
    "validate-package-completeness",
    "validate-package-consistency",
    "validate-package-integrity",
    "validate-package-readiness",
    "resolve-references",
    "validate-references",
    "working-entry-gate",
    "activate-gate",
    "execute-gate",
    "execute-p4-m4",
    "readiness-verdict",
    "validation-verdict",
    "entry-verdict",
    "gate-verdict",
    "transition-verdict",
    "approve",
    "authorize",
    "confirm",
    "recommend",
    "rank",
    "next-action",
    "execute-transition",
    "create-request-envelope-record",
    "create-entry-record",
    "create-gate-record",
    "create-readiness-record",
    "create-validation-record",
    "create-transition-record",
    "create-approval-record",
    "create-authorization-record",
    "create-confirmation-record",
    "create-recommendation-record",
    "create-ranking-record",
    "create-next-action-record",
    "write-memory",
    "start-p4-m5",
    "start-v7",
    "productize",
    "operator-console",
    "ui",
    "deploy",
}


def test_entry_gate_design_request_envelope_contract_field_order_count_and_ids_are_stable():
    fields = list_entry_gate_design_request_envelope_contract_fields()

    assert [field.field_order for field in fields] == list(range(1, 15))
    assert len(fields) == 14
    assert entry_gate_design_request_envelope_contract_field_ids() == FIELD_IDS


def test_every_entry_gate_design_request_envelope_contract_field_has_required_values():
    for field in list_entry_gate_design_request_envelope_contract_fields():
        assert field.field_name.strip()
        assert field.field_purpose.strip()
        assert field.p4_m4_entry_gate_design_request_envelope_contract_category.strip()
        assert (
            field.p4_m4_entry_gate_design_request_envelope_contract_semantics_disabled.strip()
        )


def test_required_boundary_phrase_contract_contains_all_required_phrases():
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in BOUNDARY_PHRASE_LINES


def test_required_status_flag_contract_is_literal_and_complete():
    assert TRUE_STATUS_FLAGS == EXPECTED_TRUE_STATUS_FLAGS
    assert FALSE_STATUS_FLAGS == EXPECTED_FALSE_STATUS_FLAGS


def test_markdown_output_is_stable_and_contains_required_boundaries():
    first = render_entry_gate_design_request_envelope_contract_markdown()
    second = render_entry_gate_design_request_envelope_contract_markdown()

    assert first == second
    assert first.startswith("# P4-M4.1 Entry Gate Design Request Envelope Contract\n")
    assert ENTRY_GATE_DESIGN_REQUEST_ENVELOPE_CONTRACT_BOUNDARY in first
    for field_id in FIELD_IDS:
        assert field_id in first
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in first


def test_json_output_is_stable_and_contains_required_boundaries(tmp_path):
    args = [
        "memory-loop",
        "entry-gate-design-request-envelope-contract",
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
    assert first_payload["boundary"] == ENTRY_GATE_DESIGN_REQUEST_ENVELOPE_CONTRACT_BOUNDARY
    assert first_payload["count"] == 14
    assert first_payload["status"]["phase"] == "P4-M4.1"
    assert (
        first_payload["status"]["feature"]
        == "Entry Gate Design Request Envelope Contract"
    )
    assert first_payload["status"]["mode"] == "read-only"
    assert first_payload["status"] == entry_gate_design_request_envelope_contract_report()
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
    first_fields = entry_gate_design_request_envelope_contract_as_dicts()
    second_fields = entry_gate_design_request_envelope_contract_as_dicts()
    first_status = entry_gate_design_request_envelope_contract_report()
    second_status = entry_gate_design_request_envelope_contract_report()

    assert first_fields == second_fields
    assert [field["field_id"] for field in first_fields] == list(FIELD_IDS)
    assert first_status == second_status
    assert first_status["phase"] == "P4-M4.1"
    assert first_status["feature"] == "Entry Gate Design Request Envelope Contract"
    assert first_status["mode"] == "read-only"
    assert first_status["entry_gate_design_request_envelope_contract_field_count"] == 14
    assert (
        first_status["referenced_p4_m4_0_entry_gate_design_boundary_contract_field_count"]
        == 12
    )
    assert first_status["boundary"] == ENTRY_GATE_DESIGN_REQUEST_ENVELOPE_CONTRACT_BOUNDARY


def test_status_report_locks_true_and_disabled_flags():
    status = entry_gate_design_request_envelope_contract_report()

    for flag in EXPECTED_TRUE_STATUS_FLAGS:
        assert status[flag] is True
    for flag in EXPECTED_FALSE_STATUS_FLAGS:
        assert status[flag] is False


def test_operator_markdown_default_is_read_only_and_creates_no_local_storage(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "entry-gate-design-request-envelope-contract",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M4.1 Entry Gate Design Request Envelope Contract\n")
    assert "## Status Report" in stdout
    assert ENTRY_GATE_DESIGN_REQUEST_ENVELOPE_CONTRACT_BOUNDARY in stdout
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in stdout
    assert not (tmp_path / ".local").exists()


def test_operator_markdown_format_is_explicit_and_stable(tmp_path):
    args = [
        "memory-loop",
        "entry-gate-design-request-envelope-contract",
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
    assert first_stdout.startswith("# P4-M4.1")
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
            "entry-gate-design-request-envelope-contract",
            "--workspace-root",
            str(tmp_path),
        ]
    )
    json_code, json_payload, json_stderr, _ = _run_operator(
        [
            "memory-loop",
            "entry-gate-design-request-envelope-contract",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert markdown_code == 0
    assert markdown_stderr == ""
    assert markdown_stdout.startswith("# P4-M4.1")
    assert json_code == 0
    assert json_stderr == ""
    assert json_payload["count"] == 14
    assert not (tmp_path / ".local").exists()


def test_command_creates_no_storage_files_or_state_changes(tmp_path):
    _run_operator(
        [
            "memory-loop",
            "entry-gate-design-request-envelope-contract",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    storage_root = tmp_path / ".local" / "subspace_memory"
    for filename in (
        "entry_gate_design_request_envelope_contract.jsonl",
        "request_envelope_records.jsonl",
        "request_envelope_validation.jsonl",
        "request_intake.jsonl",
        "request_parsing.jsonl",
        "request_validation.jsonl",
        "request_acceptance.jsonl",
        "request_rejection.jsonl",
        "request_routing.jsonl",
        "request_execution.jsonl",
        "request_records.jsonl",
        "entry_gate_design_boundary_contract.jsonl",
        "entry_gate_records.jsonl",
        "gate_records.jsonl",
        "readiness_records.jsonl",
        "validation_records.jsonl",
        "transition_records.jsonl",
        "approval_records.jsonl",
        "authorization_records.jsonl",
        "confirmation_records.jsonl",
        "recommendation_records.jsonl",
        "ranking_records.jsonl",
        "next_action_records.jsonl",
        "entry_gate_validation.jsonl",
        "readiness_validation.jsonl",
        "transition_readiness_validation.jsonl",
        "package_validation.jsonl",
        "reference_resolution.jsonl",
        "reference_validation.jsonl",
        "evidence_intake.jsonl",
        "human_context_intake.jsonl",
        "execution.jsonl",
        "authorization.jsonl",
        "confirmation.jsonl",
        "approvals.jsonl",
        "recommendations.jsonl",
        "rankings.jsonl",
        "next_actions.jsonl",
        "validation.jsonl",
        "readiness.jsonl",
        "memories.jsonl",
        "proposals.jsonl",
        "lifecycle.jsonl",
        "sources.jsonl",
        "provenance.jsonl",
        "evidence.jsonl",
        "citations.jsonl",
        "roadmap.jsonl",
        "audit.jsonl",
    ):
        assert not (storage_root / filename).exists()
    assert not (tmp_path / ".local").exists()


def test_read_only_allowlist_includes_new_command_and_preserves_previous_commands():
    commands = _memory_loop_commands()

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
    assert "entry-gate-design-request-envelope-contract" in commands
    assert PREVIOUS_P4_M4_0_READ_ONLY_COMMANDS.issubset(commands)
    assert commands.isdisjoint(PROHIBITED_MEMORY_LOOP_COMMANDS)


def test_doc_contains_required_boundaries():
    doc = Path(
        "docs/CIVILIZATION_CORE_P4_M4_1_ENTRY_GATE_DESIGN_REQUEST_ENVELOPE_CONTRACT.md"
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
    assert "p4_m4_entry_gate_design_request_envelope_contract" not in entry_points
    assert "entry-gate-design-request-envelope-contract" not in entry_points


def test_no_uv_lock_is_created():
    assert not Path("uv.lock").exists()


def test_custom_markdown_render_accepts_read_only_fields():
    field = EntryGateDesignRequestEnvelopeContractField(
        field_order=1,
        field_id="custom-entry-gate-design-request-envelope-contract",
        field_name="Custom Entry Gate Design Request Envelope Contract Field",
        field_purpose="Custom inspection-only purpose.",
        p4_m4_entry_gate_design_request_envelope_contract_category=(
            "custom-entry-gate-design-request-envelope-contract-category"
        ),
        p4_m4_entry_gate_design_request_envelope_contract_semantics_disabled=(
            "Custom entry gate design request envelope contract semantics are disabled."
        ),
    )

    markdown = render_entry_gate_design_request_envelope_contract_markdown([field])

    assert "custom-entry-gate-design-request-envelope-contract" in markdown
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
