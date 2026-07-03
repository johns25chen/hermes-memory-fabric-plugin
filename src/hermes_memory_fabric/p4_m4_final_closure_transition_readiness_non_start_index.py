from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence

from .p4_m4_final_closure_operator_handoff_index import (
    p4_m4_final_closure_operator_handoff_index_field_ids,
)


P4_M4_FC_3_PACKAGE_VERSION = "6.16.0"


@dataclass(frozen=True)
class P4M4FinalClosureTransitionReadinessNonStartIndexField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    p4_m4_final_closure_transition_readiness_non_start_index_category: str
    p4_m4_final_closure_transition_readiness_non_start_index_semantics_disabled: str


DIRECT_PRIOR_DEFINITION_LAYER_REFERENCES = (
    "P4-M4-FC.2 P4-M4 Final Closure Operator Handoff Index",
)

INHERITED_PRIOR_DEFINITION_LAYER_REFERENCES = (
    "P4-M4-FC.1 P4-M4 Final Closure Evidence Index",
    "P4-M4-FC.0 P4-M4 Final Closure Index / P4-M5 Entry Planning Gate",
    "P4-M4.17 Entry Gate Design Phase Terminal Closure Seal",
    "P4-M4.16 Entry Gate Design Final Phase Handoff Summary",
    "P4-M4.15 Entry Gate Design Phase Closure Review",
    "P4-M4.14 Entry Gate Design Closure Handoff Contract",
    "P4-M4.13 Entry Gate Design Final Non-Validation Boundary Audit",
    "P4-M4.12 Declared Transition Package Assembly Envelope Contract",
    "P4-M4.11 Declared Transition Safeguard Envelope Contract",
    "P4-M4.10 Declared Transition Assumption Envelope Contract",
    "P4-M4.9 Declared Transition Risk Envelope Contract",
    "P4-M4.8 Declared Transition Impact Envelope Contract",
    "P4-M4.7 Declared Transition Dependency Envelope Contract",
    "P4-M4.6 Declared Transition Constraint Envelope Contract",
    "P4-M4.5 Declared Transition Reason Envelope Contract",
    "P4-M4.4 Target Phase Envelope Contract",
    "P4-M4.3 Declared Human Context Envelope Contract",
    "P4-M4.2 Evidence Reference Envelope Contract",
    "P4-M4.1 Entry Gate Design Request Envelope Contract",
    "P4-M4.0 Entry Gate Design Boundary Contract",
    "P4-M3.16 Governed Transition Intake Final Phase Handoff Summary",
)


