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
from hermes_memory_fabric.p4_m6_5_entry_escalation_non_routing_surface import (
    BOUNDARY_PHRASE_LINES,
    FALSE_STATUS_FLAGS,
    P4_M6_5_ENTRY_ESCALATION_NON_ROUTING_SURFACE_BOUNDARY,
    TRUE_STATUS_FLAGS,
    P4M65EntryEscalationNonRoutingSurfaceField,
    list_p4_m6_5_entry_escalation_non_routing_surface_fields,
    p4_m6_5_entry_escalation_non_routing_surface_as_dicts,
    p4_m6_5_entry_escalation_non_routing_surface_field_ids,
    p4_m6_5_entry_escalation_non_routing_surface_report,
    render_p4_m6_5_entry_escalation_non_routing_surface_markdown,
)


FIELD_IDS = tuple(
    line
    for line in """
p4-m6-5-entry-escalation-non-routing-surface-id
p4-m6-5-entry-escalation-non-routing-surface-phase
p4-m6-5-entry-escalation-non-routing-surface-mode
p4-m6-5-entry-escalation-non-routing-surface-p4-m6-position
p4-m6-5-entry-escalation-non-routing-surface-direct-prior-p4-m6-4-entry-rejection-non-execution-surface-reference
p4-m6-5-entry-escalation-non-routing-surface-inherited-p4-m6-3-entry-deferral-non-execution-surface-reference
p4-m6-5-entry-escalation-non-routing-surface-inherited-p4-m6-2-entry-acceptance-non-evidence-surface-reference
p4-m6-5-entry-escalation-non-routing-surface-inherited-p4-m6-1-entry-preconditions-definition-surface-reference
p4-m6-5-entry-escalation-non-routing-surface-inherited-p4-m6-0-entry-boundary-contract-reference
p4-m6-5-entry-escalation-non-routing-surface-static-escalation-label-scope
p4-m6-5-entry-escalation-non-routing-surface-escalation-label-definition-surface
p4-m6-5-entry-escalation-non-routing-surface-escalation-non-routing-boundary
p4-m6-5-entry-escalation-non-routing-surface-escalation-non-notification-dispatch-assignment-boundary
p4-m6-5-entry-escalation-non-routing-surface-escalation-non-handoff-boundary
p4-m6-5-entry-escalation-non-routing-surface-escalation-non-approval-authorization-confirmation-boundary
p4-m6-5-entry-escalation-non-routing-surface-escalation-non-recommendation-execution-boundary
p4-m6-5-entry-escalation-non-routing-surface-escalation-non-readiness-validation-boundary
p4-m6-5-entry-escalation-non-routing-surface-escalation-non-readiness-evidence-boundary
p4-m6-5-entry-escalation-non-routing-surface-escalation-non-validation-inference-scoring-verdict-boundary
p4-m6-5-entry-escalation-non-routing-surface-escalation-non-record-storage-persistence-mutation-boundary
p4-m6-5-entry-escalation-non-routing-surface-implementation-corridor-v7-productization-ui-operator-console-deferred-boundary
p4-m6-5-entry-escalation-non-routing-surface-api-mcp-connector-agent-network-external-integration-non-start-boundary
p4-m6-5-entry-escalation-non-routing-surface-final-non-routing-definition-boundary
""".splitlines()
    if line
)

DATACLASS_FIELDS = {
    "field_order",
    "field_id",
    "field_name",
    "field_purpose",
    "p4_m6_5_entry_escalation_non_routing_surface_category",
    "p4_m6_5_entry_escalation_non_routing_surface_semantics_disabled",
}

