from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .p4_m6_8_entry_ambiguity_non_inference_surface import (
    FALSE_STATUS_FLAGS as P4_M6_8_FALSE_STATUS_FLAGS,
    TRUE_STATUS_FLAGS as P4_M6_8_TRUE_STATUS_FLAGS,
)


P4_M6_9_PACKAGE_VERSION = "6.16.0"
MEMORY_LOOP_COMMAND = "p4-m6-9-entry-dependency-non-activation-surface"
MEMORY_LOOP_COMMAND_INVOCATION = (
    "memory-loop p4-m6-9-entry-dependency-non-activation-surface"
)


@dataclass(frozen=True)
class P4M69EntryDependencyNonActivationSurfaceField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    p4_m6_9_entry_dependency_non_activation_surface_category: str
    p4_m6_9_entry_dependency_non_activation_surface_semantics_disabled: str


DIRECT_PRIOR_DEFINITION_LAYER_REFERENCE = (
    "P4-M6.8 Entry Ambiguity Non-Inference Surface"
)

PRIOR_DEFINITION_LAYER_REFERENCE_CHAIN = (
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
    "dependency-non-activation-surface-only",
    "dependency-non-resolution-surface-only",
    "dependency-non-traversal-surface-only",
    "dependency-non-expansion-surface-only",
    "dependency-non-requirement-generation-surface-only",
    "dependency-non-ordering-surface-only",
    "dependency-non-selection-surface-only",
    "dependency-non-routing-surface-only",
    "dependency-non-execution-surface-only",
)

