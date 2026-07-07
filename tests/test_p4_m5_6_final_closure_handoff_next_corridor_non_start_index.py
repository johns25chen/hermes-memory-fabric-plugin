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
from hermes_memory_fabric.p4_m5_6_final_closure_handoff_next_corridor_non_start_index import (
    BOUNDARY_PHRASE_LINES,
    FALSE_STATUS_FLAGS,
    P4_M5_6_FINAL_CLOSURE_HANDOFF_NEXT_CORRIDOR_NON_START_INDEX_BOUNDARY,
    TRUE_STATUS_FLAGS,
    P4M56FinalClosureHandoffNextCorridorNonStartIndexField,
    list_p4_m5_6_final_closure_handoff_next_corridor_non_start_index_fields,
    p4_m5_6_final_closure_handoff_next_corridor_non_start_index_as_dicts,
    p4_m5_6_final_closure_handoff_next_corridor_non_start_index_field_ids,
    p4_m5_6_final_closure_handoff_next_corridor_non_start_index_report,
    render_p4_m5_6_final_closure_handoff_next_corridor_non_start_index_markdown,
)


FIELD_IDS = (
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index-id",
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index-phase",
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index-mode",
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index-p4-m5-readiness-audit-position",
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index-direct-prior-readiness-audit-closure-non-start-boundary-seal-reference",
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index-inherited-prior-api-mcp-connector-readiness-audit-definition-corridor-reference",
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index-p4-m5-0-boundary-contract-final-handoff-surface",
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index-p4-m5-1-api-surface-map-final-handoff-surface",
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index-p4-m5-2-mcp-surface-map-final-handoff-surface",
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index-p4-m5-3-connector-surface-map-final-handoff-surface",
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index-p4-m5-4-cross-surface-alignment-map-final-handoff-surface",
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index-p4-m5-5-readiness-audit-closure-seal-final-handoff-surface",
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index-api-mcp-connector-readiness-audit-corridor-final-closure-index",
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index-next-corridor-non-start-index",
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index-api-implementation-non-start-handoff-surface",
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index-mcp-implementation-non-start-handoff-surface",
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index-connector-implementation-non-start-handoff-surface",
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index-agent-auto-call-external-integration-non-start-handoff-surface",
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index-readiness-validation-inference-scoring-verdict-non-start-handoff-surface",
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index-readiness-routing-execution-record-storage-persistence-mutation-non-start-handoff-surface",
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index-next-corridor-entry-preconditions-deferred-surface",
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index-v7-productization-ui-operator-console-deferred",
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index-static-final-closure-handoff-and-validation-inference-scoring-verdict-routing-execution-record-storage-mutation-semantics-disabled",
)

DATACLASS_FIELDS = {
    "field_order",
    "field_id",
    "field_name",
    "field_purpose",
    "p4_m5_6_final_closure_handoff_next_corridor_non_start_index_category",
    "p4_m5_6_final_closure_handoff_next_corridor_non_start_index_semantics_disabled",
}

