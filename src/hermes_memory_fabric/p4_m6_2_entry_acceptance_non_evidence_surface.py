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


P4_M6_2_PACKAGE_VERSION = "6.16.0"


@dataclass(frozen=True)
class P4M62EntryAcceptanceNonEvidenceSurfaceField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    p4_m6_2_entry_acceptance_non_evidence_surface_category: str
    p4_m6_2_entry_acceptance_non_evidence_surface_semantics_disabled: str


DIRECT_PRIOR_DEFINITION_LAYER_REFERENCES = (
    "P4-M6.1 Entry Preconditions Definition Surface",
)

INHERITED_PRIOR_DEFINITION_LAYER_REFERENCES = (
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


TRUE_STATUS_FLAGS = tuple(
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
""".splitlines()
    if line
)


SUPPLEMENTAL_TRUE_STATUS_FLAGS = tuple(
    line
    for line in """
operator_console_deferred
command_returns_before_store_creation
no_workspace_storage_created
no_memory_mutation_surface_defined
""".splitlines()
    if line
)


FALSE_STATUS_FLAGS = tuple(
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


P4_M6_2_ENTRY_ACCEPTANCE_NON_EVIDENCE_SURFACE_BOUNDARY = (
    "P4-M6.2 Entry Acceptance Non-Evidence Surface read-only "
    "definition-only p4-m6-2-entry-acceptance-non-evidence-surface-only "
    "entry-acceptance-non-evidence-surface-only "
    "static-acceptance-labels-only non-evidence-acceptance-surface-only "
    "non-validation-input-acceptance-surface-only "
    "non-validation-acceptance-surface-only "
    "non-inference-acceptance-surface-only "
    "non-scoring-acceptance-surface-only "
    "non-verdict-acceptance-surface-only "
    "non-authorization-acceptance-surface-only "
    "non-confirmation-acceptance-surface-only "
    "non-approval-acceptance-surface-only "
    "non-recommendation-acceptance-surface-only "
    "non-routing-acceptance-surface-only "
    "non-execution-acceptance-surface-only "
    "non-record-acceptance-surface-only "
    "non-storage-acceptance-surface-only "
    "non-persistence-acceptance-surface-only "
    "non-mutation-acceptance-surface-only "
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


def _field_purpose(field_id: str) -> str:
    return (
        f"Defines {field_id} as "
        f"{P4_M6_2_ENTRY_ACCEPTANCE_NON_EVIDENCE_SURFACE_BOUNDARY}"
    )


_P4_M6_2_ENTRY_ACCEPTANCE_NON_EVIDENCE_SURFACE_FIELDS = tuple(
    P4M62EntryAcceptanceNonEvidenceSurfaceField(
        index,
        field_id,
        f"P4-M6.2 Entry Acceptance Non-Evidence Surface Field {index}",
        _field_purpose(field_id),
        "p4-m6-2-entry-acceptance-non-evidence-surface-category",
        (
            "no acceptance validation semantics; no acceptance inference "
            "semantics; no acceptance scoring semantics; no acceptance "
            "verdict semantics; no readiness evidence semantics; no validation "
            "input semantics; no authorization semantics; no confirmation "
            "semantics; no approval semantics; no recommendation semantics; no "
            "API implementation semantics; no MCP implementation semantics; no "
            "Connector implementation semantics; no API client semantics; no MCP "
            "client semantics; no MCP server semantics; no MCP transport "
            "semantics; no MCP session semantics; no Connector client semantics; "
            "no Connector adapter semantics; no Connector runtime semantics; no "
            "Agent auto-call semantics; no external system integration semantics; "
            "no network access semantics; no live API endpoint probe semantics; "
            "no live MCP server probe semantics; no live provider probe semantics; "
            "no live provider discovery semantics; no OAuth flow semantics; no "
            "credential use semantics; no secret access semantics; no secret "
            "inspection semantics; no API call semantics; no MCP tool call "
            "semantics; no MCP resource access semantics; no MCP prompt execution "
            "semantics; no connector data fetch semantics; no connector data write "
            "semantics; no connector mutation semantics; no authentication testing "
            "semantics; no authorization testing semantics; no schema validation "
            "semantics; no readiness validation semantics; no readiness inference "
            "semantics; no readiness scoring semantics; no readiness verdict "
            "semantics; no routing semantics; no execution semantics; no record "
            "creation semantics; no storage semantics; no persistence semantics; "
            "no mutation semantics; no implementation start semantics; no v7 "
            "semantics; no productization semantics; no UI semantics; no Operator "
            "Console semantics"
        ),
    )
    for index, field_id in enumerate(_FIELD_IDS, start=1)
)


def list_p4_m6_2_entry_acceptance_non_evidence_surface_fields() -> (
    tuple[P4M62EntryAcceptanceNonEvidenceSurfaceField, ...]
):
    return _P4_M6_2_ENTRY_ACCEPTANCE_NON_EVIDENCE_SURFACE_FIELDS


def p4_m6_2_entry_acceptance_non_evidence_surface_field_ids() -> tuple[str, ...]:
    return tuple(
        field.field_id
        for field in list_p4_m6_2_entry_acceptance_non_evidence_surface_fields()
    )


def render_p4_m6_2_entry_acceptance_non_evidence_surface_markdown(
    fields: Sequence[P4M62EntryAcceptanceNonEvidenceSurfaceField] | None = None,
) -> str:
    field_values = (
        tuple(fields)
        if fields is not None
        else list_p4_m6_2_entry_acceptance_non_evidence_surface_fields()
    )
    status = p4_m6_2_entry_acceptance_non_evidence_surface_report()
    lines = [
        "# P4-M6.2 Entry Acceptance Non-Evidence Surface",
        "",
        "P4-M6.2 Entry Acceptance Non-Evidence Surface.",
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
            P4_M6_2_ENTRY_ACCEPTANCE_NON_EVIDENCE_SURFACE_BOUNDARY,
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
            "## P4-M6.2 Entry Acceptance Non-Evidence Surface Fields",
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
                "- P4-M6.2 entry acceptance non-evidence surface category: "
                f"{field.p4_m6_2_entry_acceptance_non_evidence_surface_category}",
                "- P4-M6.2 entry acceptance non-evidence surface semantics disabled: "
                f"{field.p4_m6_2_entry_acceptance_non_evidence_surface_semantics_disabled}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def p4_m6_2_entry_acceptance_non_evidence_surface_as_dicts() -> (
    tuple[dict[str, object], ...]
):
    return tuple(
        asdict(field)
        for field in list_p4_m6_2_entry_acceptance_non_evidence_surface_fields()
    )



# P4-M6.2 strict counted boolean status alignment.
# true_flags is locked at 94, so supplemental true flags must not appear
# as status booleans.
SUPPLEMENTAL_TRUE_STATUS_FLAGS = ()
ALL_TRUE_STATUS_FLAGS = TRUE_STATUS_FLAGS

def p4_m6_2_entry_acceptance_non_evidence_surface_report() -> dict[str, object]:
    status: dict[str, object] = {
        "phase": "P4-M6.2",
        "feature": "Entry Acceptance Non-Evidence Surface",
        "mode": "read-only",
        "boundary": P4_M6_2_ENTRY_ACCEPTANCE_NON_EVIDENCE_SURFACE_BOUNDARY,
        "package_version": P4_M6_2_PACKAGE_VERSION,
        "p4_m6_2_entry_acceptance_non_evidence_surface_field_count": len(_FIELD_IDS),
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
    status.update({flag: True for flag in SUPPLEMENTAL_TRUE_STATUS_FLAGS})
    status.update({flag: False for flag in FALSE_STATUS_FLAGS})
    # Keep the public boolean status set exactly aligned with TRUE_STATUS_FLAGS.
    # These labels remain documented as boundary language where needed, but they are
    # not counted status booleans for P4-M6.2 because true_flags is locked at 94.
    for key in (
        "command_returns_before_store_creation",
        "no_workspace_storage_created",
        "no_memory_mutation_surface_defined",
        "operator_console_deferred",
    ):
        status.pop(key, None)

    return status
