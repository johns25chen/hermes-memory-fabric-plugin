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
from .p4_m3_governed_transition_intake_declared_transition_reason_envelope_contract import (
    governed_transition_intake_declared_transition_reason_envelope_contract_field_ids,
)
from .p4_m3_governed_transition_intake_evidence_reference_envelope_contract import (
    governed_transition_intake_evidence_reference_envelope_contract_field_ids,
)
from .p4_m3_governed_transition_intake_request_envelope_contract import (
    governed_transition_intake_request_envelope_contract_field_ids,
)
from .p4_m3_governed_transition_intake_target_phase_envelope_contract import (
    governed_transition_intake_target_phase_envelope_contract_field_ids,
)


P4_M3_6_PACKAGE_VERSION = "6.16.0"


@dataclass(frozen=True)
class GovernedTransitionIntakeDeclaredTransitionConstraintEnvelopeContractField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    p4_m3_declared_transition_constraint_envelope_contract_category: str
    p4_m3_declared_transition_constraint_envelope_semantics_disabled: str


PRIOR_DEFINITION_LAYER_REFERENCES = (
    "P4-M3.5 Governed Transition Intake Declared Transition Reason Envelope Contract",
    "P4-M3.4 Governed Transition Intake Target Phase Envelope Contract",
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
P4-M3.6
Governed Transition Intake Declared Transition Constraint Envelope Contract
read-only
definition-only
inspection-only
P4-M3.6 declared transition constraint envelope definition only
P4-M3.5 Governed Transition Intake Declared Transition Reason Envelope Contract remains the source declared transition reason envelope boundary
P4-M3.4 Governed Transition Intake Target Phase Envelope Contract remains the source target phase envelope boundary
P4-M3.3 Governed Transition Intake Declared Human Context Envelope Contract remains the source declared human context envelope boundary
P4-M3.2 Governed Transition Intake Evidence Reference Envelope Contract remains the source evidence reference envelope boundary
P4-M3.1 Governed Transition Intake Request Envelope Contract remains the source request envelope boundary
P4-M3.0 Governed Transition Intake Boundary Contract remains the source intake boundary
P4-M3.6 is not transition constraint validation
P4-M3.6 is not constraint correctness validation
P4-M3.6 is not constraint feasibility validation
P4-M3.6 is not feasibility validation
P4-M3.6 is not transition reason validation
P4-M3.6 is not reason correctness validation
P4-M3.6 is not justification validation
P4-M3.6 is not rationale validation
P4-M3.6 is not target phase validation
P4-M3.6 is not target phase selection
P4-M3.6 is not phase eligibility validation
P4-M3.6 is not phase compatibility validation
P4-M3.6 is not transition readiness validation
P4-M3.6 is not readiness verdict
P4-M3.6 is not validation verdict
P4-M3.6 is not approval
P4-M3.6 is not authorization
P4-M3.6 is not confirmation
P4-M3.6 is not recommendation
P4-M3.6 is not ranking
P4-M3.6 is not next action generation
P4-M3.6 is not transition execution
P4-M3.6 is not request validation
P4-M3.6 is not evidence validation
P4-M3.6 is not human context validation
P4-M3.6 is not source validation
P4-M3.6 is not citation validation
P4-M3.6 is not transition record creation
P4-M3.6 is not request record creation
P4-M3.6 is not target-phase record creation
P4-M3.6 is not transition-reason record creation
P4-M3.6 is not transition-constraint record creation
P4-M3.6 is not memory mutation
P4-M3.6 is not roadmap mutation
P4-M3.6 is not lifecycle mutation
P4-M3.6 is not proposal mutation
P4-M3.6 is not evidence mutation
P4-M3.6 is not human context mutation
P4-M3.6 is not target phase mutation
P4-M3.6 is not transition reason mutation
P4-M3.6 is not transition constraint mutation
P4-M3.6 is not source fetching
P4-M3.6 is not provenance writing
P4-M3.6 is not citation mutation
no transition constraint validation
no constraint correctness validation
no constraint feasibility validation
no feasibility validation
no constraint scoring
no constraint ranking
no constraint precedence
no constraint arbitration
no constraint winner selection
no declared constraint acceptance
no declared constraint rejection
no transition constraint persistence
no transition constraint storage
no transition constraint mutation
no transition-constraint record creation
no transition-constraint record update
no transition-constraint record deletion
no transition reason validation
no reason correctness validation
no justification validation
no rationale validation
no reason scoring
no reason ranking
no target phase validation
no target phase selection
no phase eligibility validation
no phase compatibility validation
no readiness validation
no transition readiness validation
no readiness verdict
no validation verdict
no approval
no authorization
no confirmation
no recommendation
no ranking
no suggested next action
no next action generation
no transition execution
no transition authorization
no transition approval
no transition confirmation
no transition recommendation
no transition ranking
no transition record creation
no target-phase record creation
no transition-reason record creation
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
no target phase mutation
no transition reason mutation
no transition constraint semantics
no constraint correctness semantics
no constraint feasibility semantics
no feasibility semantics
no transition reason semantics
no reason correctness semantics
no justification semantics
no rationale semantics
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
no P4-M3.7
no P4-M3.7 command
no P4-M3.7 activation
no P4-M3.7 implementation
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
p4_m3_declared_transition_constraint_envelope_definition_started
p4_m3_6_governed_transition_intake_declared_transition_constraint_envelope_contract_started
p4_m3_6_definition_only
p4_m3_5_declared_transition_reason_envelope_contract_reference_defined
p4_m3_4_target_phase_envelope_contract_reference_defined
p4_m3_3_declared_human_context_envelope_contract_reference_defined
p4_m3_2_evidence_reference_envelope_contract_reference_defined
p4_m3_1_request_envelope_contract_reference_defined
p4_m3_0_intake_boundary_contract_reference_defined
p4_m2_17_closure_handoff_contract_reference_defined
p4_m2_final_non_execution_boundary_reference_defined
p4_m3_declared_transition_constraint_envelope_contract_defined
p4_m3_declared_transition_constraint_envelope_scope_defined
p4_m3_declared_transition_constraint_envelope_field_shape_defined
p4_m3_transition_constraint_validation_semantics_prohibited
p4_m3_constraint_correctness_validation_semantics_prohibited
p4_m3_constraint_feasibility_validation_semantics_prohibited
p4_m3_feasibility_validation_semantics_prohibited
p4_m3_transition_constraint_scoring_semantics_prohibited
p4_m3_transition_constraint_ranking_semantics_prohibited
p4_m3_transition_constraint_record_semantics_prohibited
p4_m3_transition_constraint_mutation_semantics_prohibited
p4_m3_transition_reason_validation_semantics_prohibited
p4_m3_reason_correctness_validation_semantics_prohibited
p4_m3_justification_validation_semantics_prohibited
p4_m3_rationale_validation_semantics_prohibited
p4_m3_target_phase_validation_semantics_prohibited
p4_m3_target_phase_selection_semantics_prohibited
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
p4_m3_request_validation_semantics_prohibited
p4_m3_evidence_validation_semantics_prohibited
p4_m3_human_context_validation_semantics_prohibited
p4_m3_transition_mutation_semantics_prohibited
p4_m3_7_start_deferred
""".splitlines()
    if line
)


FALSE_STATUS_FLAGS = tuple(
    line
    for line in """
transition_constraint_validation_enabled
constraint_correctness_validation_enabled
constraint_feasibility_validation_enabled
feasibility_validation_enabled
transition_constraint_scoring_enabled
transition_constraint_ranking_enabled
transition_constraint_precedence_enabled
transition_constraint_arbitration_enabled
transition_constraint_winner_selection_enabled
declared_constraint_acceptance_enabled
declared_constraint_rejection_enabled
transition_constraint_persistence_enabled
transition_constraint_storage_enabled
transition_constraint_mutation_enabled
transition_constraint_record_creation_enabled
transition_constraint_record_update_enabled
transition_constraint_record_deletion_enabled
transition_reason_validation_enabled
reason_correctness_validation_enabled
justification_validation_enabled
rationale_validation_enabled
transition_reason_scoring_enabled
transition_reason_ranking_enabled
transition_reason_precedence_enabled
transition_reason_arbitration_enabled
transition_reason_winner_selection_enabled
declared_reason_acceptance_enabled
declared_reason_rejection_enabled
transition_reason_persistence_enabled
transition_reason_storage_enabled
transition_reason_mutation_enabled
transition_reason_record_creation_enabled
transition_reason_record_update_enabled
transition_reason_record_deletion_enabled
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
p4_m3_7_started
p4_m3_7_command_enabled
p4_m3_7_activation_enabled
p4_m3_7_implementation_enabled
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


GOVERNED_TRANSITION_INTAKE_DECLARED_TRANSITION_CONSTRAINT_ENVELOPE_CONTRACT_BOUNDARY = (
    "P4-M3.6 Governed Transition Intake Declared Transition Constraint Envelope "
    "Contract read-only definition-only inspection-only. P4-M3.6 declared "
    "transition constraint envelope definition only. P4-M3.5 Governed "
    "Transition Intake Declared Transition Reason Envelope Contract remains "
    "the source declared transition reason envelope boundary. P4-M3.4 "
    "Governed Transition Intake Target Phase Envelope Contract remains the "
    "source target phase envelope boundary. P4-M3.3 Governed Transition Intake "
    "Declared Human Context Envelope Contract remains the source declared "
    "human context envelope boundary. P4-M3.2 Governed Transition Intake "
    "Evidence Reference Envelope Contract remains the source evidence "
    "reference envelope boundary. P4-M3.1 Governed Transition Intake Request "
    "Envelope Contract remains the source request envelope boundary. P4-M3.0 "
    "Governed Transition Intake Boundary Contract remains the source intake "
    "boundary. P4-M3.6 defines only the static declared transition constraint "
    "envelope shape for future governed transition intake request work; it "
    "does not validate transition constraint, constraint correctness, "
    "constraint feasibility, feasibility, transition reason, reason "
    "correctness, justification, rationale, target phase, phase eligibility, "
    "phase compatibility, or transition readiness; it does not produce "
    "readiness verdict, validation verdict, approval, authorization, "
    "confirmation, recommendation, ranking, or next action; it does not "
    "execute transition, create records, mutate memory, roadmap, lifecycle, "
    "proposal, evidence, human context, target phase, transition reason, "
    "transition constraint, source, provenance, or citations; it does not call "
    "APIs, MCP, connectors, agents, or product code; it does not start "
    "P4-M3.7, P4-M4, P4-M5, v7, productization, UI, Operator Console, MVP, "
    "deploy, or full Memory Graph behavior. "
    + " ".join(f"{phrase}." for phrase in BOUNDARY_PHRASE_LINES)
)


_FIELD_IDS = (
    "p4-m3-governed-transition-intake-declared-transition-constraint-envelope-contract-id",
    "p4-m3-governed-transition-intake-declared-transition-reason-envelope-contract-reference",
    "p4-m3-governed-transition-intake-target-phase-envelope-contract-reference",
    "p4-m3-governed-transition-intake-declared-human-context-envelope-contract-reference",
    "p4-m3-governed-transition-intake-evidence-reference-envelope-contract-reference",
    "p4-m3-governed-transition-intake-request-envelope-contract-reference",
    "p4-m3-governed-transition-intake-boundary-contract-reference",
    "p4-m2-closure-handoff-contract-reference",
    "p4-m2-final-non-execution-boundary-audit-reference",
    "p4-m3-declared-transition-constraint-envelope-source-reference",
    "p4-m3-declared-transition-constraint-envelope-scope",
    "p4-m3-declared-transition-constraint-envelope-request-reference-field",
    "p4-m3-declared-transition-constraint-envelope-target-phase-reference-field",
    "p4-m3-declared-transition-constraint-envelope-reason-reference-field",
    "p4-m3-declared-transition-constraint-envelope-constraint-label-field",
    "p4-m3-declared-transition-constraint-envelope-constraint-description-field",
    "p4-m3-declared-transition-constraint-envelope-non-constraint-validation-boundary",
    "p4-m3-declared-transition-constraint-envelope-semantics-disabled",
)


_FIELD_NAMES = (
    "P4-M3 Governed Transition Intake Declared Transition Constraint Envelope Contract Identifier",
    "P4-M3 Governed Transition Intake Declared Transition Reason Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Target Phase Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Declared Human Context Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Evidence Reference Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Request Envelope Contract Reference",
    "P4-M3 Governed Transition Intake Boundary Contract Reference",
    "P4-M2 Closure Handoff Contract Reference",
    "P4-M2 Final Non-Execution Boundary Audit Reference",
    "P4-M3 Declared Transition Constraint Envelope Source Reference",
    "P4-M3 Declared Transition Constraint Envelope Scope",
    "P4-M3 Declared Transition Constraint Envelope Request Reference Field",
    "P4-M3 Declared Transition Constraint Envelope Target Phase Reference Field",
    "P4-M3 Declared Transition Constraint Envelope Reason Reference Field",
    "P4-M3 Declared Transition Constraint Envelope Constraint Label Field",
    "P4-M3 Declared Transition Constraint Envelope Constraint Description Field",
    "P4-M3 Declared Transition Constraint Envelope Non-Constraint Validation Boundary",
    "P4-M3 Declared Transition Constraint Envelope Semantics Disabled",
)


def _field_purpose(field_id: str) -> str:
    return (
        f"Defines {field_id} as read-only definition-only inspection-only "
        "P4-M3.6 declared transition constraint envelope definition only "
        "context; P4-M3.5 Governed Transition Intake Declared Transition "
        "Reason Envelope Contract remains the source declared transition "
        "reason envelope boundary, P4-M3.4 Governed Transition Intake Target "
        "Phase Envelope Contract remains the source target phase envelope "
        "boundary, P4-M3.3 Governed Transition Intake Declared Human Context "
        "Envelope Contract remains the source declared human context envelope "
        "boundary, P4-M3.2 Governed Transition Intake Evidence Reference "
        "Envelope Contract remains the source evidence reference envelope "
        "boundary, P4-M3.1 Governed Transition Intake Request Envelope "
        "Contract remains the source request envelope boundary, P4-M3.0 "
        "Governed Transition Intake Boundary Contract remains the source "
        "intake boundary, P4-M3.6 is not transition constraint validation, "
        "not constraint correctness validation, not constraint feasibility "
        "validation, not feasibility validation, not transition reason "
        "validation, not target phase validation, not target phase selection, "
        "not transition readiness validation, no readiness verdict, no "
        "validation verdict, no approval, no authorization, no confirmation, "
        "no recommendation, no ranking, no next action generation, no "
        "transition execution, no transition-constraint record creation, no "
        "transition constraint mutation, no memory mutation, no P4-M3.7, no "
        "P4-M4, no P4-M5, no v7, no productization, no UI, no Operator "
        "Console, no version bump, and no tag."
    )


_GOVERNED_TRANSITION_INTAKE_DECLARED_TRANSITION_CONSTRAINT_ENVELOPE_CONTRACT_FIELDS = tuple(
    GovernedTransitionIntakeDeclaredTransitionConstraintEnvelopeContractField(
        index,
        field_id,
        _FIELD_NAMES[index - 1],
        _field_purpose(field_id),
        "p4-m3-declared-transition-constraint-envelope-contract-category",
        (
            "no transition constraint semantics; no constraint correctness "
            "semantics; no constraint feasibility semantics; no feasibility "
            "semantics; no validation semantics; no mutation semantics"
        ),
    )
    for index, field_id in enumerate(_FIELD_IDS, start=1)
)


def list_governed_transition_intake_declared_transition_constraint_envelope_contract_fields() -> (
    tuple[
        GovernedTransitionIntakeDeclaredTransitionConstraintEnvelopeContractField,
        ...,
    ]
):
    return (
        _GOVERNED_TRANSITION_INTAKE_DECLARED_TRANSITION_CONSTRAINT_ENVELOPE_CONTRACT_FIELDS
    )


def governed_transition_intake_declared_transition_constraint_envelope_contract_field_ids() -> (
    tuple[str, ...]
):
    return tuple(
        field.field_id
        for field in (
            list_governed_transition_intake_declared_transition_constraint_envelope_contract_fields()
        )
    )


def render_governed_transition_intake_declared_transition_constraint_envelope_contract_markdown(
    fields: Sequence[
        GovernedTransitionIntakeDeclaredTransitionConstraintEnvelopeContractField
    ]
    | None = None,
) -> str:
    field_values = (
        tuple(fields)
        if fields is not None
        else (
            list_governed_transition_intake_declared_transition_constraint_envelope_contract_fields()
        )
    )
    status = (
        governed_transition_intake_declared_transition_constraint_envelope_contract_report()
    )
    lines = [
        "# P4-M3.6 Governed Transition Intake Declared Transition Constraint Envelope Contract",
        "",
        "P4-M3.6 Governed Transition Intake Declared Transition Constraint Envelope Contract.",
        "",
        "read-only.",
        "",
        "definition-only.",
        "",
        "inspection-only.",
        "",
        "P4-M3.6 declared transition constraint envelope definition only.",
        "",
        (
            "P4-M3.5 Governed Transition Intake Declared Transition Reason "
            "Envelope Contract remains the source declared transition reason "
            "envelope boundary."
        ),
        "",
        (
            "P4-M3.4 Governed Transition Intake Target Phase Envelope Contract "
            "remains the source target phase envelope boundary."
        ),
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
            GOVERNED_TRANSITION_INTAKE_DECLARED_TRANSITION_CONSTRAINT_ENVELOPE_CONTRACT_BOUNDARY,
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
            "## Governed Transition Intake Declared Transition Constraint Envelope Contract Fields",
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
                    "- P4-M3 declared transition constraint envelope contract "
                    "category: "
                    f"{field.p4_m3_declared_transition_constraint_envelope_contract_category}"
                ),
                (
                    "- P4-M3 declared transition constraint envelope semantics "
                    "disabled: "
                    f"{field.p4_m3_declared_transition_constraint_envelope_semantics_disabled}"
                ),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def governed_transition_intake_declared_transition_constraint_envelope_contract_as_dicts() -> (
    tuple[dict[str, object], ...]
):
    return tuple(
        asdict(field)
        for field in (
            list_governed_transition_intake_declared_transition_constraint_envelope_contract_fields()
        )
    )


def governed_transition_intake_declared_transition_constraint_envelope_contract_report() -> (
    dict[str, object]
):
    status: dict[str, object] = {
        "phase": "P4-M3.6",
        "feature": (
            "Governed Transition Intake Declared Transition Constraint Envelope Contract"
        ),
        "mode": "read-only",
        "package_version": P4_M3_6_PACKAGE_VERSION,
        (
            "governed_transition_intake_declared_transition_constraint_envelope_"
            "contract_field_count"
        ): 18,
        "prior_definition_layer_references": list(PRIOR_DEFINITION_LAYER_REFERENCES),
        "declared_transition_reason_envelope_contract_field_ids": list(
            governed_transition_intake_declared_transition_reason_envelope_contract_field_ids()
        ),
        "target_phase_envelope_contract_field_ids": list(
            governed_transition_intake_target_phase_envelope_contract_field_ids()
        ),
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
        "boundary": (
            GOVERNED_TRANSITION_INTAKE_DECLARED_TRANSITION_CONSTRAINT_ENVELOPE_CONTRACT_BOUNDARY
        ),
    }
    status.update({flag: True for flag in TRUE_STATUS_FLAGS})
    status.update({flag: False for flag in FALSE_STATUS_FLAGS})
    return status
