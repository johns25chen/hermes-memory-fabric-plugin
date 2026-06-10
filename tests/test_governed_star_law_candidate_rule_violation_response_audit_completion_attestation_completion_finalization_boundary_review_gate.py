from __future__ import annotations

from copy import deepcopy
import json

import pytest

from hermes_memory_fabric.governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate import (
    LAYER_MAPPING,
    READY_NEXT_ALLOWED_STEP,
    REVIEWED_CHAIN_VERSIONS,
    REVIEWED_STAR_HUB_CHAIN_VERSIONS,
    REVIEW_COMPONENTS,
    REVIEW_GATE_FALSE_FLAGS,
    REVIEW_OBJECT_FALSE_FLAGS,
    SENSITIVE_KEYS,
    SOURCE_PROPOSED_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_COMPLETION_ATTESTATION_COMPLETION_FINALIZATION_BOUNDARY_KEYS,
    build_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate,
    governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate_to_json,
)
from tests.test_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal import (
    _build as _valid_v2_59_proposal,
)


def _valid_proposal_report() -> dict[str, object]:
    return deepcopy(_valid_v2_59_proposal())


def _build(report: dict[str, object] | None = None) -> dict[str, object]:
    return build_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate(
        report or _valid_proposal_report()
    )


def test_valid_v2_59_finalization_boundary_proposal_creates_v2_60_review_gate_ready():
    result = _build()

    assert result["version"] == "2.60.0"
    assert (
        result["status"]
        == "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate_ready"
    )
    assert result["source_proposal_version"] == "2.59.0"
    for field in [
        "read_only",
        "read_only_memory",
        "review_gate_only",
        "candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate_only",
        "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate_only",
        "twelfth_memory_layer_final_star_law_boundary_review_gate_only",
        "twelfth_memory_layer_final_star_law_boundary_reviewed_for_human_review_only",
        "star_soul_memory_continuity_boundary_proposal_ready_for_human_review_only",
    ]:
        assert result[field] is True
    assert result["blocking_reasons"] == []
    assert all(check["passed"] is True for check in result["review_gate_checks"])

    review_gate = result[
        "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate"
    ]
    assert (
        review_gate["review_status"]
        == "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_reviewed_for_human_review_only"
    )
    assert (
        review_gate["boundary_type"]
        == "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate"
    )
    assert (
        review_gate[
            "candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_reviewed"
        ]
        is True
    )
    assert (
        review_gate[
            "candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_structurally_review_ready"
        ]
        is True
    )
    assert (
        review_gate[
            "source_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal_valid"
        ]
        is True
    )
    assert (
        review_gate[
            "star_soul_memory_continuity_boundary_proposal_ready_for_human_review_only"
        ]
        is True
    )
    assert (
        review_gate[
            "twelfth_memory_layer_final_star_law_boundary_reviewed_for_human_review_only"
        ]
        is True
    )
    assert (
        set(
            review_gate[
                "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_components"
            ]
        )
        == REVIEW_COMPONENTS
    )


def test_reviewed_chain_versions_exactly_match_v2_9_0_through_v2_59_0():
    expected = [f"v2.{minor}.0" for minor in range(9, 60)]

    assert REVIEWED_CHAIN_VERSIONS == expected
    assert _build()["reviewed_chain_versions"] == expected


def test_reviewed_star_hub_chain_versions_exactly_match_v2_19_0_through_v2_59_0():
    expected = [f"v2.{minor}.0" for minor in range(19, 60)]

    assert REVIEWED_STAR_HUB_CHAIN_VERSIONS == expected
    assert _build()["reviewed_star_hub_chain_versions"] == expected


