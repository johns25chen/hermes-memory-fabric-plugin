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
from hermes_memory_fabric.p4_m6_3_entry_deferral_non_execution_surface import (
    BOUNDARY_PHRASE_LINES,
    FALSE_STATUS_FLAGS,
    P4_M6_3_ENTRY_DEFERRAL_NON_EXECUTION_SURFACE_BOUNDARY,
    TRUE_STATUS_FLAGS,
    P4M63EntryDeferralNonExecutionSurfaceField,
    list_p4_m6_3_entry_deferral_non_execution_surface_fields,
    p4_m6_3_entry_deferral_non_execution_surface_as_dicts,
    p4_m6_3_entry_deferral_non_execution_surface_field_ids,
    p4_m6_3_entry_deferral_non_execution_surface_report,
    render_p4_m6_3_entry_deferral_non_execution_surface_markdown,
)


FIELD_IDS = tuple(
    line
    for line in """
p4-m6-3-entry-deferral-non-execution-surface-id
p4-m6-3-entry-deferral-non-execution-surface-phase
p4-m6-3-entry-deferral-non-execution-surface-mode
p4-m6-3-entry-deferral-non-execution-surface-p4-m6-position
p4-m6-3-entry-deferral-non-execution-surface-direct-prior-p4-m6-2-entry-acceptance-non-evidence-surface-reference
p4-m6-3-entry-deferral-non-execution-surface-inherited-p4-m6-1-entry-preconditions-definition-surface-reference
p4-m6-3-entry-deferral-non-execution-surface-inherited-p4-m6-0-entry-boundary-contract-reference
p4-m6-3-entry-deferral-non-execution-surface-static-deferral-label-scope
p4-m6-3-entry-deferral-non-execution-surface-deferral-label-definition-surface
p4-m6-3-entry-deferral-non-execution-surface-deferral-non-execution-boundary
p4-m6-3-entry-deferral-non-execution-surface-deferral-non-rejection-boundary
p4-m6-3-entry-deferral-non-execution-surface-deferral-non-denial-boundary
p4-m6-3-entry-deferral-non-execution-surface-deferral-non-approval-boundary
p4-m6-3-entry-deferral-non-execution-surface-deferral-non-authorization-boundary
p4-m6-3-entry-deferral-non-execution-surface-deferral-non-confirmation-boundary
p4-m6-3-entry-deferral-non-execution-surface-deferral-non-recommendation-boundary
p4-m6-3-entry-deferral-non-execution-surface-deferral-non-routing-boundary
p4-m6-3-entry-deferral-non-execution-surface-deferral-non-readiness-validation-boundary
p4-m6-3-entry-deferral-non-execution-surface-deferral-non-readiness-evidence-boundary
p4-m6-3-entry-deferral-non-execution-surface-deferral-non-record-storage-persistence-mutation-boundary
p4-m6-3-entry-deferral-non-execution-surface-implementation-corridor-v7-productization-ui-operator-console-deferred-boundary
p4-m6-3-entry-deferral-non-execution-surface-api-mcp-connector-agent-network-external-integration-non-start-boundary
p4-m6-3-entry-deferral-non-execution-surface-static-deferral-and-validation-authorization-routing-execution-record-storage-mutation-semantics-disabled
""".splitlines()
    if line
)

DATACLASS_FIELDS = {
    "field_order",
    "field_id",
    "field_name",
    "field_purpose",
    "p4_m6_3_entry_deferral_non_execution_surface_category",
    "p4_m6_3_entry_deferral_non_execution_surface_semantics_disabled",
}

