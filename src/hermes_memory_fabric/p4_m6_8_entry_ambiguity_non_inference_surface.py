from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .p4_m6_7_entry_conflict_non_resolution_surface import (
    FALSE_STATUS_FLAGS as P4_M6_7_FALSE_STATUS_FLAGS,
    TRUE_STATUS_FLAGS as P4_M6_7_TRUE_STATUS_FLAGS,
)


P4_M6_8_PACKAGE_VERSION = "6.16.0"
MEMORY_LOOP_COMMAND = "p4-m6-8-entry-ambiguity-non-inference-surface"
MEMORY_LOOP_COMMAND_INVOCATION = (
    "memory-loop p4-m6-8-entry-ambiguity-non-inference-surface"
)


@dataclass(frozen=True)
class P4M68EntryAmbiguityNonInferenceSurfaceField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    p4_m6_8_entry_ambiguity_non_inference_surface_category: str
    p4_m6_8_entry_ambiguity_non_inference_surface_semantics_disabled: str


DIRECT_PRIOR_DEFINITION_LAYER_REFERENCE = (
    "P4-M6.7 Entry Conflict Non-Resolution Surface"
)

PRIOR_DEFINITION_LAYER_REFERENCE_CHAIN = (
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
    "ambiguity-non-inference-surface-only",
    "ambiguity-non-disambiguation-surface-only",
    "ambiguity-non-completion-surface-only",
    "ambiguity-non-intent-judgment-surface-only",
    "ambiguity-non-meaning-selection-surface-only",
    "ambiguity-non-conclusion-surface-only",
    "ambiguity-non-routing-surface-only",
    "ambiguity-non-execution-surface-only",
)