BOUNDARY_PHRASE_LINES = tuple(
    line
    for line in """
P4-M6.9
Entry Dependency Non-Activation Surface
P4-M6.9 Entry Dependency Non-Activation Surface
static entry dependency label surface
dependency-non-activation-surface-only
dependency-non-resolution-surface-only
dependency-non-traversal-surface-only
dependency-non-expansion-surface-only
dependency-non-requirement-generation-surface-only
dependency-non-ordering-surface-only
dependency-non-selection-surface-only
dependency-non-routing-surface-only
dependency-non-execution-surface-only
definition-only
declaration-only
read-only
inspection-only
no dependency activation
no dependency resolution
no dependency graph traversal
no dependency chain expansion
no dependency requirement inference
no dependency requirement generation
no dependency ordering
no dependency ranking
no dependency selection
no required dependency choice
no dependency blocking
no dependency unblocking
no dependency routing
no dependency execution
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
P4-M6.8 Entry Ambiguity Non-Inference Surface remains the direct prior reference
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

P4_M6_9_FIELD_IDS = tuple(
    line
    for line in """
p4_m6_9_stage
p4_m6_9_surface_id
p4_m6_9_direct_prior_reference
p4_m6_9_prior_reference_chain
p4_m6_9_entry_dependency_label_surface
p4_m6_9_dependency_non_activation_surface
p4_m6_9_dependency_non_resolution_surface
p4_m6_9_dependency_non_traversal_surface
p4_m6_9_dependency_non_expansion_surface
p4_m6_9_dependency_non_requirement_generation_surface
p4_m6_9_dependency_non_ordering_surface
p4_m6_9_dependency_non_ranking_surface
p4_m6_9_dependency_non_selection_surface
p4_m6_9_dependency_non_blocking_surface
p4_m6_9_dependency_non_routing_surface
p4_m6_9_dependency_non_execution_surface
p4_m6_9_readiness_non_evidence_surface
p4_m6_9_validation_non_input_surface
p4_m6_9_record_non_creation_surface
p4_m6_9_storage_non_persistence_surface
p4_m6_9_mutation_absence_surface
p4_m6_9_implementation_corridor_non_start_surface
p4_m6_9_operator_surface_guard
""".splitlines()
    if line
)

P4_M6_9_FIELD_DEFINITIONS = (
    (
        "P4-M6.9 stage",
        "Declares the P4-M6.9 Entry Dependency Non-Activation Surface stage.",
        "stage",
        "no implementation corridor start",
    ),
    (
        "P4-M6.9 surface id",
        "Declares the static surface id and memory-loop command label.",
        "identity",
        "no routing",
    ),
    (
        "P4-M6.9 direct prior reference",
        "Points directly to P4-M6.8 Entry Ambiguity Non-Inference Surface.",
        "lineage",
        "no dependency resolution",
    ),
    (
        "P4-M6.9 prior reference chain",
        "Preserves the P4-M6.8 through P4-M5.0 prior reference chain.",
        "lineage",
        "no dependency graph traversal",
    ),
    (
        "P4-M6.9 entry dependency label surface",
        "Declares only a static entry dependency label surface.",
        "label",
        "no dependency activation",
    ),
    (
        "P4-M6.9 dependency non-activation surface",
        "Declares that dependency labels do not activate dependencies.",
        "dependency-boundary",
        "no dependency activation",
    ),
    (
        "P4-M6.9 dependency non-resolution surface",
        "Declares that dependency labels do not resolve dependencies.",
        "dependency-boundary",
        "no dependency resolution",
    ),
    (
        "P4-M6.9 dependency non-traversal surface",
        "Declares that dependency labels do not traverse dependency graphs.",
        "dependency-boundary",
        "no dependency graph traversal",
    ),
    (
        "P4-M6.9 dependency non-expansion surface",
        "Declares that dependency labels do not expand dependency chains.",
        "dependency-boundary",
        "no dependency chain expansion",
    ),
    (
        "P4-M6.9 dependency non-requirement generation surface",
        "Declares that dependency labels do not infer or generate requirements.",
        "dependency-boundary",
        "no dependency requirement inference; no dependency requirement generation",
    ),
    (
        "P4-M6.9 dependency non-ordering surface",
        "Declares that dependency labels do not order dependencies.",
        "dependency-boundary",
        "no dependency ordering",
    ),
    (
        "P4-M6.9 dependency non-ranking surface",
        "Declares that dependency labels do not rank dependencies.",
        "dependency-boundary",
        "no dependency ranking",
    ),
    (
        "P4-M6.9 dependency non-selection surface",
        "Declares that dependency labels do not select dependencies.",
        "dependency-boundary",
        "no dependency selection; no required dependency choice",
    ),
    (
        "P4-M6.9 dependency non-blocking surface",
        "Declares that dependency labels do not block or unblock entry.",
        "dependency-boundary",
        "no dependency blocking; no dependency unblocking",
    ),
    (
        "P4-M6.9 dependency non-routing surface",
        "Declares that dependency labels do not route work.",
        "dependency-boundary",
        "no dependency routing",
    ),
    (
        "P4-M6.9 dependency non-execution surface",
        "Declares that dependency labels do not execute work.",
        "dependency-boundary",
        "no dependency execution",
    ),
    (
        "P4-M6.9 readiness non-evidence surface",
        "Declares that dependency labels are not readiness evidence.",
        "evidence-boundary",
        "no readiness evidence",
    ),
    (
        "P4-M6.9 validation non-input surface",
        "Declares that dependency labels are not validation input.",
        "validation-boundary",
        "no validation input",
    ),
    (
        "P4-M6.9 record non-creation surface",
        "Declares that dependency labels create no records.",
        "record-boundary",
        "no record creation",
    ),
    (
        "P4-M6.9 storage non-persistence surface",
        "Declares that dependency labels create no storage or persistence.",
        "storage-boundary",
        "no storage; no persistence",
    ),
    (
        "P4-M6.9 mutation absence surface",
        "Declares that dependency labels do not mutate memory or state.",
        "mutation-boundary",
        "no mutation",
    ),
    (
        "P4-M6.9 implementation corridor non-start surface",
        "Declares that the implementation corridor remains not started.",
        "implementation-boundary",
        "no implementation corridor start",
    ),
    (
        "P4-M6.9 operator surface guard",
        "Declares no UI, Operator Console, v7, productization, API, MCP, Connector, Agent, network, OAuth, credential, or secret inspection behavior.",
        "operator-boundary",
        "no UI; no Operator Console",
    ),
)

P4_M6_9_TRUE_STATUS_FLAGS = (
    "dependency_non_activation_surface_only",
    "dependency_non_resolution_surface_only",
    "dependency_non_traversal_surface_only",
    "dependency_non_expansion_surface_only",
    "dependency_non_requirement_generation_surface_only",
    "dependency_non_ordering_surface_only",
    "dependency_non_selection_surface_only",
    "dependency_non_routing_surface_only",
    "dependency_non_execution_surface_only",
)

P4_M6_9_FALSE_STATUS_FLAGS = (
    "p4_m6_9_dependency_activation_enabled",
    "p4_m6_9_dependency_resolution_enabled",
    "p4_m6_9_dependency_graph_traversal_enabled",
    "p4_m6_9_dependency_chain_expansion_enabled",
    "p4_m6_9_dependency_requirement_inference_enabled",
    "p4_m6_9_dependency_requirement_generation_enabled",
    "p4_m6_9_dependency_ordering_enabled",
    "p4_m6_9_dependency_ranking_enabled",
    "p4_m6_9_dependency_selection_enabled",
    "p4_m6_9_required_dependency_choice_enabled",
    "p4_m6_9_dependency_blocking_enabled",
    "p4_m6_9_dependency_unblocking_enabled",
    "p4_m6_9_dependency_routing_enabled",
    "p4_m6_9_dependency_execution_enabled",
    "p4_m6_9_readiness_evidence_enabled",
    "p4_m6_9_validation_input_enabled",
    "p4_m6_9_record_creation_enabled",
    "p4_m6_9_storage_enabled",
    "p4_m6_9_persistence_enabled",
    "p4_m6_9_mutation_enabled",
    "p4_m6_9_implementation_corridor_started",
    "p4_m6_9_api_call_enabled",
    "p4_m6_9_mcp_call_enabled",
    "p4_m6_9_connector_call_enabled",
    "p4_m6_9_agent_call_enabled",
    "p4_m6_9_network_enabled",
    "p4_m6_9_oauth_enabled",
    "p4_m6_9_credential_inspection_enabled",
    "p4_m6_9_secret_inspection_enabled",
)

TRUE_STATUS_FLAGS = P4_M6_8_TRUE_STATUS_FLAGS + P4_M6_9_TRUE_STATUS_FLAGS
FALSE_STATUS_FLAGS = P4_M6_8_FALSE_STATUS_FLAGS + P4_M6_9_FALSE_STATUS_FLAGS


def list_p4_m6_9_entry_dependency_non_activation_surface_fields() -> (
    tuple[P4M69EntryDependencyNonActivationSurfaceField, ...]
):
    return tuple(
        P4M69EntryDependencyNonActivationSurfaceField(
            field_order=index,
            field_id=field_id,
            field_name=definition[0],
            field_purpose=definition[1],
            p4_m6_9_entry_dependency_non_activation_surface_category=definition[2],
            p4_m6_9_entry_dependency_non_activation_surface_semantics_disabled=definition[3],
        )
        for index, (field_id, definition) in enumerate(
            zip(P4_M6_9_FIELD_IDS, P4_M6_9_FIELD_DEFINITIONS, strict=True),
            start=1,
        )
    )


def p4_m6_9_entry_dependency_non_activation_surface_field_ids() -> tuple[str, ...]:
    return tuple(
        field.field_id
        for field in list_p4_m6_9_entry_dependency_non_activation_surface_fields()
    )


def p4_m6_9_entry_dependency_non_activation_surface_as_dicts() -> (
    tuple[dict[str, Any], ...]
):
    return tuple(
        asdict(field)
        for field in list_p4_m6_9_entry_dependency_non_activation_surface_fields()
    )


def p4_m6_9_entry_dependency_non_activation_surface_status_shape() -> dict[str, Any]:
    return {
        "p4_m6_9_stage": "P4-M6.9 Entry Dependency Non-Activation Surface",
        "p4_m6_9_surface_id": MEMORY_LOOP_COMMAND,
        "p4_m6_9_direct_prior_reference": DIRECT_PRIOR_DEFINITION_LAYER_REFERENCE,
        "p4_m6_9_prior_reference_chain": PRIOR_DEFINITION_LAYER_REFERENCE_CHAIN,
        "p4_m6_9_entry_dependency_label_surface": (
            "static entry dependency label surface; definition-only; "
            "declaration-only; read-only; inspection-only"
        ),
        "p4_m6_9_dependency_non_activation_surface": (
            "dependency-non-activation-surface-only; no dependency activation"
        ),
        "p4_m6_9_dependency_non_resolution_surface": (
            "dependency-non-resolution-surface-only; no dependency resolution"
        ),
        "p4_m6_9_dependency_non_traversal_surface": (
            "dependency-non-traversal-surface-only; no dependency graph traversal"
        ),
        "p4_m6_9_dependency_non_expansion_surface": (
            "dependency-non-expansion-surface-only; no dependency chain expansion"
        ),
        "p4_m6_9_dependency_non_requirement_generation_surface": (
            "dependency-non-requirement-generation-surface-only; "
            "no dependency requirement inference; "
            "no dependency requirement generation"
        ),
        "p4_m6_9_dependency_non_ordering_surface": (
            "dependency-non-ordering-surface-only; no dependency ordering"
        ),
        "p4_m6_9_dependency_non_ranking_surface": "no dependency ranking",
        "p4_m6_9_dependency_non_selection_surface": (
            "dependency-non-selection-surface-only; "
            "no dependency selection; no required dependency choice"
        ),
        "p4_m6_9_dependency_non_blocking_surface": (
            "no dependency blocking; no dependency unblocking"
        ),
        "p4_m6_9_dependency_non_routing_surface": (
            "dependency-non-routing-surface-only; no dependency routing"
        ),
        "p4_m6_9_dependency_non_execution_surface": (
            "dependency-non-execution-surface-only; no dependency execution"
        ),
        "p4_m6_9_readiness_non_evidence_surface": "no readiness evidence",
        "p4_m6_9_validation_non_input_surface": "no validation input",
        "p4_m6_9_record_non_creation_surface": "no record creation",
        "p4_m6_9_storage_non_persistence_surface": "no storage; no persistence",
        "p4_m6_9_mutation_absence_surface": "no mutation",
        "p4_m6_9_implementation_corridor_non_start_surface": (
            "no implementation corridor start; no API; no MCP; no Connector; "
            "no Agent; no network; no OAuth; no credential; no secret inspection"
        ),
        "p4_m6_9_operator_surface_guard": (
            "no v7; no productization; no UI; no Operator Console"
        ),
    }


def _status_booleans() -> dict[str, bool]:
    return {
        **{flag: True for flag in TRUE_STATUS_FLAGS},
        **{flag: False for flag in FALSE_STATUS_FLAGS},
    }


def p4_m6_9_entry_dependency_non_activation_surface_report() -> dict[str, Any]:
    return {
        "stage": "P4-M6.9",
        "surface": "Entry Dependency Non-Activation Surface",
        "package_version": P4_M6_9_PACKAGE_VERSION,
        "command": MEMORY_LOOP_COMMAND_INVOCATION,
        "mode": "read-only declaration-only definition-only inspection-only",
        "direct_prior_reference": DIRECT_PRIOR_DEFINITION_LAYER_REFERENCE,
        "prior_reference_chain": PRIOR_DEFINITION_LAYER_REFERENCE_CHAIN,
        "status_direction": STATUS_DIRECTION,
        "boundary_phrases": BOUNDARY_PHRASE_LINES,
        "fields": p4_m6_9_entry_dependency_non_activation_surface_as_dicts(),
        "status_shape": p4_m6_9_entry_dependency_non_activation_surface_status_shape(),
        "true_flags": len(TRUE_STATUS_FLAGS),
        "false_flags": len(FALSE_STATUS_FLAGS),
        "status_booleans": _status_booleans(),
    }


def render_p4_m6_9_entry_dependency_non_activation_surface_markdown() -> str:
    report = p4_m6_9_entry_dependency_non_activation_surface_report()
    lines = [
        "# P4-M6.9 Entry Dependency Non-Activation Surface",
        "",
        "P4-M6.9 Entry Dependency Non-Activation Surface.",
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
        for field in list_p4_m6_9_entry_dependency_non_activation_surface_fields()
    )
    lines.extend(
        [
            "",
            "## Status Shape",
            "",
        ]
    )
    status_shape = p4_m6_9_entry_dependency_non_activation_surface_status_shape()
    lines.extend(f"- `{field_id}`: {status_shape[field_id]}" for field_id in P4_M6_9_FIELD_IDS)
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
            "This surface is static data only. It declares labels and boundaries; it does not activate dependencies, resolve dependencies, traverse dependency graphs, expand dependency chains, infer dependency requirements, generate dependency requirements, order dependencies, rank dependencies, select dependencies, choose required dependencies, block entry, unblock entry, route, execute, store, persist, mutate, call APIs, call MCP, call connectors, call agents, use network, inspect OAuth, inspect credentials, inspect secrets, add UI, add Operator Console, enter v7, or productize anything.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_p4_m6_9_entry_dependency_non_activation_surface_json() -> str:
    return json.dumps(
        p4_m6_9_entry_dependency_non_activation_surface_report(),
        indent=2,
        sort_keys=True,
    )


def run_p4_m6_9_entry_dependency_non_activation_surface_command(
    *, output_format: str = "markdown", workspace_root: str | Path | None = None
) -> str:
    # workspace_root is intentionally accepted only to prove the surface ignores storage.
    _ = workspace_root
    if output_format == "markdown":
        return render_p4_m6_9_entry_dependency_non_activation_surface_markdown()
    if output_format == "json":
        return render_p4_m6_9_entry_dependency_non_activation_surface_json()
    raise ValueError("output_format must be 'markdown' or 'json'")


P4_M6_9_ENTRY_DEPENDENCY_NON_ACTIVATION_SURFACE_BOUNDARY = (
    p4_m6_9_entry_dependency_non_activation_surface_report()
)
