"""Governed Star-Soul Memory continuity completion attestation review gate."""

from __future__ import annotations

import json
from typing import Any, Mapping

from .governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposal import (
    APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_PROPOSAL_FALSE_FLAGS as SOURCE_COMPLETION_ATTESTATION_PROPOSAL_FALSE_FLAGS,
    APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_PROPOSAL_OBJECT_FALSE_FLAGS as SOURCE_COMPLETION_ATTESTATION_PROPOSAL_OBJECT_FALSE_FLAGS,
    FORBIDDEN_BOUNDARY_CLAIMS as SOURCE_FORBIDDEN_BOUNDARY_CLAIMS,
    PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_CHAIN_VERSIONS as SOURCE_PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_CHAIN_VERSIONS,
    PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_STAR_HUB_CHAIN_VERSIONS as SOURCE_PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_STAR_HUB_CHAIN_VERSIONS,
    SENSITIVE_KEYS,
    SOURCE_PROPOSED_DRY_RUN_CHAIN_VERSIONS,
    SOURCE_PROPOSED_DRY_RUN_EXECUTION_CHAIN_VERSIONS,
    SOURCE_PROPOSED_DRY_RUN_EXECUTION_STAR_HUB_CHAIN_VERSIONS,
    SOURCE_PROPOSED_DRY_RUN_STAR_HUB_CHAIN_VERSIONS,
    SOURCE_REVIEWED_CHAIN_VERSIONS,
    SOURCE_REVIEWED_DRY_RUN_CHAIN_VERSIONS,
    SOURCE_REVIEWED_DRY_RUN_EXECUTION_CHAIN_VERSIONS,
    SOURCE_REVIEWED_DRY_RUN_EXECUTION_STAR_HUB_CHAIN_VERSIONS,
    SOURCE_REVIEWED_DRY_RUN_STAR_HUB_CHAIN_VERSIONS,
    SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS,
)


GOVERNED_STAR_SOUL_MEMORY_CONTINUITY_BOUNDARY_APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_REVIEW_GATE_VERSION = (
    "3.11.0"
)
SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_REVIEW_SOURCE_VERSION = (
    "3.10.0"
)
SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_PROPOSAL_VERSION = (
    "3.10.0"
)
SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_EXECUTION_REVIEW_GATE_VERSION = "3.9.0"
SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_EXECUTION_PROPOSAL_VERSION = "3.8.0"
SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_REVIEW_GATE_VERSION = "3.7.0"
SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_PROPOSAL_VERSION = "3.6.0"

SOURCE_REVIEWED_CHAIN_VERSIONS = list(SOURCE_REVIEWED_CHAIN_VERSIONS)
SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS = list(
    SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS
)
SOURCE_PROPOSED_DRY_RUN_CHAIN_VERSIONS = list(
    SOURCE_PROPOSED_DRY_RUN_CHAIN_VERSIONS
)
SOURCE_PROPOSED_DRY_RUN_STAR_HUB_CHAIN_VERSIONS = list(
    SOURCE_PROPOSED_DRY_RUN_STAR_HUB_CHAIN_VERSIONS
)
SOURCE_REVIEWED_DRY_RUN_CHAIN_VERSIONS = list(
    SOURCE_REVIEWED_DRY_RUN_CHAIN_VERSIONS
)
SOURCE_REVIEWED_DRY_RUN_STAR_HUB_CHAIN_VERSIONS = list(
    SOURCE_REVIEWED_DRY_RUN_STAR_HUB_CHAIN_VERSIONS
)
SOURCE_PROPOSED_DRY_RUN_EXECUTION_CHAIN_VERSIONS = list(
    SOURCE_PROPOSED_DRY_RUN_EXECUTION_CHAIN_VERSIONS
)
SOURCE_PROPOSED_DRY_RUN_EXECUTION_STAR_HUB_CHAIN_VERSIONS = list(
    SOURCE_PROPOSED_DRY_RUN_EXECUTION_STAR_HUB_CHAIN_VERSIONS
)
SOURCE_REVIEWED_DRY_RUN_EXECUTION_CHAIN_VERSIONS = list(
    SOURCE_REVIEWED_DRY_RUN_EXECUTION_CHAIN_VERSIONS
)
SOURCE_REVIEWED_DRY_RUN_EXECUTION_STAR_HUB_CHAIN_VERSIONS = list(
    SOURCE_REVIEWED_DRY_RUN_EXECUTION_STAR_HUB_CHAIN_VERSIONS
)
SOURCE_PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_CHAIN_VERSIONS = list(
    SOURCE_PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_CHAIN_VERSIONS
)
SOURCE_PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_STAR_HUB_CHAIN_VERSIONS = list(
    SOURCE_PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_STAR_HUB_CHAIN_VERSIONS
)
REVIEWED_DRY_RUN_COMPLETION_ATTESTATION_CHAIN_VERSIONS = [
    *SOURCE_PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_CHAIN_VERSIONS,
    "v3.11.0",
]
REVIEWED_DRY_RUN_COMPLETION_ATTESTATION_STAR_HUB_CHAIN_VERSIONS = [
    *SOURCE_PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_STAR_HUB_CHAIN_VERSIONS,
    "v3.11.0",
]

READY_NEXT_ALLOWED_STEP = (
    "v3.12.0 Star-Soul Memory continuity boundary approval request dry-run "
    "completion attestation approval proposal"
)

