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
from hermes_memory_fabric.p4_m4_entry_gate_design_final_phase_handoff_summary import (
    BOUNDARY_PHRASE_LINES,
    ENTRY_GATE_DESIGN_FINAL_PHASE_HANDOFF_SUMMARY_BOUNDARY,
    FALSE_STATUS_FLAGS,
    TRUE_STATUS_FLAGS,
    EntryGateDesignFinalPhaseHandoffSummaryField,
    entry_gate_design_final_phase_handoff_summary_as_dicts,
    entry_gate_design_final_phase_handoff_summary_field_ids,
    entry_gate_design_final_phase_handoff_summary_report,
    list_entry_gate_design_final_phase_handoff_summary_fields,
    render_entry_gate_design_final_phase_handoff_summary_markdown,
)


FIELD_IDS = (
    "p4-m4-entry-gate-design-final-phase-handoff-summary-id",
    "p4-m4-entry-gate-design-final-phase-handoff-summary-phase",
    "p4-m4-entry-gate-design-final-phase-handoff-summary-mode",
    "p4-m4-entry-gate-design-final-phase-handoff-summary-direct-prior-phase-closure-review-reference",
    "p4-m4-entry-gate-design-final-phase-handoff-summary-inherited-prior-closure-handoff-contract-reference",
    "p4-m4-entry-gate-design-final-phase-handoff-summary-inherited-prior-final-non-validation-boundary-audit-reference",
    "p4-m4-entry-gate-design-final-phase-handoff-summary-inherited-prior-declared-transition-package-assembly-envelope-reference",
    "p4-m4-entry-gate-design-final-phase-handoff-summary-inherited-prior-declared-transition-safeguard-envelope-reference",
    "p4-m4-entry-gate-design-final-phase-handoff-summary-inherited-prior-declared-transition-assumption-envelope-reference",
    "p4-m4-entry-gate-design-final-phase-handoff-summary-inherited-prior-declared-transition-risk-envelope-reference",
    "p4-m4-entry-gate-design-final-phase-handoff-summary-inherited-prior-declared-transition-impact-envelope-reference",
    "p4-m4-entry-gate-design-final-phase-handoff-summary-inherited-prior-declared-transition-dependency-envelope-reference",
    "p4-m4-entry-gate-design-final-phase-handoff-summary-inherited-prior-declared-transition-constraint-envelope-reference",
    "p4-m4-entry-gate-design-final-phase-handoff-summary-inherited-prior-declared-transition-reason-envelope-reference",
    "p4-m4-entry-gate-design-final-phase-handoff-summary-inherited-prior-target-phase-envelope-reference",
    "p4-m4-entry-gate-design-final-phase-handoff-summary-inherited-prior-declared-human-context-envelope-reference",
    "p4-m4-entry-gate-design-final-phase-handoff-summary-inherited-prior-evidence-reference-envelope-reference",
    "p4-m4-entry-gate-design-final-phase-handoff-summary-inherited-prior-request-envelope-reference",
    "p4-m4-entry-gate-design-final-phase-handoff-summary-inherited-prior-boundary-reference",
    "p4-m4-entry-gate-design-final-phase-handoff-summary-inherited-prior-closed-phase-handoff-reference",
    "p4-m4-entry-gate-design-final-phase-handoff-summary-static-summary-surface-definition",
    "p4-m4-entry-gate-design-final-phase-handoff-summary-declaration-only-semantics-definition",
    "p4-m4-entry-gate-design-final-phase-handoff-summary-validation-scoring-verdict-execution-record-mutation-p4-m5-start-semantics-disabled",
)

DATACLASS_FIELDS = {
    "field_order",
    "field_id",
    "field_name",
    "field_purpose",
    "p4_m4_entry_gate_design_final_phase_handoff_summary_category",
    "p4_m4_entry_gate_design_final_phase_handoff_summary_semantics_disabled",
}

