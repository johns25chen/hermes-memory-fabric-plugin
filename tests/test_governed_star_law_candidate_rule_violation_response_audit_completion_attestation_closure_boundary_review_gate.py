from __future__ import annotations

from copy import deepcopy
import json

import pytest

from hermes_memory_fabric.governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate import (
    READY_NEXT_ALLOWED_STEP,
    REVIEWED_CHAIN_VERSIONS,
    REVIEWED_STAR_HUB_CHAIN_VERSIONS,
    REVIEW_COMPONENTS,
    REVIEW_GATE_FALSE_FLAGS,
    REVIEW_OBJECT_FALSE_FLAGS,
    SENSITIVE_KEYS,
    SOURCE_PROPOSED_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_COMPLETION_ATTESTATION_CLOSURE_BOUNDARY_KEYS,
    build_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate,
    governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate_to_json,
)
from tests.test_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal import (
    _build as _valid_v2_51_proposal,
)


def _valid_proposal_report() -> dict[str, object]:
    return deepcopy(_valid_v2_51_proposal())


def _build(report: dict[str, object] | None = None) -> dict[str, object]:
    return build_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate(
        report or _valid_proposal_report()
    )


def test_valid_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal_creates_ready_review_gate():
    result = _build()

    assert result["version"] == "2.52.0"
    assert (
        result["status"]
        == "star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate_ready"
    )
    assert result["source_proposal_version"] == "2.51.0"
    assert result["read_only"] is True
    assert result["read_only_memory"] is True
    assert result["review_gate_only"] is True
    assert (
        result[
            "candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate_only"
        ]
        is True
    )
    assert (
        result[
            "star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate_only"
        ]
        is True
    )
    assert (
        result[
            "candidate_rule_violation_response_audit_completion_attestation_closure_boundary_reviewed_for_human_review_only"
        ]
        is True
    )
    assert (
        result[
            "candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal_ready_for_human_review_only"
        ]
        is True
    )
    assert result["blocking_reasons"] == []
    assert all(check["passed"] is True for check in result["review_gate_checks"])

    review_gate = result[
        "star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate"
    ]
    assert (
        review_gate["review_status"]
        == "star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_reviewed_for_human_review_only"
    )
    assert (
        review_gate["boundary_type"]
        == "star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate"
    )
    assert (
        review_gate[
            "candidate_rule_violation_response_audit_completion_attestation_closure_boundary_reviewed"
        ]
        is True
    )
    assert (
        review_gate[
            "candidate_rule_violation_response_audit_completion_attestation_closure_boundary_structurally_review_ready"
        ]
        is True
    )
    assert (
        review_gate[
            "candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal_ready_for_human_review_only"
        ]
        is True
    )
    assert (
        review_gate[
            "source_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal_valid"
        ]
        is True
    )
    assert (
        set(
            review_gate[
                "star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_components"
            ]
        )
        == REVIEW_COMPONENTS
    )


def test_reviewed_chain_versions_exactly_match_v2_9_0_through_v2_51_0():
    expected = [f"v2.{minor}.0" for minor in range(9, 52)]

    assert REVIEWED_CHAIN_VERSIONS == expected
    assert _build()["reviewed_chain_versions"] == expected


def test_reviewed_star_hub_chain_versions_exactly_match_v2_19_0_through_v2_51_0():
    expected = [f"v2.{minor}.0" for minor in range(19, 52)]

    assert REVIEWED_STAR_HUB_CHAIN_VERSIONS == expected
    assert _build()["reviewed_star_hub_chain_versions"] == expected