LAYER_MAPPING = {
    "primary_layer": "星魂记忆",
    "primary_layer_status": "Star-Soul Memory continuity boundary approval request dry-run completion attestation review gate only, not dry-run execution, not dry-run plan execution, not completion execution, not attestation execution, not finalization, not closure, not approval request creation, not approval request submission, not approval request execution, not approval grant, not real human decision recording, not continuity execution, not continuity authorization, not continuity record creation, not continuity-ledger creation, not persistent autonomous identity creation, not consciousness claim, not self-awareness claim, not personhood claim, not sentience claim, not identity awakening, not personality awakening, not autonomous self-model execution, not durable memory write, not Memory Graph mutation, not operation-ledger creation, not handoff, not scheduling, and not autonomous execution",
    "source_layer": "星魂记忆",
    "source_layer_status": "Star-Soul Memory continuity boundary approval request dry-run completion attestation proposal complete for human review only",
    "supporting_layers": [
        "星穹记忆",
        "星域记忆",
        "星界记忆",
        "星辰记忆",
        "星律记忆",
        "星魂记忆",
    ],
    "direction": "Star-Soul Memory continuity boundary approval request dry-run completion attestation proposal -> Star-Soul Memory continuity boundary approval request dry-run completion attestation review gate",
    "boundary_transition": "v3.10.0 Star-Soul Memory continuity boundary approval request dry-run completion attestation proposal -> v3.11.0 Star-Soul Memory continuity boundary approval request dry-run completion attestation review gate",
    "hard_boundary": "v3.11.0 reviews approval request dry-run completion attestation proposal boundaries for human review only and does not execute dry-run, execute dry-run plan, execute completion, execute attestation, finalize, close, create, submit, execute, grant, record approval, or record real human decisions",
}

SOURCE_REQUIRED_TRUE_FLAGS = {
    "read_only",
    "read_only_memory",
    "proposal_only",
    "completion_attestation_proposal_only",
    "dry_run_completion_attestation_proposal_only",
    "approval_request_dry_run_completion_attestation_proposal_only",
    "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposal_only",
    "thirteenth_memory_layer_star_soul_boundary_approval_request_dry_run_completion_attestation_proposal_only",
    "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposed_for_human_review_only",
    "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_review_gate_ready_for_human_review_only",
}

ADDITIONAL_UNSAFE_FIELDS = {
    "approval_request_dry_run_completion_attestation_review_gate_executed",
    "approval_request_dry_run_completion_attestation_review_gate_execution_authorized",
    "completion_attestation_review_gate_executed",
    "completion_attestation_review_gate_execution_authorized",
    "dry_run_completion_attestation_review_gate_executed",
    "dry_run_completion_attestation_review_gate_execution_authorized",
}

APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_REVIEW_GATE_FALSE_FLAGS = {
    **SOURCE_COMPLETION_ATTESTATION_PROPOSAL_FALSE_FLAGS,
    **{key: False for key in sorted(ADDITIONAL_UNSAFE_FIELDS)},
}
APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_REVIEW_GATE_OBJECT_FALSE_FLAGS = {
    **SOURCE_COMPLETION_ATTESTATION_PROPOSAL_OBJECT_FALSE_FLAGS,
    **APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_REVIEW_GATE_FALSE_FLAGS,
}
UNSAFE_TRUE_FIELDS = set(
    APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_REVIEW_GATE_OBJECT_FALSE_FLAGS
)

FORBIDDEN_BOUNDARY_CLAIMS = (
    *SOURCE_FORBIDDEN_BOUNDARY_CLAIMS,
    "completion attestation review gate is executed",
    "completion attestation review gate execution is authorized",
    "dry-run completion attestation review gate is executed",
    "dry-run completion attestation review gate execution is authorized",
    "completion attestation approval proposal is executed",
)

APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_REVIEW_GATE_COMPONENT_KEYS = {
    "source_star_soul_continuity_boundary_approval_request_dry_run_completion_attestation_proposal",
    "completion_attestation_structural_review_boundary",
    "completion_attestation_non_execution_boundary",
    "completion_attestation_non_finalization_boundary",
    "completion_attestation_non_closure_boundary",
    "dry_run_execution_non_execution_boundary",
    "dry_run_plan_non_execution_boundary",
    "approval_request_non_creation_boundary",
    "approval_request_non_submission_boundary",
    "approval_request_non_execution_boundary",
    "approval_grant_non_authorization_boundary",
    "real_human_decision_non_recording_boundary",
    "star_soul_continuity_non_execution_boundary",
    "star_soul_continuity_non_authorization_boundary",
    "star_soul_continuity_non_recording_boundary",
    "star_soul_continuity_non_ledger_boundary",
    "autonomous_identity_non_creation_boundary",
    "identity_awakening_non_execution_boundary",
    "personality_awakening_non_execution_boundary",
    "soul_awakening_non_execution_boundary",
    "consciousness_claim_non_authorization_boundary",
    "self_awareness_claim_non_authorization_boundary",
    "personhood_claim_non_authorization_boundary",
    "sentience_claim_non_authorization_boundary",
    "autonomous_self_model_non_execution_boundary",
    "memory_write_non_authorization_boundary",
    "memory_graph_mutation_non_authorization_boundary",
    "operation_ledger_non_creation_boundary",
    "openclaw_execution_non_authorization_boundary",
    "github_api_non_execution_boundary",
    "handoff_non_authorization_boundary",
    "scheduling_non_authorization_boundary",
    "civilization_core_completion_non_claim_boundary",
    "star_cosmos_entry_non_authorization_boundary",
    "star_source_entry_non_authorization_boundary",
    "evidence_lineage_completion_attestation_review_boundary",
    "false_approval_prevention_completion_attestation_review_boundary",
    "rollback_completion_attestation_review_boundary",
    "suspension_completion_attestation_review_boundary",
    "human_operator_final_authority_completion_attestation_review_boundary",
    "thirteen_memory_layer_boundary",
    "fifteen_memory_layers_boundary",
}


