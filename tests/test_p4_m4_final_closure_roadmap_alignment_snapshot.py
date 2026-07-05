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
from hermes_memory_fabric.p4_m4_final_closure_roadmap_alignment_snapshot import (
    BOUNDARY_PHRASE_LINES,
    FALSE_STATUS_FLAGS,
    P4_M4_FINAL_CLOSURE_ROADMAP_ALIGNMENT_SNAPSHOT_BOUNDARY,
    TRUE_STATUS_FLAGS,
    P4M4FinalClosureRoadmapAlignmentSnapshotField,
    list_p4_m4_final_closure_roadmap_alignment_snapshot_fields,
    p4_m4_final_closure_roadmap_alignment_snapshot_as_dicts,
    p4_m4_final_closure_roadmap_alignment_snapshot_field_ids,
    p4_m4_final_closure_roadmap_alignment_snapshot_report,
    render_p4_m4_final_closure_roadmap_alignment_snapshot_markdown,
)


FIELD_IDS = (
    "p4-m4-final-closure-roadmap-alignment-snapshot-id",
    "p4-m4-final-closure-roadmap-alignment-snapshot-phase",
    "p4-m4-final-closure-roadmap-alignment-snapshot-mode",
    "p4-m4-final-closure-roadmap-alignment-snapshot-p4-m4-cross-project-governance-preparation-position",
    "p4-m4-final-closure-roadmap-alignment-snapshot-p4-m5-api-mcp-connector-readiness-audit-position",
    "p4-m4-final-closure-roadmap-alignment-snapshot-direct-prior-final-closure-boundary-freeze-index-reference",
    "p4-m4-final-closure-roadmap-alignment-snapshot-inherited-prior-final-closure-non-start-bridge-index-reference",
    "p4-m4-final-closure-roadmap-alignment-snapshot-inherited-prior-final-closure-transition-readiness-non-start-index-reference",
    "p4-m4-final-closure-roadmap-alignment-snapshot-inherited-prior-final-closure-operator-handoff-index-reference",
    "p4-m4-final-closure-roadmap-alignment-snapshot-inherited-prior-final-closure-evidence-index-reference",
    "p4-m4-final-closure-roadmap-alignment-snapshot-inherited-prior-final-closure-index-entry-planning-gate-reference",
    "p4-m4-final-closure-roadmap-alignment-snapshot-inherited-prior-terminal-closure-seal-reference",
    "p4-m4-final-closure-roadmap-alignment-snapshot-inherited-prior-final-phase-handoff-summary-reference",
    "p4-m4-final-closure-roadmap-alignment-snapshot-inherited-prior-phase-closure-review-reference",
    "p4-m4-final-closure-roadmap-alignment-snapshot-inherited-prior-closure-handoff-contract-reference",
    "p4-m4-final-closure-roadmap-alignment-snapshot-inherited-prior-final-non-validation-boundary-audit-reference",
    "p4-m4-final-closure-roadmap-alignment-snapshot-static-final-closure-stack-reference-only-confirmation",
    "p4-m4-final-closure-roadmap-alignment-snapshot-fc0-through-fc5-not-readiness-validation-scoring-verdict-routing-execution-evidence",
    "p4-m4-final-closure-roadmap-alignment-snapshot-p4-m5-transition-requires-explicit-human-confirmation",
    "p4-m4-final-closure-roadmap-alignment-snapshot-api-mcp-connector-readiness-audit-only-future-phase",
    "p4-m4-final-closure-roadmap-alignment-snapshot-api-mcp-connector-implementation-disabled",
    "p4-m4-final-closure-roadmap-alignment-snapshot-v7-productization-ui-operator-console-deferred",
    "p4-m4-final-closure-roadmap-alignment-snapshot-static-alignment-and-validation-scoring-verdict-routing-execution-record-mutation-semantics-disabled",
)

DATACLASS_FIELDS = {
    "field_order",
    "field_id",
    "field_name",
    "field_purpose",
    "p4_m4_final_closure_roadmap_alignment_snapshot_category",
    "p4_m4_final_closure_roadmap_alignment_snapshot_semantics_disabled",
}