def test_blocked_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal_blocks_review_gate():
    report = _valid_proposal_report()
    report["status"] = "blocked"
    report["blocking_reasons"] = ["source_blocked"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert (
        result[
            "candidate_rule_violation_response_audit_completion_attestation_closure_boundary_reviewed_for_human_review_only"
        ]
        is False
    )
    assert (
        result[
            "candidate_rule_violation_response_audit_completion_attestation_finalization_boundary_proposal_ready_for_human_review_only"
        ]
        is False
    )
    assert result["blocking_reasons"]
    assert result["required_human_actions"]
    assert result["reviewed_chain_versions"] == REVIEWED_CHAIN_VERSIONS
    assert (
        result["reviewed_star_hub_chain_versions"]
        == REVIEWED_STAR_HUB_CHAIN_VERSIONS
    )
    review_gate = result[
        "star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate"
    ]
    assert (
        review_gate[
            "candidate_rule_violation_response_audit_completion_attestation_closure_boundary_structurally_review_ready"
        ]
        is False
    )


@pytest.mark.parametrize("field", sorted(REVIEW_GATE_FALSE_FLAGS))
def test_any_unsafe_top_level_true_flag_blocks_review_gate(field: str):
    report = _valid_proposal_report()
    report[field] = True

    result = _build(report)

    assert result["status"] == "blocked"
    assert result[field] is False
    assert result["civilization_core_complete_claimed"] is False
    assert result["enters_star_law_layer"] is False
    assert result["enters_star_soul_layer"] is False
    assert result["enters_star_cosmos_layer"] is False
    assert result["enters_star_source_layer"] is False


@pytest.mark.parametrize(
    "field",
    [
        "attestation_performed",
        "attestation_authorized",
        "attestation_executed",
        "attestation_record_written",
        "attestation_ledger_entry_written",
        "completion_performed",
        "completion_authorized",
        "completion_executed",
        "completion_record_written",
        "completion_ledger_entry_written",
        "finalization_performed",
        "finalization_authorized",
        "finalization_executed",
        "finalization_record_written",
        "finalization_ledger_entry_written",
        "closure_performed",
        "closure_authorized",
        "closure_executed",
        "closure_record_written",
        "closure_ledger_entry_written",
        "audit_log_written",
        "audit_record_written",
        "audit_ledger_entry_written",
        "violation_response_audit_performed",
        "violation_response_audit_authorized",
        "violation_response_audit_executed",
        "candidate_rules_created",
        "candidate_rules_activated",
        "candidate_rules_enforced",
        "star_hub_scheduling_authorized",
        "star_hub_scheduling_executed",
    ],
)
def test_unsafe_alias_claim_blocks_review_gate(field: str):
    report = _valid_proposal_report()
    report["unsafe_nested_claim"] = {field: True}

    assert _build(report)["status"] == "blocked"


def test_unsafe_nested_proposal_authorization_flag_blocks_review_gate():
    report = _valid_proposal_report()
    proposal = report[
        "star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal"
    ]
    assert isinstance(proposal, dict)
    proposal[
        "candidate_rule_violation_response_audit_completion_attestation_closure_authorized"
    ] = True

    assert _build(report)["status"] == "blocked"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("version", "2.44.0"),
        ("read_only", False),
        ("read_only_memory", False),
        ("proposal_only", False),
        (
            "candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal_only",
            False,
        ),
        (
            "star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_proposal_only",
            False,
        ),
        ("next_allowed_step", "wrong"),
        ("blocking_reasons", ["blocked"]),
    ],
)
def test_invalid_required_source_field_blocks_review_gate(
    field: str, value: object
):
    report = _valid_proposal_report()
    report[field] = value

    assert _build(report)["status"] == "blocked"


def test_malformed_proposed_chain_versions_blocks_review_gate():
    report = _valid_proposal_report()
    report["proposed_chain_versions"] = ["v2.51.0"]

    assert _build(report)["status"] == "blocked"


def test_malformed_proposed_star_hub_chain_versions_blocks_review_gate():
    report = _valid_proposal_report()
    report["proposed_star_hub_chain_versions"] = ["v2.51.0"]

    assert _build(report)["status"] == "blocked"


def test_malformed_proposed_boundaries_block_review_gate():
    report = _valid_proposal_report()
    report[
        "proposed_candidate_rule_violation_response_audit_completion_attestation_closure_boundaries"
    ] = {
        "unsafe": {
            "proposal_only": True,
            "finalization_execution_performed": True,
        }
    }

    assert _build(report)["status"] == "blocked"


def test_reviewed_attestation_closure_boundaries_are_review_only_and_non_authorizing():
    boundaries = _build()[
        "reviewed_candidate_rule_violation_response_audit_completion_attestation_closure_boundaries"
    ]

    assert isinstance(boundaries, dict)
    assert (
        set(boundaries)
        == SOURCE_PROPOSED_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_COMPLETION_ATTESTATION_CLOSURE_BOUNDARY_KEYS
    )
    for boundary in boundaries.values():
        assert boundary["review_only"] is True
        for key, value in boundary.items():
            if key != "review_only":
                assert value is not True


def test_sensitive_field_names_and_values_are_not_leaked():
    report = _valid_proposal_report()
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
    serialized = governed_star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate_to_json(
        result
    )

    assert result["sensitive_field_count"] == len(SENSITIVE_KEYS)
    assert result["sensitive_fields_omitted"] is True
    assert "Sensitive fields were omitted" in serialized
    for sensitive_key in SENSITIVE_KEYS:
        assert sensitive_key not in serialized
    assert "do-not-leak" not in serialized
    json.loads(serialized)