REQUIRED_BOUNDARY_PHRASES = tuple(
    line
    for line in """
P4-M6.5
Entry Escalation Non-Routing Surface
P4-M6.5 Entry Escalation Non-Routing Surface
read-only
definition-only
p4-m6-5-entry-escalation-non-routing-surface-only
entry-escalation-non-routing-surface-only
static-escalation-labels-only
escalation-non-routing-surface-only
escalation-non-notification-surface-only
escalation-non-dispatch-surface-only
escalation-non-assignment-surface-only
escalation-non-handoff-surface-only
escalation-non-execution-surface-only
escalation-non-action-surface-only
escalation-non-approval-surface-only
escalation-non-authorization-surface-only
escalation-non-confirmation-surface-only
escalation-non-recommendation-surface-only
escalation-non-validation-surface-only
escalation-non-inference-surface-only
escalation-non-scoring-surface-only
escalation-non-verdict-surface-only
escalation-non-record-surface-only
escalation-non-storage-surface-only
escalation-non-persistence-surface-only
escalation-non-mutation-surface-only
implementation-corridor-not-started-boundary-only
api-implementation-disabled
mcp-implementation-disabled
connector-implementation-disabled
agent-auto-call-disabled
network-access-disabled
external-system-integration-disabled
declaration-only
inspection-only
P4-M6.5 defines only static entry escalation label surfaces
P4-M6.5 does not perform escalation
P4-M6.5 does not enforce escalation
P4-M6.5 does not notify anyone
P4-M6.5 does not dispatch anyone
P4-M6.5 does not assign anyone
P4-M6.5 does not hand off anything
P4-M6.5 does not create tickets
P4-M6.5 does not create issues
P4-M6.5 does not enqueue work
P4-M6.5 does not trigger workflow
P4-M6.5 does not approve entry
P4-M6.5 does not authorize entry
P4-M6.5 does not confirm entry
P4-M6.5 does not recommend entry
P4-M6.5 does not route implementation
P4-M6.5 does not execute
P4-M6.5 does not validate escalation
P4-M6.5 does not infer escalation
P4-M6.5 does not score escalation
P4-M6.5 does not produce escalation verdict
P4-M6.5 does not collect readiness evidence
P4-M6.5 does not classify readiness evidence
P4-M6.5 does not treat escalation as readiness evidence
P4-M6.5 does not treat escalation as validation input
P4-M6.5 does not create records
P4-M6.5 does not create storage
P4-M6.5 does not persist state
P4-M6.5 does not mutate memory
P4-M6.5 does not start implementation corridor
P4-M6.4 Entry Rejection Non-Execution Surface remains the direct prior entry rejection reference
P4-M6.3 Entry Deferral Non-Execution Surface remains an inherited entry deferral reference
P4-M6.2 Entry Acceptance Non-Evidence Surface remains an inherited entry acceptance reference
P4-M6.1 Entry Preconditions Definition Surface remains an inherited entry preconditions reference
P4-M6.0 Next Corridor Entry Boundary Contract remains an inherited entry boundary reference
static entry escalation labels are definition-only
escalation label definition surface is definition-only
entry escalation surfaces are not live escalation actions
entry escalation surfaces are not notification
entry escalation surfaces are not dispatch
entry escalation surfaces are not assignment
entry escalation surfaces are not handoff
entry escalation surfaces are not routing
entry escalation surfaces are not execution
implementation corridor remains not started
API implementation remains not started
MCP implementation remains not started
Connector implementation remains not started
Agent auto-call remains not started
external system integration remains not started
network access remains not started
no escalation validation
no escalation inference
no escalation scoring
no escalation verdict
no escalation action
no escalation enforcement
no notification
no dispatch
no assignment
no handoff
no tickets
no issues
no queue enqueue
no workflow trigger
no approval
no authorization
no confirmation
no recommendation
no routing
no execution
no readiness evidence
no validation inputs
no API implementation
no MCP implementation
no Connector implementation
no Agent auto-call
no external system integration
no network access
no record creation
no storage
no persistence
no mutation
no implementation start
no v7
no productization
no UI
no Operator Console
no version bump
no tag
""".splitlines()
    if line
)

OPERATOR_SMOKE_PHRASES = REQUIRED_BOUNDARY_PHRASES

