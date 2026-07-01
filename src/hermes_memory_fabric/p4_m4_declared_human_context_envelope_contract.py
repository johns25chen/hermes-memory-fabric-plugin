from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence

from .p4_m4_evidence_reference_envelope_contract import (
    evidence_reference_envelope_contract_field_ids,
)


P4_M4_3_PACKAGE_VERSION = "6.16.0"


@dataclass(frozen=True)
class DeclaredHumanContextEnvelopeContractField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    p4_m4_declared_human_context_envelope_contract_category: str
    p4_m4_declared_human_context_envelope_contract_semantics_disabled: str


DIRECT_PRIOR_DEFINITION_LAYER_REFERENCES = (
    "P4-M4.2 Evidence Reference Envelope Contract",
)

INHERITED_PRIOR_DEFINITION_LAYER_REFERENCES = (
    "P4-M4.1 Entry Gate Design Request Envelope Contract",
    "P4-M4.0 Entry Gate Design Boundary Contract",
    "P4-M3.16 Governed Transition Intake Final Phase Handoff Summary",
)


BOUNDARY_PHRASE_LINES = (
    "P4-M4.3",
    "Declared Human Context Envelope Contract",
    "read-only",
    "definition-only",
    "declared-human-context-envelope-design-only",
    "inspection-only",
    "P4-M4.3 Declared Human Context Envelope Contract is definition only",
    "P4-M4.3 is declared-human-context-envelope-design-only",
    "P4-M4.2 Evidence Reference Envelope Contract remains the direct prior evidence reference envelope reference",
    "P4-M4.1 Entry Gate Design Request Envelope Contract remains the inherited prior request envelope reference",
    "P4-M4.0 Entry Gate Design Boundary Contract remains the inherited prior design boundary reference",
    "P4-M3.16 Governed Transition Intake Final Phase Handoff Summary remains the inherited prior closed-phase handoff reference",
    "P4-M3 static definition chain remains closed",
    "P4-M4 design layer remains design-boundary-only",
    "P4-M4 declared human context envelope design starts only as a static envelope definition",
    "P4-M4 human context intake remains not implemented",
    "P4-M4 human context parsing remains not implemented",
    "P4-M4 human context validation remains not implemented",
    "P4-M4 identity validation remains not implemented",
    "P4-M4 actor validation remains not implemented",
    "P4-M4 consent validation remains not implemented",
    "P4-M4 authority validation remains not implemented",
    "P4-M4 approval validation remains not implemented",
    "P4-M4 authorization validation remains not implemented",
    "P4-M4 confirmation validation remains not implemented",
    "P4-M4 human context record creation remains not implemented",
    "P4-M4 identity record creation remains not implemented",
    "P4-M4 actor record creation remains not implemented",
    "P4-M4 consent record creation remains not implemented",
    "P4-M4 evidence intake remains not implemented",
    "P4-M4 evidence validation remains not implemented",
    "P4-M4 reference resolution remains not implemented",
    "P4-M4 reference validation remains not implemented",
    "P4-M4 citation validation remains not implemented",
    "P4-M4 source fetching remains not implemented",
    "P4-M4 provenance writing remains not implemented",
    "P4-M4 request intake remains not implemented",
    "P4-M4 request validation remains not implemented",
    "P4-M4 execution remains not implemented",
    "P4-M4 entry gate remains not implemented",
    "P4-M4 entry gate validation remains not implemented",
    "P4-M4 readiness validation remains not implemented",
    "P4-M4 verdict generation remains not implemented",
    "P4-M4 approval remains not implemented",
    "P4-M4 authorization remains not implemented",
    "P4-M4 confirmation remains not implemented",
    "P4-M4 transition execution remains not implemented",
    "P4-M5 remains not started",
    "v7 remains not started",
    "productization remains not started",
    "UI remains not started",
    "Operator Console remains not started",
    "P4-M4.3 is not live validation",
    "P4-M4.3 is not human context intake",
    "P4-M4.3 is not live human context parsing",
    "P4-M4.3 is not human context validation",
    "P4-M4.3 is not human context acceptance",
    "P4-M4.3 is not human context rejection",
    "P4-M4.3 is not human context routing",
    "P4-M4.3 is not human context execution",
    "P4-M4.3 is not human context record creation",
    "P4-M4.3 is not identity validation",
    "P4-M4.3 is not actor validation",
    "P4-M4.3 is not user validation",
    "P4-M4.3 is not operator validation",
    "P4-M4.3 is not consent validation",
    "P4-M4.3 is not authority validation",
    "P4-M4.3 is not approval validation",
    "P4-M4.3 is not authorization validation",
    "P4-M4.3 is not confirmation validation",
    "P4-M4.3 is not identity record creation",
    "P4-M4.3 is not actor record creation",
    "P4-M4.3 is not consent record creation",
    "P4-M4.3 is not evidence intake",
    "P4-M4.3 is not evidence validation",
    "P4-M4.3 is not reference resolution",
    "P4-M4.3 is not reference validation",
    "P4-M4.3 is not citation validation",
    "P4-M4.3 is not source fetching",
    "P4-M4.3 is not provenance writing",
    "P4-M4.3 is not request intake",
    "P4-M4.3 is not request validation",
    "P4-M4.3 is not boundary validation",
    "P4-M4.3 is not phase validation",
    "P4-M4.3 is not entry gate validation",
    "P4-M4.3 is not readiness validation",
    "P4-M4.3 is not transition validation",
    "P4-M4.3 is not package validation",
    "P4-M4.3 is not closure validation",
    "P4-M4.3 is not handoff validation",
    "P4-M4.3 is not final phase handoff validation",
    "P4-M4.3 is not a working entry gate",
    "P4-M4.3 is not gate activation",
    "P4-M4.3 is not gate execution",
    "P4-M4.3 is not transition execution",
    "P4-M4.3 is not command execution",
    "P4-M4.3 is not readiness verdict",
    "P4-M4.3 is not validation verdict",
    "P4-M4.3 is not human context verdict",
    "P4-M4.3 is not identity verdict",
    "P4-M4.3 is not approval verdict",
    "P4-M4.3 is not authorization verdict",
    "P4-M4.3 is not confirmation verdict",
    "P4-M4.3 is not evidence verdict",
    "P4-M4.3 is not reference verdict",
    "P4-M4.3 is not citation verdict",
    "P4-M4.3 is not entry verdict",
    "P4-M4.3 is not gate verdict",
    "P4-M4.3 is not transition verdict",
    "P4-M4.3 is not approval",
    "P4-M4.3 is not authorization",
    "P4-M4.3 is not confirmation",
    "P4-M4.3 is not recommendation",
    "P4-M4.3 is not ranking",
    "P4-M4.3 is not next action generation",
    "P4-M4.3 is not package completeness validation",
    "P4-M4.3 is not package consistency validation",
    "P4-M4.3 is not package integrity validation",
    "P4-M4.3 is not package readiness validation",
    "P4-M4.3 is not record creation",
    "P4-M4.3 is not memory mutation",
    "P4-M4.3 is not roadmap mutation",
    "P4-M4.3 is not lifecycle mutation",
    "P4-M4.3 is not proposal mutation",
    "P4-M4.3 is not human context mutation",
    "P4-M4.3 is not evidence mutation",
    "no human context intake",
    "no live human context parsing",
    "no human context validation",
    "no identity validation",
    "no consent validation",
    "no authority validation",
    "no approval validation",
    "no authorization validation",
    "no confirmation validation",
    "no human context record creation",
    "no identity record creation",
    "no actor record creation",
    "no consent record creation",
    "no evidence validation",
    "no reference resolution",
    "no reference validation",
    "no citation validation",
    "no source fetching",
    "no provenance writing",
    "no request intake",
    "no request validation",
    "no entry gate validation",
    "no readiness validation",
    "no working entry gate",
    "no gate activation",
    "no gate execution",
    "no readiness verdict",
    "no validation verdict",
    "no human context verdict",
    "no identity verdict",
    "no approval",
    "no authorization",
    "no confirmation",
    "no recommendation",
    "no ranking",
    "no next action generation",
    "no transition execution",
    "no record creation",
    "no memory mutation",
    "no roadmap mutation",
    "no P4-M5",
    "no v7",
    "no productization",
    "no UI",
    "no Operator Console",
    "no MVP",
    "no deploy",
    "no full Memory Graph",
    "no version bump",
    "no tag",
)


