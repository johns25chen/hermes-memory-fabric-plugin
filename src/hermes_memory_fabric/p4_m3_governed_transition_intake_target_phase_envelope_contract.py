from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence

from .p4_m2_closure_handoff_contract import closure_handoff_contract_field_ids
from .p4_m2_final_non_execution_boundary_audit import (
    final_non_execution_boundary_audit_field_ids,
)
from .p4_m3_governed_transition_intake_boundary_contract import (
    governed_transition_intake_boundary_contract_field_ids,
)
from .p4_m3_governed_transition_intake_declared_human_context_envelope_contract import (
    governed_transition_intake_declared_human_context_envelope_contract_field_ids,
)
from .p4_m3_governed_transition_intake_evidence_reference_envelope_contract import (
    governed_transition_intake_evidence_reference_envelope_contract_field_ids,
)
from .p4_m3_governed_transition_intake_request_envelope_contract import (
    governed_transition_intake_request_envelope_contract_field_ids,
)


P4_M3_4_PACKAGE_VERSION = "6.16.0"


@dataclass(frozen=True)
class GovernedTransitionIntakeTargetPhaseEnvelopeContractField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    p4_m3_target_phase_envelope_contract_category: str
    p4_m3_target_phase_envelope_semantics_disabled: str


PRIOR_DEFINITION_LAYER_REFERENCES = (
    "P4-M3.3 Governed Transition Intake Declared Human Context Envelope Contract",
    "P4-M3.2 Governed Transition Intake Evidence Reference Envelope Contract",
    "P4-M3.1 Governed Transition Intake Request Envelope Contract",
    "P4-M3.0 Governed Transition Intake Boundary Contract",
    "P4-M2.17 P4-M2 Closure Handoff Contract",
    "P4-M2.16 Final Non-Execution Boundary Audit",
)


BOUNDARY_PHRASE_LINES = tuple(
    line
    for line in """
P4-M3.4
Governed Transition Intake Target Phase Envelope Contract
read-only
definition-only
inspection-only
P4-M3.4 target phase envelope definition only
P4-M3.3 Governed Transition Intake Declared Human Context Envelope Contract remains the source declared human context envelope boundary
P4-M3.2 Governed Transition Intake Evidence Reference Envelope Contract remains the source evidence reference envelope boundary
P4-M3.1 Governed Transition Intake Request Envelope Contract remains the source request envelope boundary
P4-M3.0 Governed Transition Intake Boundary Contract remains the source intake boundary
P4-M3.4 is not transition readiness validation
P4-M3.4 is not target phase validation
P4-M3.4 is not phase eligibility validation
P4-M3.4 is not phase compatibility validation
P4-M3.4 is not phase transition execution
P4-M3.4 is not phase transition authorization
P4-M3.4 is not approval
P4-M3.4 is not confirmation
P4-M3.4 is not recommendation
P4-M3.4 is not ranking
P4-M3.4 is not next action generation
P4-M3.4 is not target selection
P4-M3.4 is not route selection
P4-M3.4 is not lifecycle transition
P4-M3.4 is not roadmap transition
P4-M3.4 is not request validation
P4-M3.4 is not evidence validation
P4-M3.4 is not human context validation
P4-M3.4 is not source validation
P4-M3.4 is not citation validation
P4-M3.4 is not readiness verdict
P4-M3.4 is not validation verdict
P4-M3.4 is not transition execution
P4-M3.4 is not transition record creation
P4-M3.4 is not request record creation
P4-M3.4 is not target-phase record creation
P4-M3.4 is not memory mutation
P4-M3.4 is not roadmap mutation
P4-M3.4 is not lifecycle mutation
P4-M3.4 is not proposal mutation
P4-M3.4 is not evidence mutation
P4-M3.4 is not human context mutation
P4-M3.4 is not target phase mutation
P4-M3.4 is not source fetching
P4-M3.4 is not provenance writing
P4-M3.4 is not citation mutation
no target phase validation
no target phase selection
no phase eligibility validation
no phase compatibility validation
no phase transition execution
no phase transition authorization
no readiness validation
no transition readiness validation
no readiness verdict
no validation verdict
no target-phase validation
no target phase persistence
no target phase storage
no target phase mutation
no target-phase record creation
no target-phase record update
no target-phase record deletion
no transition execution
no transition authorization
no transition approval
no transition confirmation
no transition recommendation
no transition ranking
no suggested next action
no next action generation
no transition record creation
no request validation
no request acceptance
no request rejection
no request persistence
no request storage
no request mutation
no request record creation
no evidence validation
no evidence scoring
no evidence ranking
no evidence precedence
no evidence arbitration
no evidence winner selection
no human context validation
no human confirmation
no human approval
no human authorization
no consent validation
no identity verification
no source validation
no citation validation
no source fetching
no provenance writing
no citation mutation
no memory mutation
no memory record creation
no memory record update
no memory record deletion
no roadmap mutation
no lifecycle mutation
no proposal mutation
no evidence mutation
no human context mutation
no target phase semantics
no target selection semantics
no route selection semantics
no phase eligibility semantics
no phase compatibility semantics
no transition execution semantics
no transition readiness semantics
no transition validation semantics
no validation semantics
no readiness semantics
no approval semantics
no authorization semantics
no confirmation semantics
no recommendation semantics
no ranking semantics
no next-action semantics
no mutation semantics
no API
no MCP
no connector
no agent call
no Codex/Hermes/ChatGPT product-code auto-call
no P4-M3.5
no P4-M3.5 command
no P4-M3.5 activation
no P4-M3.5 implementation
no P4-M4
no P4-M5
no v7
no productization
no UI
no Operator Console
no MVP
no deploy
no full Memory Graph
no version bump
no tag
""".splitlines()
    if line
)


