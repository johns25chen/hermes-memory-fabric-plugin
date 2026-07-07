from __future__ import annotations

import argparse
import io
import json
import tomllib
from pathlib import Path

from hermes_memory_fabric.p4_m0_subspace_operator import build_parser, run_operator_command
from hermes_memory_fabric.p4_m4_declared_transition_assumption_envelope_contract import (
    BOUNDARY_PHRASE_LINES,
    DECLARED_TRANSITION_ASSUMPTION_ENVELOPE_CONTRACT_BOUNDARY,
    FALSE_STATUS_FLAGS,
    TRUE_STATUS_FLAGS,
    DeclaredTransitionAssumptionEnvelopeContractField,
    declared_transition_assumption_envelope_contract_as_dicts,
    declared_transition_assumption_envelope_contract_field_ids,
    declared_transition_assumption_envelope_contract_report,
    list_declared_transition_assumption_envelope_contract_fields,
    render_declared_transition_assumption_envelope_contract_markdown,
)


FIELD_IDS = (
    "p4-m4-declared-transition-assumption-envelope-contract-id",
    "p4-m4-declared-transition-assumption-envelope-contract-phase",
    "p4-m4-declared-transition-assumption-envelope-contract-mode",
    "p4-m4-declared-transition-assumption-envelope-contract-direct-prior-declared-transition-risk-envelope-reference",
    "p4-m4-declared-transition-assumption-envelope-contract-inherited-prior-declared-transition-impact-envelope-reference",
    "p4-m4-declared-transition-assumption-envelope-contract-inherited-prior-declared-transition-dependency-envelope-reference",
    "p4-m4-declared-transition-assumption-envelope-contract-inherited-prior-declared-transition-constraint-envelope-reference",
    "p4-m4-declared-transition-assumption-envelope-contract-inherited-prior-declared-transition-reason-envelope-reference",
    "p4-m4-declared-transition-assumption-envelope-contract-inherited-prior-target-phase-envelope-reference",
    "p4-m4-declared-transition-assumption-envelope-contract-inherited-prior-declared-human-context-envelope-reference",
    "p4-m4-declared-transition-assumption-envelope-contract-inherited-prior-evidence-reference-envelope-reference",
    "p4-m4-declared-transition-assumption-envelope-contract-inherited-prior-request-envelope-reference",
    "p4-m4-declared-transition-assumption-envelope-contract-inherited-prior-boundary-reference",
    "p4-m4-declared-transition-assumption-envelope-contract-inherited-prior-handoff-reference",
    "p4-m4-declared-transition-assumption-envelope-contract-scope",
    "p4-m4-declared-transition-assumption-envelope-contract-declared-transition-assumption-envelope-design-only",
    "p4-m4-declared-transition-assumption-envelope-contract-declared-assumption-surface-definition",
    "p4-m4-declared-transition-assumption-envelope-contract-assumption-non-validation-boundary-definition",
    "p4-m4-declared-transition-assumption-envelope-contract-assumption-non-resolution-boundary-definition",
    "p4-m4-declared-transition-assumption-envelope-contract-assumption-non-scoring-boundary-definition",
    "p4-m4-declared-transition-assumption-envelope-contract-assumption-non-graph-boundary-definition",
    "p4-m4-declared-transition-assumption-envelope-contract-declaration-only-semantics-definition",
    "p4-m4-declared-transition-assumption-envelope-contract-assumption-validation-resolution-scoring-graph-semantics-disabled",
)

DATACLASS_FIELDS = {
    "field_order",
    "field_id",
    "field_name",
    "field_purpose",
    "p4_m4_declared_transition_assumption_envelope_contract_category",
    "p4_m4_declared_transition_assumption_envelope_contract_semantics_disabled",
}

