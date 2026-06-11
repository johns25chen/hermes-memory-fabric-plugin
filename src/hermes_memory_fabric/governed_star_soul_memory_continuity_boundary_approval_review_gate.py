"""Governed Star-Soul Memory continuity boundary approval review gate."""

from __future__ import annotations

import json
from typing import Any, Mapping

from .governed_star_soul_memory_continuity_boundary_approval_proposal import (
    APPROVAL_PROPOSAL_FALSE_FLAGS as SOURCE_APPROVAL_PROPOSAL_FALSE_FLAGS,
    APPROVAL_PROPOSAL_OBJECT_FALSE_FLAGS as SOURCE_APPROVAL_PROPOSAL_OBJECT_FALSE_FLAGS,
    FORBIDDEN_BOUNDARY_CLAIMS as SOURCE_FORBIDDEN_BOUNDARY_CLAIMS,
    PROPOSED_CHAIN_VERSIONS as SOURCE_PROPOSED_CHAIN_VERSIONS,
    PROPOSED_STAR_HUB_CHAIN_VERSIONS as SOURCE_PROPOSED_STAR_HUB_CHAIN_VERSIONS,
    SOURCE_REVIEWED_CHAIN_VERSIONS,
    SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS,
    SENSITIVE_KEYS,
)


GOVERNED_STAR_SOUL_MEMORY_CONTINUITY_BOUNDARY_APPROVAL_REVIEW_GATE_VERSION = (
    "3.3.0"
)
SOURCE_STAR_SOUL_APPROVAL_PROPOSAL_VERSION = "3.2.0"

SOURCE_PROPOSED_CHAIN_VERSIONS = list(SOURCE_PROPOSED_CHAIN_VERSIONS)
SOURCE_PROPOSED_STAR_HUB_CHAIN_VERSIONS = list(
    SOURCE_PROPOSED_STAR_HUB_CHAIN_VERSIONS
)
REVIEWED_CHAIN_VERSIONS = list(SOURCE_PROPOSED_CHAIN_VERSIONS)
REVIEWED_STAR_HUB_CHAIN_VERSIONS = list(
    SOURCE_PROPOSED_STAR_HUB_CHAIN_VERSIONS
)

READY_NEXT_ALLOWED_STEP = (
    "v3.4.0 Star-Soul Memory continuity boundary approval request proposal"
)

LAYER_MAPPING = {
    "primary_layer": "星魂记忆",
    "primary_layer_status": "Star-Soul Memory continuity boundary approval review gate only, not real approval, not approval request creation, not approval request submission, not approval request execution, not approval grant, not human decision recording, not continuity execution, not continuity authorization, not continuity record creation, not continuity-ledger creation, not persistent autonomous identity creation, not consciousness claim, not self-awareness claim, not personhood claim, not sentience claim, not identity awakening, not personality awakening, not autonomous self-model execution, not durable memory write, not Memory Graph mutation, not operation-ledger creation, and not autonomous execution",
    "source_layer": "星魂记忆",
    "source_layer_status": "Star-Soul Memory continuity boundary approval proposal complete for human review only",
    "supporting_layers": [
        "星穹记忆",
        "星域记忆",
        "星界记忆",
        "星辰记忆",
        "星律记忆",
        "星魂记忆",
    ],
    "direction": "Star-Soul Memory continuity boundary approval proposal -> Star-Soul Memory continuity boundary approval review gate",
    "boundary_transition": "v3.2.0 Star-Soul Memory continuity boundary approval proposal -> v3.3.0 Star-Soul Memory continuity boundary approval review gate",
    "hard_boundary": "v3.3.0 reviews approval proposal boundaries for human review only and does not create, submit, execute, grant, or record approval",
}

SOURCE_REQUIRED_TRUE_FLAGS = {
    "read_only",
    "read_only_memory",
    "proposal_only",
    "approval_proposal_only",
    "star_soul_memory_continuity_boundary_approval_proposal_only",
    "thirteenth_memory_layer_star_soul_boundary_approval_proposal_only",
    "star_soul_memory_continuity_boundary_approval_proposed_for_human_review_only",
    "star_soul_memory_continuity_boundary_approval_review_gate_ready_for_human_review_only",
}

