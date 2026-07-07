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
from hermes_memory_fabric.p4_m6_2_entry_acceptance_non_evidence_surface import (
    BOUNDARY_PHRASE_LINES,
    FALSE_STATUS_FLAGS,
    P4_M6_2_ENTRY_ACCEPTANCE_NON_EVIDENCE_SURFACE_BOUNDARY,
    SUPPLEMENTAL_TRUE_STATUS_FLAGS,
    TRUE_STATUS_FLAGS,
    P4M62EntryAcceptanceNonEvidenceSurfaceField,
    list_p4_m6_2_entry_acceptance_non_evidence_surface_fields,
    p4_m6_2_entry_acceptance_non_evidence_surface_as_dicts,
    p4_m6_2_entry_acceptance_non_evidence_surface_field_ids,
    p4_m6_2_entry_acceptance_non_evidence_surface_report,
    render_p4_m6_2_entry_acceptance_non_evidence_surface_markdown,
)


FIELD_IDS = tuple(
    line
    for line in """
p4-m6-2-entry-acceptance-non-evidence-surface-id
p4-m6-2-entry-acceptance-non-evidence-surface-phase
p4-m6-2-entry-acceptance-non-evidence-surface-mode
p4-m6-2-entry-acceptance-non-evidence-surface-p4-m6-position
p4-m6-2-entry-acceptance-non-evidence-surface-direct-prior-p4-m6-1-entry-preconditions-definition-surface-reference
p4-m6-2-entry-acceptance-non-evidence-surface-inherited-p4-m6-0-entry-boundary-contract-reference
p4-m6-2-entry-acceptance-non-evidence-surface-static-acceptance-label-scope
p4-m6-2-entry-acceptance-non-evidence-surface-acceptance-label-definition-surface
p4-m6-2-entry-acceptance-non-evidence-surface-acceptance-non-evidence-boundary
p4-m6-2-entry-acceptance-non-evidence-surface-acceptance-non-validation-input-boundary
p4-m6-2-entry-acceptance-non-evidence-surface-acceptance-non-authorization-boundary
p4-m6-2-entry-acceptance-non-evidence-surface-acceptance-non-confirmation-boundary
p4-m6-2-entry-acceptance-non-evidence-surface-acceptance-non-approval-boundary
p4-m6-2-entry-acceptance-non-evidence-surface-acceptance-non-recommendation-boundary
p4-m6-2-entry-acceptance-non-evidence-surface-acceptance-non-routing-boundary
p4-m6-2-entry-acceptance-non-evidence-surface-acceptance-non-execution-boundary
p4-m6-2-entry-acceptance-non-evidence-surface-acceptance-non-record-boundary
p4-m6-2-entry-acceptance-non-evidence-surface-acceptance-non-storage-boundary
p4-m6-2-entry-acceptance-non-evidence-surface-acceptance-non-persistence-boundary
p4-m6-2-entry-acceptance-non-evidence-surface-acceptance-non-mutation-boundary
p4-m6-2-entry-acceptance-non-evidence-surface-implementation-corridor-v7-productization-ui-operator-console-deferred-boundary
p4-m6-2-entry-acceptance-non-evidence-surface-api-mcp-connector-agent-network-external-integration-non-start-boundary
p4-m6-2-entry-acceptance-non-evidence-surface-static-acceptance-and-evidence-validation-authorization-routing-execution-record-storage-mutation-semantics-disabled
""".splitlines()
    if line
)

DATACLASS_FIELDS = {
    "field_order",
    "field_id",
    "field_name",
    "field_purpose",
    "p4_m6_2_entry_acceptance_non_evidence_surface_category",
    "p4_m6_2_entry_acceptance_non_evidence_surface_semantics_disabled",
}

