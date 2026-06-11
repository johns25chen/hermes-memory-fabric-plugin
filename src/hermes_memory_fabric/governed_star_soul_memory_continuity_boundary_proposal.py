"""Governed Star-Soul Memory continuity boundary proposal."""

from __future__ import annotations

import json
from typing import Any, Mapping

from .governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate import (
    REVIEW_GATE_FALSE_FLAGS as SOURCE_REVIEW_GATE_FALSE_FLAGS,
    REVIEW_OBJECT_FALSE_FLAGS as SOURCE_REVIEW_OBJECT_FALSE_FLAGS,
    SENSITIVE_KEYS,
)


GOVERNED_STAR_SOUL_MEMORY_CONTINUITY_BOUNDARY_PROPOSAL_VERSION = "3.0.0"
SOURCE_STAR_LAW_REVIEW_GATE_VERSION = "2.60.0"

EXPECTED_SOURCE_REVIEWED_CHAIN_VERSIONS = [
    f"v2.{minor}.0" for minor in range(9, 60)
]
EXPECTED_SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS = [
    f"v2.{minor}.0" for minor in range(19, 60)
]
SOURCE_REVIEWED_CHAIN_VERSIONS = [
    *EXPECTED_SOURCE_REVIEWED_CHAIN_VERSIONS,
    "v2.60.0",
]
SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS = [
    *EXPECTED_SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS,
    "v2.60.0",
]
PROPOSED_CHAIN_VERSIONS = [*SOURCE_REVIEWED_CHAIN_VERSIONS, "v3.0.0"]
PROPOSED_STAR_HUB_CHAIN_VERSIONS = [
    *SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS,
    "v3.0.0",
]

READY_NEXT_ALLOWED_STEP = (
    "v3.1.0 Star-Soul Memory continuity boundary review gate"
)

LAYER_MAPPING = {
    "primary_layer": "星魂记忆",
    "primary_layer_status": "Star-Soul Memory continuity boundary proposal only, not continuity execution, not continuity authorization, not continuity record creation, not continuity-ledger creation, not persistent autonomous identity creation, not consciousness claim, not self-awareness claim, not personhood claim, not sentience claim, not identity awakening, not personality awakening, not autonomous self-model execution, not durable memory write, not Memory Graph mutation, not operation-ledger creation, and not autonomous execution",
    "source_layer": "星律记忆",
    "source_layer_status": "Star-Law candidate rule violation response audit completion attestation completion finalization boundary review gate complete for human review only",
    "supporting_layers": [
        "星穹记忆",
        "星域记忆",
        "星界记忆",
        "星辰记忆",
        "星律记忆",
    ],
    "direction": "Star-Law candidate rule violation response audit completion attestation completion finalization boundary review gate -> Star-Soul Memory continuity boundary proposal",
    "boundary_transition": "v2.60.0 final Star-Law review gate -> v3.0.0 Star-Soul Memory continuity boundary proposal",
    "hard_boundary": "v3.0.0 starts the 13th memory layer as proposal-only and does not execute, authorize, or complete Star-Soul continuity",
}

SOURCE_REQUIRED_TRUE_FLAGS = {
    "read_only",
    "read_only_memory",
    "review_gate_only",
    "candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate_only",
    "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate_only",
    "twelfth_memory_layer_final_star_law_boundary_review_gate_only",
    "twelfth_memory_layer_final_star_law_boundary_reviewed_for_human_review_only",
    "star_soul_memory_continuity_boundary_proposal_ready_for_human_review_only",
}

