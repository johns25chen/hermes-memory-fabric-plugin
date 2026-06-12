from __future__ import annotations

from copy import deepcopy
import json

import pytest

from hermes_memory_fabric.governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposal import (
    APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_PROPOSAL_COMPONENT_KEYS,
    APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_PROPOSAL_FALSE_FLAGS,
    APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_PROPOSAL_OBJECT_FALSE_FLAGS,
    LAYER_MAPPING,
    PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_CHAIN_VERSIONS,
    PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_STAR_HUB_CHAIN_VERSIONS,
    READY_NEXT_ALLOWED_STEP,
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
    build_governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposal,
    governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposal_to_json,
)
from tests.test_governed_star_soul_memory_continuity_boundary_approval_request_dry_run_execution_review_gate import (
    _build as _valid_v3_9_execution_review_gate,
)


_BASE_SOURCE_REPORT = _valid_v3_9_execution_review_gate()


def _valid_source_report() -> dict[str, object]:
    return deepcopy(_BASE_SOURCE_REPORT)


def _build(
    report: dict[str, object] | None = None,
) -> dict[str, object]:
    return build_governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposal(
        _valid_source_report() if report is None else report
    )


def test_valid_v3_9_execution_review_gate_creates_v3_10_proposal_ready():
    result = _build()

    assert result["version"] == "3.10.0"
    assert (
        result["status"]
        == "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposal_ready"
    )
    assert (
        result[
            "source_star_soul_approval_request_dry_run_completion_attestation_source_version"
        ]
        == "3.9.0"
    )
    assert (
        result[
            "source_star_soul_approval_request_dry_run_execution_review_gate_version"
        ]
        == "3.9.0"
    )
    assert (
        result[
            "source_star_soul_approval_request_dry_run_execution_proposal_version"
        ]
        == "3.8.0"
    )
    assert (
        result["source_star_soul_approval_request_dry_run_review_gate_version"]
        == "3.7.0"
    )
    assert (
        result["source_star_soul_approval_request_dry_run_proposal_version"]
        == "3.6.0"
    )
    for field in [
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
    ]:
        assert result[field] is True
    assert result["blocking_reasons"] == []
    assert all(
        check["passed"] is True
        for check in result[
            "approval_request_dry_run_completion_attestation_proposal_checks"
        ]
    )

    proposal = result[
        "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposal"
    ]
    assert (
        proposal["proposal_status"]
        == "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposed_for_human_review_only"
    )
    assert (
        proposal["boundary_type"]
        == "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposal"
    )
    assert (
        proposal[
            "source_star_soul_memory_continuity_boundary_approval_request_dry_run_execution_review_gate_valid"
        ]
        is True
    )
    assert (
        proposal[
            "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposed"
        ]
        is True
    )
    assert (
        proposal[
            "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_structurally_proposed_for_human_review_only"
        ]
        is True
    )
    assert set(
        proposal[
            "proposed_dry_run_completion_attestation_boundary_components"
        ]
    ) >= APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_PROPOSAL_COMPONENT_KEYS