EXPECTED_MEMORY_LOOP_COMMANDS = set(
    line
    for line in """
checklist
review-status
recall-verification-status
lifecycle-verification-status
do-not-retry-verification-status
source-provenance-verification-status
decision-readiness-status
manual-decision-preview
governance-pack-export
final-boundary-audit
manual-execution-hardening
execution-surface-contract
execution-contract-validation-matrix
manual-authorization-evidence-envelope
human-confirmation-snapshot-contract
execution-preconditions-snapshot-map
execution-risk-acknowledgement-map
execution-risk-acceptance-prohibition-map
execution-risk-waiver-prohibition-map
execution-decision-non-equivalence-map
execution-decision-recommendation-prohibition-map
execution-decision-default-denial-boundary-map
execution-decision-silence-non-consent-map
execution-decision-negative-evidence-non-override-map
execution-decision-conflicting-evidence-isolation-map
execution-decision-evidence-precedence-prohibition-map
final-non-execution-boundary-audit
p4-m2-closure-handoff-contract
governed-transition-intake-boundary-contract
governed-transition-intake-request-envelope-contract
governed-transition-intake-evidence-reference-envelope-contract
governed-transition-intake-declared-human-context-envelope-contract
governed-transition-intake-target-phase-envelope-contract
governed-transition-intake-declared-transition-reason-envelope-contract
governed-transition-intake-declared-transition-constraint-envelope-contract
governed-transition-intake-declared-transition-dependency-envelope-contract
governed-transition-intake-declared-transition-impact-envelope-contract
governed-transition-intake-declared-transition-risk-envelope-contract
governed-transition-intake-declared-transition-assumption-envelope-contract
governed-transition-intake-declared-transition-safeguard-envelope-contract
governed-transition-intake-package-assembly-envelope-contract
governed-transition-intake-final-non-validation-boundary-audit
governed-transition-intake-closure-handoff-contract
governed-transition-intake-phase-closure-review
governed-transition-intake-final-phase-handoff-summary
entry-gate-design-boundary-contract
entry-gate-design-request-envelope-contract
evidence-reference-envelope-contract
declared-human-context-envelope-contract
target-phase-envelope-contract
declared-transition-reason-envelope-contract
declared-transition-constraint-envelope-contract
declared-transition-dependency-envelope-contract
declared-transition-impact-envelope-contract
declared-transition-risk-envelope-contract
declared-transition-assumption-envelope-contract
declared-transition-safeguard-envelope-contract
declared-transition-package-assembly-envelope-contract
entry-gate-design-final-non-validation-boundary-audit
entry-gate-design-closure-handoff-contract
entry-gate-design-phase-closure-review
entry-gate-design-final-phase-handoff-summary
entry-gate-design-phase-terminal-closure-seal
p4-m4-final-closure-index-entry-planning-gate
p4-m4-final-closure-evidence-index
p4-m4-final-closure-operator-handoff-index
p4-m4-final-closure-transition-readiness-non-start-index
p4-m4-final-closure-non-start-bridge-index
p4-m4-final-closure-boundary-freeze-index
p4-m4-final-closure-roadmap-alignment-snapshot
p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract
p4-m5-1-api-readiness-audit-surface-map
p4-m5-2-mcp-readiness-audit-surface-map
p4-m5-3-connector-readiness-audit-surface-map
p4-m5-4-cross-surface-alignment-map
p4-m5-5-readiness-audit-closure-non-start-boundary-seal
p4-m5-6-final-closure-handoff-next-corridor-non-start-index
p4-m6-0-next-corridor-entry-boundary-contract
p4-m6-1-entry-preconditions-definition-surface
p4-m6-2-entry-acceptance-non-evidence-surface
p4-m6-3-entry-deferral-non-execution-surface
p4-m6-4-entry-rejection-non-execution-surface
p4-m6-5-entry-escalation-non-routing-surface
p4-m6-6-entry-exception-non-override-surface
p4-m6-7-entry-conflict-non-resolution-surface
p4-m6-8-entry-ambiguity-non-inference-surface
""".splitlines()
    if line
)


def test_field_inventory_is_exact_and_ordered():
    fields = list_p4_m6_5_entry_escalation_non_routing_surface_fields()

    assert len(fields) == 23
    assert p4_m6_5_entry_escalation_non_routing_surface_field_ids() == FIELD_IDS
    assert tuple(field.field_order for field in fields) == tuple(range(1, 24))
    assert all(
        isinstance(field, P4M65EntryEscalationNonRoutingSurfaceField)
        for field in fields
    )
    assert {
        field.name
        for field in dataclasses.fields(P4M65EntryEscalationNonRoutingSurfaceField)
    } == DATACLASS_FIELDS


def test_boundary_phrase_inventory_is_required_contract():
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in BOUNDARY_PHRASE_LINES
        assert phrase in P4_M6_5_ENTRY_ESCALATION_NON_ROUTING_SURFACE_BOUNDARY


def test_markdown_renders_static_boundary_and_field_ids():
    markdown = render_p4_m6_5_entry_escalation_non_routing_surface_markdown()

    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in markdown
    for field_id in FIELD_IDS:
        assert field_id in markdown
    assert "## Status Report" in markdown
    assert "## P4-M6.5 Entry Escalation Non-Routing Surface Fields" in markdown
    assert "P4-M6.5 Entry Escalation Non-Routing Surface" in markdown


