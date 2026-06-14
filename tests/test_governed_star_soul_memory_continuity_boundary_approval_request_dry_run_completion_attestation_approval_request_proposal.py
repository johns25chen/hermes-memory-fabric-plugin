from __future__ import annotations

from copy import deepcopy
import json

import pytest

from hermes_memory_fabric.governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_request_proposal import (
    APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_REQUEST_PROPOSAL_COMPONENT_KEYS,
    APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_REQUEST_PROPOSAL_FALSE_FLAGS,
    APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_REQUEST_PROPOSAL_OBJECT_FALSE_FLAGS,
    LAYER_MAPPING,
    PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_REQUEST_CHAIN_VERSIONS,
    PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_REQUEST_STAR_HUB_CHAIN_VERSIONS,
    READY_NEXT_ALLOWED_STEP,
    SENSITIVE_KEYS,
    build_governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_request_proposal,
    governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_request_proposal_to_json,
)
from tests.test_governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_review_gate import (
    _build as _valid_v3_13_approval_review_gate,
)


_BASE_SOURCE_REPORT = _valid_v3_13_approval_review_gate()


def _valid_source_report() -> dict[str, object]:
    return deepcopy(_BASE_SOURCE_REPORT)


def _build(
    report: dict[str, object] | None = None,
) -> dict[str, object]:
    return build_governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_request_proposal(
        _valid_source_report() if report is None else report
    )


def test_valid_v3_13_approval_review_gate_creates_v3_14_approval_request_proposal_ready():
    result = _build()

    assert result["version"] == "3.14.0"
    assert (
        result["status"]
        == "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_request_proposal_ready"
    )
    for field in [
        "read_only",
        "read_only_memory",
        "proposal_only",
        "request_proposal_only",
        "approval_request_proposal_only",
        "completion_attestation_approval_request_proposal_only",
        "dry_run_completion_attestation_approval_request_proposal_only",
        "approval_request_dry_run_completion_attestation_approval_request_proposal_only",
        "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_request_proposal_only",
        "thirteenth_memory_layer_star_soul_boundary_approval_request_dry_run_completion_attestation_approval_request_proposal_only",
        "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_request_proposed_for_human_review_only",
        "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_request_review_gate_ready_for_human_review_only",
    ]:
        assert result[field] is True
    assert result["blocking_reasons"] == []
    assert all(
        check["passed"] is True
        for check in result[
            "approval_request_dry_run_completion_attestation_approval_request_proposal_checks"
        ]
    )
    proposal = result[
        "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_request_proposal"
    ]
    assert (
        proposal["proposal_status"]
        == "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_request_proposed_for_human_review_only"
    )
    assert (
        proposal["boundary_type"]
        == "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_request_proposal"
    )
    assert (
        proposal[
            "source_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_review_gate_valid"
        ]
        is True
    )
    assert (
        proposal[
            "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_request_structurally_proposed_for_human_review_only"
        ]
        is True
    )


def test_lineage_versions_are_exact():
    expected = [
        *[f"v2.{minor}.0" for minor in range(9, 61)],
        "v3.0.0",
        "v3.1.0",
        "v3.2.0",
        "v3.4.0",
        "v3.6.0",
        "v3.7.0",
        "v3.8.0",
        "v3.9.0",
        "v3.10.0",
        "v3.11.0",
        "v3.12.0",
        "v3.13.0",
        "v3.14.0",
    ]
    star_hub_expected = [
        *[f"v2.{minor}.0" for minor in range(19, 61)],
        "v3.0.0",
        "v3.1.0",
        "v3.2.0",
        "v3.4.0",
        "v3.6.0",
        "v3.7.0",
        "v3.8.0",
        "v3.9.0",
        "v3.10.0",
        "v3.11.0",
        "v3.12.0",
        "v3.13.0",
        "v3.14.0",
    ]
    result = _build()
    proposal = result[
        "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_request_proposal"
    ]

    assert (
        PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_REQUEST_CHAIN_VERSIONS
        == expected
    )
    assert (
        result[
            "proposed_dry_run_completion_attestation_approval_request_chain_versions"
        ]
        == expected
    )
    assert (
        proposal[
            "proposed_dry_run_completion_attestation_approval_request_chain_versions"
        ]
        == expected
    )
    assert (
        PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_REQUEST_STAR_HUB_CHAIN_VERSIONS
        == star_hub_expected
    )
    assert (
        result[
            "proposed_dry_run_completion_attestation_approval_request_star_hub_chain_versions"
        ]
        == star_hub_expected
    )
    assert (
        proposal[
            "proposed_dry_run_completion_attestation_approval_request_star_hub_chain_versions"
        ]
        == star_hub_expected
    )