REQUIRED_BOUNDARY_PHRASES = (
    "P4-M4.10",
    "Declared Transition Assumption Envelope Contract",
    "read-only",
    "definition-only",
    "declared-transition-assumption-envelope-design-only",
    "declared-assumption-surface-only",
    "assumption-non-validation-boundary-only",
    "assumption-non-resolution-boundary-only",
    "assumption-non-scoring-boundary-only",
    "assumption-non-graph-boundary-only",
    "declaration-only",
    "inspection-only",
    "P4-M4.10 Declared Transition Assumption Envelope Contract is definition only",
    "P4-M4.10 is declared-transition-assumption-envelope-design-only",
    "P4-M4.10 is declared-assumption-surface-only",
    "P4-M4.10 is assumption-non-validation-boundary-only",
    "P4-M4.10 is assumption-non-resolution-boundary-only",
    "P4-M4.10 is assumption-non-scoring-boundary-only",
    "P4-M4.10 is assumption-non-graph-boundary-only",
    "P4-M4.10 is declaration-only",
    "P4-M4.9 Declared Transition Risk Envelope Contract remains the direct prior declared transition risk envelope reference",
    "P4-M4.9 declared transition risk remains only an inherited static declared risk surface reference",
    "P4-M4.8 Declared Transition Impact Envelope Contract remains the inherited prior declared transition impact envelope reference",
    "P4-M4.8 declared transition impact remains only an inherited static declared impact surface reference",
    "P4-M4.7 Declared Transition Dependency Envelope Contract remains the inherited prior declared transition dependency envelope reference",
    "P4-M4.7 declared transition dependency remains only an inherited static declared dependency surface reference",
    "P4-M4.6 Declared Transition Constraint Envelope Contract remains the inherited prior declared transition constraint envelope reference",
    "P4-M4.6 declared transition constraint remains only an inherited static declared constraint surface reference",
    "P4-M4.5 Declared Transition Reason Envelope Contract remains the inherited prior declared transition reason envelope reference",
    "P4-M4.5 declared transition reason remains only an inherited static declared reason surface reference",
    "P4-M4.4 Target Phase Envelope Contract remains the inherited prior target phase envelope reference",
    "P4-M4.3 Declared Human Context Envelope Contract remains the inherited prior declared human context envelope reference",
    "P4-M4.2 Evidence Reference Envelope Contract remains the inherited prior evidence reference envelope reference",
    "P4-M4.1 Entry Gate Design Request Envelope Contract remains the inherited prior request envelope reference",
    "P4-M4.0 Entry Gate Design Boundary Contract remains the inherited prior design boundary reference",
    "P4-M3.16 Governed Transition Intake Final Phase Handoff Summary remains the inherited prior closed-phase handoff reference",
    "P4-M3 static definition chain remains closed",
    "P4-M4 design layer remains design-boundary-only",
    "P4-M4 declared transition assumption envelope design starts only as a static declared assumption description surface",
    "P4-M4 transition assumption validation remains not implemented",
    "P4-M4 transition assumption resolution remains not implemented",
    "P4-M4 transition assumption scoring remains not implemented",
    "P4-M4 assumption graph construction remains not implemented",
    "P4-M4 assumption dependency solving remains not implemented",
    "P4-M4 assumption consistency checking remains not implemented",
    "P4-M4 assumption sufficiency checking remains not implemented",
    "P4-M4 assumption integrity checking remains not implemented",
    "P4-M4 transition assumption acceptance remains not implemented",
    "P4-M4 transition assumption rejection remains not implemented",
    "P4-M4 transition assumption ranking remains not implemented",
    "P4-M4 transition assumption recommendation remains not implemented",
    "P4-M4 transition assumption generation remains not implemented",
    "P4-M4 transition assumption justification remains not implemented",
    "P4-M4 transition assumption routing remains not implemented",
    "P4-M4 transition assumption planning remains not implemented",
    "P4-M4 transition assumption execution remains not implemented",
    "P4-M4 transition assumption record creation remains not implemented",
    "P4-M4 assumption validation record creation remains not implemented",
    "P4-M4 assumption resolution record creation remains not implemented",
    "P4-M4 assumption scoring record creation remains not implemented",
    "P4-M4 assumption graph record creation remains not implemented",
    "P4-M4 assumption consistency record creation remains not implemented",
    "P4-M4 assumption sufficiency record creation remains not implemented",
    "P4-M4 assumption integrity record creation remains not implemented",
    "P4-M4 assumption routing record creation remains not implemented",
    "P4-M4 assumption planning record creation remains not implemented",
    "P4-M4 assumption justification record creation remains not implemented",
    "P4-M4 transition risk analysis remains not implemented",
    "P4-M4 transition risk validation remains not implemented",
    "P4-M4 transition risk scoring remains not implemented",
    "P4-M4 risk graph construction remains not implemented",
    "P4-M4 transition risk routing remains not implemented",
    "P4-M4 transition risk planning remains not implemented",
    "P4-M4 transition risk execution remains not implemented",
    "P4-M4 transition risk to transition assumption mapping remains not implemented",
    "P4-M4 transition impact to transition assumption mapping remains not implemented",
    "P4-M4 transition dependency to transition assumption mapping remains not implemented",
    "P4-M4 transition constraint to transition assumption mapping remains not implemented",
    "P4-M4 transition reason to transition assumption mapping remains not implemented",
    "P4-M4 target phase to transition assumption mapping remains not implemented",
    "P4-M4 human context to transition assumption mapping remains not implemented",
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
    "no transition assumption intake",
    "no live transition assumption parsing",
    "no transition assumption validation",
    "no transition assumption resolution",
    "no transition assumption scoring",
    "no assumption graph construction",
    "no assumption dependency solving",
    "no assumption consistency checking",
    "no assumption sufficiency checking",
    "no assumption integrity checking",
    "no transition assumption acceptance",
    "no transition assumption rejection",
    "no transition assumption routing",
    "no transition assumption planning",
    "no transition assumption execution",
    "no transition risk to transition assumption mapping",
    "no transition impact to transition assumption mapping",
    "no transition dependency to transition assumption mapping",
    "no transition constraint to transition assumption mapping",
    "no transition reason to transition assumption mapping",
    "no target phase to transition assumption mapping",
    "no human context to transition assumption mapping",
    "no P4-M5",
    "no v7",
    "no productization",
    "no UI",
    "no Operator Console",
    "no version bump",
    "no tag",
)

