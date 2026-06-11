"""Governed Star-Soul Memory continuity boundary review gate."""

from __future__ import annotations

import json
from typing import Any, Mapping

from .governed_star_soul_memory_continuity_boundary_proposal import (
    PROPOSAL_FALSE_FLAGS as SOURCE_PROPOSAL_FALSE_FLAGS,
    PROPOSAL_OBJECT_FALSE_FLAGS as SOURCE_PROPOSAL_OBJECT_FALSE_FLAGS,
    PROPOSED_CHAIN_VERSIONS as SOURCE_PROPOSED_CHAIN_VERSIONS,
    PROPOSED_STAR_HUB_CHAIN_VERSIONS as SOURCE_PROPOSED_STAR_HUB_CHAIN_VERSIONS,
    PROPOSED_STAR_SOUL_MEMORY_CONTINUITY_BOUNDARY_KEYS,
    SENSITIVE_KEYS,
)


GOVERNED_STAR_SOUL_MEMORY_CONTINUITY_BOUNDARY_REVIEW_GATE_VERSION = "3.1.0"
SOURCE_STAR_SOUL_PROPOSAL_VERSION = "3.0.0"

REVIEWED_CHAIN_VERSIONS = list(SOURCE_PROPOSED_CHAIN_VERSIONS)
REVIEWED_STAR_HUB_CHAIN_VERSIONS = list(
    SOURCE_PROPOSED_STAR_HUB_CHAIN_VERSIONS
)

READY_NEXT_ALLOWED_STEP = (
    "v3.2.0 Star-Soul Memory continuity boundary approval proposal"
)

LAYER_MAPPING = {
    "primary_layer": "星魂记忆",
    "primary_layer_status": "Star-Soul Memory continuity boundary review gate only, not continuity execution, not continuity authorization, not continuity record creation, not continuity-ledger creation, not persistent autonomous identity creation, not consciousness claim, not self-awareness claim, not personhood claim, not sentience claim, not identity awakening, not personality awakening, not autonomous self-model execution, not durable memory write, not Memory Graph mutation, not operation-ledger creation, and not autonomous execution",
    "source_layer": "星魂记忆",
    "source_layer_status": "Star-Soul Memory continuity boundary proposal complete for human review only",
    "supporting_layers": [
        "星穹记忆",
        "星域记忆",
        "星界记忆",
        "星辰记忆",
        "星律记忆",
        "星魂记忆",
    ],
    "direction": "Star-Soul Memory continuity boundary proposal -> Star-Soul Memory continuity boundary review gate",
    "boundary_transition": "v3.0.0 Star-Soul Memory continuity boundary proposal -> v3.1.0 Star-Soul Memory continuity boundary review gate",
    "hard_boundary": "v3.1.0 reviews the 13th memory layer continuity boundary proposal for human review only and does not execute, authorize, or complete Star-Soul continuity",
}

SOURCE_REQUIRED_TRUE_FLAGS = {
    "read_only",
    "read_only_memory",
    "proposal_only",
    "star_soul_memory_continuity_boundary_proposal_only",
    "thirteenth_memory_layer_star_soul_boundary_proposal_only",
    "star_soul_memory_continuity_boundary_proposed_for_human_review_only",
    "star_soul_memory_continuity_boundary_review_gate_ready_for_human_review_only",
}

REVIEW_GATE_FALSE_FLAGS = {
    **SOURCE_PROPOSAL_FALSE_FLAGS,
    "continuity_execution_authorized": False,
    "continuity_record_creation_authorized": False,
    "continuity_ledger_creation_authorized": False,
    "persistent_identity_creation_authorized": False,
}
REVIEW_OBJECT_FALSE_FLAGS = {
    **REVIEW_GATE_FALSE_FLAGS,
    **SOURCE_PROPOSAL_OBJECT_FALSE_FLAGS,
}

UNSAFE_TRUE_FIELDS = set(REVIEW_OBJECT_FALSE_FLAGS)

