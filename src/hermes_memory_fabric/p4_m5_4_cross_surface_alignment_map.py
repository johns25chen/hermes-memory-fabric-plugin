from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence

from .p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract import (
    p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_field_ids,
)
from .p4_m5_1_api_readiness_audit_surface_map import (
    p4_m5_1_api_readiness_audit_surface_map_field_ids,
)
from .p4_m5_2_mcp_readiness_audit_surface_map import (
    p4_m5_2_mcp_readiness_audit_surface_map_field_ids,
)
from .p4_m5_3_connector_readiness_audit_surface_map import (
    p4_m5_3_connector_readiness_audit_surface_map_field_ids,
)


P4_M5_4_PACKAGE_VERSION = "6.16.0"


@dataclass(frozen=True)
class P4M54CrossSurfaceAlignmentMapField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    p4_m5_4_cross_surface_alignment_map_category: str
    p4_m5_4_cross_surface_alignment_map_semantics_disabled: str


DIRECT_PRIOR_DEFINITION_LAYER_REFERENCES = (
    "P4-M5.3 Connector Readiness Audit Surface Map",
)

INHERITED_PRIOR_DEFINITION_LAYER_REFERENCES = (
    "P4-M5.2 MCP Readiness Audit Surface Map",
    "P4-M5.1 API Readiness Audit Surface Map",
    "P4-M5.0 API / MCP / Connector Readiness Audit Boundary Contract",
    "P4-M4-FC.6 P4-M4 Final Closure Roadmap Alignment Snapshot",
    "P4-M4-FC.5 P4-M4 Final Closure Boundary Freeze Index",
    "P4-M4-FC.4 P4-M4 Final Closure Non-Start Bridge Index",
    "P4-M4-FC.3 P4-M4 Final Closure Transition Readiness Non-Start Index",
)