REQUIRED_BOUNDARY_PHRASES = tuple(
    line
    for line in """
P4-M5.6
Final Closure Handoff / Next Corridor Non-Start Index
P4-M5.6 Final Closure Handoff / Next Corridor Non-Start Index
read-only
definition-only
p4-m5-6-final-closure-handoff-next-corridor-non-start-index-only
api-mcp-connector-readiness-audit-corridor-final-closure-only
next-corridor-non-start-index-only
final-closure-handoff-non-validation-boundary-only
final-closure-handoff-non-inference-boundary-only
final-closure-handoff-non-scoring-boundary-only
final-closure-handoff-non-verdict-boundary-only
final-closure-handoff-non-routing-boundary-only
final-closure-handoff-non-execution-boundary-only
final-closure-handoff-non-record-boundary-only
final-closure-handoff-non-storage-boundary-only
final-closure-handoff-non-mutation-boundary-only
api-implementation-disabled
mcp-implementation-disabled
connector-implementation-disabled
agent-auto-call-disabled
network-access-disabled
external-system-integration-disabled
declaration-only
inspection-only
P4-M5.6 finalizes the P4-M5.0 through P4-M5.5 readiness audit definition corridor only
P4-M5.6 declares the next corridor not started
P4-M5.6 is not API implementation
P4-M5.6 is not MCP implementation
P4-M5.6 is not Connector implementation
P4-M5.6 is not API client implementation
P4-M5.6 is not MCP client implementation
P4-M5.6 is not MCP server implementation
P4-M5.6 is not MCP transport implementation
P4-M5.6 is not MCP session implementation
P4-M5.6 is not Connector client implementation
P4-M5.6 is not Connector adapter implementation
P4-M5.6 is not Connector runtime implementation
P4-M5.6 is not Agent auto-call
P4-M5.6 is not external system integration
P4-M5.6 is not network access
P4-M5.6 is not live API endpoint probing
P4-M5.6 is not live MCP server probing
P4-M5.6 is not live provider probing
P4-M5.6 is not live provider discovery
P4-M5.6 is not OAuth flow
P4-M5.6 is not credential use
P4-M5.6 is not secret access
P4-M5.6 is not secret inspection
P4-M5.6 is not API call
P4-M5.6 is not MCP tool call
P4-M5.6 is not MCP resource access
P4-M5.6 is not MCP prompt execution
P4-M5.6 is not connector data fetch
P4-M5.6 is not connector data write
P4-M5.6 is not connector mutation
P4-M5.6 is not authentication testing
P4-M5.6 is not authorization testing
P4-M5.6 is not schema validation
P4-M5.6 does not perform readiness validation
P4-M5.6 does not infer readiness
P4-M5.6 does not score readiness
P4-M5.6 does not produce readiness verdict
P4-M5.6 does not route implementation
P4-M5.6 does not execute
P4-M5.6 does not create readiness records
P4-M5.6 does not create storage
P4-M5.6 does not persist state
P4-M5.6 does not mutate memory
P4-M5.6 does not start the next corridor
P4-M5.5 Readiness Audit Closure / Non-Start Boundary Seal remains the direct prior closure seal reference
P4-M5.4 API / MCP / Connector Cross-Surface Alignment Map remains an inherited cross-surface alignment map reference
P4-M5.3 Connector Readiness Audit Surface Map remains an inherited Connector surface map reference
P4-M5.2 MCP Readiness Audit Surface Map remains an inherited MCP surface map reference
P4-M5.1 API Readiness Audit Surface Map remains an inherited API surface map reference
P4-M5.0 API / MCP / Connector Readiness Audit Boundary Contract remains the inherited prior boundary contract reference
P4-M5.0 boundary contract final handoff surface is definition-only
P4-M5.1 API surface map final handoff surface is definition-only
P4-M5.2 MCP surface map final handoff surface is definition-only
P4-M5.3 Connector surface map final handoff surface is definition-only
P4-M5.4 cross-surface alignment map final handoff surface is definition-only
P4-M5.5 readiness audit closure seal final handoff surface is definition-only
API / MCP / Connector readiness audit corridor final closure index is definition-only
next corridor non-start index is definition-only
API implementation non-start handoff surface is definition-only
MCP implementation non-start handoff surface is definition-only
Connector implementation non-start handoff surface is definition-only
Agent auto-call external integration non-start handoff surface is definition-only
readiness validation inference scoring verdict non-start handoff surface is definition-only
readiness routing execution record storage persistence mutation non-start handoff surface is definition-only
next corridor entry preconditions deferred surface is definition-only
Final closure handoff surfaces are not readiness evidence
Final closure handoff surfaces are not validation inputs
Final closure handoff surfaces are not next corridor start
API implementation remains not started
MCP implementation remains not started
Connector implementation remains not started
Agent auto-call remains not started
external system integration remains not started
network access remains not started
live API endpoint probing remains not started
live MCP server probing remains not started
live provider probing remains not started
live provider discovery remains not started
OAuth flow remains not started
credential use remains not started
secret access remains not started
secret inspection remains not started
API call remains not started
MCP tool call remains not started
MCP resource access remains not started
MCP prompt execution remains not started
connector data fetch remains not started
connector data write remains not started
connector mutation remains not started
authentication testing remains not started
authorization testing remains not started
schema validation remains not started
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
next corridor remains not started
v7 remains not started
productization remains not started
UI remains not started
Operator Console remains not started
no API implementation
no MCP implementation
no Connector implementation
no API client
no MCP client
no MCP server
no MCP transport
no MCP session
no Connector client
no Connector adapter
no Connector runtime
no Agent auto-call
no external system integration
no network access
no live API endpoint probing
no live MCP server probing
no live provider probing
no live provider discovery
no OAuth flow
no credential use
no secret access
no secret inspection
no API call
no MCP tool call
no MCP resource access
no MCP prompt execution
no connector data fetch
no connector data write
no connector mutation
no authentication testing
no authorization testing
no schema validation
no readiness validation
no readiness inference
no readiness scoring
no readiness verdict
no validation
no scoring
no verdict
no routing
no execution
no command execution
no record creation
no storage
no persistence
no mutation
no next corridor start
no v7
no productization
no UI
no Operator Console
no version bump
no tag
""".splitlines()
    if line
)

