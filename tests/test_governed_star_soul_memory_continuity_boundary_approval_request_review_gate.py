from __future__ import annotations

from copy import deepcopy
import json

import pytest

from hermes_memory_fabric.governed_star_soul_memory_continuity_boundary_approval_request_review_gate import (
    APPROVAL_REQUEST_REVIEW_GATE_COMPONENT_KEYS,
    APPROVAL_REQUEST_REVIEW_GATE_FALSE_FLAGS,
    APPROVAL_REQUEST_REVIEW_GATE_OBJECT_FALSE_FLAGS,
    LAYER_MAPPING,
    READY_NEXT_ALLOWED_STEP,
    REVIEWED_CHAIN_VERSIONS,
    REVIEWED_STAR_HUB_CHAIN_VERSIONS,
    SENSITIVE_KEYS,
    SOURCE_PROPOSED_CHAIN_VERSIONS,
    SOURCE_PROPOSED_STAR_HUB_CHAIN_VERSIONS,
    SOURCE_REVIEWED_CHAIN_VERSIONS,
    SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS,
    build_governed_star_soul_memory_continuity_boundary_approval_request_review_gate,
    governed_star_soul_memory_continuity_boundary_approval_request_review_gate_to_json,
)
from tests.test_governed_star_soul_memory_continuity_boundary_approval_request_proposal import (
    _build as _valid_v3_4_approval_request_proposal,
)


_BASE_SOURCE_REPORT = _valid_v3_4_approval_request_proposal()


def _valid_source_report() -> dict[str, object]:
    return deepcopy(_BASE_SOURCE_REPORT)


def _build(
    report: dict[str, object] | None = None,
) -> dict[str, object]:
    return build_governed_star_soul_memory_continuity_boundary_approval_request_review_gate(
        _valid_source_report() if report is None else report
    )


def test_valid_v3_4_approval_request_proposal_creates_v3_5_review_gate_ready():
    result = _build()

    assert result["version"] == "3.5.0"
    assert (
        result["status"]
        == "star_soul_memory_continuity_boundary_approval_request_review_gate_ready"
    )
    assert (
        result["source_star_soul_approval_request_proposal_version"]
        == "3.4.0"
    )
    for field in [
        "read_only",
        "read_only_memory",
        "review_gate_only",
        "approval_request_review_gate_only",
        "star_soul_memory_continuity_boundary_approval_request_review_gate_only",
        "thirteenth_memory_layer_star_soul_boundary_approval_request_review_gate_only",
        "star_soul_memory_continuity_boundary_approval_request_reviewed_for_human_review_only",
        "star_soul_memory_continuity_boundary_approval_request_dry_run_proposal_ready_for_human_review_only",
    ]:
        assert result[field] is True
    assert result["blocking_reasons"] == []
    assert all(
        check["passed"] is True
        for check in result["approval_request_review_gate_checks"]
    )

    review_gate = result[
        "star_soul_memory_continuity_boundary_approval_request_review_gate"
    ]
    assert (
        review_gate["review_status"]
        == "star_soul_memory_continuity_boundary_approval_request_reviewed_for_human_review_only"
    )
    assert (
        review_gate["boundary_type"]
        == "star_soul_memory_continuity_boundary_approval_request_review_gate"
    )
    assert (
        review_gate[
            "source_star_soul_memory_continuity_boundary_approval_request_proposal_valid"
        ]
        is True
    )
    assert (
        review_gate[
            "star_soul_memory_continuity_boundary_approval_request_reviewed"
        ]
        is True
    )
    assert (
        review_gate[
            "star_soul_memory_continuity_boundary_approval_request_structurally_review_ready"
        ]
        is True
    )
    assert set(review_gate["approval_request_review_gate_components"]) >= (
        APPROVAL_REQUEST_REVIEW_GATE_COMPONENT_KEYS
    )


