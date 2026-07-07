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
from hermes_memory_fabric.p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract import (
    BOUNDARY_PHRASE_LINES,
    FALSE_STATUS_FLAGS,
    P4_M5_0_API_MCP_CONNECTOR_READINESS_AUDIT_BOUNDARY_CONTRACT_BOUNDARY,
    TRUE_STATUS_FLAGS,
    P4M50ApiMcpConnectorReadinessAuditBoundaryContractField,
    list_p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_fields,
    p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_as_dicts,
    p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_field_ids,
    p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_report,
    render_p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_markdown,
)


FIELD_IDS = (
    "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract-id",
    "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract-phase",
    "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract-mode",
    "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract-p4-m5-readiness-audit-position",
    "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract-api-readiness-audit-scope",
    "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract-mcp-readiness-audit-scope",
    "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract-connector-readiness-audit-scope",
    "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract-agent-auto-call-disabled",
    "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract-external-system-integration-disabled",
    "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract-readiness-validation-disabled",
    "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract-readiness-inference-disabled",
    "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract-readiness-scoring-disabled",
    "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract-readiness-verdict-disabled",
    "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract-routing-disabled",
    "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract-execution-disabled",
    "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract-record-storage-mutation-disabled",
    "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract-direct-prior-roadmap-alignment-snapshot-reference",
    "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract-inherited-prior-boundary-freeze-index-reference",
    "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract-inherited-prior-non-start-bridge-index-reference",
    "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract-inherited-prior-transition-readiness-non-start-index-reference",
    "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract-p4-m4-final-closure-stack-static-reference-only-confirmation",
    "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract-v7-productization-ui-operator-console-deferred",
    "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract-static-boundary-and-validation-inference-scoring-verdict-routing-execution-record-storage-mutation-semantics-disabled",
)

DATACLASS_FIELDS = {
    "field_order",
    "field_id",
    "field_name",
    "field_purpose",
    "p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_category",
    "p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_semantics_disabled",
}

