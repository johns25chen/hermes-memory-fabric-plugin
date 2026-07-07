from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .p4_m6_6_entry_exception_non_override_surface import (
    FALSE_STATUS_FLAGS as P4_M6_6_FALSE_STATUS_FLAGS,
    TRUE_STATUS_FLAGS as P4_M6_6_TRUE_STATUS_FLAGS,
)


P4_M6_7_PACKAGE_VERSION = "6.16.0"
MEMORY_LOOP_COMMAND = "p4-m6-7-entry-conflict-non-resolution-surface"
MEMORY_LOOP_COMMAND_INVOCATION = (
    "memory-loop p4-m6-7-entry-conflict-non-resolution-surface"
)


@dataclass(frozen=True)
class P4M67EntryConflictNonResolutionSurfaceField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    p4_m6_7_entry_conflict_non_resolution_surface_category: str
    p4_m6_7_entry_conflict_non_resolution_surface_semantics_disabled: str


DIRECT_PRIOR_DEFINITION_LAYER_REFERENCE = (
    "P4-M6.6 Entry Exception Non-Override Surface"
)

PRIOR_DEFINITION_LAYER_REFERENCE_CHAIN = (
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
    "conflict-non-resolution-surface-only",
    "conflict-non-arbitration-surface-only",
    "conflict-non-selection-surface-only",
    "conflict-non-ranking-surface-only",
    "conflict-non-verdict-surface-only",
    "conflict-non-routing-surface-only",
    "conflict-non-execution-surface-only",
)