def test_reviewed_chain_versions_exactly_match_required_ranges():
    source_expected = [
        *[f"v2.{minor}.0" for minor in range(9, 61)],
        "v3.0.0",
        "v3.1.0",
        "v3.2.0",
    ]
    source_star_hub_expected = [
        *[f"v2.{minor}.0" for minor in range(19, 61)],
        "v3.0.0",
        "v3.1.0",
        "v3.2.0",
    ]
    expected = [*source_expected, "v3.4.0"]
    expected_star_hub = [*source_star_hub_expected, "v3.4.0"]
    result = _build()
    review_gate = result[
        "star_soul_memory_continuity_boundary_approval_request_review_gate"
    ]

    assert SOURCE_REVIEWED_CHAIN_VERSIONS == source_expected
    assert result["source_reviewed_chain_versions"] == source_expected
    assert SOURCE_PROPOSED_CHAIN_VERSIONS == expected
    assert result["source_proposed_chain_versions"] == expected
    assert REVIEWED_CHAIN_VERSIONS == expected
    assert result["reviewed_chain_versions"] == expected
    assert review_gate["reviewed_chain_versions"] == expected
    assert SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS == source_star_hub_expected
    assert result["source_reviewed_star_hub_chain_versions"] == (
        source_star_hub_expected
    )
    assert SOURCE_PROPOSED_STAR_HUB_CHAIN_VERSIONS == expected_star_hub
    assert result["source_proposed_star_hub_chain_versions"] == (
        expected_star_hub
    )
    assert REVIEWED_STAR_HUB_CHAIN_VERSIONS == expected_star_hub
    assert result["reviewed_star_hub_chain_versions"] == expected_star_hub
    assert review_gate["reviewed_star_hub_chain_versions"] == (
        expected_star_hub
    )


def test_blocked_source_approval_request_proposal_blocks_review_gate():
    report = _valid_source_report()
    report["status"] = "blocked"
    report["blocking_reasons"] = ["source_blocked"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert (
        result[
            "star_soul_memory_continuity_boundary_approval_request_reviewed_for_human_review_only"
        ]
        is False
    )
    assert (
        result[
            "star_soul_memory_continuity_boundary_approval_request_dry_run_proposal_ready_for_human_review_only"
        ]
        is False
    )
    assert result["reviewed_chain_versions"] == REVIEWED_CHAIN_VERSIONS
    assert (
        result["reviewed_star_hub_chain_versions"]
        == REVIEWED_STAR_HUB_CHAIN_VERSIONS
    )
    assert result["blocking_reasons"]
    assert result["required_human_actions"]


@pytest.mark.parametrize(
    "field",
    [
        "authorization_granted",
        "approval_request_created",
        "approval_request_submitted",
        "approval_request_executed",
        "approval_granted",
        "real_human_decision_recorded",
        "dry_run_executed",
        "dry_run_plan_executed",
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
        "finalization_executed",
        "completion_executed",
        "closure_executed",
        "attestation_executed",
        "audit_executed",
        "audit_log_written",
        "violation_response_executed",
        "automated_correction_performed",
        "violation_enforced",
        "candidate_rules_enforced",
        "star_law_rules_created",
        "star_law_rules_activated",
        "star_law_rules_enforced",
        "autonomous_governance_created",
        "autonomous_execution_authorized",
        "enters_star_soul_layer",
        "enters_star_cosmos_layer",
        "enters_star_source_layer",
        "civilization_core_complete_claimed",
        "handoff_authorized",
        "star_hub_handoff_authorized",
        "scheduling_performed",
        "memory_write_performed",
        "would_write_durable_memory",
        "memory_graph_mutated",
        "would_mutate_memory_graph",
        "operation_ledger_entry_created",
        "would_create_operation_ledger_entry",
        "openclaw_called",
        "invokes_openclaw",
        "github_api_called",
        "github_api_executed",
        "would_call_github_api",
    ],
)
def test_unsafe_claim_blocks_review_gate_and_output_stays_false(field: str):
    report = _valid_source_report()
    report["unsafe_nested_claim"] = {field: True}

    result = _build(report)

    assert result["status"] == "blocked"
    assert result[field] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("version", "3.3.0"),
        ("read_only", False),
        ("read_only_memory", False),
        ("proposal_only", False),
        ("approval_request_proposal_only", False),
        (
            "star_soul_memory_continuity_boundary_approval_request_proposal_only",
            False,
        ),
        (
            "thirteenth_memory_layer_star_soul_boundary_approval_request_proposal_only",
            False,
        ),
        (
            "star_soul_memory_continuity_boundary_approval_request_proposed_for_human_review_only",
            False,
        ),
        (
            "star_soul_memory_continuity_boundary_approval_request_review_gate_ready_for_human_review_only",
            False,
        ),
        ("source_star_soul_approval_review_gate_version", "3.2.0"),
        ("next_allowed_step", "wrong"),
        ("blocking_reasons", ["blocked"]),
    ],
)
def test_missing_or_invalid_required_source_field_blocks_review_gate(
    field: str, value: object
):
    report = _valid_source_report()
    report[field] = value

    assert _build(report)["status"] == "blocked"