def test_all_source_and_proposed_lineages_are_exact():
    reviewed_expected = [
        *[f"v2.{minor}.0" for minor in range(9, 61)],
        "v3.0.0",
        "v3.1.0",
        "v3.2.0",
        "v3.4.0",
    ]
    reviewed_star_hub_expected = [
        *[f"v2.{minor}.0" for minor in range(19, 61)],
        "v3.0.0",
        "v3.1.0",
        "v3.2.0",
        "v3.4.0",
    ]
    dry_run_expected = [*reviewed_expected, "v3.6.0"]
    dry_run_star_hub_expected = [*reviewed_star_hub_expected, "v3.6.0"]
    execution_expected = [
        *dry_run_expected,
        "v3.7.0",
        "v3.8.0",
    ]
    execution_star_hub_expected = [
        *dry_run_star_hub_expected,
        "v3.7.0",
        "v3.8.0",
    ]
    execution_reviewed_expected = [*execution_expected, "v3.9.0"]
    execution_reviewed_star_hub_expected = [
        *execution_star_hub_expected,
        "v3.9.0",
    ]
    completion_attestation_expected = [
        *execution_reviewed_expected,
        "v3.10.0",
    ]
    completion_attestation_star_hub_expected = [
        *execution_reviewed_star_hub_expected,
        "v3.10.0",
    ]
    result = _build()
    proposal = result[
        "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposal"
    ]

    assert SOURCE_REVIEWED_CHAIN_VERSIONS == reviewed_expected
    assert result["source_reviewed_chain_versions"] == reviewed_expected
    assert SOURCE_REVIEWED_STAR_HUB_CHAIN_VERSIONS == reviewed_star_hub_expected
    assert (
        result["source_reviewed_star_hub_chain_versions"]
        == reviewed_star_hub_expected
    )
    assert SOURCE_PROPOSED_DRY_RUN_CHAIN_VERSIONS == dry_run_expected
    assert SOURCE_REVIEWED_DRY_RUN_CHAIN_VERSIONS == dry_run_expected
    assert result["source_proposed_dry_run_chain_versions"] == dry_run_expected
    assert result["source_reviewed_dry_run_chain_versions"] == dry_run_expected
    assert (
        SOURCE_PROPOSED_DRY_RUN_STAR_HUB_CHAIN_VERSIONS
        == dry_run_star_hub_expected
    )
    assert (
        SOURCE_REVIEWED_DRY_RUN_STAR_HUB_CHAIN_VERSIONS
        == dry_run_star_hub_expected
    )
    assert (
        result["source_proposed_dry_run_star_hub_chain_versions"]
        == dry_run_star_hub_expected
    )
    assert (
        result["source_reviewed_dry_run_star_hub_chain_versions"]
        == dry_run_star_hub_expected
    )
    assert (
        SOURCE_PROPOSED_DRY_RUN_EXECUTION_CHAIN_VERSIONS
        == execution_expected
    )
    assert (
        result["source_proposed_dry_run_execution_chain_versions"]
        == execution_expected
    )
    assert (
        SOURCE_PROPOSED_DRY_RUN_EXECUTION_STAR_HUB_CHAIN_VERSIONS
        == execution_star_hub_expected
    )
    assert (
        result[
            "source_proposed_dry_run_execution_star_hub_chain_versions"
        ]
        == execution_star_hub_expected
    )
    assert (
        SOURCE_REVIEWED_DRY_RUN_EXECUTION_CHAIN_VERSIONS
        == execution_reviewed_expected
    )
    assert (
        result["source_reviewed_dry_run_execution_chain_versions"]
        == execution_reviewed_expected
    )
    assert (
        SOURCE_REVIEWED_DRY_RUN_EXECUTION_STAR_HUB_CHAIN_VERSIONS
        == execution_reviewed_star_hub_expected
    )
    assert (
        result[
            "source_reviewed_dry_run_execution_star_hub_chain_versions"
        ]
        == execution_reviewed_star_hub_expected
    )
    assert (
        PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_CHAIN_VERSIONS
        == completion_attestation_expected
    )
    assert (
        result["proposed_dry_run_completion_attestation_chain_versions"]
        == completion_attestation_expected
    )
    assert (
        proposal["proposed_dry_run_completion_attestation_chain_versions"]
        == completion_attestation_expected
    )
    assert (
        PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_STAR_HUB_CHAIN_VERSIONS
        == completion_attestation_star_hub_expected
    )
    assert (
        result[
            "proposed_dry_run_completion_attestation_star_hub_chain_versions"
        ]
        == completion_attestation_star_hub_expected
    )
    assert (
        proposal[
            "proposed_dry_run_completion_attestation_star_hub_chain_versions"
        ]
        == completion_attestation_star_hub_expected
    )


