from __future__ import annotations

from copy import deepcopy
import json

import pytest

from hermes_memory_fabric.governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal import (
    PROPOSAL_COMPONENTS,
    PROPOSAL_FALSE_FLAGS,
    PROPOSAL_OBJECT_FALSE_FLAGS,
    PROPOSED_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_COMPLETION_ATTESTATION_COMPLETION_FINALIZATION_BOUNDARY_KEYS,
    PROPOSED_CHAIN_VERSIONS,
    PROPOSED_STAR_HUB_CHAIN_VERSIONS,
    READY_NEXT_ALLOWED_STEP,
    SENSITIVE_KEYS,
    build_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal,
    governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal_to_json,
)
from tests.test_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate import (
    _build as _valid_v2_58_review_gate,
)


def _valid_review_gate_report() -> dict[str, object]:
    return deepcopy(_valid_v2_58_review_gate())


def _build(report: dict[str, object] | None = None) -> dict[str, object]:
    return build_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal(
        report or _valid_review_gate_report()
    )


def test_valid_v2_58_closure_boundary_review_gate_creates_completion_finalization_boundary_proposal_ready():
    result = _build()

    assert result["version"] == "2.59.0"
    assert (
        result["status"]
        == "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal_ready"
    )
    assert result["source_review_gate_version"] == "2.58.0"
    for field in [
        "read_only",
        "read_only_memory",
        "proposal_only",
        "candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal_only",
        "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal_only",
        "candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposed_for_human_review_only",
        "candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate_ready_for_human_review_only",
    ]:
        assert result[field] is True
    assert result["blocking_reasons"] == []
    assert all(check["passed"] is True for check in result["proposal_checks"])

    proposal = result[
        "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal"
    ]
    assert (
        proposal["proposal_status"]
        == "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposed_for_human_review_only"
    )
    assert (
        proposal["boundary_type"]
        == "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal"
    )
    assert (
        proposal[
            "source_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate_valid"
        ]
        is True
    )
    assert (
        set(
            proposal[
                "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_components"
            ]
        )
        == PROPOSAL_COMPONENTS
    )


def test_proposed_chain_versions_exactly_match_v2_9_0_through_v2_58_0():
    expected = [f"v2.{minor}.0" for minor in range(9, 59)]

    assert PROPOSED_CHAIN_VERSIONS == expected
    assert _build()["proposed_chain_versions"] == expected


def test_proposed_star_hub_chain_versions_exactly_match_v2_19_0_through_v2_58_0():
    expected = [f"v2.{minor}.0" for minor in range(19, 59)]

    assert PROPOSED_STAR_HUB_CHAIN_VERSIONS == expected
    assert _build()["proposed_star_hub_chain_versions"] == expected