APPROVAL_REVIEW_GATE_FALSE_FLAGS = dict(
    SOURCE_APPROVAL_PROPOSAL_FALSE_FLAGS
)
APPROVAL_REVIEW_GATE_OBJECT_FALSE_FLAGS = {
    **SOURCE_APPROVAL_PROPOSAL_OBJECT_FALSE_FLAGS,
    **APPROVAL_REVIEW_GATE_FALSE_FLAGS,
}
UNSAFE_TRUE_FIELDS = set(APPROVAL_REVIEW_GATE_OBJECT_FALSE_FLAGS)

FORBIDDEN_BOUNDARY_CLAIMS = (
    *SOURCE_FORBIDDEN_BOUNDARY_CLAIMS,
    "approval request creation is authorized",
    "approval request submission is authorized",
    "approval request execution is authorized",
    "approval grant is authorized",
    "real human decision recording is authorized",
    "star-soul continuity record creation is authorized",
    "star-soul continuity ledger creation is authorized",
    "github api execution is authorized",
)

APPROVAL_REVIEW_GATE_COMPONENT_KEYS = {
    "source_star_soul_continuity_boundary_approval_proposal",
    "approval_proposal_structural_review_boundary",
    "approval_request_non_creation_review_boundary",
    "approval_request_non_submission_review_boundary",
    "approval_request_non_execution_review_boundary",
    "approval_grant_non_authorization_review_boundary",
    "real_human_decision_non_recording_review_boundary",
    "star_soul_continuity_non_execution_review_boundary",
    "star_soul_continuity_non_authorization_review_boundary",
    "star_soul_continuity_non_recording_review_boundary",
    "star_soul_continuity_non_ledger_review_boundary",
    "autonomous_identity_non_creation_review_boundary",
    "identity_awakening_non_execution_review_boundary",
    "personality_awakening_non_execution_review_boundary",
    "soul_awakening_non_execution_review_boundary",
    "consciousness_claim_non_authorization_review_boundary",
    "self_awareness_claim_non_authorization_review_boundary",
    "personhood_claim_non_authorization_review_boundary",
    "sentience_claim_non_authorization_review_boundary",
    "autonomous_self_model_non_execution_review_boundary",
    "memory_write_non_authorization_review_boundary",
    "memory_graph_mutation_non_authorization_review_boundary",
    "operation_ledger_non_creation_review_boundary",
    "openclaw_execution_non_authorization_review_boundary",
    "github_api_non_execution_review_boundary",
    "handoff_non_authorization_review_boundary",
    "scheduling_non_authorization_review_boundary",
    "dry_run_non_execution_review_boundary",
    "civilization_core_completion_non_claim_review_boundary",
    "star_cosmos_entry_non_authorization_review_boundary",
    "star_source_entry_non_authorization_review_boundary",
    "evidence_lineage_review_boundary",
    "false_approval_prevention_review_boundary",
    "approval_rollback_review_boundary",
    "approval_suspension_review_boundary",
    "human_operator_final_authority_review_boundary",
    "thirteen_memory_layer_review_boundary",
    "fifteen_memory_layers_review_boundary",
}

BOUNDARY_FALSE_FLAGS = {
    "approval_request_created": False,
    "approval_request_submitted": False,
    "approval_request_executed": False,
    "approval_granted": False,
    "real_human_decision_recorded": False,
    "star_soul_continuity_executed": False,
    "star_soul_continuity_authorized": False,
    "star_soul_continuity_record_created": False,
    "star_soul_continuity_ledger_entry_created": False,
    "persistent_autonomous_identity_created": False,
    "persistent_autonomous_identity_activated": False,
    "identity_awakening_performed": False,
    "personality_awakening_performed": False,
    "soul_awakening_performed": False,
    "consciousness_claimed": False,
    "self_awareness_claimed": False,
    "personhood_claimed": False,
    "sentience_claimed": False,
    "autonomous_self_model_executed": False,
    "autonomous_self_model_authorized": False,
    "finalization_executed": False,
    "completion_executed": False,
    "closure_executed": False,
    "attestation_executed": False,
    "audit_executed": False,
    "audit_log_written": False,
    "violation_response_executed": False,
    "automated_correction_performed": False,
    "violation_enforced": False,
    "candidate_rules_enforced": False,
    "star_law_rules_created": False,
    "star_law_rules_activated": False,
    "star_law_rules_enforced": False,
    "autonomous_governance_created": False,
    "autonomous_execution_authorized": False,
    "memory_write_performed": False,
    "durable_memory_written": False,
    "memory_graph_mutated": False,
    "operation_ledger_entry_created": False,
    "openclaw_called": False,
    "openclaw_executed": False,
    "github_api_called": False,
    "handoff_authorized": False,
    "star_hub_handoff_authorized": False,
    "scheduling_performed": False,
    "dry_run_executed": False,
    "civilization_core_complete_claimed": False,
    "enters_star_soul_layer": False,
    "enters_star_cosmos_layer": False,
    "enters_star_source_layer": False,
}


