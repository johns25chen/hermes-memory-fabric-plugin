from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .p4_m6_12_entry_safeguard_non_activation_surface import (
    FALSE_STATUS_FLAGS as P4_M6_12_FALSE_STATUS_FLAGS,
    TRUE_STATUS_FLAGS as P4_M6_12_TRUE_STATUS_FLAGS,
)


P4_M6_13_PACKAGE_VERSION = "6.16.0"
MEMORY_LOOP_COMMAND = "p4-m6-13-entry-definition-corridor-closure-review"
MEMORY_LOOP_COMMAND_INVOCATION = (
    "memory-loop p4-m6-13-entry-definition-corridor-closure-review"
)


@dataclass(frozen=True)
class P4M613EntryDefinitionCorridorClosureReviewField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    p4_m6_13_entry_definition_corridor_closure_review_category: str
    p4_m6_13_entry_definition_corridor_closure_review_semantics_disabled: str


DIRECT_PRIOR_DEFINITION_LAYER_REFERENCE = (
    "P4-M6.12 Entry Safeguard Non-Activation Surface"
)

P4_M6_CORRIDOR_REFERENCE_CHAIN = (
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
    "corridor-closure-review-surface-only",
    "entry-definition-inventory-review-surface-only",
    "lineage-alignment-review-surface-only",
    "operator-alignment-review-surface-only",
    "documentation-alignment-review-surface-only",
    "status-shape-alignment-review-surface-only",
    "closure-non-verdict-surface-only",
    "next-corridor-non-start-surface-only",
    "operator-guard-surface-only",
)

BOUNDARY_PHRASE_LINES = tuple(
    line
    for line in """
P4-M6.13
Entry Definition Corridor Closure Review
P4-M6.13 Entry Definition Corridor Closure Review
static entry definition corridor closure review surface
corridor-closure-review-surface-only
entry-definition-inventory-review-surface-only
lineage-alignment-review-surface-only
operator-alignment-review-surface-only
documentation-alignment-review-surface-only
status-shape-alignment-review-surface-only
closure-non-verdict-surface-only
next-corridor-non-start-surface-only
operator-guard-surface-only
definition-only
declaration-only
read-only
inspection-only
static declared review rows only
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
P4-M6.12 Entry Safeguard Non-Activation Surface remains the direct prior reference
P4-M6.11 Entry Risk Non-Mitigation Surface remains a preserved corridor reference
P4-M6.10 Entry Constraint Non-Enforcement Surface remains a preserved corridor reference
P4-M6.9 Entry Dependency Non-Activation Surface remains a preserved corridor reference
P4-M6.8 Entry Ambiguity Non-Inference Surface remains a preserved corridor reference
P4-M6.7 Entry Conflict Non-Resolution Surface remains a preserved corridor reference
P4-M6.6 Entry Exception Non-Override Surface remains a preserved corridor reference
P4-M6.5 Entry Escalation Non-Routing Surface remains a preserved corridor reference
P4-M6.4 Entry Rejection Non-Execution Surface remains a preserved corridor reference
P4-M6.3 Entry Deferral Non-Execution Surface remains a preserved corridor reference
P4-M6.2 Entry Acceptance Non-Evidence Surface remains a preserved corridor reference
P4-M6.1 Entry Preconditions Definition Surface remains a preserved corridor reference
P4-M6.0 Next Corridor Entry Boundary Contract remains a preserved corridor reference
P4-M5.6 Final Closure Handoff / Next Corridor Non-Start Index remains a preserved pre-corridor reference
P4-M5.5 Readiness Audit Closure / Non-Start Boundary Seal remains a preserved pre-corridor reference
P4-M5.4 API / MCP / Connector Cross-Surface Alignment Map remains a preserved pre-corridor reference
P4-M5.3 Connector Readiness Audit Surface Map remains a preserved pre-corridor reference
P4-M5.2 MCP Readiness Audit Surface Map remains a preserved pre-corridor reference
P4-M5.1 API Readiness Audit Surface Map remains a preserved pre-corridor reference
P4-M5.0 API / MCP / Connector Readiness Audit Boundary Contract remains a preserved pre-corridor reference
""".splitlines()
    if line
)