TRUE_STATUS_FLAGS = tuple(
    line
    for line in """
definition_only
inspection_only
p4_m3_target_phase_envelope_definition_started
p4_m3_4_governed_transition_intake_target_phase_envelope_contract_started
p4_m3_4_definition_only
p4_m3_3_declared_human_context_envelope_contract_reference_defined
p4_m3_2_evidence_reference_envelope_contract_reference_defined
p4_m3_1_request_envelope_contract_reference_defined
p4_m3_0_intake_boundary_contract_reference_defined
p4_m2_17_closure_handoff_contract_reference_defined
p4_m2_final_non_execution_boundary_reference_defined
p4_m3_target_phase_envelope_contract_defined
p4_m3_target_phase_envelope_scope_defined
p4_m3_target_phase_envelope_field_shape_defined
p4_m3_target_phase_validation_semantics_prohibited
p4_m3_target_phase_selection_semantics_prohibited
p4_m3_phase_eligibility_validation_semantics_prohibited
p4_m3_phase_compatibility_validation_semantics_prohibited
p4_m3_transition_readiness_validation_semantics_prohibited
p4_m3_transition_readiness_verdict_semantics_prohibited
p4_m3_transition_validation_verdict_semantics_prohibited
p4_m3_transition_execution_semantics_prohibited
p4_m3_transition_authorization_semantics_prohibited
p4_m3_transition_approval_semantics_prohibited
p4_m3_transition_confirmation_semantics_prohibited
p4_m3_transition_recommendation_semantics_prohibited
p4_m3_transition_ranking_semantics_prohibited
p4_m3_transition_next_action_semantics_prohibited
p4_m3_target_phase_record_semantics_prohibited
p4_m3_target_phase_mutation_semantics_prohibited
p4_m3_request_validation_semantics_prohibited
p4_m3_evidence_validation_semantics_prohibited
p4_m3_human_context_validation_semantics_prohibited
p4_m3_transition_mutation_semantics_prohibited
p4_m3_5_start_deferred
""".splitlines()
    if line
)


