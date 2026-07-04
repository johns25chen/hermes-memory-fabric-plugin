from __future__ import annotations

import argparse
import io
import json
import tomllib
from pathlib import Path

from hermes_memory_fabric.p4_m0_subspace_operator import build_parser, run_operator_command
from hermes_memory_fabric.p4_m4_entry_gate_design_final_non_validation_boundary_audit import (
    BOUNDARY_PHRASE_LINES,
    ENTRY_GATE_DESIGN_FINAL_NON_VALIDATION_BOUNDARY_AUDIT_BOUNDARY,
    FALSE_STATUS_FLAGS,
    TRUE_STATUS_FLAGS,
    EntryGateDesignFinalNonValidationBoundaryAuditField,
    entry_gate_design_final_non_validation_boundary_audit_as_dicts,
    entry_gate_design_final_non_validation_boundary_audit_field_ids,
    entry_gate_design_final_non_validation_boundary_audit_report,
    list_entry_gate_design_final_non_validation_boundary_audit_fields,
    render_entry_gate_design_final_non_validation_boundary_audit_markdown,
)


FIELD_IDS = (
    "p4-m4-entry-gate-design-final-non-validation-boundary-audit-id",
    "p4-m4-entry-gate-design-final-non-validation-boundary-audit-phase",
    "p4-m4-entry-gate-design-final-non-validation-boundary-audit-mode",
    "p4-m4-entry-gate-design-final-non-validation-boundary-audit-direct-prior-declared-transition-package-assembly-envelope-reference",
    "p4-m4-entry-gate-design-final-non-validation-boundary-audit-inherited-prior-declared-transition-safeguard-envelope-reference",
    "p4-m4-entry-gate-design-final-non-validation-boundary-audit-inherited-prior-declared-transition-assumption-envelope-reference",
    "p4-m4-entry-gate-design-final-non-validation-boundary-audit-inherited-prior-declared-transition-risk-envelope-reference",
    "p4-m4-entry-gate-design-final-non-validation-boundary-audit-inherited-prior-declared-transition-impact-envelope-reference",
    "p4-m4-entry-gate-design-final-non-validation-boundary-audit-inherited-prior-declared-transition-dependency-envelope-reference",
    "p4-m4-entry-gate-design-final-non-validation-boundary-audit-inherited-prior-declared-transition-constraint-envelope-reference",
    "p4-m4-entry-gate-design-final-non-validation-boundary-audit-inherited-prior-declared-transition-reason-envelope-reference",
    "p4-m4-entry-gate-design-final-non-validation-boundary-audit-inherited-prior-target-phase-envelope-reference",
    "p4-m4-entry-gate-design-final-non-validation-boundary-audit-inherited-prior-declared-human-context-envelope-reference",
    "p4-m4-entry-gate-design-final-non-validation-boundary-audit-inherited-prior-evidence-reference-envelope-reference",
    "p4-m4-entry-gate-design-final-non-validation-boundary-audit-inherited-prior-request-envelope-reference",
    "p4-m4-entry-gate-design-final-non-validation-boundary-audit-inherited-prior-boundary-reference",
    "p4-m4-entry-gate-design-final-non-validation-boundary-audit-inherited-prior-handoff-reference",
    "p4-m4-entry-gate-design-final-non-validation-boundary-audit-scope",
    "p4-m4-entry-gate-design-final-non-validation-boundary-audit-design-only",
    "p4-m4-entry-gate-design-final-non-validation-boundary-audit-static-audit-surface-definition",
    "p4-m4-entry-gate-design-final-non-validation-boundary-audit-final-non-validation-verdict-execution-boundary-definition",
    "p4-m4-entry-gate-design-final-non-validation-boundary-audit-declaration-only-semantics-definition",
    "p4-m4-entry-gate-design-final-non-validation-boundary-audit-validation-verdict-execution-record-mutation-semantics-disabled",
)

