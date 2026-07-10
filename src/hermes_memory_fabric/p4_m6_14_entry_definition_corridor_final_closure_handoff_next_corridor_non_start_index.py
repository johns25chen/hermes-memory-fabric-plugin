from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .p4_m6_13_entry_definition_corridor_closure_review import (
    FALSE_STATUS_FLAGS as P4_M6_13_FALSE_STATUS_FLAGS,
    TRUE_STATUS_FLAGS as P4_M6_13_TRUE_STATUS_FLAGS,
)


P4_M6_14_PACKAGE_VERSION = "6.16.0"
MEMORY_LOOP_COMMAND = (
    "p4-m6-14-entry-definition-corridor-final-closure-handoff-"
    "next-corridor-non-start-index"
)
MEMORY_LOOP_COMMAND_INVOCATION = (
    "memory-loop p4-m6-14-entry-definition-corridor-final-closure-handoff-"
    "next-corridor-non-start-index"
)


@dataclass(frozen=True)
class P4M614EntryDefinitionCorridorFinalClosureHandoffNextCorridorNonStartIndexField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_category: str
    p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_semantics_disabled: str


DIRECT_PRIOR_DEFINITION_LAYER_REFERENCE = (
    "P4-M6.13 Entry Definition Corridor Closure Review"
)

P4_M6_CORRIDOR_REFERENCE_CHAIN = (
    "P4-M6.13 Entry Definition Corridor Closure Review",
    "P4-M6.12 Entry Safeguard Non-Activation Surface",
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
)

P4_M5_PRE_CORRIDOR_REFERENCE_CHAIN = (
    "P4-M5.6 Final Closure Handoff / Next Corridor Non-Start Index",
    "P4-M5.5 Readiness Audit Closure / Non-Start Boundary Seal",
    "P4-M5.4 API / MCP / Connector Cross-Surface Alignment Map",
    "P4-M5.3 Connector Readiness Audit Surface Map",
    "P4-M5.2 MCP Readiness Audit Surface Map",
    "P4-M5.1 API Readiness Audit Surface Map",
    "P4-M5.0 API / MCP / Connector Readiness Audit Boundary Contract",
)

PRIOR_DEFINITION_LAYER_REFERENCE_CHAIN = (
    *P4_M6_CORRIDOR_REFERENCE_CHAIN,
    *P4_M5_PRE_CORRIDOR_REFERENCE_CHAIN,
)

STATUS_DIRECTION = (
    "final-closure-handoff-index-only",
    "corridor-closed-declaration-index-only",
    "closure-review-reference-index-only",
    "corridor-lineage-index-only",
    "operator-alignment-index-only",
    "documentation-alignment-index-only",
    "status-shape-alignment-index-only",
    "next-corridor-non-start-index-only",
    "operator-guard-index-only",
)

BOUNDARY_PHRASE_LINES = tuple(
    line
    for line in """
P4-M6.14
Entry Definition Corridor Final Closure Handoff
Next Corridor Non-Start Index
P4-M6.14 Entry Definition Corridor Final Closure Handoff / Next Corridor Non-Start Index
static entry definition corridor final closure handoff and next corridor non-start index
final-closure-handoff-index-only
corridor-closed-declaration-index-only
closure-review-reference-index-only
corridor-lineage-index-only
operator-alignment-index-only
documentation-alignment-index-only
status-shape-alignment-index-only
next-corridor-non-start-index-only
operator-guard-index-only
definition-only
declaration-only
read-only
inspection-only
static declared index rows only
P4-M6 corridor closed
handoff declaration only
P4-M6.13 closure review remains the direct prior reference
no repeated closure review
no live repository inspection
no live workspace inspection
no validation
no inference
no scoring
no verdict
no readiness determination
no approval
no authorization
no confirmation
no acceptance
no rejection
no deferral
no escalation
no override
no resolution
no safeguard activation
no safeguard enforcement
no prioritization
no selection
no recommendation
no entry blocking
no entry unblocking
no routing
no execution
no record creation
no storage
no persistence
no mutation
no next corridor start
no P4-M7.0 start
no API
no MCP
no Connector
no Agent
no network
no OAuth
no credential inspection
no secret inspection
no v7
no productization
no UI
no Operator Console
""".splitlines()
    if line
)

