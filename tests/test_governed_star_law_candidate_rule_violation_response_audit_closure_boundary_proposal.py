from __future__ import annotations

from copy import deepcopy
import json

import pytest

from hermes_memory_fabric.governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal import (
    PROPOSAL_COMPONENTS,
    PROPOSAL_FALSE_FLAGS,
    PROPOSAL_OBJECT_FALSE_FLAGS,
    PROPOSED_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_CLOSURE_BOUNDARY_KEYS,
    PROPOSED_CHAIN_VERSIONS,
    PROPOSED_STAR_HUB_CHAIN_VERSIONS,
    READY_NEXT_ALLOWED_STEP,
    SENSITIVE_KEYS,
    build_governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal,
    governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_to_json,
)
from tests.test_governed_star_law_candidate_rule_violation_response_audit_boundary_review_gate import (
    _build as _valid_v2_42_review_gate,
)


TOP_LEVEL_FALSE_FLAGS = list(PROPOSAL_FALSE_FLAGS)
PROPOSAL_BOUNDARY_FALSE_FLAGS = list(PROPOSAL_OBJECT_FALSE_FLAGS)

FORBIDDEN_CLAIMS = [
    "closure execution is performed",
    "closure execution is authorized",
    "closure record is created",
    "closure ledger entry is created",
    "audit execution is performed",
    "audit execution is authorized",
    "audit logging is performed",
    "audit log is created",
    "audit record is created",
    "audit ledger entries are created",
    "violation response is performed",
    "violation response is authorized",
    "violation response is executed",
    "automated correction is performed",
    "automated correction is authorized",
    "violations are enforced",
    "candidate rules are enforced",
    "star-law rules are created",
    "star-law rules are active",
    "star-law rules are enforced",
    "autonomous governance is created",
    "autonomous execution is authorized",
    "civilization core is complete",
]


def _valid_review_gate_report() -> dict[str, object]:
    return deepcopy(_valid_v2_42_review_gate())


def _build(report: dict[str, object] | None = None) -> dict[str, object]:
    return build_governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal(
        report or _valid_review_gate_report()
    )


def test_valid_candidate_rule_violation_response_audit_boundary_review_gate_creates_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_ready():
    result = _build()

    assert result["version"] == "2.43.0"
    assert (
        result["status"]
        == "star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_ready"
    )
    assert result["source_review_gate_version"] == "2.42.0"
    assert result["read_only"] is True
    assert result["read_only_memory"] is True
    assert result["proposal_only"] is True
    assert (
        result[
            "candidate_rule_violation_response_audit_closure_boundary_proposal_only"
        ]
        is True
    )
    assert (
        result[
            "star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_only"
        ]
        is True
    )
    assert (
        result[
            "candidate_rule_violation_response_audit_closure_boundary_proposed_for_human_review_only"
        ]
        is True
    )
    assert (
        result[
            "candidate_rule_violation_response_audit_closure_boundary_review_gate_ready_for_human_review_only"
        ]
        is True
    )
    assert all(check["passed"] is True for check in result["proposal_checks"])
    assert result["blocking_reasons"] == []
    proposal = result[
        "star_law_candidate_rule_violation_response_audit_closure_boundary_proposal"
    ]
    assert (
        proposal["proposal_status"]
        == "star_law_candidate_rule_violation_response_audit_closure_boundary_proposed_for_human_review_only"
    )
    assert (
        proposal["boundary_type"]
        == "star_law_candidate_rule_violation_response_audit_closure_boundary_proposal"
    )
    assert proposal["source_review_gate_version"] == "2.42.0"
    assert (
        proposal["candidate_rule_violation_response_audit_closure_boundary_proposed"]
        is True
    )
    assert (
        proposal[
            "candidate_rule_violation_response_audit_closure_boundary_review_gate_ready_for_human_review_only"
        ]
        is True
    )
    assert (
        proposal[
            "source_star_law_candidate_rule_violation_response_audit_boundary_review_gate_valid"
        ]
        is True
    )
    assert (
        set(
            proposal[
                "star_law_candidate_rule_violation_response_audit_closure_boundary_components"
            ]
        )
        == PROPOSAL_COMPONENTS
    )