ALL_EXPECTED_TRUE_STATUS_KEYS = tuple(
    line
    for line in """
definition_only
p4_m5_6_final_closure_handoff_next_corridor_non_start_index_started
p4_m5_6_final_closure_handoff_next_corridor_non_start_index_only
api_mcp_connector_readiness_audit_corridor_final_closure_only
next_corridor_non_start_index_only
final_closure_handoff_non_validation_boundary_only
final_closure_handoff_non_inference_boundary_only
final_closure_handoff_non_scoring_boundary_only
final_closure_handoff_non_verdict_boundary_only
final_closure_handoff_non_routing_boundary_only
final_closure_handoff_non_execution_boundary_only
final_closure_handoff_non_record_boundary_only
final_closure_handoff_non_storage_boundary_only
final_closure_handoff_non_mutation_boundary_only
api_implementation_disabled
mcp_implementation_disabled
connector_implementation_disabled
agent_auto_call_disabled
network_access_disabled
external_system_integration_disabled
declaration_only
inspection_only
p4_m5_6_started_as_final_closure_handoff_only
p4_m5_readiness_audit_position_preserved
p4_m5_5_closure_seal_reference_defined
p4_m5_4_cross_surface_alignment_map_reference_defined
p4_m5_3_connector_surface_map_reference_defined
p4_m5_2_mcp_surface_map_reference_defined
p4_m5_1_api_surface_map_reference_defined
p4_m5_0_boundary_contract_reference_defined
p4_m5_0_boundary_contract_final_handoff_surface_defined
p4_m5_1_api_surface_map_final_handoff_surface_defined
p4_m5_2_mcp_surface_map_final_handoff_surface_defined
p4_m5_3_connector_surface_map_final_handoff_surface_defined
p4_m5_4_cross_surface_alignment_map_final_handoff_surface_defined
p4_m5_5_readiness_audit_closure_seal_final_handoff_surface_defined
readiness_audit_corridor_final_closure_index_defined
next_corridor_non_start_index_defined
api_implementation_non_start_handoff_surface_defined
mcp_implementation_non_start_handoff_surface_defined
connector_implementation_non_start_handoff_surface_defined
agent_auto_call_external_integration_non_start_handoff_surface_defined
readiness_validation_inference_scoring_verdict_non_start_handoff_surface_defined
readiness_routing_execution_record_storage_persistence_mutation_non_start_handoff_surface_defined
next_corridor_entry_preconditions_deferred_surface_defined
p4_m5_final_closure_surfaces_are_definition_only
p4_m5_final_closure_surfaces_are_not_readiness_evidence
p4_m5_final_closure_surfaces_are_not_validation_inputs
p4_m5_final_closure_surfaces_are_not_next_corridor_start
p4_m5_corridor_closed_as_definition_only
next_corridor_start_deferred
api_surface_handoff_reference_only
mcp_surface_handoff_reference_only
connector_surface_handoff_reference_only
cross_surface_alignment_handoff_reference_only
closure_seal_handoff_reference_only
api_implementation_deferred
mcp_implementation_deferred
connector_implementation_deferred
agent_auto_call_deferred
readiness_validation_deferred
readiness_inference_deferred
readiness_scoring_deferred
readiness_verdict_deferred
readiness_routing_deferred
readiness_execution_deferred
readiness_record_creation_deferred
readiness_storage_deferred
readiness_persistence_deferred
readiness_mutation_deferred
v7_start_deferred
productization_deferred
ui_deferred
operator_console_deferred
""".splitlines()
    if line
)