TRUE_STATUS_FLAGS = (
    "definition_only",
    "declared_human_context_envelope_design_only",
    "inspection_only",
    "p4_m4_3_declared_human_context_envelope_contract_started",
    "p4_m4_3_definition_only",
    "p4_m4_3_declared_human_context_envelope_design_only",
    "p4_m4_2_evidence_reference_envelope_contract_reference_defined",
    "p4_m4_1_entry_gate_design_request_envelope_contract_reference_defined",
    "p4_m4_0_entry_gate_design_boundary_contract_reference_defined",
    "p4_m3_16_final_phase_handoff_summary_reference_defined",
    "p4_m3_static_definition_chain_closed_reference_defined",
    "p4_m4_design_boundary_reference_defined",
    "p4_m4_declared_human_context_envelope_design_defined",
    "p4_m4_declared_human_context_shape_defined",
    "p4_m4_human_context_intake_non_implementation_boundary_defined",
    "p4_m4_human_context_validation_semantics_prohibited",
    "p4_m4_identity_validation_semantics_prohibited",
    "p4_m4_consent_validation_semantics_prohibited",
    "p4_m4_authority_validation_semantics_prohibited",
    "p4_m4_approval_validation_semantics_prohibited",
    "p4_m4_authorization_validation_semantics_prohibited",
    "p4_m4_confirmation_validation_semantics_prohibited",
    "p4_m4_validation_semantics_prohibited",
    "p4_m4_verdict_semantics_prohibited",
    "p4_m4_execution_semantics_prohibited",
    "p4_m4_record_creation_semantics_prohibited",
    "p4_m4_mutation_semantics_prohibited",
    "p4_m5_start_deferred",
    "v7_start_deferred",
    "productization_deferred",
    "ui_deferred",
    "operator_console_deferred",
)


