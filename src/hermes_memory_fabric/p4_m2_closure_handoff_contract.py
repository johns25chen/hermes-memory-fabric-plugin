from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence

from .p4_m2_final_non_execution_boundary_audit import (
    final_non_execution_boundary_audit_field_ids,
)


P4_M2_17_PACKAGE_VERSION = "6.16.0"


@dataclass(frozen=True)
class ClosureHandoffContractField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    closure_handoff_contract_category: str
    closure_handoff_semantics_disabled: str


PRIOR_DEFINITION_LAYER_REFERENCES = (
    "P4-M2.1 Execution Surface Contract Definition",
    "P4-M2.2 Execution Contract Validation Matrix",
    "P4-M2.3 Manual Authorization Evidence Envelope",
    "P4-M2.4 Human Confirmation Snapshot Contract",
    "P4-M2.5 Execution Preconditions Snapshot Map",
    "P4-M2.6 Execution Risk Acknowledgement Map",
    "P4-M2.7 Execution Risk Acceptance Prohibition Map",
    "P4-M2.8 Execution Risk Waiver Prohibition Map",
    "P4-M2.9 Execution Decision Non-Equivalence Map",
    "P4-M2.10 Execution Decision Recommendation Prohibition Map",
    "P4-M2.11 Execution Decision Default Denial Boundary Map",
    "P4-M2.12 Execution Decision Silence Non-Consent Map",
    "P4-M2.13 Execution Decision Negative Evidence Non-Override Map",
    "P4-M2.14 Execution Decision Conflicting Evidence Isolation Map",
    "P4-M2.15 Execution Decision Evidence Precedence Prohibition Map",
    "P4-M2.16 Final Non-Execution Boundary Audit",
)