P4_M6_13_FIELD_IDS = tuple(
    line
    for line in """
p4_m6_13_stage
p4_m6_13_surface_id
p4_m6_13_direct_prior_reference
p4_m6_13_prior_reference_chain
p4_m6_13_corridor_scope
p4_m6_13_entry_definition_inventory_review_surface
p4_m6_13_lineage_alignment_review_surface
p4_m6_13_operator_alignment_review_surface
p4_m6_13_documentation_alignment_review_surface
p4_m6_13_status_shape_alignment_review_surface
p4_m6_13_closure_non_verdict_surface
p4_m6_13_closure_non_approval_surface
p4_m6_13_closure_non_authorization_surface
p4_m6_13_closure_non_confirmation_surface
p4_m6_13_entry_non_validation_surface
p4_m6_13_readiness_non_determination_surface
p4_m6_13_routing_non_execution_surface
p4_m6_13_record_non_creation_surface
p4_m6_13_storage_non_persistence_surface
p4_m6_13_mutation_absence_surface
p4_m6_13_next_corridor_non_start_surface
p4_m6_13_v7_non_start_surface
p4_m6_13_operator_surface_guard
""".splitlines()
    if line
)

P4_M6_13_FIELD_DEFINITIONS = (
    (
        "P4-M6.13 stage",
        "Declares the P4-M6.13 Entry Definition Corridor Closure Review stage.",
        "stage",
        "no next corridor start",
    ),
    (
        "P4-M6.13 surface id",
        "Declares the static surface id and memory-loop command label.",
        "identity",
        "no routing",
    ),
    (
        "P4-M6.13 direct prior reference",
        "Points directly to P4-M6.12 Entry Safeguard Non-Activation Surface.",
        "lineage",
        "no live repository inspection",
    ),
    (
        "P4-M6.13 prior reference chain",
        "Preserves the P4-M6.12 through P4-M5.0 reference chain.",
        "lineage",
        "no live workspace inspection",
    ),
    (
        "P4-M6.13 corridor scope",
        "Declares the static P4-M6.0 through P4-M6.12 entry definition corridor scope.",
        "scope",
        "no validation",
    ),
    (
        "P4-M6.13 entry definition inventory review surface",
        "Declares only a static entry definition inventory review row.",
        "review-row",
        "no inference",
    ),
    (
        "P4-M6.13 lineage alignment review surface",
        "Declares only a static lineage alignment review row.",
        "review-row",
        "no scoring",
    ),
    (
        "P4-M6.13 operator alignment review surface",
        "Declares only a static operator alignment review row.",
        "review-row",
        "no verdict",
    ),
    (
        "P4-M6.13 documentation alignment review surface",
        "Declares only a static documentation alignment review row.",
        "review-row",
        "no readiness determination",
    ),
    (
        "P4-M6.13 status shape alignment review surface",
        "Declares only a static status shape alignment review row.",
        "review-row",
        "no confirmation",
    ),
    (
        "P4-M6.13 closure non-verdict surface",
        "Declares that closure review produces no verdict.",
        "closure-boundary",
        "no verdict",
    ),
    (
        "P4-M6.13 closure non-approval surface",
        "Declares that closure review produces no approval.",
        "closure-boundary",
        "no approval",
    ),
    (
        "P4-M6.13 closure non-authorization surface",
        "Declares that closure review produces no authorization.",
        "closure-boundary",
        "no authorization",
    ),
    (
        "P4-M6.13 closure non-confirmation surface",
        "Declares that closure review produces no confirmation.",
        "closure-boundary",
        "no confirmation",
    ),
    (
        "P4-M6.13 entry non-validation surface",
        "Declares that closure review performs no validation.",
        "entry-boundary",
        "no validation",
    ),
    (
        "P4-M6.13 readiness non-determination surface",
        "Declares that closure review determines no readiness.",
        "readiness-boundary",
        "no readiness determination",
    ),
    (
        "P4-M6.13 routing non-execution surface",
        "Declares that closure review routes and executes nothing.",
        "execution-boundary",
        "no routing; no execution",
    ),
    (
        "P4-M6.13 record non-creation surface",
        "Declares that closure review creates no records.",
        "record-boundary",
        "no record creation",
    ),
    (
        "P4-M6.13 storage non-persistence surface",
        "Declares that closure review stores and persists nothing.",
        "storage-boundary",
        "no storage; no persistence",
    ),
    (
        "P4-M6.13 mutation absence surface",
        "Declares that closure review mutates no memory or state.",
        "mutation-boundary",
        "no mutation",
    ),
    (
        "P4-M6.13 next corridor non-start surface",
        "Declares that closure review starts no next corridor.",
        "corridor-boundary",
        "no next corridor start",
    ),
    (
        "P4-M6.13 v7 non-start surface",
        "Declares that closure review starts no v7.",
        "v7-boundary",
        "no v7",
    ),
    (
        "P4-M6.13 operator surface guard",
        "Declares no API, MCP, Connector, Agent, network, OAuth, credential, secret, UI, Operator Console, or productization behavior.",
        "operator-boundary",
        "no API; no MCP; no Connector; no Agent",
    ),
)

