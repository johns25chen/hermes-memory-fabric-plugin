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


P4_M3_1_PACKAGE_VERSION = "6.16.0"


@dataclass(frozen=True)
class GovernedTransitionIntakeRequestEnvelopeContractField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    p4_m3_request_envelope_contract_category: str
    p4_m3_request_envelope_semantics_disabled: str


PRIOR_DEFINITION_LAYER_REFERENCES = (
    "P4-M3.0 Governed Transition Intake Boundary Contract",
    "P4-M2.17 P4-M2 Closure Handoff Contract",
    "P4-M2.16 Final Non-Execution Boundary Audit",
)


BOUNDARY_PHRASE_LINES = (
    "P4-M3.1",
    "Governed Transition Intake Request Envelope Contract",
    "read-only",
    "definition-only",
    "inspection-only",
    "P4-M3.1 request envelope definition only",
    "P4-M3.0 Governed Transition Intake Boundary Contract remains the source intake boundary",
    "P4-M3.1 is not live request intake",
    "P4-M3.1 is not request acceptance",
    "P4-M3.1 is not request rejection",
    "P4-M3.1 is not request validation",
    "P4-M3.1 is not schema validation",
    "P4-M3.1 is not evidence validation",
    "P4-M3.1 is not consent validation",
    "P4-M3.1 is not transition readiness validation",
    "P4-M3.1 is not transition readiness verdict",
    "P4-M3.1 is not transition execution",
    "P4-M3.1 is not transition authorization",
    "P4-M3.1 is not transition approval",
    "P4-M3.1 is not transition confirmation",
    "P4-M3.1 is not transition recommendation",
    "P4-M3.1 is not transition ranking",
    "P4-M3.1 is not next action generation",
    "P4-M3.1 is not transition record creation",
    "P4-M3.1 is not roadmap mutation",
    "P4-M3.1 is not memory mutation",
    "P4-M3.1 is not lifecycle mutation",
    "P4-M3.1 is not proposal mutation",
    "P4-M3.1 is not evidence mutation",
    "P4-M3.1 is not source fetching",
    "P4-M3.1 is not provenance writing",
    "P4-M3.1 is not citation mutation",
    "no live request intake",
    "no request acceptance",
    "no request rejection",
    "no request validation",
    "no request schema validation",
    "no request content validation",
    "no request completeness validation",
    "no request eligibility validation",
    "no request normalization",
    "no request enrichment",
    "no request routing",
    "no request queueing",
    "no request persistence",
    "no request storage",
    "no request mutation",
    "no request record creation",
    "no request record update",
    "no request record deletion",
    "no execution",
    "no decision execution",
    "no transition execution",
    "no transition command execution",
    "no phase transition execution",
    "no authorization",
    "no transition authorization",
    "no approval",
    "no transition approval",
    "no confirmation",
    "no transition confirmation",
    "no recommendation",
    "no transition recommendation",
    "no ranking",
    "no transition ranking",
    "no suggested next action",
    "no next action generation",
    "no readiness verdict",
    "no transition readiness verdict",
    "no validation verdict",
    "no transition validation verdict",
    "no override verdict",
    "no transition override verdict",
    "no precedence verdict",
    "no conflict resolution verdict",
    "no automatic readiness verdict",
    "no evidence validation",
    "no live evidence validation",
    "no transition readiness validation",
    "no live transition readiness validation",
    "no consent validation",
    "no live consent validation",
    "no live confirmation validation",
    "no live authorization validation",
    "no live contract validation",
    "no input validation",
    "no record validation",
    "no risk acceptance",
    "no risk waiver",
    "no implied risk acceptance",
    "no implied risk waiver",
    "no acknowledgement-as-acceptance",
    "no acknowledgement-as-waiver",
    "no evidence precedence",
    "no source precedence",
    "no chronological precedence",
    "no recency precedence",
    "no confidence precedence",
    "no authority precedence",
    "no citation precedence",
    "no winning evidence",
    "no evidence winner",
    "no evidence ranking",
    "no evidence scoring",
    "no source ranking",
    "no evidence tie-breaker",
    "no evidence arbitration",
    "no conflict resolution",
    "no evidence resolution",
    "no evidence merge",
    "no evidence reconciliation",
    "no evidence override",
    "no approval override",
    "no authorization override",
    "no readiness override",
    "no execution override",
    "no transition override",
    "no consent override",
    "no risk acceptance override",
    "no risk waiver override",
    "no transition record creation",
    "no transition readiness record creation",
    "no transition validation record creation",
    "no transition approval record creation",
    "no transition authorization record creation",
    "no transition confirmation record creation",
    "no transition execution record creation",
    "no transition recommendation record creation",
    "no transition ranking record creation",
    "no transition next-action record creation",
    "no evidence precedence record creation",
    "no evidence ranking record creation",
    "no evidence score record creation",
    "no evidence winner record creation",
    "no evidence arbitration record creation",
    "no conflict resolution record creation",
    "no evidence merge record creation",
    "no evidence override record creation",
    "no approval override record creation",
    "no consent record creation",
    "no non-consent record creation",
    "no memory mutation",
    "no memory record creation",
    "no memory record update",
    "no memory record deletion",
    "no proposal mutation",
    "no lifecycle mutation",
    "no retry policy mutation",
    "no source fetching",
    "no provenance writing",
    "no evidence mutation",
    "no citation mutation",
    "no roadmap mutation",
    "no execution semantics",
    "no authorization semantics",
    "no confirmation semantics",
    "no approval semantics",
    "no recommendation semantics",
    "no ranking semantics",
    "no next-action semantics",
    "no validation semantics",
    "no readiness semantics",
    "no override semantics",
    "no request semantics",
    "no live request semantics",
    "no request validation semantics",
    "no request acceptance semantics",
    "no request rejection semantics",
    "no request routing semantics",
    "no request persistence semantics",
    "no request mutation semantics",
    "no transition semantics",
    "no transition execution semantics",
    "no transition authorization semantics",
    "no transition approval semantics",
    "no transition confirmation semantics",
    "no transition recommendation semantics",
    "no transition ranking semantics",
    "no transition readiness semantics",
    "no transition validation semantics",
    "no transition next-action semantics",
    "no mutation semantics",
    "no roadmap mutation semantics",
    "no API",
    "no MCP",
    "no connector",
    "no agent call",
    "no Codex/Hermes/ChatGPT product-code auto-call",
    "no P4-M3.2",
    "no P4-M3.2 command",
    "no P4-M3.2 activation",
    "no P4-M3.2 implementation",
    "no P4-M4",
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


GOVERNED_TRANSITION_INTAKE_REQUEST_ENVELOPE_CONTRACT_BOUNDARY = (
    "P4-M3.1 Governed Transition Intake Request Envelope Contract read-only "
    "definition-only inspection-only. P4-M3.1 request envelope definition only. "
    "P4-M3.0 Governed Transition Intake Boundary Contract remains the source "
    "intake boundary. P4-M3.1 defines only the static request envelope shape "
    "for future governed transition intake work; it does not parse live request "
    "payloads, accept requests, reject requests, validate request contents, "
    "validate schema, validate evidence, validate consent, validate transition "
    "readiness, produce readiness verdict, produce validation verdict, execute "
    "transition, authorize transition, approve transition, confirm transition, "
    "recommend transition, rank transition candidates, produce next action, "
    "create transition records, mutate memory, mutate roadmap, mutate proposal, "
    "mutate lifecycle, fetch sources, write provenance, mutate evidence, mutate "
    "citations, call APIs, call MCP, call connectors, call agents, productize, "
    "deploy, create UI, create Operator Console behavior, start P4-M3.2, start "
    "P4-M4, start P4-M5, or start v7. "
    + " ".join(f"{phrase}." for phrase in BOUNDARY_PHRASE_LINES)
)


_FIELD_IDS = (
    "p4-m3-governed-transition-intake-request-envelope-contract-id",
    "p4-m3-governed-transition-intake-boundary-contract-reference",
    "p4-m2-closure-handoff-contract-reference",
    "p4-m2-final-non-execution-boundary-audit-reference",
    "p4-m3-request-envelope-source-reference",
    "p4-m3-request-envelope-scope",
    "p4-m3-request-envelope-target-label-reference",
    "p4-m3-request-envelope-request-identity-field",
    "p4-m3-request-envelope-requester-reference-field",
    "p4-m3-request-envelope-intent-description-field",
    "p4-m3-request-envelope-target-phase-label-field",
    "p4-m3-request-envelope-source-context-field",
    "p4-m3-request-envelope-declared-evidence-reference-field",
    "p4-m3-request-envelope-declared-human-context-field",
    "p4-m3-request-envelope-non-validation-boundary",
    "p4-m3-request-envelope-non-mutation-boundary",
    "p4-m3-request-envelope-contract-category",
    "p4-m3-request-envelope-semantics-disabled",
)


_FIELD_NAMES = (
    "P4-M3 Governed Transition Intake Request Envelope Contract Identifier",
    "P4-M3 Governed Transition Intake Boundary Contract Reference",
    "P4-M2 Closure Handoff Contract Reference",
    "P4-M2 Final Non-Execution Boundary Audit Reference",
    "P4-M3 Request Envelope Source Reference",
    "P4-M3 Request Envelope Scope",
    "P4-M3 Request Envelope Target Label Reference",
    "P4-M3 Request Envelope Request Identity Field",
    "P4-M3 Request Envelope Requester Reference Field",
    "P4-M3 Request Envelope Intent Description Field",
    "P4-M3 Request Envelope Target Phase Label Field",
    "P4-M3 Request Envelope Source Context Field",
    "P4-M3 Request Envelope Declared Evidence Reference Field",
    "P4-M3 Request Envelope Declared Human Context Field",
    "P4-M3 Request Envelope Non-Validation Boundary",
    "P4-M3 Request Envelope Non-Mutation Boundary",
    "P4-M3 Request Envelope Contract Category",
    "P4-M3 Request Envelope Semantics Disabled",
)


def _field_purpose(field_id: str) -> str:
    return (
        f"Defines {field_id} as read-only definition-only inspection-only "
        "P4-M3.1 request envelope definition only context; P4-M3.0 Governed "
        "Transition Intake Boundary Contract remains the source intake boundary, "
        "P4-M3.1 is not live request intake, not request acceptance, not request "
        "rejection, not request validation, not schema validation, not evidence "
        "validation, not consent validation, not transition readiness validation, "
        "not transition readiness verdict, not transition execution, not "
        "transition authorization, not transition approval, not transition "
        "confirmation, not transition recommendation, not transition ranking, "
        "no next action generation, no transition record creation, no memory "
        "mutation, no roadmap mutation, no P4-M3.2, no P4-M4, no P4-M5, no v7, "
        "no productization, no UI, no Operator Console, no version bump, and no tag."
    )


_GOVERNED_TRANSITION_INTAKE_REQUEST_ENVELOPE_CONTRACT_FIELDS = tuple(
    GovernedTransitionIntakeRequestEnvelopeContractField(
        index,
        field_id,
        _FIELD_NAMES[index - 1],
        _field_purpose(field_id),
        "p4-m3-request-envelope-contract-category",
        "no request semantics; no validation semantics; no mutation semantics",
    )
    for index, field_id in enumerate(_FIELD_IDS, start=1)
)


def list_governed_transition_intake_request_envelope_contract_fields() -> (
    tuple[GovernedTransitionIntakeRequestEnvelopeContractField, ...]
):
    return _GOVERNED_TRANSITION_INTAKE_REQUEST_ENVELOPE_CONTRACT_FIELDS


def governed_transition_intake_request_envelope_contract_field_ids() -> tuple[str, ...]:
    return tuple(
        field.field_id
        for field in list_governed_transition_intake_request_envelope_contract_fields()
    )


def render_governed_transition_intake_request_envelope_contract_markdown(
    fields: Sequence[GovernedTransitionIntakeRequestEnvelopeContractField] | None = None,
) -> str:
    field_values = (
        tuple(fields)
        if fields is not None
        else list_governed_transition_intake_request_envelope_contract_fields()
    )
    status = governed_transition_intake_request_envelope_contract_report()
    lines = [
        "# P4-M3.1 Governed Transition Intake Request Envelope Contract",
        "",
        "P4-M3.1 Governed Transition Intake Request Envelope Contract.",
        "",
        "read-only.",
        "",
        "definition-only.",
        "",
        "inspection-only.",
        "",
        "P4-M3.1 request envelope definition only.",
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
            GOVERNED_TRANSITION_INTAKE_REQUEST_ENVELOPE_CONTRACT_BOUNDARY,
            "",
            "## Status Report",
            "",
        ]
    )
    for key, value in status.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Governed Transition Intake Request Envelope Contract Fields", ""])
    for field in field_values:
        lines.extend(
            [
                f"### {field.field_order}. {field.field_id}",
                "",
                f"- Field name: {field.field_name}",
                f"- Field purpose: {field.field_purpose}",
                (
                    "- P4-M3 request envelope contract category: "
                    f"{field.p4_m3_request_envelope_contract_category}"
                ),
                (
                    "- P4-M3 request envelope semantics disabled: "
                    f"{field.p4_m3_request_envelope_semantics_disabled}"
                ),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def governed_transition_intake_request_envelope_contract_as_dicts(
    fields: Sequence[GovernedTransitionIntakeRequestEnvelopeContractField] | None = None,
) -> tuple[dict[str, object], ...]:
    field_values = (
        tuple(fields)
        if fields is not None
        else list_governed_transition_intake_request_envelope_contract_fields()
    )
    return tuple(asdict(field) for field in field_values)


def governed_transition_intake_request_envelope_contract_report() -> dict[str, object]:
    disabled_false_flags = {
        "live_request_intake_enabled": False,
        "request_acceptance_enabled": False,
        "request_rejection_enabled": False,
        "request_validation_enabled": False,
        "request_schema_validation_enabled": False,
        "request_content_validation_enabled": False,
        "request_completeness_validation_enabled": False,
        "request_eligibility_validation_enabled": False,
        "request_normalization_enabled": False,
        "request_enrichment_enabled": False,
        "request_routing_enabled": False,
        "request_queueing_enabled": False,
        "request_persistence_enabled": False,
        "request_storage_enabled": False,
        "request_mutation_enabled": False,
        "request_record_creation_enabled": False,
        "request_record_update_enabled": False,
        "request_record_deletion_enabled": False,
        "execution_enabled": False,
        "decision_execution_enabled": False,
        "transition_execution_enabled": False,
        "transition_command_execution_enabled": False,
        "phase_transition_execution_enabled": False,
        "authorization_enabled": False,
        "transition_authorization_enabled": False,
        "approval_enabled": False,
        "transition_approval_enabled": False,
        "confirmation_enabled": False,
        "transition_confirmation_enabled": False,
        "recommendation_enabled": False,
        "transition_recommendation_enabled": False,
        "ranking_enabled": False,
        "transition_ranking_enabled": False,
        "suggested_next_action_enabled": False,
        "next_action_generation_enabled": False,
        "readiness_verdict_enabled": False,
        "transition_readiness_verdict_enabled": False,
        "validation_verdict_enabled": False,
        "transition_validation_verdict_enabled": False,
        "override_verdict_enabled": False,
        "transition_override_verdict_enabled": False,
        "precedence_verdict_enabled": False,
        "conflict_resolution_verdict_enabled": False,
        "automatic_readiness_verdict_enabled": False,
        "evidence_validation_enabled": False,
        "live_evidence_validation_enabled": False,
        "transition_readiness_validation_enabled": False,
        "live_transition_readiness_validation_enabled": False,
        "consent_validation_enabled": False,
        "live_consent_validation_enabled": False,
        "live_confirmation_validation_enabled": False,
        "live_authorization_validation_enabled": False,
        "live_contract_validation_enabled": False,
        "input_validation_enabled": False,
        "record_validation_enabled": False,
        "risk_acceptance_enabled": False,
        "risk_waiver_enabled": False,
        "evidence_precedence_enabled": False,
        "source_precedence_enabled": False,
        "chronological_precedence_enabled": False,
        "recency_precedence_enabled": False,
        "confidence_precedence_enabled": False,
        "authority_precedence_enabled": False,
        "citation_precedence_enabled": False,
        "winning_evidence_enabled": False,
        "evidence_winner_enabled": False,
        "evidence_ranking_enabled": False,
        "evidence_scoring_enabled": False,
        "source_ranking_enabled": False,
        "evidence_tie_breaker_enabled": False,
        "evidence_arbitration_enabled": False,
        "conflict_resolution_enabled": False,
        "evidence_resolution_enabled": False,
        "evidence_merge_enabled": False,
        "evidence_reconciliation_enabled": False,
        "evidence_override_enabled": False,
        "approval_override_enabled": False,
        "authorization_override_enabled": False,
        "readiness_override_enabled": False,
        "execution_override_enabled": False,
        "transition_override_enabled": False,
        "consent_override_enabled": False,
        "risk_acceptance_override_enabled": False,
        "risk_waiver_override_enabled": False,
        "transition_record_creation_enabled": False,
        "transition_readiness_record_creation_enabled": False,
        "transition_validation_record_creation_enabled": False,
        "transition_approval_record_creation_enabled": False,
        "transition_authorization_record_creation_enabled": False,
        "transition_confirmation_record_creation_enabled": False,
        "transition_execution_record_creation_enabled": False,
        "transition_recommendation_record_creation_enabled": False,
        "transition_ranking_record_creation_enabled": False,
        "transition_next_action_record_creation_enabled": False,
        "memory_mutation_enabled": False,
        "memory_record_creation_enabled": False,
        "memory_record_update_enabled": False,
        "memory_record_deletion_enabled": False,
        "proposal_mutation_enabled": False,
        "lifecycle_mutation_enabled": False,
        "retry_policy_mutation_enabled": False,
        "source_fetching_enabled": False,
        "provenance_writing_enabled": False,
        "evidence_mutation_enabled": False,
        "citation_mutation_enabled": False,
        "roadmap_mutation_enabled": False,
        "api_enabled": False,
        "mcp_enabled": False,
        "connector_enabled": False,
        "agent_call_enabled": False,
        "codex_hermes_chatgpt_product_code_auto_call_enabled": False,
        "p4_m3_2_started": False,
        "p4_m3_2_command_enabled": False,
        "p4_m3_2_activation_enabled": False,
        "p4_m3_2_implementation_enabled": False,
        "p4_m4_started": False,
        "p4_m5_started": False,
        "v7_started": False,
        "productization_started": False,
        "ui_started": False,
        "operator_console_started": False,
        "mvp_started": False,
        "deploy_started": False,
        "full_memory_graph_started": False,
        "version_bump_enabled": False,
        "tag_creation_enabled": False,
    }
    return {
        "phase": "P4-M3.1",
        "feature": "Governed Transition Intake Request Envelope Contract",
        "mode": "read-only",
        "definition_only": True,
        "inspection_only": True,
        "governed_transition_intake_request_envelope_contract_field_count": len(
            _GOVERNED_TRANSITION_INTAKE_REQUEST_ENVELOPE_CONTRACT_FIELDS
        ),
        "p4_m3_request_envelope_definition_started": True,
        "p4_m3_1_governed_transition_intake_request_envelope_contract_started": True,
        "p4_m3_1_definition_only": True,
        "p4_m3_0_intake_boundary_contract_reference_defined": True,
        "p4_m2_17_closure_handoff_contract_reference_defined": True,
        "p4_m2_final_non_execution_boundary_reference_defined": True,
        "p4_m3_request_envelope_contract_defined": True,
        "p4_m3_request_envelope_scope_defined": True,
        "p4_m3_request_envelope_field_shape_defined": True,
        "p4_m3_request_intake_semantics_prohibited": True,
        "p4_m3_request_acceptance_semantics_prohibited": True,
        "p4_m3_request_rejection_semantics_prohibited": True,
        "p4_m3_request_validation_semantics_prohibited": True,
        "p4_m3_transition_execution_semantics_prohibited": True,
        "p4_m3_transition_authorization_semantics_prohibited": True,
        "p4_m3_transition_approval_semantics_prohibited": True,
        "p4_m3_transition_confirmation_semantics_prohibited": True,
        "p4_m3_transition_recommendation_semantics_prohibited": True,
        "p4_m3_transition_ranking_semantics_prohibited": True,
        "p4_m3_transition_readiness_verdict_semantics_prohibited": True,
        "p4_m3_transition_validation_verdict_semantics_prohibited": True,
        "p4_m3_transition_mutation_semantics_prohibited": True,
        "p4_m3_2_start_deferred": True,
        **disabled_false_flags,
        "boundary": GOVERNED_TRANSITION_INTAKE_REQUEST_ENVELOPE_CONTRACT_BOUNDARY,
    }


if len(_FIELD_IDS) != 18:
    raise RuntimeError("P4-M3.1 governed transition intake request envelope field drift")

if len(PRIOR_DEFINITION_LAYER_REFERENCES) != 3:
    raise RuntimeError("P4-M3.1 prior definition layer reference drift")

if not governed_transition_intake_boundary_contract_field_ids():
    raise RuntimeError("P4-M3.1 P4-M3.0 intake boundary reference is empty")

if not closure_handoff_contract_field_ids():
    raise RuntimeError("P4-M3.1 P4-M2.17 closure handoff reference is empty")

if not final_non_execution_boundary_audit_field_ids():
    raise RuntimeError("P4-M3.1 P4-M2.16 audit reference is empty")