def test_report_has_exact_true_false_status_flags():
    status = p4_m6_5_entry_escalation_non_routing_surface_report()

    assert status["phase"] == "P4-M6.5"
    assert status["feature"] == "Entry Escalation Non-Routing Surface"
    assert status["mode"] == "read-only"
    assert status["package_version"] == "6.16.0"
    assert status["p4_m6_5_entry_escalation_non_routing_surface_field_count"] == 23
    assert (
        status["referenced_p4_m6_4_entry_rejection_non_execution_surface_field_count"]
        == 23
    )
    assert (
        status["referenced_p4_m6_3_entry_deferral_non_execution_surface_field_count"]
        == 23
    )
    assert (
        status["referenced_p4_m6_2_entry_acceptance_non_evidence_surface_field_count"]
        == 23
    )
    assert (
        status[
            "referenced_p4_m6_1_entry_preconditions_definition_surface_field_count"
        ]
        == 23
    )
    assert (
        status["referenced_p4_m6_0_next_corridor_entry_boundary_contract_field_count"]
        == 23
    )
    assert (
        status[
            "referenced_p4_m5_6_final_closure_handoff_next_corridor_non_start_index_field_count"
        ]
        == 23
    )
    assert (
        status[
            "referenced_p4_m5_5_readiness_audit_closure_non_start_boundary_seal_field_count"
        ]
        == 23
    )
    assert status["referenced_p4_m5_4_cross_surface_alignment_map_field_count"] == 23
    assert len(TRUE_STATUS_FLAGS) == 121
    assert len(FALSE_STATUS_FLAGS) == 186
    actual_true_keys = {key for key, value in status.items() if value is True}
    actual_false_keys = {key for key, value in status.items() if value is False}
    assert actual_true_keys == set(TRUE_STATUS_FLAGS)
    assert actual_false_keys == set(FALSE_STATUS_FLAGS)