OPERATOR_SMOKE_PHRASES = (
    "P4-M4.10 Declared Transition Assumption Envelope Contract",
    "read-only",
    "definition-only",
    "declared-transition-assumption-envelope-design-only",
    "declared-assumption-surface-only",
    "assumption-non-validation-boundary-only",
    "assumption-non-resolution-boundary-only",
    "assumption-non-scoring-boundary-only",
    "assumption-non-graph-boundary-only",
    "declaration-only",
    "inspection-only",
    "P4-M4.9 Declared Transition Risk Envelope Contract remains the direct prior declared transition risk envelope reference",
    "P4-M4.9 declared transition risk remains only an inherited static declared risk surface reference",
    "P4-M4 transition assumption validation remains not implemented",
    "P4-M4 transition assumption resolution remains not implemented",
    "P4-M4 transition assumption scoring remains not implemented",
    "P4-M4 assumption graph construction remains not implemented",
    "P4-M4 transition assumption acceptance remains not implemented",
    "P4-M4 transition assumption rejection remains not implemented",
    "P4-M4 transition assumption routing remains not implemented",
    "P4-M4 transition assumption planning remains not implemented",
    "P4-M4 transition assumption execution remains not implemented",
    "P4-M4 transition risk to transition assumption mapping remains not implemented",
    "P4-M4 transition impact to transition assumption mapping remains not implemented",
    "P4-M4 transition dependency to transition assumption mapping remains not implemented",
    "P4-M4 transition constraint to transition assumption mapping remains not implemented",
    "P4-M4 transition reason to transition assumption mapping remains not implemented",
    "P4-M4 target phase to transition assumption mapping remains not implemented",
    "P4-M4 human context to transition assumption mapping remains not implemented",
    "no transition assumption validation",
    "no transition assumption resolution",
    "no transition assumption scoring",
    "no assumption graph construction",
    "no transition assumption acceptance",
    "no transition assumption rejection",
    "no transition assumption routing",
    "no transition assumption planning",
    "no transition assumption execution",
    "no transition risk to transition assumption mapping",
    "no transition impact to transition assumption mapping",
    "no transition dependency to transition assumption mapping",
    "no transition constraint to transition assumption mapping",
    "no transition reason to transition assumption mapping",
    "no target phase to transition assumption mapping",
    "no human context to transition assumption mapping",
    "no P4-M5",
    "no v7",
    "no productization",
    "no UI",
    "no Operator Console",
    "no version bump",
    "no tag",
)

