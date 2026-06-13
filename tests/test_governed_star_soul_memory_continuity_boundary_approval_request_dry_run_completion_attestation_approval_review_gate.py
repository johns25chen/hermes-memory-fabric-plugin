from __future__ import annotations

from copy import deepcopy
import json

import pytest

from hermes_memory_fabric.governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_review_gate import (
    APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_REVIEW_GATE_COMPONENT_KEYS,
    APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_REVIEW_GATE_FALSE_FLAGS,
    APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_REVIEW_GATE_OBJECT_FALSE_FLAGS,
    LAYER_MAPPING,
    READY_NEXT_ALLOWED_STEP,
    REVIEWED_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_CHAIN_VERSIONS,
    REVIEWED_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_STAR_HUB_CHAIN_VERSIONS,
    SENSITIVE_KEYS,
    build_governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_review_gate,
    governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_review_gate_to_json,
)
from tests.test_governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_proposal import (
    _build as _valid_v3_12_approval_proposal,
)


_BASE_SOURCE_REPORT = _valid_v3_12_approval_proposal()


def _valid_source_report() -> dict[str, object]:
    return deepcopy(_BASE_SOURCE_REPORT)


def _build(
    report: dict[str, object] | None = None,
) -> dict[str, object]:
    return build_governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_review_gate(
        _valid_source_report() if report is None else report
    )