FALSE_STATUS_FLAGS = (
    "live_validation_enabled",
    "human_context_intake_enabled",
    "live_human_context_parsing_enabled",
    "human_context_validation_enabled",
    "human_context_acceptance_enabled",
    "human_context_rejection_enabled",
    "human_context_routing_enabled",
    "human_context_execution_enabled",
    "human_context_record_creation_enabled",
    "identity_validation_enabled",
    "actor_validation_enabled",
    "user_validation_enabled",
    "operator_validation_enabled",
    "consent_validation_enabled",
    "authority_validation_enabled",
    "approval_validation_enabled",
    "authorization_validation_enabled",
    "confirmation_validation_enabled",
    "identity_record_creation_enabled",
    "actor_record_creation_enabled",
    "consent_record_creation_enabled",
    "evidence_intake_enabled",
    "live_evidence_parsing_enabled",
    "evidence_validation_enabled",
    "evidence_record_creation_enabled",
    "reference_resolution_enabled",
    "reference_validation_enabled",
    "reference_integrity_validation_enabled",
    "citation_validation_enabled",
    "citation_mutation_enabled",
    "source_validation_enabled",
    "source_fetching_enabled",
    "provenance_writing_enabled",
    "provenance_mutation_enabled",
    "request_intake_enabled",
    "live_request_parsing_enabled",
    "request_validation_enabled",
    "request_acceptance_enabled",
    "request_rejection_enabled",
    "request_routing_enabled",
    "request_execution_enabled",
    "request_record_creation_enabled",
    "boundary_validation_enabled",
    "phase_validation_enabled",
    "entry_gate_validation_enabled",
    "entry_readiness_validation_enabled",
    "readiness_validation_enabled",
    "transition_readiness_validation_enabled",
    "transition_validation_enabled",
    "governed_transition_intake_validation_enabled",
    "package_validation_enabled",
    "package_completeness_validation_enabled",
    "package_consistency_validation_enabled",
    "package_integrity_validation_enabled",
    "package_readiness_validation_enabled",
    "closure_validation_enabled",
    "handoff_validation_enabled",
    "final_phase_handoff_validation_enabled",
    "working_entry_gate_enabled",
    "gate_activation_enabled",
    "gate_execution_enabled",
    "p4_m4_execution_enabled",
    "operational_behavior_enabled",
    "readiness_verdict_enabled",
    "validation_verdict_enabled",
    "human_context_verdict_enabled",
    "identity_verdict_enabled",
    "approval_verdict_enabled",
    "authorization_verdict_enabled",
    "confirmation_verdict_enabled",
    "evidence_verdict_enabled",
    "reference_verdict_enabled",
    "citation_verdict_enabled",
    "entry_verdict_enabled",
    "gate_verdict_enabled",
    "transition_verdict_enabled",
    "approval_enabled",
    "authorization_enabled",
    "confirmation_enabled",
    "recommendation_enabled",
    "ranking_enabled",
    "next_action_generation_enabled",
    "transition_execution_enabled",
    "command_execution_enabled",
    "record_creation_enabled",
    "reference_record_creation_enabled",
    "citation_record_creation_enabled",
    "provenance_record_creation_enabled",
    "request_envelope_record_creation_enabled",
    "entry_record_creation_enabled",
    "gate_record_creation_enabled",
    "readiness_record_creation_enabled",
    "validation_record_creation_enabled",
    "transition_record_creation_enabled",
    "approval_record_creation_enabled",
    "authorization_record_creation_enabled",
    "confirmation_record_creation_enabled",
    "recommendation_record_creation_enabled",
    "ranking_record_creation_enabled",
    "next_action_record_creation_enabled",
    "persistence_enabled",
    "storage_enabled",
    "memory_mutation_enabled",
    "roadmap_mutation_enabled",
    "lifecycle_mutation_enabled",
    "proposal_mutation_enabled",
    "human_context_mutation_enabled",
    "evidence_mutation_enabled",
    "api_enabled",
    "mcp_enabled",
    "connector_enabled",
    "agent_call_enabled",
    "p4_m5_started",
    "v7_started",
    "productization_started",
    "ui_started",
    "operator_console_started",
    "mvp_started",
    "deploy_started",
    "full_memory_graph_started",
    "version_bump_enabled",
    "tag_creation_enabled",
)