@pytest.mark.parametrize("field", sorted(REVIEW_GATE_FALSE_FLAGS))
def test_review_gate_preserves_all_top_level_false_flags(field: str):
    assert _build()[field] is False


@pytest.mark.parametrize("field", sorted(REVIEW_OBJECT_FALSE_FLAGS))
def test_review_object_preserves_all_false_flags(field: str):
    review_gate = _build()[
        "star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate"
    ]

    assert review_gate[field] is False


@pytest.mark.parametrize(
    "fields",
    [
        [
            "candidate_rule_violation_response_audit_completion_attestation_closure_performed",
            "candidate_rule_violation_response_audit_completion_attestation_closure_authorized",
            "candidate_rule_violation_response_audit_completion_attestation_closure_executed",
            "candidate_rule_violation_response_audit_completion_attestation_closure_execution_authorized",
            "candidate_rule_violation_response_audit_completion_attestation_closure_record_created",
            "candidate_rule_violation_response_audit_completion_attestation_closure_ledger_entry_created",
            "closure_execution_performed",
            "closure_execution_authorized",
            "closure_record_created",
            "closure_ledger_entry_created",
        ],
        [
            "candidate_rule_violation_response_audit_completion_attestation_performed",
            "candidate_rule_violation_response_audit_completion_attestation_authorized",
            "candidate_rule_violation_response_audit_completion_attestation_executed",
            "candidate_rule_violation_response_audit_completion_attestation_execution_authorized",
            "candidate_rule_violation_response_audit_completion_attestation_record_created",
            "candidate_rule_violation_response_audit_completion_attestation_ledger_entry_created",
            "attestation_execution_performed",
            "attestation_execution_authorized",
            "attestation_record_created",
            "attestation_ledger_entry_created",
        ],
        [
            "candidate_rule_violation_response_audit_completion_performed",
            "candidate_rule_violation_response_audit_completion_authorized",
            "candidate_rule_violation_response_audit_completion_executed",
            "candidate_rule_violation_response_audit_completion_execution_authorized",
            "candidate_rule_violation_response_audit_completion_record_created",
            "candidate_rule_violation_response_audit_completion_ledger_entry_created",
            "completion_execution_performed",
            "completion_execution_authorized",
            "completion_record_created",
            "completion_ledger_entry_created",
        ],
        [
            "candidate_rule_violation_response_audit_finalization_performed",
            "candidate_rule_violation_response_audit_finalization_authorized",
            "candidate_rule_violation_response_audit_finalization_executed",
            "candidate_rule_violation_response_audit_finalization_execution_authorized",
            "candidate_rule_violation_response_audit_finalization_record_created",
            "candidate_rule_violation_response_audit_finalization_ledger_entry_created",
            "finalization_execution_performed",
            "finalization_execution_authorized",
            "finalization_record_created",
            "finalization_ledger_entry_created",
        ],
        [
            "candidate_rule_violation_response_audit_closure_performed",
            "candidate_rule_violation_response_audit_closure_authorized",
            "candidate_rule_violation_response_audit_closure_executed",
            "candidate_rule_violation_response_audit_closure_execution_authorized",
            "candidate_rule_violation_response_audit_closure_record_created",
            "candidate_rule_violation_response_audit_closure_ledger_entry_created",
            "closure_execution_performed",
            "closure_execution_authorized",
            "closure_record_created",
            "closure_ledger_entry_created",
        ],
        [
            "candidate_rule_violation_response_audit_performed",
            "candidate_rule_violation_response_audit_authorized",
            "candidate_rule_violation_response_audit_executed",
            "candidate_rule_violation_response_audit_execution_authorized",
            "candidate_rule_violation_response_audit_log_created",
            "candidate_rule_violation_response_audit_record_created",
            "candidate_rule_violation_response_audit_ledger_entry_created",
            "audit_execution_performed",
            "audit_execution_authorized",
            "audit_logging_performed",
            "audit_log_created",
            "audit_record_created",
            "audit_ledger_entry_created",
        ],
        [
            "candidate_rule_violation_response_performed",
            "candidate_rule_violation_response_authorized",
            "candidate_rule_violation_response_executed",
            "candidate_rule_violation_response_execution_authorized",
            "candidate_rule_violation_response_record_created",
            "candidate_rule_violation_response_ledger_entry_created",
        ],
        [
            "automated_correction_performed",
            "automated_correction_authorized",
            "automated_correction_executed",
            "automated_correction_execution_authorized",
        ],
        [
            "candidate_rule_violation_observation_performed",
            "candidate_rule_violation_observation_authorized",
            "candidate_rule_violation_observation_executed",
            "candidate_rule_violation_observation_execution_authorized",
            "candidate_rule_violation_detected",
            "candidate_rule_violation_recorded",
            "candidate_rule_violation_enforced",
            "candidate_rule_violation_ledger_entry_created",
        ],
    ],
)
def test_review_gate_does_not_perform_authorize_record_or_create_ledgers(
    fields: list[str],
):
    result = _build()
    review_gate = result[
        "star_law_candidate_rule_violation_response_audit_completion_attestation_closure_boundary_review_gate"
    ]

    for field in fields:
        assert result[field] is False
        assert review_gate[field] is False