BOUNDARY_PHRASE_LINES = tuple(
    line
    for line in """
P4-M6.7
Entry Conflict Non-Resolution Surface
P4-M6.7 Entry Conflict Non-Resolution Surface
static entry conflict label surface
conflict-non-resolution-surface-only
conflict-non-arbitration-surface-only
conflict-non-selection-surface-only
conflict-non-ranking-surface-only
conflict-non-verdict-surface-only
conflict-non-routing-surface-only
conflict-non-execution-surface-only
definition-only
declaration-only
read-only
inspection-only
no conflict resolution
no conflict arbitration
no conflict mediation
no conflict selection
no conflict ranking
no conflict priority decision
no conflict verdict
no conflict override
no conflict bypass
no conflict waiver
no conflict exemption
no conflict routing
no conflict execution
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
P4-M6.6 Entry Exception Non-Override Surface remains the direct prior reference
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

P4_M6_7_FIELD_IDS = tuple(
    line
    for line in """
p4_m6_7_stage
p4_m6_7_surface_id
p4_m6_7_direct_prior_reference
p4_m6_7_prior_reference_chain
p4_m6_7_entry_conflict_label_surface
p4_m6_7_conflict_non_resolution_surface
p4_m6_7_conflict_non_arbitration_surface
p4_m6_7_conflict_non_selection_surface
p4_m6_7_conflict_non_ranking_surface
p4_m6_7_conflict_non_verdict_surface
p4_m6_7_conflict_non_override_surface
p4_m6_7_conflict_non_bypass_surface
p4_m6_7_conflict_non_waiver_surface
p4_m6_7_conflict_non_exemption_surface
p4_m6_7_conflict_non_routing_surface
p4_m6_7_conflict_non_execution_surface
p4_m6_7_readiness_non_evidence_surface
p4_m6_7_validation_non_input_surface
p4_m6_7_record_non_creation_surface
p4_m6_7_storage_non_persistence_surface
p4_m6_7_mutation_absence_surface
p4_m6_7_implementation_corridor_non_start_surface
p4_m6_7_operator_surface_guard
""".splitlines()
    if line
)

P4_M6_7_FIELD_DEFINITIONS = (
    (
        "P4-M6.7 stage",
        "Declares the P4-M6.7 Entry Conflict Non-Resolution Surface stage.",
        "stage",
        "no implementation corridor start",
    ),
    (
        "P4-M6.7 surface id",
        "Declares the static surface id and memory-loop command label.",
        "identity",
        "no routing",
    ),
    (
        "P4-M6.7 direct prior reference",
        "Points directly to P4-M6.6 Entry Exception Non-Override Surface.",
        "lineage",
        "no override",
    ),
    (
        "P4-M6.7 prior reference chain",
        "Preserves the P4-M6.6 through P4-M5.0 prior reference chain.",
        "lineage",
        "no bypass",
    ),
    (
        "P4-M6.7 entry conflict label surface",
        "Declares only a static entry conflict label surface.",
        "label",
        "no conflict mediation",
    ),
    (
        "P4-M6.7 conflict non-resolution surface",
        "Declares that conflict labels do not resolve conflicts.",
        "conflict-boundary",
        "no conflict resolution",
    ),
    (
        "P4-M6.7 conflict non-arbitration surface",
        "Declares that conflict labels do not arbitrate conflicts.",
        "conflict-boundary",
        "no conflict arbitration",
    ),
    (
        "P4-M6.7 conflict non-selection surface",
        "Declares that conflict labels do not select among conflicts.",
        "conflict-boundary",
        "no conflict selection",
    ),
    (
        "P4-M6.7 conflict non-ranking surface",
        "Declares that conflict labels do not rank conflicts.",
        "conflict-boundary",
        "no conflict ranking",
    ),
    (
        "P4-M6.7 conflict non-verdict surface",
        "Declares that conflict labels do not produce conflict verdicts.",
        "conflict-boundary",
        "no conflict verdict",
    ),
    (
        "P4-M6.7 conflict non-override surface",
        "Declares that conflict labels do not override boundaries.",
        "conflict-boundary",
        "no conflict override",
    ),
    (
        "P4-M6.7 conflict non-bypass surface",
        "Declares that conflict labels do not bypass boundaries.",
        "conflict-boundary",
        "no conflict bypass",
    ),
    (
        "P4-M6.7 conflict non-waiver surface",
        "Declares that conflict labels do not waive boundaries.",
        "conflict-boundary",
        "no conflict waiver",
    ),
    (
        "P4-M6.7 conflict non-exemption surface",
        "Declares that conflict labels do not exempt boundaries.",
        "conflict-boundary",
        "no conflict exemption",
    ),
    (
        "P4-M6.7 conflict non-routing surface",
        "Declares that conflict labels do not route work.",
        "conflict-boundary",
        "no conflict routing",
    ),
    (
        "P4-M6.7 conflict non-execution surface",
        "Declares that conflict labels do not execute work.",
        "conflict-boundary",
        "no conflict execution",
    ),
    (
        "P4-M6.7 readiness non-evidence surface",
        "Declares that conflict labels are not readiness evidence.",
        "evidence-boundary",
        "no readiness evidence",
    ),
    (
        "P4-M6.7 validation non-input surface",
        "Declares that conflict labels are not validation input.",
        "validation-boundary",
        "no validation input",
    ),
    (
        "P4-M6.7 record non-creation surface",
        "Declares that conflict labels create no records.",
        "record-boundary",
        "no record creation",
    ),
    (
        "P4-M6.7 storage non-persistence surface",
        "Declares that conflict labels create no storage or persistence.",
        "storage-boundary",
        "no storage; no persistence",
    ),
    (
        "P4-M6.7 mutation absence surface",
        "Declares that conflict labels do not mutate memory or state.",
        "mutation-boundary",
        "no mutation",
    ),
    (
        "P4-M6.7 implementation corridor non-start surface",
        "Declares that the implementation corridor remains not started.",
        "implementation-boundary",
        "no implementation corridor start",
    ),
    (
        "P4-M6.7 operator surface guard",
        "Declares no UI, Operator Console, v7, productization, API, MCP, Connector, Agent, network, OAuth, credential, or secret inspection behavior.",
        "operator-boundary",
        "no UI; no Operator Console",
    ),
)

P4_M6_7_TRUE_STATUS_FLAGS = (
    "p4_m6_7_entry_conflict_non_resolution_surface_started",
    "p4_m6_7_static_entry_conflict_label_surface_only",
    "conflict_non_resolution_surface_only",
    "conflict_non_arbitration_surface_only",
    "conflict_non_selection_surface_only",
    "conflict_non_ranking_surface_only",
    "conflict_non_verdict_surface_only",
    "conflict_non_routing_surface_only",
    "conflict_non_execution_surface_only",
)

P4_M6_7_FALSE_STATUS_FLAGS = (
    "p4_m6_7_conflict_resolution_enabled",
    "p4_m6_7_conflict_arbitration_enabled",
    "p4_m6_7_conflict_mediation_enabled",
    "p4_m6_7_conflict_selection_enabled",
    "p4_m6_7_conflict_ranking_enabled",
    "p4_m6_7_conflict_priority_decision_enabled",
    "p4_m6_7_conflict_verdict_enabled",
    "p4_m6_7_conflict_override_enabled",
    "p4_m6_7_conflict_bypass_enabled",
    "p4_m6_7_conflict_waiver_enabled",
    "p4_m6_7_conflict_exemption_enabled",
    "p4_m6_7_conflict_routing_enabled",
    "p4_m6_7_conflict_execution_enabled",
    "p4_m6_7_readiness_evidence_enabled",
    "p4_m6_7_validation_input_enabled",
    "p4_m6_7_record_creation_enabled",
    "p4_m6_7_storage_enabled",
    "p4_m6_7_persistence_enabled",
    "p4_m6_7_mutation_enabled",
    "p4_m6_7_implementation_corridor_started",
    "p4_m6_7_api_call_enabled",
    "p4_m6_7_mcp_call_enabled",
    "p4_m6_7_connector_call_enabled",
    "p4_m6_7_agent_call_enabled",
    "p4_m6_7_network_enabled",
    "p4_m6_7_oauth_enabled",
    "p4_m6_7_credential_inspection_enabled",
    "p4_m6_7_secret_inspection_enabled",
    "p4_m6_7_operator_console_enabled",
)

TRUE_STATUS_FLAGS = P4_M6_6_TRUE_STATUS_FLAGS + P4_M6_7_TRUE_STATUS_FLAGS
FALSE_STATUS_FLAGS = P4_M6_6_FALSE_STATUS_FLAGS + P4_M6_7_FALSE_STATUS_FLAGS


def list_p4_m6_7_entry_conflict_non_resolution_surface_fields() -> (
    tuple[P4M67EntryConflictNonResolutionSurfaceField, ...]
):
    return tuple(
        P4M67EntryConflictNonResolutionSurfaceField(
            field_order=index,
            field_id=field_id,
            field_name=definition[0],
            field_purpose=definition[1],
            p4_m6_7_entry_conflict_non_resolution_surface_category=definition[2],
            p4_m6_7_entry_conflict_non_resolution_surface_semantics_disabled=definition[3],
        )
        for index, (field_id, definition) in enumerate(
            zip(P4_M6_7_FIELD_IDS, P4_M6_7_FIELD_DEFINITIONS, strict=True),
            start=1,
        )
    )


def p4_m6_7_entry_conflict_non_resolution_surface_field_ids() -> tuple[str, ...]:
    return tuple(
        field.field_id
        for field in list_p4_m6_7_entry_conflict_non_resolution_surface_fields()
    )


def p4_m6_7_entry_conflict_non_resolution_surface_as_dicts() -> (
    tuple[dict[str, Any], ...]
):
    return tuple(
        asdict(field)
        for field in list_p4_m6_7_entry_conflict_non_resolution_surface_fields()
    )


def p4_m6_7_entry_conflict_non_resolution_surface_status_shape() -> dict[str, Any]:
    return {
        "p4_m6_7_stage": "P4-M6.7 Entry Conflict Non-Resolution Surface",
        "p4_m6_7_surface_id": MEMORY_LOOP_COMMAND,
        "p4_m6_7_direct_prior_reference": DIRECT_PRIOR_DEFINITION_LAYER_REFERENCE,
        "p4_m6_7_prior_reference_chain": PRIOR_DEFINITION_LAYER_REFERENCE_CHAIN,
        "p4_m6_7_entry_conflict_label_surface": (
            "static entry conflict label surface; definition-only; "
            "declaration-only; read-only; inspection-only"
        ),
        "p4_m6_7_conflict_non_resolution_surface": (
            "conflict-non-resolution-surface-only; no conflict resolution"
        ),
        "p4_m6_7_conflict_non_arbitration_surface": (
            "conflict-non-arbitration-surface-only; no conflict arbitration"
        ),
        "p4_m6_7_conflict_non_selection_surface": (
            "conflict-non-selection-surface-only; no conflict selection"
        ),
        "p4_m6_7_conflict_non_ranking_surface": (
            "conflict-non-ranking-surface-only; no conflict ranking"
        ),
        "p4_m6_7_conflict_non_verdict_surface": (
            "conflict-non-verdict-surface-only; no conflict verdict"
        ),
        "p4_m6_7_conflict_non_override_surface": "no conflict override",
        "p4_m6_7_conflict_non_bypass_surface": "no conflict bypass",
        "p4_m6_7_conflict_non_waiver_surface": "no conflict waiver",
        "p4_m6_7_conflict_non_exemption_surface": "no conflict exemption",
        "p4_m6_7_conflict_non_routing_surface": (
            "conflict-non-routing-surface-only; no conflict routing"
        ),
        "p4_m6_7_conflict_non_execution_surface": (
            "conflict-non-execution-surface-only; no conflict execution"
        ),
        "p4_m6_7_readiness_non_evidence_surface": "no readiness evidence",
        "p4_m6_7_validation_non_input_surface": "no validation input",
        "p4_m6_7_record_non_creation_surface": "no record creation",
        "p4_m6_7_storage_non_persistence_surface": "no storage; no persistence",
        "p4_m6_7_mutation_absence_surface": "no mutation",
        "p4_m6_7_implementation_corridor_non_start_surface": (
            "no implementation corridor start; no API; no MCP; no Connector; "
            "no Agent; no network; no OAuth; no credential; no secret inspection"
        ),
        "p4_m6_7_operator_surface_guard": (
            "no v7; no productization; no UI; no Operator Console"
        ),
    }


def _status_booleans() -> dict[str, bool]:
    return {
        **{flag: True for flag in TRUE_STATUS_FLAGS},
        **{flag: False for flag in FALSE_STATUS_FLAGS},
    }


def p4_m6_7_entry_conflict_non_resolution_surface_report() -> dict[str, Any]:
    return {
        "stage": "P4-M6.7",
        "surface": "Entry Conflict Non-Resolution Surface",
        "package_version": P4_M6_7_PACKAGE_VERSION,
        "command": MEMORY_LOOP_COMMAND_INVOCATION,
        "mode": "read-only declaration-only definition-only inspection-only",
        "direct_prior_reference": DIRECT_PRIOR_DEFINITION_LAYER_REFERENCE,
        "prior_reference_chain": PRIOR_DEFINITION_LAYER_REFERENCE_CHAIN,
        "status_direction": STATUS_DIRECTION,
        "boundary_phrases": BOUNDARY_PHRASE_LINES,
        "fields": p4_m6_7_entry_conflict_non_resolution_surface_as_dicts(),
        "status_shape": p4_m6_7_entry_conflict_non_resolution_surface_status_shape(),
        "true_flags": len(TRUE_STATUS_FLAGS),
        "false_flags": len(FALSE_STATUS_FLAGS),
        "status_booleans": _status_booleans(),
    }


def render_p4_m6_7_entry_conflict_non_resolution_surface_markdown() -> str:
    report = p4_m6_7_entry_conflict_non_resolution_surface_report()
    lines = [
        "# P4-M6.7 Entry Conflict Non-Resolution Surface",
        "",
        "P4-M6.7 Entry Conflict Non-Resolution Surface.",
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
        for field in list_p4_m6_7_entry_conflict_non_resolution_surface_fields()
    )
    lines.extend(
        [
            "",
            "## Status Shape",
            "",
        ]
    )
    status_shape = p4_m6_7_entry_conflict_non_resolution_surface_status_shape()
    lines.extend(f"- `{field_id}`: {status_shape[field_id]}" for field_id in P4_M6_7_FIELD_IDS)
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
            "This surface is static data only. It declares labels and boundaries; it does not resolve, arbitrate, mediate, rank, select, prioritize, override, bypass, waive, exempt, route, execute, validate, infer, score, approve, authorize, confirm, recommend, store, persist, mutate, call APIs, call MCP, call connectors, call agents, use network, inspect OAuth, inspect credentials, inspect secrets, add UI, add Operator Console, enter v7, or productize anything.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_p4_m6_7_entry_conflict_non_resolution_surface_json() -> str:
    return json.dumps(
        p4_m6_7_entry_conflict_non_resolution_surface_report(),
        indent=2,
        sort_keys=True,
    )


def run_p4_m6_7_entry_conflict_non_resolution_surface_command(
    *, output_format: str = "markdown", workspace_root: str | Path | None = None
) -> str:
    # workspace_root is intentionally accepted only to prove the surface ignores storage.
    _ = workspace_root
    if output_format == "markdown":
        return render_p4_m6_7_entry_conflict_non_resolution_surface_markdown()
    if output_format == "json":
        return render_p4_m6_7_entry_conflict_non_resolution_surface_json()
    raise ValueError("output_format must be 'markdown' or 'json'")


P4_M6_7_ENTRY_CONFLICT_NON_RESOLUTION_SURFACE_BOUNDARY = (
    p4_m6_7_entry_conflict_non_resolution_surface_report()
)