REQUIRED_BOUNDARY_PHRASES = tuple(
    line
    for line in """
P4-M6.2
Entry Acceptance Non-Evidence Surface
P4-M6.2 Entry Acceptance Non-Evidence Surface
read-only
definition-only
p4-m6-2-entry-acceptance-non-evidence-surface-only
entry-acceptance-non-evidence-surface-only
static-acceptance-labels-only
non-evidence-acceptance-surface-only
non-validation-input-acceptance-surface-only
non-validation-acceptance-surface-only
non-inference-acceptance-surface-only
non-scoring-acceptance-surface-only
non-verdict-acceptance-surface-only
non-authorization-acceptance-surface-only
non-confirmation-acceptance-surface-only
non-approval-acceptance-surface-only
non-recommendation-acceptance-surface-only
non-routing-acceptance-surface-only
non-execution-acceptance-surface-only
non-record-acceptance-surface-only
non-storage-acceptance-surface-only
non-persistence-acceptance-surface-only
non-mutation-acceptance-surface-only
implementation-corridor-not-started-boundary-only
api-implementation-disabled
mcp-implementation-disabled
connector-implementation-disabled
agent-auto-call-disabled
network-access-disabled
external-system-integration-disabled
declaration-only
inspection-only
P4-M6.2 defines only static entry acceptance surfaces
P4-M6.2 does not accept readiness evidence
P4-M6.2 does not collect readiness evidence
P4-M6.2 does not classify readiness evidence
P4-M6.2 does not treat acceptance as readiness evidence
P4-M6.2 does not treat acceptance as validation input
P4-M6.2 does not validate acceptance
P4-M6.2 does not infer acceptance
P4-M6.2 does not score acceptance
P4-M6.2 does not produce acceptance verdict
P4-M6.2 does not authorize entry
P4-M6.2 does not confirm entry
P4-M6.2 does not approve entry
P4-M6.2 does not recommend entry
P4-M6.2 does not route implementation
P4-M6.2 does not execute
P4-M6.2 does not create records
P4-M6.2 does not create storage
P4-M6.2 does not persist state
P4-M6.2 does not mutate memory
P4-M6.2 does not start implementation corridor
P4-M6.2 is not API implementation
P4-M6.2 is not MCP implementation
P4-M6.2 is not Connector implementation
P4-M6.2 is not API client implementation
P4-M6.2 is not MCP client implementation
P4-M6.2 is not MCP server implementation
P4-M6.2 is not MCP transport implementation
P4-M6.2 is not MCP session implementation
P4-M6.2 is not Connector client implementation
P4-M6.2 is not Connector adapter implementation
P4-M6.2 is not Connector runtime implementation
P4-M6.2 is not Agent auto-call
P4-M6.2 is not external system integration
P4-M6.2 is not network access
P4-M6.2 is not live API endpoint probing
P4-M6.2 is not live MCP server probing
P4-M6.2 is not live provider probing
P4-M6.2 is not live provider discovery
P4-M6.2 is not OAuth flow
P4-M6.2 is not credential use
P4-M6.2 is not secret access
P4-M6.2 is not secret inspection
P4-M6.2 is not API call
P4-M6.2 is not MCP tool call
P4-M6.2 is not MCP resource access
P4-M6.2 is not MCP prompt execution
P4-M6.2 is not connector data fetch
P4-M6.2 is not connector data write
P4-M6.2 is not connector mutation
P4-M6.2 is not authentication testing
P4-M6.2 is not authorization testing
P4-M6.2 is not schema validation
P4-M6.1 Entry Preconditions Definition Surface remains the direct prior entry preconditions reference
P4-M6.0 Next Corridor Entry Boundary Contract remains an inherited entry boundary reference
P4-M5.6 Final Closure Handoff / Next Corridor Non-Start Index remains an inherited final closure handoff reference
P4-M5.5 Readiness Audit Closure / Non-Start Boundary Seal remains an inherited closure seal reference
P4-M5.4 API / MCP / Connector Cross-Surface Alignment Map remains an inherited cross-surface alignment map reference
static entry acceptance labels are definition-only
acceptance label definition surface is definition-only
acceptance surface scope is definition-only
entry acceptance surfaces are not readiness evidence
entry acceptance surfaces are not validation inputs
entry acceptance surfaces are not authorization
entry acceptance surfaces are not confirmation
entry acceptance surfaces are not approval
entry acceptance surfaces are not recommendation
entry acceptance surfaces are not routing
entry acceptance surfaces are not execution
entry acceptance surfaces are not records
entry acceptance surfaces are not storage
entry acceptance surfaces are not persistence
entry acceptance surfaces are not mutation
implementation corridor remains not started
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
v7 remains not started
productization remains not started
UI remains not started
Operator Console remains not started
no acceptance validation
no acceptance inference
no acceptance scoring
no acceptance verdict
no readiness evidence
no validation inputs
no authorization
no confirmation
no approval
no recommendation
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
no routing
no execution
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

ALL_EXPECTED_TRUE_STATUS_KEYS = tuple(
    line
    for line in """
definition_only
p4_m6_2_entry_acceptance_non_evidence_surface_started
p4_m6_2_entry_acceptance_non_evidence_surface_only
entry_acceptance_non_evidence_surface_only
static_acceptance_labels_only
acceptance_non_evidence_surface_only
acceptance_non_validation_input_surface_only
acceptance_non_validation_surface_only
acceptance_non_inference_surface_only
acceptance_non_scoring_surface_only
acceptance_non_verdict_surface_only
acceptance_non_authorization_surface_only
acceptance_non_confirmation_surface_only
acceptance_non_approval_surface_only
acceptance_non_recommendation_surface_only
acceptance_non_routing_surface_only
acceptance_non_execution_surface_only
acceptance_non_record_surface_only
acceptance_non_storage_surface_only
acceptance_non_persistence_surface_only
acceptance_non_mutation_surface_only
implementation_corridor_not_started_boundary_only
api_implementation_disabled
mcp_implementation_disabled
connector_implementation_disabled
agent_auto_call_disabled
network_access_disabled
external_system_integration_disabled
declaration_only
inspection_only
p4_m6_2_started_as_acceptance_definition_only
p4_m6_position_preserved
p4_m6_1_entry_preconditions_definition_surface_reference_defined
p4_m6_0_entry_boundary_contract_reference_defined
p4_m5_6_final_closure_handoff_reference_defined
p4_m5_5_closure_seal_reference_defined
p4_m5_4_cross_surface_alignment_map_reference_defined
static_entry_acceptance_labels_defined
acceptance_label_definition_surface_defined
acceptance_surface_scope_defined
acceptance_non_evidence_boundary_defined
acceptance_non_validation_input_boundary_defined
acceptance_non_authorization_boundary_defined
acceptance_non_confirmation_boundary_defined
acceptance_non_approval_boundary_defined
acceptance_non_recommendation_boundary_defined
acceptance_non_routing_boundary_defined
acceptance_non_execution_boundary_defined
acceptance_non_record_boundary_defined
acceptance_non_storage_boundary_defined
acceptance_non_persistence_boundary_defined
acceptance_non_mutation_boundary_defined
entry_acceptance_surfaces_are_definition_only
entry_acceptance_surfaces_are_static_labels_only
entry_acceptance_surfaces_are_not_readiness_evidence
entry_acceptance_surfaces_are_not_validation_inputs
entry_acceptance_surfaces_are_not_authorization
entry_acceptance_surfaces_are_not_confirmation
entry_acceptance_surfaces_are_not_approval
entry_acceptance_surfaces_are_not_recommendation
entry_acceptance_surfaces_are_not_routing
entry_acceptance_surfaces_are_not_execution
entry_acceptance_surfaces_are_not_records
entry_acceptance_surfaces_are_not_storage
entry_acceptance_surfaces_are_not_persistence
entry_acceptance_surfaces_are_not_mutation
acceptance_validation_deferred
acceptance_inference_deferred
acceptance_scoring_deferred
acceptance_verdict_deferred
acceptance_authorization_deferred
acceptance_confirmation_deferred
acceptance_approval_deferred
acceptance_recommendation_deferred
implementation_start_deferred
api_implementation_deferred
mcp_implementation_deferred
connector_implementation_deferred
agent_auto_call_deferred
network_access_deferred
external_system_integration_deferred
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
command_returns_before_store_creation
no_workspace_storage_created
no_memory_mutation_surface_defined
""".splitlines()
    if line
)

COUNTED_EXPECTED_TRUE_STATUS_KEYS = tuple(ALL_EXPECTED_TRUE_STATUS_KEYS[:94])
SUPPLEMENTAL_EXPECTED_TRUE_STATUS_KEYS = tuple(ALL_EXPECTED_TRUE_STATUS_KEYS[94:])

ALL_EXPECTED_FALSE_STATUS_KEYS = tuple(
    line
    for line in """
live_validation_enabled
entry_acceptance_validation_enabled
entry_acceptance_inference_enabled
entry_acceptance_scoring_enabled
entry_acceptance_verdict_enabled
entry_acceptance_evidence_enabled
entry_acceptance_validation_input_enabled
entry_acceptance_authorization_enabled
entry_acceptance_confirmation_enabled
entry_acceptance_approval_enabled
entry_acceptance_recommendation_enabled
entry_acceptance_routing_enabled
entry_acceptance_execution_enabled
entry_acceptance_record_creation_enabled
entry_acceptance_storage_enabled
entry_acceptance_persistence_enabled
entry_acceptance_mutation_enabled
acceptance_validation_enabled
acceptance_inference_enabled
acceptance_scoring_enabled
acceptance_verdict_enabled
acceptance_evidence_collection_enabled
acceptance_validation_input_enabled
acceptance_authorization_enabled
acceptance_confirmation_enabled
acceptance_approval_enabled
acceptance_recommendation_enabled
acceptance_routing_enabled
acceptance_execution_enabled
acceptance_record_creation_enabled
acceptance_storage_enabled
acceptance_persistence_enabled
acceptance_mutation_enabled
readiness_evidence_collection_enabled
readiness_evidence_classification_enabled
validation_input_enabled
authorization_enabled
confirmation_enabled
approval_enabled
recommendation_enabled
routing_enabled
executable_planning_enabled
next_action_generation_enabled
implementation_corridor_started
implementation_entry_enabled
implementation_acceptance_validation_enabled
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
entry_validation_enabled
entry_inference_enabled
entry_scoring_enabled
entry_verdict_enabled
entry_authorization_enabled
entry_confirmation_enabled
entry_approval_enabled
entry_recommendation_enabled
entry_routing_enabled
entry_execution_enabled
entry_record_creation_enabled
entry_storage_enabled
entry_mutation_enabled
boundary_validation_enabled
boundary_inference_enabled
boundary_scoring_enabled
boundary_verdict_enabled
boundary_routing_enabled
boundary_execution_enabled
boundary_record_creation_enabled
boundary_storage_enabled
boundary_mutation_enabled
handoff_validation_enabled
handoff_inference_enabled
handoff_scoring_enabled
handoff_verdict_enabled
handoff_routing_enabled
handoff_execution_enabled
handoff_record_creation_enabled
handoff_storage_enabled
handoff_mutation_enabled
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
version_bump_enabled
tag_creation_enabled
""".splitlines()
    if line
)

OPERATOR_SMOKE_PHRASES = tuple(
    line
    for line in """
P4-M6.2 Entry Acceptance Non-Evidence Surface
read-only
definition-only
p4-m6-2-entry-acceptance-non-evidence-surface-only
entry-acceptance-non-evidence-surface-only
static-acceptance-labels-only
non-evidence-acceptance-surface-only
non-validation-input-acceptance-surface-only
non-validation-acceptance-surface-only
non-inference-acceptance-surface-only
non-scoring-acceptance-surface-only
non-verdict-acceptance-surface-only
non-authorization-acceptance-surface-only
non-confirmation-acceptance-surface-only
non-approval-acceptance-surface-only
non-recommendation-acceptance-surface-only
non-routing-acceptance-surface-only
non-execution-acceptance-surface-only
non-record-acceptance-surface-only
non-storage-acceptance-surface-only
non-persistence-acceptance-surface-only
non-mutation-acceptance-surface-only
implementation-corridor-not-started-boundary-only
api-implementation-disabled
mcp-implementation-disabled
connector-implementation-disabled
agent-auto-call-disabled
network-access-disabled
external-system-integration-disabled
declaration-only
inspection-only
P4-M6.2 defines only static entry acceptance surfaces
P4-M6.2 does not accept readiness evidence
P4-M6.2 does not collect readiness evidence
P4-M6.2 does not classify readiness evidence
P4-M6.2 does not treat acceptance as readiness evidence
P4-M6.2 does not treat acceptance as validation input
P4-M6.2 does not validate acceptance
P4-M6.2 does not infer acceptance
P4-M6.2 does not score acceptance
P4-M6.2 does not produce acceptance verdict
P4-M6.2 does not authorize entry
P4-M6.2 does not confirm entry
P4-M6.2 does not approve entry
P4-M6.2 does not recommend entry
P4-M6.2 does not route implementation
P4-M6.2 does not execute
P4-M6.2 does not create storage
P4-M6.2 does not mutate memory
P4-M6.2 does not start implementation corridor
no acceptance validation
no readiness evidence
no validation inputs
no authorization
no API implementation
no MCP implementation
no Connector implementation
no Agent auto-call
no external system integration
no network access
no readiness validation
no readiness inference
no readiness scoring
no readiness verdict
no routing
no execution
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
""".splitlines()
    if line
)



# P4-M6.2 strict counted boolean status alignment.
# Expected true status keys must exactly match TRUE_STATUS_FLAGS.
ALL_EXPECTED_TRUE_STATUS_KEYS = COUNTED_EXPECTED_TRUE_STATUS_KEYS
SUPPLEMENTAL_EXPECTED_TRUE_STATUS_KEYS = ()

def test_field_inventory_is_exact_and_ordered():
    fields = list_p4_m6_2_entry_acceptance_non_evidence_surface_fields()

    assert len(fields) == 23
    assert p4_m6_2_entry_acceptance_non_evidence_surface_field_ids() == FIELD_IDS
    assert tuple(field.field_order for field in fields) == tuple(range(1, 24))
    assert all(
        isinstance(field, P4M62EntryAcceptanceNonEvidenceSurfaceField)
        for field in fields
    )
    assert {
        field.name
        for field in dataclasses.fields(P4M62EntryAcceptanceNonEvidenceSurfaceField)
    } == DATACLASS_FIELDS


def test_boundary_phrase_inventory_is_required_contract():
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in BOUNDARY_PHRASE_LINES
        assert phrase in P4_M6_2_ENTRY_ACCEPTANCE_NON_EVIDENCE_SURFACE_BOUNDARY


def test_markdown_renders_static_boundary_and_field_ids():
    markdown = render_p4_m6_2_entry_acceptance_non_evidence_surface_markdown()

    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in markdown
    for field_id in FIELD_IDS:
        assert field_id in markdown
    assert "## Status Report" in markdown
    assert "## P4-M6.2 Entry Acceptance Non-Evidence Surface Fields" in markdown
    assert "P4-M6.2 Entry Acceptance Non-Evidence Surface" in markdown


def test_report_has_required_true_false_status_flags():
    status = p4_m6_2_entry_acceptance_non_evidence_surface_report()

    assert status["phase"] == "P4-M6.2"
    assert status["feature"] == "Entry Acceptance Non-Evidence Surface"
    assert status["mode"] == "read-only"
    assert status["package_version"] == "6.16.0"
    assert status["p4_m6_2_entry_acceptance_non_evidence_surface_field_count"] == 23
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
    assert TRUE_STATUS_FLAGS == COUNTED_EXPECTED_TRUE_STATUS_KEYS
    assert SUPPLEMENTAL_TRUE_STATUS_FLAGS == SUPPLEMENTAL_EXPECTED_TRUE_STATUS_KEYS
    assert FALSE_STATUS_FLAGS == ALL_EXPECTED_FALSE_STATUS_KEYS
    assert len(TRUE_STATUS_FLAGS) == 94
    assert len(SUPPLEMENTAL_TRUE_STATUS_FLAGS) == 0
    assert len(ALL_EXPECTED_TRUE_STATUS_KEYS) == 94
    assert len(FALSE_STATUS_FLAGS) == 144
    for flag in ALL_EXPECTED_TRUE_STATUS_KEYS:
        assert status[flag] is True
    for flag in ALL_EXPECTED_FALSE_STATUS_KEYS:
        assert status[flag] is False


def test_as_dicts_is_deterministic_and_read_only_shape():
    fields = p4_m6_2_entry_acceptance_non_evidence_surface_as_dicts()

    assert len(fields) == 23
    assert tuple(field["field_id"] for field in fields) == FIELD_IDS
    assert fields == p4_m6_2_entry_acceptance_non_evidence_surface_as_dicts()
    assert all(
        field["p4_m6_2_entry_acceptance_non_evidence_surface_category"]
        == "p4-m6-2-entry-acceptance-non-evidence-surface-category"
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
            "p4-m6-2-entry-acceptance-non-evidence-surface",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M6.2 Entry Acceptance Non-Evidence Surface\n")
    for phrase in OPERATOR_SMOKE_PHRASES:
        assert phrase in stdout
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in stdout
    assert not (tmp_path / ".local" / "subspace_memory").exists()


def test_operator_json_command_returns_required_report(tmp_path: Path):
    code, output, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "p4-m6-2-entry-acceptance-non-evidence-surface",
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
    assert output["true_flags"] == 94
    assert output["false_flags"] == 144
    assert output["boundary"] == P4_M6_2_ENTRY_ACCEPTANCE_NON_EVIDENCE_SURFACE_BOUNDARY
    assert tuple(field["field_id"] for field in output["fields"]) == FIELD_IDS
    status = output["status"]
    assert status["phase"] == "P4-M6.2"
    assert status["feature"] == "Entry Acceptance Non-Evidence Surface"
    assert status["mode"] == "read-only"
    for flag in ALL_EXPECTED_TRUE_STATUS_KEYS:
        assert status[flag] is True
    for flag in ALL_EXPECTED_FALSE_STATUS_KEYS:
        assert status[flag] is False
    assert not (tmp_path / ".local" / "subspace_memory").exists()


def test_parser_exposes_only_expected_memory_loop_command_surface():
    commands = _memory_loop_subcommands(build_parser())

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
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

    command = "p4-m6-2-entry-acceptance-non-evidence-surface"
    assert command not in entry_points
    assert command not in str(entry_points)
    assert pyproject["project"]["version"] == "6.16.0"


def test_static_doc_contains_required_boundaries_and_fields():
    project_root = Path(__file__).resolve().parents[1]
    doc_path = (
        project_root
        / "docs"
        / "CIVILIZATION_CORE_P4_M6_2_ENTRY_ACCEPTANCE_NON_EVIDENCE_SURFACE.md"
    )
    doc = doc_path.read_text(encoding="utf-8")

    assert doc.startswith("# P4-M6.2 Entry Acceptance Non-Evidence Surface\n")
    for field_id in FIELD_IDS:
        assert field_id in doc
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in doc


def test_custom_field_rendering_remains_definition_only():
    field = P4M62EntryAcceptanceNonEvidenceSurfaceField(
        field_order=99,
        field_id="custom-p4-m6-2-entry-acceptance-non-evidence-surface",
        field_name="Custom P4-M6.2 Entry Acceptance Non-Evidence Surface",
        field_purpose="custom read-only definition-only inspection-only field",
        p4_m6_2_entry_acceptance_non_evidence_surface_category=(
            "custom-p4-m6-2-entry-acceptance-non-evidence-surface-category"
        ),
        p4_m6_2_entry_acceptance_non_evidence_surface_semantics_disabled=(
            "no acceptance validation semantics; no readiness evidence semantics"
        ),
    )

    markdown = render_p4_m6_2_entry_acceptance_non_evidence_surface_markdown((field,))

    assert "custom-p4-m6-2-entry-acceptance-non-evidence-surface" in markdown
    assert "no acceptance validation semantics" in markdown
    assert "P4-M6.2 Entry Acceptance Non-Evidence Surface" in markdown


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