REQUIRED_BOUNDARY_PHRASES = tuple(
    line
    for line in """
P4-M6.3
Entry Deferral Non-Execution Surface
P4-M6.3 Entry Deferral Non-Execution Surface
read-only
definition-only
p4-m6-3-entry-deferral-non-execution-surface-only
entry-deferral-non-execution-surface-only
static-deferral-labels-only
non-execution-deferral-surface-only
non-rejection-deferral-surface-only
non-denial-deferral-surface-only
non-approval-deferral-surface-only
non-authorization-deferral-surface-only
non-confirmation-deferral-surface-only
non-recommendation-deferral-surface-only
non-routing-deferral-surface-only
non-validation-deferral-surface-only
non-inference-deferral-surface-only
non-scoring-deferral-surface-only
non-verdict-deferral-surface-only
non-record-deferral-surface-only
non-storage-deferral-surface-only
non-persistence-deferral-surface-only
non-mutation-deferral-surface-only
implementation-corridor-not-started-boundary-only
api-implementation-disabled
mcp-implementation-disabled
connector-implementation-disabled
agent-auto-call-disabled
network-access-disabled
external-system-integration-disabled
declaration-only
inspection-only
P4-M6.3 defines only static entry deferral surfaces
P4-M6.3 does not reject entry
P4-M6.3 does not deny entry
P4-M6.3 does not approve entry
P4-M6.3 does not authorize entry
P4-M6.3 does not confirm entry
P4-M6.3 does not recommend entry
P4-M6.3 does not route implementation
P4-M6.3 does not execute
P4-M6.3 does not validate deferral
P4-M6.3 does not infer deferral
P4-M6.3 does not score deferral
P4-M6.3 does not produce deferral verdict
P4-M6.3 does not collect readiness evidence
P4-M6.3 does not classify readiness evidence
P4-M6.3 does not treat deferral as readiness evidence
P4-M6.3 does not treat deferral as validation input
P4-M6.3 does not create records
P4-M6.3 does not create storage
P4-M6.3 does not persist state
P4-M6.3 does not mutate memory
P4-M6.3 does not start implementation corridor
P4-M6.3 is not API implementation
P4-M6.3 is not MCP implementation
P4-M6.3 is not Connector implementation
P4-M6.3 is not API client implementation
P4-M6.3 is not MCP client implementation
P4-M6.3 is not MCP server implementation
P4-M6.3 is not MCP transport implementation
P4-M6.3 is not MCP session implementation
P4-M6.3 is not Connector client implementation
P4-M6.3 is not Connector adapter implementation
P4-M6.3 is not Connector runtime implementation
P4-M6.3 is not Agent auto-call
P4-M6.3 is not external system integration
P4-M6.3 is not network access
P4-M6.3 is not live API endpoint probing
P4-M6.3 is not live MCP server probing
P4-M6.3 is not live provider probing
P4-M6.3 is not live provider discovery
P4-M6.3 is not OAuth flow
P4-M6.3 is not credential use
P4-M6.3 is not secret access
P4-M6.3 is not secret inspection
P4-M6.3 is not API call
P4-M6.3 is not MCP tool call
P4-M6.3 is not MCP resource access
P4-M6.3 is not MCP prompt execution
P4-M6.3 is not connector data fetch
P4-M6.3 is not connector data write
P4-M6.3 is not connector mutation
P4-M6.3 is not authentication testing
P4-M6.3 is not authorization testing
P4-M6.3 is not schema validation
P4-M6.2 Entry Acceptance Non-Evidence Surface remains the direct prior entry acceptance reference
P4-M6.1 Entry Preconditions Definition Surface remains an inherited entry preconditions reference
P4-M6.0 Next Corridor Entry Boundary Contract remains an inherited entry boundary reference
P4-M5.6 Final Closure Handoff / Next Corridor Non-Start Index remains an inherited final closure handoff reference
P4-M5.5 Readiness Audit Closure / Non-Start Boundary Seal remains an inherited closure seal reference
P4-M5.4 API / MCP / Connector Cross-Surface Alignment Map remains an inherited cross-surface alignment map reference
static entry deferral labels are definition-only
deferral label definition surface is definition-only
deferral surface scope is definition-only
entry deferral surfaces are not rejection
entry deferral surfaces are not denial
entry deferral surfaces are not approval
entry deferral surfaces are not authorization
entry deferral surfaces are not confirmation
entry deferral surfaces are not recommendation
entry deferral surfaces are not routing
entry deferral surfaces are not execution
entry deferral surfaces are not readiness validation
entry deferral surfaces are not readiness evidence
entry deferral surfaces are not records
entry deferral surfaces are not storage
entry deferral surfaces are not persistence
entry deferral surfaces are not mutation
implementation corridor remains not started
API implementation remains not started
MCP implementation remains not started
Connector implementation remains not started
Agent auto-call remains not started
external system integration remains not started
network access remains not started
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
no deferral validation
no deferral inference
no deferral scoring
no deferral verdict
no rejection
no denial
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
no readiness validation
no readiness inference
no readiness scoring
no readiness verdict
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

EXPECTED_TRUE_STATUS_KEYS = tuple(
    line
    for line in """
definition_only
p4_m6_3_entry_deferral_non_execution_surface_started
p4_m6_3_entry_deferral_non_execution_surface_only
entry_deferral_non_execution_surface_only
static_deferral_labels_only
deferral_non_execution_surface_only
deferral_non_rejection_surface_only
deferral_non_denial_surface_only
deferral_non_approval_surface_only
deferral_non_authorization_surface_only
deferral_non_confirmation_surface_only
deferral_non_recommendation_surface_only
deferral_non_routing_surface_only
deferral_non_validation_surface_only
deferral_non_inference_surface_only
deferral_non_scoring_surface_only
deferral_non_verdict_surface_only
deferral_non_record_surface_only
deferral_non_storage_surface_only
deferral_non_persistence_surface_only
deferral_non_mutation_surface_only
implementation_corridor_not_started_boundary_only
api_implementation_disabled
mcp_implementation_disabled
connector_implementation_disabled
agent_auto_call_disabled
network_access_disabled
external_system_integration_disabled
declaration_only
inspection_only
p4_m6_3_started_as_deferral_definition_only
p4_m6_position_preserved
p4_m6_2_entry_acceptance_non_evidence_surface_reference_defined
p4_m6_1_entry_preconditions_definition_surface_reference_defined
p4_m6_0_entry_boundary_contract_reference_defined
p4_m5_6_final_closure_handoff_reference_defined
p4_m5_5_closure_seal_reference_defined
p4_m5_4_cross_surface_alignment_map_reference_defined
static_entry_deferral_labels_defined
deferral_label_definition_surface_defined
deferral_surface_scope_defined
deferral_non_execution_boundary_defined
deferral_non_rejection_boundary_defined
deferral_non_denial_boundary_defined
deferral_non_approval_boundary_defined
deferral_non_authorization_boundary_defined
deferral_non_confirmation_boundary_defined
deferral_non_recommendation_boundary_defined
deferral_non_routing_boundary_defined
deferral_non_readiness_validation_boundary_defined
deferral_non_readiness_evidence_boundary_defined
deferral_non_record_boundary_defined
deferral_non_storage_boundary_defined
deferral_non_persistence_boundary_defined
deferral_non_mutation_boundary_defined
entry_deferral_surfaces_are_definition_only
entry_deferral_surfaces_are_static_labels_only
entry_deferral_surfaces_are_not_rejection
entry_deferral_surfaces_are_not_denial
entry_deferral_surfaces_are_not_approval
entry_deferral_surfaces_are_not_authorization
entry_deferral_surfaces_are_not_confirmation
entry_deferral_surfaces_are_not_recommendation
entry_deferral_surfaces_are_not_routing
entry_deferral_surfaces_are_not_execution
entry_deferral_surfaces_are_not_readiness_validation
entry_deferral_surfaces_are_not_readiness_evidence
entry_deferral_surfaces_are_not_records
entry_deferral_surfaces_are_not_storage
entry_deferral_surfaces_are_not_persistence
entry_deferral_surfaces_are_not_mutation
deferral_validation_deferred
deferral_inference_deferred
deferral_scoring_deferred
deferral_verdict_deferred
deferral_authorization_deferred
deferral_confirmation_deferred
deferral_approval_deferred
deferral_recommendation_deferred
deferral_routing_deferred
deferral_execution_deferred
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
""".splitlines()
    if line
)

EXPECTED_FALSE_STATUS_KEYS = tuple(
    line
    for line in """
live_validation_enabled
entry_deferral_validation_enabled
entry_deferral_inference_enabled
entry_deferral_scoring_enabled
entry_deferral_verdict_enabled
entry_deferral_rejection_enabled
entry_deferral_denial_enabled
entry_deferral_approval_enabled
entry_deferral_authorization_enabled
entry_deferral_confirmation_enabled
entry_deferral_recommendation_enabled
entry_deferral_routing_enabled
entry_deferral_execution_enabled
entry_deferral_evidence_enabled
entry_deferral_validation_input_enabled
entry_deferral_record_creation_enabled
entry_deferral_storage_enabled
entry_deferral_persistence_enabled
entry_deferral_mutation_enabled
deferral_validation_enabled
deferral_inference_enabled
deferral_scoring_enabled
deferral_verdict_enabled
deferral_rejection_enabled
deferral_denial_enabled
deferral_approval_enabled
deferral_authorization_enabled
deferral_confirmation_enabled
deferral_recommendation_enabled
deferral_routing_enabled
deferral_execution_enabled
deferral_evidence_collection_enabled
deferral_validation_input_enabled
deferral_record_creation_enabled
deferral_storage_enabled
deferral_persistence_enabled
deferral_mutation_enabled
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
implementation_deferral_validation_enabled
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
inference_enabled
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
entry_rejection_enabled
entry_denial_enabled
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
deferral_as_rejection_enabled
deferral_as_denial_enabled
deferral_as_approval_enabled
deferral_as_authorization_enabled
deferral_as_execution_enabled
deferral_as_readiness_validation_enabled
deferral_as_readiness_evidence_enabled
""".splitlines()
    if line
)

OPERATOR_SMOKE_PHRASES = tuple(
    line
    for line in """
P4-M6.3 Entry Deferral Non-Execution Surface
read-only
definition-only
p4-m6-3-entry-deferral-non-execution-surface-only
entry-deferral-non-execution-surface-only
static-deferral-labels-only
non-execution-deferral-surface-only
non-rejection-deferral-surface-only
non-denial-deferral-surface-only
non-approval-deferral-surface-only
non-authorization-deferral-surface-only
non-confirmation-deferral-surface-only
non-recommendation-deferral-surface-only
non-routing-deferral-surface-only
non-validation-deferral-surface-only
non-inference-deferral-surface-only
non-scoring-deferral-surface-only
non-verdict-deferral-surface-only
non-record-deferral-surface-only
non-storage-deferral-surface-only
non-persistence-deferral-surface-only
non-mutation-deferral-surface-only
implementation-corridor-not-started-boundary-only
api-implementation-disabled
mcp-implementation-disabled
connector-implementation-disabled
agent-auto-call-disabled
network-access-disabled
external-system-integration-disabled
declaration-only
inspection-only
P4-M6.3 defines only static entry deferral surfaces
P4-M6.3 does not reject entry
P4-M6.3 does not deny entry
P4-M6.3 does not approve entry
P4-M6.3 does not authorize entry
P4-M6.3 does not confirm entry
P4-M6.3 does not recommend entry
P4-M6.3 does not route implementation
P4-M6.3 does not execute
P4-M6.3 does not validate deferral
P4-M6.3 does not infer deferral
P4-M6.3 does not score deferral
P4-M6.3 does not produce deferral verdict
P4-M6.3 does not collect readiness evidence
P4-M6.3 does not treat deferral as readiness evidence
P4-M6.3 does not treat deferral as validation input
P4-M6.3 does not create storage
P4-M6.3 does not mutate memory
P4-M6.3 does not start implementation corridor
no deferral validation
no deferral inference
no deferral scoring
no deferral verdict
no rejection
no denial
no approval
no authorization
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
no readiness validation
no readiness inference
no readiness scoring
no readiness verdict
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
p4-m6-9-entry-dependency-non-activation-surface
p4-m6-10-entry-constraint-non-enforcement-surface
p4-m6-11-entry-risk-non-mitigation-surface
p4-m6-12-entry-safeguard-non-activation-surface
p4-m6-13-entry-definition-corridor-closure-review
""".splitlines()
    if line
)


def test_field_inventory_is_exact_and_ordered():
    fields = list_p4_m6_3_entry_deferral_non_execution_surface_fields()

    assert len(fields) == 23
    assert p4_m6_3_entry_deferral_non_execution_surface_field_ids() == FIELD_IDS
    assert tuple(field.field_order for field in fields) == tuple(range(1, 24))
    assert all(
        isinstance(field, P4M63EntryDeferralNonExecutionSurfaceField)
        for field in fields
    )
    assert {
        field.name
        for field in dataclasses.fields(P4M63EntryDeferralNonExecutionSurfaceField)
    } == DATACLASS_FIELDS


def test_boundary_phrase_inventory_is_required_contract():
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in BOUNDARY_PHRASE_LINES
        assert phrase in P4_M6_3_ENTRY_DEFERRAL_NON_EXECUTION_SURFACE_BOUNDARY


def test_markdown_renders_static_boundary_and_field_ids():
    markdown = render_p4_m6_3_entry_deferral_non_execution_surface_markdown()

    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in markdown
    for field_id in FIELD_IDS:
        assert field_id in markdown
    assert "## Status Report" in markdown
    assert "## P4-M6.3 Entry Deferral Non-Execution Surface Fields" in markdown
    assert "P4-M6.3 Entry Deferral Non-Execution Surface" in markdown


def test_report_has_exact_true_false_status_flags():
    status = p4_m6_3_entry_deferral_non_execution_surface_report()

    assert status["phase"] == "P4-M6.3"
    assert status["feature"] == "Entry Deferral Non-Execution Surface"
    assert status["mode"] == "read-only"
    assert status["package_version"] == "6.16.0"
    assert status["p4_m6_3_entry_deferral_non_execution_surface_field_count"] == 23
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
    assert TRUE_STATUS_FLAGS == EXPECTED_TRUE_STATUS_KEYS
    assert FALSE_STATUS_FLAGS == EXPECTED_FALSE_STATUS_KEYS
    assert len(TRUE_STATUS_FLAGS) == 102
    assert len(FALSE_STATUS_FLAGS) == 158
    actual_true_keys = tuple(key for key, value in status.items() if value is True)
    actual_false_keys = tuple(key for key, value in status.items() if value is False)
    assert actual_true_keys == TRUE_STATUS_FLAGS
    assert actual_false_keys == FALSE_STATUS_FLAGS


def test_as_dicts_is_deterministic_and_read_only_shape():
    fields = p4_m6_3_entry_deferral_non_execution_surface_as_dicts()

    assert len(fields) == 23
    assert tuple(field["field_id"] for field in fields) == FIELD_IDS
    assert fields == p4_m6_3_entry_deferral_non_execution_surface_as_dicts()
    assert all(
        field["p4_m6_3_entry_deferral_non_execution_surface_category"]
        == "p4-m6-3-entry-deferral-non-execution-surface-category"
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
            "p4-m6-3-entry-deferral-non-execution-surface",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M6.3 Entry Deferral Non-Execution Surface\n")
    for phrase in OPERATOR_SMOKE_PHRASES:
        assert phrase in stdout
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in stdout
    assert not (tmp_path / ".local" / "subspace_memory").exists()


def test_operator_json_command_returns_required_report(tmp_path: Path):
    code, output, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "p4-m6-3-entry-deferral-non-execution-surface",
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
    assert output["true_flags"] == 102
    assert output["false_flags"] == 158
    assert output["boundary"] == P4_M6_3_ENTRY_DEFERRAL_NON_EXECUTION_SURFACE_BOUNDARY
    assert tuple(field["field_id"] for field in output["fields"]) == FIELD_IDS
    status = output["status"]
    assert status["phase"] == "P4-M6.3"
    assert status["feature"] == "Entry Deferral Non-Execution Surface"
    assert status["mode"] == "read-only"
    actual_true_keys = {key for key, value in status.items() if value is True}
    actual_false_keys = {key for key, value in status.items() if value is False}
    assert actual_true_keys == set(TRUE_STATUS_FLAGS)
    assert actual_false_keys == set(FALSE_STATUS_FLAGS)
    assert not (tmp_path / ".local" / "subspace_memory").exists()


def test_parser_exposes_only_expected_memory_loop_command_surface():
    commands = _memory_loop_subcommands(build_parser())

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
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

    command = "p4-m6-3-entry-deferral-non-execution-surface"
    assert command not in entry_points
    assert command not in str(entry_points)
    assert pyproject["project"]["version"] == "6.16.0"


def test_static_doc_contains_required_boundaries_and_fields():
    project_root = Path(__file__).resolve().parents[1]
    doc_path = (
        project_root
        / "docs"
        / "CIVILIZATION_CORE_P4_M6_3_ENTRY_DEFERRAL_NON_EXECUTION_SURFACE.md"
    )
    doc = doc_path.read_text(encoding="utf-8")

    assert doc.startswith("# P4-M6.3 Entry Deferral Non-Execution Surface\n")
    for field_id in FIELD_IDS:
        assert field_id in doc
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in doc


def test_custom_field_rendering_remains_definition_only():
    field = P4M63EntryDeferralNonExecutionSurfaceField(
        field_order=99,
        field_id="custom-p4-m6-3-entry-deferral-non-execution-surface",
        field_name="Custom P4-M6.3 Entry Deferral Non-Execution Surface",
        field_purpose="custom read-only definition-only inspection-only field",
        p4_m6_3_entry_deferral_non_execution_surface_category=(
            "custom-p4-m6-3-entry-deferral-non-execution-surface-category"
        ),
        p4_m6_3_entry_deferral_non_execution_surface_semantics_disabled=(
            "no deferral validation semantics; no execution semantics"
        ),
    )

    markdown = render_p4_m6_3_entry_deferral_non_execution_surface_markdown((field,))

    assert "custom-p4-m6-3-entry-deferral-non-execution-surface" in markdown
    assert "no deferral validation semantics" in markdown
    assert "P4-M6.3 Entry Deferral Non-Execution Surface" in markdown


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
