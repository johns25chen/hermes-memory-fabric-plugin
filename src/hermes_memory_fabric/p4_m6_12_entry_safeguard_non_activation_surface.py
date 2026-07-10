from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .p4_m6_11_entry_risk_non_mitigation_surface import (
    FALSE_STATUS_FLAGS as P4_M6_11_FALSE_STATUS_FLAGS,
    TRUE_STATUS_FLAGS as P4_M6_11_TRUE_STATUS_FLAGS,
)


P4_M6_12_PACKAGE_VERSION = "6.16.0"
MEMORY_LOOP_COMMAND = "p4-m6-12-entry-safeguard-non-activation-surface"
MEMORY_LOOP_COMMAND_INVOCATION = (
    "memory-loop p4-m6-12-entry-safeguard-non-activation-surface"
)


@dataclass(frozen=True)
class P4M612EntrySafeguardNonActivationSurfaceField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    p4_m6_12_entry_safeguard_non_activation_surface_category: str
    p4_m6_12_entry_safeguard_non_activation_surface_semantics_disabled: str


DIRECT_PRIOR_DEFINITION_LAYER_REFERENCE = (
    "P4-M6.11 Entry Risk Non-Mitigation Surface"
)

PRIOR_DEFINITION_LAYER_REFERENCE_CHAIN = (
    "P4-M6.11 Entry Risk Non-Mitigation Surface",
    "P4-M6.10 Entry Constraint Non-Enforcement Surface",
    "P4-M6.9 Entry Dependency Non-Activation Surface",
    "P4-M6.8 Entry Ambiguity Non-Inference Surface",
    "P4-M6.7 Entry Conflict Non-Resolution Surface",
    "P4-M6.6 Entry Exception Non-Override Surface",
    "P4-M6.5 Entry Escalation Non-Routing Surface",
    "P4-M6.4 Entry Rejection Non-Execution Surface",
    "P4-M6.3 Entry Deferral Non-Execution Surface",
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

STATUS_DIRECTION = (
    "safeguard-non-activation-surface-only",
    "safeguard-non-application-surface-only",
    "safeguard-non-enforcement-surface-only",
    "safeguard-non-configuration-surface-only",
    "safeguard-non-prioritization-surface-only",
    "safeguard-non-selection-surface-only",
    "safeguard-non-recommendation-surface-only",
    "safeguard-non-routing-surface-only",
    "safeguard-non-execution-surface-only",
)

BOUNDARY_PHRASE_LINES = tuple(
    line
    for line in """
P4-M6.12
Entry Safeguard Non-Activation Surface
P4-M6.12 Entry Safeguard Non-Activation Surface
static entry safeguard label surface
safeguard-non-activation-surface-only
safeguard-non-application-surface-only
safeguard-non-enforcement-surface-only
safeguard-non-configuration-surface-only
safeguard-non-prioritization-surface-only
safeguard-non-selection-surface-only
safeguard-non-recommendation-surface-only
safeguard-non-routing-surface-only
safeguard-non-execution-surface-only
definition-only
declaration-only
read-only
inspection-only
no safeguard activation
no safeguard application
no safeguard enforcement
no safeguard configuration
no safeguard prioritization
no safeguard selection
no safeguard recommendation
no entry blocking
no entry unblocking
no safeguard routing
no safeguard execution
no readiness evidence
no validation input
no record creation
no storage
no persistence
no mutation
no implementation corridor start
no API
no MCP
no Connector
no Agent
no network
no OAuth
no credential
no secret inspection
no v7
no productization
no UI
no Operator Console
P4-M6.11 Entry Risk Non-Mitigation Surface remains the direct prior reference
P4-M6.10 Entry Constraint Non-Enforcement Surface remains a preserved prior reference
P4-M6.9 Entry Dependency Non-Activation Surface remains a preserved prior reference
P4-M6.8 Entry Ambiguity Non-Inference Surface remains a preserved prior reference
P4-M6.7 Entry Conflict Non-Resolution Surface remains a preserved prior reference
P4-M6.6 Entry Exception Non-Override Surface remains a preserved prior reference
P4-M6.5 Entry Escalation Non-Routing Surface remains a preserved prior reference
P4-M6.4 Entry Rejection Non-Execution Surface remains a preserved prior reference
P4-M6.3 Entry Deferral Non-Execution Surface remains a preserved prior reference
P4-M6.2 Entry Acceptance Non-Evidence Surface remains a preserved prior reference
P4-M6.1 Entry Preconditions Definition Surface remains a preserved prior reference
P4-M6.0 Next Corridor Entry Boundary Contract remains a preserved prior reference
P4-M5.6 Final Closure Handoff / Next Corridor Non-Start Index remains a preserved prior reference
P4-M5.5 Readiness Audit Closure / Non-Start Boundary Seal remains a preserved prior reference
P4-M5.4 API / MCP / Connector Cross-Surface Alignment Map remains a preserved prior reference
P4-M5.3 Connector Readiness Audit Surface Map remains a preserved prior reference
P4-M5.2 MCP Readiness Audit Surface Map remains a preserved prior reference
P4-M5.1 API Readiness Audit Surface Map remains a preserved prior reference
P4-M5.0 API / MCP / Connector Readiness Audit Boundary Contract remains a preserved prior reference
""".splitlines()
    if line
)

P4_M6_12_FIELD_IDS = tuple(
    line
    for line in """
p4_m6_12_stage
p4_m6_12_surface_id
p4_m6_12_direct_prior_reference
p4_m6_12_prior_reference_chain
p4_m6_12_entry_safeguard_label_surface
p4_m6_12_safeguard_non_activation_surface
p4_m6_12_safeguard_non_application_surface
p4_m6_12_safeguard_non_enforcement_surface
p4_m6_12_safeguard_non_configuration_surface
p4_m6_12_safeguard_non_prioritization_surface
p4_m6_12_safeguard_non_selection_surface
p4_m6_12_safeguard_non_recommendation_surface
p4_m6_12_entry_non_blocking_surface
p4_m6_12_entry_non_unblocking_surface
p4_m6_12_safeguard_non_routing_surface
p4_m6_12_safeguard_non_execution_surface
p4_m6_12_readiness_non_evidence_surface
p4_m6_12_validation_non_input_surface
p4_m6_12_record_non_creation_surface
p4_m6_12_storage_non_persistence_surface
p4_m6_12_mutation_absence_surface
p4_m6_12_implementation_corridor_non_start_surface
p4_m6_12_operator_surface_guard
""".splitlines()
    if line
)

P4_M6_12_FIELD_DEFINITIONS = (
    (
        "P4-M6.12 stage",
        "Declares the P4-M6.12 Entry Safeguard Non-Activation Surface stage.",
        "stage",
        "no implementation corridor start",
    ),
    (
        "P4-M6.12 surface id",
        "Declares the static surface id and memory-loop command label.",
        "identity",
        "no routing",
    ),
    (
        "P4-M6.12 direct prior reference",
        "Points directly to P4-M6.11 Entry Risk Non-Mitigation Surface.",
        "lineage",
        "no safeguard activation",
    ),
    (
        "P4-M6.12 prior reference chain",
        "Preserves the P4-M6.11 through P4-M5.0 prior reference chain.",
        "lineage",
        "no safeguard application",
    ),
    (
        "P4-M6.12 entry safeguard label surface",
        "Declares only a static entry safeguard label surface.",
        "label",
        "no safeguard activation",
    ),
    (
        "P4-M6.12 safeguard non-activation surface",
        "Declares that safeguard labels do not activate safeguards.",
        "safeguard-boundary",
        "no safeguard activation",
    ),
    (
        "P4-M6.12 safeguard non-application surface",
        "Declares that safeguard labels do not apply safeguards.",
        "safeguard-boundary",
        "no safeguard application",
    ),
    (
        "P4-M6.12 safeguard non-enforcement surface",
        "Declares that safeguard labels do not enforce safeguards.",
        "safeguard-boundary",
        "no safeguard enforcement",
    ),
    (
        "P4-M6.12 safeguard non-configuration surface",
        "Declares that safeguard labels do not configure safeguards.",
        "safeguard-boundary",
        "no safeguard configuration",
    ),
    (
        "P4-M6.12 safeguard non-prioritization surface",
        "Declares that safeguard labels do not prioritize safeguards.",
        "safeguard-boundary",
        "no safeguard prioritization",
    ),
    (
        "P4-M6.12 safeguard non-selection surface",
        "Declares that safeguard labels do not select safeguards.",
        "safeguard-boundary",
        "no safeguard selection",
    ),
    (
        "P4-M6.12 safeguard non-recommendation surface",
        "Declares that safeguard labels do not recommend safeguards.",
        "safeguard-boundary",
        "no safeguard recommendation",
    ),
    (
        "P4-M6.12 entry non-blocking surface",
        "Declares that safeguard labels do not block entry.",
        "entry-boundary",
        "no entry blocking",
    ),
    (
        "P4-M6.12 entry non-unblocking surface",
        "Declares that safeguard labels do not unblock entry.",
        "entry-boundary",
        "no entry unblocking",
    ),
    (
        "P4-M6.12 safeguard non-routing surface",
        "Declares that safeguard labels do not route work.",
        "safeguard-boundary",
        "no safeguard routing",
    ),
    (
        "P4-M6.12 safeguard non-execution surface",
        "Declares that safeguard labels do not execute work.",
        "safeguard-boundary",
        "no safeguard execution",
    ),
    (
        "P4-M6.12 readiness non-evidence surface",
        "Declares that safeguard labels are not readiness evidence.",
        "evidence-boundary",
        "no readiness evidence",
    ),
    (
        "P4-M6.12 validation non-input surface",
        "Declares that safeguard labels are not validation input.",
        "validation-boundary",
        "no validation input",
    ),
    (
        "P4-M6.12 record non-creation surface",
        "Declares that safeguard labels create no records.",
        "record-boundary",
        "no record creation",
    ),
    (
        "P4-M6.12 storage non-persistence surface",
        "Declares that safeguard labels create no storage or persistence.",
        "storage-boundary",
        "no storage; no persistence",
    ),
    (
        "P4-M6.12 mutation absence surface",
        "Declares that safeguard labels do not mutate memory or state.",
        "mutation-boundary",
        "no mutation",
    ),
    (
        "P4-M6.12 implementation corridor non-start surface",
        "Declares that the implementation corridor remains not started.",
        "implementation-boundary",
        "no implementation corridor start",
    ),
    (
        "P4-M6.12 operator surface guard",
        "Declares no UI, Operator Console, v7, productization, API, MCP, Connector, Agent, network, OAuth, credential, or secret inspection behavior.",
        "operator-boundary",
        "no UI; no Operator Console",
    ),
)

P4_M6_12_TRUE_STATUS_FLAGS = (
    "safeguard_non_activation_surface_only",
    "safeguard_non_application_surface_only",
    "safeguard_non_enforcement_surface_only",
    "safeguard_non_configuration_surface_only",
    "safeguard_non_prioritization_surface_only",
    "safeguard_non_selection_surface_only",
    "safeguard_non_recommendation_surface_only",
    "safeguard_non_routing_surface_only",
    "safeguard_non_execution_surface_only",
)

P4_M6_12_FALSE_STATUS_FLAGS = (
    "p4_m6_12_safeguard_activation_enabled",
    "p4_m6_12_safeguard_application_enabled",
    "p4_m6_12_safeguard_enforcement_enabled",
    "p4_m6_12_safeguard_configuration_enabled",
    "p4_m6_12_safeguard_inference_enabled",
    "p4_m6_12_safeguard_scoring_enabled",
    "p4_m6_12_safeguard_recommendation_enabled",
    "p4_m6_12_safeguard_prioritization_enabled",
    "p4_m6_12_safeguard_selection_enabled",
    "p4_m6_12_entry_blocking_enabled",
    "p4_m6_12_entry_unblocking_enabled",
    "p4_m6_12_safeguard_routing_enabled",
    "p4_m6_12_safeguard_execution_enabled",
    "p4_m6_12_safeguard_verdict_enabled",
    "p4_m6_12_readiness_evidence_enabled",
    "p4_m6_12_validation_input_enabled",
    "p4_m6_12_record_creation_enabled",
    "p4_m6_12_storage_enabled",
    "p4_m6_12_persistence_enabled",
    "p4_m6_12_mutation_enabled",
    "p4_m6_12_implementation_corridor_started",
    "p4_m6_12_api_call_enabled",
    "p4_m6_12_mcp_call_enabled",
    "p4_m6_12_connector_call_enabled",
    "p4_m6_12_agent_call_enabled",
    "p4_m6_12_network_enabled",
    "p4_m6_12_oauth_enabled",
    "p4_m6_12_credential_inspection_enabled",
    "p4_m6_12_secret_inspection_enabled",
)

TRUE_STATUS_FLAGS = P4_M6_11_TRUE_STATUS_FLAGS + P4_M6_12_TRUE_STATUS_FLAGS
FALSE_STATUS_FLAGS = P4_M6_11_FALSE_STATUS_FLAGS + P4_M6_12_FALSE_STATUS_FLAGS


def list_p4_m6_12_entry_safeguard_non_activation_surface_fields() -> (
    tuple[P4M612EntrySafeguardNonActivationSurfaceField, ...]
):
    return tuple(
        P4M612EntrySafeguardNonActivationSurfaceField(
            field_order=index,
            field_id=field_id,
            field_name=definition[0],
            field_purpose=definition[1],
            p4_m6_12_entry_safeguard_non_activation_surface_category=definition[2],
            p4_m6_12_entry_safeguard_non_activation_surface_semantics_disabled=(
                definition[3]
            ),
        )
        for index, (field_id, definition) in enumerate(
            zip(P4_M6_12_FIELD_IDS, P4_M6_12_FIELD_DEFINITIONS, strict=True),
            start=1,
        )
    )


def p4_m6_12_entry_safeguard_non_activation_surface_field_ids() -> tuple[str, ...]:
    return tuple(
        field.field_id
        for field in list_p4_m6_12_entry_safeguard_non_activation_surface_fields()
    )


def p4_m6_12_entry_safeguard_non_activation_surface_as_dicts() -> (
    tuple[dict[str, Any], ...]
):
    return tuple(
        asdict(field)
        for field in list_p4_m6_12_entry_safeguard_non_activation_surface_fields()
    )


def p4_m6_12_entry_safeguard_non_activation_surface_status_shape() -> (
    dict[str, Any]
):
    return {
        "p4_m6_12_stage": "P4-M6.12 Entry Safeguard Non-Activation Surface",
        "p4_m6_12_surface_id": MEMORY_LOOP_COMMAND,
        "p4_m6_12_direct_prior_reference": DIRECT_PRIOR_DEFINITION_LAYER_REFERENCE,
        "p4_m6_12_prior_reference_chain": PRIOR_DEFINITION_LAYER_REFERENCE_CHAIN,
        "p4_m6_12_entry_safeguard_label_surface": (
            "static entry safeguard label surface; definition-only; "
            "declaration-only; read-only; inspection-only"
        ),
        "p4_m6_12_safeguard_non_activation_surface": (
            "safeguard-non-activation-surface-only; no safeguard activation"
        ),
        "p4_m6_12_safeguard_non_application_surface": (
            "safeguard-non-application-surface-only; no safeguard application"
        ),
        "p4_m6_12_safeguard_non_enforcement_surface": (
            "safeguard-non-enforcement-surface-only; no safeguard enforcement"
        ),
        "p4_m6_12_safeguard_non_configuration_surface": (
            "safeguard-non-configuration-surface-only; no safeguard configuration"
        ),
        "p4_m6_12_safeguard_non_prioritization_surface": (
            "safeguard-non-prioritization-surface-only; no safeguard prioritization"
        ),
        "p4_m6_12_safeguard_non_selection_surface": (
            "safeguard-non-selection-surface-only; no safeguard selection"
        ),
        "p4_m6_12_safeguard_non_recommendation_surface": (
            "safeguard-non-recommendation-surface-only; no safeguard recommendation"
        ),
        "p4_m6_12_entry_non_blocking_surface": "no entry blocking",
        "p4_m6_12_entry_non_unblocking_surface": "no entry unblocking",
        "p4_m6_12_safeguard_non_routing_surface": (
            "safeguard-non-routing-surface-only; no safeguard routing"
        ),
        "p4_m6_12_safeguard_non_execution_surface": (
            "safeguard-non-execution-surface-only; no safeguard execution"
        ),
        "p4_m6_12_readiness_non_evidence_surface": "no readiness evidence",
        "p4_m6_12_validation_non_input_surface": "no validation input",
        "p4_m6_12_record_non_creation_surface": "no record creation",
        "p4_m6_12_storage_non_persistence_surface": "no storage; no persistence",
        "p4_m6_12_mutation_absence_surface": "no mutation",
        "p4_m6_12_implementation_corridor_non_start_surface": (
            "no implementation corridor start; no API; no MCP; no Connector; "
            "no Agent; no network; no OAuth; no credential; no secret inspection"
        ),
        "p4_m6_12_operator_surface_guard": (
            "no v7; no productization; no UI; no Operator Console"
        ),
    }


def _status_booleans() -> dict[str, bool]:
    return {
        **{flag: True for flag in TRUE_STATUS_FLAGS},
        **{flag: False for flag in FALSE_STATUS_FLAGS},
    }


def p4_m6_12_entry_safeguard_non_activation_surface_report() -> dict[str, Any]:
    return {
        "stage": "P4-M6.12",
        "surface": "Entry Safeguard Non-Activation Surface",
        "package_version": P4_M6_12_PACKAGE_VERSION,
        "command": MEMORY_LOOP_COMMAND_INVOCATION,
        "mode": "read-only declaration-only definition-only inspection-only",
        "direct_prior_reference": DIRECT_PRIOR_DEFINITION_LAYER_REFERENCE,
        "prior_reference_chain": PRIOR_DEFINITION_LAYER_REFERENCE_CHAIN,
        "status_direction": STATUS_DIRECTION,
        "boundary_phrases": BOUNDARY_PHRASE_LINES,
        "fields": p4_m6_12_entry_safeguard_non_activation_surface_as_dicts(),
        "status_shape": p4_m6_12_entry_safeguard_non_activation_surface_status_shape(),
        "true_flags": len(TRUE_STATUS_FLAGS),
        "false_flags": len(FALSE_STATUS_FLAGS),
        "status_booleans": _status_booleans(),
    }


def render_p4_m6_12_entry_safeguard_non_activation_surface_markdown() -> str:
    report = p4_m6_12_entry_safeguard_non_activation_surface_report()
    lines = [
        "# P4-M6.12 Entry Safeguard Non-Activation Surface",
        "",
        "P4-M6.12 Entry Safeguard Non-Activation Surface.",
        "",
        f"Command: `{report['command']}`.",
        "",
        "## Boundary Phrases",
        "",
    ]
    lines.extend(f"- {phrase}." for phrase in BOUNDARY_PHRASE_LINES)
    lines.extend(
        [
            "",
            "## Status Direction",
            "",
        ]
    )
    lines.extend(f"- {direction}." for direction in STATUS_DIRECTION)
    lines.extend(
        [
            "",
            "## Prior Reference Chain",
            "",
            f"- Direct prior reference: {DIRECT_PRIOR_DEFINITION_LAYER_REFERENCE}.",
        ]
    )
    lines.extend(
        f"- Preserved prior reference: {reference}."
        for reference in PRIOR_DEFINITION_LAYER_REFERENCE_CHAIN
    )
    lines.extend(
        [
            "",
            "## Semantic Field IDs",
            "",
        ]
    )
    lines.extend(
        f"- `{field.field_id}`: {field.field_purpose}"
        for field in list_p4_m6_12_entry_safeguard_non_activation_surface_fields()
    )
    lines.extend(
        [
            "",
            "## Status Shape",
            "",
        ]
    )
    status_shape = p4_m6_12_entry_safeguard_non_activation_surface_status_shape()
    lines.extend(
        f"- `{field_id}`: {status_shape[field_id]}"
        for field_id in P4_M6_12_FIELD_IDS
    )
    lines.extend(
        [
            "",
            "## Aggregate Counts",
            "",
            f"- true_flags={report['true_flags']}.",
            f"- false_flags={report['false_flags']}.",
            "",
            "## Non-Behavior Boundary",
            "",
            "This surface is static data only. It declares labels and boundaries; it does not activate safeguards, apply safeguards, enforce safeguards, configure safeguards, prioritize safeguards, select safeguards, recommend safeguards, block entry, unblock entry, route safeguards, execute safeguards, provide readiness evidence, provide validation input, create records, store, persist, mutate, call APIs, call MCP, call connectors, call agents, use network, inspect OAuth, inspect credentials, inspect secrets, add UI, add Operator Console, enter v7, or productize anything.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_p4_m6_12_entry_safeguard_non_activation_surface_json() -> str:
    return json.dumps(
        p4_m6_12_entry_safeguard_non_activation_surface_report(),
        indent=2,
        sort_keys=True,
    )


def run_p4_m6_12_entry_safeguard_non_activation_surface_command(
    *, output_format: str = "markdown", workspace_root: str | Path | None = None
) -> str:
    # workspace_root is intentionally accepted only to prove the surface ignores storage.
    _ = workspace_root
    if output_format == "markdown":
        return render_p4_m6_12_entry_safeguard_non_activation_surface_markdown()
    if output_format == "json":
        return render_p4_m6_12_entry_safeguard_non_activation_surface_json()
    raise ValueError("output_format must be 'markdown' or 'json'")


P4_M6_12_ENTRY_SAFEGUARD_NON_ACTIVATION_SURFACE_BOUNDARY = (
    p4_m6_12_entry_safeguard_non_activation_surface_report()
)