def test_malformed_proposed_chain_versions_blocks_review_gate():
    report = _valid_source_report()
    report["proposed_chain_versions"] = ["v3.4.0"]

    assert _build(report)["status"] == "blocked"


def test_malformed_proposed_star_hub_chain_versions_blocks_review_gate():
    report = _valid_source_report()
    report["proposed_star_hub_chain_versions"] = ["v3.4.0"]

    assert _build(report)["status"] == "blocked"


def test_invalid_nested_approval_request_proposal_blocks_review_gate():
    report = _valid_source_report()
    proposal = report[
        "star_soul_memory_continuity_boundary_approval_request_proposal"
    ]
    assert isinstance(proposal, dict)
    proposal[
        "star_soul_memory_continuity_boundary_approval_request_proposed"
    ] = False

    assert _build(report)["status"] == "blocked"


def test_invalid_proposed_approval_request_boundaries_block_review_gate():
    report = _valid_source_report()
    report[
        "proposed_star_soul_memory_continuity_approval_request_boundaries"
    ] = {"unsafe": {"proposal_only": False}}

    assert _build(report)["status"] == "blocked"


def test_invalid_thirteenth_memory_layer_boundary_blocks_review_gate():
    report = _valid_source_report()
    boundary = report["thirteenth_memory_layer_boundary"]
    assert isinstance(boundary, dict)
    boundary["approval_granted"] = True

    assert _build(report)["status"] == "blocked"


def test_reviewed_approval_request_boundaries_are_review_only_non_authorizing():
    result = _build()
    boundaries = result[
        "reviewed_star_soul_memory_continuity_approval_request_boundaries"
    ]

    assert isinstance(boundaries, dict)
    assert set(boundaries) >= APPROVAL_REQUEST_REVIEW_GATE_COMPONENT_KEYS
    for boundary in boundaries.values():
        assert boundary["review_only"] is True
        assert boundary["approval_request_review_gate_only"] is True
        assert boundary["human_review_only"] is True
        assert boundary["non_authorizing"] is True
        assert boundary["boundary_status"] == "reviewed_for_human_review_only"
        for field in APPROVAL_REQUEST_REVIEW_GATE_FALSE_FLAGS:
            assert boundary[field] is False


def test_sensitive_field_names_and_values_are_not_leaked():
    report = _valid_source_report()
    report["nested_sensitive"] = {
        "approval_phrase": "do-not-leak-approval-phrase",
        "stdout_tail": "do-not-leak-stdout-tail",
        "stdout": "do-not-leak-stdout",
        "raw_logs": "do-not-leak-raw-logs",
        "token": "do-not-leak-token",
        "api_key": "do-not-leak-api-key",
        "secret": "do-not-leak-secret",
        "password": "do-not-leak-password",
        "credential": "do-not-leak-credential",
    }

    result = _build(report)
    serialized = governed_star_soul_memory_continuity_boundary_approval_request_review_gate_to_json(
        result
    )

    assert result["sensitive_field_count"] == len(SENSITIVE_KEYS)
    assert result["sensitive_fields_omitted"] is True
    assert "Sensitive fields were omitted" in serialized
    for sensitive_key in SENSITIVE_KEYS:
        assert sensitive_key not in serialized
    assert "do-not-leak" not in serialized
    json.loads(serialized)


@pytest.mark.parametrize(
    "field", sorted(APPROVAL_REQUEST_REVIEW_GATE_FALSE_FLAGS)
)
def test_review_gate_preserves_all_top_level_false_flags(field: str):
    assert _build()[field] is False


@pytest.mark.parametrize(
    "field", sorted(APPROVAL_REQUEST_REVIEW_GATE_OBJECT_FALSE_FLAGS)
)
def test_review_gate_object_preserves_all_false_flags(field: str):
    review_gate = _build()[
        "star_soul_memory_continuity_boundary_approval_request_review_gate"
    ]

    assert review_gate[field] is False