BOUNDARY_PHRASE_LINES = tuple(
    line
    for line in """
P4-M4-FC.3
P4-M4 Final Closure Transition Readiness Non-Start Index
read-only
definition-only
p4-m4-final-closure-transition-readiness-non-start-index-only
transition-readiness-non-start-index-only
transition-readiness-non-validation-boundary-only
transition-readiness-non-scoring-boundary-only
transition-readiness-non-verdict-boundary-only
transition-readiness-non-execution-boundary-only
transition-readiness-non-record-boundary-only
transition-readiness-non-mutation-boundary-only
p4-m5-non-start-boundary-only
declaration-only
inspection-only
P4-M4-FC.3 is not P4-M4.18
P4-M4-FC.3 is not P4-M5
P4-M4-FC.3 P4-M4 Final Closure Transition Readiness Non-Start Index is definition only
P4-M4-FC.3 is p4-m4-final-closure-transition-readiness-non-start-index-only
P4-M4-FC.3 is transition-readiness-non-start-index-only
P4-M4-FC.3 is transition-readiness-non-validation-boundary-only
P4-M4-FC.3 is transition-readiness-non-scoring-boundary-only
P4-M4-FC.3 is transition-readiness-non-verdict-boundary-only
P4-M4-FC.3 is transition-readiness-non-execution-boundary-only
P4-M4-FC.3 is transition-readiness-non-record-boundary-only
P4-M4-FC.3 is transition-readiness-non-mutation-boundary-only
P4-M4-FC.3 is p4-m5-non-start-boundary-only
P4-M4-FC.3 is declaration-only
P4-M4-FC.2 P4-M4 Final Closure Operator Handoff Index remains the direct prior final closure operator handoff index reference
P4-M4-FC.2 remains only an inherited static final closure operator handoff index surface reference
P4-M4-FC.1 P4-M4 Final Closure Evidence Index remains the inherited prior final closure evidence index reference
P4-M4-FC.0 P4-M4 Final Closure Index / P4-M5 Entry Planning Gate remains the inherited prior final closure index and entry planning gate reference
P4-M4.17 Entry Gate Design Phase Terminal Closure Seal remains the inherited prior terminal closure seal reference
P4-M4.16 Entry Gate Design Final Phase Handoff Summary remains the inherited prior final phase handoff summary reference
P4-M4.15 Entry Gate Design Phase Closure Review remains the inherited prior phase closure review reference
P4-M4.14 Entry Gate Design Closure Handoff Contract remains the inherited prior closure handoff contract reference
P4-M4.13 Entry Gate Design Final Non-Validation Boundary Audit remains the inherited prior final non-validation boundary audit reference
P4-M4.12 Declared Transition Package Assembly Envelope Contract remains the inherited prior declared transition package assembly envelope reference
P4-M4.11 Declared Transition Safeguard Envelope Contract remains the inherited prior declared transition safeguard envelope reference
P4-M4.10 Declared Transition Assumption Envelope Contract remains the inherited prior declared transition assumption envelope reference
P4-M4.9 Declared Transition Risk Envelope Contract remains the inherited prior declared transition risk envelope reference
P4-M4.8 Declared Transition Impact Envelope Contract remains the inherited prior declared transition impact envelope reference
P4-M4.7 Declared Transition Dependency Envelope Contract remains the inherited prior declared transition dependency envelope reference
P4-M4.6 Declared Transition Constraint Envelope Contract remains the inherited prior declared transition constraint envelope reference
P4-M4.5 Declared Transition Reason Envelope Contract remains the inherited prior declared transition reason envelope reference
P4-M4.4 Target Phase Envelope Contract remains the inherited prior target phase envelope reference
P4-M4.3 Declared Human Context Envelope Contract remains the inherited prior declared human context envelope reference
P4-M4.2 Evidence Reference Envelope Contract remains the inherited prior evidence reference envelope reference
P4-M4.1 Entry Gate Design Request Envelope Contract remains the inherited prior request envelope reference
P4-M4.0 Entry Gate Design Boundary Contract remains the inherited prior design boundary reference
P4-M3.16 Governed Transition Intake Final Phase Handoff Summary remains the inherited prior closed-phase handoff context reference
P4-M4 static definition chain remains closed
P4-M4 design layer remains terminally sealed
P4-M4 final closure transition readiness non-start index starts only as a static declared transition readiness discussion index surface
P4-M4 transition readiness references remain static reference-only entries
transition readiness validation remains not implemented
transition readiness scoring remains not implemented
transition readiness verdict remains not implemented
transition readiness execution remains not implemented
transition readiness record creation remains not implemented
transition readiness storage remains not implemented
transition readiness persistence remains not implemented
transition readiness mutation remains not implemented
operator handoff validation remains not implemented
P4-M4 evidence validation remains not implemented
P4-M5 entry validation remains not implemented
P4-M5 readiness validation remains not implemented
P4-M5 readiness inference remains not implemented
P4-M5 readiness scoring remains not implemented
P4-M5 readiness verdict remains not implemented
P4-M5 entry scoring remains not implemented
P4-M5 entry verdict remains not implemented
P4-M5 entry execution remains not implemented
P4-M5 start remains not implemented
P4-M4.18 remains not started
P4-M5 remains not started
v7 remains not started
productization remains not started
UI remains not started
Operator Console remains not started
no P4-M4.18
no P4-M5 implementation
no P4-M5 entry validation
no P4-M5 readiness validation
no P4-M5 readiness inference
no P4-M5 readiness scoring
no P4-M5 readiness verdict
no P4-M5 entry scoring
no P4-M5 entry verdict
no P4-M5 entry execution
no P4-M5 start
no transition readiness validation
no transition readiness scoring
no transition readiness verdict
no transition readiness execution
no transition readiness record creation
no transition readiness storage
no transition readiness persistence
no transition readiness mutation
no operator handoff validation
no evidence validation
no evidence scoring
no evidence verdict
no evidence execution
no validation
no scoring
no verdict
no approval
no authorization
no confirmation
no recommendation
no ranking
no routing
no executable planning
no execution
no record creation
no storage
no persistence
no mutation
no v7
no productization
no UI
no Operator Console
no version bump
no tag
""".splitlines()
    if line
)