P4_M6_13_TRUE_STATUS_FLAGS = (
    "p4_m6_13_corridor_closure_review_surface_declared",
    "p4_m6_13_entry_definition_inventory_review_surface_declared",
    "p4_m6_13_lineage_alignment_review_surface_declared",
    "p4_m6_13_operator_alignment_review_surface_declared",
    "p4_m6_13_documentation_alignment_review_surface_declared",
    "p4_m6_13_status_shape_alignment_review_surface_declared",
    "p4_m6_13_closure_non_verdict_surface_declared",
    "p4_m6_13_next_corridor_non_start_surface_declared",
    "p4_m6_13_operator_guard_surface_declared",
)

P4_M6_13_FALSE_STATUS_FLAGS = (
    "p4_m6_13_live_validation_enabled",
    "p4_m6_13_inference_enabled",
    "p4_m6_13_scoring_enabled",
    "p4_m6_13_verdict_enabled",
    "p4_m6_13_readiness_determination_enabled",
    "p4_m6_13_approval_enabled",
    "p4_m6_13_authorization_enabled",
    "p4_m6_13_confirmation_enabled",
    "p4_m6_13_acceptance_enabled",
    "p4_m6_13_rejection_enabled",
    "p4_m6_13_deferral_enabled",
    "p4_m6_13_escalation_enabled",
    "p4_m6_13_override_enabled",
    "p4_m6_13_resolution_enabled",
    "p4_m6_13_safeguard_activation_enabled",
    "p4_m6_13_safeguard_enforcement_enabled",
    "p4_m6_13_prioritization_enabled",
    "p4_m6_13_selection_enabled",
    "p4_m6_13_recommendation_enabled",
    "p4_m6_13_routing_enabled",
    "p4_m6_13_execution_enabled",
    "p4_m6_13_entry_blocking_enabled",
    "p4_m6_13_entry_unblocking_enabled",
    "p4_m6_13_record_creation_enabled",
    "p4_m6_13_storage_enabled",
    "p4_m6_13_persistence_enabled",
    "p4_m6_13_mutation_enabled",
    "p4_m6_13_next_corridor_start_enabled",
    "p4_m6_13_v7_start_enabled",
)

TRUE_STATUS_FLAGS = P4_M6_12_TRUE_STATUS_FLAGS + P4_M6_13_TRUE_STATUS_FLAGS
FALSE_STATUS_FLAGS = P4_M6_12_FALSE_STATUS_FLAGS + P4_M6_13_FALSE_STATUS_FLAGS