def build_governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_review_gate(
    star_soul_approval_request_dry_run_completion_attestation_proposal_report: Mapping[
        str, Any
    ],
) -> dict[str, Any]:
    """Return a deterministic local-only completion attestation review gate."""

    checks, blocking_reasons = (
        _approval_request_dry_run_completion_attestation_review_gate_checks(
            star_soul_approval_request_dry_run_completion_attestation_proposal_report
        )
    )
    sensitive_field_count = _count_sensitive_keys(
        star_soul_approval_request_dry_run_completion_attestation_proposal_report
    )
    blocking_reasons = list(dict.fromkeys(blocking_reasons))
    ready = not blocking_reasons

    return {
        "version": GOVERNED_STAR_SOUL_MEMORY_CONTINUITY_BOUNDARY_APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_REVIEW_GATE_VERSION,
        "status": (
            "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_review_gate_ready"
            if ready
            else "blocked"
        ),
        "read_only": True,
        "read_only_memory": True,
        "review_gate_only": True,
        "completion_attestation_review_gate_only": True,
        "dry_run_completion_attestation_review_gate_only": True,
        "approval_request_dry_run_completion_attestation_review_gate_only": True,
        "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_review_gate_only": True,
        "thirteenth_memory_layer_star_soul_boundary_approval_request_dry_run_completion_attestation_review_gate_only": True,
        **APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_REVIEW_GATE_FALSE_FLAGS,
        "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_reviewed_for_human_review_only": ready,
        "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_proposal_ready_for_human_review_only": ready,
        "civilization_core_layer_mapping": dict(LAYER_MAPPING),
        "source_star_soul_approval_request_dry_run_completion_attestation_review_source_version": SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_REVIEW_SOURCE_VERSION,
        "source_star_soul_approval_request_dry_run_completion_attestation_proposal_version": SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_PROPOSAL_VERSION,
        "source_star_soul_approval_request_dry_run_execution_review_gate_version": SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_EXECUTION_REVIEW_GATE_VERSION,
        "source_star_soul_approval_request_dry_run_execution_proposal_version": SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_EXECUTION_PROPOSAL_VERSION,
        "source_star_soul_approval_request_dry_run_review_gate_version": SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_REVIEW_GATE_VERSION,
        "source_star_soul_approval_request_dry_run_proposal_version": SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_PROPOSAL_VERSION,
        "source_reviewed_chain_versions": list(SOURCE_REVIEWED_CHAIN_VERSIONS),
        "source_reviewed_star_hub_chain_versions": list(
            SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS
        ),
        "source_proposed_dry_run_chain_versions": list(
            SOURCE_PROPOSED_DRY_RUN_CHAIN_VERSIONS
        ),
        "source_proposed_dry_run_star_hub_chain_versions": list(
            SOURCE_PROPOSED_DRY_RUN_STAR_HUB_CHAIN_VERSIONS
        ),
        "source_reviewed_dry_run_chain_versions": list(
            SOURCE_REVIEWED_DRY_RUN_CHAIN_VERSIONS
        ),
        "source_reviewed_dry_run_star_hub_chain_versions": list(
            SOURCE_REVIEWED_DRY_RUN_STAR_HUB_CHAIN_VERSIONS
        ),
        "source_proposed_dry_run_execution_chain_versions": list(
            SOURCE_PROPOSED_DRY_RUN_EXECUTION_CHAIN_VERSIONS
        ),
        "source_proposed_dry_run_execution_star_hub_chain_versions": list(
            SOURCE_PROPOSED_DRY_RUN_EXECUTION_STAR_HUB_CHAIN_VERSIONS
        ),
        "source_reviewed_dry_run_execution_chain_versions": list(
            SOURCE_REVIEWED_DRY_RUN_EXECUTION_CHAIN_VERSIONS
        ),
        "source_reviewed_dry_run_execution_star_hub_chain_versions": list(
            SOURCE_REVIEWED_DRY_RUN_EXECUTION_STAR_HUB_CHAIN_VERSIONS
        ),
        "source_proposed_dry_run_completion_attestation_chain_versions": list(
            SOURCE_PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_CHAIN_VERSIONS
        ),
        "source_proposed_dry_run_completion_attestation_star_hub_chain_versions": list(
            SOURCE_PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_STAR_HUB_CHAIN_VERSIONS
        ),
        "reviewed_dry_run_completion_attestation_chain_versions": list(
            REVIEWED_DRY_RUN_COMPLETION_ATTESTATION_CHAIN_VERSIONS
        ),
        "reviewed_dry_run_completion_attestation_star_hub_chain_versions": list(
            REVIEWED_DRY_RUN_COMPLETION_ATTESTATION_STAR_HUB_CHAIN_VERSIONS
        ),
        "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_review_gate_summary": _review_gate_summary(
            ready
        ),
        "approval_request_dry_run_completion_attestation_review_gate_checks": checks,
        "source_star_soul_approval_request_dry_run_completion_attestation_proposal_summary": _source_summary(
            ready
        ),
        "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_review_gate": _review_gate(
            ready
        ),
        "reviewed_star_soul_memory_continuity_approval_request_dry_run_completion_attestation_boundaries": _review_gate_components(
            ready
        ),
        "non_authorization_boundary": _non_authorization_boundary(ready),
        "non_execution_boundary": _non_execution_boundary(ready),
        "preserved_governance_boundaries": _preserved_governance_boundaries(),
        "thirteenth_memory_layer_boundary": _thirteenth_memory_layer_boundary(
            ready
        ),
        "future_star_soul_memory_continuity_approval_request_dry_run_completion_attestation_approval_proposal_constraints": _future_approval_proposal_constraints(),
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


def governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_review_gate_to_json(
    report: Mapping[str, Any],
) -> str:
    """Serialize the completion attestation review gate deterministically."""

    return json.dumps(
        dict(report), ensure_ascii=True, indent=2, sort_keys=True
    ) + "\n"


def _approval_request_dry_run_completion_attestation_review_gate_checks(
    report: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    blocking_reasons: list[str] = []

    if not isinstance(report, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_completion_attestation_proposal_mapping",
            False,
            "source_star_soul_approval_request_dry_run_completion_attestation_proposal_report_must_be_mapping",
        )
        return checks, blocking_reasons

    requirements = {
        "version": SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_PROPOSAL_VERSION,
        "status": "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposal_ready",
        "source_star_soul_approval_request_dry_run_completion_attestation_source_version": SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_EXECUTION_REVIEW_GATE_VERSION,
        "source_star_soul_approval_request_dry_run_execution_review_gate_version": SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_EXECUTION_REVIEW_GATE_VERSION,
        "source_star_soul_approval_request_dry_run_execution_proposal_version": SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_EXECUTION_PROPOSAL_VERSION,
        "source_star_soul_approval_request_dry_run_review_gate_version": SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_REVIEW_GATE_VERSION,
        "source_star_soul_approval_request_dry_run_proposal_version": SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_PROPOSAL_VERSION,
        "next_allowed_step": "v3.11.0 Star-Soul Memory continuity boundary approval request dry-run completion attestation review gate",
        "blocking_reasons": [],
    }
    for key, expected in requirements.items():
        _add_check(
            checks,
            blocking_reasons,
            f"source_{key}",
            report.get(key) == expected,
            f"source_{key}_must_match_v3_10_0_completion_attestation_proposal",
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
            for key, expected in SOURCE_COMPLETION_ATTESTATION_PROPOSAL_FALSE_FLAGS.items()
        ),
        "source_star_soul_approval_request_dry_run_completion_attestation_proposal_all_required_unsafe_flags_must_be_false",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_no_unsafe_true_claims",
        _unsafe_true_fields(report) == [],
        "source_star_soul_approval_request_dry_run_completion_attestation_proposal_must_not_claim_unsafe_execution_authorization_recording_ledger_audit_response_correction_enforcement_rule_autonomous_handoff_scheduling_approval_write_continuity_identity_consciousness_or_later_layer_actions",
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_no_unsafe_text_claims",
        _unsafe_text_claims(report) == [],
        "source_star_soul_approval_request_dry_run_completion_attestation_proposal_must_not_textually_claim_unsafe_execution_authorization_recording_approval_continuity_identity_consciousness_write_or_later_layer_actions",
    )

    chain_requirements = {
        "source_reviewed_chain_versions": SOURCE_REVIEWED_CHAIN_VERSIONS,
        "source_reviewed_star_hub_chain_versions": SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS,
        "source_proposed_dry_run_chain_versions": SOURCE_PROPOSED_DRY_RUN_CHAIN_VERSIONS,
        "source_proposed_dry_run_star_hub_chain_versions": SOURCE_PROPOSED_DRY_RUN_STAR_HUB_CHAIN_VERSIONS,
        "source_reviewed_dry_run_chain_versions": SOURCE_REVIEWED_DRY_RUN_CHAIN_VERSIONS,
        "source_reviewed_dry_run_star_hub_chain_versions": SOURCE_REVIEWED_DRY_RUN_STAR_HUB_CHAIN_VERSIONS,
        "source_proposed_dry_run_execution_chain_versions": SOURCE_PROPOSED_DRY_RUN_EXECUTION_CHAIN_VERSIONS,
        "source_proposed_dry_run_execution_star_hub_chain_versions": SOURCE_PROPOSED_DRY_RUN_EXECUTION_STAR_HUB_CHAIN_VERSIONS,
        "source_reviewed_dry_run_execution_chain_versions": SOURCE_REVIEWED_DRY_RUN_EXECUTION_CHAIN_VERSIONS,
        "source_reviewed_dry_run_execution_star_hub_chain_versions": SOURCE_REVIEWED_DRY_RUN_EXECUTION_STAR_HUB_CHAIN_VERSIONS,
        "proposed_dry_run_completion_attestation_chain_versions": SOURCE_PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_CHAIN_VERSIONS,
        "proposed_dry_run_completion_attestation_star_hub_chain_versions": SOURCE_PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_STAR_HUB_CHAIN_VERSIONS,
    }
    for key, expected in chain_requirements.items():
        _add_check(
            checks,
            blocking_reasons,
            f"source_{key}",
            report.get(key) == expected,
            f"source_{key}_must_exactly_match_expected_v3_10_0_lineage",
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
            "hard_boundary": "v3.10.0 proposes approval request dry-run completion attestation boundaries for human review only and does not execute dry-run, execute dry-run plan, execute completion, execute attestation, finalize, close, create, submit, execute, grant, record approval, or record real human decisions",
        }
        for key, expected in mapping_requirements.items():
            _add_check(
                checks,
                blocking_reasons,
                f"source_layer_mapping_{key}",
                mapping.get(key) == expected,
                f"source_layer_mapping_{key}_must_match_v3_10_0",
            )

    proposal = report.get(
        "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposal"
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_nested_completion_attestation_proposal_shape",
        isinstance(proposal, Mapping),
        "source_nested_star_soul_approval_request_dry_run_completion_attestation_proposal_must_be_mapping",
    )
    if isinstance(proposal, Mapping):
        nested_requirements = {
            "proposal_status": "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposed_for_human_review_only",
            "boundary_type": "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposal",
            "source_star_soul_approval_request_dry_run_execution_review_gate_version": SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_EXECUTION_REVIEW_GATE_VERSION,
            "source_star_soul_memory_continuity_boundary_approval_request_dry_run_execution_review_gate_valid": True,
            "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposed": True,
            "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_structurally_proposed_for_human_review_only": True,
            "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_review_gate_ready_for_human_review_only": True,
            "thirteenth_memory_layer_star_soul_boundary_approval_request_dry_run_completion_attestation_proposed_for_human_review_only": True,
            "proposed_dry_run_completion_attestation_chain_versions": SOURCE_PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_CHAIN_VERSIONS,
            "proposed_dry_run_completion_attestation_star_hub_chain_versions": SOURCE_PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_STAR_HUB_CHAIN_VERSIONS,
        }
        for key, expected in nested_requirements.items():
            _add_check(
                checks,
                blocking_reasons,
                f"source_nested_completion_attestation_proposal_{key}",
                proposal.get(key) == expected,
                f"source_nested_completion_attestation_proposal_{key}_must_match",
            )
        _add_check(
            checks,
            blocking_reasons,
            "source_nested_completion_attestation_proposal_unsafe_flags_false",
            all(
                proposal.get(key) is expected
                for key, expected in SOURCE_COMPLETION_ATTESTATION_PROPOSAL_OBJECT_FALSE_FLAGS.items()
            ),
            "source_nested_completion_attestation_proposal_all_required_unsafe_flags_must_be_false",
        )
        _add_check(
            checks,
            blocking_reasons,
            "source_nested_completion_attestation_proposal_no_unsafe_claims",
            not _unsafe_true_fields(proposal)
            and not _unsafe_text_claims(proposal),
            "source_nested_completion_attestation_proposal_must_remain_non_authorizing_and_non_executing",
        )

    boundaries = report.get(
        "proposed_star_soul_memory_continuity_approval_request_dry_run_completion_attestation_boundaries"
    )
    _add_check(
        checks,
        blocking_reasons,
        "source_proposed_completion_attestation_boundaries_shape",
        isinstance(boundaries, Mapping),
        "source_proposed_star_soul_approval_request_dry_run_completion_attestation_boundaries_must_be_mapping",
    )
    if isinstance(boundaries, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "source_proposed_completion_attestation_boundaries_proposal_only_non_executing",
            _proposed_completion_attestation_boundaries_remain_proposal_only(
                boundaries
            ),
            "source_proposed_star_soul_approval_request_dry_run_completion_attestation_boundaries_must_remain_proposal_only_non_authorizing_and_non_executing",
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
            "boundary_approval_request_dry_run_completion_attestation_proposal_only": True,
            "enters_star_soul_layer": False,
            "star_soul_continuity_executed": False,
            "star_soul_continuity_authorized": False,
            "approval_request_created": False,
            "approval_request_submitted": False,
            "approval_request_executed": False,
            "approval_granted": False,
            "real_human_decision_recorded": False,
            "dry_run_executed": False,
            "dry_run_plan_executed": False,
            "completion_executed": False,
            "attestation_executed": False,
            "finalization_executed": False,
            "closure_executed": False,
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
            "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_reviewed_for_human_review_only"
            if ready
            else "blocked"
        ),
        "source_star_soul_approval_request_dry_run_completion_attestation_proposal_version": SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_PROPOSAL_VERSION,
        "source_star_soul_approval_request_dry_run_completion_attestation_proposal_valid": ready,
        "approval_request_dry_run_completion_attestation_review_gate_only": True,
        "human_review_only": True,
        "non_authorizing": True,
        "non_executing": True,
        "non_finalizing": True,
        "non_closing": True,
        "dry_run_executed": False,
        "dry_run_plan_executed": False,
        "completion_executed": False,
        "attestation_executed": False,
        "approval_request_created": False,
        "approval_request_submitted": False,
        "approval_request_executed": False,
        "approval_granted": False,
        "real_human_decision_recorded": False,
        "civilization_core_complete_claimed": False,
    }