def build_governed_star_soul_memory_continuity_boundary_approval_review_gate(
    star_soul_approval_proposal_report: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a deterministic, local-only Star-Soul approval review gate."""

    checks, blocking_reasons = _approval_review_gate_checks(
        star_soul_approval_proposal_report
    )
    sensitive_field_count = _count_sensitive_keys(
        star_soul_approval_proposal_report
    )
    blocking_reasons = list(dict.fromkeys(blocking_reasons))
    ready = not blocking_reasons

    return {
        "version": GOVERNED_STAR_SOUL_MEMORY_CONTINUITY_BOUNDARY_APPROVAL_REVIEW_GATE_VERSION,
        "status": (
            "star_soul_memory_continuity_boundary_approval_review_gate_ready"
            if ready
            else "blocked"
        ),
        "read_only": True,
        "read_only_memory": True,
        "review_gate_only": True,
        "approval_review_gate_only": True,
        "star_soul_memory_continuity_boundary_approval_review_gate_only": True,
        "thirteenth_memory_layer_star_soul_boundary_approval_review_gate_only": True,
        **APPROVAL_REVIEW_GATE_FALSE_FLAGS,
        "star_soul_memory_continuity_boundary_approval_reviewed_for_human_review_only": ready,
        "star_soul_memory_continuity_boundary_approval_request_proposal_ready_for_human_review_only": ready,
        "civilization_core_layer_mapping": dict(LAYER_MAPPING),
        "source_star_soul_approval_proposal_version": SOURCE_STAR_SOUL_APPROVAL_PROPOSAL_VERSION,
        "source_reviewed_chain_versions": list(
            SOURCE_REVIEWED_CHAIN_VERSIONS
        ),
        "source_reviewed_star_hub_chain_versions": list(
            SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS
        ),
        "source_proposed_chain_versions": list(
            SOURCE_PROPOSED_CHAIN_VERSIONS
        ),
        "source_proposed_star_hub_chain_versions": list(
            SOURCE_PROPOSED_STAR_HUB_CHAIN_VERSIONS
        ),
        "reviewed_chain_versions": list(REVIEWED_CHAIN_VERSIONS),
        "reviewed_star_hub_chain_versions": list(
            REVIEWED_STAR_HUB_CHAIN_VERSIONS
        ),
        "star_soul_memory_continuity_boundary_approval_review_gate_summary": _approval_review_gate_summary(
            ready
        ),
        "approval_review_gate_checks": checks,
        "source_star_soul_approval_proposal_summary": _source_approval_proposal_summary(
            ready
        ),
        "star_soul_memory_continuity_boundary_approval_review_gate": _approval_review_gate(
            ready
        ),
        "reviewed_star_soul_memory_continuity_approval_boundaries": _reviewed_approval_boundaries(
            ready
        ),
        "non_authorization_boundary": _non_authorization_boundary(ready),
        "preserved_governance_boundaries": _preserved_governance_boundaries(),
        "thirteenth_memory_layer_boundary": _thirteenth_memory_layer_boundary(
            ready
        ),
        "future_star_soul_memory_continuity_approval_request_proposal_constraints": _future_approval_request_proposal_constraints(),
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


def governed_star_soul_memory_continuity_boundary_approval_review_gate_to_json(
    report: Mapping[str, Any],
) -> str:
    """Serialize the Star-Soul continuity boundary approval review gate."""

    return json.dumps(
        dict(report), ensure_ascii=True, indent=2, sort_keys=True
    ) + "\n"


def _approval_review_gate_checks(
    report: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    blocking_reasons: list[str] = []

    if not isinstance(report, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_star_soul_approval_proposal_mapping",
            False,
            "source_star_soul_approval_proposal_report_must_be_mapping",
        )
        return checks, blocking_reasons

    _add_check(
        checks,
        blocking_reasons,
        "source_star_soul_approval_proposal_version",
        report.get("version") == SOURCE_STAR_SOUL_APPROVAL_PROPOSAL_VERSION,
        "source_star_soul_approval_proposal_version_must_be_3_2_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_star_soul_approval_proposal_status",
        report.get("status")
        == "star_soul_memory_continuity_boundary_approval_proposal_ready",
        "source_star_soul_approval_proposal_status_must_be_ready",
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
            for key, expected in SOURCE_APPROVAL_PROPOSAL_FALSE_FLAGS.items()
        ),
        "source_star_soul_approval_proposal_all_required_unsafe_flags_must_be_false",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_no_unsafe_true_claims",
        _unsafe_true_fields(report) == [],
        "source_star_soul_approval_proposal_must_not_claim_execution_authorization_recording_ledger_audit_response_correction_enforcement_rule_autonomous_handoff_scheduling_approval_write_continuity_identity_consciousness_or_later_layer_actions",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_no_unsafe_text_claims",
        _unsafe_text_claims(report) == [],
        "source_star_soul_approval_proposal_must_not_textually_claim_unsafe_approval_continuity_identity_consciousness_execution_write_or_later_layer_actions",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_star_soul_review_gate_version",
        report.get("source_star_soul_review_gate_version") == "3.1.0",
        "source_star_soul_review_gate_version_must_be_3_1_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_reviewed_chain_versions",
        report.get("source_reviewed_chain_versions")
        == SOURCE_REVIEWED_CHAIN_VERSIONS,
        "source_reviewed_chain_versions_must_exactly_match_v2_9_0_through_v2_60_0_plus_v3_0_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_reviewed_star_hub_chain_versions",
        report.get("source_reviewed_star_hub_chain_versions")
        == SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS,
        "source_reviewed_star_hub_chain_versions_must_exactly_match_v2_19_0_through_v2_60_0_plus_v3_0_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_proposed_chain_versions",
        report.get("proposed_chain_versions")
        == SOURCE_PROPOSED_CHAIN_VERSIONS,
        "source_proposed_chain_versions_must_exactly_match_v2_9_0_through_v2_60_0_plus_v3_0_0_v3_1_0_v3_2_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_proposed_star_hub_chain_versions",
        report.get("proposed_star_hub_chain_versions")
        == SOURCE_PROPOSED_STAR_HUB_CHAIN_VERSIONS,
        "source_proposed_star_hub_chain_versions_must_exactly_match_v2_19_0_through_v2_60_0_plus_v3_0_0_v3_1_0_v3_2_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_next_allowed_step",
        report.get("next_allowed_step")
        == "v3.3.0 Star-Soul Memory continuity boundary approval review gate",
        "source_next_allowed_step_must_be_v3_3_0_star_soul_memory_continuity_boundary_approval_review_gate",
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
            "source_layer": "星魂记忆",
            "hard_boundary": "v3.2.0 proposes approval boundaries for human review only and does not create, submit, execute, or grant approval",
        }
        for key, expected in mapping_requirements.items():
            _add_check(
                checks,
                blocking_reasons,
                f"source_layer_mapping_{key}",
                mapping.get(key) == expected,
                f"source_layer_mapping_{key}_must_match_v3_2_0",
            )

    approval_proposal = report.get(
        "star_soul_memory_continuity_boundary_approval_proposal"
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_nested_approval_proposal_shape",
        isinstance(approval_proposal, Mapping),
        "source_nested_star_soul_approval_proposal_must_be_mapping",
    )
    if isinstance(approval_proposal, Mapping):
        nested_requirements = {
            "proposal_status": "star_soul_memory_continuity_boundary_approval_proposed_for_human_review_only",
            "boundary_type": "star_soul_memory_continuity_boundary_approval_proposal",
            "source_star_soul_review_gate_version": "3.1.0",
            "source_star_soul_memory_continuity_boundary_review_gate_valid": True,
            "star_soul_memory_continuity_boundary_approval_proposed": True,
            "star_soul_memory_continuity_boundary_approval_review_gate_ready_for_human_review_only": True,
            "thirteenth_memory_layer_star_soul_boundary_approval_proposed_for_human_review_only": True,
        }
        for key, expected in nested_requirements.items():
            _add_check(
                checks,
                blocking_reasons,
                f"source_nested_approval_proposal_{key}",
                approval_proposal.get(key) == expected,
                f"source_nested_approval_proposal_{key}_must_match",
            )
        _add_check(
            checks,
            blocking_reasons,
            "source_nested_approval_proposal_unsafe_flags_false",
            all(
                approval_proposal.get(key) is expected
                for key, expected in SOURCE_APPROVAL_PROPOSAL_OBJECT_FALSE_FLAGS.items()
            ),
            "source_nested_approval_proposal_all_required_unsafe_flags_must_be_false",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_nested_approval_proposal_chain_versions",
            approval_proposal.get("proposed_chain_versions")
            == SOURCE_PROPOSED_CHAIN_VERSIONS,
            "source_nested_approval_proposal_chain_versions_must_match",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_nested_approval_proposal_star_hub_chain_versions",
            approval_proposal.get("proposed_star_hub_chain_versions")
            == SOURCE_PROPOSED_STAR_HUB_CHAIN_VERSIONS,
            "source_nested_approval_proposal_star_hub_chain_versions_must_match",
        )

    boundaries = report.get(
        "proposed_star_soul_memory_continuity_approval_boundaries"
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_proposed_approval_boundaries_shape",
        isinstance(boundaries, Mapping),
        "source_proposed_star_soul_approval_boundaries_must_be_mapping",
    )
    if isinstance(boundaries, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_proposed_approval_boundaries_proposal_only_non_authorizing",
            _approval_boundaries_remain_proposal_only(boundaries),
            "source_proposed_star_soul_approval_boundaries_must_remain_approval_proposal_only_and_non_authorizing",
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
            "boundary_approval_proposal_only": True,
            "enters_star_soul_layer": False,
            "star_soul_continuity_executed": False,
            "star_soul_continuity_authorized": False,
            "approval_request_created": False,
            "approval_request_submitted": False,
            "approval_request_executed": False,
            "approval_granted": False,
            "real_human_decision_recorded": False,
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


def _approval_review_gate_summary(ready: bool) -> dict[str, Any]:
    return {
        "review_status": (
            "star_soul_memory_continuity_boundary_approval_reviewed_for_human_review_only"
            if ready
            else "blocked"
        ),
        "source_star_soul_approval_proposal_version": SOURCE_STAR_SOUL_APPROVAL_PROPOSAL_VERSION,
        "source_star_soul_approval_proposal_valid": ready,
        "approval_review_gate_only": True,
        "human_review_only": True,
        "non_authorizing": True,
        "non_executing": True,
        "non_recording": True,
        "non_ledger_creating": True,
        "approval_request_created": False,
        "approval_request_submitted": False,
        "approval_request_executed": False,
        "approval_granted": False,
        "real_human_decision_recorded": False,
        "civilization_core_complete_claimed": False,
    }


def _source_approval_proposal_summary(ready: bool) -> dict[str, Any]:
    return {
        "source_star_soul_approval_proposal_version": SOURCE_STAR_SOUL_APPROVAL_PROPOSAL_VERSION,
        "source_star_soul_approval_proposal_status": (
            "star_soul_memory_continuity_boundary_approval_proposal_ready"
            if ready
            else "blocked"
        ),
        "source_reviewed_chain_versions": list(
            SOURCE_REVIEWED_CHAIN_VERSIONS
        ),
        "source_reviewed_star_hub_chain_versions": list(
            SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS
        ),
        "source_proposed_chain_versions": list(
            SOURCE_PROPOSED_CHAIN_VERSIONS
        ),
        "source_proposed_star_hub_chain_versions": list(
            SOURCE_PROPOSED_STAR_HUB_CHAIN_VERSIONS
        ),
        "source_star_soul_memory_continuity_boundary_approval_proposal_valid": ready,
        "source_approval_proposal_created_approval_request": False,
        "source_approval_proposal_submitted_approval_request": False,
        "source_approval_proposal_executed_approval_request": False,
        "source_approval_proposal_granted_approval": False,
        "source_approval_proposal_recorded_real_human_decision": False,
        "source_approval_proposal_authorized_star_soul_continuity": False,
        "source_approval_proposal_authorized_memory_write": False,
        "source_approval_proposal_authorized_openclaw_execution": False,
        "raw_source_approval_proposal_copied": False,
    }


def _approval_review_gate(ready: bool) -> dict[str, Any]:
    return {
        "review_status": (
            "star_soul_memory_continuity_boundary_approval_reviewed_for_human_review_only"
            if ready
            else "blocked_no_star_soul_memory_continuity_boundary_approval_review_readiness_claim"
        ),
        "boundary_type": "star_soul_memory_continuity_boundary_approval_review_gate",
        "source_star_soul_approval_proposal_version": SOURCE_STAR_SOUL_APPROVAL_PROPOSAL_VERSION,
        "source_star_soul_memory_continuity_boundary_approval_proposal_valid": ready,
        "star_soul_memory_continuity_boundary_approval_reviewed": ready,
        "star_soul_memory_continuity_boundary_approval_structurally_review_ready": ready,
        "star_soul_memory_continuity_boundary_approval_request_proposal_ready_for_human_review_only": ready,
        "thirteenth_memory_layer_star_soul_boundary_approval_reviewed_for_human_review_only": ready,
        **APPROVAL_REVIEW_GATE_OBJECT_FALSE_FLAGS,
        "reviewed_chain_versions": list(REVIEWED_CHAIN_VERSIONS),
        "reviewed_star_hub_chain_versions": list(
            REVIEWED_STAR_HUB_CHAIN_VERSIONS
        ),
        "approval_review_gate_components": _approval_review_gate_components(
            ready
        ),
        "next_allowed_step": READY_NEXT_ALLOWED_STEP,
        "non_authorization_notice": (
            "The v3.2.0 Star-Soul Memory continuity boundary approval proposal has been structurally reviewed for human review only. This review creates, submits, executes, and grants no approval; records no real human decision; and grants no continuity, identity, consciousness, execution, authorization, recording, ledger, write, handoff, scheduling, dry-run, or autonomous authority."
            if ready
            else "The Star-Soul Memory continuity boundary approval review gate is blocked and grants no approval readiness, continuity, identity, consciousness, execution, authorization, recording, ledger, write, handoff, scheduling, dry-run, or autonomous authority."
        ),
    }


def _approval_review_gate_components(
    ready: bool,
) -> dict[str, dict[str, Any]]:
    status = "reviewed_for_human_review_only" if ready else "blocked"
    return {
        key: {
            "review_only": True,
            "approval_review_gate_only": True,
            "human_review_only": True,
            "non_authorizing": True,
            "boundary_status": status,
            "summary": "This sanitized approval boundary was structurally reviewed for human review only and creates, submits, executes, grants, or records no approval.",
            "raw_source_boundary_copied": False,
            **BOUNDARY_FALSE_FLAGS,
        }
        for key in sorted(APPROVAL_REVIEW_GATE_COMPONENT_KEYS)
    }


def _reviewed_approval_boundaries(
    ready: bool,
) -> dict[str, dict[str, Any]]:
    return _approval_review_gate_components(ready)


def _non_authorization_boundary(ready: bool) -> dict[str, Any]:
    return {
        "approval_review_gate_ready_is_real_approval": False,
        "approval_review_gate_ready_is_approval_request_creation": False,
        "approval_review_gate_ready_is_approval_request_submission": False,
        "approval_review_gate_ready_is_approval_request_execution": False,
        "approval_review_gate_ready_is_approval_grant": False,
        "approval_review_gate_ready_is_real_human_decision_recording": False,
        "approval_review_gate_ready_is_star_soul_continuity_execution": False,
        "approval_review_gate_ready_is_star_soul_continuity_authorization": False,
        "approval_review_gate_ready_is_star_soul_continuity_record_creation": False,
        "approval_review_gate_ready_is_star_soul_continuity_ledger_creation": False,
        "approval_review_gate_ready_is_persistent_autonomous_identity_creation": False,
        "approval_review_gate_ready_is_identity_personality_or_soul_awakening": False,
        "approval_review_gate_ready_is_consciousness_self_awareness_personhood_or_sentience_claim": False,
        "approval_review_gate_ready_is_autonomous_self_model_execution": False,
        "approval_review_gate_ready_is_finalization_completion_closure_or_attestation_execution": False,
        "approval_review_gate_ready_is_audit_response_correction_or_enforcement": False,
        "approval_review_gate_ready_is_rule_creation_activation_or_enforcement": False,
        "approval_review_gate_ready_is_autonomous_governance_or_execution": False,
        "approval_review_gate_ready_is_memory_write_or_graph_mutation": False,
        "approval_review_gate_ready_is_operation_ledger_creation": False,
        "approval_review_gate_ready_is_openclaw_or_github_execution": False,
        "approval_review_gate_ready_is_handoff_scheduling_or_dry_run": False,
        "approval_review_gate_ready_is_civilization_core_completion": False,
        "approval_review_gate_ready_is_star_soul_star_cosmos_or_star_source_entry": False,
        "only_permits_later_star_soul_memory_continuity_boundary_approval_request_proposal": ready,
        "human_operator_remains_final_authority": True,
    }


def _preserved_governance_boundaries() -> list[str]:
    return [
        "This approval review gate does not create, submit, execute, or grant an approval request.",
        "This approval review gate does not approve anything or record a real Human Operator decision.",
        "This approval review gate does not execute or authorize Star-Soul continuity.",
        "This approval review gate does not create Star-Soul continuity records or continuity-ledger entries.",
        "This approval review gate does not create or activate a persistent autonomous identity.",
        "This approval review gate does not perform identity, personality, or soul awakening.",
        "This approval review gate makes no consciousness, self-awareness, personhood, or sentience claim.",
        "This approval review gate does not execute or authorize an autonomous self-model.",
        "This approval review gate does not execute finalization, completion, closure, attestation, audit, response, correction, enforcement, or rules.",
        "This approval review gate does not create autonomous governance or authorize autonomous execution.",
        "This approval review gate does not authorize handoff, scheduling, or dry-run execution.",
        "This approval review gate does not write durable memory, mutate Memory Graph, create operation-ledger entries, or call OpenClaw or GitHub APIs.",
        "This approval review gate does not claim Civilization Core completion, mature 星魂 continuity, 星宙 evolution, or 星源 self-evolution.",
        "Human Operator remains final authority.",
    ]


def _thirteenth_memory_layer_boundary(ready: bool) -> dict[str, Any]:
    return {
        "memory_layer": "星魂记忆",
        "memory_layer_number": 13,
        "boundary_approval_review_gate_only": True,
        "approval_reviewed_for_human_review_only": ready,
        "enters_thirteenth_memory_layer": False,
        "thirteenth_memory_layer_transition_authorized": False,
        **BOUNDARY_FALSE_FLAGS,
        "boundary_notice": "v3.3.0 reviews only approval proposal boundaries for the 13th memory layer. A later separate v3.4.0 approval request proposal is required before any further governed consideration.",
    }


def _future_approval_request_proposal_constraints() -> list[str]:
    return [
        "A later separate v3.4.0 approval request proposal may consume this sanitized approval review gate through a local governed process.",
        "The later proposal must remain proposal-only and preserve every non-execution, non-authorization, non-recording, non-ledger, non-write, and non-consciousness boundary.",
        "This approval review gate records no real Human Operator decision and creates, submits, executes, or approves no approval request.",
        "Any later continuity design must retain false-approval prevention, evidence lineage, auditability, rollback, suspension, and Human Operator final authority.",
        "Human Operator remains final authority for all later Star-Soul continuity decisions.",
    ]


def _next_stage_constraints() -> list[str]:
    return [
        f"The only next allowed step is {READY_NEXT_ALLOWED_STEP}.",
        "v3.3.0 remains a Star-Soul Memory continuity boundary approval review gate only.",
        "No approval request creation, submission, execution, grant, approval, or real human decision recording occurs.",
        "No Star-Soul continuity execution, authorization, record, ledger, identity creation, awakening, consciousness claim, self-model execution, write, handoff, scheduling, or dry-run occurs.",
        "No entry into mature 星魂 continuity, 星宙 evolution, or 星源 self-evolution occurs.",
    ]


def _scope_boundaries() -> list[str]:
    return [
        "Civilization Core is the total system.",
        "Fifteen Memory Layers are the highest memory coordinate system.",
        "Subspace Memory System is the engineering carrier.",
        "Hermes, Codex CLI, OpenClaw, Terminal, and GitHub are components, not the core.",
        "This v3.3.0 step is limited to the 星魂记忆 continuity boundary approval review gate.",
    ]


def _risk_notes(sensitive_field_count: int) -> list[str]:
    notes = [
        "Approval review readiness must not be interpreted as real approval, approval request creation, submission, execution, grant, or real human decision recording.",
        "False continuity, inferred identity, persona drift, unsupported memory lineage, and false approval remain explicit risks for later human review.",
        "The report is deterministic, local-only, read-only, and contains sanitized structural summaries rather than raw source approval-proposal data.",
        "Civilization Core completion and later memory-layer entry are not claimed.",
    ]
    if sensitive_field_count:
        notes.append("Sensitive fields were omitted from approval review output.")
    return notes


def _required_human_actions(
    ready: bool, blocking_reasons: list[str]
) -> list[str]:
    if ready:
        return [
            "human_operator_must_review_v3_3_0_star_soul_memory_continuity_boundary_approval_review_gate_before_any_v3_4_0_approval_request_proposal",
            "human_operator_must_confirm_approval_review_readiness_grants_no_approval_continuity_identity_consciousness_execution_authorization_recording_ledger_write_handoff_scheduling_or_autonomous_authority",
            "human_operator_must_use_a_separate_governed_process_for_v3_4_0_star_soul_memory_continuity_boundary_approval_request_proposal",
        ]
    actions = [
        "repair_source_v3_2_0_star_soul_memory_continuity_boundary_approval_proposal_before_approval_review_can_continue",
        "confirm_all_unsafe_approval_continuity_identity_consciousness_execution_authorization_recording_ledger_audit_response_correction_enforcement_rule_write_handoff_scheduling_and_later_layer_flags_remain_false",
        "rerun_local_v3_3_0_star_soul_memory_continuity_boundary_approval_review_gate_after_blockers_are_resolved",
    ]
    if blocking_reasons:
        actions.append(
            "resolve_blocking_reasons_before_star_soul_memory_continuity_boundary_approval_review_gate_can_be_ready"
        )
    return actions


def _approval_boundaries_remain_proposal_only(
    boundaries: Mapping[str, Any],
) -> bool:
    for boundary in boundaries.values():
        if not isinstance(boundary, Mapping):
            return False
        if boundary.get("proposal_only") is not True:
            return False
        if boundary.get("approval_proposal_only") is not True:
            return False
        if boundary.get("human_review_only") is not True:
            return False
        if boundary.get("non_authorizing") is not True:
            return False
        if boundary.get("boundary_status") != "proposed_for_human_review_only":
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
    "GOVERNED_STAR_SOUL_MEMORY_CONTINUITY_BOUNDARY_APPROVAL_REVIEW_GATE_VERSION",
    "SOURCE_STAR_SOUL_APPROVAL_PROPOSAL_VERSION",
    "SOURCE_PROPOSED_CHAIN_VERSIONS",
    "SOURCE_PROPOSED_STAR_HUB_CHAIN_VERSIONS",
    "REVIEWED_CHAIN_VERSIONS",
    "REVIEWED_STAR_HUB_CHAIN_VERSIONS",
    "READY_NEXT_ALLOWED_STEP",
    "LAYER_MAPPING",
    "APPROVAL_REVIEW_GATE_FALSE_FLAGS",
    "APPROVAL_REVIEW_GATE_OBJECT_FALSE_FLAGS",
    "APPROVAL_REVIEW_GATE_COMPONENT_KEYS",
    "SENSITIVE_KEYS",
    "build_governed_star_soul_memory_continuity_boundary_approval_review_gate",
    "governed_star_soul_memory_continuity_boundary_approval_review_gate_to_json",
]