def test_proposed_chain_versions_exactly_match_v2_9_0_through_v2_42_0():
    result = _build()

    assert result["proposed_chain_versions"] == PROPOSED_CHAIN_VERSIONS
    assert PROPOSED_CHAIN_VERSIONS == [
        "v2.9.0",
        "v2.10.0",
        "v2.11.0",
        "v2.12.0",
        "v2.13.0",
        "v2.14.0",
        "v2.15.0",
        "v2.16.0",
        "v2.17.0",
        "v2.18.0",
        "v2.19.0",
        "v2.20.0",
        "v2.21.0",
        "v2.22.0",
        "v2.23.0",
        "v2.24.0",
        "v2.25.0",
        "v2.26.0",
        "v2.27.0",
        "v2.28.0",
        "v2.29.0",
        "v2.30.0",
        "v2.31.0",
        "v2.32.0",
        "v2.33.0",
        "v2.34.0",
        "v2.35.0",
        "v2.36.0",
        "v2.37.0",
        "v2.38.0",
        "v2.39.0",
        "v2.40.0",
        "v2.41.0",
        "v2.42.0",
    ]
    assert (
        result[
            "star_law_candidate_rule_violation_response_audit_closure_boundary_proposal"
        ]["proposed_chain_versions"]
        == PROPOSED_CHAIN_VERSIONS
    )


def test_proposed_star_hub_chain_versions_exactly_match_v2_19_0_through_v2_42_0():
    result = _build()

    assert (
        result["proposed_star_hub_chain_versions"]
        == PROPOSED_STAR_HUB_CHAIN_VERSIONS
    )
    assert PROPOSED_STAR_HUB_CHAIN_VERSIONS == [
        "v2.19.0",
        "v2.20.0",
        "v2.21.0",
        "v2.22.0",
        "v2.23.0",
        "v2.24.0",
        "v2.25.0",
        "v2.26.0",
        "v2.27.0",
        "v2.28.0",
        "v2.29.0",
        "v2.30.0",
        "v2.31.0",
        "v2.32.0",
        "v2.33.0",
        "v2.34.0",
        "v2.35.0",
        "v2.36.0",
        "v2.37.0",
        "v2.38.0",
        "v2.39.0",
        "v2.40.0",
        "v2.41.0",
        "v2.42.0",
    ]


