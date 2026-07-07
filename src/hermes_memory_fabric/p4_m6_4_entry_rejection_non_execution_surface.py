from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence

from .p4_m5_4_cross_surface_alignment_map import (
    p4_m5_4_cross_surface_alignment_map_field_ids,
)
from .p4_m5_5_readiness_audit_closure_non_start_boundary_seal import (
    p4_m5_5_readiness_audit_closure_non_start_boundary_seal_field_ids,
)
from .p4_m5_6_final_closure_handoff_next_corridor_non_start_index import (
    p4_m5_6_final_closure_handoff_next_corridor_non_start_index_field_ids,
)
from .p4_m6_0_next_corridor_entry_boundary_contract import (
    p4_m6_0_next_corridor_entry_boundary_contract_field_ids,
)
from .p4_m6_1_entry_preconditions_definition_surface import (
    p4_m6_1_entry_preconditions_definition_surface_field_ids,
)
from .p4_m6_2_entry_acceptance_non_evidence_surface import (
    p4_m6_2_entry_acceptance_non_evidence_surface_field_ids,
)
from .p4_m6_3_entry_deferral_non_execution_surface import (
    p4_m6_3_entry_deferral_non_execution_surface_field_ids,
)


P4_M6_4_PACKAGE_VERSION = "6.16.0"


@dataclass(frozen=True)
class P4M64EntryRejectionNonExecutionSurfaceField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    p4_m6_4_entry_rejection_non_execution_surface_category: str
    p4_m6_4_entry_rejection_non_execution_surface_semantics_disabled: str


DIRECT_PRIOR_DEFINITION_LAYER_REFERENCES = (
    "P4-M6.3 Entry Deferral Non-Execution Surface",
)

INHERITED_PRIOR_DEFINITION_LAYER_REFERENCES = (
    "P4-M6.2 Entry Acceptance Non-Evidence Surface",
    "P4-M6.1 Entry Preconditions Definition Surface",
    "P4-M6.0 Next Corridor Entry Boundary Contract",
    "P4-M5.6 Final Closure Handoff / Next Corridor Non-Start Index",
    "P4-M5.5 Readiness Audit Closure / Non-Start Boundary Seal",
    "P4-M5.4 API / MCP / Connector Cross-Surface Alignment Map",
    "P4-M5.3 Connector Readiness Audit Surface Map",
    "P4-M5.2 MCP Readiness Audit Surface Map",
    "P4-M5.1 API Readiness Audit Surface Map",
    "P4-M5.0 API / MCP / Connector Readiness Audit Boundary Contract",
)