DECLARED_HUMAN_CONTEXT_ENVELOPE_CONTRACT_BOUNDARY = (
    "P4-M4.3 Declared Human Context Envelope Contract read-only "
    "definition-only declared-human-context-envelope-design-only "
    "inspection-only. P4-M4.3 Declared Human Context Envelope Contract is "
    "definition only. "
    + " ".join(f"{phrase}." for phrase in BOUNDARY_PHRASE_LINES)
)


_FIELD_IDS = (
    "p4-m4-declared-human-context-envelope-contract-id",
    "p4-m4-declared-human-context-envelope-contract-phase",
    "p4-m4-declared-human-context-envelope-contract-mode",
    "p4-m4-declared-human-context-envelope-contract-direct-prior-evidence-reference-envelope-reference",
    "p4-m4-declared-human-context-envelope-contract-inherited-prior-request-envelope-reference",
    "p4-m4-declared-human-context-envelope-contract-inherited-prior-boundary-reference",
    "p4-m4-declared-human-context-envelope-contract-inherited-prior-handoff-reference",
    "p4-m4-declared-human-context-envelope-contract-scope",
    "p4-m4-declared-human-context-envelope-contract-declared-human-context-envelope-design-only",
    "p4-m4-declared-human-context-envelope-contract-declared-human-context-shape-definition",
    "p4-m4-declared-human-context-envelope-contract-human-context-intake-non-implementation",
    "p4-m4-declared-human-context-envelope-contract-human-context-validation-semantics-disabled",
    "p4-m4-declared-human-context-envelope-contract-identity-consent-authority-semantics-disabled",
    "p4-m4-declared-human-context-envelope-contract-approval-authorization-confirmation-semantics-disabled",
    "p4-m4-declared-human-context-envelope-contract-verdict-execution-mutation-semantics-disabled",
    "p4-m4-declared-human-context-envelope-contract-p4-m5-v7-productization-ui-deferred",
)