def test_as_dicts_is_deterministic_and_read_only_shape():
    fields = p4_m6_5_entry_escalation_non_routing_surface_as_dicts()

    assert len(fields) == 23
    assert tuple(field["field_id"] for field in fields) == FIELD_IDS
    assert fields == p4_m6_5_entry_escalation_non_routing_surface_as_dicts()
    assert all(
        field["p4_m6_5_entry_escalation_non_routing_surface_category"]
        == "p4-m6-5-entry-escalation-non-routing-surface-category"
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
            "p4-m6-5-entry-escalation-non-routing-surface",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M6.5 Entry Escalation Non-Routing Surface\n")
    for phrase in OPERATOR_SMOKE_PHRASES:
        assert phrase in stdout
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in stdout
    assert not (tmp_path / ".local" / "subspace_memory").exists()


def test_operator_json_command_returns_required_report(tmp_path: Path):
    code, output, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "p4-m6-5-entry-escalation-non-routing-surface",
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
    assert output["true_flags"] == 121
    assert output["false_flags"] == 186
    assert output["boundary"] == P4_M6_5_ENTRY_ESCALATION_NON_ROUTING_SURFACE_BOUNDARY
    assert tuple(field["field_id"] for field in output["fields"]) == FIELD_IDS
    status = output["status"]
    assert status["phase"] == "P4-M6.5"
    assert status["feature"] == "Entry Escalation Non-Routing Surface"
    assert status["mode"] == "read-only"
    actual_true_keys = {key for key, value in status.items() if value is True}
    actual_false_keys = {key for key, value in status.items() if value is False}
    assert actual_true_keys == set(TRUE_STATUS_FLAGS)
    assert actual_false_keys == set(FALSE_STATUS_FLAGS)
    assert not (tmp_path / ".local" / "subspace_memory").exists()


def test_parser_exposes_only_expected_memory_loop_command_surface():
    commands = _memory_loop_subcommands(build_parser())

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
    assert "p4-m6-5-entry-escalation-non-routing-surface" in commands
    assert "p4-m6-4-entry-rejection-non-execution-surface" in commands
    assert "p4-m6-3-entry-deferral-non-execution-surface" in commands
    assert "p4-m6-2-entry-acceptance-non-evidence-surface" in commands
    assert "p4-m6-1-entry-preconditions-definition-surface" in commands
    assert "p4-m6-0-next-corridor-entry-boundary-contract" in commands
    assert "p4-m5-6-final-closure-handoff-next-corridor-non-start-index" in commands
    assert "p4-m5-5-readiness-audit-closure-non-start-boundary-seal" in commands
    assert "p4-m5-4-cross-surface-alignment-map" in commands
    assert "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract" in commands
    assert "p4-m5-1-api-readiness-audit-surface-map" in commands
    assert "p4-m5-2-mcp-readiness-audit-surface-map" in commands
    assert "p4-m5-3-connector-readiness-audit-surface-map" in commands


def test_pyproject_entry_points_do_not_productize_command():
    pyproject = tomllib.loads(Path("pyproject.toml").read_text())
    entry_points = pyproject["project"]["entry-points"]

    command = "p4-m6-5-entry-escalation-non-routing-surface"
    assert command not in entry_points
    assert command not in str(entry_points)
    assert pyproject["project"]["version"] == "6.16.0"


def test_static_doc_contains_required_boundaries_and_fields():
    project_root = Path(__file__).resolve().parents[1]
    doc_path = (
        project_root
        / "docs"
        / "CIVILIZATION_CORE_P4_M6_5_ENTRY_ESCALATION_NON_ROUTING_SURFACE.md"
    )
    doc = doc_path.read_text(encoding="utf-8")

    assert doc.startswith("# P4-M6.5 Entry Escalation Non-Routing Surface\n")
    for field_id in FIELD_IDS:
        assert field_id in doc
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in doc


def test_custom_field_rendering_remains_definition_only():
    field = P4M65EntryEscalationNonRoutingSurfaceField(
        field_order=99,
        field_id="custom-p4-m6-5-entry-escalation-non-routing-surface",
        field_name="Custom P4-M6.5 Entry Escalation Non-Routing Surface",
        field_purpose="custom read-only definition-only inspection-only field",
        p4_m6_5_entry_escalation_non_routing_surface_category=(
            "custom-p4-m6-5-entry-escalation-non-routing-surface-category"
        ),
        p4_m6_5_entry_escalation_non_routing_surface_semantics_disabled=(
            "no escalation validation semantics; no routing semantics"
        ),
    )

    markdown = render_p4_m6_5_entry_escalation_non_routing_surface_markdown((field,))

    assert "custom-p4-m6-5-entry-escalation-non-routing-surface" in markdown
    assert "no escalation validation semantics" in markdown
    assert "P4-M6.5 Entry Escalation Non-Routing Surface" in markdown


def test_forbidden_implementation_files_are_not_created():
    project_root = Path(__file__).resolve().parents[1]

    forbidden_patterns = (
        "src/hermes_memory_fabric/*api_client*",
        "src/hermes_memory_fabric/*mcp_client*",
        "src/hermes_memory_fabric/*mcp_server*",
        "src/hermes_memory_fabric/*mcp_transport*",
        "src/hermes_memory_fabric/*mcp_session*",
        "src/hermes_memory_fabric/*agent_call*",
        "src/hermes_memory_fabric/*connector_client*",
        "src/hermes_memory_fabric/*connector_adapter*",
        "src/hermes_memory_fabric/*connector_runtime*",
        "src/hermes_memory_fabric/*live_connector*",
        "tests/*api_client*",
        "tests/*mcp_client*",
        "tests/*mcp_server*",
        "tests/*mcp_transport*",
        "tests/*mcp_session*",
        "tests/*agent_call*",
        "tests/*connector_client*",
        "tests/*connector_adapter*",
        "tests/*connector_runtime*",
        "tests/*live_connector*",
    )

    for pattern in forbidden_patterns:
        assert not list(project_root.glob(pattern))


def _run_operator(args: list[str]) -> tuple[int, dict[str, object], str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    code = run_operator_command(args, stdout=stdout, stderr=stderr)
    stdout_text = stdout.getvalue()
    payload = json.loads(stdout_text) if stdout_text.startswith("{") else {}
    return code, payload, stderr.getvalue(), stdout_text


def _memory_loop_subcommands(parser: argparse.ArgumentParser) -> set[str]:
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            memory_loop_parser = action.choices["memory-loop"]
            break
    else:  # pragma: no cover - parser structure regression guard
        raise AssertionError("memory-loop parser is missing")

    for action in memory_loop_parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            return set(action.choices)

    raise AssertionError("memory-loop subparser choices are missing")