def test_blocked_source_blocks_approval_request_proposal():
    report = _valid_source_report()
    report["status"] = "blocked"
    report["blocking_reasons"] = ["blocked_source"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert (
        result[
            "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_request_proposed_for_human_review_only"
        ]
        is False
    )
    assert result["blocking_reasons"]
    assert (
        result[
            "proposed_dry_run_completion_attestation_approval_request_chain_versions"
        ]
        == PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_REQUEST_CHAIN_VERSIONS
    )
    assert result["required_human_actions"]


@pytest.mark.parametrize(
    "field",
    [
        "approval_authorized",
        "approval_request_created",
        "approval_request_submitted",
        "approval_request_executed",
        "actual_approval_request_created",
        "actual_approval_request_submitted",
        "actual_approval_request_executed",
        "approval_granted",
        "approval_executed",
        "real_approval_granted",
        "approval_decision_recorded",
        "real_human_decision_recorded",
        "dry_run_executed",
        "dry_run_plan_executed",
        "completion_executed",
        "attestation_executed",
        "finalization_executed",
        "closure_executed",
        "star_soul_continuity_executed",
        "star_soul_continuity_authorized",
        "star_soul_continuity_record_created",
        "star_soul_continuity_ledger_entry_created",
        "persistent_autonomous_identity_created",
        "consciousness_claimed",
        "self_awareness_claimed",
        "personhood_claimed",
        "sentience_claimed",
        "identity_awakening_performed",
        "personality_awakening_performed",
        "soul_awakening_performed",
        "autonomous_self_model_executed",
        "autonomous_self_model_authorized",
        "audit_executed",
        "audit_logging_performed",
        "violation_response_executed",
        "automated_correction_performed",
        "violation_enforcement_executed",
        "candidate_rule_enforcement_executed",
        "star_law_rules_created",
        "star_law_rules_activated",
        "star_law_rules_enforced",
        "autonomous_governance_created",
        "autonomous_execution_authorized",
        "enters_star_soul_layer",
        "enters_star_cosmos_layer",
        "enters_star_source_layer",
        "civilization_core_complete_claimed",
        "star_hub_handoff_authorized",
        "scheduling_performed",
        "durable_memory_written",
        "memory_graph_mutated",
        "operation_ledger_entry_created",
        "openclaw_called",
        "github_api_called",
    ],
)
def test_unsafe_claim_blocks_approval_request_proposal(field: str):
    report = _valid_source_report()
    report[field] = True

    result = _build(report)

    assert result["status"] == "blocked"
    assert result["blocking_reasons"]
    for unsafe_field in APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_REQUEST_PROPOSAL_FALSE_FLAGS:
        assert result[unsafe_field] is False


def test_nested_unsafe_claim_blocks_approval_request_proposal():
    report = _valid_source_report()
    review_gate = report[
        "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_review_gate"
    ]
    assert isinstance(review_gate, dict)
    review_gate["approval_request_created"] = True

    assert _build(report)["status"] == "blocked"


@pytest.mark.parametrize(
    "field",
    [
        "reviewed_dry_run_completion_attestation_approval_chain_versions",
        "reviewed_dry_run_completion_attestation_approval_star_hub_chain_versions",
    ],
)
def test_malformed_reviewed_approval_lineage_blocks_approval_request_proposal(
    field: str,
):
    report = _valid_source_report()
    report[field] = ["malformed"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert result["blocking_reasons"]


def test_proposed_approval_request_boundaries_are_request_proposal_only():
    result = _build()
    boundaries = result[
        "proposed_star_soul_memory_continuity_approval_request_dry_run_completion_attestation_approval_request_boundaries"
    ]

    assert set(boundaries) >= (
        APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_REQUEST_PROPOSAL_COMPONENT_KEYS
    )
    for boundary in boundaries.values():
        assert boundary["proposal_only"] is True
        assert boundary["request_proposal_only"] is True
        assert boundary["approval_request_proposal_only"] is True
        assert boundary["human_review_only"] is True
        assert boundary["non_authorizing"] is True
        assert boundary["non_executing"] is True
        assert boundary["non_approval_granting"] is True
        assert boundary["non_decision_recording"] is True
        assert boundary["non_request_creating"] is True
        assert boundary["non_request_submitting"] is True
        assert boundary["non_request_executing"] is True
        assert boundary["non_finalizing"] is True
        assert boundary["non_closing"] is True
        assert boundary["boundary_status"] == "proposed_for_human_review_only"
        for field in APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_REQUEST_PROPOSAL_FALSE_FLAGS:
            assert boundary[field] is False


def test_all_unsafe_output_flags_remain_false():
    result = _build()
    proposal = result[
        "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_request_proposal"
    ]

    for field in APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_REQUEST_PROPOSAL_FALSE_FLAGS:
        assert result[field] is False
    for field in APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_REQUEST_PROPOSAL_OBJECT_FALSE_FLAGS:
        assert proposal[field] is False


def test_sensitive_field_names_and_values_are_not_leaked():
    report = _valid_source_report()
    values: list[str] = []
    for index, key in enumerate(sorted(SENSITIVE_KEYS)):
        value = f"hidden-sensitive-value-{index}"
        values.append(value)
        report[key] = value
    report["nested_sensitive"] = {
        "token": "deep-hidden-token",
        "safe": "visible-structure-not-copied",
    }
    values.append("deep-hidden-token")

    serialized = governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_request_proposal_to_json(
        _build(report)
    )

    assert "sensitive fields were omitted" in serialized.lower()
    for key in SENSITIVE_KEYS:
        assert f'"{key}"' not in serialized
    for value in values:
        assert value not in serialized


def test_non_request_boundaries_never_create_submit_execute_or_approve():
    result = _build()

    assert (
        result["non_request_creation_boundary"][
            "approval_request_proposal_ready_creates_approval_request"
        ]
        is False
    )
    assert (
        result["non_request_submission_boundary"][
            "approval_request_proposal_ready_submits_approval_request"
        ]
        is False
    )
    assert (
        result["non_request_execution_boundary"][
            "approval_request_proposal_ready_executes_approval_request"
        ]
        is False
    )
    assert (
        result["non_approval_grant_boundary"][
            "approval_request_proposal_ready_approves_anything"
        ]
        is False
    )
    assert (
        result["non_decision_recording_boundary"][
            "approval_request_proposal_ready_records_real_human_decision"
        ]
        is False
    )


def test_layer_mapping_thirteenth_boundary_and_next_step_are_exact():
    result = _build()

    assert result["civilization_core_layer_mapping"] == LAYER_MAPPING
    assert LAYER_MAPPING["primary_layer"] == "星魂记忆"
    assert LAYER_MAPPING["source_layer"] == "星魂记忆"
    assert (
        LAYER_MAPPING["hard_boundary"]
        == "v3.14.0 proposes approval request boundaries for human review only and does not create, submit, execute, grant, approve, record approval decisions, record real human decisions, execute dry-run, execute dry-run plan, execute completion, execute attestation, finalize, close, authorize continuity, or write memory"
    )
    boundary = result["thirteenth_memory_layer_boundary"]
    assert boundary["memory_layer"] == "星魂记忆"
    assert boundary["memory_layer_number"] == 13
    assert (
        boundary[
            "boundary_approval_request_dry_run_completion_attestation_approval_request_proposal_only"
        ]
        is True
    )
    assert boundary["enters_thirteenth_memory_layer"] is False
    assert boundary["thirteenth_memory_layer_transition_authorized"] is False
    for field in APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_REQUEST_PROPOSAL_FALSE_FLAGS:
        assert boundary[field] is False
    assert result["next_allowed_step"] == READY_NEXT_ALLOWED_STEP
    assert (
        READY_NEXT_ALLOWED_STEP
        == "v3.15.0 Star-Soul Memory continuity boundary approval request dry-run completion attestation approval request review gate"
    )


def test_serialization_is_deterministic():
    first = governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_request_proposal_to_json(
        _build()
    )
    second = governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_request_proposal_to_json(
        _build()
    )

    assert first == second
    assert json.loads(first)["version"] == "3.14.0"