_FIELD_NAMES = (
    "P4-M4 Declared Human Context Envelope Contract Id",
    "P4-M4 Declared Human Context Envelope Contract Phase",
    "P4-M4 Declared Human Context Envelope Contract Mode",
    "P4-M4 Declared Human Context Envelope Contract Direct Prior Evidence Reference Envelope Reference",
    "P4-M4 Declared Human Context Envelope Contract Inherited Prior Request Envelope Reference",
    "P4-M4 Declared Human Context Envelope Contract Inherited Prior Boundary Reference",
    "P4-M4 Declared Human Context Envelope Contract Inherited Prior Handoff Reference",
    "P4-M4 Declared Human Context Envelope Contract Scope",
    "P4-M4 Declared Human Context Envelope Contract Declared Human Context Envelope Design Only",
    "P4-M4 Declared Human Context Envelope Contract Declared Human Context Shape Definition",
    "P4-M4 Declared Human Context Envelope Contract Human Context Intake Non Implementation",
    "P4-M4 Declared Human Context Envelope Contract Human Context Validation Semantics Disabled",
    "P4-M4 Declared Human Context Envelope Contract Identity Consent Authority Semantics Disabled",
    "P4-M4 Declared Human Context Envelope Contract Approval Authorization Confirmation Semantics Disabled",
    "P4-M4 Declared Human Context Envelope Contract Verdict Execution Mutation Semantics Disabled",
    "P4-M4 Declared Human Context Envelope Contract P4-M5 V7 Productization UI Deferred",
)


def _field_purpose(field_id: str) -> str:
    return (
        f"Defines {field_id} as read-only definition-only "
        "declared-human-context-envelope-design-only inspection-only P4-M4.3 "
        "Declared Human Context Envelope Contract context; P4-M4.2 Evidence "
        "Reference Envelope Contract remains the direct prior evidence "
        "reference envelope reference; P4-M4.1 Entry Gate Design Request "
        "Envelope Contract remains the inherited prior request envelope "
        "reference; P4-M4.0 Entry Gate Design Boundary Contract remains the "
        "inherited prior design boundary reference; P4-M3.16 Governed "
        "Transition Intake Final Phase Handoff Summary remains the inherited "
        "prior closed-phase handoff reference; P4-M3 static definition chain "
        "remains closed; P4-M4 declared human context envelope design starts "
        "only as a static envelope definition; no human context intake; no "
        "live human context parsing; no human context validation; no identity "
        "validation; no consent validation; no authority validation; no "
        "approval validation; no authorization validation; no confirmation "
        "validation; no human context record creation; no evidence validation; "
        "no reference resolution; no reference validation; no citation "
        "validation; no source fetching; no provenance writing; no request "
        "intake; no request validation; no entry gate validation; no readiness "
        "validation; no working entry gate; no gate activation; no gate "
        "execution; no readiness verdict; no validation verdict; no human "
        "context verdict; no identity verdict; no approval; no authorization; "
        "no confirmation; no recommendation; no ranking; no next action "
        "generation; no transition execution; no record creation; no memory "
        "mutation; no roadmap mutation; no P4-M5; no v7; no productization; "
        "no UI; no Operator Console; no version bump; no tag."
    )


_DECLARED_HUMAN_CONTEXT_ENVELOPE_CONTRACT_FIELDS = tuple(
    DeclaredHumanContextEnvelopeContractField(
        index,
        field_id,
        _FIELD_NAMES[index - 1],
        _field_purpose(field_id),
        "p4-m4-declared-human-context-envelope-contract-category",
        (
            "no human context intake semantics; no live human context parsing "
            "semantics; no human context validation semantics; no identity "
            "validation semantics; no actor validation semantics; no user "
            "validation semantics; no operator validation semantics; no "
            "consent validation semantics; no authority validation semantics; "
            "no approval validation semantics; no authorization validation "
            "semantics; no confirmation validation semantics; no human context "
            "record creation semantics; no evidence validation semantics; no "
            "reference resolution semantics; no reference validation semantics; "
            "no citation validation semantics; no source fetching semantics; no "
            "provenance writing semantics; no request intake semantics; no "
            "request validation semantics; no verdict semantics; no approval "
            "semantics; no authorization semantics; no confirmation semantics; "
            "no recommendation semantics; no ranking semantics; no next-action "
            "semantics; no transition execution semantics; no record creation "
            "semantics; no mutation semantics"
        ),
    )
    for index, field_id in enumerate(_FIELD_IDS, start=1)
)