BOUNDARY_PHRASE_LINES = tuple(
    line
    for line in """
P4-M5.4
API / MCP / Connector Cross-Surface Alignment Map
P4-M5.4 API / MCP / Connector Cross-Surface Alignment Map
read-only
definition-only
p4-m5-4-cross-surface-alignment-map-only
api-mcp-connector-cross-surface-alignment-map-only
cross-surface-alignment-non-validation-boundary-only
cross-surface-alignment-non-inference-boundary-only
cross-surface-alignment-non-scoring-boundary-only
cross-surface-alignment-non-verdict-boundary-only
cross-surface-alignment-non-routing-boundary-only
cross-surface-alignment-non-execution-boundary-only
cross-surface-alignment-non-record-boundary-only
cross-surface-alignment-non-storage-boundary-only
cross-surface-alignment-non-mutation-boundary-only
api-implementation-disabled
mcp-implementation-disabled
connector-implementation-disabled
agent-auto-call-disabled
network-access-disabled
external-system-integration-disabled
declaration-only
inspection-only
P4-M5.4 defines API / MCP / Connector cross-surface alignment surfaces only
P4-M5.4 is not API implementation
P4-M5.4 is not MCP implementation
P4-M5.4 is not Connector implementation
P4-M5.4 is not API client implementation
P4-M5.4 is not MCP client implementation
P4-M5.4 is not MCP server implementation
P4-M5.4 is not MCP transport implementation
P4-M5.4 is not MCP session implementation
P4-M5.4 is not Connector client implementation
P4-M5.4 is not Connector adapter implementation
P4-M5.4 is not Connector runtime implementation
P4-M5.4 is not Agent auto-call
P4-M5.4 is not external system integration
P4-M5.4 is not network access
P4-M5.4 is not live API endpoint probing
P4-M5.4 is not live MCP server probing
P4-M5.4 is not live provider probing
P4-M5.4 is not OAuth flow
P4-M5.4 is not credential use
P4-M5.4 is not secret access
P4-M5.4 is not secret inspection
P4-M5.4 is not API call
P4-M5.4 is not MCP tool call
P4-M5.4 is not MCP resource access
P4-M5.4 is not MCP prompt execution
P4-M5.4 is not connector data fetch
P4-M5.4 is not connector data write
P4-M5.4 is not connector mutation
P4-M5.4 is not authentication testing
P4-M5.4 is not authorization testing
P4-M5.4 is not schema validation
P4-M5.4 does not perform readiness validation
P4-M5.4 does not infer readiness
P4-M5.4 does not score readiness
P4-M5.4 does not produce readiness verdict
P4-M5.4 does not route implementation
P4-M5.4 does not execute
P4-M5.4 does not create readiness records
P4-M5.4 does not create storage
P4-M5.4 does not persist state
P4-M5.4 does not mutate memory
P4-M4.x remains cross-project memory governance preparation
P4-M5.x remains API / MCP / Connector readiness audit
P4-M5.3 Connector Readiness Audit Surface Map remains the direct prior Connector surface map reference
P4-M5.2 MCP Readiness Audit Surface Map remains an inherited MCP surface map reference
P4-M5.1 API Readiness Audit Surface Map remains an inherited API surface map reference
P4-M5.0 API / MCP / Connector Readiness Audit Boundary Contract remains the inherited prior boundary contract reference
API / MCP / Connector identity alignment surface is definition-only
API / MCP / Connector boundary model alignment surface is definition-only
API / MCP / Connector capability declaration alignment surface is definition-only
API / MCP / Connector operation inventory alignment surface is definition-only
API / MCP / Connector input contract alignment surface is definition-only
API / MCP / Connector output contract alignment surface is definition-only
API / MCP / Connector authentication boundary alignment surface is definition-only
API / MCP / Connector authorization boundary alignment surface is definition-only
API / MCP / Connector access control permission scope alignment surface is definition-only
API / MCP / Connector error contract alignment surface is definition-only
API / MCP / Connector timeout retry rate limit alignment surface is definition-only
API / MCP / Connector observability audit logging alignment surface is definition-only
API / MCP / Connector secret credential boundary alignment surface is definition-only
API / MCP / Connector data resource classification alignment surface is definition-only
API / MCP / Connector non-execution semantics alignment surface is definition-only
Cross-surface alignment surfaces are not readiness evidence
Cross-surface alignment surfaces are not validation inputs
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
p4_m5_4_cross_surface_alignment_map_started
p4_m5_4_cross_surface_alignment_map_only
api_mcp_connector_cross_surface_alignment_map_only
cross_surface_alignment_non_validation_boundary_only
cross_surface_alignment_non_inference_boundary_only
cross_surface_alignment_non_scoring_boundary_only
cross_surface_alignment_non_verdict_boundary_only
cross_surface_alignment_non_routing_boundary_only
cross_surface_alignment_non_execution_boundary_only
cross_surface_alignment_non_record_boundary_only
cross_surface_alignment_non_storage_boundary_only
cross_surface_alignment_non_mutation_boundary_only
api_implementation_disabled
mcp_implementation_disabled
connector_implementation_disabled
agent_auto_call_disabled
network_access_disabled
external_system_integration_disabled
declaration_only
inspection_only
p4_m5_4_started_as_alignment_map_only
p4_m5_readiness_audit_position_preserved
p4_m5_3_connector_surface_map_reference_defined
p4_m5_2_mcp_surface_map_reference_defined
p4_m5_1_api_surface_map_reference_defined
p4_m5_0_boundary_contract_reference_defined
api_mcp_connector_identity_alignment_surface_defined
api_mcp_connector_boundary_model_alignment_surface_defined
api_mcp_connector_capability_declaration_alignment_surface_defined
api_mcp_connector_operation_inventory_alignment_surface_defined
api_mcp_connector_input_contract_alignment_surface_defined
api_mcp_connector_output_contract_alignment_surface_defined
api_mcp_connector_authentication_boundary_alignment_surface_defined
api_mcp_connector_authorization_boundary_alignment_surface_defined
api_mcp_connector_access_control_permission_scope_alignment_surface_defined
api_mcp_connector_error_contract_alignment_surface_defined
api_mcp_connector_timeout_retry_rate_limit_alignment_surface_defined
api_mcp_connector_observability_audit_logging_alignment_surface_defined
api_mcp_connector_secret_credential_boundary_alignment_surface_defined
api_mcp_connector_data_resource_classification_alignment_surface_defined
api_mcp_connector_non_execution_semantics_alignment_surface_defined
cross_surface_alignment_surfaces_are_definition_only
cross_surface_alignment_surfaces_are_not_readiness_evidence
cross_surface_alignment_surfaces_are_not_validation_inputs
api_surface_alignment_reference_only
mcp_surface_alignment_reference_only
connector_surface_alignment_reference_only
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
v7_start_deferred
productization_deferred
ui_deferred
operator_console_deferred
""".splitlines()
    if line
)