def test_blocked_source_execution_review_gate_blocks_proposal():
    report = _valid_source_report()
    report["status"] = "blocked"
    report["blocking_reasons"] = ["source_blocked"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert (
        result[
            "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposed_for_human_review_only"
        ]
        is False
    )
    assert (
        result[
            "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_review_gate_ready_for_human_review_only"
        ]
        is False
    )
    assert (
        result["proposed_dry_run_completion_attestation_chain_versions"]
        == PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_CHAIN_VERSIONS
    )
    assert (
        result[
            "proposed_dry_run_completion_attestation_star_hub_chain_versions"
        ]
        == PROPOSED_DRY_RUN_COMPLETION_ATTESTATION_STAR_HUB_CHAIN_VERSIONS
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
        "audit_log_written",
        "audit_logging_performed",
        "response_executed",
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
def test_unsafe_claim_blocks_proposal_and_output_stays_false(field: str):
    report = _valid_source_report()
    report["unsafe_nested_claim"] = {field: True}

    result = _build(report)

    assert result["status"] == "blocked"
    assert result[field] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("version", "3.8.0"),
        ("read_only", False),
        ("read_only_memory", False),
        ("review_gate_only", False),
        ("dry_run_execution_review_gate_only", False),
        ("approval_request_dry_run_execution_review_gate_only", False),
        (
            "star_soul_memory_continuity_boundary_approval_request_dry_run_execution_review_gate_only",
            False,
        ),
        (
            "thirteenth_memory_layer_star_soul_boundary_approval_request_dry_run_execution_review_gate_only",
            False,
        ),
        (
            "star_soul_memory_continuity_boundary_approval_request_dry_run_execution_reviewed_for_human_review_only",
            False,
        ),
        (
            "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposal_ready_for_human_review_only",
            False,
        ),
        (
            "source_star_soul_approval_request_dry_run_execution_proposal_version",
            "3.7.0",
        ),
        ("next_allowed_step", "wrong"),
        ("blocking_reasons", ["blocked"]),
    ],
)
def test_missing_or_invalid_required_source_field_blocks_proposal(
    field: str, value: object
):
    report = _valid_source_report()
    report[field] = value

    assert _build(report)["status"] == "blocked"


def test_malformed_reviewed_dry_run_execution_chain_versions_blocks_proposal():
    report = _valid_source_report()
    report["reviewed_dry_run_execution_chain_versions"] = ["v3.9.0"]

    assert _build(report)["status"] == "blocked"


def test_malformed_reviewed_dry_run_execution_star_hub_chain_versions_blocks_proposal():
    report = _valid_source_report()
    report["reviewed_dry_run_execution_star_hub_chain_versions"] = ["v3.9.0"]

    assert _build(report)["status"] == "blocked"


def test_invalid_nested_execution_review_gate_blocks_proposal():
    report = _valid_source_report()
    review_gate = report[
        "star_soul_memory_continuity_boundary_approval_request_dry_run_execution_review_gate"
    ]
    assert isinstance(review_gate, dict)
    review_gate[
        "star_soul_memory_continuity_boundary_approval_request_dry_run_execution_reviewed"
    ] = False

    assert _build(report)["status"] == "blocked"


def test_unsafe_nested_execution_review_gate_claim_blocks_proposal():
    report = _valid_source_report()
    review_gate = report[
        "star_soul_memory_continuity_boundary_approval_request_dry_run_execution_review_gate"
    ]
    assert isinstance(review_gate, dict)
    review_gate["completion_executed"] = True

    result = _build(report)

    assert result["status"] == "blocked"
    assert result["completion_executed"] is False


def test_invalid_reviewed_execution_boundaries_block_proposal():
    report = _valid_source_report()
    report[
        "reviewed_star_soul_memory_continuity_approval_request_dry_run_execution_boundaries"
    ] = {"unsafe": {"review_only": False}}

    assert _build(report)["status"] == "blocked"