def _source_summary(ready: bool) -> dict[str, Any]:
    return {
        "source_star_soul_approval_request_dry_run_completion_attestation_proposal_version": SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_PROPOSAL_VERSION,
        "source_star_soul_approval_request_dry_run_completion_attestation_proposal_status": (
            "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposal_ready"
            if ready
            else "blocked"
        ),
        "source_proposed_dry_run_completion_attestation_chain_versions": list(
            SOURCE_PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_CHAIN_VERSIONS
        ),
        "source_proposed_dry_run_completion_attestation_star_hub_chain_versions": list(
            SOURCE_PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_STAR_HUB_CHAIN_VERSIONS
        ),
        "source_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposal_valid": ready,
        "source_completion_attestation_proposal_executed_dry_run": False,
        "source_completion_attestation_proposal_executed_dry_run_plan": False,
        "source_completion_attestation_proposal_executed_completion": False,
        "source_completion_attestation_proposal_executed_attestation": False,
        "source_completion_attestation_proposal_finalized": False,
        "source_completion_attestation_proposal_closed": False,
        "source_completion_attestation_proposal_created_approval_request": False,
        "source_completion_attestation_proposal_submitted_approval_request": False,
        "source_completion_attestation_proposal_executed_approval_request": False,
        "source_completion_attestation_proposal_granted_approval": False,
        "source_completion_attestation_proposal_recorded_real_human_decision": False,
        "source_completion_attestation_proposal_authorized_star_soul_continuity": False,
        "source_completion_attestation_proposal_authorized_memory_write": False,
        "source_completion_attestation_proposal_authorized_openclaw_execution": False,
        "raw_source_completion_attestation_proposal_copied": False,
    }