def list_declared_human_context_envelope_contract_fields() -> tuple[DeclaredHumanContextEnvelopeContractField, ...]:
    return _DECLARED_HUMAN_CONTEXT_ENVELOPE_CONTRACT_FIELDS


def declared_human_context_envelope_contract_field_ids() -> tuple[str, ...]:
    return tuple(
        field.field_id
        for field in list_declared_human_context_envelope_contract_fields()
    )


def render_declared_human_context_envelope_contract_markdown(
    fields: Sequence[DeclaredHumanContextEnvelopeContractField] | None = None,
) -> str:
    field_values = (
        tuple(fields)
        if fields is not None
        else list_declared_human_context_envelope_contract_fields()
    )
    status = declared_human_context_envelope_contract_report()
    lines = [
        "# P4-M4.3 Declared Human Context Envelope Contract",
        "",
        "P4-M4.3 Declared Human Context Envelope Contract.",
        "",
        "read-only.",
        "",
        "definition-only.",
        "",
        "declared-human-context-envelope-design-only.",
        "",
        "inspection-only.",
        "",
        "P4-M4.3 Declared Human Context Envelope Contract is definition only.",
        "",
        "P4-M4.3 is declared-human-context-envelope-design-only.",
        "",
        "P4-M4.2 Evidence Reference Envelope Contract remains the direct prior evidence reference envelope reference.",
        "",
        "P4-M4.1 Entry Gate Design Request Envelope Contract remains the inherited prior request envelope reference.",
        "",
        "P4-M4.0 Entry Gate Design Boundary Contract remains the inherited prior design boundary reference.",
        "",
        "P4-M3.16 Governed Transition Intake Final Phase Handoff Summary remains the inherited prior closed-phase handoff reference.",
        "",
        "P4-M3 static definition chain remains closed.",
        "",
        "P4-M4 design layer remains design-boundary-only.",
        "",
        "P4-M4 declared human context envelope design starts only as a static envelope definition.",
        "",
    ]
    for prior_layer in DIRECT_PRIOR_DEFINITION_LAYER_REFERENCES:
        lines.extend([f"{prior_layer} remains a referenced definition layer.", ""])
    for prior_layer in INHERITED_PRIOR_DEFINITION_LAYER_REFERENCES:
        lines.extend([f"{prior_layer} remains an inherited referenced definition layer.", ""])
    for phrase in BOUNDARY_PHRASE_LINES:
        lines.extend([f"{phrase}.", ""])
    lines.extend([
        DECLARED_HUMAN_CONTEXT_ENVELOPE_CONTRACT_BOUNDARY,
        "",
        "## Status Report",
        "",
    ])
    for key, value in status.items():
        lines.append(f"- {key}: {value}")
    lines.extend([
        "",
        "## Declared Human Context Envelope Contract Fields",
        "",
    ])
    for field in field_values:
        lines.extend([
            f"### {field.field_order}. {field.field_id}",
            "",
            f"- Field name: {field.field_name}",
            f"- Field purpose: {field.field_purpose}",
            "- P4-M4 declared human context envelope contract category: "
            f"{field.p4_m4_declared_human_context_envelope_contract_category}",
            "- P4-M4 declared human context envelope contract semantics disabled: "
            f"{field.p4_m4_declared_human_context_envelope_contract_semantics_disabled}",
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def declared_human_context_envelope_contract_as_dicts() -> tuple[dict[str, object], ...]:
    return tuple(
        asdict(field)
        for field in list_declared_human_context_envelope_contract_fields()
    )


def declared_human_context_envelope_contract_report() -> dict[str, object]:
    status: dict[str, object] = {
        "phase": "P4-M4.3",
        "feature": "Declared Human Context Envelope Contract",
        "mode": "read-only",
        "boundary": DECLARED_HUMAN_CONTEXT_ENVELOPE_CONTRACT_BOUNDARY,
        "package_version": P4_M4_3_PACKAGE_VERSION,
        "declared_human_context_envelope_contract_field_count": len(_FIELD_IDS),
        "referenced_p4_m4_2_evidence_reference_envelope_contract_field_count": len(
            evidence_reference_envelope_contract_field_ids()
        ),
    }
    status.update({flag: True for flag in TRUE_STATUS_FLAGS})
    status.update({flag: False for flag in FALSE_STATUS_FLAGS})
    return status