TRUE_STATUS_FLAGS = tuple(
    line
    for line in """
definition_only
p4_m4_final_closure_transition_readiness_non_start_index_only
transition_readiness_non_start_index_only
transition_readiness_non_validation_boundary_only
transition_readiness_non_scoring_boundary_only
transition_readiness_non_verdict_boundary_only
transition_readiness_non_execution_boundary_only
transition_readiness_non_record_boundary_only
transition_readiness_non_mutation_boundary_only
p4_m5_non_start_boundary_only
declaration_only
inspection_only
p4_m4_fc_3_started
p4_m4_fc_3_definition_only
p4_m4_fc_3_final_closure_transition_readiness_non_start_index_only
p4_m4_fc_3_transition_readiness_non_start_index_only
p4_m4_fc_3_p4_m5_non_start_boundary_only
p4_m4_fc_2_final_closure_operator_handoff_index_reference_defined
p4_m4_fc_2_static_reference_defined
p4_m4_fc_1_final_closure_evidence_index_reference_defined
p4_m4_fc_0_final_closure_index_entry_planning_gate_reference_defined
p4_m4_17_terminal_closure_seal_reference_defined
p4_m4_16_final_phase_handoff_summary_reference_defined
p4_m4_15_phase_closure_review_reference_defined
p4_m4_14_closure_handoff_contract_reference_defined
p4_m4_13_final_non_validation_boundary_audit_reference_defined
p4_m4_12_declared_transition_package_assembly_envelope_contract_reference_defined
p4_m4_11_declared_transition_safeguard_envelope_contract_reference_defined
p4_m4_10_declared_transition_assumption_envelope_contract_reference_defined
p4_m4_9_declared_transition_risk_envelope_contract_reference_defined
p4_m4_8_declared_transition_impact_envelope_contract_reference_defined
p4_m4_7_declared_transition_dependency_envelope_contract_reference_defined
p4_m4_6_declared_transition_constraint_envelope_contract_reference_defined
p4_m4_5_declared_transition_reason_envelope_contract_reference_defined
p4_m4_4_target_phase_envelope_contract_reference_defined
p4_m4_3_declared_human_context_envelope_contract_reference_defined
p4_m4_2_evidence_reference_envelope_contract_reference_defined
p4_m4_1_entry_gate_design_request_envelope_contract_reference_defined
p4_m4_0_entry_gate_design_boundary_contract_reference_defined
p4_m3_16_final_phase_handoff_summary_reference_defined
p4_m4_static_definition_chain_closed_reference_defined
p4_m4_design_layer_terminally_sealed_reference_defined
p4_m4_final_closure_transition_readiness_non_start_index_surface_defined
p4_m4_static_transition_readiness_references_defined
p4_m5_readiness_discussion_deferred
p4_m5_start_deferred
v7_start_deferred
productization_deferred
ui_deferred
operator_console_deferred
""".splitlines()
    if line
)