BOUNDARY_PHRASE_LINES = tuple(
    line
    for line in """
P4-M6.4
Entry Rejection Non-Execution Surface
P4-M6.4 Entry Rejection Non-Execution Surface
read-only
definition-only
p4-m6-4-entry-rejection-non-execution-surface-only
entry-rejection-non-execution-surface-only
static-rejection-labels-only
non-execution-rejection-surface-only
non-action-rejection-surface-only
non-denial-rejection-surface-only
non-punishment-rejection-surface-only
non-blocking-rejection-surface-only
non-approval-rejection-surface-only
non-authorization-rejection-surface-only
non-confirmation-rejection-surface-only
non-recommendation-rejection-surface-only
non-routing-rejection-surface-only
non-validation-rejection-surface-only
non-inference-rejection-surface-only
non-scoring-rejection-surface-only
non-verdict-rejection-surface-only
non-record-rejection-surface-only
non-storage-rejection-surface-only
non-persistence-rejection-surface-only
non-mutation-rejection-surface-only
implementation-corridor-not-started-boundary-only
api-implementation-disabled
mcp-implementation-disabled
connector-implementation-disabled
agent-auto-call-disabled
network-access-disabled
external-system-integration-disabled
declaration-only
inspection-only
P4-M6.4 defines only static entry rejection label surfaces
P4-M6.4 does not perform rejection
P4-M6.4 does not enforce rejection
P4-M6.4 does not deny entry
P4-M6.4 does not punish entry
P4-M6.4 does not block entry
P4-M6.4 does not approve entry
P4-M6.4 does not authorize entry
P4-M6.4 does not confirm entry
P4-M6.4 does not recommend entry
P4-M6.4 does not route implementation
P4-M6.4 does not execute
P4-M6.4 does not validate rejection
P4-M6.4 does not infer rejection
P4-M6.4 does not score rejection
P4-M6.4 does not produce rejection verdict
P4-M6.4 does not collect readiness evidence
P4-M6.4 does not classify readiness evidence
P4-M6.4 does not treat rejection as readiness evidence
P4-M6.4 does not treat rejection as validation input
P4-M6.4 does not create records
P4-M6.4 does not create storage
P4-M6.4 does not persist state
P4-M6.4 does not mutate memory
P4-M6.4 does not start implementation corridor
P4-M6.4 is not API implementation
P4-M6.4 is not MCP implementation
P4-M6.4 is not Connector implementation
P4-M6.4 is not API client implementation
P4-M6.4 is not MCP client implementation
P4-M6.4 is not MCP server implementation
P4-M6.4 is not MCP transport implementation
P4-M6.4 is not MCP session implementation
P4-M6.4 is not Connector client implementation
P4-M6.4 is not Connector adapter implementation
P4-M6.4 is not Connector runtime implementation
P4-M6.4 is not Agent auto-call
P4-M6.4 is not external system integration
P4-M6.4 is not network access
P4-M6.4 is not live API endpoint probing
P4-M6.4 is not live MCP server probing
P4-M6.4 is not live provider probing
P4-M6.4 is not live provider discovery
P4-M6.4 is not OAuth flow
P4-M6.4 is not credential use
P4-M6.4 is not secret access
P4-M6.4 is not secret inspection
P4-M6.4 is not API call
P4-M6.4 is not MCP tool call
P4-M6.4 is not MCP resource access
P4-M6.4 is not MCP prompt execution
P4-M6.4 is not connector data fetch
P4-M6.4 is not connector data write
P4-M6.4 is not connector mutation
P4-M6.4 is not authentication testing
P4-M6.4 is not authorization testing
P4-M6.4 is not schema validation
P4-M6.3 Entry Deferral Non-Execution Surface remains the direct prior entry deferral reference
P4-M6.2 Entry Acceptance Non-Evidence Surface remains an inherited entry acceptance reference
P4-M6.1 Entry Preconditions Definition Surface remains an inherited entry preconditions reference
P4-M6.0 Next Corridor Entry Boundary Contract remains an inherited entry boundary reference
P4-M5.6 Final Closure Handoff / Next Corridor Non-Start Index remains an inherited final closure handoff reference
P4-M5.5 Readiness Audit Closure / Non-Start Boundary Seal remains an inherited closure seal reference
P4-M5.4 API / MCP / Connector Cross-Surface Alignment Map remains an inherited cross-surface alignment map reference
static entry rejection labels are definition-only
rejection label definition surface is definition-only
rejection surface scope is definition-only
entry rejection surfaces are not live rejection actions
entry rejection surfaces are not denial
entry rejection surfaces are not punishment
entry rejection surfaces are not blocking
entry rejection surfaces are not approval
entry rejection surfaces are not authorization
entry rejection surfaces are not confirmation
entry rejection surfaces are not recommendation
entry rejection surfaces are not routing
entry rejection surfaces are not execution
entry rejection surfaces are not readiness validation
entry rejection surfaces are not readiness evidence
entry rejection surfaces are not validation input
entry rejection surfaces are not records
entry rejection surfaces are not storage
entry rejection surfaces are not persistence
entry rejection surfaces are not mutation
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
no rejection validation
no rejection inference
no rejection scoring
no rejection verdict
no rejection action
no rejection enforcement
no denial
no punishment
no blocking
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


TRUE_STATUS_FLAGS = tuple(
    line
    for line in """
definition_only
p4_m6_4_entry_rejection_non_execution_surface_started
p4_m6_4_entry_rejection_non_execution_surface_only
entry_rejection_non_execution_surface_only
static_rejection_labels_only
rejection_non_execution_surface_only
rejection_non_action_surface_only
rejection_non_denial_surface_only
rejection_non_punishment_surface_only
rejection_non_blocking_surface_only
rejection_non_approval_surface_only
rejection_non_authorization_surface_only
rejection_non_confirmation_surface_only
rejection_non_recommendation_surface_only
rejection_non_routing_surface_only
rejection_non_validation_surface_only
rejection_non_inference_surface_only
rejection_non_scoring_surface_only
rejection_non_verdict_surface_only
rejection_non_record_surface_only
rejection_non_storage_surface_only
rejection_non_persistence_surface_only
rejection_non_mutation_surface_only
implementation_corridor_not_started_boundary_only
api_implementation_disabled
mcp_implementation_disabled
connector_implementation_disabled
agent_auto_call_disabled
network_access_disabled
external_system_integration_disabled
declaration_only
inspection_only
p4_m6_4_started_as_rejection_definition_only
p4_m6_position_preserved
p4_m6_3_entry_deferral_non_execution_surface_reference_defined
p4_m6_2_entry_acceptance_non_evidence_surface_reference_defined
p4_m6_1_entry_preconditions_definition_surface_reference_defined
p4_m6_0_entry_boundary_contract_reference_defined
p4_m5_6_final_closure_handoff_reference_defined
p4_m5_5_closure_seal_reference_defined
p4_m5_4_cross_surface_alignment_map_reference_defined
static_entry_rejection_labels_defined
rejection_label_definition_surface_defined
rejection_surface_scope_defined
rejection_non_execution_boundary_defined
rejection_non_action_boundary_defined
rejection_non_denial_boundary_defined
rejection_non_punishment_boundary_defined
rejection_non_blocking_boundary_defined
rejection_non_approval_boundary_defined
rejection_non_authorization_boundary_defined
rejection_non_confirmation_boundary_defined
rejection_non_recommendation_boundary_defined
rejection_non_routing_boundary_defined
rejection_non_readiness_validation_boundary_defined
rejection_non_readiness_evidence_boundary_defined
rejection_non_validation_input_boundary_defined
rejection_non_record_boundary_defined
rejection_non_storage_boundary_defined
rejection_non_persistence_boundary_defined
rejection_non_mutation_boundary_defined
entry_rejection_surfaces_are_definition_only
entry_rejection_surfaces_are_static_labels_only
entry_rejection_surfaces_are_not_live_rejection_action
entry_rejection_surfaces_are_not_denial
entry_rejection_surfaces_are_not_punishment
entry_rejection_surfaces_are_not_blocking
entry_rejection_surfaces_are_not_approval
entry_rejection_surfaces_are_not_authorization
entry_rejection_surfaces_are_not_confirmation
entry_rejection_surfaces_are_not_recommendation
entry_rejection_surfaces_are_not_routing
entry_rejection_surfaces_are_not_execution
entry_rejection_surfaces_are_not_readiness_validation
entry_rejection_surfaces_are_not_readiness_evidence
entry_rejection_surfaces_are_not_validation_input
entry_rejection_surfaces_are_not_records
entry_rejection_surfaces_are_not_storage
entry_rejection_surfaces_are_not_persistence
entry_rejection_surfaces_are_not_mutation
rejection_validation_deferred
rejection_inference_deferred
rejection_scoring_deferred
rejection_verdict_deferred
rejection_action_deferred
rejection_enforcement_deferred
denial_deferred
punishment_deferred
blocking_deferred
approval_deferred
authorization_deferred
confirmation_deferred
recommendation_deferred
routing_deferred
execution_deferred
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
""".splitlines()
    if line
)


FALSE_STATUS_FLAGS = tuple(
    line
    for line in """
live_validation_enabled
entry_rejection_validation_enabled
entry_rejection_inference_enabled
entry_rejection_scoring_enabled
entry_rejection_verdict_enabled
entry_rejection_action_enabled
entry_rejection_enforcement_enabled
entry_rejection_denial_enabled
entry_rejection_punishment_enabled
entry_rejection_blocking_enabled
entry_rejection_approval_enabled
entry_rejection_authorization_enabled
entry_rejection_confirmation_enabled
entry_rejection_recommendation_enabled
entry_rejection_routing_enabled
entry_rejection_execution_enabled
entry_rejection_evidence_enabled
entry_rejection_validation_input_enabled
entry_rejection_record_creation_enabled
entry_rejection_storage_enabled
entry_rejection_persistence_enabled
entry_rejection_mutation_enabled
rejection_validation_enabled
rejection_inference_enabled
rejection_scoring_enabled
rejection_verdict_enabled
rejection_action_enabled
rejection_enforcement_enabled
rejection_denial_enabled
rejection_punishment_enabled
rejection_blocking_enabled
rejection_approval_enabled
rejection_authorization_enabled
rejection_confirmation_enabled
rejection_recommendation_enabled
rejection_routing_enabled
rejection_execution_enabled
rejection_evidence_collection_enabled
rejection_validation_input_enabled
rejection_record_creation_enabled
rejection_storage_enabled
rejection_persistence_enabled
rejection_mutation_enabled
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
implementation_rejection_validation_enabled
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
entry_action_enabled
entry_enforcement_enabled
entry_denial_enabled
entry_punishment_enabled
entry_blocking_enabled
entry_authorization_enabled
entry_confirmation_enabled
entry_approval_enabled
entry_recommendation_enabled
entry_routing_enabled
entry_execution_enabled
entry_record_creation_enabled
entry_storage_enabled
entry_persistence_enabled
entry_mutation_enabled
boundary_validation_enabled
boundary_inference_enabled
boundary_scoring_enabled
boundary_verdict_enabled
boundary_routing_enabled
boundary_execution_enabled
boundary_record_creation_enabled
boundary_storage_enabled
boundary_persistence_enabled
boundary_mutation_enabled
handoff_validation_enabled
handoff_inference_enabled
handoff_scoring_enabled
handoff_verdict_enabled
handoff_routing_enabled
handoff_execution_enabled
handoff_record_creation_enabled
handoff_storage_enabled
handoff_persistence_enabled
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
rejection_as_denial_enabled
rejection_as_punishment_enabled
rejection_as_blocking_enabled
rejection_as_approval_enabled
rejection_as_authorization_enabled
rejection_as_routing_enabled
rejection_as_execution_enabled
rejection_as_readiness_validation_enabled
rejection_as_readiness_evidence_enabled
rejection_as_validation_input_enabled
""".splitlines()
    if line
)


P4_M6_4_ENTRY_REJECTION_NON_EXECUTION_SURFACE_BOUNDARY = (
    "P4-M6.4 Entry Rejection Non-Execution Surface read-only "
    "definition-only p4-m6-4-entry-rejection-non-execution-surface-only "
    "entry-rejection-non-execution-surface-only "
    "static-rejection-labels-only non-execution-rejection-surface-only "
    "non-action-rejection-surface-only non-denial-rejection-surface-only "
    "non-punishment-rejection-surface-only "
    "non-blocking-rejection-surface-only "
    "non-approval-rejection-surface-only "
    "non-authorization-rejection-surface-only "
    "non-confirmation-rejection-surface-only "
    "non-recommendation-rejection-surface-only "
    "non-routing-rejection-surface-only "
    "non-validation-rejection-surface-only "
    "non-inference-rejection-surface-only "
    "non-scoring-rejection-surface-only "
    "non-verdict-rejection-surface-only "
    "non-record-rejection-surface-only "
    "non-storage-rejection-surface-only "
    "non-persistence-rejection-surface-only "
    "non-mutation-rejection-surface-only "
    "implementation-corridor-not-started-boundary-only "
    "api-implementation-disabled mcp-implementation-disabled "
    "connector-implementation-disabled agent-auto-call-disabled "
    "network-access-disabled external-system-integration-disabled "
    "declaration-only inspection-only. "
    + " ".join(f"{phrase}." for phrase in BOUNDARY_PHRASE_LINES)
)


_FIELD_IDS = tuple(
    line
    for line in """
p4-m6-4-entry-rejection-non-execution-surface-id
p4-m6-4-entry-rejection-non-execution-surface-phase
p4-m6-4-entry-rejection-non-execution-surface-mode
p4-m6-4-entry-rejection-non-execution-surface-p4-m6-position
p4-m6-4-entry-rejection-non-execution-surface-direct-prior-p4-m6-3-entry-deferral-non-execution-surface-reference
p4-m6-4-entry-rejection-non-execution-surface-inherited-p4-m6-2-entry-acceptance-non-evidence-surface-reference
p4-m6-4-entry-rejection-non-execution-surface-inherited-p4-m6-1-entry-preconditions-definition-surface-reference
p4-m6-4-entry-rejection-non-execution-surface-inherited-p4-m6-0-entry-boundary-contract-reference
p4-m6-4-entry-rejection-non-execution-surface-static-rejection-label-scope
p4-m6-4-entry-rejection-non-execution-surface-rejection-label-definition-surface
p4-m6-4-entry-rejection-non-execution-surface-rejection-non-execution-boundary
p4-m6-4-entry-rejection-non-execution-surface-rejection-non-action-boundary
p4-m6-4-entry-rejection-non-execution-surface-rejection-non-denial-punishment-blocking-boundary
p4-m6-4-entry-rejection-non-execution-surface-rejection-non-approval-authorization-confirmation-boundary
p4-m6-4-entry-rejection-non-execution-surface-rejection-non-recommendation-routing-boundary
p4-m6-4-entry-rejection-non-execution-surface-rejection-non-readiness-validation-boundary
p4-m6-4-entry-rejection-non-execution-surface-rejection-non-readiness-evidence-boundary
p4-m6-4-entry-rejection-non-execution-surface-rejection-non-validation-inference-scoring-verdict-boundary
p4-m6-4-entry-rejection-non-execution-surface-rejection-non-record-storage-persistence-mutation-boundary
p4-m6-4-entry-rejection-non-execution-surface-implementation-corridor-v7-productization-ui-operator-console-deferred-boundary
p4-m6-4-entry-rejection-non-execution-surface-api-mcp-connector-agent-network-external-integration-non-start-boundary
p4-m6-4-entry-rejection-non-execution-surface-static-rejection-and-validation-authorization-routing-execution-record-storage-mutation-semantics-disabled
p4-m6-4-entry-rejection-non-execution-surface-final-non-execution-definition-boundary
""".splitlines()
    if line
)


def _field_purpose(field_id: str) -> str:
    return (
        f"Defines {field_id} as "
        f"{P4_M6_4_ENTRY_REJECTION_NON_EXECUTION_SURFACE_BOUNDARY}"
    )


_P4_M6_4_ENTRY_REJECTION_NON_EXECUTION_SURFACE_FIELDS = tuple(
    P4M64EntryRejectionNonExecutionSurfaceField(
        index,
        field_id,
        f"P4-M6.4 Entry Rejection Non-Execution Surface Field {index}",
        _field_purpose(field_id),
        "p4-m6-4-entry-rejection-non-execution-surface-category",
        (
            "no rejection validation semantics; no rejection inference semantics; "
            "no rejection scoring semantics; no rejection verdict semantics; no "
            "rejection action semantics; no rejection enforcement semantics; no "
            "denial semantics; no punishment semantics; no blocking semantics; no "
            "approval semantics; no authorization semantics; no confirmation "
            "semantics; no recommendation semantics; no routing semantics; no "
            "execution semantics; no readiness evidence semantics; no validation "
            "input semantics; no record creation semantics; no storage semantics; "
            "no persistence semantics; no mutation semantics; no API implementation "
            "semantics; no MCP implementation semantics; no Connector "
            "implementation semantics; no API client semantics; no MCP client "
            "semantics; no MCP server semantics; no MCP transport semantics; no "
            "MCP session semantics; no Connector client semantics; no Connector "
            "adapter semantics; no Connector runtime semantics; no Agent auto-call "
            "semantics; no external system integration semantics; no network access "
            "semantics; no live API endpoint probe semantics; no live MCP server "
            "probe semantics; no live provider probe semantics; no live provider "
            "discovery semantics; no OAuth flow semantics; no credential use "
            "semantics; no secret access semantics; no secret inspection semantics; "
            "no API call semantics; no MCP tool call semantics; no MCP resource "
            "access semantics; no MCP prompt execution semantics; no connector data "
            "fetch semantics; no connector data write semantics; no connector "
            "mutation semantics; no authentication testing semantics; no "
            "authorization testing semantics; no schema validation semantics; no "
            "readiness validation semantics; no readiness inference semantics; no "
            "readiness scoring semantics; no readiness verdict semantics; no "
            "implementation start semantics; no v7 semantics; no productization "
            "semantics; no UI semantics; no Operator Console semantics"
        ),
    )
    for index, field_id in enumerate(_FIELD_IDS, start=1)
)


def list_p4_m6_4_entry_rejection_non_execution_surface_fields() -> (
    tuple[P4M64EntryRejectionNonExecutionSurfaceField, ...]
):
    return _P4_M6_4_ENTRY_REJECTION_NON_EXECUTION_SURFACE_FIELDS


def p4_m6_4_entry_rejection_non_execution_surface_field_ids() -> tuple[str, ...]:
    return tuple(
        field.field_id
        for field in list_p4_m6_4_entry_rejection_non_execution_surface_fields()
    )


def render_p4_m6_4_entry_rejection_non_execution_surface_markdown(
    fields: Sequence[P4M64EntryRejectionNonExecutionSurfaceField] | None = None,
) -> str:
    field_values = (
        tuple(fields)
        if fields is not None
        else list_p4_m6_4_entry_rejection_non_execution_surface_fields()
    )
    status = p4_m6_4_entry_rejection_non_execution_surface_report()
    lines = [
        "# P4-M6.4 Entry Rejection Non-Execution Surface",
        "",
        "P4-M6.4 Entry Rejection Non-Execution Surface.",
        "",
    ]
    for phrase in BOUNDARY_PHRASE_LINES:
        lines.extend([f"{phrase}.", ""])
    for prior_layer in DIRECT_PRIOR_DEFINITION_LAYER_REFERENCES:
        lines.extend([f"{prior_layer} remains a direct referenced definition layer.", ""])
    for prior_layer in INHERITED_PRIOR_DEFINITION_LAYER_REFERENCES:
        lines.extend(
            [f"{prior_layer} remains an inherited referenced definition layer.", ""]
        )
    lines.extend(
        [
            P4_M6_4_ENTRY_REJECTION_NON_EXECUTION_SURFACE_BOUNDARY,
            "",
            "## Status Report",
            "",
        ]
    )
    for key, value in status.items():
        lines.append(f"- {key}: {value}")
    lines.extend(
        [
            "",
            "## P4-M6.4 Entry Rejection Non-Execution Surface Fields",
            "",
        ]
    )
    for field in field_values:
        lines.extend(
            [
                f"### {field.field_order}. {field.field_id}",
                "",
                f"- Field name: {field.field_name}",
                f"- Field purpose: {field.field_purpose}",
                "- P4-M6.4 entry rejection non-execution surface category: "
                f"{field.p4_m6_4_entry_rejection_non_execution_surface_category}",
                "- P4-M6.4 entry rejection non-execution surface semantics disabled: "
                f"{field.p4_m6_4_entry_rejection_non_execution_surface_semantics_disabled}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def p4_m6_4_entry_rejection_non_execution_surface_as_dicts() -> (
    tuple[dict[str, object], ...]
):
    return tuple(
        asdict(field)
        for field in list_p4_m6_4_entry_rejection_non_execution_surface_fields()
    )


def p4_m6_4_entry_rejection_non_execution_surface_report() -> dict[str, object]:
    status: dict[str, object] = {
        "phase": "P4-M6.4",
        "feature": "Entry Rejection Non-Execution Surface",
        "mode": "read-only",
        "boundary": P4_M6_4_ENTRY_REJECTION_NON_EXECUTION_SURFACE_BOUNDARY,
        "package_version": P4_M6_4_PACKAGE_VERSION,
        "p4_m6_4_entry_rejection_non_execution_surface_field_count": len(_FIELD_IDS),
        "referenced_p4_m6_3_entry_deferral_non_execution_surface_field_count": len(
            p4_m6_3_entry_deferral_non_execution_surface_field_ids()
        ),
        "referenced_p4_m6_2_entry_acceptance_non_evidence_surface_field_count": len(
            p4_m6_2_entry_acceptance_non_evidence_surface_field_ids()
        ),
        "referenced_p4_m6_1_entry_preconditions_definition_surface_field_count": len(
            p4_m6_1_entry_preconditions_definition_surface_field_ids()
        ),
        "referenced_p4_m6_0_next_corridor_entry_boundary_contract_field_count": len(
            p4_m6_0_next_corridor_entry_boundary_contract_field_ids()
        ),
        "referenced_p4_m5_6_final_closure_handoff_next_corridor_non_start_index_field_count": len(
            p4_m5_6_final_closure_handoff_next_corridor_non_start_index_field_ids()
        ),
        "referenced_p4_m5_5_readiness_audit_closure_non_start_boundary_seal_field_count": len(
            p4_m5_5_readiness_audit_closure_non_start_boundary_seal_field_ids()
        ),
        "referenced_p4_m5_4_cross_surface_alignment_map_field_count": len(
            p4_m5_4_cross_surface_alignment_map_field_ids()
        ),
    }
    status.update({flag: True for flag in TRUE_STATUS_FLAGS})
    status.update({flag: False for flag in FALSE_STATUS_FLAGS})
    return status