P4_M6_14_FIELD_IDS = tuple(
    line
    for line in """
p4_m6_14_stage
p4_m6_14_surface_id
p4_m6_14_direct_prior_reference
p4_m6_14_prior_reference_chain
p4_m6_14_closed_corridor_scope
p4_m6_14_final_closure_handoff_index
p4_m6_14_corridor_closed_declaration_index
p4_m6_14_closure_review_reference_index
p4_m6_14_corridor_lineage_index
p4_m6_14_operator_alignment_index
p4_m6_14_documentation_alignment_index
p4_m6_14_status_shape_alignment_index
p4_m6_14_final_closure_non_verdict_index
p4_m6_14_final_closure_non_approval_index
p4_m6_14_final_closure_non_authorization_index
p4_m6_14_final_closure_non_confirmation_index
p4_m6_14_entry_non_validation_index
p4_m6_14_readiness_non_determination_index
p4_m6_14_routing_non_execution_index
p4_m6_14_record_non_creation_index
p4_m6_14_storage_non_persistence_index
p4_m6_14_mutation_absence_index
p4_m6_14_next_corridor_and_v7_non_start_operator_guard
""".splitlines()
    if line
)

P4_M6_14_FIELD_DEFINITIONS = (
    ("P4-M6.14 stage", "Declares the P4-M6.14 final closure handoff stage.", "stage", "no next corridor start"),
    ("P4-M6.14 surface id", "Declares the static memory-loop command label.", "identity", "no routing"),
    ("P4-M6.14 direct prior reference", "References P4-M6.13 as the completed closure review.", "lineage", "no repeated closure review"),
    ("P4-M6.14 prior reference chain", "Preserves the P4-M6.13 through P4-M5.0 static lineage.", "lineage", "no live repository inspection"),
    ("P4-M6.14 closed corridor scope", "Declares P4-M6.0 through P4-M6.13 closed as an index only.", "scope", "no live workspace inspection"),
    ("P4-M6.14 final closure handoff index", "Declares a static final closure handoff index row.", "index-row", "no validation"),
    ("P4-M6.14 corridor closed declaration index", "Declares P4-M6 corridor closed as declaration-only.", "index-row", "no inference"),
    ("P4-M6.14 closure review reference index", "References the P4-M6.13 closure review without repeating it.", "index-row", "no scoring"),
    ("P4-M6.14 corridor lineage index", "Preserves static P4-M6.0 through P4-M6.13 lineage.", "index-row", "no verdict"),
    ("P4-M6.14 operator alignment index", "Declares operator alignment as a static index row.", "index-row", "no readiness determination"),
    ("P4-M6.14 documentation alignment index", "Declares documentation alignment as a static index row.", "index-row", "no approval"),
    ("P4-M6.14 status shape alignment index", "Declares status shape alignment as a static index row.", "index-row", "no confirmation"),
    ("P4-M6.14 final closure non-verdict index", "Declares final closure produces no verdict.", "closure-boundary", "no verdict"),
    ("P4-M6.14 final closure non-approval index", "Declares final closure produces no approval.", "closure-boundary", "no approval"),
    ("P4-M6.14 final closure non-authorization index", "Declares final closure produces no authorization.", "closure-boundary", "no authorization"),
    ("P4-M6.14 final closure non-confirmation index", "Declares final closure produces no confirmation.", "closure-boundary", "no confirmation"),
    ("P4-M6.14 entry non-validation index", "Declares final closure performs no validation.", "entry-boundary", "no validation"),
    ("P4-M6.14 readiness non-determination index", "Declares final closure determines no readiness.", "readiness-boundary", "no readiness determination"),
    ("P4-M6.14 routing non-execution index", "Declares final closure routes and executes nothing.", "execution-boundary", "no routing; no execution"),
    ("P4-M6.14 record non-creation index", "Declares final closure creates no records.", "record-boundary", "no record creation"),
    ("P4-M6.14 storage non-persistence index", "Declares final closure stores and persists nothing.", "storage-boundary", "no storage; no persistence"),
    ("P4-M6.14 mutation absence index", "Declares final closure mutates no memory or state.", "mutation-boundary", "no mutation"),
    ("P4-M6.14 next corridor and v7 non-start operator guard", "Declares no next corridor start, no P4-M7.0 start, no v7, and no API/MCP/Connector/Agent/network/OAuth/credential/secret/UI/Operator Console/productization behavior.", "operator-boundary", "no next corridor start; no P4-M7.0 start; no v7"),
)

P4_M6_14_TRUE_STATUS_FLAGS = (
    "p4_m6_14_final_closure_handoff_index_declared",
    "p4_m6_14_corridor_closed_declaration_index_declared",
    "p4_m6_14_closure_review_reference_index_declared",
    "p4_m6_14_corridor_lineage_index_declared",
    "p4_m6_14_operator_alignment_index_declared",
    "p4_m6_14_documentation_alignment_index_declared",
    "p4_m6_14_status_shape_alignment_index_declared",
    "p4_m6_14_next_corridor_non_start_index_declared",
    "p4_m6_14_operator_guard_index_declared",
)