def test_blocked_attestation_completion_boundary_review_gate_blocks_proposal():
    report = _valid_review_gate_report()
    report["status"] = "blocked"
    report["blocking_reasons"] = ["source_blocked"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert (
        result[
            "candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposed_for_human_review_only"
        ]
        is False
    )
    assert (
        result[
            "candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate_ready_for_human_review_only"
        ]
        is False
    )
    proposal = result[
        "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal"
    ]
    assert (
        proposal[
            "candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposed"
        ]
        is False
    )
    assert result["proposed_chain_versions"] == PROPOSED_CHAIN_VERSIONS
    assert (
        result["proposed_star_hub_chain_versions"]
        == PROPOSED_STAR_HUB_CHAIN_VERSIONS
    )
    assert result["blocking_reasons"]
    assert result["required_human_actions"]


@pytest.mark.parametrize("field", sorted(PROPOSAL_FALSE_FLAGS))
def test_unsafe_claim_blocks_proposal_and_output_stays_safe(field: str):
    report = _valid_review_gate_report()
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
        "closure_performed",
        "closure_authorized",
        "closure_executed",
        "closure_record_written",
        "closure_ledger_entry_written",
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
def test_unsafe_alias_claim_blocks_proposal(field: str):
    report = _valid_review_gate_report()
    report["unsafe_nested_claim"] = {field: True}

    assert _build(report)["status"] == "blocked"


def test_nested_closure_execution_claim_blocks_proposal():
    report = _valid_review_gate_report()
    review_gate = report[
        "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundary_review_gate"
    ]
    assert isinstance(review_gate, dict)
    review_gate[
        "candidate_rule_violation_response_audit_completion_attestation_completion_closure_executed"
    ] = True

    assert _build(report)["status"] == "blocked"


def test_malformed_reviewed_chain_versions_blocks_proposal():
    report = _valid_review_gate_report()
    report["reviewed_chain_versions"] = ["v2.9.0", "v2.55.0"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert result["proposed_chain_versions"] == PROPOSED_CHAIN_VERSIONS


def test_malformed_reviewed_star_hub_chain_versions_blocks_proposal():
    report = _valid_review_gate_report()
    report["reviewed_star_hub_chain_versions"] = ["v2.19.0", "v2.55.0"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert (
        result["proposed_star_hub_chain_versions"]
        == PROPOSED_STAR_HUB_CHAIN_VERSIONS
    )


def test_malformed_reviewed_boundaries_block_proposal():
    report = _valid_review_gate_report()
    report[
        "reviewed_candidate_rule_violation_response_audit_completion_attestation_completion_closure_boundaries"
    ] = {
        "unsafe": {
            "review_only": True,
            "candidate_rule_violation_response_audit_completion_attestation_completion_closure_authorized": True,
        }
    }

    assert _build(report)["status"] == "blocked"


def test_proposed_finalization_boundaries_are_proposal_only_and_non_authorizing():
    boundaries = _build()[
        "proposed_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundaries"
    ]

    assert isinstance(boundaries, dict)
    assert (
        set(boundaries)
        == PROPOSED_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_COMPLETION_ATTESTATION_COMPLETION_FINALIZATION_BOUNDARY_KEYS
    )
    for boundary in boundaries.values():
        assert boundary["proposal_only"] is True
        for key, value in boundary.items():
            if key != "proposal_only":
                assert value is not True


def test_sensitive_field_names_and_values_are_not_leaked_in_serialized_output():
    report = _valid_review_gate_report()
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
    serialized = governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal_to_json(
        result
    )

    assert result["sensitive_field_count"] == len(SENSITIVE_KEYS)
    assert result["sensitive_fields_omitted"] is True
    assert "Sensitive fields were omitted" in serialized
    for sensitive_key in SENSITIVE_KEYS:
        assert sensitive_key not in serialized
    assert "do-not-leak" not in serialized
    json.loads(serialized)


@pytest.mark.parametrize("field", sorted(PROPOSAL_FALSE_FLAGS))
def test_proposal_preserves_all_top_level_false_flags(field: str):
    assert _build()[field] is False


@pytest.mark.parametrize("field", sorted(PROPOSAL_OBJECT_FALSE_FLAGS))
def test_proposal_object_preserves_all_false_flags(field: str):
    proposal = _build()[
        "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal"
    ]

    assert proposal[field] is False


def test_layer_mapping_and_next_allowed_step_are_exact():
    result = _build()
    mapping = result["civilization_core_layer_mapping"]

    assert mapping["primary_layer"] == "星律记忆"
    assert (
        mapping["primary_layer_status"]
        == "Star-Law candidate rule violation response audit completion attestation completion finalization boundary proposal only, not finalization execution, not finalization record creation, not finalization-ledger creation, not completion execution, not completion record creation, not completion-ledger creation, not closure execution, not closure record creation, not closure-ledger creation, not attestation execution, not attestation record creation, not attestation-ledger creation, not audit execution, not audit logging, not audit record creation, not audit-ledger creation, not violation response execution, not automated correction, not violation enforcement, and not autonomous execution"
    )
    assert mapping["source_layer"] == "星律记忆"
    assert (
        mapping["source_layer_status"]
        == "Star-Law candidate rule violation response audit completion attestation completion closure boundary review gate complete for human review only"
    )
    assert all(
        layer in mapping["supporting_layers"]
        for layer in ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"]
    )
    assert (
        mapping["direction"]
        == "Star-Law candidate rule violation response audit completion attestation completion closure boundary review gate -> Star-Law candidate rule violation response audit completion attestation completion finalization boundary proposal"
    )
    assert result["next_allowed_step"] == READY_NEXT_ALLOWED_STEP
    assert (
        READY_NEXT_ALLOWED_STEP
        == "v2.60.0 Star-Law candidate rule violation response audit completion attestation completion finalization boundary review gate"
    )


@pytest.mark.parametrize(
    "claim",
    [
        "closure execution is performed",
        "closure execution is authorized",
        "closure record is created",
        "closure-ledger entries are created",
        "attestation execution is performed",
        "attestation record is created",
        "completion execution is performed",
        "completion record is created",
        "finalization execution is authorized",
        "audit logging is performed",
        "violation response is executed",
        "automated correction is authorized",
        "violations are enforced",
        "star-law rules are created",
        "autonomous execution is authorized",
        "civilization core is complete",
    ],
)
def test_positive_unsafe_text_claim_blocks_proposal(claim: str):
    report = _valid_review_gate_report()
    report["unsafe_text"] = claim

    assert _build(report)["status"] == "blocked"