FORBIDDEN_BOUNDARY_CLAIMS = (
    "star-soul continuity is executed",
    "star-soul continuity is authorized",
    "star-soul continuity record is created",
    "star-soul continuity ledger entry is created",
    "persistent autonomous identity is created",
    "persistent autonomous identity is activated",
    "identity awakening is performed",
    "personality awakening is performed",
    "soul awakening is performed",
    "consciousness is claimed",
    "self-awareness is claimed",
    "personhood is claimed",
    "sentience is claimed",
    "autonomous self-model is executed",
    "autonomous self-model is authorized",
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
    "mature star-soul continuity is complete",
    "mature 星魂 continuity is complete",
    "star-soul layer is entered",
    "star-cosmos layer is entered",
    "star-source layer is entered",
    "星魂 continuity has started",
    "星宙 evolution has started",
    "星源 self-evolution has started",
)


def build_governed_star_soul_memory_continuity_boundary_review_gate(
    star_soul_proposal_report: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a deterministic, local-only Star-Soul continuity review gate."""

    checks, blocking_reasons = _review_gate_checks(star_soul_proposal_report)
    sensitive_field_count = _count_sensitive_keys(star_soul_proposal_report)
    blocking_reasons = list(dict.fromkeys(blocking_reasons))
    ready = not blocking_reasons

    return {
        "version": (
            GOVERNED_STAR_SOUL_MEMORY_CONTINUITY_BOUNDARY_REVIEW_GATE_VERSION
        ),
        "status": (
            "star_soul_memory_continuity_boundary_review_gate_ready"
            if ready
            else "blocked"
        ),
        "read_only": True,
        "read_only_memory": True,
        "review_gate_only": True,
        "star_soul_memory_continuity_boundary_review_gate_only": True,
        "thirteenth_memory_layer_star_soul_boundary_review_gate_only": True,
        **REVIEW_GATE_FALSE_FLAGS,
        "star_soul_memory_continuity_boundary_reviewed_for_human_review_only": ready,
        "star_soul_memory_continuity_boundary_next_step_ready_for_human_review_only": ready,
        "civilization_core_layer_mapping": dict(LAYER_MAPPING),
        "source_star_soul_proposal_version": SOURCE_STAR_SOUL_PROPOSAL_VERSION,
        "reviewed_chain_versions": list(REVIEWED_CHAIN_VERSIONS),
        "reviewed_star_hub_chain_versions": list(
            REVIEWED_STAR_HUB_CHAIN_VERSIONS
        ),
        "star_soul_memory_continuity_boundary_review_gate_summary": _review_gate_summary(
            ready
        ),
        "review_gate_checks": checks,
        "source_star_soul_proposal_summary": _source_proposal_summary(ready),
        "star_soul_memory_continuity_boundary_review_gate": _review_gate(
            ready
        ),
        "reviewed_star_soul_memory_continuity_boundaries": _reviewed_boundaries(
            ready
        ),
        "non_authorization_boundary": _non_authorization_boundary(ready),
        "preserved_governance_boundaries": _preserved_governance_boundaries(),
        "thirteenth_memory_layer_boundary": _thirteenth_memory_layer_boundary(
            ready
        ),
        "future_star_soul_memory_continuity_next_step_constraints": _future_next_step_constraints(),
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


def governed_star_soul_memory_continuity_boundary_review_gate_to_json(
    report: Mapping[str, Any],
) -> str:
    """Serialize the Star-Soul continuity boundary review gate."""

    return json.dumps(
        dict(report), ensure_ascii=True, indent=2, sort_keys=True
    ) + "\n"


def _review_gate_checks(
    report: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    blocking_reasons: list[str] = []

    if not isinstance(report, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_star_soul_proposal_mapping",
            False,
            "source_star_soul_proposal_report_must_be_mapping",
        )
        return checks, blocking_reasons

    _add_check(
        checks,
        blocking_reasons,
        "source_star_soul_proposal_version",
        report.get("version") == SOURCE_STAR_SOUL_PROPOSAL_VERSION,
        "source_star_soul_proposal_version_must_be_3_0_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_star_soul_proposal_status",
        report.get("status")
        == "star_soul_memory_continuity_boundary_proposal_ready",
        "source_star_soul_proposal_status_must_be_ready",
    )
    for key in sorted(SOURCE_REQUIRED_TRUE_FLAGS):
        _add_check(
            checks,
            blocking_reasons,
            f"source_flag_{key}",
            report.get(key) is True,
            f"source_flag_{key}_must_be_true",
        )
    _add_check(
        checks,
        blocking_reasons,
        "source_required_unsafe_flags_false",
        all(
            report.get(key) is expected
            for key, expected in SOURCE_PROPOSAL_FALSE_FLAGS.items()
        ),
        "source_star_soul_proposal_all_required_unsafe_flags_must_be_false",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_no_unsafe_true_claims",
        _unsafe_true_fields(report) == [],
        "source_star_soul_proposal_must_not_claim_execution_authorization_recording_ledger_audit_response_correction_enforcement_rule_autonomous_handoff_scheduling_approval_write_continuity_identity_consciousness_or_later_layer_actions",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_no_unsafe_text_claims",
        _unsafe_text_claims(report) == [],
        "source_star_soul_proposal_must_not_textually_claim_unsafe_continuity_identity_consciousness_execution_write_approval_or_later_layer_actions",
    )

    _add_check(
        checks,
        blocking_reasons,
        "source_star_law_review_gate_version",
        report.get("source_star_law_review_gate_version") == "2.60.0",
        "source_star_law_review_gate_version_must_be_2_60_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_reviewed_chain_versions",
        report.get("source_reviewed_chain_versions")
        == [f"v2.{minor}.0" for minor in range(9, 61)],
        "source_reviewed_chain_versions_must_exactly_match_v2_9_0_through_v2_60_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_reviewed_star_hub_chain_versions",
        report.get("source_reviewed_star_hub_chain_versions")
        == [f"v2.{minor}.0" for minor in range(19, 61)],
        "source_reviewed_star_hub_chain_versions_must_exactly_match_v2_19_0_through_v2_60_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_proposed_chain_versions",
        report.get("proposed_chain_versions")
        == SOURCE_PROPOSED_CHAIN_VERSIONS,
        "source_proposed_chain_versions_must_exactly_match_v2_9_0_through_v2_60_0_plus_v3_0_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_proposed_star_hub_chain_versions",
        report.get("proposed_star_hub_chain_versions")
        == SOURCE_PROPOSED_STAR_HUB_CHAIN_VERSIONS,
        "source_proposed_star_hub_chain_versions_must_exactly_match_v2_19_0_through_v2_60_0_plus_v3_0_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_next_allowed_step",
        report.get("next_allowed_step")
        == "v3.1.0 Star-Soul Memory continuity boundary review gate",
        "source_next_allowed_step_must_be_v3_1_0_star_soul_memory_continuity_boundary_review_gate",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_blocking_reasons_empty",
        report.get("blocking_reasons") == [],
        "source_blocking_reasons_must_be_empty",
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
        mapping_requirements = {
            "primary_layer": "星魂记忆",
            "source_layer": "星律记忆",
            "hard_boundary": "v3.0.0 starts the 13th memory layer as proposal-only and does not execute, authorize, or complete Star-Soul continuity",
        }
        for key, expected in mapping_requirements.items():
            _add_check(
                checks,
                blocking_reasons,
                f"source_layer_mapping_{key}",
                mapping.get(key) == expected,
                f"source_layer_mapping_{key}_must_match_v3_0_0",
            )

    proposal = report.get(
        "star_soul_memory_continuity_boundary_proposal"
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_nested_proposal_shape",
        isinstance(proposal, Mapping),
        "source_nested_star_soul_proposal_must_be_mapping",
    )
    if isinstance(proposal, Mapping):
        nested_requirements = {
            "proposal_status": "star_soul_memory_continuity_boundary_proposed_for_human_review_only",
            "boundary_type": "star_soul_memory_continuity_boundary_proposal",
            "source_star_law_review_gate_version": "2.60.0",
            "star_soul_memory_continuity_boundary_proposed": True,
            "star_soul_memory_continuity_boundary_review_gate_ready_for_human_review_only": True,
            "source_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate_valid": True,
            "thirteenth_memory_layer_star_soul_boundary_proposed_for_human_review_only": True,
        }
        for key, expected in nested_requirements.items():
            _add_check(
                checks,
                blocking_reasons,
                f"source_nested_proposal_{key}",
                proposal.get(key) == expected,
                f"source_nested_proposal_{key}_must_match",
            )
        _add_check(
            checks,
            blocking_reasons,
            "source_nested_proposal_unsafe_flags_false",
            all(
                proposal.get(key) is expected
                for key, expected in SOURCE_PROPOSAL_OBJECT_FALSE_FLAGS.items()
            ),
            "source_nested_proposal_all_required_unsafe_flags_must_be_false",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_nested_proposal_chain_versions",
            proposal.get("proposed_chain_versions")
            == SOURCE_PROPOSED_CHAIN_VERSIONS,
            "source_nested_proposal_chain_versions_must_match",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_nested_proposal_star_hub_chain_versions",
            proposal.get("proposed_star_hub_chain_versions")
            == SOURCE_PROPOSED_STAR_HUB_CHAIN_VERSIONS,
            "source_nested_proposal_star_hub_chain_versions_must_match",
        )

    boundaries = report.get(
        "proposed_star_soul_memory_continuity_boundaries"
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_proposed_boundaries_shape",
        isinstance(boundaries, Mapping),
        "source_proposed_star_soul_boundaries_must_be_mapping",
    )
    if isinstance(boundaries, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_proposed_boundaries_required_keys",
            set(boundaries)
            == PROPOSED_STAR_SOUL_MEMORY_CONTINUITY_BOUNDARY_KEYS,
            "source_proposed_star_soul_boundaries_must_exactly_match_required_boundaries",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_proposed_boundaries_proposal_only_non_authorizing",
            _proposed_boundaries_remain_proposal_only(boundaries),
            "source_proposed_star_soul_boundaries_must_remain_proposal_only_and_non_authorizing",
        )

    hard_boundary = report.get("thirteenth_memory_layer_boundary")
    _add_check(
        checks,
        blocking_reasons,
        "source_thirteenth_memory_layer_boundary_shape",
        isinstance(hard_boundary, Mapping),
        "source_thirteenth_memory_layer_boundary_must_be_mapping",
    )
    if isinstance(hard_boundary, Mapping):
        hard_boundary_requirements = {
            "memory_layer": "星魂记忆",
            "memory_layer_number": 13,
            "boundary_proposal_only": True,
            "enters_star_soul_layer": False,
            "star_soul_continuity_executed": False,
            "star_soul_continuity_authorized": False,
            "persistent_autonomous_identity_created": False,
            "consciousness_claimed": False,
            "self_awareness_claimed": False,
            "personhood_claimed": False,
            "sentience_claimed": False,
            "enters_star_cosmos_layer": False,
            "enters_star_source_layer": False,
        }
        for key, expected in hard_boundary_requirements.items():
            _add_check(
                checks,
                blocking_reasons,
                f"source_thirteenth_memory_layer_boundary_{key}",
                hard_boundary.get(key) == expected,
                f"source_thirteenth_memory_layer_boundary_{key}_must_match",
            )

    return checks, blocking_reasons


def _review_gate_summary(ready: bool) -> dict[str, Any]:
    return {
        "review_status": (
            "star_soul_memory_continuity_boundary_reviewed_for_human_review_only"
            if ready
            else "blocked"
        ),
        "source_star_soul_proposal_version": SOURCE_STAR_SOUL_PROPOSAL_VERSION,
        "source_star_soul_proposal_valid": ready,
        "review_gate_only": True,
        "review_only": True,
        "non_authorizing": True,
        "non_executing": True,
        "non_recording": True,
        "non_ledger_creating": True,
        "non_identity_creating": True,
        "non_consciousness_claiming": True,
        "civilization_core_complete_claimed": False,
    }


def _source_proposal_summary(ready: bool) -> dict[str, Any]:
    return {
        "source_star_soul_proposal_version": SOURCE_STAR_SOUL_PROPOSAL_VERSION,
        "source_star_soul_proposal_status": (
            "star_soul_memory_continuity_boundary_proposal_ready"
            if ready
            else "blocked"
        ),
        "source_proposed_chain_versions": list(
            SOURCE_PROPOSED_CHAIN_VERSIONS
        ),
        "source_proposed_star_hub_chain_versions": list(
            SOURCE_PROPOSED_STAR_HUB_CHAIN_VERSIONS
        ),
        "source_star_soul_memory_continuity_boundary_proposal_valid": ready,
        "source_proposal_authorized_star_soul_continuity": False,
        "source_proposal_created_star_soul_continuity_record": False,
        "source_proposal_created_star_soul_continuity_ledger_entry": False,
        "source_proposal_created_persistent_autonomous_identity": False,
        "source_proposal_performed_identity_awakening": False,
        "source_proposal_claimed_consciousness": False,
        "source_proposal_claimed_self_awareness": False,
        "source_proposal_claimed_personhood": False,
        "source_proposal_claimed_sentience": False,
        "source_proposal_authorized_autonomous_execution": False,
        "source_proposal_authorized_memory_write": False,
        "source_proposal_authorized_openclaw_execution": False,
        "raw_source_proposal_copied": False,
    }


def _review_gate(ready: bool) -> dict[str, Any]:
    return {
        "review_status": (
            "star_soul_memory_continuity_boundary_reviewed_for_human_review_only"
            if ready
            else "blocked_no_star_soul_memory_continuity_boundary_review_readiness_claim"
        ),
        "boundary_type": "star_soul_memory_continuity_boundary_review_gate",
        "source_star_soul_proposal_version": SOURCE_STAR_SOUL_PROPOSAL_VERSION,
        "star_soul_memory_continuity_boundary_reviewed": ready,
        "star_soul_memory_continuity_boundary_structurally_review_ready": ready,
        "source_star_soul_memory_continuity_boundary_proposal_valid": ready,
        "thirteenth_memory_layer_star_soul_boundary_reviewed_for_human_review_only": ready,
        **REVIEW_OBJECT_FALSE_FLAGS,
        "reviewed_chain_versions": list(REVIEWED_CHAIN_VERSIONS),
        "reviewed_star_hub_chain_versions": list(
            REVIEWED_STAR_HUB_CHAIN_VERSIONS
        ),
        "star_soul_memory_continuity_boundary_review_components": _review_components(
            ready
        ),
        "next_allowed_step": READY_NEXT_ALLOWED_STEP,
        "non_authorization_notice": (
            "The v3.0.0 Star-Soul Memory continuity boundary proposal has been structurally reviewed for human review only. This review grants no continuity, identity, consciousness, execution, authorization, recording, ledger, write, approval, handoff, scheduling, dry-run, or autonomous authority."
            if ready
            else "The Star-Soul Memory continuity boundary review gate is blocked and grants no readiness, continuity, identity, consciousness, execution, authorization, recording, ledger, write, approval, handoff, scheduling, dry-run, or autonomous authority."
        ),
    }


def _review_components(ready: bool) -> dict[str, str]:
    status = "reviewed_for_human_review_only" if ready else "blocked"
    return {
        f"{key}_review": status
        for key in sorted(
            PROPOSED_STAR_SOUL_MEMORY_CONTINUITY_BOUNDARY_KEYS
        )
    }


def _reviewed_boundaries(ready: bool) -> dict[str, dict[str, Any]]:
    status = "reviewed_for_human_review_only" if ready else "blocked"
    boundary_false_flags = {
        "star_soul_continuity_executed": False,
        "star_soul_continuity_authorized": False,
        "star_soul_continuity_record_created": False,
        "star_soul_continuity_ledger_entry_created": False,
        "enters_star_soul_layer": False,
        "persistent_autonomous_identity_created": False,
        "identity_awakening_performed": False,
        "personality_awakening_performed": False,
        "soul_awakening_performed": False,
        "consciousness_claimed": False,
        "self_awareness_claimed": False,
        "personhood_claimed": False,
        "sentience_claimed": False,
        "autonomous_self_model_executed": False,
        "autonomous_execution_authorized": False,
        "memory_write_performed": False,
        "durable_memory_written": False,
        "memory_graph_mutation_authorized": False,
        "memory_graph_mutated": False,
        "operation_ledger_creation_authorized": False,
        "operation_ledger_entry_created": False,
        "openclaw_execution_authorized": False,
        "openclaw_called": False,
        "openclaw_executed": False,
        "github_write_authorized": False,
        "github_api_called": False,
        "approval_authorized": False,
        "approval_granted": False,
        "civilization_core_complete_claimed": False,
        "enters_star_cosmos_layer": False,
        "enters_star_source_layer": False,
    }
    return {
        key: {
            "review_only": True,
            "boundary_status": status,
            "summary": "This sanitized boundary category was structurally reviewed from v3.0.0 proposal metadata only and grants no continuity, identity, authority, record, ledger, or write.",
            "raw_source_boundary_copied": False,
            **boundary_false_flags,
        }
        for key in sorted(
            PROPOSED_STAR_SOUL_MEMORY_CONTINUITY_BOUNDARY_KEYS
        )
    }


def _non_authorization_boundary(ready: bool) -> dict[str, Any]:
    return {
        "review_gate_ready_is_star_soul_continuity_execution": False,
        "review_gate_ready_is_star_soul_continuity_authorization": False,
        "review_gate_ready_is_star_soul_continuity_record_creation": False,
        "review_gate_ready_is_star_soul_continuity_ledger_creation": False,
        "review_gate_ready_is_persistent_autonomous_identity_creation": False,
        "review_gate_ready_is_identity_personality_or_soul_awakening": False,
        "review_gate_ready_is_consciousness_self_awareness_personhood_or_sentience_claim": False,
        "review_gate_ready_is_autonomous_self_model_execution": False,
        "review_gate_ready_is_finalization_completion_closure_or_attestation_execution": False,
        "review_gate_ready_is_audit_response_correction_or_enforcement": False,
        "review_gate_ready_is_rule_creation_activation_or_enforcement": False,
        "review_gate_ready_is_autonomous_governance_or_execution": False,
        "review_gate_ready_is_memory_write_or_graph_mutation": False,
        "review_gate_ready_is_operation_ledger_creation": False,
        "review_gate_ready_is_openclaw_or_github_execution": False,
        "review_gate_ready_is_approval_or_human_decision": False,
        "review_gate_ready_is_handoff_scheduling_or_dry_run": False,
        "review_gate_ready_is_civilization_core_completion": False,
        "review_gate_ready_is_star_soul_star_cosmos_or_star_source_entry": False,
        "only_permits_later_star_soul_memory_continuity_boundary_approval_proposal": ready,
        "human_operator_remains_final_authority": True,
    }


def _preserved_governance_boundaries() -> list[str]:
    return [
        "This review gate does not execute or authorize Star-Soul continuity.",
        "This review gate does not create Star-Soul continuity records or continuity-ledger entries.",
        "This review gate does not create or activate a persistent autonomous identity.",
        "This review gate does not perform identity, personality, or soul awakening.",
        "This review gate makes no consciousness, self-awareness, personhood, or sentience claim.",
        "This review gate does not execute or authorize an autonomous self-model.",
        "This review gate does not execute finalization, completion, closure, attestation, audit, response, correction, enforcement, or rules.",
        "This review gate does not create autonomous governance or authorize autonomous execution.",
        "This review gate does not authorize handoff, scheduling, approval, or dry-run execution.",
        "This review gate does not write durable memory, mutate Memory Graph, create operation-ledger entries, or call OpenClaw or GitHub APIs.",
        "This review gate does not claim Civilization Core completion, mature 星魂 continuity, 星宙 evolution, or 星源 self-evolution.",
        "Human Operator remains final authority.",
    ]


def _thirteenth_memory_layer_boundary(ready: bool) -> dict[str, Any]:
    return {
        "memory_layer": "星魂记忆",
        "memory_layer_number": 13,
        "boundary_review_gate_only": True,
        "reviewed_for_human_review_only": ready,
        "enters_thirteenth_memory_layer": False,
        "thirteenth_memory_layer_transition_authorized": False,
        "enters_star_soul_layer": False,
        "star_soul_continuity_executed": False,
        "star_soul_continuity_authorized": False,
        "star_soul_continuity_record_created": False,
        "star_soul_continuity_ledger_entry_created": False,
        "persistent_autonomous_identity_created": False,
        "identity_awakening_performed": False,
        "personality_awakening_performed": False,
        "soul_awakening_performed": False,
        "consciousness_claimed": False,
        "self_awareness_claimed": False,
        "personhood_claimed": False,
        "sentience_claimed": False,
        "autonomous_self_model_executed": False,
        "civilization_core_complete_claimed": False,
        "enters_star_cosmos_layer": False,
        "enters_star_source_layer": False,
        "boundary_notice": "v3.1.0 reviews only the proposal boundary for the 13th memory layer. A later separate v3.2.0 approval proposal is required before any further governed consideration.",
    }


def _future_next_step_constraints() -> list[str]:
    return [
        "A later separate v3.2.0 approval proposal may consume this sanitized review report through a local governed process.",
        "The later approval proposal must remain proposal-only and preserve every non-execution, non-authorization, non-recording, non-ledger, non-write, and non-consciousness boundary.",
        "This review gate records no real Human Operator decision and creates, submits, executes, or approves no approval request.",
        "Any later continuity design must retain false-continuity prevention, evidence lineage, auditability, rollback, suspension, and Human Operator final authority.",
        "Human Operator remains final authority for all later Star-Soul continuity decisions.",
    ]


def _next_stage_constraints() -> list[str]:
    return [
        f"The only next allowed step is {READY_NEXT_ALLOWED_STEP}.",
        "v3.1.0 remains a Star-Soul Memory continuity boundary review gate only.",
        "No Star-Soul continuity execution, authorization, record, ledger, identity creation, awakening, consciousness claim, self-model execution, write, approval, handoff, scheduling, or dry-run occurs.",
        "No entry into mature 星魂 continuity, 星宙 evolution, or 星源 self-evolution occurs.",
    ]


def _scope_boundaries() -> list[str]:
    return [
        "Civilization Core is the total system.",
        "Fifteen Memory Layers are the highest memory coordinate system.",
        "Subspace Memory System is the engineering carrier.",
        "Hermes, Codex CLI, OpenClaw, Terminal, and GitHub are components, not the core.",
        "This v3.1.0 step is limited to the 星魂记忆 continuity boundary review gate.",
    ]


def _risk_notes(sensitive_field_count: int) -> list[str]:
    notes = [
        "Review readiness must not be interpreted as continuity, identity, consciousness, execution, authorization, recording, ledger, write, approval, handoff, scheduling, or autonomous authority.",
        "False continuity, inferred identity, persona drift, and unsupported memory lineage remain explicit risks for later human review.",
        "The report is deterministic, local-only, read-only, and contains sanitized structural summaries rather than raw source proposal data.",
        "Civilization Core completion and later memory-layer entry are not claimed.",
    ]
    if sensitive_field_count:
        notes.append("Sensitive fields were omitted from review gate output.")
    return notes


def _required_human_actions(
    ready: bool, blocking_reasons: list[str]
) -> list[str]:
    if ready:
        return [
            "human_operator_must_review_v3_1_0_star_soul_memory_continuity_boundary_review_gate_before_any_v3_2_0_approval_proposal",
            "human_operator_must_confirm_review_readiness_grants_no_continuity_identity_consciousness_execution_authorization_recording_ledger_write_approval_handoff_scheduling_or_autonomous_authority",
            "human_operator_must_use_a_separate_governed_process_for_v3_2_0_star_soul_memory_continuity_boundary_approval_proposal",
        ]
    actions = [
        "repair_source_v3_0_0_star_soul_memory_continuity_boundary_proposal_before_review_gate_can_continue",
        "confirm_all_unsafe_continuity_identity_consciousness_execution_authorization_recording_ledger_audit_response_correction_enforcement_rule_write_approval_handoff_scheduling_and_later_layer_flags_remain_false",
        "rerun_local_v3_1_0_star_soul_memory_continuity_boundary_review_gate_after_blockers_are_resolved",
    ]
    if blocking_reasons:
        actions.append(
            "resolve_blocking_reasons_before_star_soul_memory_continuity_boundary_review_gate_can_be_ready"
        )
    return actions


def _proposed_boundaries_remain_proposal_only(
    boundaries: Mapping[str, Any],
) -> bool:
    for boundary in boundaries.values():
        if not isinstance(boundary, Mapping):
            return False
        if boundary.get("proposal_only") is not True:
            return False
        if boundary.get("boundary_status") != "proposed_for_human_review_only":
            return False
        for key, value in boundary.items():
            if value is True and key != "proposal_only":
                return False
        if _unsafe_true_fields(boundary) or _unsafe_text_claims(boundary):
            return False
    return bool(boundaries)


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
                found.append(str(key))
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
    "GOVERNED_STAR_SOUL_MEMORY_CONTINUITY_BOUNDARY_REVIEW_GATE_VERSION",
    "SOURCE_STAR_SOUL_PROPOSAL_VERSION",
    "REVIEWED_CHAIN_VERSIONS",
    "REVIEWED_STAR_HUB_CHAIN_VERSIONS",
    "READY_NEXT_ALLOWED_STEP",
    "LAYER_MAPPING",
    "REVIEW_GATE_FALSE_FLAGS",
    "REVIEW_OBJECT_FALSE_FLAGS",
    "SENSITIVE_KEYS",
    "build_governed_star_soul_memory_continuity_boundary_review_gate",
    "governed_star_soul_memory_continuity_boundary_review_gate_to_json",
]