def test_review_gate_does_not_enforce_rules_create_autonomy_or_enter_layers():
    result = _build()

    for field in [
        "candidate_rule_enforcement_performed",
        "candidate_rule_enforcement_authorized",
        "candidate_rule_activation_performed",
        "candidate_rule_activation_authorized",
        "star_law_candidate_rules_created",
        "star_law_candidate_rules_activated",
        "star_law_candidate_rules_enforced",
        "star_law_rules_created",
        "star_law_rules_activated",
        "star_law_rules_enforced",
        "star_law_self_enforcing_law_created",
        "star_law_self_enforcing_law_active",
        "autonomous_governance_created",
        "autonomous_execution_authorized",
        "enters_star_law_layer",
        "enters_star_soul_layer",
        "enters_star_cosmos_layer",
        "enters_star_source_layer",
    ]:
        assert result[field] is False


def test_review_gate_does_not_authorize_handoff_write_openclaw_or_completion():
    result = _build()

    for field in [
        "handoff_authorized",
        "star_hub_handoff_authorized",
        "memory_write_authorized",
        "would_write_durable_memory",
        "would_mutate_memory_graph",
        "would_create_operation_ledger_entry",
        "openclaw_execution_authorized",
        "invokes_openclaw",
        "approval_granted",
        "human_decision_recorded",
        "civilization_core_complete_claimed",
    ]:
        assert result[field] is False


def test_layer_mapping_and_next_allowed_step_are_exact():
    result = _build()
    mapping = result["civilization_core_layer_mapping"]

    assert mapping["primary_layer"] == "星律记忆"
    assert (
        mapping["primary_layer_status"]
        == "Star-Law candidate rule violation response audit completion attestation closure boundary review gate only, not closure execution, not closure record creation, not closure-ledger creation, not attestation execution, not attestation record creation, not attestation-ledger creation, not completion execution, not finalization execution, not audit execution, not audit logging, not audit record creation, not audit-ledger creation, not violation response execution, not automated correction, not violation enforcement, and not autonomous execution"
    )
    assert mapping["source_layer"] == "星律记忆"
    assert (
        mapping["source_layer_status"]
        == "Star-Law candidate rule violation response audit completion attestation closure boundary proposal complete for human review only"
    )
    assert all(
        layer in mapping["supporting_layers"]
        for layer in ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"]
    )
    assert (
        mapping["direction"]
        == "Star-Law candidate rule violation response audit completion attestation closure boundary proposal -> Star-Law candidate rule violation response audit completion attestation closure boundary review gate"
    )
    assert result["next_allowed_step"] == READY_NEXT_ALLOWED_STEP
    assert (
        READY_NEXT_ALLOWED_STEP
        == "v2.53.0 Star-Law candidate rule violation response audit completion attestation finalization boundary proposal"
    )


@pytest.mark.parametrize(
    "claim",
    [
        "attestation execution is performed",
        "attestation execution is authorized",
        "attestation record is created",
        "attestation-ledger entries are created",
        "completion execution is performed",
        "completion execution is authorized",
        "completion record is created",
        "completion-ledger entries are created",
        "finalization execution is authorized",
        "finalization record is created",
        "closure execution is performed",
        "audit logging is performed",
        "violation response is executed",
        "automated correction is authorized",
        "violations are enforced",
        "star-law rules are created",
        "autonomous execution is authorized",
        "civilization core is complete",
    ],
)
def test_positive_unsafe_text_claim_blocks_review_gate(claim: str):
    report = _valid_proposal_report()
    report["unsafe_text"] = claim

    assert _build(report)["status"] == "blocked"