def test_approval_request_review_gate_crosses_no_unsafe_boundary():
    result = _build()

    for field in [
        "approval_request_created",
        "approval_request_submitted",
        "approval_request_executed",
        "approval_granted",
        "real_human_decision_recorded",
        "dry_run_executed",
        "dry_run_plan_executed",
        "enters_star_soul_layer",
        "star_soul_continuity_executed",
        "star_soul_continuity_authorized",
        "star_soul_continuity_record_created",
        "star_soul_continuity_ledger_entry_created",
        "persistent_autonomous_identity_created",
        "identity_awakening_performed",
        "personality_awakening_performed",
        "soul_awakening_performed",
        "consciousness_claimed",
        "self_awareness_claimed",
        "personhood_claimed",
        "sentience_claimed",
        "autonomous_self_model_executed",
        "autonomous_self_model_authorized",
        "handoff_authorized",
        "star_hub_handoff_authorized",
        "would_write_durable_memory",
        "would_mutate_memory_graph",
        "would_create_operation_ledger_entry",
        "invokes_openclaw",
        "openclaw_execution_authorized",
        "would_call_github_api",
        "civilization_core_complete_claimed",
        "enters_star_cosmos_layer",
        "enters_star_source_layer",
    ]:
        assert result[field] is False


def test_layer_mapping_thirteenth_boundary_and_next_step_are_exact():
    result = _build()

    assert result["civilization_core_layer_mapping"] == LAYER_MAPPING
    assert LAYER_MAPPING == {
        "primary_layer": "星魂记忆",
        "primary_layer_status": "Star-Soul Memory continuity boundary approval request review gate only, not approval request creation, not approval request submission, not approval request execution, not approval grant, not real human decision recording, not continuity execution, not continuity authorization, not continuity record creation, not continuity-ledger creation, not persistent autonomous identity creation, not consciousness claim, not self-awareness claim, not personhood claim, not sentience claim, not identity awakening, not personality awakening, not autonomous self-model execution, not durable memory write, not Memory Graph mutation, not operation-ledger creation, not handoff, not scheduling, not dry-run execution, and not autonomous execution",
        "source_layer": "星魂记忆",
        "source_layer_status": "Star-Soul Memory continuity boundary approval request proposal complete for human review only",
        "supporting_layers": [
            "星穹记忆",
            "星域记忆",
            "星界记忆",
            "星辰记忆",
            "星律记忆",
            "星魂记忆",
        ],
        "direction": "Star-Soul Memory continuity boundary approval request proposal -> Star-Soul Memory continuity boundary approval request review gate",
        "boundary_transition": "v3.4.0 Star-Soul Memory continuity boundary approval request proposal -> v3.5.0 Star-Soul Memory continuity boundary approval request review gate",
        "hard_boundary": "v3.5.0 reviews approval request proposal boundaries for human review only and does not create, submit, execute, grant, record approval, or perform dry-run execution",
    }
    boundary = result["thirteenth_memory_layer_boundary"]
    assert boundary["memory_layer"] == "星魂记忆"
    assert boundary["memory_layer_number"] == 13
    assert boundary["boundary_approval_request_review_gate_only"] is True
    assert boundary["approval_request_reviewed_for_human_review_only"] is True
    assert boundary["enters_thirteenth_memory_layer"] is False
    assert boundary["thirteenth_memory_layer_transition_authorized"] is False
    assert boundary["enters_star_soul_layer"] is False
    assert boundary["star_soul_continuity_executed"] is False
    assert boundary["star_soul_continuity_authorized"] is False
    assert boundary["approval_request_created"] is False
    assert boundary["approval_request_submitted"] is False
    assert boundary["approval_request_executed"] is False
    assert boundary["approval_granted"] is False
    assert boundary["real_human_decision_recorded"] is False
    assert boundary["dry_run_executed"] is False
    assert boundary["persistent_autonomous_identity_created"] is False
    assert boundary["consciousness_claimed"] is False
    assert boundary["self_awareness_claimed"] is False
    assert boundary["personhood_claimed"] is False
    assert boundary["sentience_claimed"] is False
    assert boundary["enters_star_cosmos_layer"] is False
    assert boundary["enters_star_source_layer"] is False
    assert result["next_allowed_step"] == READY_NEXT_ALLOWED_STEP
    assert (
        READY_NEXT_ALLOWED_STEP
        == "v3.6.0 Star-Soul Memory continuity boundary approval request dry-run proposal"
    )


@pytest.mark.parametrize(
    "claim",
    [
        "approval request is created",
        "approval request is submitted",
        "approval request is executed",
        "approval is granted",
        "human decision is recorded",
        "star-soul continuity is executed",
        "star-soul continuity is authorized",
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
        "civilization core is complete",
        "star-soul layer is entered",
        "star-cosmos layer is entered",
        "star-source layer is entered",
        "approval request dry-run is executed",
        "approval request dry-run plan is executed",
    ],
)
def test_positive_unsafe_text_claim_blocks_review_gate(claim: str):
    report = _valid_source_report()
    report["unsafe_text"] = claim

    assert _build(report)["status"] == "blocked"