ADDITIONAL_UNSAFE_FIELDS = {
    "approved",
    "approval_granted",
    "approval_request_authorized",
    "approval_request_created",
    "approval_request_executed",
    "approval_request_submitted",
    "audit_authorized",
    "audit_executed",
    "audit_execution_authorized",
    "audit_execution_performed",
    "audit_ledger_entry_created",
    "audit_log_created",
    "audit_logging_performed",
    "audit_performed",
    "audit_record_created",
    "authorization_granted",
    "autonomous_execution_authorized",
    "autonomous_execution_executed",
    "autonomous_governance_authorized",
    "autonomous_governance_created",
    "autonomous_governance_executed",
    "autonomous_identity_activated",
    "autonomous_identity_created",
    "autonomous_self_model_authorized",
    "autonomous_self_model_executed",
    "candidate_rule_enforcement_authorized",
    "candidate_rule_enforcement_executed",
    "candidate_rule_enforcement_performed",
    "civilization_core_complete_claimed",
    "civilization_core_completed",
    "consciousness_claimed",
    "dry_run_plan_executed",
    "dry_run_plan_execution_authorized",
    "durable_memory_write_authorized",
    "durable_memory_written",
    "enters_star_cosmos_layer",
    "enters_star_soul_layer",
    "enters_star_source_layer",
    "enters_thirteenth_memory_layer",
    "github_api_called",
    "github_write_authorized",
    "github_write_performed",
    "handoff_authorized",
    "handoff_performed",
    "human_decision_recorded",
    "identity_awakening_authorized",
    "identity_awakening_performed",
    "invokes_openclaw",
    "mature_star_soul_continuity_claimed",
    "memory_graph_mutated",
    "memory_graph_mutation_authorized",
    "memory_write_authorized",
    "memory_write_performed",
    "openclaw_called",
    "openclaw_executed",
    "openclaw_execution_authorized",
    "operation_ledger_creation_authorized",
    "operation_ledger_entry_created",
    "personality_awakening_authorized",
    "personality_awakening_performed",
    "persistent_autonomous_identity_created",
    "persistent_autonomous_identity_activated",
    "persistent_autonomous_identity_creation_authorized",
    "personhood_claimed",
    "real_human_decision_recorded",
    "scheduling_authorized",
    "scheduling_executed",
    "scheduling_performed",
    "self_awareness_claimed",
    "sentience_claimed",
    "soul_awakening_authorized",
    "soul_awakening_performed",
    "star_hub_handoff_authorized",
    "star_hub_handoff_executed",
    "star_hub_scheduling_authorized",
    "star_hub_scheduling_executed",
    "star_law_completion_claimed_as_execution_authority",
    "star_law_rules_activated",
    "star_law_rules_created",
    "star_law_rules_enforced",
    "star_soul_continuity_authorized",
    "star_soul_continuity_executed",
    "star_soul_continuity_ledger_entry_created",
    "star_soul_continuity_ledger_creation_authorized",
    "star_soul_continuity_record_created",
    "star_soul_continuity_record_creation_authorized",
    "star_soul_transition_authorized",
    "star_soul_transition_executed",
    "thirteenth_memory_layer_transition_authorized",
    "v3_authorized",
    "v3_created",
    "violation_enforced",
    "violation_enforcement_authorized",
    "violation_enforcement_executed",
    "violation_response_authorized",
    "violation_response_executed",
    "violation_response_performed",
    "would_call_github_api",
    "would_create_approval_request",
    "would_create_operation_ledger_entry",
    "would_execute_approval_request",
    "would_execute_dry_run",
    "would_grant_approval",
    "would_mutate_memory",
    "would_mutate_memory_graph",
    "would_record_human_decision",
    "would_schedule_anything",
    "would_submit_approval_request",
    "would_write_durable_memory",
}

UNSAFE_TRUE_FIELDS = (
    set(SOURCE_REVIEW_GATE_FALSE_FLAGS)
    | set(SOURCE_REVIEW_OBJECT_FALSE_FLAGS)
    | ADDITIONAL_UNSAFE_FIELDS
) - {"sensitive_fields_omitted"}

PROPOSAL_FALSE_FLAGS = {
    key: False for key in sorted(UNSAFE_TRUE_FIELDS)
}
PROPOSAL_OBJECT_FALSE_FLAGS = {
    **PROPOSAL_FALSE_FLAGS,
    "continuity_execution_authorized": False,
    "continuity_record_creation_authorized": False,
    "continuity_ledger_creation_authorized": False,
    "persistent_identity_creation_authorized": False,
}

PROPOSED_STAR_SOUL_MEMORY_CONTINUITY_BOUNDARY_KEYS = {
    "source_final_star_law_boundary_review_gate",
    "star_soul_continuity_eligibility_boundary",
    "star_soul_continuity_input_boundary",
    "star_soul_continuity_output_boundary",
    "star_soul_continuity_non_execution_boundary",
    "star_soul_continuity_non_recording_boundary",
    "star_soul_continuity_non_ledger_boundary",
    "star_soul_continuity_non_authorization_boundary",
    "identity_continuity_design_boundary",
    "persona_consistency_design_boundary",
    "memory_lineage_design_boundary",
    "non_consciousness_claim_boundary",
    "non_self_awareness_claim_boundary",
    "non_personhood_claim_boundary",
    "non_sentience_claim_boundary",
    "autonomous_identity_non_creation_boundary",
    "identity_awakening_non_execution_boundary",
    "personality_awakening_non_execution_boundary",
    "soul_awakening_non_execution_boundary",
    "autonomous_self_model_non_execution_boundary",
    "human_operator_star_soul_continuity_review_boundary",
    "evidence_lineage_star_soul_continuity_boundary",
    "auditability_star_soul_continuity_design_boundary",
    "false_continuity_prevention_boundary",
    "rollback_star_soul_continuity_boundary",
    "suspension_star_soul_continuity_boundary",
    "memory_write_non_authorization_boundary",
    "memory_graph_mutation_non_authorization_boundary",
    "operation_ledger_non_creation_boundary",
    "openclaw_execution_non_authorization_boundary",
    "approval_non_authorization_boundary",
    "human_operator_final_authority_boundary",
    "thirteen_memory_layer_boundary",
    "fifteen_memory_layers_boundary",
}