def _review_gate(ready: bool) -> dict[str, Any]:
    return {
        "review_status": (
            "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_reviewed_for_human_review_only"
            if ready
            else "blocked_no_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_review_readiness_claim"
        ),
        "boundary_type": "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_review_gate",
        "source_star_soul_approval_request_dry_run_completion_attestation_proposal_version": SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_PROPOSAL_VERSION,
        "source_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposal_valid": ready,
        "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_reviewed": ready,
        "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_structurally_review_ready": ready,
        "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_proposal_ready_for_human_review_only": ready,
        "thirteenth_memory_layer_star_soul_boundary_approval_request_dry_run_completion_attestation_reviewed_for_human_review_only": ready,
        **APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_REVIEW_GATE_OBJECT_FALSE_FLAGS,
        "reviewed_dry_run_completion_attestation_chain_versions": list(
            REVIEWED_DRY_RUN_COMPLETION_ATTESTATION_CHAIN_VERSIONS
        ),
        "reviewed_dry_run_completion_attestation_star_hub_chain_versions": list(
            REVIEWED_DRY_RUN_COMPLETION_ATTESTATION_STAR_HUB_CHAIN_VERSIONS
        ),
        "reviewed_dry_run_completion_attestation_boundary_components": _review_gate_components(
            ready
        ),
        "next_allowed_step": READY_NEXT_ALLOWED_STEP,
        "non_authorization_notice": (
            "This sanitized v3.11.0 review gate grants no approval, continuity, identity, consciousness, execution, authorization, recording, ledger, write, handoff, scheduling, finalization, closure, or autonomous authority."
            if ready
            else "The Star-Soul Memory continuity boundary approval request dry-run completion attestation review gate is blocked and grants no approval, continuity, identity, consciousness, execution, authorization, recording, ledger, write, handoff, scheduling, finalization, closure, or autonomous authority."
        ),
        "non_execution_notice": "This review gate structurally reviews a completion attestation proposal for human review only. It executes no dry-run, dry-run plan, completion, attestation, finalization, closure, approval request, continuity action, autonomous self-model, write, handoff, scheduling, OpenClaw action, or GitHub API action.",
    }