FALSE_STATUS_FLAGS = tuple(
    line
    for line in """
live_validation_enabled
cross_surface_alignment_validation_enabled
cross_surface_alignment_inference_enabled
cross_surface_alignment_scoring_enabled
cross_surface_alignment_verdict_enabled
cross_surface_alignment_routing_enabled
cross_surface_alignment_execution_enabled
cross_surface_alignment_record_creation_enabled
cross_surface_alignment_storage_enabled
cross_surface_alignment_mutation_enabled
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


P4_M5_4_CROSS_SURFACE_ALIGNMENT_MAP_BOUNDARY = (
    "P4-M5.4 API / MCP / Connector Cross-Surface Alignment Map read-only "
    "definition-only p4-m5-4-cross-surface-alignment-map-only "
    "api-mcp-connector-cross-surface-alignment-map-only "
    "cross-surface-alignment-non-validation-boundary-only "
    "cross-surface-alignment-non-inference-boundary-only "
    "cross-surface-alignment-non-scoring-boundary-only "
    "cross-surface-alignment-non-verdict-boundary-only "
    "cross-surface-alignment-non-routing-boundary-only "
    "cross-surface-alignment-non-execution-boundary-only "
    "cross-surface-alignment-non-record-boundary-only "
    "cross-surface-alignment-non-storage-boundary-only "
    "cross-surface-alignment-non-mutation-boundary-only "
    "api-implementation-disabled mcp-implementation-disabled "
    "connector-implementation-disabled agent-auto-call-disabled "
    "network-access-disabled external-system-integration-disabled "
    "declaration-only inspection-only. "
    + " ".join(f"{phrase}." for phrase in BOUNDARY_PHRASE_LINES)
)


_FIELD_IDS = (
    "p4-m5-4-cross-surface-alignment-map-id",
    "p4-m5-4-cross-surface-alignment-map-phase",
    "p4-m5-4-cross-surface-alignment-map-mode",
    "p4-m5-4-cross-surface-alignment-map-p4-m5-readiness-audit-position",
    "p4-m5-4-cross-surface-alignment-map-direct-prior-connector-surface-map-reference",
    "p4-m5-4-cross-surface-alignment-map-inherited-prior-api-mcp-connector-surface-map-and-boundary-contract-reference",
    "p4-m5-4-cross-surface-alignment-map-api-mcp-connector-identity-alignment-surface",
    "p4-m5-4-cross-surface-alignment-map-api-mcp-connector-boundary-model-alignment-surface",
    "p4-m5-4-cross-surface-alignment-map-api-mcp-connector-capability-declaration-alignment-surface",
    "p4-m5-4-cross-surface-alignment-map-api-mcp-connector-operation-inventory-alignment-surface",
    "p4-m5-4-cross-surface-alignment-map-api-mcp-connector-input-contract-alignment-surface",
    "p4-m5-4-cross-surface-alignment-map-api-mcp-connector-output-contract-alignment-surface",
    "p4-m5-4-cross-surface-alignment-map-api-mcp-connector-authentication-boundary-alignment-surface",
    "p4-m5-4-cross-surface-alignment-map-api-mcp-connector-authorization-boundary-alignment-surface",
    "p4-m5-4-cross-surface-alignment-map-api-mcp-connector-access-control-permission-scope-alignment-surface",
    "p4-m5-4-cross-surface-alignment-map-api-mcp-connector-error-contract-alignment-surface",
    "p4-m5-4-cross-surface-alignment-map-api-mcp-connector-timeout-retry-rate-limit-alignment-surface",
    "p4-m5-4-cross-surface-alignment-map-api-mcp-connector-observability-audit-logging-alignment-surface",
    "p4-m5-4-cross-surface-alignment-map-api-mcp-connector-secret-credential-boundary-alignment-surface",
    "p4-m5-4-cross-surface-alignment-map-api-mcp-connector-data-resource-classification-alignment-surface",
    "p4-m5-4-cross-surface-alignment-map-api-mcp-connector-non-execution-semantics-alignment-surface",
    "p4-m5-4-cross-surface-alignment-map-v7-productization-ui-operator-console-deferred",
    "p4-m5-4-cross-surface-alignment-map-static-alignment-map-and-validation-inference-scoring-verdict-routing-execution-record-storage-mutation-semantics-disabled",
)


def _field_purpose(field_id: str) -> str:
    return (
        f"Defines {field_id} as read-only definition-only "
        "p4-m5-4-cross-surface-alignment-map-only "
        "api-mcp-connector-cross-surface-alignment-map-only "
        "cross-surface-alignment-non-validation-boundary-only "
        "cross-surface-alignment-non-inference-boundary-only "
        "cross-surface-alignment-non-scoring-boundary-only "
        "cross-surface-alignment-non-verdict-boundary-only "
        "cross-surface-alignment-non-routing-boundary-only "
        "cross-surface-alignment-non-execution-boundary-only "
        "cross-surface-alignment-non-record-boundary-only "
        "cross-surface-alignment-non-storage-boundary-only "
        "cross-surface-alignment-non-mutation-boundary-only "
        "api-implementation-disabled mcp-implementation-disabled "
        "connector-implementation-disabled agent-auto-call-disabled "
        "network-access-disabled external-system-integration-disabled "
        "declaration-only inspection-only P4-M5.4 API / MCP / Connector "
        "Cross-Surface Alignment Map context; P4-M5.4 defines API / MCP / "
        "Connector cross-surface alignment surfaces only; P4-M5.4 is not "
        "API implementation; P4-M5.4 is not MCP implementation; P4-M5.4 is "
        "not Connector implementation; P4-M5.4 is not API client "
        "implementation; P4-M5.4 is not MCP client implementation; "
        "P4-M5.4 is not MCP server implementation; P4-M5.4 is not MCP "
        "transport implementation; P4-M5.4 is not MCP session "
        "implementation; P4-M5.4 is not Connector client implementation; "
        "P4-M5.4 is not Connector adapter implementation; P4-M5.4 is not "
        "Connector runtime implementation; P4-M5.4 is not Agent auto-call; "
        "P4-M5.4 is not external system integration; P4-M5.4 is not "
        "network access; P4-M5.4 is not live API endpoint probing; "
        "P4-M5.4 is not live MCP server probing; P4-M5.4 is not live "
        "provider probing; P4-M5.4 is not OAuth flow; P4-M5.4 is not "
        "credential use; P4-M5.4 is not secret access; P4-M5.4 is not "
        "secret inspection; P4-M5.4 is not API call; P4-M5.4 is not MCP "
        "tool call; P4-M5.4 is not MCP resource access; P4-M5.4 is not "
        "MCP prompt execution; P4-M5.4 is not connector data fetch; "
        "P4-M5.4 is not connector data write; P4-M5.4 is not connector "
        "mutation; P4-M5.4 is not authentication testing; P4-M5.4 is not "
        "authorization testing; P4-M5.4 is not schema validation; "
        "P4-M5.4 does not perform readiness validation; P4-M5.4 does not "
        "infer readiness; P4-M5.4 does not score readiness; P4-M5.4 does "
        "not produce readiness verdict; P4-M5.4 does not route "
        "implementation; P4-M5.4 does not execute; P4-M5.4 does not create "
        "readiness records; P4-M5.4 does not create storage; P4-M5.4 does "
        "not persist state; P4-M5.4 does not mutate memory; Cross-surface "
        "alignment surfaces are not readiness evidence; Cross-surface "
        "alignment surfaces are not validation inputs; no API "
        "implementation; no MCP implementation; no Connector "
        "implementation; no API client; no MCP client; no MCP server; no "
        "MCP transport; no MCP session; no Connector client; no Connector "
        "adapter; no Connector runtime; no Agent auto-call; no external "
        "system integration; no network access; no live API endpoint "
        "probing; no live MCP server probing; no live provider probing; no "
        "live provider discovery; no OAuth flow; no credential use; no "
        "secret access; no secret inspection; no API call; no MCP tool "
        "call; no MCP resource access; no MCP prompt execution; no "
        "connector data fetch; no connector data write; no connector "
        "mutation; no authentication testing; no authorization testing; no "
        "schema validation; no readiness validation; no readiness "
        "inference; no readiness scoring; no readiness verdict; no "
        "validation; no scoring; no verdict; no routing; no execution; no "
        "command execution; no record creation; no storage; no persistence; "
        "no mutation; no v7; no productization; no UI; no Operator Console; "
        "no version bump; no tag."
    )


_P4_M5_4_CROSS_SURFACE_ALIGNMENT_MAP_FIELDS = tuple(
    P4M54CrossSurfaceAlignmentMapField(
        index,
        field_id,
        f"P4-M5.4 API / MCP / Connector Cross-Surface Alignment Map Field {index}",
        _field_purpose(field_id),
        "p4-m5-4-cross-surface-alignment-map-category",
        (
            "no API implementation semantics; no MCP implementation "
            "semantics; no Connector implementation semantics; no API "
            "client semantics; no MCP client semantics; no MCP server "
            "semantics; no MCP transport semantics; no MCP session "
            "semantics; no Connector client semantics; no Connector "
            "adapter semantics; no Connector runtime semantics; no Agent "
            "auto-call semantics; no external system integration semantics; "
            "no network access semantics; no live API endpoint probe "
            "semantics; no live MCP server probe semantics; no live "
            "provider probe semantics; no live provider discovery "
            "semantics; no OAuth flow semantics; no credential use "
            "semantics; no secret access semantics; no secret inspection "
            "semantics; no API call semantics; no MCP tool call semantics; "
            "no MCP resource access semantics; no MCP prompt execution "
            "semantics; no connector data fetch semantics; no connector "
            "data write semantics; no connector mutation semantics; no "
            "authentication testing semantics; no authorization testing "
            "semantics; no schema validation semantics; no readiness "
            "validation semantics; no readiness inference semantics; no "
            "readiness scoring semantics; no readiness verdict semantics; "
            "no readiness routing semantics; no readiness execution "
            "semantics; no readiness record creation semantics; no "
            "readiness storage semantics; no readiness persistence "
            "semantics; no readiness mutation semantics; no validation "
            "semantics; no scoring semantics; no verdict semantics; no "
            "routing semantics; no executable planning semantics; no "
            "execution semantics; no command execution semantics; no "
            "record creation semantics; no storage semantics; no "
            "persistence semantics; no mutation semantics; no v7 semantics; "
            "no productization semantics; no UI semantics; no Operator "
            "Console semantics"
        ),
    )
    for index, field_id in enumerate(_FIELD_IDS, start=1)
)


def list_p4_m5_4_cross_surface_alignment_map_fields() -> (
    tuple[P4M54CrossSurfaceAlignmentMapField, ...]
):
    return _P4_M5_4_CROSS_SURFACE_ALIGNMENT_MAP_FIELDS


def p4_m5_4_cross_surface_alignment_map_field_ids() -> tuple[str, ...]:
    return tuple(
        field.field_id
        for field in list_p4_m5_4_cross_surface_alignment_map_fields()
    )


def render_p4_m5_4_cross_surface_alignment_map_markdown(
    fields: Sequence[P4M54CrossSurfaceAlignmentMapField] | None = None,
) -> str:
    field_values = (
        tuple(fields)
        if fields is not None
        else list_p4_m5_4_cross_surface_alignment_map_fields()
    )
    status = p4_m5_4_cross_surface_alignment_map_report()
    lines = [
        "# P4-M5.4 API / MCP / Connector Cross-Surface Alignment Map",
        "",
        "P4-M5.4 API / MCP / Connector Cross-Surface Alignment Map.",
        "",
    ]
    for phrase in BOUNDARY_PHRASE_LINES:
        lines.extend([f"{phrase}.", ""])
    for prior_layer in DIRECT_PRIOR_DEFINITION_LAYER_REFERENCES:
        lines.extend([f"{prior_layer} remains a referenced definition layer.", ""])
    for prior_layer in INHERITED_PRIOR_DEFINITION_LAYER_REFERENCES:
        lines.extend(
            [f"{prior_layer} remains an inherited referenced definition layer.", ""]
        )
    lines.extend(
        [
            P4_M5_4_CROSS_SURFACE_ALIGNMENT_MAP_BOUNDARY,
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
            "## P4-M5.4 API / MCP / Connector Cross-Surface Alignment Map Fields",
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
                "- P4-M5.4 cross-surface alignment map category: "
                f"{field.p4_m5_4_cross_surface_alignment_map_category}",
                "- P4-M5.4 cross-surface alignment map semantics disabled: "
                f"{field.p4_m5_4_cross_surface_alignment_map_semantics_disabled}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def p4_m5_4_cross_surface_alignment_map_as_dicts() -> tuple[dict[str, object], ...]:
    return tuple(
        asdict(field)
        for field in list_p4_m5_4_cross_surface_alignment_map_fields()
    )


def p4_m5_4_cross_surface_alignment_map_report() -> dict[str, object]:
    status: dict[str, object] = {
        "phase": "P4-M5.4",
        "feature": "API / MCP / Connector Cross-Surface Alignment Map",
        "mode": "read-only",
        "boundary": P4_M5_4_CROSS_SURFACE_ALIGNMENT_MAP_BOUNDARY,
        "package_version": P4_M5_4_PACKAGE_VERSION,
        "p4_m5_4_cross_surface_alignment_map_field_count": len(_FIELD_IDS),
        "referenced_p4_m5_3_connector_readiness_audit_surface_map_field_count": len(
            p4_m5_3_connector_readiness_audit_surface_map_field_ids()
        ),
        "referenced_p4_m5_2_mcp_readiness_audit_surface_map_field_count": len(
            p4_m5_2_mcp_readiness_audit_surface_map_field_ids()
        ),
        "referenced_p4_m5_1_api_readiness_audit_surface_map_field_count": len(
            p4_m5_1_api_readiness_audit_surface_map_field_ids()
        ),
        "referenced_p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_field_count": len(
            p4_m5_0_api_mcp_connector_readiness_audit_boundary_contract_field_ids()
        ),
    }
    status.update({flag: True for flag in TRUE_STATUS_FLAGS})
    status.update({flag: False for flag in FALSE_STATUS_FLAGS})
    return status