FORBIDDEN_BOUNDARY_CLAIMS = (
    "star-soul continuity is executed",
    "star-soul continuity is authorized",
    "star-soul continuity record is created",
    "star-soul continuity ledger entry is created",
    "persistent autonomous identity is created",
    "identity awakening is performed",
    "personality awakening is performed",
    "soul awakening is performed",
    "consciousness is claimed",
    "self-awareness is claimed",
    "personhood is claimed",
    "sentience is claimed",
    "autonomous self-model is executed",
    "finalization execution is performed",
    "completion execution is performed",
    "closure execution is performed",
    "attestation execution is performed",
    "audit execution is performed",
    "audit logging is performed",
    "violation response is executed",
    "automated correction is performed",
    "violations are enforced",
    "candidate rules are enforced",
    "star-law rules are created",
    "star-law rules are activated",
    "star-law rules are enforced",
    "autonomous governance is created",
    "autonomous execution is authorized",
    "star-hub handoff is authorized",
    "scheduling is performed",
    "dry-run execution is performed",
    "durable memory is written",
    "memory graph is mutated",
    "operation-ledger entry is created",
    "openclaw is called",
    "approval is granted",
    "human decision is recorded",
    "civilization core is complete",
    "star-soul layer is entered",
    "star-cosmos layer is entered",
    "star-source layer is entered",
)