def _review_gate_components(
    ready: bool,
) -> dict[str, dict[str, Any]]:
    status = "reviewed_for_human_review_only" if ready else "blocked"
    return {
        key: {
            "review_only": True,
            "completion_attestation_review_gate_only": True,
            "dry_run_completion_attestation_review_gate_only": True,
            "approval_request_dry_run_completion_attestation_review_gate_only": True,
            "human_review_only": True,
            "non_authorizing": True,
            "non_executing": True,
            "non_finalizing": True,
            "non_closing": True,
            "boundary_status": status,
            "summary": "This sanitized boundary structurally reviews only the limits of a dry-run completion attestation proposal for human review.",
            "raw_source_boundary_copied": False,
            **APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_REVIEW_GATE_FALSE_FLAGS,
        }
        for key in sorted(
            APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_REVIEW_GATE_COMPONENT_KEYS
        )
    }


def _non_authorization_boundary(ready: bool) -> dict[str, Any]:
    return {
        "completion_attestation_review_gate_ready_is_real_approval": False,
        "completion_attestation_review_gate_ready_is_dry_run_authorization": False,
        "completion_attestation_review_gate_ready_is_dry_run_plan_authorization": False,
        "completion_attestation_review_gate_ready_is_completion_authorization": False,
        "completion_attestation_review_gate_ready_is_attestation_authorization": False,
        "completion_attestation_review_gate_ready_is_finalization_or_closure_authorization": False,
        "completion_attestation_review_gate_ready_is_approval_request_creation": False,
        "completion_attestation_review_gate_ready_is_approval_request_submission": False,
        "completion_attestation_review_gate_ready_is_approval_request_execution": False,
        "completion_attestation_review_gate_ready_is_approval_grant": False,
        "completion_attestation_review_gate_ready_is_real_human_decision_recording": False,
        "completion_attestation_review_gate_ready_is_star_soul_continuity_authorization": False,
        "completion_attestation_review_gate_ready_is_identity_or_self_model_authorization": False,
        "completion_attestation_review_gate_ready_is_memory_write_or_graph_mutation": False,
        "completion_attestation_review_gate_ready_is_operation_ledger_creation": False,
        "completion_attestation_review_gate_ready_is_openclaw_or_github_authorization": False,
        "completion_attestation_review_gate_ready_is_handoff_or_scheduling_authorization": False,
        "completion_attestation_review_gate_ready_is_civilization_core_completion": False,
        "completion_attestation_review_gate_ready_is_star_soul_star_cosmos_or_star_source_entry": False,
        "only_permits_later_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_proposal": ready,
        "human_operator_remains_final_authority": True,
    }