BOUNDARY_PHRASE_LINES = tuple(
    line
    for line in """
P4-M6.8
Entry Ambiguity Non-Inference Surface
P4-M6.8 Entry Ambiguity Non-Inference Surface
static entry ambiguity label surface
ambiguity-non-inference-surface-only
ambiguity-non-disambiguation-surface-only
ambiguity-non-completion-surface-only
ambiguity-non-intent-judgment-surface-only
ambiguity-non-meaning-selection-surface-only
ambiguity-non-conclusion-surface-only
ambiguity-non-routing-surface-only
ambiguity-non-execution-surface-only
definition-only
declaration-only
read-only
inspection-only
no ambiguity inference
no ambiguity disambiguation
no ambiguity clarification
no ambiguity completion
no intent judgment
no meaning selection
no interpretation ranking
no candidate meaning choice
no ambiguity conclusion
no ambiguity verdict
no ambiguity validation
no ambiguity scoring
no ambiguity routing
no ambiguity execution
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
P4-M6.7 Entry Conflict Non-Resolution Surface remains the direct prior reference
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

P4_M6_8_FIELD_IDS = tuple(
    line
    for line in """
p4_m6_8_stage
p4_m6_8_surface_id
p4_m6_8_direct_prior_reference
p4_m6_8_prior_reference_chain
p4_m6_8_entry_ambiguity_label_surface
p4_m6_8_ambiguity_non_inference_surface
p4_m6_8_ambiguity_non_disambiguation_surface
p4_m6_8_ambiguity_non_completion_surface
p4_m6_8_ambiguity_non_intent_judgment_surface
p4_m6_8_ambiguity_non_meaning_selection_surface
p4_m6_8_ambiguity_non_ranking_surface
p4_m6_8_ambiguity_non_candidate_choice_surface
p4_m6_8_ambiguity_non_conclusion_surface
p4_m6_8_ambiguity_non_verdict_surface
p4_m6_8_ambiguity_non_routing_surface
p4_m6_8_ambiguity_non_execution_surface
p4_m6_8_readiness_non_evidence_surface
p4_m6_8_validation_non_input_surface
p4_m6_8_record_non_creation_surface
p4_m6_8_storage_non_persistence_surface
p4_m6_8_mutation_absence_surface
p4_m6_8_implementation_corridor_non_start_surface
p4_m6_8_operator_surface_guard
""".splitlines()
    if line
)

P4_M6_8_FIELD_DEFINITIONS = (
    (
        "P4-M6.8 stage",
        "Declares the P4-M6.8 Entry Ambiguity Non-Inference Surface stage.",
        "stage",
        "no implementation corridor start",
    ),
    (
        "P4-M6.8 surface id",
        "Declares the static surface id and memory-loop command label.",
        "identity",
        "no routing",
    ),
    (
        "P4-M6.8 direct prior reference",
        "Points directly to P4-M6.7 Entry Conflict Non-Resolution Surface.",
        "lineage",
        "no override",
    ),
    (
        "P4-M6.8 prior reference chain",
        "Preserves the P4-M6.7 through P4-M5.0 prior reference chain.",
        "lineage",
        "no bypass",
    ),
    (
        "P4-M6.8 entry ambiguity label surface",
        "Declares only a static entry ambiguity label surface.",
        "label",
        "no ambiguity clarification",
    ),
    (
        "P4-M6.8 ambiguity non-inference surface",
        "Declares that ambiguity labels do not infer ambiguity.",
        "ambiguity-boundary",
        "no ambiguity inference",
    ),
    (
        "P4-M6.8 ambiguity non-disambiguation surface",
        "Declares that ambiguity labels do not disambiguate ambiguity.",
        "ambiguity-boundary",
        "no ambiguity disambiguation",
    ),
    (
        "P4-M6.8 ambiguity non-completion surface",
        "Declares that ambiguity labels do not complete ambiguity.",
        "ambiguity-boundary",
        "no ambiguity completion",
    ),
    (
        "P4-M6.8 ambiguity non-intent judgment surface",
        "Declares that ambiguity labels do not judge intent.",
        "ambiguity-boundary",
        "no intent judgment",
    ),
    (
        "P4-M6.8 ambiguity non-meaning selection surface",
        "Declares that ambiguity labels do not select meaning.",
        "ambiguity-boundary",
        "no meaning selection",
    ),
    (
        "P4-M6.8 ambiguity non-ranking surface",
        "Declares that ambiguity labels do not rank interpretations.",
        "ambiguity-boundary",
        "no interpretation ranking",
    ),
    (
        "P4-M6.8 ambiguity non-candidate choice surface",
        "Declares that ambiguity labels do not choose a candidate meaning.",
        "ambiguity-boundary",
        "no candidate meaning choice",
    ),
    (
        "P4-M6.8 ambiguity non-conclusion surface",
        "Declares that ambiguity labels do not conclude ambiguity.",
        "ambiguity-boundary",
        "no ambiguity conclusion",
    ),
    (
        "P4-M6.8 ambiguity non-verdict surface",
        "Declares that ambiguity labels do not produce ambiguity verdicts.",
        "ambiguity-boundary",
        "no ambiguity verdict",
    ),
    (
        "P4-M6.8 ambiguity non-routing surface",
        "Declares that ambiguity labels do not route work.",
        "ambiguity-boundary",
        "no ambiguity routing",
    ),
    (
        "P4-M6.8 ambiguity non-execution surface",
        "Declares that ambiguity labels do not execute work.",
        "ambiguity-boundary",
        "no ambiguity execution",
    ),
    (
        "P4-M6.8 readiness non-evidence surface",
        "Declares that ambiguity labels are not readiness evidence.",
        "evidence-boundary",
        "no readiness evidence",
    ),
    (
        "P4-M6.8 validation non-input surface",
        "Declares that ambiguity labels are not validation input.",
        "validation-boundary",
        "no validation input; no ambiguity validation; no ambiguity scoring",
    ),
    (
        "P4-M6.8 record non-creation surface",
        "Declares that ambiguity labels create no records.",
        "record-boundary",
        "no record creation",
    ),
    (
        "P4-M6.8 storage non-persistence surface",
        "Declares that ambiguity labels create no storage or persistence.",
        "storage-boundary",
        "no storage; no persistence",
    ),
    (
        "P4-M6.8 mutation absence surface",
        "Declares that ambiguity labels do not mutate memory or state.",
        "mutation-boundary",
        "no mutation",
    ),
    (
        "P4-M6.8 implementation corridor non-start surface",
        "Declares that the implementation corridor remains not started.",
        "implementation-boundary",
        "no implementation corridor start",
    ),
    (
        "P4-M6.8 operator surface guard",
        "Declares no UI, Operator Console, v7, productization, API, MCP, Connector, Agent, network, OAuth, credential, or secret inspection behavior.",
        "operator-boundary",
        "no UI; no Operator Console",
    ),
)

P4_M6_8_TRUE_STATUS_FLAGS = (
    "p4_m6_8_entry_ambiguity_non_inference_surface_started",
    "ambiguity_non_inference_surface_only",
    "ambiguity_non_disambiguation_surface_only",
    "ambiguity_non_completion_surface_only",
    "ambiguity_non_intent_judgment_surface_only",
    "ambiguity_non_meaning_selection_surface_only",
    "ambiguity_non_conclusion_surface_only",
    "ambiguity_non_routing_surface_only",
    "ambiguity_non_execution_surface_only",
)

P4_M6_8_FALSE_STATUS_FLAGS = (
    "p4_m6_8_ambiguity_inference_enabled",
    "p4_m6_8_ambiguity_disambiguation_enabled",
    "p4_m6_8_ambiguity_clarification_enabled",
    "p4_m6_8_ambiguity_completion_enabled",
    "p4_m6_8_intent_judgment_enabled",
    "p4_m6_8_meaning_selection_enabled",
    "p4_m6_8_interpretation_ranking_enabled",
    "p4_m6_8_candidate_meaning_choice_enabled",
    "p4_m6_8_ambiguity_conclusion_enabled",
    "p4_m6_8_ambiguity_verdict_enabled",
    "p4_m6_8_ambiguity_validation_enabled",
    "p4_m6_8_ambiguity_scoring_enabled",
    "p4_m6_8_ambiguity_routing_enabled",
    "p4_m6_8_ambiguity_execution_enabled",
    "p4_m6_8_readiness_evidence_enabled",
    "p4_m6_8_validation_input_enabled",
    "p4_m6_8_record_creation_enabled",
    "p4_m6_8_storage_enabled",
    "p4_m6_8_persistence_enabled",
    "p4_m6_8_mutation_enabled",
    "p4_m6_8_implementation_corridor_started",
    "p4_m6_8_api_call_enabled",
    "p4_m6_8_mcp_call_enabled",
    "p4_m6_8_connector_call_enabled",
    "p4_m6_8_agent_call_enabled",
    "p4_m6_8_network_enabled",
    "p4_m6_8_oauth_enabled",
    "p4_m6_8_credential_inspection_enabled",
    "p4_m6_8_secret_inspection_enabled",
)

TRUE_STATUS_FLAGS = P4_M6_7_TRUE_STATUS_FLAGS + P4_M6_8_TRUE_STATUS_FLAGS
FALSE_STATUS_FLAGS = P4_M6_7_FALSE_STATUS_FLAGS + P4_M6_8_FALSE_STATUS_FLAGS


def list_p4_m6_8_entry_ambiguity_non_inference_surface_fields() -> (
    tuple[P4M68EntryAmbiguityNonInferenceSurfaceField, ...]
):
    return tuple(
        P4M68EntryAmbiguityNonInferenceSurfaceField(
            field_order=index,
            field_id=field_id,
            field_name=definition[0],
            field_purpose=definition[1],
            p4_m6_8_entry_ambiguity_non_inference_surface_category=definition[2],
            p4_m6_8_entry_ambiguity_non_inference_surface_semantics_disabled=definition[3],
        )
        for index, (field_id, definition) in enumerate(
            zip(P4_M6_8_FIELD_IDS, P4_M6_8_FIELD_DEFINITIONS, strict=True),
            start=1,
        )
    )


def p4_m6_8_entry_ambiguity_non_inference_surface_field_ids() -> tuple[str, ...]:
    return tuple(
        field.field_id
        for field in list_p4_m6_8_entry_ambiguity_non_inference_surface_fields()
    )


def p4_m6_8_entry_ambiguity_non_inference_surface_as_dicts() -> (
    tuple[dict[str, Any], ...]
):
    return tuple(
        asdict(field)
        for field in list_p4_m6_8_entry_ambiguity_non_inference_surface_fields()
    )


def p4_m6_8_entry_ambiguity_non_inference_surface_status_shape() -> dict[str, Any]:
    return {
        "p4_m6_8_stage": "P4-M6.8 Entry Ambiguity Non-Inference Surface",
        "p4_m6_8_surface_id": MEMORY_LOOP_COMMAND,
        "p4_m6_8_direct_prior_reference": DIRECT_PRIOR_DEFINITION_LAYER_REFERENCE,
        "p4_m6_8_prior_reference_chain": PRIOR_DEFINITION_LAYER_REFERENCE_CHAIN,
        "p4_m6_8_entry_ambiguity_label_surface": (
            "static entry ambiguity label surface; definition-only; "
            "declaration-only; read-only; inspection-only"
        ),
        "p4_m6_8_ambiguity_non_inference_surface": (
            "ambiguity-non-inference-surface-only; no ambiguity inference"
        ),
        "p4_m6_8_ambiguity_non_disambiguation_surface": (
            "ambiguity-non-disambiguation-surface-only; "
            "no ambiguity disambiguation; no ambiguity clarification"
        ),
        "p4_m6_8_ambiguity_non_completion_surface": (
            "ambiguity-non-completion-surface-only; no ambiguity completion"
        ),
        "p4_m6_8_ambiguity_non_intent_judgment_surface": (
            "ambiguity-non-intent-judgment-surface-only; no intent judgment"
        ),
        "p4_m6_8_ambiguity_non_meaning_selection_surface": (
            "ambiguity-non-meaning-selection-surface-only; no meaning selection"
        ),
        "p4_m6_8_ambiguity_non_ranking_surface": "no interpretation ranking",
        "p4_m6_8_ambiguity_non_candidate_choice_surface": (
            "no candidate meaning choice"
        ),
        "p4_m6_8_ambiguity_non_conclusion_surface": (
            "ambiguity-non-conclusion-surface-only; no ambiguity conclusion"
        ),
        "p4_m6_8_ambiguity_non_verdict_surface": "no ambiguity verdict",
        "p4_m6_8_ambiguity_non_routing_surface": (
            "ambiguity-non-routing-surface-only; no ambiguity routing"
        ),
        "p4_m6_8_ambiguity_non_execution_surface": (
            "ambiguity-non-execution-surface-only; no ambiguity execution"
        ),
        "p4_m6_8_readiness_non_evidence_surface": "no readiness evidence",
        "p4_m6_8_validation_non_input_surface": (
            "no validation input; no ambiguity validation; no ambiguity scoring"
        ),
        "p4_m6_8_record_non_creation_surface": "no record creation",
        "p4_m6_8_storage_non_persistence_surface": "no storage; no persistence",
        "p4_m6_8_mutation_absence_surface": "no mutation",
        "p4_m6_8_implementation_corridor_non_start_surface": (
            "no implementation corridor start; no API; no MCP; no Connector; "
            "no Agent; no network; no OAuth; no credential; no secret inspection"
        ),
        "p4_m6_8_operator_surface_guard": (
            "no v7; no productization; no UI; no Operator Console"
        ),
    }


def _status_booleans() -> dict[str, bool]:
    return {
        **{flag: True for flag in TRUE_STATUS_FLAGS},
        **{flag: False for flag in FALSE_STATUS_FLAGS},
    }


def p4_m6_8_entry_ambiguity_non_inference_surface_report() -> dict[str, Any]:
    return {
        "stage": "P4-M6.8",
        "surface": "Entry Ambiguity Non-Inference Surface",
        "package_version": P4_M6_8_PACKAGE_VERSION,
        "command": MEMORY_LOOP_COMMAND_INVOCATION,
        "mode": "read-only declaration-only definition-only inspection-only",
        "direct_prior_reference": DIRECT_PRIOR_DEFINITION_LAYER_REFERENCE,
        "prior_reference_chain": PRIOR_DEFINITION_LAYER_REFERENCE_CHAIN,
        "status_direction": STATUS_DIRECTION,
        "boundary_phrases": BOUNDARY_PHRASE_LINES,
        "fields": p4_m6_8_entry_ambiguity_non_inference_surface_as_dicts(),
        "status_shape": p4_m6_8_entry_ambiguity_non_inference_surface_status_shape(),
        "true_flags": len(TRUE_STATUS_FLAGS),
        "false_flags": len(FALSE_STATUS_FLAGS),
        "status_booleans": _status_booleans(),
    }


def render_p4_m6_8_entry_ambiguity_non_inference_surface_markdown() -> str:
    report = p4_m6_8_entry_ambiguity_non_inference_surface_report()
    lines = [
        "# P4-M6.8 Entry Ambiguity Non-Inference Surface",
        "",
        "P4-M6.8 Entry Ambiguity Non-Inference Surface.",
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
        for field in list_p4_m6_8_entry_ambiguity_non_inference_surface_fields()
    )
    lines.extend(
        [
            "",
            "## Status Shape",
            "",
        ]
    )
    status_shape = p4_m6_8_entry_ambiguity_non_inference_surface_status_shape()
    lines.extend(f"- `{field_id}`: {status_shape[field_id]}" for field_id in P4_M6_8_FIELD_IDS)
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
            "This surface is static data only. It declares labels and boundaries; it does not infer, disambiguate, clarify, complete, judge intent, select meaning, rank interpretations, choose candidate meaning, conclude, produce verdicts, validate, score, route, execute, store, persist, mutate, call APIs, call MCP, call connectors, call agents, use network, inspect OAuth, inspect credentials, inspect secrets, add UI, add Operator Console, enter v7, or productize anything.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_p4_m6_8_entry_ambiguity_non_inference_surface_json() -> str:
    return json.dumps(
        p4_m6_8_entry_ambiguity_non_inference_surface_report(),
        indent=2,
        sort_keys=True,
    )


def run_p4_m6_8_entry_ambiguity_non_inference_surface_command(
    *, output_format: str = "markdown", workspace_root: str | Path | None = None
) -> str:
    # workspace_root is intentionally accepted only to prove the surface ignores storage.
    _ = workspace_root
    if output_format == "markdown":
        return render_p4_m6_8_entry_ambiguity_non_inference_surface_markdown()
    if output_format == "json":
        return render_p4_m6_8_entry_ambiguity_non_inference_surface_json()
    raise ValueError("output_format must be 'markdown' or 'json'")


P4_M6_8_ENTRY_AMBIGUITY_NON_INFERENCE_SURFACE_BOUNDARY = (
    p4_m6_8_entry_ambiguity_non_inference_surface_report()
)