REQUIRED_BOUNDARY_PHRASES = tuple(
    line
    for line in """
P4-M4.16
Entry Gate Design Final Phase Handoff Summary
read-only
definition-only
entry-gate-design-final-phase-handoff-summary-only
final-phase-handoff-summary-surface-only
final-phase-handoff-non-validation-boundary-only
final-phase-handoff-non-scoring-boundary-only
final-phase-handoff-non-verdict-boundary-only
final-phase-handoff-non-execution-boundary-only
final-phase-handoff-non-record-boundary-only
final-phase-handoff-non-mutation-boundary-only
p4-m5-non-start-boundary-only
declaration-only
inspection-only
P4-M4.16 Entry Gate Design Final Phase Handoff Summary is definition only
P4-M4.16 is entry-gate-design-final-phase-handoff-summary-only
P4-M4.16 is final-phase-handoff-summary-surface-only
P4-M4.16 is final-phase-handoff-non-validation-boundary-only
P4-M4.16 is final-phase-handoff-non-scoring-boundary-only
P4-M4.16 is final-phase-handoff-non-verdict-boundary-only
P4-M4.16 is final-phase-handoff-non-execution-boundary-only
P4-M4.16 is final-phase-handoff-non-record-boundary-only
P4-M4.16 is final-phase-handoff-non-mutation-boundary-only
P4-M4.16 is p4-m5-non-start-boundary-only
P4-M4.16 is declaration-only
P4-M4.15 Entry Gate Design Phase Closure Review remains the direct prior phase closure review reference
P4-M4.15 phase closure review remains only an inherited static phase closure review surface reference
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
P4-M4 final phase handoff summary starts only as a static declared summary surface
P4-M4 final phase handoff validation remains not implemented
P4-M4 final phase handoff scoring remains not implemented
P4-M4 final phase handoff verdict remains not implemented
P4-M4 final phase handoff execution remains not implemented
P4-M4 final phase handoff record creation remains not implemented
P4-M4 final phase handoff storage remains not implemented
P4-M4 final phase handoff persistence remains not implemented
P4-M4 final phase handoff mutation remains not implemented
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
no final phase handoff validation
no final phase handoff scoring
no final phase handoff verdict
no final phase handoff execution
no final phase handoff record creation
no final phase handoff storage
no final phase handoff persistence
no final phase handoff mutation
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
    "P4-M4.16 Entry Gate Design Final Phase Handoff Summary",
    "read-only",
    "definition-only",
    "entry-gate-design-final-phase-handoff-summary-only",
    "final-phase-handoff-summary-surface-only",
    "final-phase-handoff-non-validation-boundary-only",
    "final-phase-handoff-non-scoring-boundary-only",
    "final-phase-handoff-non-verdict-boundary-only",
    "final-phase-handoff-non-execution-boundary-only",
    "final-phase-handoff-non-record-boundary-only",
    "final-phase-handoff-non-mutation-boundary-only",
    "p4-m5-non-start-boundary-only",
    "declaration-only",
    "inspection-only",
    "P4-M4.15 Entry Gate Design Phase Closure Review remains the direct prior phase closure review reference",
    "P4-M4.15 phase closure review remains only an inherited static phase closure review surface reference",
    "P4-M4 final phase handoff summary starts only as a static declared summary surface",
    "P4-M4 final phase handoff validation remains not implemented",
    "P4-M4 final phase handoff scoring remains not implemented",
    "P4-M4 final phase handoff verdict remains not implemented",
    "P4-M4 final phase handoff execution remains not implemented",
    "P4-M5 remains not started",
    "no final phase handoff validation",
    "no final phase handoff scoring",
    "no final phase handoff verdict",
    "no final phase handoff execution",
    "no final phase handoff record creation",
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
}


def test_field_inventory_is_exact_and_ordered():
    fields = list_entry_gate_design_final_phase_handoff_summary_fields()

    assert len(fields) == 23
    assert entry_gate_design_final_phase_handoff_summary_field_ids() == FIELD_IDS
    assert tuple(field.field_order for field in fields) == tuple(range(1, 24))
    assert all(
        isinstance(field, EntryGateDesignFinalPhaseHandoffSummaryField)
        for field in fields
    )
    assert {
        field.name
        for field in dataclasses.fields(EntryGateDesignFinalPhaseHandoffSummaryField)
    } == DATACLASS_FIELDS


def test_boundary_phrase_inventory_is_required_contract():
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in BOUNDARY_PHRASE_LINES
        assert phrase in ENTRY_GATE_DESIGN_FINAL_PHASE_HANDOFF_SUMMARY_BOUNDARY


def test_markdown_renders_static_boundary_and_field_ids():
    markdown = render_entry_gate_design_final_phase_handoff_summary_markdown()

    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in markdown
    for field_id in FIELD_IDS:
        assert field_id in markdown
    assert "## Status Report" in markdown
    assert "## Entry Gate Design Final Phase Handoff Summary Fields" in markdown
    assert "P4-M4.16 Entry Gate Design Final Phase Handoff Summary" in markdown


def test_report_has_required_true_false_status_flags():
    status = entry_gate_design_final_phase_handoff_summary_report()

    assert status["phase"] == "P4-M4.16"
    assert status["feature"] == "Entry Gate Design Final Phase Handoff Summary"
    assert status["mode"] == "read-only"
    assert status["package_version"] == "6.16.0"
    assert status["entry_gate_design_final_phase_handoff_summary_field_count"] == 23
    assert (
        status[
            "referenced_p4_m4_15_entry_gate_design_phase_closure_review_field_count"
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
    fields = entry_gate_design_final_phase_handoff_summary_as_dicts()

    assert len(fields) == 23
    assert tuple(field["field_id"] for field in fields) == FIELD_IDS
    assert fields == entry_gate_design_final_phase_handoff_summary_as_dicts()
    assert all(
        field["p4_m4_entry_gate_design_final_phase_handoff_summary_category"]
        == "p4-m4-entry-gate-design-final-phase-handoff-summary-category"
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
            "entry-gate-design-final-phase-handoff-summary",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith(
        "# P4-M4.16 Entry Gate Design Final Phase Handoff Summary\n"
    )
    for phrase in OPERATOR_SMOKE_PHRASES:
        assert phrase in stdout
    assert not (tmp_path / ".local" / "subspace_memory").exists()


def test_operator_json_command_returns_required_report(tmp_path: Path):
    code, output, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "entry-gate-design-final-phase-handoff-summary",
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
    assert output["boundary"] == ENTRY_GATE_DESIGN_FINAL_PHASE_HANDOFF_SUMMARY_BOUNDARY
    assert tuple(field["field_id"] for field in output["fields"]) == FIELD_IDS
    status = output["status"]
    assert status["phase"] == "P4-M4.16"
    assert status["feature"] == "Entry Gate Design Final Phase Handoff Summary"
    assert status["mode"] == "read-only"
    for flag in EXPECTED_TRUE_STATUS_FLAGS:
        assert status[flag] is True
    for flag in EXPECTED_FALSE_STATUS_FLAGS:
        assert status[flag] is False
    assert not (tmp_path / ".local" / "subspace_memory").exists()


def test_parser_exposes_only_expected_memory_loop_command_surface():
    commands = _memory_loop_subcommands(build_parser())

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
    assert "entry-gate-design-final-phase-handoff-summary" in commands


def test_pyproject_entry_points_do_not_productize_command():
    pyproject = tomllib.loads(Path("pyproject.toml").read_text())
    entry_points = pyproject["project"]["entry-points"]

    assert "entry-gate-design-final-phase-handoff-summary" not in entry_points
    assert "entry-gate-design-final-phase-handoff-summary" not in str(entry_points)
    assert pyproject["project"]["version"] == "6.16.0"


def test_static_doc_contains_required_boundaries_and_fields():
    project_root = Path(__file__).resolve().parents[1]
    doc_path = (
        project_root
        / "docs"
        / "CIVILIZATION_CORE_P4_M4_16_ENTRY_GATE_DESIGN_FINAL_PHASE_HANDOFF_SUMMARY.md"
    )
    doc = doc_path.read_text(encoding="utf-8")

    assert doc.startswith(
        "# P4-M4.16 Entry Gate Design Final Phase Handoff Summary\n"
    )
    for field_id in FIELD_IDS:
        assert field_id in doc
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in doc


def test_custom_field_rendering_remains_definition_only():
    field = EntryGateDesignFinalPhaseHandoffSummaryField(
        field_order=99,
        field_id="custom-entry-gate-design-final-phase-handoff-summary",
        field_name="Custom Entry Gate Design Final Phase Handoff Summary",
        field_purpose="custom read-only definition-only inspection-only field",
        p4_m4_entry_gate_design_final_phase_handoff_summary_category=(
            "custom-entry-gate-design-final-phase-handoff-summary-category"
        ),
        p4_m4_entry_gate_design_final_phase_handoff_summary_semantics_disabled=(
            "no validation semantics; no execution semantics; no mutation semantics"
        ),
    )

    markdown = render_entry_gate_design_final_phase_handoff_summary_markdown((field,))

    assert "custom-entry-gate-design-final-phase-handoff-summary" in markdown
    assert "no validation semantics; no execution semantics" in markdown
    assert "P4-M4.16 Entry Gate Design Final Phase Handoff Summary" in markdown


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