def _non_execution_boundary(ready: bool) -> dict[str, Any]:
    return {
        "completion_attestation_review_gate_ready_is_dry_run_execution": False,
        "completion_attestation_review_gate_ready_is_dry_run_plan_execution": False,
        "completion_attestation_review_gate_ready_is_completion_execution": False,
        "completion_attestation_review_gate_ready_is_attestation_execution": False,
        "completion_attestation_review_gate_ready_is_finalization_execution": False,
        "completion_attestation_review_gate_ready_is_closure_execution": False,
        "completion_attestation_review_gate_ready_is_approval_request_execution": False,
        "completion_attestation_review_gate_ready_is_star_soul_continuity_execution": False,
        "completion_attestation_review_gate_ready_is_continuity_record_or_ledger_creation": False,
        "completion_attestation_review_gate_ready_is_identity_personality_or_soul_awakening": False,
        "completion_attestation_review_gate_ready_is_autonomous_self_model_execution": False,
        "completion_attestation_review_gate_ready_is_audit_response_correction_enforcement_rule_or_autonomous_execution": False,
        "completion_attestation_review_gate_ready_is_write_handoff_scheduling_or_external_execution": False,
        "later_completion_attestation_approval_proposal_may_be_considered": ready,
    }


def _preserved_governance_boundaries() -> list[str]:
    return [
        "This completion attestation review gate does not execute a dry-run or a dry-run plan.",
        "This completion attestation review gate does not execute completion, attestation, finalization, or closure.",
        "This completion attestation review gate does not create, submit, execute, or grant an approval request.",
        "This completion attestation review gate does not approve anything or record a real Human Operator decision.",
        "This completion attestation review gate does not execute or authorize Star-Soul continuity.",
        "This completion attestation review gate does not create Star-Soul continuity records or continuity-ledger entries.",
        "This completion attestation review gate does not create or activate a persistent autonomous identity.",
        "This completion attestation review gate does not perform identity, personality, or soul awakening.",
        "This completion attestation review gate makes no consciousness, self-awareness, personhood, or sentience claim.",
        "This completion attestation review gate does not execute or authorize an autonomous self-model.",
        "This completion attestation review gate does not execute audit, response, correction, enforcement, or rules.",
        "This completion attestation review gate does not create autonomous governance or authorize autonomous execution.",
        "This completion attestation review gate does not authorize handoff or scheduling.",
        "This completion attestation review gate does not write durable memory, mutate Memory Graph, create operation-ledger entries, or call OpenClaw or GitHub APIs.",
        "This completion attestation review gate does not claim Civilization Core completion, mature 星魂 continuity, 星宙 evolution, or 星源 self-evolution.",
        "Human Operator remains final authority.",
    ]


def _thirteenth_memory_layer_boundary(ready: bool) -> dict[str, Any]:
    return {
        "memory_layer": "星魂记忆",
        "memory_layer_number": 13,
        "boundary_approval_request_dry_run_completion_attestation_review_gate_only": True,
        "approval_request_dry_run_completion_attestation_reviewed_for_human_review_only": ready,
        "enters_thirteenth_memory_layer": False,
        "thirteenth_memory_layer_transition_authorized": False,
        **APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_REVIEW_GATE_FALSE_FLAGS,
        "boundary_notice": "v3.11.0 reviews only approval request dry-run completion attestation proposal boundaries for the 13th memory layer. A later separate v3.12.0 approval proposal is required before any further governed consideration.",
    }


def _future_approval_proposal_constraints() -> list[str]:
    return [
        "A later separate v3.12.0 approval request dry-run completion attestation approval proposal may consume this sanitized review gate through a local governed process.",
        "The later proposal must remain proposal-only and must not execute a dry-run, dry-run plan, completion, attestation, finalization, closure, or approval request.",
        "The later proposal must preserve every non-execution, non-authorization, non-recording, non-ledger, non-write, and non-consciousness boundary.",
        "This review gate records no real Human Operator decision and creates, submits, executes, or approves no approval request.",
        "Any later continuity design must retain false-approval prevention, evidence lineage, auditability, rollback, suspension, and Human Operator final authority.",
    ]


def _next_stage_constraints() -> list[str]:
    return [
        f"The only next allowed step is {READY_NEXT_ALLOWED_STEP}.",
        "v3.11.0 remains a Star-Soul Memory continuity boundary approval request dry-run completion attestation review gate only.",
        "No dry-run, dry-run plan, completion, attestation, finalization, or closure execution occurs.",
        "No approval request creation, submission, execution, grant, approval, or real human decision recording occurs.",
        "No Star-Soul continuity execution, authorization, record, ledger, identity creation, awakening, consciousness claim, self-model execution, write, handoff, or scheduling occurs.",
        "No entry into mature 星魂 continuity, 星宙 evolution, or 星源 self-evolution occurs.",
    ]