def test_blocked_source_proposal_blocks_review_gate():
    report = _valid_proposal_report()
    report["status"] = "blocked"
    report["blocking_reasons"] = ["source_blocked"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert (
        result[
            "twelfth_memory_layer_final_star_law_boundary_reviewed_for_human_review_only"
        ]
        is False
    )
    assert (
        result[
            "star_soul_memory_continuity_boundary_proposal_ready_for_human_review_only"
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


@pytest.mark.parametrize("field", sorted(REVIEW_GATE_FALSE_FLAGS))
def test_any_unsafe_true_flag_blocks_review_gate_and_output_stays_false(field: str):
    report = _valid_proposal_report()
    report[field] = True

    result = _build(report)

    assert result["status"] == "blocked"
    assert result[field] is False


@pytest.mark.parametrize(
    "field",
    [
        "finalization_performed",
        "finalization_authorized",
        "finalization_executed",
        "finalization_record_written",
        "finalization_ledger_entry_written",
        "completion_performed",
        "completion_authorized",
        "completion_executed",
        "completion_record_written",
        "completion_ledger_entry_written",
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
        "audit_log_written",
        "audit_record_written",
        "audit_ledger_entry_written",
        "violation_response_audit_performed",
        "violation_response_audit_authorized",
        "violation_response_audit_executed",
        "automated_correction_performed",
        "automated_correction_authorized",
        "automated_correction_executed",
        "violation_enforced",
        "candidate_rules_enforced",
        "candidate_rules_created",
        "candidate_rules_activated",
        "autonomous_governance_created",
        "autonomous_execution_authorized",
        "enters_star_law_layer",
        "enters_star_soul_layer",
        "enters_star_cosmos_layer",
        "enters_star_source_layer",
        "star_soul_transition_executed",
        "star_soul_transition_authorized",
        "enters_thirteenth_memory_layer",
        "thirteenth_memory_layer_transition_authorized",
        "v3_created",
        "v3_authorized",
        "civilization_core_complete_claimed",
        "handoff_authorized",
        "star_hub_scheduling_authorized",
        "dry_run_executed",
        "would_write_durable_memory",
        "would_mutate_memory_graph",
        "operation_ledger_entry_created",
        "openclaw_called",
        "github_api_called",
        "approval_granted",
        "human_decision_recorded",
    ],
)
def test_unsafe_nested_claim_blocks_review_gate(field: str):
    report = _valid_proposal_report()
    report["unsafe_nested_claim"] = {field: True}

    assert _build(report)["status"] == "blocked"


def test_unsafe_nested_source_proposal_flag_blocks_review_gate():
    report = _valid_proposal_report()
    proposal = report[
        "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal"
    ]
    assert isinstance(proposal, dict)
    proposal[
        "candidate_rule_violation_response_audit_completion_attestation_completion_finalization_authorized"
    ] = True

    assert _build(report)["status"] == "blocked"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("version", "2.58.0"),
        ("read_only", False),
        ("read_only_memory", False),
        ("proposal_only", False),
        (
            "candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal_only",
            False,
        ),
        (
            "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_proposal_only",
            False,
        ),
        ("next_allowed_step", "wrong"),
        ("blocking_reasons", ["blocked"]),
    ],
)
def test_missing_or_invalid_required_source_field_blocks_review_gate(
    field: str, value: object
):
    report = _valid_proposal_report()
    report[field] = value

    assert _build(report)["status"] == "blocked"


def test_malformed_proposed_chain_versions_blocks_review_gate():
    report = _valid_proposal_report()
    report["proposed_chain_versions"] = ["v2.59.0"]

    assert _build(report)["status"] == "blocked"


def test_malformed_proposed_star_hub_chain_versions_blocks_review_gate():
    report = _valid_proposal_report()
    report["proposed_star_hub_chain_versions"] = ["v2.59.0"]

    assert _build(report)["status"] == "blocked"


def test_malformed_proposed_boundaries_block_review_gate():
    report = _valid_proposal_report()
    report[
        "proposed_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundaries"
    ] = {
        "unsafe": {
            "proposal_only": True,
            "finalization_execution_performed": True,
        }
    }

    assert _build(report)["status"] == "blocked"


def test_reviewed_finalization_boundaries_are_review_only_and_non_authorizing():
    boundaries = _build()[
        "reviewed_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundaries"
    ]

    assert isinstance(boundaries, dict)
    assert (
        set(boundaries)
        == SOURCE_PROPOSED_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_COMPLETION_ATTESTATION_COMPLETION_FINALIZATION_BOUNDARY_KEYS
    )
    for boundary in boundaries.values():
        assert boundary["review_only"] is True
        for key, value in boundary.items():
            if key != "review_only":
                assert value is not True


def test_sensitive_field_names_and_values_are_not_leaked_in_serialized_output():
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
    serialized = governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate_to_json(
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
        "star_law_candidate_rule_violation_response_audit_completion_attestation_completion_finalization_boundary_review_gate"
    ]

    assert review_gate[field] is False


def test_review_gate_does_not_execute_transition_write_or_external_actions():
    result = _build()

    for field in [
        "enters_star_law_layer",
        "enters_star_soul_layer",
        "enters_star_cosmos_layer",
        "enters_star_source_layer",
        "star_soul_transition_executed",
        "star_soul_transition_authorized",
        "enters_thirteenth_memory_layer",
        "thirteenth_memory_layer_transition_authorized",
        "v3_created",
        "v3_authorized",
        "civilization_core_complete_claimed",
        "handoff_authorized",
        "star_hub_handoff_authorized",
        "scheduling_performed",
        "dry_run_performed",
        "dry_run_executed",
        "memory_write_authorized",
        "would_write_durable_memory",
        "would_mutate_memory_graph",
        "would_create_operation_ledger_entry",
        "operation_ledger_entry_created",
        "invokes_openclaw",
        "openclaw_execution_authorized",
        "would_call_github_api",
        "approval_granted",
        "human_decision_recorded",
    ]:
        assert result[field] is False


def test_layer_mapping_twelfth_layer_boundary_and_next_step_are_exact():
    result = _build()

    assert result["civilization_core_layer_mapping"] == LAYER_MAPPING
    assert LAYER_MAPPING == {
        "primary_layer": "星律记忆",
        "primary_layer_status": "Star-Law candidate rule violation response audit completion attestation completion finalization boundary review gate only, not finalization execution, not finalization record creation, not finalization-ledger creation, not completion execution, not completion record creation, not completion-ledger creation, not closure execution, not closure record creation, not closure-ledger creation, not attestation execution, not attestation record creation, not attestation-ledger creation, not audit execution, not audit logging, not audit record creation, not audit-ledger creation, not violation response execution, not automated correction, not violation enforcement, not autonomous execution, and not Star-Soul transition execution",
        "source_layer": "星律记忆",
        "source_layer_status": "Star-Law candidate rule violation response audit completion attestation completion finalization boundary proposal complete for human review only",
        "supporting_layers": ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"],
        "direction": "Star-Law candidate rule violation response audit completion attestation completion finalization boundary proposal -> Star-Law candidate rule violation response audit completion attestation completion finalization boundary review gate",
        "hard_boundary": "v2.60.0 is the final v2.x Star-Law memory layer review gate before a later separate v3.0.0 Star-Soul Memory continuity boundary proposal",
    }
    hard_boundary = result["twelfth_memory_layer_hard_boundary"]
    assert hard_boundary["memory_layer"] == "星律记忆"
    assert hard_boundary["memory_layer_number"] == 12
    assert hard_boundary["final_v2_x_star_law_boundary"] is True
    assert hard_boundary["enters_thirteenth_memory_layer"] is False
    assert hard_boundary["thirteenth_memory_layer_transition_authorized"] is False
    assert hard_boundary["star_soul_transition_authorized"] is False
    assert hard_boundary["v3_created"] is False
    assert result["next_allowed_step"] == READY_NEXT_ALLOWED_STEP
    assert (
        READY_NEXT_ALLOWED_STEP
        == "v3.0.0 Star-Soul Memory continuity boundary proposal"
    )


@pytest.mark.parametrize(
    "claim",
    [
        "finalization execution is performed",
        "finalization execution is authorized",
        "finalization record is created",
        "finalization-ledger entries are created",
        "completion execution is performed",
        "closure execution is authorized",
        "attestation execution is performed",
        "audit logging is performed",
        "violation response is executed",
        "automated correction is authorized",
        "violations are enforced",
        "candidate rules are enforced",
        "star-law rules are created",
        "autonomous execution is authorized",
        "civilization core is complete",
        "star-soul transition is authorized",
        "v3 is created",
        "the thirteenth memory layer has been entered",
    ],
)
def test_positive_unsafe_text_claim_blocks_review_gate(claim: str):
    report = _valid_proposal_report()
    report["unsafe_text"] = claim

    assert _build(report)["status"] == "blocked"