def test_proposed_completion_attestation_boundaries_are_proposal_only():
    result = _build()
    boundaries = result[
        "proposed_star_soul_memory_continuity_approval_request_dry_run_completion_attestation_boundaries"
    ]

    assert isinstance(boundaries, dict)
    assert set(
        boundaries
    ) >= APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_PROPOSAL_COMPONENT_KEYS
    for boundary in boundaries.values():
        assert boundary["proposal_only"] is True
        assert boundary["completion_attestation_proposal_only"] is True
        assert boundary["dry_run_completion_attestation_proposal_only"] is True
        assert (
            boundary[
                "approval_request_dry_run_completion_attestation_proposal_only"
            ]
            is True
        )
        assert boundary["human_review_only"] is True
        assert boundary["non_authorizing"] is True
        assert boundary["non_executing"] is True
        assert boundary["non_finalizing"] is True
        assert boundary["non_closing"] is True
        assert boundary["boundary_status"] == "proposed_for_human_review_only"
        for field in APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_PROPOSAL_FALSE_FLAGS:
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
    serialized = governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposal_to_json(
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
    "field",
    sorted(APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_PROPOSAL_FALSE_FLAGS),
)
def test_proposal_preserves_all_top_level_false_flags(field: str):
    assert _build()[field] is False


@pytest.mark.parametrize(
    "field",
    sorted(
        APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_PROPOSAL_OBJECT_FALSE_FLAGS
    ),
)
def test_proposal_object_preserves_all_false_flags(field: str):
    proposal = _build()[
        "star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_proposal"
    ]

    assert proposal[field] is False


def test_proposal_crosses_no_unsafe_boundary():
    result = _build()

    for field in [
        "dry_run_executed",
        "dry_run_plan_executed",
        "completion_executed",
        "attestation_executed",
        "finalization_executed",
        "closure_executed",
        "approval_request_created",
        "approval_request_submitted",
        "approval_request_executed",
        "approval_granted",
        "real_human_decision_recorded",
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
    assert LAYER_MAPPING["primary_layer"] == "星魂记忆"
    assert LAYER_MAPPING["source_layer"] == "星魂记忆"
    assert (
        LAYER_MAPPING["hard_boundary"]
        == "v3.10.0 proposes approval request dry-run completion attestation boundaries for human review only and does not execute dry-run, execute dry-run plan, execute completion, execute attestation, finalize, close, create, submit, execute, grant, record approval, or record real human decisions"
    )
    boundary = result["thirteenth_memory_layer_boundary"]
    assert boundary["memory_layer"] == "星魂记忆"
    assert boundary["memory_layer_number"] == 13
    assert (
        boundary[
            "boundary_approval_request_dry_run_completion_attestation_proposal_only"
        ]
        is True
    )
    assert (
        boundary[
            "approval_request_dry_run_completion_attestation_proposed_for_human_review_only"
        ]
        is True
    )
    assert boundary["enters_thirteenth_memory_layer"] is False
    assert boundary["thirteenth_memory_layer_transition_authorized"] is False
    for field in APPROVAL_REQUEST_DRY_RUN_COMPLETION_ATTESTATION_PROPOSAL_FALSE_FLAGS:
        assert boundary[field] is False
    assert result["next_allowed_step"] == READY_NEXT_ALLOWED_STEP
    assert (
        READY_NEXT_ALLOWED_STEP
        == "v3.11.0 Star-Soul Memory continuity boundary approval request dry-run completion attestation review gate"
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
        "completion attestation is executed",
        "completion attestation is finalized",
        "completion attestation boundary is closed",
    ],
)
def test_positive_unsafe_text_claim_blocks_proposal(claim: str):
    report = _valid_source_report()
    report["unsafe_text"] = claim

    assert _build(report)["status"] == "blocked"