def list_p4_m6_13_entry_definition_corridor_closure_review_fields() -> (
    tuple[P4M613EntryDefinitionCorridorClosureReviewField, ...]
):
    return tuple(
        P4M613EntryDefinitionCorridorClosureReviewField(
            field_order=index,
            field_id=field_id,
            field_name=definition[0],
            field_purpose=definition[1],
            p4_m6_13_entry_definition_corridor_closure_review_category=definition[2],
            p4_m6_13_entry_definition_corridor_closure_review_semantics_disabled=(
                definition[3]
            ),
        )
        for index, (field_id, definition) in enumerate(
            zip(P4_M6_13_FIELD_IDS, P4_M6_13_FIELD_DEFINITIONS, strict=True),
            start=1,
        )
    )


def p4_m6_13_entry_definition_corridor_closure_review_field_ids() -> tuple[str, ...]:
    return tuple(
        field.field_id
        for field in list_p4_m6_13_entry_definition_corridor_closure_review_fields()
    )


def p4_m6_13_entry_definition_corridor_closure_review_as_dicts() -> (
    tuple[dict[str, Any], ...]
):
    return tuple(
        asdict(field)
        for field in list_p4_m6_13_entry_definition_corridor_closure_review_fields()
    )


def p4_m6_13_entry_definition_corridor_closure_review_status_shape() -> (
    dict[str, Any]
):
    return {
        "p4_m6_13_stage": "P4-M6.13 Entry Definition Corridor Closure Review",
        "p4_m6_13_surface_id": MEMORY_LOOP_COMMAND,
        "p4_m6_13_direct_prior_reference": DIRECT_PRIOR_DEFINITION_LAYER_REFERENCE,
        "p4_m6_13_prior_reference_chain": PRIOR_DEFINITION_LAYER_REFERENCE_CHAIN,
        "p4_m6_13_corridor_scope": (
            "P4-M6.0 through P4-M6.12; static declared review rows only"
        ),
        "p4_m6_13_entry_definition_inventory_review_surface": (
            "entry-definition-inventory-review-surface-only; no validation"
        ),
        "p4_m6_13_lineage_alignment_review_surface": (
            "lineage-alignment-review-surface-only; no inference"
        ),
        "p4_m6_13_operator_alignment_review_surface": (
            "operator-alignment-review-surface-only; no routing"
        ),
        "p4_m6_13_documentation_alignment_review_surface": (
            "documentation-alignment-review-surface-only; no scoring"
        ),
        "p4_m6_13_status_shape_alignment_review_surface": (
            "status-shape-alignment-review-surface-only; no verdict"
        ),
        "p4_m6_13_closure_non_verdict_surface": (
            "closure-non-verdict-surface-only; no verdict"
        ),
        "p4_m6_13_closure_non_approval_surface": "no approval",
        "p4_m6_13_closure_non_authorization_surface": "no authorization",
        "p4_m6_13_closure_non_confirmation_surface": "no confirmation",
        "p4_m6_13_entry_non_validation_surface": "no validation",
        "p4_m6_13_readiness_non_determination_surface": (
            "no readiness determination"
        ),
        "p4_m6_13_routing_non_execution_surface": "no routing; no execution",
        "p4_m6_13_record_non_creation_surface": "no record creation",
        "p4_m6_13_storage_non_persistence_surface": "no storage; no persistence",
        "p4_m6_13_mutation_absence_surface": "no mutation",
        "p4_m6_13_next_corridor_non_start_surface": (
            "next-corridor-non-start-surface-only; no next corridor start"
        ),
        "p4_m6_13_v7_non_start_surface": "no v7",
        "p4_m6_13_operator_surface_guard": (
            "operator-guard-surface-only; no API; no MCP; no Connector; "
            "no Agent; no network; no OAuth; no credential inspection; "
            "no secret inspection; no UI; no Operator Console; no productization"
        ),
    }


def _status_booleans() -> dict[str, bool]:
    return {
        **{flag: True for flag in TRUE_STATUS_FLAGS},
        **{flag: False for flag in FALSE_STATUS_FLAGS},
    }