P4_M6_14_FALSE_STATUS_FLAGS = (
    "p4_m6_14_live_validation_enabled",
    "p4_m6_14_inference_enabled",
    "p4_m6_14_scoring_enabled",
    "p4_m6_14_verdict_enabled",
    "p4_m6_14_readiness_determination_enabled",
    "p4_m6_14_approval_enabled",
    "p4_m6_14_authorization_enabled",
    "p4_m6_14_confirmation_enabled",
    "p4_m6_14_acceptance_enabled",
    "p4_m6_14_rejection_enabled",
    "p4_m6_14_deferral_enabled",
    "p4_m6_14_escalation_enabled",
    "p4_m6_14_override_enabled",
    "p4_m6_14_resolution_enabled",
    "p4_m6_14_safeguard_activation_enabled",
    "p4_m6_14_safeguard_enforcement_enabled",
    "p4_m6_14_prioritization_enabled",
    "p4_m6_14_selection_enabled",
    "p4_m6_14_recommendation_enabled",
    "p4_m6_14_routing_enabled",
    "p4_m6_14_execution_enabled",
    "p4_m6_14_entry_blocking_enabled",
    "p4_m6_14_entry_unblocking_enabled",
    "p4_m6_14_record_creation_enabled",
    "p4_m6_14_storage_enabled",
    "p4_m6_14_persistence_enabled",
    "p4_m6_14_mutation_enabled",
    "p4_m6_14_next_corridor_start_enabled",
    "p4_m6_14_v7_start_enabled",
)

TRUE_STATUS_FLAGS = P4_M6_13_TRUE_STATUS_FLAGS + P4_M6_14_TRUE_STATUS_FLAGS
FALSE_STATUS_FLAGS = P4_M6_13_FALSE_STATUS_FLAGS + P4_M6_14_FALSE_STATUS_FLAGS


def list_p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_fields() -> tuple[P4M614EntryDefinitionCorridorFinalClosureHandoffNextCorridorNonStartIndexField, ...]:
    return tuple(
        P4M614EntryDefinitionCorridorFinalClosureHandoffNextCorridorNonStartIndexField(
            field_order=index,
            field_id=field_id,
            field_name=definition[0],
            field_purpose=definition[1],
            p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_category=definition[2],
            p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_semantics_disabled=definition[3],
        )
        for index, (field_id, definition) in enumerate(
            zip(P4_M6_14_FIELD_IDS, P4_M6_14_FIELD_DEFINITIONS, strict=True),
            start=1,
        )
    )


def p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_field_ids() -> tuple[str, ...]:
    return tuple(
        field.field_id
        for field in list_p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_fields()
    )


def p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_as_dicts() -> tuple[dict[str, Any], ...]:
    return tuple(
        asdict(field)
        for field in list_p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_fields()
    )


def p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_status_shape() -> dict[str, Any]:
    return {
        "p4_m6_14_stage": "P4-M6.14 Entry Definition Corridor Final Closure Handoff / Next Corridor Non-Start Index",
        "p4_m6_14_surface_id": MEMORY_LOOP_COMMAND,
        "p4_m6_14_direct_prior_reference": DIRECT_PRIOR_DEFINITION_LAYER_REFERENCE,
        "p4_m6_14_prior_reference_chain": PRIOR_DEFINITION_LAYER_REFERENCE_CHAIN,
        "p4_m6_14_closed_corridor_scope": "P4-M6.0 through P4-M6.13; P4-M6 corridor closed; static declared index rows only",
        "p4_m6_14_final_closure_handoff_index": "final-closure-handoff-index-only; handoff declaration only",
        "p4_m6_14_corridor_closed_declaration_index": "corridor-closed-declaration-index-only; P4-M6 corridor closed",
        "p4_m6_14_closure_review_reference_index": "closure-review-reference-index-only; P4-M6.13 closure review remains the direct prior reference; no repeated closure review",
        "p4_m6_14_corridor_lineage_index": "corridor-lineage-index-only; static P4-M6.0 through P4-M6.13 lineage",
        "p4_m6_14_operator_alignment_index": "operator-alignment-index-only; no routing",
        "p4_m6_14_documentation_alignment_index": "documentation-alignment-index-only; no scoring",
        "p4_m6_14_status_shape_alignment_index": "status-shape-alignment-index-only; no verdict",
        "p4_m6_14_final_closure_non_verdict_index": "no verdict",
        "p4_m6_14_final_closure_non_approval_index": "no approval",
        "p4_m6_14_final_closure_non_authorization_index": "no authorization",
        "p4_m6_14_final_closure_non_confirmation_index": "no confirmation",
        "p4_m6_14_entry_non_validation_index": "no validation",
        "p4_m6_14_readiness_non_determination_index": "no readiness determination",
        "p4_m6_14_routing_non_execution_index": "no routing; no execution",
        "p4_m6_14_record_non_creation_index": "no record creation",
        "p4_m6_14_storage_non_persistence_index": "no storage; no persistence",
        "p4_m6_14_mutation_absence_index": "no mutation",
        "p4_m6_14_next_corridor_and_v7_non_start_operator_guard": "next-corridor-non-start-index-only; operator-guard-index-only; no next corridor start; no P4-M7.0 start; no v7; no API; no MCP; no Connector; no Agent; no network; no OAuth; no credential inspection; no secret inspection; no productization; no UI; no Operator Console",
    }