BOUNDARY_PHRASE_LINES = (
    "P4-M2.17",
    "P4-M2 Closure Handoff Contract",
    "Closure Handoff Contract",
    "read-only",
    "definition-only",
    "inspection-only",
    "P4-M2.x closure handoff only",
    "P4-M2.1 through P4-M2.16 remain definition-only",
    "handoff is not readiness",
    "handoff is not approval",
    "handoff is not authorization",
    "handoff is not execution",
    "handoff is not recommendation",
    "handoff is not ranking",
    "handoff is not transition execution",
    "handoff is not P4-M3 start",
    "no execution",
    "no decision execution",
    "no authorization",
    "no decision authorization",
    "no confirmation",
    "no decision confirmation",
    "no approval",
    "no decision approval",
    "no rejection",
    "no decision rejection",
    "no recommendation",
    "no decision recommendation",
    "no ranking",
    "no decision ranking",
    "no suggested next action",
    "no readiness verdict",
    "no validation verdict",
    "no override verdict",
    "no precedence verdict",
    "no conflict resolution verdict",
    "no automatic readiness verdict",
    "no execution hint",
    "no authorization hint",
    "no confirmation hint",
    "no approval hint",
    "no recommendation hint",
    "no readiness hint",
    "no validation hint",
    "no override hint",
    "no resolution hint",
    "no precedence hint",
    "no default readiness",
    "no default approval",
    "no default allow",
    "no default permit",
    "no default continue",
    "no default execute",
    "no auto-pass",
    "no auto-execution hint",
    "no advisory verdict",
    "no evidence validation",
    "no live evidence validation",
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
    "no consent override",
    "no risk acceptance override",
    "no risk waiver override",
    "no transition execution",
    "no transition command",
    "no phase transition action",
    "no handoff execution",
    "no handoff authorization",
    "no handoff approval",
    "no handoff recommendation",
    "no handoff ranking",
    "no handoff readiness verdict",
    "no handoff validation verdict",
    "no handoff override verdict",
    "no handoff mutation",
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
    "no rejection execution semantics",
    "no recommendation semantics",
    "no ranking semantics",
    "no next-action semantics",
    "no validation semantics",
    "no readiness semantics",
    "no override semantics",
    "no conflict resolution semantics",
    "no evidence resolution semantics",
    "no evidence merge semantics",
    "no evidence arbitration semantics",
    "no evidence precedence semantics",
    "no source precedence semantics",
    "no winner semantics",
    "no acceptance semantics",
    "no waiver semantics",
    "no acknowledgement semantics",
    "no consent semantics",
    "no permission semantics",
    "no default-allowance semantics",
    "no transition semantics",
    "no handoff execution semantics",
    "no handoff authorization semantics",
    "no handoff approval semantics",
    "no handoff readiness semantics",
    "no API",
    "no MCP",
    "no connector",
    "no agent call",
    "no Codex/Hermes/ChatGPT product-code auto-call",
    "no P4-M3",
    "no P4-M3 command",
    "no P4-M3 activation",
    "no P4-M3 implementation",
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


CLOSURE_HANDOFF_CONTRACT_BOUNDARY = (
    "P4-M2.17 P4-M2 Closure Handoff Contract read-only definition-only "
    "inspection-only. This Closure Handoff Contract is P4-M2.x closure "
    "handoff only; P4-M2.1 through P4-M2.16 remain definition-only. The "
    "handoff is not readiness, handoff is not approval, handoff is not "
    "authorization, handoff is not execution, handoff is not recommendation, "
    "handoff is not ranking, handoff is not transition execution, and handoff "
    "is not P4-M3 start. It records how the P4-M2.x non-execution definition "
    "corridor may be referenced before any future P4-M3 work without creating "
    "P4-M3 work, P4-M3 commands, P4-M3 APIs, P4-M3 readiness, P4-M3 "
    "authorization, P4-M3 approval, P4-M3 execution, P4-M3 implementation, or "
    "P4-M3 mutation. "
    + " ".join(f"{phrase}." for phrase in BOUNDARY_PHRASE_LINES)
)


_FIELD_IDS = (
    "p4-m2-closure-handoff-contract-id",
    "p4-m2-closure-source-reference",
    "p4-m2-final-non-execution-boundary-audit-reference",
    "p4-m2-prior-definition-layer-reference-set",
    "p4-m3-target-label-reference",
    "p4-m3-not-started-boundary",
    "closure-handoff-contract-scope",
    "closure-handoff-non-execution-boundary",
    "closure-handoff-non-authorization-boundary",
    "closure-handoff-non-confirmation-boundary",
    "closure-handoff-non-approval-boundary",
    "closure-handoff-non-recommendation-boundary",
    "closure-handoff-non-ranking-boundary",
    "closure-handoff-non-verdict-boundary",
    "closure-handoff-non-override-boundary",
    "closure-handoff-non-mutation-boundary",
    "closure-handoff-contract-category",
    "closure-handoff-semantics-disabled",
)


_FIELD_NAMES = (
    "P4-M2 Closure Handoff Contract Identifier",
    "P4-M2 Closure Source Reference",
    "P4-M2 Final Non-Execution Boundary Audit Reference",
    "P4-M2 Prior Definition Layer Reference Set",
    "P4-M3 Target Label Reference",
    "P4-M3 Not Started Boundary",
    "Closure Handoff Contract Scope",
    "Closure Handoff Non-Execution Boundary",
    "Closure Handoff Non-Authorization Boundary",
    "Closure Handoff Non-Confirmation Boundary",
    "Closure Handoff Non-Approval Boundary",
    "Closure Handoff Non-Recommendation Boundary",
    "Closure Handoff Non-Ranking Boundary",
    "Closure Handoff Non-Verdict Boundary",
    "Closure Handoff Non-Override Boundary",
    "Closure Handoff Non-Mutation Boundary",
    "Closure Handoff Contract Category",
    "Closure Handoff Semantics Disabled",
)


def _field_purpose(field_id: str) -> str:
    return (
        f"Defines {field_id} as read-only definition-only inspection-only "
        "P4-M2.x closure handoff only context; P4-M2.1 through P4-M2.16 remain "
        "definition-only, handoff is not P4-M3 start, no execution, no "
        "authorization, no approval, no recommendation, no ranking, no "
        "readiness verdict, no validation verdict, no precedence verdict, no "
        "override verdict, no transition execution, no phase transition action, "
        "no handoff execution, no memory mutation, no version bump, and no tag."
    )


_CLOSURE_HANDOFF_CONTRACT_FIELDS = tuple(
    ClosureHandoffContractField(
        index,
        field_id,
        _FIELD_NAMES[index - 1],
        _field_purpose(field_id),
        "closure-handoff-contract-category",
        "no handoff execution semantics; no transition semantics; no mutation semantics",
    )
    for index, field_id in enumerate(_FIELD_IDS, start=1)
)


def list_closure_handoff_contract_fields() -> tuple[ClosureHandoffContractField, ...]:
    return _CLOSURE_HANDOFF_CONTRACT_FIELDS


def closure_handoff_contract_field_ids() -> tuple[str, ...]:
    return tuple(field.field_id for field in list_closure_handoff_contract_fields())


def render_closure_handoff_contract_markdown(
    fields: Sequence[ClosureHandoffContractField] | None = None,
) -> str:
    field_values = tuple(fields) if fields is not None else list_closure_handoff_contract_fields()
    status = closure_handoff_contract_report()
    lines = [
        "# P4-M2.17 P4-M2 Closure Handoff Contract",
        "",
        "P4-M2.17 P4-M2 Closure Handoff Contract.",
        "",
        "Closure Handoff Contract.",
        "",
        "read-only.",
        "",
        "definition-only.",
        "",
        "inspection-only.",
        "",
        "P4-M2.x closure handoff only.",
        "",
        "P4-M2.1 through P4-M2.16 remain definition-only.",
        "",
        "handoff is not P4-M3 start.",
        "",
    ]
    for prior_layer in PRIOR_DEFINITION_LAYER_REFERENCES:
        lines.extend([f"{prior_layer} remains a referenced definition layer.", ""])
    for phrase in BOUNDARY_PHRASE_LINES:
        lines.extend([f"{phrase}.", ""])
    lines.extend(
        [
            CLOSURE_HANDOFF_CONTRACT_BOUNDARY,
            "",
            "## Status Report",
            "",
        ]
    )
    for key, value in status.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Closure Handoff Contract Fields", ""])
    for field in field_values:
        lines.extend(
            [
                f"### {field.field_order}. {field.field_id}",
                "",
                f"- Field name: {field.field_name}",
                f"- Field purpose: {field.field_purpose}",
                f"- Closure handoff contract category: {field.closure_handoff_contract_category}",
                f"- Closure handoff semantics disabled: {field.closure_handoff_semantics_disabled}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def closure_handoff_contract_as_dicts(
    fields: Sequence[ClosureHandoffContractField] | None = None,
) -> tuple[dict[str, object], ...]:
    field_values = tuple(fields) if fields is not None else list_closure_handoff_contract_fields()
    return tuple(asdict(field) for field in field_values)


def closure_handoff_contract_report() -> dict[str, object]:
    disabled_false_flags = {
        "execution_enabled": False,
        "decision_execution_enabled": False,
        "authorization_enabled": False,
        "decision_authorization_enabled": False,
        "confirmation_enabled": False,
        "decision_confirmation_enabled": False,
        "approval_enabled": False,
        "decision_approval_enabled": False,
        "rejection_enabled": False,
        "decision_rejection_enabled": False,
        "recommendation_enabled": False,
        "decision_recommendation_enabled": False,
        "ranking_enabled": False,
        "decision_ranking_enabled": False,
        "suggested_next_action_enabled": False,
        "readiness_verdict_enabled": False,
        "validation_verdict_enabled": False,
        "override_verdict_enabled": False,
        "precedence_verdict_enabled": False,
        "conflict_resolution_verdict_enabled": False,
        "automatic_readiness_verdict_enabled": False,
        "execution_hint_enabled": False,
        "authorization_hint_enabled": False,
        "confirmation_hint_enabled": False,
        "approval_hint_enabled": False,
        "recommendation_hint_enabled": False,
        "readiness_hint_enabled": False,
        "validation_hint_enabled": False,
        "override_hint_enabled": False,
        "resolution_hint_enabled": False,
        "precedence_hint_enabled": False,
        "default_readiness_enabled": False,
        "default_approval_enabled": False,
        "default_allow_enabled": False,
        "default_permit_enabled": False,
        "default_continue_enabled": False,
        "default_execute_enabled": False,
        "auto_pass_enabled": False,
        "auto_execution_hint_enabled": False,
        "advisory_verdict_enabled": False,
        "evidence_validation_enabled": False,
        "live_evidence_validation_enabled": False,
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
        "consent_override_enabled": False,
        "risk_acceptance_override_enabled": False,
        "risk_waiver_override_enabled": False,
        "transition_execution_enabled": False,
        "transition_command_enabled": False,
        "phase_transition_action_enabled": False,
        "handoff_execution_enabled": False,
        "handoff_authorization_enabled": False,
        "handoff_approval_enabled": False,
        "handoff_recommendation_enabled": False,
        "handoff_ranking_enabled": False,
        "handoff_readiness_verdict_enabled": False,
        "handoff_validation_verdict_enabled": False,
        "handoff_override_verdict_enabled": False,
        "handoff_mutation_enabled": False,
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
        "p4_m3_started": False,
        "p4_m3_command_enabled": False,
        "p4_m3_activation_enabled": False,
        "p4_m3_implementation_enabled": False,
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
        "phase": "P4-M2.17",
        "feature": "P4-M2 Closure Handoff Contract",
        "mode": "read-only",
        "definition_only": True,
        "inspection_only": True,
        "closure_handoff_contract_field_count": len(_CLOSURE_HANDOFF_CONTRACT_FIELDS),
        "p4_m2_started": True,
        "p4_m2_closure_handoff_contract_started": True,
        "p4_m2_closure_handoff_contract_definition_only": True,
        "p4_m2_1_through_p4_m2_16_references_defined": True,
        "p4_m2_closure_handoff_contract_defined": True,
        "p4_m2_to_p4_m3_boundary_documented": True,
        "p4_m3_start_deferred": True,
        "p4_m2_execution_semantics_prohibited": True,
        "p4_m2_authorization_semantics_prohibited": True,
        "p4_m2_confirmation_semantics_prohibited": True,
        "p4_m2_approval_semantics_prohibited": True,
        "p4_m2_recommendation_semantics_prohibited": True,
        "p4_m2_ranking_semantics_prohibited": True,
        "p4_m2_validation_verdict_semantics_prohibited": True,
        "p4_m2_precedence_verdict_semantics_prohibited": True,
        "p4_m2_override_semantics_prohibited": True,
        "p4_m2_transition_semantics_prohibited": True,
        "p4_m2_mutation_semantics_prohibited": True,
        **disabled_false_flags,
        "boundary": CLOSURE_HANDOFF_CONTRACT_BOUNDARY,
    }


if len(_FIELD_IDS) != 18:
    raise RuntimeError("P4-M2.17 closure handoff contract field drift")

if len(PRIOR_DEFINITION_LAYER_REFERENCES) != 16:
    raise RuntimeError("P4-M2.17 prior definition layer reference drift")

if not final_non_execution_boundary_audit_field_ids():
    raise RuntimeError("P4-M2.17 final non-execution boundary audit reference is empty")
