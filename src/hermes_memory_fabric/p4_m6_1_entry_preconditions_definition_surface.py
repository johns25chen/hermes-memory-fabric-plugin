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


P4_M6_1_PACKAGE_VERSION = "6.16.0"


@dataclass(frozen=True)
class P4M61EntryPreconditionsDefinitionSurfaceField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    p4_m6_1_entry_preconditions_definition_surface_category: str
    p4_m6_1_entry_preconditions_definition_surface_semantics_disabled: str


DIRECT_PRIOR_DEFINITION_LAYER_REFERENCES = (
    "P4-M6.0 Next Corridor Entry Boundary Contract",
)

INHERITED_PRIOR_DEFINITION_LAYER_REFERENCES = (
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
P4-M6.1
Entry Preconditions Definition Surface
P4-M6.1 Entry Preconditions Definition Surface
read-only
definition-only
p4-m6-1-entry-preconditions-definition-surface-only
entry-preconditions-definition-surface-only
static-precondition-labels-only
non-evidence-precondition-surface-only
non-validation-precondition-surface-only
non-inference-precondition-surface-only
non-scoring-precondition-surface-only
non-verdict-precondition-surface-only
non-authorization-precondition-surface-only
non-confirmation-precondition-surface-only
non-approval-precondition-surface-only
non-routing-precondition-surface-only
non-execution-precondition-surface-only
non-record-precondition-surface-only
non-storage-precondition-surface-only
non-mutation-precondition-surface-only
implementation-corridor-not-started-boundary-only
api-implementation-disabled
mcp-implementation-disabled
connector-implementation-disabled
agent-auto-call-disabled
network-access-disabled
external-system-integration-disabled
declaration-only
inspection-only
P4-M6.1 defines only static entry precondition surfaces
P4-M6.1 does not validate preconditions
P4-M6.1 does not infer preconditions
P4-M6.1 does not score preconditions
P4-M6.1 does not produce precondition verdict
P4-M6.1 does not treat preconditions as readiness evidence
P4-M6.1 does not treat preconditions as validation inputs
P4-M6.1 does not authorize entry
P4-M6.1 does not confirm entry
P4-M6.1 does not approve entry
P4-M6.1 does not recommend entry
P4-M6.1 does not route implementation
P4-M6.1 does not execute
P4-M6.1 does not create records
P4-M6.1 does not create storage
P4-M6.1 does not persist state
P4-M6.1 does not mutate memory
P4-M6.1 does not start implementation corridor
P4-M6.1 is not API implementation
P4-M6.1 is not MCP implementation
P4-M6.1 is not Connector implementation
P4-M6.1 is not API client implementation
P4-M6.1 is not MCP client implementation
P4-M6.1 is not MCP server implementation
P4-M6.1 is not MCP transport implementation
P4-M6.1 is not MCP session implementation
P4-M6.1 is not Connector client implementation
P4-M6.1 is not Connector adapter implementation
P4-M6.1 is not Connector runtime implementation
P4-M6.1 is not Agent auto-call
P4-M6.1 is not external system integration
P4-M6.1 is not network access
P4-M6.1 is not live API endpoint probing
P4-M6.1 is not live MCP server probing
P4-M6.1 is not live provider probing
P4-M6.1 is not live provider discovery
P4-M6.1 is not OAuth flow
P4-M6.1 is not credential use
P4-M6.1 is not secret access
P4-M6.1 is not secret inspection
P4-M6.1 is not API call
P4-M6.1 is not MCP tool call
P4-M6.1 is not MCP resource access
P4-M6.1 is not MCP prompt execution
P4-M6.1 is not connector data fetch
P4-M6.1 is not connector data write
P4-M6.1 is not connector mutation
P4-M6.1 is not authentication testing
P4-M6.1 is not authorization testing
P4-M6.1 is not schema validation
P4-M6.0 Next Corridor Entry Boundary Contract remains the direct prior entry boundary reference
P4-M5.6 Final Closure Handoff / Next Corridor Non-Start Index remains an inherited final closure handoff reference
P4-M5.5 Readiness Audit Closure / Non-Start Boundary Seal remains an inherited closure seal reference
P4-M5.4 API / MCP / Connector Cross-Surface Alignment Map remains an inherited cross-surface alignment map reference
static entry precondition labels are definition-only
repository state precondition label is definition-only
version lock precondition label is definition-only
main cleanliness precondition label is definition-only
no uv.lock precondition label is definition-only
no repo .codex precondition label is definition-only
no tag precondition label is definition-only
command allowlist precondition label is definition-only
boundary phrase precondition label is definition-only
field and status shape precondition label is definition-only
entry precondition surfaces are not readiness evidence
entry precondition surfaces are not validation inputs
entry precondition surfaces are not authorization
entry precondition surfaces are not confirmation
entry precondition surfaces are not approval
entry precondition surfaces are not recommendation
entry precondition surfaces are not routing
entry precondition surfaces are not execution
entry precondition surfaces are not records
entry precondition surfaces are not storage
entry precondition surfaces are not persistence
entry precondition surfaces are not mutation
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
no precondition validation
no precondition inference
no precondition scoring
no precondition verdict
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
p4_m6_1_entry_preconditions_definition_surface_started
p4_m6_1_entry_preconditions_definition_surface_only
entry_preconditions_definition_surface_only
static_precondition_labels_only
non_evidence_precondition_surface_only
non_validation_precondition_surface_only
non_inference_precondition_surface_only
non_scoring_precondition_surface_only
non_verdict_precondition_surface_only
non_authorization_precondition_surface_only
non_confirmation_precondition_surface_only
non_approval_precondition_surface_only
non_routing_precondition_surface_only
non_execution_precondition_surface_only
non_record_precondition_surface_only
non_storage_precondition_surface_only
non_mutation_precondition_surface_only
implementation_corridor_not_started_boundary_only
api_implementation_disabled
mcp_implementation_disabled
connector_implementation_disabled
agent_auto_call_disabled
network_access_disabled
external_system_integration_disabled
declaration_only
inspection_only
p4_m6_1_started_as_precondition_definition_only
p4_m6_position_preserved
p4_m6_0_entry_boundary_contract_reference_defined
p4_m5_6_final_closure_handoff_reference_defined
p4_m5_5_closure_seal_reference_defined
p4_m5_4_cross_surface_alignment_map_reference_defined
static_entry_precondition_labels_defined
repository_state_precondition_label_defined
version_lock_precondition_label_defined
main_cleanliness_precondition_label_defined
no_uv_lock_precondition_label_defined
no_repo_codex_precondition_label_defined
no_tag_precondition_label_defined
command_allowlist_precondition_label_defined
boundary_phrase_precondition_label_defined
field_and_status_shape_precondition_label_defined
entry_precondition_surfaces_are_definition_only
entry_precondition_surfaces_are_static_labels_only
entry_precondition_surfaces_are_not_readiness_evidence
entry_precondition_surfaces_are_not_validation_inputs
entry_precondition_surfaces_are_not_authorization
entry_precondition_surfaces_are_not_confirmation
entry_precondition_surfaces_are_not_approval
entry_precondition_surfaces_are_not_recommendation
entry_precondition_surfaces_are_not_routing
entry_precondition_surfaces_are_not_execution
entry_precondition_surfaces_are_not_records
entry_precondition_surfaces_are_not_storage
entry_precondition_surfaces_are_not_persistence
entry_precondition_surfaces_are_not_mutation
precondition_validation_deferred
precondition_inference_deferred
precondition_scoring_deferred
precondition_verdict_deferred
precondition_authorization_deferred
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


FALSE_STATUS_FLAGS = tuple(
    line
    for line in """
live_validation_enabled
entry_precondition_validation_enabled
entry_precondition_inference_enabled
entry_precondition_scoring_enabled
entry_precondition_verdict_enabled
entry_precondition_authorization_enabled
entry_precondition_confirmation_enabled
entry_precondition_approval_enabled
entry_precondition_recommendation_enabled
entry_precondition_routing_enabled
entry_precondition_execution_enabled
entry_precondition_record_creation_enabled
entry_precondition_storage_enabled
entry_precondition_persistence_enabled
entry_precondition_mutation_enabled
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
implementation_preconditions_validation_enabled
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
mvp_started
deploy_started
full_memory_graph_started
version_bump_enabled
""".splitlines()
    if line
)


P4_M6_1_ENTRY_PRECONDITIONS_DEFINITION_SURFACE_BOUNDARY = (
    "P4-M6.1 Entry Preconditions Definition Surface read-only "
    "definition-only p4-m6-1-entry-preconditions-definition-surface-only "
    "entry-preconditions-definition-surface-only "
    "static-precondition-labels-only non-evidence-precondition-surface-only "
    "non-validation-precondition-surface-only "
    "non-inference-precondition-surface-only "
    "non-scoring-precondition-surface-only "
    "non-verdict-precondition-surface-only "
    "non-authorization-precondition-surface-only "
    "non-confirmation-precondition-surface-only "
    "non-approval-precondition-surface-only "
    "non-routing-precondition-surface-only "
    "non-execution-precondition-surface-only "
    "non-record-precondition-surface-only "
    "non-storage-precondition-surface-only "
    "non-mutation-precondition-surface-only "
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
p4-m6-1-entry-preconditions-definition-surface-id
p4-m6-1-entry-preconditions-definition-surface-phase
p4-m6-1-entry-preconditions-definition-surface-mode
p4-m6-1-entry-preconditions-definition-surface-p4-m6-position
p4-m6-1-entry-preconditions-definition-surface-direct-prior-p4-m6-0-entry-boundary-contract-reference
p4-m6-1-entry-preconditions-definition-surface-inherited-p4-m5-final-closure-handoff-reference
p4-m6-1-entry-preconditions-definition-surface-static-precondition-label-scope
p4-m6-1-entry-preconditions-definition-surface-repository-state-precondition-label
p4-m6-1-entry-preconditions-definition-surface-version-lock-precondition-label
p4-m6-1-entry-preconditions-definition-surface-main-cleanliness-precondition-label
p4-m6-1-entry-preconditions-definition-surface-no-uv-lock-precondition-label
p4-m6-1-entry-preconditions-definition-surface-no-repo-codex-precondition-label
p4-m6-1-entry-preconditions-definition-surface-no-tag-precondition-label
p4-m6-1-entry-preconditions-definition-surface-command-allowlist-precondition-label
p4-m6-1-entry-preconditions-definition-surface-boundary-phrase-precondition-label
p4-m6-1-entry-preconditions-definition-surface-field-and-status-shape-precondition-label
p4-m6-1-entry-preconditions-definition-surface-non-evidence-boundary
p4-m6-1-entry-preconditions-definition-surface-non-validation-non-inference-non-scoring-non-verdict-boundary
p4-m6-1-entry-preconditions-definition-surface-non-authorization-non-confirmation-non-approval-boundary
p4-m6-1-entry-preconditions-definition-surface-non-routing-non-execution-boundary
p4-m6-1-entry-preconditions-definition-surface-non-record-non-storage-non-persistence-non-mutation-boundary
p4-m6-1-entry-preconditions-definition-surface-implementation-corridor-v7-productization-ui-operator-console-deferred-boundary
p4-m6-1-entry-preconditions-definition-surface-static-precondition-and-validation-inference-scoring-verdict-authorization-routing-execution-record-storage-mutation-semantics-disabled
""".splitlines()
    if line
)


def _field_purpose(field_id: str) -> str:
    return (
        f"Defines {field_id} as "
        f"{P4_M6_1_ENTRY_PRECONDITIONS_DEFINITION_SURFACE_BOUNDARY}"
    )


_P4_M6_1_ENTRY_PRECONDITIONS_DEFINITION_SURFACE_FIELDS = tuple(
    P4M61EntryPreconditionsDefinitionSurfaceField(
        index,
        field_id,
        f"P4-M6.1 Entry Preconditions Definition Surface Field {index}",
        _field_purpose(field_id),
        "p4-m6-1-entry-preconditions-definition-surface-category",
        (
            "no precondition validation semantics; no precondition inference "
            "semantics; no precondition scoring semantics; no precondition "
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


def list_p4_m6_1_entry_preconditions_definition_surface_fields() -> (
    tuple[P4M61EntryPreconditionsDefinitionSurfaceField, ...]
):
    return _P4_M6_1_ENTRY_PRECONDITIONS_DEFINITION_SURFACE_FIELDS


def p4_m6_1_entry_preconditions_definition_surface_field_ids() -> tuple[str, ...]:
    return tuple(
        field.field_id
        for field in list_p4_m6_1_entry_preconditions_definition_surface_fields()
    )


def render_p4_m6_1_entry_preconditions_definition_surface_markdown(
    fields: Sequence[P4M61EntryPreconditionsDefinitionSurfaceField] | None = None,
) -> str:
    field_values = (
        tuple(fields)
        if fields is not None
        else list_p4_m6_1_entry_preconditions_definition_surface_fields()
    )
    status = p4_m6_1_entry_preconditions_definition_surface_report()
    lines = [
        "# P4-M6.1 Entry Preconditions Definition Surface",
        "",
        "P4-M6.1 Entry Preconditions Definition Surface.",
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
            P4_M6_1_ENTRY_PRECONDITIONS_DEFINITION_SURFACE_BOUNDARY,
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
            "## P4-M6.1 Entry Preconditions Definition Surface Fields",
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
                "- P4-M6.1 entry preconditions definition surface category: "
                f"{field.p4_m6_1_entry_preconditions_definition_surface_category}",
                "- P4-M6.1 entry preconditions definition surface semantics disabled: "
                f"{field.p4_m6_1_entry_preconditions_definition_surface_semantics_disabled}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def p4_m6_1_entry_preconditions_definition_surface_as_dicts() -> (
    tuple[dict[str, object], ...]
):
    return tuple(
        asdict(field)
        for field in list_p4_m6_1_entry_preconditions_definition_surface_fields()
    )


def p4_m6_1_entry_preconditions_definition_surface_report() -> dict[str, object]:
    status: dict[str, object] = {
        "phase": "P4-M6.1",
        "feature": "Entry Preconditions Definition Surface",
        "mode": "read-only",
        "boundary": P4_M6_1_ENTRY_PRECONDITIONS_DEFINITION_SURFACE_BOUNDARY,
        "package_version": P4_M6_1_PACKAGE_VERSION,
        "p4_m6_1_entry_preconditions_definition_surface_field_count": len(
            _FIELD_IDS
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
    status["tag_creation_enabled"] = False
    return status