FALSE_STATUS_FLAGS = tuple(
    line
    for line in """
target_phase_validation_enabled
target_phase_selection_enabled
phase_eligibility_validation_enabled
phase_compatibility_validation_enabled
phase_transition_execution_enabled
phase_transition_authorization_enabled
target_selection_enabled
route_selection_enabled
lifecycle_transition_enabled
roadmap_transition_enabled
target_phase_persistence_enabled
target_phase_storage_enabled
target_phase_mutation_enabled
target_phase_record_creation_enabled
target_phase_record_update_enabled
target_phase_record_deletion_enabled
transition_readiness_validation_enabled
live_transition_readiness_validation_enabled
readiness_verdict_enabled
transition_readiness_verdict_enabled
validation_verdict_enabled
transition_validation_verdict_enabled
execution_enabled
decision_execution_enabled
transition_execution_enabled
transition_command_execution_enabled
authorization_enabled
transition_authorization_enabled
approval_enabled
transition_approval_enabled
confirmation_enabled
transition_confirmation_enabled
recommendation_enabled
transition_recommendation_enabled
ranking_enabled
transition_ranking_enabled
suggested_next_action_enabled
next_action_generation_enabled
transition_record_creation_enabled
transition_readiness_record_creation_enabled
transition_validation_record_creation_enabled
transition_approval_record_creation_enabled
transition_authorization_record_creation_enabled
transition_confirmation_record_creation_enabled
transition_execution_record_creation_enabled
transition_recommendation_record_creation_enabled
transition_ranking_record_creation_enabled
transition_next_action_record_creation_enabled
live_request_intake_enabled
request_acceptance_enabled
request_rejection_enabled
request_validation_enabled
request_schema_validation_enabled
request_content_validation_enabled
request_completeness_validation_enabled
request_eligibility_validation_enabled
request_persistence_enabled
request_storage_enabled
request_mutation_enabled
request_record_creation_enabled
request_record_update_enabled
request_record_deletion_enabled
evidence_validation_enabled
evidence_scoring_enabled
evidence_ranking_enabled
evidence_precedence_enabled
evidence_arbitration_enabled
evidence_winner_selection_enabled
evidence_record_creation_enabled
human_context_validation_enabled
human_context_mutation_enabled
human_context_record_creation_enabled
human_confirmation_enabled
human_approval_enabled
human_authorization_enabled
consent_validation_enabled
identity_verification_enabled
source_validation_enabled
citation_validation_enabled
source_fetching_enabled
provenance_writing_enabled
citation_mutation_enabled
input_validation_enabled
record_validation_enabled
memory_mutation_enabled
memory_record_creation_enabled
memory_record_update_enabled
memory_record_deletion_enabled
proposal_mutation_enabled
lifecycle_mutation_enabled
retry_policy_mutation_enabled
evidence_mutation_enabled
roadmap_mutation_enabled
api_enabled
mcp_enabled
connector_enabled
agent_call_enabled
codex_hermes_chatgpt_product_code_auto_call_enabled
p4_m3_5_started
p4_m3_5_command_enabled
p4_m3_5_activation_enabled
p4_m3_5_implementation_enabled
p4_m4_started
p4_m5_started
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


GOVERNED_TRANSITION_INTAKE_TARGET_PHASE_ENVELOPE_CONTRACT_BOUNDARY = (
    "P4-M3.4 Governed Transition Intake Target Phase Envelope Contract "
    "read-only definition-only inspection-only. P4-M3.4 target phase envelope "
    "definition only. P4-M3.3 Governed Transition Intake Declared Human Context "
    "Envelope Contract remains the source declared human context envelope "
    "boundary. P4-M3.2 Governed Transition Intake Evidence Reference Envelope "
    "Contract remains the source evidence reference envelope boundary. P4-M3.1 "
    "Governed Transition Intake Request Envelope Contract remains the source "
    "request envelope boundary. P4-M3.0 Governed Transition Intake Boundary "
    "Contract remains the source intake boundary. P4-M3.4 defines only the "
    "static target phase envelope shape for future governed transition intake "
    "request work; it does not validate target phase, select target phase, "
    "validate phase eligibility, validate phase compatibility, validate "
    "transition readiness, produce readiness verdict, produce validation "
    "verdict, execute transition, authorize transition, approve transition, "
    "confirm transition, recommend transition, rank transition candidates, "
    "produce next action, create transition records, create request records, "
    "create target-phase records, mutate target phase, mutate memory, mutate "
    "roadmap, mutate lifecycle, mutate proposal, mutate evidence, mutate human "
    "context, fetch sources, write provenance, mutate citations, call APIs, "
    "call MCP, call connectors, call agents, productize, deploy, create UI, "
    "create Operator Console behavior, start P4-M3.5, start P4-M4, start P4-M5, "
    "or start v7. "
    + " ".join(f"{phrase}." for phrase in BOUNDARY_PHRASE_LINES)
)


_FIELD_IDS = (
    "p4-m3-governed-transition-intake-target-phase-envelope-contract-id",
    "p4-m3-governed-transition-intake-declared-human-context-envelope-contract-reference",
    "p4-m3-governed-transition-intake-evidence-reference-envelope-contract-reference",
    "p4-m3-governed-transition-intake-request-envelope-contract-reference",
    "p4-m3-governed-transition-intake-boundary-contract-reference",
    "p4-m2-closure-handoff-contract-reference",
    "p4-m2-final-non-execution-boundary-audit-reference",
    "p4-m3-target-phase-envelope-source-reference",
    "p4-m3-target-phase-envelope-scope",
    "p4-m3-target-phase-envelope-request-reference-field",
    "p4-m3-target-phase-envelope-target-phase-label-field",
    "p4-m3-target-phase-envelope-target-phase-family-field",
    "p4-m3-target-phase-envelope-target-phase-boundary-reference-field",
    "p4-m3-target-phase-envelope-declared-transition-reason-field",
    "p4-m3-target-phase-envelope-non-readiness-validation-boundary",
    "p4-m3-target-phase-envelope-non-execution-boundary",
    "p4-m3-target-phase-envelope-contract-category",
    "p4-m3-target-phase-envelope-semantics-disabled",
)


_FIELD_NAMES = (
    "P4-M3 Governed Transition Intake Target Phase Envelope Contract Identifier",
    "P4-M3 Governed Transition Intake Declared Human Context Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Evidence Reference Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Request Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Boundary Contract Reference",
    "P4-M2 Closure Handoff Contract Reference",
    "P4-M2 Final Non-Execution Boundary Audit Reference",
    "P4-M3 Target Phase Envelope Source Reference",
    "P4-M3 Target Phase Envelope Scope",
    "P4-M3 Target Phase Envelope Request Reference Field",
    "P4-M3 Target Phase Envelope Target Phase Label Field",
    "P4-M3 Target Phase Envelope Target Phase Family Field",
    "P4-M3 Target Phase Envelope Target Phase Boundary Reference Field",
    "P4-M3 Target Phase Envelope Declared Transition Reason Field",
    "P4-M3 Target Phase Envelope Non-Readiness Validation Boundary",
    "P4-M3 Target Phase Envelope Non-Execution Boundary",
    "P4-M3 Target Phase Envelope Contract Category",
    "P4-M3 Target Phase Envelope Semantics Disabled",
)


def _field_purpose(field_id: str) -> str:
    return (
        f"Defines {field_id} as read-only definition-only inspection-only "
        "P4-M3.4 target phase envelope definition only context; P4-M3.3 "
        "Governed Transition Intake Declared Human Context Envelope Contract "
        "remains the source declared human context envelope boundary, P4-M3.2 "
        "Governed Transition Intake Evidence Reference Envelope Contract remains "
        "the source evidence reference envelope boundary, P4-M3.1 Governed "
        "Transition Intake Request Envelope Contract remains the source request "
        "envelope boundary, P4-M3.0 Governed Transition Intake Boundary Contract "
        "remains the source intake boundary, P4-M3.4 is not target phase "
        "validation, not target phase selection, not phase eligibility "
        "validation, not phase compatibility validation, not transition "
        "readiness validation, not transition execution, no next action "
        "generation, no transition record creation, no request record creation, "
        "no target-phase record creation, no target phase mutation, no memory "
        "mutation, no roadmap mutation, no P4-M3.5, no P4-M4, no P4-M5, no v7, "
        "no productization, no UI, no Operator Console, no version bump, and no "
        "tag."
    )


_GOVERNED_TRANSITION_INTAKE_TARGET_PHASE_ENVELOPE_CONTRACT_FIELDS = tuple(
    GovernedTransitionIntakeTargetPhaseEnvelopeContractField(
        index,
        field_id,
        _FIELD_NAMES[index - 1],
        _field_purpose(field_id),
        "p4-m3-target-phase-envelope-contract-category",
        "no target phase semantics; no validation semantics; no mutation semantics",
    )
    for index, field_id in enumerate(_FIELD_IDS, start=1)
)


def list_governed_transition_intake_target_phase_envelope_contract_fields() -> (
    tuple[GovernedTransitionIntakeTargetPhaseEnvelopeContractField, ...]
):
    return _GOVERNED_TRANSITION_INTAKE_TARGET_PHASE_ENVELOPE_CONTRACT_FIELDS


def governed_transition_intake_target_phase_envelope_contract_field_ids() -> tuple[str, ...]:
    return tuple(
        field.field_id
        for field in list_governed_transition_intake_target_phase_envelope_contract_fields()
    )


def render_governed_transition_intake_target_phase_envelope_contract_markdown(
    fields: Sequence[GovernedTransitionIntakeTargetPhaseEnvelopeContractField] | None = None,
) -> str:
    field_values = (
        tuple(fields)
        if fields is not None
        else list_governed_transition_intake_target_phase_envelope_contract_fields()
    )
    status = governed_transition_intake_target_phase_envelope_contract_report()
    lines = [
        "# P4-M3.4 Governed Transition Intake Target Phase Envelope Contract",
        "",
        "P4-M3.4 Governed Transition Intake Target Phase Envelope Contract.",
        "",
        "read-only.",
        "",
        "definition-only.",
        "",
        "inspection-only.",
        "",
        "P4-M3.4 target phase envelope definition only.",
        "",
        (
            "P4-M3.3 Governed Transition Intake Declared Human Context Envelope "
            "Contract remains the source declared human context envelope boundary."
        ),
        "",
        (
            "P4-M3.2 Governed Transition Intake Evidence Reference Envelope "
            "Contract remains the source evidence reference envelope boundary."
        ),
        "",
        (
            "P4-M3.1 Governed Transition Intake Request Envelope Contract "
            "remains the source request envelope boundary."
        ),
        "",
        (
            "P4-M3.0 Governed Transition Intake Boundary Contract remains the "
            "source intake boundary."
        ),
        "",
    ]
    for prior_layer in PRIOR_DEFINITION_LAYER_REFERENCES:
        lines.extend([f"{prior_layer} remains a referenced definition layer.", ""])
    for phrase in BOUNDARY_PHRASE_LINES:
        lines.extend([f"{phrase}.", ""])
    lines.extend(
        [
            GOVERNED_TRANSITION_INTAKE_TARGET_PHASE_ENVELOPE_CONTRACT_BOUNDARY,
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
            "## Governed Transition Intake Target Phase Envelope Contract Fields",
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
                (
                    "- P4-M3 target phase envelope contract category: "
                    f"{field.p4_m3_target_phase_envelope_contract_category}"
                ),
                (
                    "- P4-M3 target phase envelope semantics disabled: "
                    f"{field.p4_m3_target_phase_envelope_semantics_disabled}"
                ),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def governed_transition_intake_target_phase_envelope_contract_as_dicts() -> (
    tuple[dict[str, object], ...]
):
    return tuple(
        asdict(field)
        for field in list_governed_transition_intake_target_phase_envelope_contract_fields()
    )


def governed_transition_intake_target_phase_envelope_contract_report() -> dict[str, object]:
    status: dict[str, object] = {
        "phase": "P4-M3.4",
        "feature": "Governed Transition Intake Target Phase Envelope Contract",
        "mode": "read-only",
        "package_version": P4_M3_4_PACKAGE_VERSION,
        "governed_transition_intake_target_phase_envelope_contract_field_count": 18,
        "prior_definition_layer_references": list(PRIOR_DEFINITION_LAYER_REFERENCES),
        "declared_human_context_envelope_contract_field_ids": list(
            governed_transition_intake_declared_human_context_envelope_contract_field_ids()
        ),
        "evidence_reference_envelope_contract_field_ids": list(
            governed_transition_intake_evidence_reference_envelope_contract_field_ids()
        ),
        "request_envelope_contract_field_ids": list(
            governed_transition_intake_request_envelope_contract_field_ids()
        ),
        "intake_boundary_contract_field_ids": list(
            governed_transition_intake_boundary_contract_field_ids()
        ),
        "closure_handoff_contract_field_ids": list(closure_handoff_contract_field_ids()),
        "final_non_execution_boundary_audit_field_ids": list(
            final_non_execution_boundary_audit_field_ids()
        ),
        "boundary": GOVERNED_TRANSITION_INTAKE_TARGET_PHASE_ENVELOPE_CONTRACT_BOUNDARY,
    }
    status.update({flag: True for flag in TRUE_STATUS_FLAGS})
    status.update({flag: False for flag in FALSE_STATUS_FLAGS})
    return status