REQUIRED_BOUNDARY_PHRASES = tuple(
    line
    for line in """
P4-M5.0
API / MCP / Connector Readiness Audit Boundary Contract
P4-M5.0 API / MCP / Connector Readiness Audit Boundary Contract
read-only
definition-only
p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract-only
readiness-audit-boundary-contract-only
readiness-audit-non-validation-boundary-only
readiness-audit-non-inference-boundary-only
readiness-audit-non-scoring-boundary-only
readiness-audit-non-verdict-boundary-only
readiness-audit-non-routing-boundary-only
readiness-audit-non-execution-boundary-only
readiness-audit-non-record-boundary-only
readiness-audit-non-storage-boundary-only
readiness-audit-non-mutation-boundary-only
api-mcp-connector-implementation-disabled
agent-auto-call-disabled
declaration-only
inspection-only
P4-M5.0 is the first P4-M5 boundary contract
P4-M5.0 is readiness audit boundary only
P4-M5.0 is not API implementation
P4-M5.0 is not MCP implementation
P4-M5.0 is not Connector implementation
P4-M5.0 is not Agent auto-call
P4-M5.0 is not external system integration
P4-M5.0 does not perform readiness validation
P4-M5.0 does not infer readiness
P4-M5.0 does not score readiness
P4-M5.0 does not produce readiness verdict
P4-M5.0 does not route implementation
P4-M5.0 does not execute
P4-M5.0 does not create readiness records
P4-M5.0 does not create storage
P4-M5.0 does not persist state
P4-M5.0 does not mutate memory
P4-M4.x remains cross-project memory governance preparation
P4-M5.x remains API / MCP / Connector readiness audit
API readiness audit scope is definition-only
MCP readiness audit scope is definition-only
Connector readiness audit scope is definition-only
API implementation remains not started
MCP implementation remains not started
Connector implementation remains not started
Agent auto-call remains not started
external system integration remains not started
readiness validation remains not implemented
readiness inference remains not implemented
readiness scoring remains not implemented
readiness verdict remains not implemented
routing remains not implemented
execution remains not implemented
record creation remains not implemented
storage remains not implemented
persistence remains not implemented
mutation remains not implemented
P4-M4-FC.6 P4-M4 Final Closure Roadmap Alignment Snapshot remains the direct prior roadmap alignment snapshot reference
P4-M4-FC.5 P4-M4 Final Closure Boundary Freeze Index remains the inherited prior final closure boundary freeze index reference
P4-M4-FC.4 P4-M4 Final Closure Non-Start Bridge Index remains the inherited prior final closure non-start bridge index reference
P4-M4-FC.3 P4-M4 Final Closure Transition Readiness Non-Start Index remains the inherited prior final closure transition readiness non-start index reference
P4-M4 final closure stack remains static reference-only
FC.0 through FC.6 remain static prior reference layers only
FC.0 through FC.6 are not readiness validation evidence
FC.0 through FC.6 are not readiness scoring evidence
FC.0 through FC.6 are not readiness verdict evidence
FC.0 through FC.6 are not routing evidence
FC.0 through FC.6 are not execution evidence
v7 remains not started
productization remains not started
UI remains not started
Operator Console remains not started
no API implementation
no MCP implementation
no Connector implementation
no Agent auto-call
no external system integration
no readiness validation
no readiness inference
no readiness scoring
no readiness verdict
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
no command execution
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
    "P4-M5.0 API / MCP / Connector Readiness Audit Boundary Contract",
    "read-only",
    "definition-only",
    "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract-only",
    "readiness-audit-boundary-contract-only",
    "readiness-audit-non-validation-boundary-only",
    "readiness-audit-non-inference-boundary-only",
    "readiness-audit-non-scoring-boundary-only",
    "readiness-audit-non-verdict-boundary-only",
    "readiness-audit-non-routing-boundary-only",
    "readiness-audit-non-execution-boundary-only",
    "readiness-audit-non-record-boundary-only",
    "readiness-audit-non-storage-boundary-only",
    "readiness-audit-non-mutation-boundary-only",
    "api-mcp-connector-implementation-disabled",
    "agent-auto-call-disabled",
    "declaration-only",
    "inspection-only",
    "P4-M5.0 is the first P4-M5 boundary contract",
    "P4-M5.0 is readiness audit boundary only",
    "P4-M5.0 is not API implementation",
    "P4-M5.0 is not MCP implementation",
    "P4-M5.0 is not Connector implementation",
    "P4-M5.0 is not Agent auto-call",
    "P4-M5.0 does not perform readiness validation",
    "P4-M5.0 does not infer readiness",
    "P4-M5.0 does not score readiness",
    "P4-M5.0 does not produce readiness verdict",
    "no API implementation",
    "no MCP implementation",
    "no Connector implementation",
    "no Agent auto-call",
    "no external system integration",
    "no readiness validation",
    "no readiness inference",
    "no readiness scoring",
    "no readiness verdict",
    "no validation",
    "no scoring",
    "no verdict",
    "no routing",
    "no execution",
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
p4_m5_0_boundary_contract_started
p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_only
readiness_audit_boundary_contract_only
readiness_audit_non_validation_boundary_only
readiness_audit_non_inference_boundary_only
readiness_audit_non_scoring_boundary_only
readiness_audit_non_verdict_boundary_only
readiness_audit_non_routing_boundary_only
readiness_audit_non_execution_boundary_only
readiness_audit_non_record_boundary_only
readiness_audit_non_storage_boundary_only
readiness_audit_non_mutation_boundary_only
api_mcp_connector_implementation_disabled
agent_auto_call_disabled
declaration_only
inspection_only
p4_m5_0_started_as_boundary_contract_only
p4_m5_readiness_audit_position_confirmed
p4_m5_0_first_p4_m5_boundary_contract
p4_m4_cross_project_governance_preparation_position_preserved
p4_m5_api_mcp_connector_readiness_audit_position_preserved
api_readiness_audit_scope_definition_only
mcp_readiness_audit_scope_definition_only
connector_readiness_audit_scope_definition_only
p4_m4_fc_6_roadmap_alignment_snapshot_reference_defined
p4_m4_fc_5_boundary_freeze_index_reference_defined
p4_m4_fc_4_non_start_bridge_index_reference_defined
p4_m4_fc_3_transition_readiness_non_start_index_reference_defined
p4_m4_final_closure_stack_static_reference_only
fc_0_through_fc_6_static_reference_layers_only
fc_0_through_fc_6_not_readiness_validation_evidence
fc_0_through_fc_6_not_readiness_scoring_evidence
fc_0_through_fc_6_not_readiness_verdict_evidence
fc_0_through_fc_6_not_routing_evidence
fc_0_through_fc_6_not_execution_evidence
api_implementation_deferred
mcp_implementation_deferred
connector_implementation_deferred
agent_auto_call_deferred
external_system_integration_deferred
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
readiness_validation_enabled
readiness_inference_enabled
readiness_scoring_enabled
readiness_verdict_enabled
readiness_routing_enabled
readiness_execution_enabled
readiness_record_creation_enabled
readiness_storage_enabled
readiness_persistence_enabled
readiness_mutation_enabled
api_implementation_enabled
mcp_implementation_enabled
connector_implementation_enabled
agent_auto_call_enabled
external_system_integration_enabled
api_enabled
mcp_enabled
connector_enabled
agent_call_enabled
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
    "p4-m5-3-connector-readiness-audit-surface-map",
    "p4-m5-4-cross-surface-alignment-map",
    "p4-m5-5-readiness-audit-closure-non-start-boundary-seal",
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index",
    "p4-m6-0-next-corridor-entry-boundary-contract",
    "p4-m6-1-entry-preconditions-definition-surface",
    "p4-m6-2-entry-acceptance-non-evidence-surface",
    "p4-m6-3-entry-deferral-non-execution-surface",
}


def test_field_inventory_is_exact_and_ordered():
    fields = (
        list_p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_fields()
    )

    assert len(fields) == 23
    assert (
        p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_field_ids()
        == FIELD_IDS
    )
    assert tuple(field.field_order for field in fields) == tuple(range(1, 24))
    assert all(
        isinstance(
            field,
            P4M50ApiMcpConnectorReadinessAuditBoundaryContractField,
        )
        for field in fields
    )
    assert {
        field.name
        for field in dataclasses.fields(
            P4M50ApiMcpConnectorReadinessAuditBoundaryContractField
        )
    } == DATACLASS_FIELDS


def test_boundary_phrase_inventory_is_required_contract():
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in BOUNDARY_PHRASE_LINES
        assert (
            phrase
            in P4_M5_0_API_MCP_CONNECTOR_READINESS_AUDIT_BOUNDARY_CONTRACT_BOUNDARY
        )


def test_markdown_renders_static_boundary_and_field_ids():
    markdown = (
        render_p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_markdown()
    )

    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in markdown
    for field_id in FIELD_IDS:
        assert field_id in markdown
    assert "## Status Report" in markdown
    assert (
        "## P4-M5.0 API / MCP / Connector Readiness Audit Boundary Contract Fields"
        in markdown
    )
    assert "P4-M5.0 API / MCP / Connector Readiness Audit Boundary Contract" in markdown


def test_report_has_required_true_false_status_flags():
    status = p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_report()

    assert status["phase"] == "P4-M5.0"
    assert (
        status["feature"]
        == "API / MCP / Connector Readiness Audit Boundary Contract"
    )
    assert status["mode"] == "read-only"
    assert status["package_version"] == "6.16.0"
    assert (
        status[
            "p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_field_count"
        ]
        == 23
    )
    assert status["referenced_p4_m4_fc_6_roadmap_alignment_snapshot_field_count"] == 23
    assert TRUE_STATUS_FLAGS == EXPECTED_TRUE_STATUS_FLAGS
    assert FALSE_STATUS_FLAGS == EXPECTED_FALSE_STATUS_FLAGS
    for flag in EXPECTED_TRUE_STATUS_FLAGS:
        assert status[flag] is True
    for flag in EXPECTED_FALSE_STATUS_FLAGS:
        assert status[flag] is False


def test_as_dicts_is_deterministic_and_read_only_shape():
    fields = (
        p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_as_dicts()
    )

    assert len(fields) == 23
    assert tuple(field["field_id"] for field in fields) == FIELD_IDS
    assert (
        fields
        == p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_as_dicts()
    )
    assert all(
        field[
            "p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_category"
        ]
        == (
            "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract-category"
        )
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
            "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith(
        "# P4-M5.0 API / MCP / Connector Readiness Audit Boundary Contract\n"
    )
    for phrase in OPERATOR_SMOKE_PHRASES:
        assert phrase in stdout
    assert not (tmp_path / ".local" / "subspace_memory").exists()


def test_operator_json_command_returns_required_report(tmp_path: Path):
    code, output, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract",
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
        == P4_M5_0_API_MCP_CONNECTOR_READINESS_AUDIT_BOUNDARY_CONTRACT_BOUNDARY
    )
    assert tuple(field["field_id"] for field in output["fields"]) == FIELD_IDS
    status = output["status"]
    assert status["phase"] == "P4-M5.0"
    assert (
        status["feature"]
        == "API / MCP / Connector Readiness Audit Boundary Contract"
    )
    assert status["mode"] == "read-only"
    for flag in EXPECTED_TRUE_STATUS_FLAGS:
        assert status[flag] is True
    for flag in EXPECTED_FALSE_STATUS_FLAGS:
        assert status[flag] is False
    assert not (tmp_path / ".local" / "subspace_memory").exists()


def test_parser_exposes_only_expected_memory_loop_command_surface():
    commands = _memory_loop_subcommands(build_parser())

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
    assert (
        "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract"
        in commands
    )


def test_pyproject_entry_points_do_not_productize_command():
    pyproject = tomllib.loads(Path("pyproject.toml").read_text())
    entry_points = pyproject["project"]["entry-points"]

    assert (
        "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract"
        not in entry_points
    )
    assert (
        "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract"
        not in str(entry_points)
    )
    assert pyproject["project"]["version"] == "6.16.0"


def test_static_doc_contains_required_boundaries_and_fields():
    project_root = Path(__file__).resolve().parents[1]
    doc_path = (
        project_root
        / "docs"
        / "CIVILIZATION_CORE_P4_M5_0_API_MCP_CONNECTOR_READINESS_AUDIT_BOUNDARY_CONTRACT.md"
    )
    doc = doc_path.read_text(encoding="utf-8")

    assert doc.startswith(
        "# P4-M5.0 API / MCP / Connector Readiness Audit Boundary Contract\n"
    )
    for field_id in FIELD_IDS:
        assert field_id in doc
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in doc


def test_custom_field_rendering_remains_definition_only():
    field = P4M50ApiMcpConnectorReadinessAuditBoundaryContractField(
        field_order=99,
        field_id="custom-p4-m5-0-readiness-audit-boundary-contract",
        field_name="Custom P4-M5.0 Readiness Audit Boundary Contract",
        field_purpose="custom read-only definition-only inspection-only field",
        p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_category=(
            "custom-p4-m5-0-readiness-audit-boundary-contract-category"
        ),
        p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_semantics_disabled=(
            "no readiness validation semantics; no execution semantics; no mutation semantics"
        ),
    )

    markdown = (
        render_p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_markdown(
            (field,)
        )
    )

    assert "custom-p4-m5-0-readiness-audit-boundary-contract" in markdown
    assert "no readiness validation semantics; no execution semantics" in markdown
    assert "P4-M5.0 API / MCP / Connector Readiness Audit Boundary Contract" in markdown


def test_forbidden_implementation_files_are_not_created():
    project_root = Path(__file__).resolve().parents[1]

    forbidden_relative_paths = (
        "src/hermes_memory_fabric/p4_m5_api_client.py",
        "src/hermes_memory_fabric/p4_m5_mcp_client.py",
        "src/hermes_memory_fabric/p4_m5_connector.py",
        "src/hermes_memory_fabric/p4_m5_agent_call.py",
        "tests/test_p4_m5_api_client.py",
        "tests/test_p4_m5_mcp_client.py",
        "tests/test_p4_m5_connector.py",
        "tests/test_p4_m5_agent_call.py",
    )

    for relative_path in forbidden_relative_paths:
        assert not (project_root / relative_path).exists()


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