def test_blocked_candidate_rule_violation_response_audit_boundary_review_gate_blocks_proposal():
    report = _valid_review_gate_report()
    report["status"] = "blocked"
    report["blocking_reasons"] = ["source_blocked"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert (
        result[
            "candidate_rule_violation_response_audit_closure_boundary_proposed_for_human_review_only"
        ]
        is False
    )
    proposal = result[
        "star_law_candidate_rule_violation_response_audit_closure_boundary_proposal"
    ]
    assert (
        proposal["candidate_rule_violation_response_audit_closure_boundary_proposed"]
        is False
    )
    assert result["proposed_chain_versions"] == PROPOSED_CHAIN_VERSIONS
    assert (
        result["proposed_star_hub_chain_versions"]
        == PROPOSED_STAR_HUB_CHAIN_VERSIONS
    )
    assert result["blocking_reasons"]
    assert result["required_human_actions"]


@pytest.mark.parametrize(
    "field",
    [
        "authorization_granted",
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
        "candidate_rule_violation_response_performed",
        "candidate_rule_violation_response_authorized",
        "candidate_rule_violation_response_executed",
        "candidate_rule_violation_response_execution_authorized",
        "candidate_rule_violation_response_record_created",
        "candidate_rule_violation_response_ledger_entry_created",
        "automated_correction_performed",
        "automated_correction_authorized",
        "automated_correction_executed",
        "automated_correction_execution_authorized",
        "candidate_rule_violation_observation_performed",
        "candidate_rule_violation_observation_authorized",
        "candidate_rule_violation_observation_executed",
        "candidate_rule_violation_observation_execution_authorized",
        "candidate_rule_violation_detected",
        "candidate_rule_violation_recorded",
        "candidate_rule_violation_enforced",
        "candidate_rule_violation_ledger_entry_created",
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
        "self_executing_policy_created",
        "self_executing_policy_active",
        "enters_star_law_layer",
        "enters_star_soul_layer",
        "enters_star_cosmos_layer",
        "enters_star_source_layer",
        "civilization_core_complete_claimed",
        "star_hub_handoff_authorized",
        "handoff_authorized",
        "handoff_performed",
        "scheduling_performed",
        "would_schedule_anything",
        "dry_run_performed",
        "dry_run_executed",
        "would_execute_dry_run",
        "would_mutate_memory",
        "memory_write_authorized",
        "durable_memory_write_authorized",
        "would_write_durable_memory",
        "memory_graph_mutation_authorized",
        "would_mutate_memory_graph",
        "operation_ledger_creation_authorized",
        "would_create_operation_ledger_entry",
        "openclaw_execution_authorized",
        "invokes_openclaw",
        "would_call_github_api",
        "would_merge_pr",
        "would_create_tag",
        "would_create_approval_request",
        "would_submit_approval_request",
        "would_execute_approval_request",
        "approval_granted",
        "approval_authorized",
        "approval_request_authorized",
        "approval_request_created",
        "approval_request_submitted",
        "human_decision_recorded",
        "real_human_decision_recorded",
    ],
)
def test_unsafe_authorization_execution_write_audit_closure_or_boundary_claim_blocks_proposal(
    field: str,
):
    report = _valid_review_gate_report()
    report[field] = True

    result = _build(report)

    assert result["status"] == "blocked"
    assert (
        result[
            "candidate_rule_violation_response_audit_closure_boundary_proposed_for_human_review_only"
        ]
        is False
    )
    for safe_field in TOP_LEVEL_FALSE_FLAGS:
        assert result[safe_field] is False
    assert result["civilization_core_complete_claimed"] is False
    assert result["enters_star_law_layer"] is False
    assert result["enters_star_soul_layer"] is False
    assert result["enters_star_cosmos_layer"] is False
    assert result["enters_star_source_layer"] is False


def test_nested_closure_execution_claim_blocks_proposal():
    report = _valid_review_gate_report()
    review_gate = report[
        "star_law_candidate_rule_violation_response_audit_boundary_review_gate"
    ]
    assert isinstance(review_gate, dict)
    review_gate["candidate_rule_violation_response_audit_closure_executed"] = True

    result = _build(report)

    assert result["status"] == "blocked"
    assert result["candidate_rule_violation_response_audit_closure_executed"] is False


def test_malformed_reviewed_chain_versions_blocks_proposal():
    report = _valid_review_gate_report()
    report["reviewed_chain_versions"] = ["v2.9.0", "v2.42.0"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert result["proposed_chain_versions"] == PROPOSED_CHAIN_VERSIONS


def test_malformed_reviewed_star_hub_chain_versions_blocks_proposal():
    report = _valid_review_gate_report()
    report["reviewed_star_hub_chain_versions"] = ["v2.19.0", "v2.42.0"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert (
        result["proposed_star_hub_chain_versions"]
        == PROPOSED_STAR_HUB_CHAIN_VERSIONS
    )


def test_proposed_closure_boundaries_are_proposal_only_and_non_authorizing():
    result = _build()
    boundaries = result[
        "proposed_candidate_rule_violation_response_audit_closure_boundaries"
    ]

    assert isinstance(boundaries, dict)
    assert (
        set(boundaries)
        == PROPOSED_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_CLOSURE_BOUNDARY_KEYS
    )
    for boundary in boundaries.values():
        assert boundary["proposal_only"] is True
        for key, value in boundary.items():
            if key != "proposal_only":
                assert value is not True
    serialized = json.dumps(boundaries, ensure_ascii=True, sort_keys=True).lower()
    for forbidden_claim in FORBIDDEN_CLAIMS:
        assert forbidden_claim not in serialized


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
    serialized = governed_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_to_json(
        result
    )

    assert result["sensitive_field_count"] == len(SENSITIVE_KEYS)
    assert result["sensitive_fields_omitted"] is True
    assert "Sensitive fields were omitted" in serialized
    for sensitive_key in SENSITIVE_KEYS:
        assert sensitive_key not in serialized
    assert "do-not-leak" not in serialized
    json.loads(serialized)


@pytest.mark.parametrize("field", TOP_LEVEL_FALSE_FLAGS)
def test_proposal_preserves_top_level_non_authorization_flags(field: str):
    assert _build()[field] is False


@pytest.mark.parametrize("field", PROPOSAL_BOUNDARY_FALSE_FLAGS)
def test_star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_preserves_non_authorization_flags(
    field: str,
):
    assert (
        _build()[
            "star_law_candidate_rule_violation_response_audit_closure_boundary_proposal"
        ][field]
        is False
    )


def test_proposal_does_not_perform_closure_execution_or_create_closure_artifacts():
    result = _build()
    proposal = result[
        "star_law_candidate_rule_violation_response_audit_closure_boundary_proposal"
    ]

    for field in [
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
    ]:
        assert result[field] is False
        assert proposal[field] is False


def test_proposal_does_not_perform_audit_execution_or_create_audit_artifacts():
    result = _build()
    proposal = result[
        "star_law_candidate_rule_violation_response_audit_closure_boundary_proposal"
    ]

    for field in [
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
    ]:
        assert result[field] is False
        assert proposal[field] is False


def test_proposal_does_not_perform_authorize_execute_or_record_violation_response():
    result = _build()
    proposal = result[
        "star_law_candidate_rule_violation_response_audit_closure_boundary_proposal"
    ]

    for field in [
        "candidate_rule_violation_response_performed",
        "candidate_rule_violation_response_authorized",
        "candidate_rule_violation_response_executed",
        "candidate_rule_violation_response_execution_authorized",
        "candidate_rule_violation_response_record_created",
        "candidate_rule_violation_response_ledger_entry_created",
    ]:
        assert result[field] is False
        assert proposal[field] is False


def test_proposal_does_not_perform_authorize_or_execute_automated_correction():
    result = _build()
    proposal = result[
        "star_law_candidate_rule_violation_response_audit_closure_boundary_proposal"
    ]

    for field in [
        "automated_correction_performed",
        "automated_correction_authorized",
        "automated_correction_executed",
        "automated_correction_execution_authorized",
    ]:
        assert result[field] is False
        assert proposal[field] is False


def test_proposal_does_not_observe_detect_record_or_enforce_violations():
    result = _build()
    proposal = result[
        "star_law_candidate_rule_violation_response_audit_closure_boundary_proposal"
    ]

    for field in [
        "candidate_rule_violation_observation_performed",
        "candidate_rule_violation_observation_authorized",
        "candidate_rule_violation_observation_executed",
        "candidate_rule_violation_observation_execution_authorized",
        "candidate_rule_violation_detected",
        "candidate_rule_violation_recorded",
        "candidate_rule_violation_enforced",
        "candidate_rule_violation_ledger_entry_created",
    ]:
        assert result[field] is False
        assert proposal[field] is False


def test_proposal_does_not_enforce_authorize_activate_or_create_candidate_rules():
    result = _build()

    assert result["candidate_rule_enforcement_performed"] is False
    assert result["candidate_rule_enforcement_authorized"] is False
    assert result["candidate_rule_activation_performed"] is False
    assert result["candidate_rule_activation_authorized"] is False
    assert result["star_law_candidate_rules_created"] is False
    assert result["star_law_candidate_rules_activated"] is False
    assert result["star_law_candidate_rules_enforced"] is False


def test_proposal_does_not_create_activate_or_enforce_star_law_rules():
    result = _build()

    assert result["star_law_rules_created"] is False
    assert result["star_law_rules_activated"] is False
    assert result["star_law_rules_enforced"] is False
    assert result["star_law_self_enforcing_law_created"] is False
    assert result["star_law_self_enforcing_law_active"] is False


def test_proposal_does_not_create_autonomous_governance_or_authorize_execution():
    result = _build()

    assert result["autonomous_governance_created"] is False
    assert result["autonomous_execution_authorized"] is False
    assert (
        result["non_authorization_boundary"][
            "star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_ready_is_autonomous_execution"
        ]
        is False
    )


def test_proposal_does_not_enter_star_law_or_next_layers():
    result = _build()

    assert result["enters_star_law_layer"] is False
    assert result["enters_star_soul_layer"] is False
    assert result["enters_star_cosmos_layer"] is False
    assert result["enters_star_source_layer"] is False


def test_proposal_does_not_authorize_handoff_durable_memory_or_openclaw_execution():
    result = _build()

    assert result["handoff_authorized"] is False
    assert result["star_hub_handoff_authorized"] is False
    assert result["would_write_durable_memory"] is False
    assert result["memory_write_authorized"] is False
    assert result["openclaw_execution_authorized"] is False
    assert result["invokes_openclaw"] is False


def test_proposal_does_not_claim_civilization_core_completion():
    result = _build()

    assert result["civilization_core_complete_claimed"] is False
    assert (
        result["non_authorization_boundary"][
            "star_law_candidate_rule_violation_response_audit_closure_boundary_proposal_ready_is_civilization_core_completion"
        ]
        is False
    )


def test_layer_mapping_is_correct():
    result = _build()
    mapping = result["civilization_core_layer_mapping"]

    assert mapping["primary_layer"] == "星律记忆"
    assert mapping["primary_layer_status"] == (
        "Star-Law candidate rule violation response audit closure boundary proposal only, not closure execution, not audit execution, not audit logging, not audit record creation, not audit-ledger creation, not violation response execution, not automated correction, not violation enforcement, and not autonomous execution"
    )
    assert mapping["source_layer"] == "星律记忆"
    assert mapping["source_layer_status"] == (
        "Star-Law candidate rule violation response audit boundary review gate complete for human review only"
    )
    assert all(
        layer in mapping["supporting_layers"]
        for layer in ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"]
    )
    assert mapping["direction"] == (
        "Star-Law candidate rule violation response audit boundary review gate -> Star-Law candidate rule violation response audit closure boundary proposal"
    )


def test_next_allowed_step_is_v2_44_0_star_law_candidate_rule_violation_response_audit_closure_boundary_review_gate():
    assert _build()["next_allowed_step"] == READY_NEXT_ALLOWED_STEP
    assert READY_NEXT_ALLOWED_STEP == (
        "v2.44.0 Star-Law candidate rule violation response audit closure boundary review gate"
    )