FALSE_STATUS_FLAGS = tuple(
    line
    for line in """
live_validation_enabled
p4_m4_18_started
p4_m5_started
p4_m5_implementation_started
p4_m5_entry_validation_enabled
p4_m5_readiness_validation_enabled
p4_m5_readiness_inference_enabled
p4_m5_readiness_scoring_enabled
p4_m5_readiness_verdict_enabled
p4_m5_entry_scoring_enabled
p4_m5_entry_verdict_enabled
p4_m5_entry_execution_enabled
p4_m5_start_enabled
transition_readiness_validation_enabled
transition_readiness_scoring_enabled
transition_readiness_verdict_enabled
transition_readiness_execution_enabled
transition_readiness_record_creation_enabled
transition_readiness_storage_enabled
transition_readiness_persistence_enabled
transition_readiness_mutation_enabled
final_closure_transition_readiness_non_start_index_validation_enabled
final_closure_transition_readiness_non_start_index_scoring_enabled
final_closure_transition_readiness_non_start_index_verdict_enabled
final_closure_transition_readiness_non_start_index_execution_enabled
operator_handoff_validation_enabled
operator_handoff_scoring_enabled
operator_handoff_verdict_enabled
operator_handoff_execution_enabled
final_closure_operator_handoff_index_validation_enabled
final_closure_operator_handoff_index_scoring_enabled
final_closure_operator_handoff_index_verdict_enabled
final_closure_operator_handoff_index_execution_enabled
evidence_validation_enabled
evidence_scoring_enabled
evidence_verdict_enabled
evidence_execution_enabled
final_closure_evidence_index_validation_enabled
final_closure_evidence_index_scoring_enabled
final_closure_evidence_index_verdict_enabled
final_closure_evidence_index_execution_enabled
final_closure_index_validation_enabled
final_closure_index_scoring_enabled
final_closure_index_verdict_enabled
final_closure_index_execution_enabled
entry_planning_gate_validation_enabled
entry_planning_gate_scoring_enabled
entry_planning_gate_verdict_enabled
entry_planning_gate_execution_enabled
p4_m4_closure_validation_enabled
p4_m4_closure_scoring_enabled
p4_m4_closure_verdict_enabled
p4_m4_closure_execution_enabled
terminal_closure_validation_enabled
terminal_closure_scoring_enabled
terminal_closure_verdict_enabled
terminal_closure_execution_enabled
final_phase_handoff_validation_enabled
final_phase_handoff_scoring_enabled
final_phase_handoff_verdict_enabled
final_phase_handoff_execution_enabled
phase_closure_validation_enabled
phase_closure_scoring_enabled
phase_closure_verdict_enabled
phase_closure_execution_enabled
closure_handoff_validation_enabled
closure_handoff_execution_enabled
final_audit_execution_enabled
live_audit_evaluation_enabled
entry_gate_validation_enabled
readiness_validation_enabled
transition_validation_enabled
package_validation_enabled
package_assembly_validation_enabled
gate_activation_enabled
verdict_generation_enabled
approval_enabled
authorization_enabled
confirmation_enabled
recommendation_enabled
ranking_enabled
routing_enabled
planning_enabled
executable_planning_enabled
next_action_generation_enabled
execution_enabled
command_execution_enabled
record_creation_enabled
storage_enabled
persistence_enabled
memory_mutation_enabled
api_enabled
mcp_enabled
connector_enabled
agent_call_enabled
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


P4_M4_FINAL_CLOSURE_TRANSITION_READINESS_NON_START_INDEX_BOUNDARY = (
    "P4-M4-FC.3 P4-M4 Final Closure Transition Readiness Non-Start "
    "Index read-only definition-only "
    "p4-m4-final-closure-transition-readiness-non-start-index-only "
    "transition-readiness-non-start-index-only "
    "transition-readiness-non-validation-boundary-only "
    "transition-readiness-non-scoring-boundary-only "
    "transition-readiness-non-verdict-boundary-only "
    "transition-readiness-non-execution-boundary-only "
    "transition-readiness-non-record-boundary-only "
    "transition-readiness-non-mutation-boundary-only "
    "p4-m5-non-start-boundary-only declaration-only inspection-only. "
    "P4-M4-FC.3 is not P4-M4.18. P4-M4-FC.3 is not P4-M5. "
    "P4-M4-FC.3 P4-M4 Final Closure Transition Readiness Non-Start "
    "Index is definition only. "
    + " ".join(f"{phrase}." for phrase in BOUNDARY_PHRASE_LINES)
)


_FIELD_IDS = (
    "p4-m4-final-closure-transition-readiness-non-start-index-id",
    "p4-m4-final-closure-transition-readiness-non-start-index-phase",
    "p4-m4-final-closure-transition-readiness-non-start-index-mode",
    "p4-m4-final-closure-transition-readiness-non-start-index-direct-prior-final-closure-operator-handoff-index-reference",
    "p4-m4-final-closure-transition-readiness-non-start-index-inherited-prior-final-closure-evidence-index-reference",
    "p4-m4-final-closure-transition-readiness-non-start-index-inherited-prior-final-closure-index-entry-planning-gate-reference",
    "p4-m4-final-closure-transition-readiness-non-start-index-inherited-prior-terminal-closure-seal-reference",
    "p4-m4-final-closure-transition-readiness-non-start-index-inherited-prior-final-phase-handoff-summary-reference",
    "p4-m4-final-closure-transition-readiness-non-start-index-inherited-prior-phase-closure-review-reference",
    "p4-m4-final-closure-transition-readiness-non-start-index-inherited-prior-closure-handoff-contract-reference",
    "p4-m4-final-closure-transition-readiness-non-start-index-inherited-prior-final-non-validation-boundary-audit-reference",
    "p4-m4-final-closure-transition-readiness-non-start-index-inherited-prior-declared-transition-package-assembly-envelope-reference",
    "p4-m4-final-closure-transition-readiness-non-start-index-inherited-prior-declared-transition-safeguard-envelope-reference",
    "p4-m4-final-closure-transition-readiness-non-start-index-inherited-prior-declared-transition-assumption-envelope-reference",
    "p4-m4-final-closure-transition-readiness-non-start-index-inherited-prior-declared-transition-risk-envelope-reference",
    "p4-m4-final-closure-transition-readiness-non-start-index-inherited-prior-declared-transition-impact-envelope-reference",
    "p4-m4-final-closure-transition-readiness-non-start-index-inherited-prior-declared-transition-dependency-envelope-reference",
    "p4-m4-final-closure-transition-readiness-non-start-index-inherited-prior-declared-transition-constraint-envelope-reference",
    "p4-m4-final-closure-transition-readiness-non-start-index-inherited-prior-declared-transition-reason-envelope-reference",
    "p4-m4-final-closure-transition-readiness-non-start-index-inherited-prior-target-phase-envelope-reference",
    "p4-m4-final-closure-transition-readiness-non-start-index-inherited-prior-declared-human-context-envelope-reference",
    "p4-m4-final-closure-transition-readiness-non-start-index-inherited-prior-evidence-request-and-boundary-reference",
    "p4-m4-final-closure-transition-readiness-non-start-index-static-readiness-discussion-and-validation-scoring-verdict-execution-record-mutation-semantics-disabled",
)


def _field_purpose(field_id: str) -> str:
    return (
        f"Defines {field_id} as read-only definition-only "
        "p4-m4-final-closure-transition-readiness-non-start-index-only "
        "transition-readiness-non-start-index-only "
        "transition-readiness-non-validation-boundary-only "
        "transition-readiness-non-scoring-boundary-only "
        "transition-readiness-non-verdict-boundary-only "
        "transition-readiness-non-execution-boundary-only "
        "transition-readiness-non-record-boundary-only "
        "transition-readiness-non-mutation-boundary-only "
        "p4-m5-non-start-boundary-only declaration-only inspection-only "
        "P4-M4-FC.3 P4-M4 Final Closure Transition Readiness Non-Start "
        "Index context; P4-M4-FC.2 P4-M4 Final Closure Operator Handoff "
        "Index remains the direct prior final closure operator handoff index "
        "reference; P4-M4-FC.1 P4-M4 Final Closure Evidence Index remains "
        "the inherited prior final closure evidence index reference; "
        "P4-M4-FC.0 P4-M4 Final Closure Index / P4-M5 Entry Planning Gate "
        "remains the inherited prior final closure index and entry planning "
        "gate reference; P4-M4.17 Entry Gate Design Phase Terminal Closure "
        "Seal remains the inherited prior terminal closure seal reference; "
        "P4-M4 static definition chain remains closed; P4-M4 design layer "
        "remains terminally sealed; transition readiness validation remains "
        "not implemented; transition readiness scoring remains not "
        "implemented; transition readiness verdict remains not implemented; "
        "transition readiness execution remains not implemented; transition "
        "readiness record creation remains not implemented; transition "
        "readiness storage remains not implemented; transition readiness "
        "persistence remains not implemented; transition readiness mutation "
        "remains not implemented; P4-M5 readiness inference remains not "
        "implemented; no P4-M4.18; no P4-M5 implementation; no P4-M5 entry "
        "validation; no P4-M5 readiness validation; no P4-M5 readiness "
        "inference; no P4-M5 readiness scoring; no P4-M5 readiness verdict; "
        "no P4-M5 entry scoring; no P4-M5 entry verdict; no P4-M5 entry "
        "execution; no P4-M5 start; no transition readiness validation; no "
        "transition readiness scoring; no transition readiness verdict; no "
        "transition readiness execution; no transition readiness record "
        "creation; no transition readiness storage; no transition readiness "
        "persistence; no transition readiness mutation; no operator handoff "
        "validation; no evidence validation; no evidence scoring; no "
        "evidence verdict; no evidence execution; no validation; no scoring; "
        "no verdict; no approval; no authorization; no confirmation; no "
        "recommendation; no ranking; no routing; no executable planning; no "
        "execution; no record creation; no storage; no persistence; no "
        "mutation; no v7; no productization; no UI; no Operator Console; no "
        "version bump; no tag."
    )


_P4_M4_FINAL_CLOSURE_TRANSITION_READINESS_NON_START_INDEX_FIELDS = tuple(
    P4M4FinalClosureTransitionReadinessNonStartIndexField(
        index,
        field_id,
        (
            "P4-M4 Final Closure Transition Readiness Non-Start Index "
            f"Field {index}"
        ),
        _field_purpose(field_id),
        "p4-m4-final-closure-transition-readiness-non-start-index-category",
        (
            "no transition readiness validation semantics; no transition "
            "readiness scoring semantics; no transition readiness verdict "
            "semantics; no transition readiness execution semantics; no "
            "transition readiness record creation semantics; no transition "
            "readiness storage semantics; no transition readiness persistence "
            "semantics; no transition readiness mutation semantics; no "
            "operator handoff validation semantics; no operator handoff "
            "scoring semantics; no operator handoff verdict semantics; no "
            "operator handoff execution semantics; no evidence validation "
            "semantics; no evidence scoring semantics; no evidence verdict "
            "semantics; no evidence execution semantics; no validation "
            "semantics; no scoring semantics; no verdict semantics; no "
            "approval semantics; no authorization semantics; no confirmation "
            "semantics; no recommendation semantics; no ranking semantics; "
            "no routing semantics; no executable planning semantics; no "
            "execution semantics; no record creation semantics; no storage "
            "semantics; no persistence semantics; no mutation semantics; no "
            "P4-M4.18 semantics; no P4-M5 readiness inference semantics; no "
            "P4-M5 start semantics; no v7 semantics; no productization "
            "semantics; no UI semantics; no Operator Console semantics"
        ),
    )
    for index, field_id in enumerate(_FIELD_IDS, start=1)
)


def list_p4_m4_final_closure_transition_readiness_non_start_index_fields() -> (
    tuple[P4M4FinalClosureTransitionReadinessNonStartIndexField, ...]
):
    return _P4_M4_FINAL_CLOSURE_TRANSITION_READINESS_NON_START_INDEX_FIELDS


def p4_m4_final_closure_transition_readiness_non_start_index_field_ids() -> (
    tuple[str, ...]
):
    return tuple(
        field.field_id
        for field in (
            list_p4_m4_final_closure_transition_readiness_non_start_index_fields()
        )
    )


def render_p4_m4_final_closure_transition_readiness_non_start_index_markdown(
    fields: (
        Sequence[P4M4FinalClosureTransitionReadinessNonStartIndexField] | None
    ) = None,
) -> str:
    field_values = (
        tuple(fields)
        if fields is not None
        else list_p4_m4_final_closure_transition_readiness_non_start_index_fields()
    )
    status = p4_m4_final_closure_transition_readiness_non_start_index_report()
    lines = [
        "# P4-M4-FC.3 P4-M4 Final Closure Transition Readiness Non-Start Index",
        "",
        "P4-M4-FC.3 P4-M4 Final Closure Transition Readiness Non-Start Index.",
        "",
    ]
    for phrase in BOUNDARY_PHRASE_LINES:
        lines.extend([f"{phrase}.", ""])
    for prior_layer in DIRECT_PRIOR_DEFINITION_LAYER_REFERENCES:
        lines.extend([f"{prior_layer} remains a referenced definition layer.", ""])
    for prior_layer in INHERITED_PRIOR_DEFINITION_LAYER_REFERENCES:
        lines.extend(
            [f"{prior_layer} remains an inherited referenced definition layer.", ""]
        )
    lines.extend(
        [
            P4_M4_FINAL_CLOSURE_TRANSITION_READINESS_NON_START_INDEX_BOUNDARY,
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
            "## P4-M4 Final Closure Transition Readiness Non-Start Index Fields",
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
                "- P4-M4 final closure transition readiness non-start index "
                "category: "
                f"{field.p4_m4_final_closure_transition_readiness_non_start_index_category}",
                "- P4-M4 final closure transition readiness non-start index "
                "semantics disabled: "
                f"{field.p4_m4_final_closure_transition_readiness_non_start_index_semantics_disabled}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def p4_m4_final_closure_transition_readiness_non_start_index_as_dicts() -> (
    tuple[dict[str, object], ...]
):
    return tuple(
        asdict(field)
        for field in (
            list_p4_m4_final_closure_transition_readiness_non_start_index_fields()
        )
    )


def p4_m4_final_closure_transition_readiness_non_start_index_report() -> (
    dict[str, object]
):
    status: dict[str, object] = {
        "phase": "P4-M4-FC.3",
        "feature": "P4-M4 Final Closure Transition Readiness Non-Start Index",
        "mode": "read-only",
        "boundary": (
            P4_M4_FINAL_CLOSURE_TRANSITION_READINESS_NON_START_INDEX_BOUNDARY
        ),
        "package_version": P4_M4_FC_3_PACKAGE_VERSION,
        "p4_m4_final_closure_transition_readiness_non_start_index_field_count": len(
            _FIELD_IDS
        ),
        "referenced_p4_m4_fc_2_final_closure_operator_handoff_index_field_count": len(
            p4_m4_final_closure_operator_handoff_index_field_ids()
        ),
    }
    status.update({flag: True for flag in TRUE_STATUS_FLAGS})
    status.update({flag: False for flag in FALSE_STATUS_FLAGS})
    return status