def p4_m6_13_entry_definition_corridor_closure_review_report() -> dict[str, Any]:
    return {
        "stage": "P4-M6.13",
        "surface": "Entry Definition Corridor Closure Review",
        "package_version": P4_M6_13_PACKAGE_VERSION,
        "command": MEMORY_LOOP_COMMAND_INVOCATION,
        "mode": "read-only declaration-only definition-only inspection-only",
        "direct_prior_reference": DIRECT_PRIOR_DEFINITION_LAYER_REFERENCE,
        "prior_reference_chain": PRIOR_DEFINITION_LAYER_REFERENCE_CHAIN,
        "p4_m6_corridor_reference_chain": P4_M6_CORRIDOR_REFERENCE_CHAIN,
        "p4_m5_pre_corridor_reference_chain": P4_M5_PRE_CORRIDOR_REFERENCE_CHAIN,
        "status_direction": STATUS_DIRECTION,
        "boundary_phrases": BOUNDARY_PHRASE_LINES,
        "fields": p4_m6_13_entry_definition_corridor_closure_review_as_dicts(),
        "status_shape": p4_m6_13_entry_definition_corridor_closure_review_status_shape(),
        "true_flags": len(TRUE_STATUS_FLAGS),
        "false_flags": len(FALSE_STATUS_FLAGS),
        "status_booleans": _status_booleans(),
    }


def render_p4_m6_13_entry_definition_corridor_closure_review_markdown() -> str:
    report = p4_m6_13_entry_definition_corridor_closure_review_report()
    lines = [
        "# P4-M6.13 Entry Definition Corridor Closure Review",
        "",
        "P4-M6.13 Entry Definition Corridor Closure Review.",
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
        f"- Preserved corridor reference: {reference}."
        for reference in P4_M6_CORRIDOR_REFERENCE_CHAIN
    )
    lines.extend(
        f"- Preserved pre-corridor reference: {reference}."
        for reference in P4_M5_PRE_CORRIDOR_REFERENCE_CHAIN
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
        for field in list_p4_m6_13_entry_definition_corridor_closure_review_fields()
    )
    lines.extend(
        [
            "",
            "## Status Shape",
            "",
        ]
    )
    status_shape = p4_m6_13_entry_definition_corridor_closure_review_status_shape()
    lines.extend(
        f"- `{field_id}`: {status_shape[field_id]}"
        for field_id in P4_M6_13_FIELD_IDS
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
            "This surface is static data only. It declares static review rows only; it does not inspect repositories, inspect workspaces, validate, infer, score, make verdicts, determine readiness, approve, authorize, confirm, accept, reject, defer, escalate, override, resolve, activate safeguards, enforce safeguards, prioritize, select, recommend, block entry, unblock entry, route, execute, create records, store, persist, mutate, start the next corridor, call APIs, call MCP, call connectors, call agents, use network, inspect OAuth, inspect credentials, inspect secrets, enter v7, productize, add UI, or add Operator Console behavior.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_p4_m6_13_entry_definition_corridor_closure_review_json() -> str:
    return json.dumps(
        p4_m6_13_entry_definition_corridor_closure_review_report(),
        indent=2,
        sort_keys=True,
    )


def run_p4_m6_13_entry_definition_corridor_closure_review_command(
    *, output_format: str = "markdown", workspace_root: str | Path | None = None
) -> str:
    # workspace_root is accepted only for operator interface consistency.
    _ = workspace_root
    if output_format == "markdown":
        return render_p4_m6_13_entry_definition_corridor_closure_review_markdown()
    if output_format == "json":
        return render_p4_m6_13_entry_definition_corridor_closure_review_json()
    raise ValueError("output_format must be 'markdown' or 'json'")


P4_M6_13_ENTRY_DEFINITION_CORRIDOR_CLOSURE_REVIEW_BOUNDARY = (
    p4_m6_13_entry_definition_corridor_closure_review_report()
)