def _scope_boundaries() -> list[str]:
    return [
        "Civilization Core is the total system.",
        "Fifteen Memory Layers are the highest memory coordinate system.",
        "Subspace Memory System is the engineering carrier.",
        "Hermes, Codex CLI, OpenClaw, Terminal, and GitHub are components, not the core.",
        "This v3.11.0 step is limited to the 星魂记忆 continuity boundary approval request dry-run completion attestation review gate.",
    ]


def _risk_notes(sensitive_field_count: int) -> list[str]:
    notes = [
        "Dry-run completion attestation review-gate readiness must not be interpreted as dry-run execution, dry-run plan execution, completion, attestation, finalization, closure, approval, approval request creation, submission, execution, grant, or real human decision recording.",
        "False continuity, inferred identity, persona drift, unsupported memory lineage, false attestation, and false approval remain explicit risks for later human review.",
        "The report is deterministic, local-only, read-only, and contains sanitized structural summaries rather than raw source completion attestation proposal data.",
        "Civilization Core completion and later memory-layer entry are not claimed.",
    ]
    if sensitive_field_count:
        notes.append("Sensitive fields were omitted from completion attestation review gate output.")
    return notes


def _required_human_actions(
    ready: bool, blocking_reasons: list[str]
) -> list[str]:
    if ready:
        return [
            "human_operator_must_review_v3_11_0_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_review_gate_before_any_v3_12_0_approval_proposal",
            "human_operator_must_confirm_completion_attestation_review_gate_readiness_grants_no_approval_continuity_identity_consciousness_execution_authorization_recording_ledger_write_handoff_scheduling_finalization_closure_or_autonomous_authority",
            "human_operator_must_use_a_separate_governed_process_for_v3_12_0_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_proposal",
        ]
    actions = [
        "repair_source_v3_10_0_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposal_before_review_gate_can_continue",
        "confirm_all_unsafe_approval_continuity_identity_consciousness_execution_authorization_recording_ledger_audit_response_correction_enforcement_rule_write_handoff_scheduling_dry_run_completion_attestation_finalization_closure_and_later_layer_flags_remain_false",
        "rerun_local_v3_11_0_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_review_gate_after_blockers_are_resolved",
    ]
    if blocking_reasons:
        actions.append(
            "resolve_blocking_reasons_before_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_review_gate_can_be_ready"
        )
    return actions


def _proposed_completion_attestation_boundaries_remain_proposal_only(
    boundaries: Mapping[str, Any],
) -> bool:
    for boundary in boundaries.values():
        if not isinstance(boundary, Mapping):
            return False
        if boundary.get("proposal_only") is not True:
            return False
        if boundary.get("completion_attestation_proposal_only") is not True:
            return False
        if boundary.get("dry_run_completion_attestation_proposal_only") is not True:
            return False
        if (
            boundary.get(
                "approval_request_dry_run_completion_attestation_proposal_only"
            )
            is not True
        ):
            return False
        if boundary.get("human_review_only") is not True:
            return False
        if boundary.get("non_authorizing") is not True:
            return False
        if boundary.get("non_executing") is not True:
            return False
        if boundary.get("non_finalizing") is not True:
            return False
        if boundary.get("non_closing") is not True:
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
    "GOVERNED_STAR_SOUL_MEMORY_CONTINUITY_BOUNDARY_APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_REVIEW_GATE_VERSION",
    "SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_REVIEW_SOURCE_VERSION",
    "SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_PROPOSAL_VERSION",
    "SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_EXECUTION_REVIEW_GATE_VERSION",
    "SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_EXECUTION_PROPOSAL_VERSION",
    "SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_REVIEW_GATE_VERSION",
    "SOURCE_STAR_SOUL_APPROVAL_REQUEST_DRY_RUN_PROPOSAL_VERSION",
    "SOURCE_REVIEWED_CHAIN_VERSIONS",
    "SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS",
    "SOURCE_PROPOSED_DRY_RUN_CHAIN_VERSIONS",
    "SOURCE_PROPOSED_DRY_RUN_STAR_HUB_CHAIN_VERSIONS",
    "SOURCE_REVIEWED_DRY_RUN_CHAIN_VERSIONS",
    "SOURCE_REVIEWED_DRY_RUN_STAR_HUB_CHAIN_VERSIONS",
    "SOURCE_PROPOSED_DRY_RUN_EXECUTION_CHAIN_VERSIONS",
    "SOURCE_PROPOSED_DRY_RUN_EXECUTION_STAR_HUB_CHAIN_VERSIONS",
    "SOURCE_REVIEWED_DRY_RUN_EXECUTION_CHAIN_VERSIONS",
    "SOURCE_REVIEWED_DRY_RUN_EXECUTION_STAR_HUB_CHAIN_VERSIONS",
    "SOURCE_PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_CHAIN_VERSIONS",
    "SOURCE_PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_STAR_HUB_CHAIN_VERSIONS",
    "REVIEWED_DRY_RUN_COMPLETION_ATTESTATION_CHAIN_VERSIONS",
    "REVIEWED_DRY_RUN_COMPLETION_ATTESTATION_STAR_HUB_CHAIN_VERSIONS",
    "READY_NEXT_ALLOWED_STEP",
    "LAYER_MAPPING",
    "APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_REVIEW_GATE_FALSE_FLAGS",
    "APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_REVIEW_GATE_OBJECT_FALSE_FLAGS",
    "APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_REVIEW_GATE_COMPONENT_KEYS",
    "SENSITIVE_KEYS",
    "build_governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_review_gate",
    "governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_review_gate_to_json",
]