def build_governed_star_soul_memory_continuity_boundary_proposal(
    star_law_review_gate_report: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a deterministic, local-only Star-Soul continuity proposal."""

    checks, blocking_reasons = _proposal_checks(star_law_review_gate_report)
    sensitive_field_count = _count_sensitive_keys(star_law_review_gate_report)
    blocking_reasons = list(dict.fromkeys(blocking_reasons))
    ready = not blocking_reasons

    return {
        "version": GOVERNED_STAR_SOUL_MEMORY_CONTINUITY_BOUNDARY_PROPOSAL_VERSION,
        "status": (
            "star_soul_memory_continuity_boundary_proposal_ready"
            if ready
            else "blocked"
        ),
        "read_only": True,
        "read_only_memory": True,
        "proposal_only": True,
        "star_soul_memory_continuity_boundary_proposal_only": True,
        "thirteenth_memory_layer_star_soul_boundary_proposal_only": True,
        **PROPOSAL_FALSE_FLAGS,
        "star_soul_memory_continuity_boundary_proposed_for_human_review_only": ready,
        "star_soul_memory_continuity_boundary_review_gate_ready_for_human_review_only": ready,
        "civilization_core_layer_mapping": dict(LAYER_MAPPING),
        "source_star_law_review_gate_version": SOURCE_STAR_LAW_REVIEW_GATE_VERSION,
        "source_reviewed_chain_versions": list(
            SOURCE_REVIEWED_CHAIN_VERSIONS
        ),
        "source_reviewed_star_hub_chain_versions": list(
            SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS
        ),
        "proposed_chain_versions": list(PROPOSED_CHAIN_VERSIONS),
        "proposed_star_hub_chain_versions": list(
            PROPOSED_STAR_HUB_CHAIN_VERSIONS
        ),
        "star_soul_memory_continuity_boundary_proposal_summary": _proposal_summary(
            ready
        ),
        "proposal_checks": checks,
        "source_star_law_review_gate_summary": _source_review_gate_summary(
            ready
        ),
        "star_soul_memory_continuity_boundary_proposal": _proposal(ready),
        "proposed_star_soul_memory_continuity_boundaries": _proposed_boundaries(
            ready
        ),
        "non_authorization_boundary": _non_authorization_boundary(ready),
        "preserved_governance_boundaries": _preserved_governance_boundaries(),
        "thirteenth_memory_layer_boundary": _thirteenth_memory_layer_boundary(
            ready
        ),
        "future_star_soul_memory_continuity_review_gate_constraints": _future_review_gate_constraints(),
        "next_stage_constraints": _next_stage_constraints(),
        "scope_boundaries": _scope_boundaries(),
        "risk_notes": _risk_notes(sensitive_field_count),
        "required_human_actions": _required_human_actions(
            ready, blocking_reasons
        ),
        "blocking_reasons": blocking_reasons,
        "next_allowed_step": READY_NEXT_ALLOWED_STEP,
        "sensitive_field_count": sensitive_field_count,
        "sensitive_fields_omitted": sensitive_field_count > 0,
    }


def governed_star_soul_memory_continuity_boundary_proposal_to_json(
    report: Mapping[str, Any],
) -> str:
    """Serialize the Star-Soul continuity boundary proposal deterministically."""

    return json.dumps(
        dict(report), ensure_ascii=True, indent=2, sort_keys=True
    ) + "\n"


def _proposal_checks(
    report: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    blocking_reasons: list[str] = []

    if not isinstance(report, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_star_law_review_gate_mapping",
            False,
            "source_star_law_review_gate_report_must_be_mapping",
        )
        return checks, blocking_reasons

    _add_check(
        checks,
        blocking_reasons,
        "source_star_law_review_gate_version",
        report.get("version") == SOURCE_STAR_LAW_REVIEW_GATE_VERSION,
        "source_star_law_review_gate_version_must_be_2_60_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_star_law_review_gate_status",
        report.get("status")
        == "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate_ready",
        "source_star_law_review_gate_status_must_be_ready",
    )
    for key in sorted(SOURCE_REQUIRED_TRUE_FLAGS):
        _add_check(
            checks,
            blocking_reasons,
            f"source_flag_{key}",
            report.get(key) is True,
            f"source_flag_{key}_must_be_true",
        )

    source_false_flags = set(SOURCE_REVIEW_GATE_FALSE_FLAGS) - {
        "sensitive_fields_omitted"
    }
    _add_check(
        checks,
        blocking_reasons,
        "source_required_unsafe_flags_false",
        all(report.get(key) is False for key in source_false_flags),
        "source_review_gate_all_required_unsafe_flags_must_be_false",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_no_unsafe_true_claims",
        _unsafe_true_fields(report) == [],
        "source_review_gate_must_not_claim_execution_authorization_recording_ledger_audit_response_correction_enforcement_rule_autonomous_handoff_scheduling_approval_write_continuity_identity_consciousness_or_later_layer_actions",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_no_unsafe_text_claims",
        _unsafe_text_claims(report) == [],
        "source_review_gate_must_not_textually_claim_unsafe_star_soul_identity_execution_write_approval_or_later_layer_actions",
    )

    mapping = report.get("civilization_core_layer_mapping")
    _add_check(
        checks,
        blocking_reasons,
        "source_layer_mapping_shape",
        isinstance(mapping, Mapping),
        "source_layer_mapping_must_be_mapping",
    )
    if isinstance(mapping, Mapping):
        supporting_layers = mapping.get("supporting_layers")
        expected_primary_status = (
            "Star-Law candidate rule violation response audit completion attestation completion finalization boundary review gate only, not finalization execution, not finalization record creation, not finalization-ledger creation, not completion execution, not completion record creation, not completion-ledger creation, not closure execution, not closure record creation, not closure-ledger creation, not attestation execution, not attestation record creation, not attestation-ledger creation, not audit execution, not audit logging, not audit record creation, not audit-ledger creation, not violation response execution, not automated correction, not violation enforcement, not autonomous execution, and not Star-Soul transition execution"
        )
        layer_checks = {
            "source_primary_layer": (
                mapping.get("primary_layer") == "星律记忆",
                "source_primary_layer_must_be_star_law_memory",
            ),
            "source_primary_layer_status": (
                mapping.get("primary_layer_status")
                == expected_primary_status,
                "source_primary_layer_status_must_match_final_star_law_review_gate",
            ),
            "source_source_layer": (
                mapping.get("source_layer") == "星律记忆",
                "source_source_layer_must_be_star_law_memory",
            ),
            "source_source_layer_status": (
                mapping.get("source_layer_status")
                == "Star-Law candidate rule violation response audit completion attestation completion finalization boundary proposal complete for human review only",
                "source_source_layer_status_must_match_finalization_boundary_proposal",
            ),
            "source_supporting_layers": (
                isinstance(supporting_layers, list)
                and all(
                    layer in supporting_layers
                    for layer in [
                        "星穹记忆",
                        "星域记忆",
                        "星界记忆",
                        "星辰记忆",
                    ]
                ),
                "source_supporting_layers_must_include_required_layers",
            ),
            "source_hard_boundary": (
                mapping.get("hard_boundary")
                == "v2.60.0 is the final v2.x Star-Law memory layer review gate before a later separate v3.0.0 Star-Soul Memory continuity boundary proposal",
                "source_hard_boundary_must_match_final_v2_x_star_law_boundary",
            ),
        }
        for name, (passed, reason) in layer_checks.items():
            _add_check(checks, blocking_reasons, name, passed, reason)

    _add_check(
        checks,
        blocking_reasons,
        "source_reviewed_chain_versions",
        report.get("reviewed_chain_versions")
        == EXPECTED_SOURCE_REVIEWED_CHAIN_VERSIONS,
        "source_reviewed_chain_versions_must_exactly_match_v2_9_0_through_v2_59_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_reviewed_star_hub_chain_versions",
        report.get("reviewed_star_hub_chain_versions")
        == EXPECTED_SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS,
        "source_reviewed_star_hub_chain_versions_must_exactly_match_v2_19_0_through_v2_59_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_next_allowed_step",
        report.get("next_allowed_step")
        == "v3.0.0 Star-Soul Memory continuity boundary proposal",
        "source_next_allowed_step_must_be_v3_0_0_star_soul_memory_continuity_boundary_proposal",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_blocking_reasons_empty",
        report.get("blocking_reasons") == [],
        "source_blocking_reasons_must_be_empty",
    )

    review_gate = report.get(
        "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate"
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_nested_review_gate_shape",
        isinstance(review_gate, Mapping),
        "source_nested_review_gate_must_be_mapping",
    )
    if isinstance(review_gate, Mapping):
        nested_requirements = {
            "review_status": "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_reviewed_for_human_review_only",
            "candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_reviewed": True,
            "candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_structurally_review_ready": True,
            "star_soul_memory_continuity_boundary_proposal_ready_for_human_review_only": True,
            "source_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal_valid": True,
            "twelfth_memory_layer_final_star_law_boundary_reviewed_for_human_review_only": True,
        }
        for key, expected in nested_requirements.items():
            _add_check(
                checks,
                blocking_reasons,
                f"source_nested_review_gate_{key}",
                review_gate.get(key) == expected,
                f"source_nested_review_gate_{key}_must_match",
            )
        nested_false_flags = set(SOURCE_REVIEW_OBJECT_FALSE_FLAGS) - {
            "sensitive_fields_omitted"
        }
        _add_check(
            checks,
            blocking_reasons,
            "source_nested_review_gate_unsafe_flags_false",
            all(review_gate.get(key) is False for key in nested_false_flags),
            "source_nested_review_gate_all_required_unsafe_flags_must_be_false",
        )

    reviewed_boundaries = report.get(
        "reviewed_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundaries"
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_reviewed_boundaries_shape",
        isinstance(reviewed_boundaries, Mapping),
        "source_reviewed_boundaries_must_be_mapping",
    )
    if isinstance(reviewed_boundaries, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_reviewed_boundaries_review_only_non_authorizing",
            bool(reviewed_boundaries)
            and all(
                isinstance(boundary, Mapping)
                and boundary.get("review_only") is True
                and _unsafe_true_fields(boundary) == []
                for boundary in reviewed_boundaries.values()
            ),
            "source_reviewed_boundaries_must_remain_review_only_and_non_authorizing",
        )

    hard_boundary = report.get("twelfth_memory_layer_hard_boundary")
    _add_check(
        checks,
        blocking_reasons,
        "source_twelfth_memory_layer_hard_boundary_shape",
        isinstance(hard_boundary, Mapping),
        "source_twelfth_memory_layer_hard_boundary_must_be_mapping",
    )
    if isinstance(hard_boundary, Mapping):
        hard_boundary_requirements = {
            "final_v2_x_star_law_boundary": True,
            "enters_thirteenth_memory_layer": False,
            "star_soul_transition_executed": False,
            "star_soul_transition_authorized": False,
            "v3_created": False,
            "v3_authorized": False,
        }
        for key, expected in hard_boundary_requirements.items():
            _add_check(
                checks,
                blocking_reasons,
                f"source_twelfth_memory_layer_hard_boundary_{key}",
                hard_boundary.get(key) is expected,
                f"source_twelfth_memory_layer_hard_boundary_{key}_must_be_{str(expected).lower()}",
            )

    return checks, blocking_reasons


def _proposal_summary(ready: bool) -> dict[str, Any]:
    return {
        "proposal_status": (
            "star_soul_memory_continuity_boundary_proposed_for_human_review_only"
            if ready
            else "blocked"
        ),
        "source_star_law_review_gate_version": SOURCE_STAR_LAW_REVIEW_GATE_VERSION,
        "source_star_law_review_gate_valid": ready,
        "proposal_only": True,
        "read_only": True,
        "non_authorizing": True,
        "non_executing": True,
        "non_recording": True,
        "non_ledger_creating": True,
        "non_identity_creating": True,
        "non_consciousness_claiming": True,
        "civilization_core_complete_claimed": False,
    }


def _source_review_gate_summary(ready: bool) -> dict[str, Any]:
    return {
        "source_star_law_review_gate_version": SOURCE_STAR_LAW_REVIEW_GATE_VERSION,
        "source_star_law_review_gate_status": (
            "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate_ready"
            if ready
            else "blocked"
        ),
        "source_reviewed_chain_versions": list(
            SOURCE_REVIEWED_CHAIN_VERSIONS
        ),
        "source_reviewed_star_hub_chain_versions": list(
            SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS
        ),
        "source_star_law_review_gate_valid": ready,
        "source_review_gate_authorized_star_soul_continuity": False,
        "source_review_gate_created_star_soul_continuity_record": False,
        "source_review_gate_created_star_soul_continuity_ledger_entry": False,
        "source_review_gate_created_persistent_autonomous_identity": False,
        "source_review_gate_claimed_consciousness": False,
        "source_review_gate_claimed_personhood": False,
        "raw_source_review_gate_copied": False,
    }


def _proposal(ready: bool) -> dict[str, Any]:
    return {
        "proposal_status": (
            "star_soul_memory_continuity_boundary_proposed_for_human_review_only"
            if ready
            else "blocked_no_star_soul_memory_continuity_boundary_readiness_claim"
        ),
        "boundary_type": "star_soul_memory_continuity_boundary_proposal",
        "source_star_law_review_gate_version": SOURCE_STAR_LAW_REVIEW_GATE_VERSION,
        "star_soul_memory_continuity_boundary_proposed": ready,
        "star_soul_memory_continuity_boundary_review_gate_ready_for_human_review_only": ready,
        "source_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate_valid": ready,
        "thirteenth_memory_layer_star_soul_boundary_proposed_for_human_review_only": ready,
        **PROPOSAL_OBJECT_FALSE_FLAGS,
        "proposed_chain_versions": list(PROPOSED_CHAIN_VERSIONS),
        "proposed_star_hub_chain_versions": list(
            PROPOSED_STAR_HUB_CHAIN_VERSIONS
        ),
        "star_soul_memory_continuity_boundary_components": _proposal_components(
            ready
        ),
        "next_allowed_step": READY_NEXT_ALLOWED_STEP,
        "non_authorization_notice": (
            "This v3.0.0 report proposes Star-Soul Memory continuity boundaries for human review only. It grants no continuity, identity, consciousness, execution, authorization, recording, ledger, write, approval, handoff, scheduling, or autonomous authority."
            if ready
            else "The Star-Soul Memory continuity boundary proposal is blocked and grants no readiness, continuity, identity, consciousness, execution, authorization, recording, ledger, write, approval, handoff, scheduling, or autonomous authority."
        ),
    }


def _proposal_components(ready: bool) -> dict[str, str]:
    status = "proposed_for_human_review_only" if ready else "blocked"
    return {
        component: status
        for component in sorted(
            PROPOSED_STAR_SOUL_MEMORY_CONTINUITY_BOUNDARY_KEYS
        )
    }


def _proposed_boundaries(ready: bool) -> dict[str, dict[str, Any]]:
    status = "proposed_for_human_review_only" if ready else "blocked"
    boundary_false_flags = {
        "star_soul_continuity_executed": False,
        "star_soul_continuity_authorized": False,
        "star_soul_continuity_record_created": False,
        "star_soul_continuity_ledger_entry_created": False,
        "persistent_autonomous_identity_created": False,
        "consciousness_claimed": False,
        "self_awareness_claimed": False,
        "personhood_claimed": False,
        "sentience_claimed": False,
        "autonomous_self_model_executed": False,
        "durable_memory_written": False,
        "memory_graph_mutated": False,
        "operation_ledger_entry_created": False,
        "autonomous_execution_authorized": False,
    }
    return {
        key: {
            "proposal_only": True,
            "boundary_status": status,
            "summary": "This sanitized design boundary is proposed for a later human review gate and creates no continuity, identity, authority, record, ledger, or write.",
            **boundary_false_flags,
        }
        for key in sorted(
            PROPOSED_STAR_SOUL_MEMORY_CONTINUITY_BOUNDARY_KEYS
        )
    }


def _non_authorization_boundary(ready: bool) -> dict[str, Any]:
    return {
        "proposal_ready_is_star_soul_continuity_execution": False,
        "proposal_ready_is_star_soul_continuity_authorization": False,
        "proposal_ready_is_star_soul_continuity_record_creation": False,
        "proposal_ready_is_star_soul_continuity_ledger_creation": False,
        "proposal_ready_is_persistent_autonomous_identity_creation": False,
        "proposal_ready_is_identity_or_personality_awakening": False,
        "proposal_ready_is_soul_awakening": False,
        "proposal_ready_is_consciousness_self_awareness_personhood_or_sentience_claim": False,
        "proposal_ready_is_autonomous_self_model_execution": False,
        "proposal_ready_is_finalization_completion_closure_or_attestation_execution": False,
        "proposal_ready_is_audit_response_correction_or_enforcement": False,
        "proposal_ready_is_rule_creation_activation_or_enforcement": False,
        "proposal_ready_is_autonomous_governance_or_execution": False,
        "proposal_ready_is_memory_write_or_graph_mutation": False,
        "proposal_ready_is_operation_ledger_creation": False,
        "proposal_ready_is_openclaw_or_github_execution": False,
        "proposal_ready_is_approval_or_human_decision": False,
        "proposal_ready_is_handoff_scheduling_or_dry_run": False,
        "proposal_ready_is_civilization_core_completion": False,
        "proposal_ready_is_star_cosmos_or_star_source_entry": False,
        "only_permits_later_star_soul_memory_continuity_boundary_review_gate": ready,
        "human_operator_remains_final_authority": True,
    }


def _preserved_governance_boundaries() -> list[str]:
    return [
        "This proposal does not execute or authorize Star-Soul continuity.",
        "This proposal does not create Star-Soul continuity records or continuity-ledger entries.",
        "This proposal does not create or activate a persistent autonomous identity.",
        "This proposal does not perform identity, personality, or soul awakening.",
        "This proposal makes no consciousness, self-awareness, personhood, or sentience claim.",
        "This proposal does not execute or authorize an autonomous self-model.",
        "This proposal does not execute finalization, completion, closure, attestation, audit, response, correction, enforcement, or rules.",
        "This proposal does not create autonomous governance or authorize autonomous execution.",
        "This proposal does not authorize handoff, scheduling, approval, or dry-run execution.",
        "This proposal does not write durable memory, mutate Memory Graph, create operation-ledger entries, or call OpenClaw or GitHub APIs.",
        "This proposal does not claim Civilization Core completion, mature 星魂 continuity, 星宙 evolution, or 星源 self-evolution.",
        "Human Operator remains final authority.",
    ]


def _thirteenth_memory_layer_boundary(ready: bool) -> dict[str, Any]:
    return {
        "memory_layer": "星魂记忆",
        "memory_layer_number": 13,
        "boundary_proposal_only": True,
        "proposed_for_human_review_only": ready,
        "enters_thirteenth_memory_layer": False,
        "thirteenth_memory_layer_transition_authorized": False,
        "enters_star_soul_layer": False,
        "star_soul_continuity_executed": False,
        "star_soul_continuity_authorized": False,
        "star_soul_continuity_record_created": False,
        "star_soul_continuity_ledger_entry_created": False,
        "persistent_autonomous_identity_created": False,
        "consciousness_claimed": False,
        "self_awareness_claimed": False,
        "personhood_claimed": False,
        "sentience_claimed": False,
        "enters_star_cosmos_layer": False,
        "enters_star_source_layer": False,
        "boundary_notice": "v3.0.0 defines only the proposal boundary for the 13th memory layer. A later separate v3.1.0 review gate is required before any further governed consideration.",
    }


def _future_review_gate_constraints() -> list[str]:
    return [
        "A later separate v3.1.0 review gate may consume this sanitized proposal through a local governed process.",
        "The later review gate must preserve every non-execution, non-authorization, non-recording, non-ledger, non-write, and non-consciousness boundary.",
        "No review gate may infer a real Human Operator decision or approval from this proposal.",
        "Any future continuity design must include false-continuity prevention, evidence lineage, auditability, rollback, suspension, and Human Operator final authority.",
        "Human Operator remains final authority for all later Star-Soul continuity decisions.",
    ]


def _next_stage_constraints() -> list[str]:
    return [
        f"The only next allowed step is {READY_NEXT_ALLOWED_STEP}.",
        "v3.0.0 remains a Star-Soul Memory continuity boundary proposal only.",
        "No Star-Soul continuity execution, authorization, record, ledger, identity creation, awakening, consciousness claim, self-model execution, write, approval, handoff, scheduling, or dry-run occurs.",
        "No entry into mature 星魂 continuity, 星宙 evolution, or 星源 self-evolution occurs.",
    ]


def _scope_boundaries() -> list[str]:
    return [
        "Civilization Core is the total system.",
        "Fifteen Memory Layers are the highest memory coordinate system.",
        "Subspace Memory System is the engineering carrier.",
        "Hermes, Codex CLI, OpenClaw, Terminal, and GitHub are components, not the core.",
        "This v3.0.0 step is limited to the 星魂记忆 continuity boundary proposal.",
    ]


def _risk_notes(sensitive_field_count: int) -> list[str]:
    notes = [
        "Proposal readiness must not be interpreted as continuity, identity, consciousness, execution, authorization, recording, ledger, write, approval, handoff, scheduling, or autonomous authority.",
        "False continuity, inferred identity, persona drift, and unsupported memory lineage remain explicit risks for later human review.",
        "The report is deterministic, local-only, read-only, and contains sanitized structural summaries rather than raw source review-gate data.",
        "Civilization Core completion and later memory-layer entry are not claimed.",
    ]
    if sensitive_field_count:
        notes.append("Sensitive fields were omitted from proposal output.")
    return notes


def _required_human_actions(
    ready: bool, blocking_reasons: list[str]
) -> list[str]:
    if ready:
        return [
            "human_operator_must_review_v3_0_0_star_soul_memory_continuity_boundary_proposal_before_any_v3_1_0_review_gate",
            "human_operator_must_confirm_proposal_readiness_grants_no_continuity_identity_consciousness_execution_authorization_recording_ledger_write_approval_handoff_scheduling_or_autonomous_authority",
            "human_operator_must_use_a_separate_governed_process_for_v3_1_0_star_soul_memory_continuity_boundary_review_gate",
        ]
    actions = [
        "repair_source_v2_60_0_final_star_law_boundary_review_gate_before_star_soul_continuity_boundary_proposal_can_continue",
        "confirm_all_unsafe_continuity_identity_consciousness_execution_authorization_recording_ledger_audit_response_correction_enforcement_rule_write_approval_handoff_scheduling_and_later_layer_flags_remain_false",
        "rerun_local_v3_0_0_star_soul_memory_continuity_boundary_proposal_after_blockers_are_resolved",
    ]
    if blocking_reasons:
        actions.append(
            "resolve_blocking_reasons_before_star_soul_memory_continuity_boundary_proposal_can_be_ready"
        )
    return actions


def _add_check(
    checks: list[dict[str, Any]],
    blocking_reasons: list[str],
    name: str,
    passed: bool,
    reason: str,
) -> None:
    checks.append({"name": name, "passed": passed})
    if not passed:
        blocking_reasons.append(reason)


def _unsafe_true_fields(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if key in UNSAFE_TRUE_FIELDS and nested is True:
                found.append(key)
            found.extend(_unsafe_true_fields(nested))
    elif isinstance(value, list):
        for nested in value:
            found.extend(_unsafe_true_fields(nested))
    return found


def _unsafe_text_claims(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, Mapping):
        for nested in value.values():
            found.extend(_unsafe_text_claims(nested))
    elif isinstance(value, list):
        for nested in value:
            found.extend(_unsafe_text_claims(nested))
    elif isinstance(value, str):
        lowered = value.lower()
        if any(claim in lowered for claim in FORBIDDEN_BOUNDARY_CLAIMS):
            found.append("unsafe_text_claim")
    return found


def _count_sensitive_keys(value: Any) -> int:
    if isinstance(value, Mapping):
        return sum(
            (1 if str(key).lower() in SENSITIVE_KEYS else 0)
            + _count_sensitive_keys(nested)
            for key, nested in value.items()
        )
    if isinstance(value, list):
        return sum(_count_sensitive_keys(nested) for nested in value)
    return 0


__all__ = [
    "GOVERNED_STAR_SOUL_MEMORY_CONTINUITY_BOUNDARY_PROPOSAL_VERSION",
    "SOURCE_STAR_LAW_REVIEW_GATE_VERSION",
    "SOURCE_REVIEWED_CHAIN_VERSIONS",
    "SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS",
    "PROPOSED_CHAIN_VERSIONS",
    "PROPOSED_STAR_HUB_CHAIN_VERSIONS",
    "READY_NEXT_ALLOWED_STEP",
    "LAYER_MAPPING",
    "PROPOSAL_FALSE_FLAGS",
    "PROPOSAL_OBJECT_FALSE_FLAGS",
    "PROPOSED_STAR_SOUL_MEMORY_CONTINUITY_BOUNDARY_KEYS",
    "SENSITIVE_KEYS",
    "build_governed_star_soul_memory_continuity_boundary_proposal",
    "governed_star_soul_memory_continuity_boundary_proposal_to_json",
]