REQUIRED_BOUNDARY_PHRASES = tuple(
    line
    for line in """
P4-M4-FC.6
P4-M4 Final Closure Roadmap Alignment Snapshot
read-only
definition-only
p4-m4-final-closure-roadmap-alignment-snapshot-only
roadmap-alignment-snapshot-only
roadmap-alignment-non-validation-boundary-only
roadmap-alignment-non-scoring-boundary-only
roadmap-alignment-non-verdict-boundary-only
roadmap-alignment-non-routing-boundary-only
roadmap-alignment-non-execution-boundary-only
roadmap-alignment-non-record-boundary-only
roadmap-alignment-non-mutation-boundary-only
p4-m5-readiness-audit-future-phase-only
p4-m5-non-start-boundary-only
declaration-only
inspection-only
P4-M4-FC.6 is not P4-M4.18
P4-M4-FC.6 is not P4-M5
P4-M4-FC.6 is not P4-M5.0
P4-M4-FC.6 P4-M4 Final Closure Roadmap Alignment Snapshot is definition only
P4-M4.x remains cross-project memory governance preparation
P4-M5.x remains API / MCP / Connector readiness audit
P4-M5.x is not API implementation
P4-M5.x is not MCP implementation
P4-M5.x is not Connector implementation
P4-M5.x is not Agent auto-call
P4-M5.x is not UI
P4-M5.x is not Operator Console
P4-M5.x is not productization
P4-M5.x is not v7
P4-M5 readiness audit remains future-phase only
P4-M5 phase transition requires explicit human confirmation
P4-M4-FC.5 P4-M4 Final Closure Boundary Freeze Index remains the direct prior final closure boundary freeze index reference
P4-M4-FC.4 P4-M4 Final Closure Non-Start Bridge Index remains the inherited prior final closure non-start bridge index reference
P4-M4-FC.3 P4-M4 Final Closure Transition Readiness Non-Start Index remains the inherited prior final closure transition readiness non-start index reference
P4-M4-FC.2 P4-M4 Final Closure Operator Handoff Index remains the inherited prior final closure operator handoff index reference
P4-M4-FC.1 P4-M4 Final Closure Evidence Index remains the inherited prior final closure evidence index reference
P4-M4-FC.0 P4-M4 Final Closure Index / P4-M5 Entry Planning Gate remains the inherited prior final closure index and entry planning gate reference
P4-M4.17 Entry Gate Design Phase Terminal Closure Seal remains the inherited prior terminal closure seal reference
P4-M4 static definition chain remains closed
P4-M4 design layer remains terminally sealed
P4-M4 final closure stack remains static reference-only
FC.0 through FC.5 remain static final closure reference layers only
FC.0 through FC.5 are not readiness evidence
FC.0 through FC.5 are not validation evidence
FC.0 through FC.5 are not scoring evidence
FC.0 through FC.5 are not verdict evidence
FC.0 through FC.5 are not routing evidence
FC.0 through FC.5 are not execution evidence
roadmap alignment validation remains not implemented
roadmap alignment scoring remains not implemented
roadmap alignment verdict remains not implemented
roadmap alignment routing remains not implemented
roadmap alignment execution remains not implemented
roadmap alignment record creation remains not implemented
roadmap alignment storage remains not implemented
roadmap alignment persistence remains not implemented
roadmap alignment mutation remains not implemented
P4-M5 entry validation remains not implemented
P4-M5 readiness validation remains not implemented
P4-M5 readiness inference remains not implemented
P4-M5 readiness scoring remains not implemented
P4-M5 readiness verdict remains not implemented
P4-M5 entry scoring remains not implemented
P4-M5 entry verdict remains not implemented
P4-M5 entry execution remains not implemented
API implementation remains not started
MCP implementation remains not started
Connector implementation remains not started
Agent auto-call remains not started
P4-M5 start remains not implemented
P4-M4.18 remains not started
P4-M5 remains not started
P4-M5.0 remains not started
v7 remains not started
productization remains not started
UI remains not started
Operator Console remains not started
no P4-M4.18
no P4-M5 implementation
no P4-M5.0
no API implementation
no MCP implementation
no Connector implementation
no Agent auto-call
no P4-M5 entry validation
no P4-M5 readiness validation
no P4-M5 readiness inference
no P4-M5 readiness scoring
no P4-M5 readiness verdict
no P4-M5 entry scoring
no P4-M5 entry verdict
no P4-M5 entry execution
no P4-M5 start
no roadmap alignment validation
no roadmap alignment scoring
no roadmap alignment verdict
no roadmap alignment routing
no roadmap alignment execution
no roadmap alignment record creation
no roadmap alignment storage
no roadmap alignment persistence
no roadmap alignment mutation
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
    "P4-M4-FC.6 P4-M4 Final Closure Roadmap Alignment Snapshot",
    "read-only",
    "definition-only",
    "p4-m4-final-closure-roadmap-alignment-snapshot-only",
    "roadmap-alignment-snapshot-only",
    "roadmap-alignment-non-validation-boundary-only",
    "roadmap-alignment-non-scoring-boundary-only",
    "roadmap-alignment-non-verdict-boundary-only",
    "roadmap-alignment-non-routing-boundary-only",
    "roadmap-alignment-non-execution-boundary-only",
    "roadmap-alignment-non-record-boundary-only",
    "roadmap-alignment-non-mutation-boundary-only",
    "p4-m5-readiness-audit-future-phase-only",
    "p4-m5-non-start-boundary-only",
    "declaration-only",
    "inspection-only",
    "P4-M4.x remains cross-project memory governance preparation",
    "P4-M5.x remains API / MCP / Connector readiness audit",
    "P4-M5.x is not API implementation",
    "P4-M5.x is not MCP implementation",
    "P4-M5.x is not Connector implementation",
    "P4-M5 phase transition requires explicit human confirmation",
    "P4-M5 readiness audit remains future-phase only",
    "P4-M5.0 remains not started",
    "no P4-M5.0",
    "no API implementation",
    "no MCP implementation",
    "no Connector implementation",
    "no Agent auto-call",
    "no validation",
    "no scoring",
    "no verdict",
    "no routing",
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
p4_m4_final_closure_roadmap_alignment_snapshot_only
roadmap_alignment_snapshot_only
roadmap_alignment_non_validation_boundary_only
roadmap_alignment_non_scoring_boundary_only
roadmap_alignment_non_verdict_boundary_only
roadmap_alignment_non_routing_boundary_only
roadmap_alignment_non_execution_boundary_only
roadmap_alignment_non_record_boundary_only
roadmap_alignment_non_mutation_boundary_only
p4_m5_readiness_audit_future_phase_only
p4_m5_non_start_boundary_only
declaration_only
inspection_only
p4_m4_fc_6_started
p4_m4_fc_6_definition_only
p4_m4_fc_6_roadmap_alignment_snapshot_only
p4_m4_cross_project_governance_preparation_position_confirmed
p4_m5_api_mcp_connector_readiness_audit_position_confirmed
p4_m5_readiness_audit_only_future_phase_confirmed
p4_m5_phase_transition_requires_human_confirmation
p4_m4_fc_5_final_closure_boundary_freeze_index_reference_defined
p4_m4_fc_4_final_closure_non_start_bridge_index_reference_defined
p4_m4_fc_3_final_closure_transition_readiness_non_start_index_reference_defined
p4_m4_fc_2_final_closure_operator_handoff_index_reference_defined
p4_m4_fc_1_final_closure_evidence_index_reference_defined
p4_m4_fc_0_final_closure_index_entry_planning_gate_reference_defined
p4_m4_17_terminal_closure_seal_reference_defined
p4_m4_static_definition_chain_closed_reference_defined
p4_m4_design_layer_terminally_sealed_reference_defined
p4_m4_final_closure_stack_static_reference_only
fc_0_through_fc_5_static_reference_layers_only
fc_0_through_fc_5_not_readiness_evidence
fc_0_through_fc_5_not_validation_evidence
fc_0_through_fc_5_not_scoring_evidence
fc_0_through_fc_5_not_verdict_evidence
fc_0_through_fc_5_not_routing_evidence
fc_0_through_fc_5_not_execution_evidence
api_mcp_connector_implementation_deferred
agent_auto_call_deferred
p4_m5_start_deferred
p4_m5_0_start_deferred
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
p4_m5_0_started
p4_m5_implementation_started
p4_m5_entry_validation_enabled
p4_m5_readiness_validation_enabled
p4_m5_readiness_inference_enabled
p4_m5_readiness_scoring_enabled
p4_m5_readiness_verdict_enabled
p4_m5_entry_scoring_enabled
p4_m5_entry_verdict_enabled
p4_m5_entry_execution_enabled
p4_m5_start_enabled
roadmap_alignment_validation_enabled
roadmap_alignment_scoring_enabled
roadmap_alignment_verdict_enabled
roadmap_alignment_routing_enabled
roadmap_alignment_execution_enabled
roadmap_alignment_record_creation_enabled
roadmap_alignment_storage_enabled
roadmap_alignment_persistence_enabled
roadmap_alignment_mutation_enabled
api_implementation_enabled
mcp_implementation_enabled
connector_implementation_enabled
agent_auto_call_enabled
api_enabled
mcp_enabled
connector_enabled
agent_call_enabled
readiness_validation_enabled
validation_enabled
scoring_enabled
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
}


def test_field_inventory_is_exact_and_ordered():
    fields = list_p4_m4_final_closure_roadmap_alignment_snapshot_fields()

    assert len(fields) == 23
    assert p4_m4_final_closure_roadmap_alignment_snapshot_field_ids() == FIELD_IDS
    assert tuple(field.field_order for field in fields) == tuple(range(1, 24))
    assert all(
        isinstance(field, P4M4FinalClosureRoadmapAlignmentSnapshotField)
        for field in fields
    )
    assert {
        field.name
        for field in dataclasses.fields(
            P4M4FinalClosureRoadmapAlignmentSnapshotField
        )
    } == DATACLASS_FIELDS


def test_boundary_phrase_inventory_is_required_contract():
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in BOUNDARY_PHRASE_LINES
        assert phrase in P4_M4_FINAL_CLOSURE_ROADMAP_ALIGNMENT_SNAPSHOT_BOUNDARY


def test_markdown_renders_static_boundary_and_field_ids():
    markdown = render_p4_m4_final_closure_roadmap_alignment_snapshot_markdown()

    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in markdown
    for field_id in FIELD_IDS:
        assert field_id in markdown
    assert "## Status Report" in markdown
    assert "## P4-M4 Final Closure Roadmap Alignment Snapshot Fields" in markdown
    assert "P4-M4-FC.6 P4-M4 Final Closure Roadmap Alignment Snapshot" in markdown


def test_report_has_required_true_false_status_flags():
    status = p4_m4_final_closure_roadmap_alignment_snapshot_report()

    assert status["phase"] == "P4-M4-FC.6"
    assert status["feature"] == "P4-M4 Final Closure Roadmap Alignment Snapshot"
    assert status["mode"] == "read-only"
    assert status["package_version"] == "6.16.0"
    assert status["p4_m4_final_closure_roadmap_alignment_snapshot_field_count"] == 23
    assert (
        status[
            "referenced_p4_m4_fc_5_final_closure_boundary_freeze_index_field_count"
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
    fields = p4_m4_final_closure_roadmap_alignment_snapshot_as_dicts()

    assert len(fields) == 23
    assert tuple(field["field_id"] for field in fields) == FIELD_IDS
    assert fields == p4_m4_final_closure_roadmap_alignment_snapshot_as_dicts()
    assert all(
        field["p4_m4_final_closure_roadmap_alignment_snapshot_category"]
        == "p4-m4-final-closure-roadmap-alignment-snapshot-category"
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
            "p4-m4-final-closure-roadmap-alignment-snapshot",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith(
        "# P4-M4-FC.6 P4-M4 Final Closure Roadmap Alignment Snapshot\n"
    )
    for phrase in OPERATOR_SMOKE_PHRASES:
        assert phrase in stdout
    assert not (tmp_path / ".local" / "subspace_memory").exists()


def test_operator_json_command_returns_required_report(tmp_path: Path):
    code, output, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "p4-m4-final-closure-roadmap-alignment-snapshot",
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
    assert (
        output["boundary"]
        == P4_M4_FINAL_CLOSURE_ROADMAP_ALIGNMENT_SNAPSHOT_BOUNDARY
    )
    assert tuple(field["field_id"] for field in output["fields"]) == FIELD_IDS
    status = output["status"]
    assert status["phase"] == "P4-M4-FC.6"
    assert status["feature"] == "P4-M4 Final Closure Roadmap Alignment Snapshot"
    assert status["mode"] == "read-only"
    for flag in EXPECTED_TRUE_STATUS_FLAGS:
        assert status[flag] is True
    for flag in EXPECTED_FALSE_STATUS_FLAGS:
        assert status[flag] is False
    assert not (tmp_path / ".local" / "subspace_memory").exists()


def test_parser_exposes_only_expected_memory_loop_command_surface():
    commands = _memory_loop_subcommands(build_parser())

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
    assert "p4-m4-final-closure-roadmap-alignment-snapshot" in commands


def test_pyproject_entry_points_do_not_productize_command():
    pyproject = tomllib.loads(Path("pyproject.toml").read_text())
    entry_points = pyproject["project"]["entry-points"]

    assert "p4-m4-final-closure-roadmap-alignment-snapshot" not in entry_points
    assert "p4-m4-final-closure-roadmap-alignment-snapshot" not in str(entry_points)
    assert pyproject["project"]["version"] == "6.16.0"


def test_static_doc_contains_required_boundaries_and_fields():
    project_root = Path(__file__).resolve().parents[1]
    doc_path = (
        project_root
        / "docs"
        / "CIVILIZATION_CORE_P4_M4_FC_6_FINAL_CLOSURE_ROADMAP_ALIGNMENT_SNAPSHOT.md"
    )
    doc = doc_path.read_text(encoding="utf-8")

    assert doc.startswith(
        "# P4-M4-FC.6 P4-M4 Final Closure Roadmap Alignment Snapshot\n"
    )
    for field_id in FIELD_IDS:
        assert field_id in doc
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in doc


def test_custom_field_rendering_remains_definition_only():
    field = P4M4FinalClosureRoadmapAlignmentSnapshotField(
        field_order=99,
        field_id="custom-final-closure-roadmap-alignment-snapshot",
        field_name="Custom Final Closure Roadmap Alignment Snapshot",
        field_purpose="custom read-only definition-only inspection-only field",
        p4_m4_final_closure_roadmap_alignment_snapshot_category=(
            "custom-final-closure-roadmap-alignment-snapshot-category"
        ),
        p4_m4_final_closure_roadmap_alignment_snapshot_semantics_disabled=(
            "no roadmap alignment validation semantics; no execution semantics; no mutation semantics"
        ),
    )

    markdown = render_p4_m4_final_closure_roadmap_alignment_snapshot_markdown(
        (field,)
    )

    assert "custom-final-closure-roadmap-alignment-snapshot" in markdown
    assert "no roadmap alignment validation semantics; no execution semantics" in markdown
    assert "P4-M4-FC.6 P4-M4 Final Closure Roadmap Alignment Snapshot" in markdown


def test_forbidden_stage_filenames_are_not_created():
    project_root = Path(__file__).resolve().parents[1]
    changed_names = (
        "src/hermes_memory_fabric/p4_m4_final_closure_roadmap_alignment_snapshot.py",
        "tests/test_p4_m4_final_closure_roadmap_alignment_snapshot.py",
        "docs/CIVILIZATION_CORE_P4_M4_FC_6_FINAL_CLOSURE_ROADMAP_ALIGNMENT_SNAPSHOT.md",
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