ALL_EXPECTED_FALSE_STATUS_KEYS = tuple(
    line
    for line in """
live_validation_enabled
final_closure_handoff_validation_enabled
final_closure_handoff_inference_enabled
final_closure_handoff_scoring_enabled
final_closure_handoff_verdict_enabled
final_closure_handoff_routing_enabled
final_closure_handoff_execution_enabled
final_closure_handoff_record_creation_enabled
final_closure_handoff_storage_enabled
final_closure_handoff_mutation_enabled
next_corridor_started
next_corridor_entry_enabled
next_corridor_preconditions_enabled
api_enabled
api_implementation_enabled
api_client_enabled
api_call_enabled
api_endpoint_probe_enabled
api_schema_validation_enabled
mcp_enabled
mcp_implementation_enabled
mcp_client_enabled
mcp_server_enabled
mcp_transport_enabled
mcp_session_enabled
mcp_tool_call_enabled
mcp_resource_access_enabled
mcp_prompt_execution_enabled
mcp_live_server_probe_enabled
connector_enabled
connector_implementation_enabled
connector_client_enabled
connector_adapter_enabled
connector_runtime_enabled
connector_live_connection_enabled
connector_oauth_flow_enabled
connector_secret_access_enabled
connector_secret_inspection_enabled
connector_data_fetch_enabled
connector_data_write_enabled
connector_mutation_enabled
connector_permission_validation_enabled
connector_access_validation_enabled
connector_authentication_test_enabled
connector_authorization_test_enabled
connector_schema_validation_enabled
network_access_enabled
live_provider_probe_enabled
live_provider_discovery_enabled
authentication_testing_enabled
authorization_testing_enabled
schema_validation_enabled
agent_auto_call_enabled
agent_call_enabled
external_system_integration_enabled
validation_enabled
scoring_enabled
verdict_generation_enabled
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
closure_validation_enabled
closure_inference_enabled
closure_scoring_enabled
closure_verdict_enabled
closure_routing_enabled
closure_execution_enabled
closure_record_creation_enabled
closure_storage_enabled
closure_mutation_enabled
handoff_validation_enabled
handoff_inference_enabled
handoff_scoring_enabled
handoff_verdict_enabled
handoff_routing_enabled
handoff_execution_enabled
handoff_record_creation_enabled
handoff_storage_enabled
handoff_mutation_enabled
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

OPERATOR_SMOKE_PHRASES = (
    "P4-M5.6 Final Closure Handoff / Next Corridor Non-Start Index",
    "read-only",
    "definition-only",
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index-only",
    "api-mcp-connector-readiness-audit-corridor-final-closure-only",
    "next-corridor-non-start-index-only",
    "final-closure-handoff-non-validation-boundary-only",
    "final-closure-handoff-non-inference-boundary-only",
    "final-closure-handoff-non-scoring-boundary-only",
    "final-closure-handoff-non-verdict-boundary-only",
    "final-closure-handoff-non-routing-boundary-only",
    "final-closure-handoff-non-execution-boundary-only",
    "final-closure-handoff-non-record-boundary-only",
    "final-closure-handoff-non-storage-boundary-only",
    "final-closure-handoff-non-mutation-boundary-only",
    "api-implementation-disabled",
    "mcp-implementation-disabled",
    "connector-implementation-disabled",
    "agent-auto-call-disabled",
    "network-access-disabled",
    "external-system-integration-disabled",
    "declaration-only",
    "inspection-only",
    "P4-M5.6 finalizes the P4-M5.0 through P4-M5.5 readiness audit definition corridor only",
    "P4-M5.6 declares the next corridor not started",
    "P4-M5.6 is not API implementation",
    "P4-M5.6 is not MCP implementation",
    "P4-M5.6 is not Connector implementation",
    "P4-M5.6 is not network access",
    "P4-M5.6 does not perform readiness validation",
    "P4-M5.6 does not infer readiness",
    "P4-M5.6 does not score readiness",
    "P4-M5.6 does not produce readiness verdict",
    "P4-M5.6 does not start the next corridor",
    "no API implementation",
    "no MCP implementation",
    "no Connector implementation",
    "no Agent auto-call",
    "no external system integration",
    "no network access",
    "no readiness validation",
    "no readiness inference",
    "no readiness scoring",
    "no readiness verdict",
    "no routing",
    "no execution",
    "no storage",
    "no persistence",
    "no mutation",
    "no next corridor start",
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
}


def test_field_inventory_is_exact_and_ordered():
    fields = list_p4_m5_6_final_closure_handoff_next_corridor_non_start_index_fields()

    assert len(fields) == 23
    assert (
        p4_m5_6_final_closure_handoff_next_corridor_non_start_index_field_ids()
        == FIELD_IDS
    )
    assert tuple(field.field_order for field in fields) == tuple(range(1, 24))
    assert all(
        isinstance(
            field,
            P4M56FinalClosureHandoffNextCorridorNonStartIndexField,
        )
        for field in fields
    )
    assert {
        field.name
        for field in dataclasses.fields(
            P4M56FinalClosureHandoffNextCorridorNonStartIndexField
        )
    } == DATACLASS_FIELDS


def test_boundary_phrase_inventory_is_required_contract():
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in BOUNDARY_PHRASE_LINES
        assert (
            phrase
            in P4_M5_6_FINAL_CLOSURE_HANDOFF_NEXT_CORRIDOR_NON_START_INDEX_BOUNDARY
        )


def test_markdown_renders_static_boundary_and_field_ids():
    markdown = (
        render_p4_m5_6_final_closure_handoff_next_corridor_non_start_index_markdown()
    )

    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in markdown
    for field_id in FIELD_IDS:
        assert field_id in markdown
    assert "## Status Report" in markdown
    assert (
        "## P4-M5.6 Final Closure Handoff / Next Corridor Non-Start Index Fields"
        in markdown
    )
    assert (
        "P4-M5.6 Final Closure Handoff / Next Corridor Non-Start Index"
        in markdown
    )


def test_report_has_required_true_false_status_flags():
    status = p4_m5_6_final_closure_handoff_next_corridor_non_start_index_report()

    assert status["phase"] == "P4-M5.6"
    assert (
        status["feature"]
        == "Final Closure Handoff / Next Corridor Non-Start Index"
    )
    assert status["mode"] == "read-only"
    assert status["package_version"] == "6.16.0"
    assert (
        status[
            "p4_m5_6_final_closure_handoff_next_corridor_non_start_index_field_count"
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
    assert (
        status[
            "referenced_p4_m5_3_connector_readiness_audit_surface_map_field_count"
        ]
        == 23
    )
    assert (
        status["referenced_p4_m5_2_mcp_readiness_audit_surface_map_field_count"]
        == 23
    )
    assert status["referenced_p4_m5_1_api_readiness_audit_surface_map_field_count"] == 23
    assert (
        status[
            "referenced_p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_field_count"
        ]
        == 23
    )
    assert TRUE_STATUS_FLAGS == ALL_EXPECTED_TRUE_STATUS_KEYS
    assert FALSE_STATUS_FLAGS == ALL_EXPECTED_FALSE_STATUS_KEYS
    assert len(TRUE_STATUS_FLAGS) == 74
    assert len(FALSE_STATUS_FLAGS) == 110
    for flag in ALL_EXPECTED_TRUE_STATUS_KEYS:
        assert status[flag] is True
    for flag in ALL_EXPECTED_FALSE_STATUS_KEYS:
        assert status[flag] is False


def test_as_dicts_is_deterministic_and_read_only_shape():
    fields = p4_m5_6_final_closure_handoff_next_corridor_non_start_index_as_dicts()

    assert len(fields) == 23
    assert tuple(field["field_id"] for field in fields) == FIELD_IDS
    assert (
        fields
        == p4_m5_6_final_closure_handoff_next_corridor_non_start_index_as_dicts()
    )
    assert all(
        field[
            "p4_m5_6_final_closure_handoff_next_corridor_non_start_index_category"
        ]
        == "p4-m5-6-final-closure-handoff-next-corridor-non-start-index-category"
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
            "p4-m5-6-final-closure-handoff-next-corridor-non-start-index",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith(
        "# P4-M5.6 Final Closure Handoff / Next Corridor Non-Start Index\n"
    )
    for phrase in OPERATOR_SMOKE_PHRASES:
        assert phrase in stdout
    assert not (tmp_path / ".local" / "subspace_memory").exists()


def test_operator_json_command_returns_required_report(tmp_path: Path):
    code, output, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "p4-m5-6-final-closure-handoff-next-corridor-non-start-index",
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
    assert output["true_flags"] == 74
    assert output["false_flags"] == 110
    assert (
        output["boundary"]
        == P4_M5_6_FINAL_CLOSURE_HANDOFF_NEXT_CORRIDOR_NON_START_INDEX_BOUNDARY
    )
    assert tuple(field["field_id"] for field in output["fields"]) == FIELD_IDS
    status = output["status"]
    assert status["phase"] == "P4-M5.6"
    assert (
        status["feature"]
        == "Final Closure Handoff / Next Corridor Non-Start Index"
    )
    assert status["mode"] == "read-only"
    for flag in ALL_EXPECTED_TRUE_STATUS_KEYS:
        assert status[flag] is True
    for flag in ALL_EXPECTED_FALSE_STATUS_KEYS:
        assert status[flag] is False
    assert not (tmp_path / ".local" / "subspace_memory").exists()


def test_parser_exposes_only_expected_memory_loop_command_surface():
    commands = _memory_loop_subcommands(build_parser())

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
    assert (
        "p4-m5-6-final-closure-handoff-next-corridor-non-start-index"
        in commands
    )
    assert (
        "p4-m5-5-readiness-audit-closure-non-start-boundary-seal"
        in commands
    )
    assert "p4-m5-4-cross-surface-alignment-map" in commands
    assert "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract" in commands
    assert "p4-m5-1-api-readiness-audit-surface-map" in commands
    assert "p4-m5-2-mcp-readiness-audit-surface-map" in commands
    assert "p4-m5-3-connector-readiness-audit-surface-map" in commands


def test_pyproject_entry_points_do_not_productize_command():
    pyproject = tomllib.loads(Path("pyproject.toml").read_text())
    entry_points = pyproject["project"]["entry-points"]

    command = "p4-m5-6-final-closure-handoff-next-corridor-non-start-index"
    assert command not in entry_points
    assert command not in str(entry_points)
    assert pyproject["project"]["version"] == "6.16.0"


def test_static_doc_contains_required_boundaries_and_fields():
    project_root = Path(__file__).resolve().parents[1]
    doc_path = (
        project_root
        / "docs"
        / "CIVILIZATION_CORE_P4_M5_6_FINAL_CLOSURE_HANDOFF_NEXT_CORRIDOR_NON_START_INDEX.md"
    )
    doc = doc_path.read_text(encoding="utf-8")

    assert doc.startswith(
        "# P4-M5.6 Final Closure Handoff / Next Corridor Non-Start Index\n"
    )
    for field_id in FIELD_IDS:
        assert field_id in doc
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in doc


def test_custom_field_rendering_remains_definition_only():
    field = P4M56FinalClosureHandoffNextCorridorNonStartIndexField(
        field_order=99,
        field_id=(
            "custom-p4-m5-6-final-closure-handoff-next-corridor-non-start-index"
        ),
        field_name="Custom P4-M5.6 Final Closure Handoff Index",
        field_purpose="custom read-only definition-only inspection-only field",
        p4_m5_6_final_closure_handoff_next_corridor_non_start_index_category=(
            "custom-p4-m5-6-final-closure-handoff-next-corridor-non-start-index-category"
        ),
        p4_m5_6_final_closure_handoff_next_corridor_non_start_index_semantics_disabled=(
            "no API client semantics; no MCP client semantics; "
            "no Connector runtime semantics"
        ),
    )

    markdown = (
        render_p4_m5_6_final_closure_handoff_next_corridor_non_start_index_markdown(
            (field,)
        )
    )

    assert (
        "custom-p4-m5-6-final-closure-handoff-next-corridor-non-start-index"
        in markdown
    )
    assert "no API client semantics; no MCP client semantics" in markdown
    assert (
        "P4-M5.6 Final Closure Handoff / Next Corridor Non-Start Index"
        in markdown
    )


def test_forbidden_implementation_files_are_not_created():
    project_root = Path(__file__).resolve().parents[1]

    forbidden_relative_paths = (
        "src/hermes_memory_fabric/p4_m5_api_client.py",
        "src/hermes_memory_fabric/p4_m5_mcp_client.py",
        "src/hermes_memory_fabric/p4_m5_mcp_server.py",
        "src/hermes_memory_fabric/p4_m5_mcp_transport.py",
        "src/hermes_memory_fabric/p4_m5_mcp_session.py",
        "src/hermes_memory_fabric/p4_m5_connector.py",
        "src/hermes_memory_fabric/p4_m5_connector_client.py",
        "src/hermes_memory_fabric/p4_m5_connector_adapter.py",
        "src/hermes_memory_fabric/p4_m5_connector_runtime.py",
        "src/hermes_memory_fabric/p4_m5_agent_call.py",
        "tests/test_p4_m5_api_client.py",
        "tests/test_p4_m5_mcp_client.py",
        "tests/test_p4_m5_mcp_server.py",
        "tests/test_p4_m5_mcp_transport.py",
        "tests/test_p4_m5_mcp_session.py",
        "tests/test_p4_m5_connector.py",
        "tests/test_p4_m5_connector_client.py",
        "tests/test_p4_m5_connector_adapter.py",
        "tests/test_p4_m5_connector_runtime.py",
        "tests/test_p4_m5_agent_call.py",
    )

    for relative_path in forbidden_relative_paths:
        assert not (project_root / relative_path).exists()


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