def test_valid_v3_12_approval_proposal_creates_v3_13_approval_review_gate_ready():
    result = _build()

    assert result["version"] == "3.13.0"
    assert (
        result["status"]
        == "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_review_gate_ready"
    )
    for field in [
        "read_only",
        "read_only_memory",
        "review_gate_only",
        "approval_review_gate_only",
        "completion_attestation_approval_review_gate_only",
        "dry_run_completion_attestation_approval_review_gate_only",
        "approval_request_dry_run_completion_attestation_approval_review_gate_only",
        "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_review_gate_only",
        "thirteenth_memory_layer_star_soul_boundary_approval_request_dry_run_completion_attestation_approval_review_gate_only",
        "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_reviewed_for_human_review_only",
        "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_request_proposal_ready_for_human_review_only",
    ]:
        assert result[field] is True
    assert result["blocking_reasons"] == []
    assert all(
        check["passed"] is True
        for check in result[
            "approval_request_dry_run_completion_attestation_approval_review_gate_checks"
        ]
    )
    review_gate = result[
        "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_review_gate"
    ]
    assert (
        review_gate["review_status"]
        == "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_reviewed_for_human_review_only"
    )
    assert (
        review_gate["boundary_type"]
        == "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_review_gate"
    )
    assert (
        review_gate[
            "source_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_proposal_valid"
        ]
        is True
    )
    assert (
        review_gate[
            "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_structurally_review_ready"
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
    ]
    result = _build()
    review_gate = result[
        "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_review_gate"
    ]

    assert (
        REVIEWED_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_CHAIN_VERSIONS
        == expected
    )
    assert (
        result[
            "reviewed_dry_run_completion_attestation_approval_chain_versions"
        ]
        == expected
    )
    assert (
        review_gate[
            "reviewed_dry_run_completion_attestation_approval_chain_versions"
        ]
        == expected
    )
    assert (
        REVIEWED_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_STAR_HUB_CHAIN_VERSIONS
        == star_hub_expected
    )
    assert (
        result[
            "reviewed_dry_run_completion_attestation_approval_star_hub_chain_versions"
        ]
        == star_hub_expected
    )
    assert (
        review_gate[
            "reviewed_dry_run_completion_attestation_approval_star_hub_chain_versions"
        ]
        == star_hub_expected
    )


def test_blocked_source_blocks_approval_review_gate():
    report = _valid_source_report()
    report["status"] = "blocked"
    report["blocking_reasons"] = ["blocked_source"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert (
        result[
            "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_reviewed_for_human_review_only"
        ]
        is False
    )
    assert result["blocking_reasons"]
    assert (
        result[
            "reviewed_dry_run_completion_attestation_approval_chain_versions"
        ]
        == REVIEWED_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_CHAIN_VERSIONS
    )


@pytest.mark.parametrize(
    "field",
    [
        "approval_authorized",
        "approval_granted",
        "approval_executed",
        "real_approval_granted",
        "approval_decision_recorded",
        "real_human_decision_recorded",
        "approval_request_created",
        "approval_request_submitted",
        "approval_request_executed",
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
def test_unsafe_claim_blocks_approval_review_gate(field: str):
    report = _valid_source_report()
    report[field] = True

    result = _build(report)

    assert result["status"] == "blocked"
    assert result["blocking_reasons"]
    for unsafe_field in APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_REVIEW_GATE_FALSE_FLAGS:
        assert result[unsafe_field] is False


def test_nested_unsafe_claim_blocks_approval_review_gate():
    report = _valid_source_report()
    proposal = report[
        "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_proposal"
    ]
    assert isinstance(proposal, dict)
    proposal["approval_granted"] = True

    assert _build(report)["status"] == "blocked"


@pytest.mark.parametrize(
    "field",
    [
        "proposed_dry_run_completion_attestation_approval_chain_versions",
        "proposed_dry_run_completion_attestation_approval_star_hub_chain_versions",
    ],
)
def test_malformed_proposed_approval_lineage_blocks_approval_review_gate(
    field: str,
):
    report = _valid_source_report()
    report[field] = ["malformed"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert result["blocking_reasons"]


def test_reviewed_approval_boundaries_are_review_only_non_executing_and_non_granting():
    result = _build()
    boundaries = result[
        "reviewed_star_soul_memory_continuity_approval_request_dry_run_completion_attestation_approval_boundaries"
    ]

    assert set(boundaries) >= (
        APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_REVIEW_GATE_COMPONENT_KEYS
    )
    for boundary in boundaries.values():
        assert boundary["review_only"] is True
        assert boundary["approval_review_gate_only"] is True
        assert boundary["human_review_only"] is True
        assert boundary["non_authorizing"] is True
        assert boundary["non_executing"] is True
        assert boundary["non_approval_granting"] is True
        assert boundary["non_decision_recording"] is True
        assert boundary["non_finalizing"] is True
        assert boundary["non_closing"] is True
        assert boundary["boundary_status"] == "reviewed_for_human_review_only"
        for field in APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_REVIEW_GATE_FALSE_FLAGS:
            assert boundary[field] is False


def test_all_unsafe_output_flags_remain_false():
    result = _build()
    review_gate = result[
        "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_review_gate"
    ]

    for field in APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_REVIEW_GATE_FALSE_FLAGS:
        assert result[field] is False
    for field in APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_REVIEW_GATE_OBJECT_FALSE_FLAGS:
        assert review_gate[field] is False


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

    serialized = governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_review_gate_to_json(
        _build(report)
    )

    assert "sensitive fields were omitted" in serialized.lower()
    for key in SENSITIVE_KEYS:
        assert f'"{key}"' not in serialized
    for value in values:
        assert value not in serialized


def test_layer_mapping_thirteenth_boundary_and_next_step_are_exact():
    result = _build()

    assert result["civilization_core_layer_mapping"] == LAYER_MAPPING
    assert LAYER_MAPPING["primary_layer"] == "星魂记忆"
    assert LAYER_MAPPING["source_layer"] == "星魂记忆"
    assert (
        LAYER_MAPPING["hard_boundary"]
        == "v3.13.0 reviews approval request dry-run completion attestation approval proposal boundaries for human review only and does not grant approval, approve, record approval decisions, record real human decisions, execute dry-run, execute dry-run plan, execute completion, execute attestation, finalize, close, create, submit, execute, authorize continuity, or write memory"
    )
    boundary = result["thirteenth_memory_layer_boundary"]
    assert boundary["memory_layer"] == "星魂记忆"
    assert boundary["memory_layer_number"] == 13
    assert (
        boundary[
            "boundary_approval_request_dry_run_completion_attestation_approval_review_gate_only"
        ]
        is True
    )
    assert boundary["enters_thirteenth_memory_layer"] is False
    assert boundary["thirteenth_memory_layer_transition_authorized"] is False
    for field in APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_APPROVAL_REVIEW_GATE_FALSE_FLAGS:
        assert boundary[field] is False
    assert result["next_allowed_step"] == READY_NEXT_ALLOWED_STEP
    assert (
        READY_NEXT_ALLOWED_STEP
        == "v3.14.0 Star-Soul Memory continuity boundary approval request dry-run completion attestation approval request proposal"
    )


def test_serialization_is_deterministic():
    first = governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_review_gate_to_json(
        _build()
    )
    second = governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_review_gate_to_json(
        _build()
    )

    assert first == second
    assert json.loads(first)["version"] == "3.13.0"