DATACLASS_FIELDS = {
    "field_order",
    "field_id",
    "field_name",
    "field_purpose",
    "p4_m4_entry_gate_design_final_non_validation_boundary_audit_category",
    "p4_m4_entry_gate_design_final_non_validation_boundary_audit_semantics_disabled",
}

REQUIRED_BOUNDARY_PHRASES = tuple(
    line
    for line in """
P4-M4.13
Entry Gate Design Final Non-Validation Boundary Audit
read-only
definition-only
entry-gate-design-final-non-validation-boundary-audit-only
final-non-validation-audit-surface-only
final-non-validation-boundary-only
final-non-verdict-boundary-only
final-non-execution-boundary-only
final-non-record-boundary-only
final-non-mutation-boundary-only
declaration-only
inspection-only
P4-M4.13 Entry Gate Design Final Non-Validation Boundary Audit is definition only
P4-M4.13 is entry-gate-design-final-non-validation-boundary-audit-only
P4-M4.13 is final-non-validation-audit-surface-only
P4-M4.13 is final-non-validation-boundary-only
P4-M4.13 is final-non-verdict-boundary-only
P4-M4.13 is final-non-execution-boundary-only
P4-M4.13 is final-non-record-boundary-only
P4-M4.13 is final-non-mutation-boundary-only
P4-M4.13 is declaration-only
P4-M4.12 Declared Transition Package Assembly Envelope Contract remains the direct prior declared transition package assembly envelope reference
P4-M4.12 declared transition package assembly remains only an inherited static declared package assembly surface reference
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
P4-M4 final non-validation boundary audit starts only as a static declared audit surface
P4-M4 entry gate validation remains not implemented
P4-M4 readiness validation remains not implemented
P4-M4 transition validation remains not implemented
P4-M4 package validation remains not implemented
P4-M4 transition package assembly validation remains not implemented
P4-M4 transition package assembly composition remains not implemented
P4-M4 transition package assembly execution remains not implemented
P4-M4 transition package assembly scoring remains not implemented
P4-M4 transition package assembly routing remains not implemented
P4-M4 transition package assembly planning remains not implemented
P4-M4 package assembly graph construction remains not implemented
P4-M4 transition safeguard validation remains not implemented
P4-M4 transition safeguard enforcement remains not implemented
P4-M4 transition safeguard execution remains not implemented
P4-M4 transition assumption validation remains not implemented
P4-M4 transition risk validation remains not implemented
P4-M4 transition impact validation remains not implemented
P4-M4 transition dependency validation remains not implemented
P4-M4 transition constraint validation remains not implemented
P4-M4 transition reason validation remains not implemented
P4-M4 target phase validation remains not implemented
P4-M4 human context validation remains not implemented
P4-M4 evidence validation remains not implemented
P4-M4 reference validation remains not implemented
P4-M4 citation validation remains not implemented
P4-M4 reference resolution remains not implemented
P4-M4 source fetching remains not implemented
P4-M4 provenance writing remains not implemented
P4-M4 request intake remains not implemented
P4-M4 request validation remains not implemented
P4-M4 verdict generation remains not implemented
P4-M4 approval remains not implemented
P4-M4 authorization remains not implemented
P4-M4 confirmation remains not implemented
P4-M4 recommendation remains not implemented
P4-M4 ranking remains not implemented
P4-M4 transition execution remains not implemented
P4-M4 record creation remains not implemented
P4-M4 storage remains not implemented
P4-M4 persistence remains not implemented
P4-M4 mutation remains not implemented
P4-M5 remains not started
v7 remains not started
productization remains not started
UI remains not started
Operator Console remains not started
no entry gate validation
no readiness validation
no transition validation
no package validation
no package assembly validation
no package assembly composition
no package assembly execution
no package assembly scoring
no package assembly routing
no package assembly planning
no package assembly graph construction
no safeguard validation
no assumption validation
no risk validation
no impact validation
no dependency validation
no constraint validation
no reason validation
no target phase validation
no human context validation
no evidence validation
no reference validation
no citation validation
no reference resolution
no source fetching
no provenance writing
no request intake
no request validation
no verdict generation
no approval
no authorization
no confirmation
no recommendation
no ranking
no transition execution
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
    "P4-M4.13 Entry Gate Design Final Non-Validation Boundary Audit",
    "read-only",
    "definition-only",
    "entry-gate-design-final-non-validation-boundary-audit-only",
    "final-non-validation-audit-surface-only",
    "final-non-validation-boundary-only",
    "final-non-verdict-boundary-only",
    "final-non-execution-boundary-only",
    "final-non-record-boundary-only",
    "final-non-mutation-boundary-only",
    "declaration-only",
    "inspection-only",
    "P4-M4.12 Declared Transition Package Assembly Envelope Contract remains the direct prior declared transition package assembly envelope reference",
    "P4-M4.12 declared transition package assembly remains only an inherited static declared package assembly surface reference",
    "P4-M4 final non-validation boundary audit starts only as a static declared audit surface",
    "P4-M4 entry gate validation remains not implemented",
    "P4-M4 readiness validation remains not implemented",
    "P4-M4 transition validation remains not implemented",
    "P4-M4 package validation remains not implemented",
    "P4-M4 transition package assembly validation remains not implemented",
    "P4-M4 verdict generation remains not implemented",
    "P4-M4 approval remains not implemented",
    "P4-M4 authorization remains not implemented",
    "P4-M4 confirmation remains not implemented",
    "P4-M4 transition execution remains not implemented",
    "P4-M4 record creation remains not implemented",
    "no entry gate validation",
    "no readiness validation",
    "no transition validation",
    "no package validation",
    "no package assembly validation",
    "no verdict generation",
    "no approval",
    "no authorization",
    "no confirmation",
    "no transition execution",
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
}

PROHIBITED_MEMORY_LOOP_COMMANDS = {
    "validate-entry-gate",
    "validate-readiness",
    "validate-transition",
    "validate-package",
    "validate-package-assembly",
    "compose-package-assembly",
    "execute-package-assembly",
    "score-package-assembly",
    "route-package-assembly",
    "plan-package-assembly",
    "build-package-assembly-graph",
    "final-audit-execution",
    "live-audit-evaluation",
    "generate-verdict",
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
}


def test_entry_gate_design_final_non_validation_boundary_audit_field_order_count_and_ids_are_stable():
    fields = list_entry_gate_design_final_non_validation_boundary_audit_fields()

    assert [field.field_order for field in fields] == list(range(1, 24))
    assert len(fields) == 23
    assert entry_gate_design_final_non_validation_boundary_audit_field_ids() == FIELD_IDS


def test_every_entry_gate_design_final_non_validation_boundary_audit_field_has_required_values():
    for field in list_entry_gate_design_final_non_validation_boundary_audit_fields():
        assert field.field_name.strip()
        assert field.field_purpose.strip()
        assert (
            field.p4_m4_entry_gate_design_final_non_validation_boundary_audit_category.strip()
        )
        assert (
            field.p4_m4_entry_gate_design_final_non_validation_boundary_audit_semantics_disabled.strip()
        )


def test_required_boundary_phrase_contract_contains_all_required_phrases():
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in BOUNDARY_PHRASE_LINES
        assert phrase in ENTRY_GATE_DESIGN_FINAL_NON_VALIDATION_BOUNDARY_AUDIT_BOUNDARY
    for phrase in OPERATOR_SMOKE_PHRASES:
        assert (
            phrase in BOUNDARY_PHRASE_LINES
            or phrase in ENTRY_GATE_DESIGN_FINAL_NON_VALIDATION_BOUNDARY_AUDIT_BOUNDARY
        )


def test_markdown_output_is_stable_and_contains_required_boundaries():
    first = render_entry_gate_design_final_non_validation_boundary_audit_markdown()
    second = render_entry_gate_design_final_non_validation_boundary_audit_markdown()

    assert first == second
    assert first.startswith(
        "# P4-M4.13 Entry Gate Design Final Non-Validation Boundary Audit\n"
    )
    assert ENTRY_GATE_DESIGN_FINAL_NON_VALIDATION_BOUNDARY_AUDIT_BOUNDARY in first
    for field_id in FIELD_IDS:
        assert field_id in first
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in first


def test_json_output_is_stable_and_contains_required_boundaries(tmp_path):
    args = [
        "memory-loop",
        "entry-gate-design-final-non-validation-boundary-audit",
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
        == ENTRY_GATE_DESIGN_FINAL_NON_VALIDATION_BOUNDARY_AUDIT_BOUNDARY
    )
    assert first_payload["count"] == 23
    assert first_payload["status"]["phase"] == "P4-M4.13"
    assert (
        first_payload["status"]["feature"]
        == "Entry Gate Design Final Non-Validation Boundary Audit"
    )
    assert first_payload["status"]["mode"] == "read-only"
    assert first_payload["status"] == (
        entry_gate_design_final_non_validation_boundary_audit_report()
    )
    assert [item["field_id"] for item in first_payload["fields"]] == list(FIELD_IDS)
    assert set(first_payload["fields"][0]) == DATACLASS_FIELDS
    for flag in TRUE_STATUS_FLAGS:
        assert first_payload["status"][flag] is True
    for flag in FALSE_STATUS_FLAGS:
        assert first_payload["status"][flag] is False
    for phrase in OPERATOR_SMOKE_PHRASES:
        assert phrase in first_stdout
    assert not (tmp_path / ".local").exists()


def test_dict_conversion_and_status_report_are_deterministic():
    first_fields = entry_gate_design_final_non_validation_boundary_audit_as_dicts()
    second_fields = entry_gate_design_final_non_validation_boundary_audit_as_dicts()
    first_status = entry_gate_design_final_non_validation_boundary_audit_report()
    second_status = entry_gate_design_final_non_validation_boundary_audit_report()

    assert first_fields == second_fields
    assert [field["field_id"] for field in first_fields] == list(FIELD_IDS)
    assert first_status == second_status
    assert first_status["phase"] == "P4-M4.13"
    assert first_status["feature"] == (
        "Entry Gate Design Final Non-Validation Boundary Audit"
    )
    assert first_status["mode"] == "read-only"
    assert (
        first_status[
            "entry_gate_design_final_non_validation_boundary_audit_field_count"
        ]
        == 23
    )
    assert (
        first_status[
            "referenced_p4_m4_12_declared_transition_package_assembly_envelope_contract_field_count"
        ]
        == 23
    )


def test_status_report_locks_true_and_disabled_flags():
    status = entry_gate_design_final_non_validation_boundary_audit_report()

    for flag in TRUE_STATUS_FLAGS:
        assert status[flag] is True
    for flag in FALSE_STATUS_FLAGS:
        assert status[flag] is False


def test_operator_markdown_default_is_read_only_and_creates_no_local_storage(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "entry-gate-design-final-non-validation-boundary-audit",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith(
        "# P4-M4.13 Entry Gate Design Final Non-Validation Boundary Audit\n"
    )
    assert "## Status Report" in stdout
    assert ENTRY_GATE_DESIGN_FINAL_NON_VALIDATION_BOUNDARY_AUDIT_BOUNDARY in stdout
    for phrase in OPERATOR_SMOKE_PHRASES:
        assert phrase in stdout
    assert not (tmp_path / ".local").exists()


def test_operator_markdown_format_is_explicit_and_stable(tmp_path):
    args = [
        "memory-loop",
        "entry-gate-design-final-non-validation-boundary-audit",
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
    assert first_stdout.startswith("# P4-M4.13")
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
            "entry-gate-design-final-non-validation-boundary-audit",
            "--workspace-root",
            str(tmp_path),
        ]
    )
    json_code, json_payload, json_stderr, _ = _run_operator(
        [
            "memory-loop",
            "entry-gate-design-final-non-validation-boundary-audit",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert markdown_code == 0
    assert markdown_stderr == ""
    assert markdown_stdout.startswith("# P4-M4.13")
    assert json_code == 0
    assert json_stderr == ""
    assert json_payload["count"] == 23
    assert not (tmp_path / ".local").exists()


def test_command_creates_no_storage_files_or_state_changes(tmp_path):
    _run_operator(
        [
            "memory-loop",
            "entry-gate-design-final-non-validation-boundary-audit",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    storage_root = tmp_path / ".local" / "subspace_memory"
    for filename in (
        "entry_gate_design_final_non_validation_boundary_audit.jsonl",
        "final_non_validation_audit_execution.jsonl",
        "live_audit_evaluation.jsonl",
        "entry_gate_validation.jsonl",
        "readiness_validation.jsonl",
        "transition_validation.jsonl",
        "package_validation.jsonl",
        "package_assembly_validation.jsonl",
        "package_assembly_composition.jsonl",
        "package_assembly_execution.jsonl",
        "package_assembly_scoring.jsonl",
        "package_assembly_routing.jsonl",
        "package_assembly_planning.jsonl",
        "package_assembly_graph_construction.jsonl",
        "verdict_generation.jsonl",
        "approval.jsonl",
        "authorization.jsonl",
        "confirmation.jsonl",
        "recommendation.jsonl",
        "ranking.jsonl",
        "transition_execution.jsonl",
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
    assert "entry-gate-design-final-non-validation-boundary-audit" in commands
    assert not (commands & PROHIBITED_MEMORY_LOOP_COMMANDS)


def test_command_is_not_packaged_as_top_level_entry_point():
    entry_points = _project_entry_points()

    assert "entry-gate-design-final-non-validation-boundary-audit" not in entry_points
    assert "entry-gate-design-final-non-validation-boundary-audit" not in str(
        entry_points
    )


def test_static_doc_contains_required_boundaries_and_fields():
    project_root = Path(__file__).resolve().parents[1]
    doc_path = (
        project_root
        / "docs"
        / "CIVILIZATION_CORE_P4_M4_13_ENTRY_GATE_DESIGN_FINAL_NON_VALIDATION_BOUNDARY_AUDIT.md"
    )
    doc = doc_path.read_text(encoding="utf-8")

    assert doc.startswith(
        "# P4-M4.13 Entry Gate Design Final Non-Validation Boundary Audit\n"
    )
    for field_id in FIELD_IDS:
        assert field_id in doc
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in doc


def test_custom_field_rendering_remains_definition_only():
    custom = EntryGateDesignFinalNonValidationBoundaryAuditField(
        field_order=24,
        field_id="custom-entry-gate-design-final-non-validation-boundary-audit",
        field_name="Custom Entry Gate Design Final Non-Validation Boundary Audit Field",
        field_purpose="Custom read-only final non-validation audit surface field.",
        p4_m4_entry_gate_design_final_non_validation_boundary_audit_category=(
            "custom-entry-gate-design-final-non-validation-boundary-audit-category"
        ),
        p4_m4_entry_gate_design_final_non_validation_boundary_audit_semantics_disabled=(
            "no validation semantics"
        ),
    )

    markdown = render_entry_gate_design_final_non_validation_boundary_audit_markdown(
        [custom]
    )

    assert "custom-entry-gate-design-final-non-validation-boundary-audit" in markdown
    assert "Custom read-only final non-validation audit surface field." in markdown
    assert ENTRY_GATE_DESIGN_FINAL_NON_VALIDATION_BOUNDARY_AUDIT_BOUNDARY in markdown


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