def _status_booleans() -> dict[str, bool]:
    return {
        **{flag: True for flag in TRUE_STATUS_FLAGS},
        **{flag: False for flag in FALSE_STATUS_FLAGS},
    }


def p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_report() -> dict[str, Any]:
    return {
        "stage": "P4-M6.14",
        "surface": "Entry Definition Corridor Final Closure Handoff / Next Corridor Non-Start Index",
        "package_version": P4_M6_14_PACKAGE_VERSION,
        "command": MEMORY_LOOP_COMMAND_INVOCATION,
        "mode": "read-only declaration-only definition-only inspection-only",
        "direct_prior_reference": DIRECT_PRIOR_DEFINITION_LAYER_REFERENCE,
        "prior_reference_chain": PRIOR_DEFINITION_LAYER_REFERENCE_CHAIN,
        "p4_m6_corridor_reference_chain": P4_M6_CORRIDOR_REFERENCE_CHAIN,
        "p4_m5_pre_corridor_reference_chain": P4_M5_PRE_CORRIDOR_REFERENCE_CHAIN,
        "status_direction": STATUS_DIRECTION,
        "boundary_phrases": BOUNDARY_PHRASE_LINES,
        "fields": p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_as_dicts(),
        "status_shape": p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_status_shape(),
        "true_flags": len(TRUE_STATUS_FLAGS),
        "false_flags": len(FALSE_STATUS_FLAGS),
        "status_booleans": _status_booleans(),
    }


def render_p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_markdown() -> str:
    report = p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_report()
    lines = [
        "# P4-M6.14 Entry Definition Corridor Final Closure Handoff / Next Corridor Non-Start Index",
        "",
        "P4-M6.14 Entry Definition Corridor Final Closure Handoff / Next Corridor Non-Start Index.",
        "",
        f"Command: `{report['command']}`.",
        "",
        "## Boundary Phrases",
        "",
    ]
    lines.extend(f"- {phrase}." for phrase in BOUNDARY_PHRASE_LINES)
    lines.extend(["", "## Status Direction", ""])
    lines.extend(f"- {direction}." for direction in STATUS_DIRECTION)
    lines.extend(["", "## Prior Reference Chain", "", f"- Direct prior reference: {DIRECT_PRIOR_DEFINITION_LAYER_REFERENCE}."])
    lines.extend(f"- Preserved corridor reference: {reference}." for reference in P4_M6_CORRIDOR_REFERENCE_CHAIN)
    lines.extend(f"- Preserved pre-corridor reference: {reference}." for reference in P4_M5_PRE_CORRIDOR_REFERENCE_CHAIN)
    lines.extend(["", "## Semantic Field IDs", ""])
    lines.extend(
        f"- `{field.field_id}`: {field.field_purpose}"
        for field in list_p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_fields()
    )
    status_shape = p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_status_shape()
    lines.extend(["", "## Status Shape", ""])
    lines.extend(f"- `{field_id}`: {status_shape[field_id]}" for field_id in P4_M6_14_FIELD_IDS)
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
            "This surface is a static entry definition corridor final closure handoff and next corridor non-start index. It is definition-only, declaration-only, read-only, inspection-only, and contains static declared index rows only.",
            "",
            "It declares P4-M6 corridor closed as handoff declaration only. P4-M6.13 closure review remains the direct prior reference; this surface performs no repeated closure review. It does not inspect repositories, inspect workspaces, validate, infer, score, make verdicts, determine readiness, approve, authorize, confirm, accept, reject, defer, escalate, override, resolve, activate safeguards, enforce safeguards, prioritize, select, recommend, block entry, unblock entry, route, execute, create records, store, persist, mutate, start the next corridor, start P4-M7.0, call APIs, call MCP, call connectors, call agents, use network, inspect OAuth, inspect credentials, inspect secrets, enter v7, productize, add UI, or add Operator Console behavior.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_json() -> str:
    return json.dumps(
        p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_report(),
        indent=2,
        sort_keys=True,
    )


def run_p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_command(
    *, output_format: str = "markdown", workspace_root: str | Path | None = None
) -> str:
    _ = workspace_root
    if output_format == "markdown":
        return render_p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_markdown()
    if output_format == "json":
        return render_p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_json()
    raise ValueError("output_format must be 'markdown' or 'json'")


P4_M6_14_ENTRY_DEFINITION_CORRIDOR_FINAL_CLOSURE_HANDOFF_NEXT_CORRIDOR_NON_START_INDEX_BOUNDARY = (
    p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_report()
)