EXPECTED_TRUE_STATUS_FLAGS = TRUE_STATUS_FLAGS
EXPECTED_FALSE_STATUS_FLAGS = FALSE_STATUS_FLAGS

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

PROHIBITED_MEMORY_LOOP_COMMANDS = {
    "transition-assumption-intake",
    "parse-transition-assumption",
    "validate-transition-assumption",
    "resolve-transition-assumption",
    "score-transition-assumption",
    "build-assumption-graph",
    "solve-assumption-dependency",
    "check-assumption-consistency",
    "check-assumption-sufficiency",
    "check-assumption-integrity",
    "accept-transition-assumption",
    "reject-transition-assumption",
    "rank-transition-assumption",
    "recommend-transition-assumption",
    "generate-transition-assumption",
    "justify-transition-assumption",
    "route-transition-assumption",
    "plan-transition-assumption",
    "execute-transition-assumption",
    "create-transition-assumption-record",
    "map-transition-risk-to-transition-assumption",
    "map-transition-impact-to-transition-assumption",
    "map-transition-dependency-to-transition-assumption",
    "map-transition-constraint-to-transition-assumption",
    "map-transition-reason-to-transition-assumption",
    "map-target-phase-to-transition-assumption",
    "map-human-context-to-transition-assumption",
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
    "transition-assumption-verdict",
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


def test_declared_transition_assumption_envelope_contract_field_order_count_and_ids_are_stable():
    fields = list_declared_transition_assumption_envelope_contract_fields()

    assert [field.field_order for field in fields] == list(range(1, 24))
    assert len(fields) == 23
    assert declared_transition_assumption_envelope_contract_field_ids() == FIELD_IDS


def test_every_declared_transition_assumption_envelope_contract_field_has_required_values():
    for field in list_declared_transition_assumption_envelope_contract_fields():
        assert field.field_name.strip()
        assert field.field_purpose.strip()
        assert (
            field.p4_m4_declared_transition_assumption_envelope_contract_category.strip()
        )
        assert (
            field.p4_m4_declared_transition_assumption_envelope_contract_semantics_disabled.strip()
        )


def test_required_boundary_phrase_contract_contains_all_required_phrases():
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in BOUNDARY_PHRASE_LINES
    for phrase in OPERATOR_SMOKE_PHRASES:
        assert (
            phrase in BOUNDARY_PHRASE_LINES
            or phrase in DECLARED_TRANSITION_ASSUMPTION_ENVELOPE_CONTRACT_BOUNDARY
        )


def test_required_status_flag_contract_is_literal_and_complete():
    assert TRUE_STATUS_FLAGS == EXPECTED_TRUE_STATUS_FLAGS
    assert FALSE_STATUS_FLAGS == EXPECTED_FALSE_STATUS_FLAGS


def test_markdown_output_is_stable_and_contains_required_boundaries():
    first = render_declared_transition_assumption_envelope_contract_markdown()
    second = render_declared_transition_assumption_envelope_contract_markdown()

    assert first == second
    assert first.startswith(
        "# P4-M4.10 Declared Transition Assumption Envelope Contract\n"
    )
    assert DECLARED_TRANSITION_ASSUMPTION_ENVELOPE_CONTRACT_BOUNDARY in first
    for field_id in FIELD_IDS:
        assert field_id in first
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in first


def test_json_output_is_stable_and_contains_required_boundaries(tmp_path):
    args = [
        "memory-loop",
        "declared-transition-assumption-envelope-contract",
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
        == DECLARED_TRANSITION_ASSUMPTION_ENVELOPE_CONTRACT_BOUNDARY
    )
    assert first_payload["count"] == 23
    assert first_payload["status"]["phase"] == "P4-M4.10"
    assert (
        first_payload["status"]["feature"]
        == "Declared Transition Assumption Envelope Contract"
    )
    assert first_payload["status"]["mode"] == "read-only"
    assert (
        first_payload["status"]
        == declared_transition_assumption_envelope_contract_report()
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
    first_fields = declared_transition_assumption_envelope_contract_as_dicts()
    second_fields = declared_transition_assumption_envelope_contract_as_dicts()
    first_status = declared_transition_assumption_envelope_contract_report()
    second_status = declared_transition_assumption_envelope_contract_report()

    assert first_fields == second_fields
    assert [field["field_id"] for field in first_fields] == list(FIELD_IDS)
    assert first_status == second_status
    assert first_status["phase"] == "P4-M4.10"
    assert first_status["feature"] == "Declared Transition Assumption Envelope Contract"
    assert first_status["mode"] == "read-only"
    assert first_status["declared_transition_assumption_envelope_contract_field_count"] == 23
    assert (
        first_status[
            "referenced_p4_m4_9_declared_transition_risk_envelope_contract_field_count"
        ]
        == 23
    )
    assert first_status["boundary"] == DECLARED_TRANSITION_ASSUMPTION_ENVELOPE_CONTRACT_BOUNDARY


def test_status_report_locks_true_and_disabled_flags():
    status = declared_transition_assumption_envelope_contract_report()

    for flag in EXPECTED_TRUE_STATUS_FLAGS:
        assert status[flag] is True
    for flag in EXPECTED_FALSE_STATUS_FLAGS:
        assert status[flag] is False


def test_operator_markdown_default_is_read_only_and_creates_no_local_storage(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "declared-transition-assumption-envelope-contract",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith(
        "# P4-M4.10 Declared Transition Assumption Envelope Contract\n"
    )
    assert "## Status Report" in stdout
    assert DECLARED_TRANSITION_ASSUMPTION_ENVELOPE_CONTRACT_BOUNDARY in stdout
    for phrase in OPERATOR_SMOKE_PHRASES:
        assert phrase in stdout
    assert not (tmp_path / ".local").exists()


def test_operator_markdown_format_is_explicit_and_stable(tmp_path):
    args = [
        "memory-loop",
        "declared-transition-assumption-envelope-contract",
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
    assert first_stdout.startswith("# P4-M4.10")
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
            "declared-transition-assumption-envelope-contract",
            "--workspace-root",
            str(tmp_path),
        ]
    )
    json_code, json_payload, json_stderr, _ = _run_operator(
        [
            "memory-loop",
            "declared-transition-assumption-envelope-contract",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert markdown_code == 0
    assert markdown_stderr == ""
    assert markdown_stdout.startswith("# P4-M4.10")
    assert json_code == 0
    assert json_stderr == ""
    assert json_payload["count"] == 23
    assert not (tmp_path / ".local").exists()


def test_command_creates_no_storage_files_or_state_changes(tmp_path):
    _run_operator(
        [
            "memory-loop",
            "declared-transition-assumption-envelope-contract",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    storage_root = tmp_path / ".local" / "subspace_memory"
    for filename in (
        "declared_transition_assumption_envelope_contract.jsonl",
        "transition_assumption_intake.jsonl",
        "transition_assumption_parsing.jsonl",
        "transition_assumption_validation.jsonl",
        "transition_assumption_resolution.jsonl",
        "transition_assumption_scoring.jsonl",
        "assumption_graph_construction.jsonl",
        "assumption_dependency_solving.jsonl",
        "assumption_consistency_checking.jsonl",
        "assumption_sufficiency_checking.jsonl",
        "assumption_integrity_checking.jsonl",
        "transition_assumption_acceptance.jsonl",
        "transition_assumption_rejection.jsonl",
        "transition_assumption_routing.jsonl",
        "transition_assumption_planning.jsonl",
        "transition_assumption_execution.jsonl",
        "transition_assumption_record_creation.jsonl",
        "assumption_validation_record_creation.jsonl",
        "assumption_resolution_record_creation.jsonl",
        "assumption_scoring_record_creation.jsonl",
        "assumption_graph_record_creation.jsonl",
        "assumption_routing_record_creation.jsonl",
        "assumption_planning_record_creation.jsonl",
        "assumption_justification_record_creation.jsonl",
        "transition_risk_to_transition_assumption_mapping.jsonl",
        "transition_impact_to_transition_assumption_mapping.jsonl",
        "transition_dependency_to_transition_assumption_mapping.jsonl",
        "transition_constraint_to_transition_assumption_mapping.jsonl",
        "transition_reason_to_transition_assumption_mapping.jsonl",
        "target_phase_to_transition_assumption_mapping.jsonl",
        "human_context_to_transition_assumption_mapping.jsonl",
    ):
        assert not (storage_root / filename).exists()
    assert not storage_root.exists()


def test_parser_exposes_only_expected_memory_loop_command_surface():
    commands = _memory_loop_subcommands(build_parser())

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
    assert "declared-transition-assumption-envelope-contract" in commands
    assert not (commands & PROHIBITED_MEMORY_LOOP_COMMANDS)


def test_command_is_not_packaged_as_top_level_entry_point():
    entry_points = _project_entry_points()

    assert "declared-transition-assumption-envelope-contract" not in entry_points
    assert "declared-transition-assumption-envelope-contract" not in str(entry_points)


def test_static_doc_contains_required_boundaries_and_fields():
    project_root = Path(__file__).resolve().parents[1]
    doc_path = (
        project_root
        / "docs"
        / "CIVILIZATION_CORE_P4_M4_10_DECLARED_TRANSITION_ASSUMPTION_ENVELOPE_CONTRACT.md"
    )
    doc = doc_path.read_text(encoding="utf-8")

    assert doc.startswith("# P4-M4.10 Declared Transition Assumption Envelope Contract\n")
    for field_id in FIELD_IDS:
        assert field_id in doc
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in doc


def test_custom_field_rendering_remains_definition_only():
    custom = DeclaredTransitionAssumptionEnvelopeContractField(
        field_order=24,
        field_id="custom-declared-transition-assumption-envelope-contract",
        field_name="Custom Declared Transition Assumption Envelope Contract Field",
        field_purpose="Custom read-only declared assumption surface field.",
        p4_m4_declared_transition_assumption_envelope_contract_category=(
            "custom-declared-transition-assumption-envelope-contract-category"
        ),
        p4_m4_declared_transition_assumption_envelope_contract_semantics_disabled=(
            "no transition assumption validation semantics"
        ),
    )

    markdown = render_declared_transition_assumption_envelope_contract_markdown([custom])

    assert "custom-declared-transition-assumption-envelope-contract" in markdown
    assert "Custom read-only declared assumption surface field." in markdown
    assert DECLARED_TRANSITION_ASSUMPTION_ENVELOPE_CONTRACT_BOUNDARY in markdown


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
