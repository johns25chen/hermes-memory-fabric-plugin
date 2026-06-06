from __future__ import annotations

from copy import deepcopy
import json

import pytest

from hermes_memory_fabric.governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal import (
    PROPOSAL_COMPONENTS,
    PROPOSAL_FALSE_FLAGS,
    PROPOSAL_OBJECT_FALSE_FLAGS,
    PROPOSED_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_COMPLETION_BOUNDARY_KEYS,
    PROPOSED_CHAIN_VERSIONS,
    PROPOSED_STAR_HUB_CHAIN_VERSIONS,
    READY_NEXT_ALLOWED_STEP,
    SENSITIVE_KEYS,
    build_governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal,
    governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal_to_json,
)
from tests.test_governed_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate import (
    _build as _valid_v2_46_review_gate,
)


TOP_LEVEL_FALSE_FLAGS = list(PROPOSAL_FALSE_FLAGS)
PROPOSAL_BOUNDARY_FALSE_FLAGS = list(PROPOSAL_OBJECT_FALSE_FLAGS)

UNSAFE_FIELDS = [
    "authorization_granted",
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
    "writes_files",
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
]

FORBIDDEN_CLAIMS = [
    "completion execution is performed",
    "completion execution is authorized",
    "completion record is created",
    "completion ledger entry is created",
    "finalization execution is performed",
    "finalization execution is authorized",
    "finalization record is created",
    "finalization ledger entry is created",
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
    return deepcopy(_valid_v2_46_review_gate())


def _build(report: dict[str, object] | None = None) -> dict[str, object]:
    return build_governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal(
        report or _valid_review_gate_report()
    )


def test_valid_finalization_boundary_review_gate_creates_completion_boundary_proposal_ready():
    result = _build()

    assert result["version"] == "2.47.0"
    assert (
        result["status"]
        == "star_law_candidate_rule_violation_response_audit_completion_boundary_proposal_ready"
    )
    assert result["source_review_gate_version"] == "2.46.0"
    for field in [
        "read_only",
        "read_only_memory",
        "proposal_only",
        "candidate_rule_violation_response_audit_completion_boundary_proposal_only",
        "star_law_candidate_rule_violation_response_audit_completion_boundary_proposal_only",
        "candidate_rule_violation_response_audit_completion_boundary_proposed_for_human_review_only",
        "candidate_rule_violation_response_audit_completion_boundary_review_gate_ready_for_human_review_only",
    ]:
        assert result[field] is True
    assert result["blocking_reasons"] == []
    assert all(check["passed"] is True for check in result["proposal_checks"])

    proposal = result[
        "star_law_candidate_rule_violation_response_audit_completion_boundary_proposal"
    ]
    assert (
        proposal["proposal_status"]
        == "star_law_candidate_rule_violation_response_audit_completion_boundary_proposed_for_human_review_only"
    )
    assert (
        proposal["boundary_type"]
        == "star_law_candidate_rule_violation_response_audit_completion_boundary_proposal"
    )
    assert proposal["source_review_gate_version"] == "2.46.0"
    assert (
        proposal[
            "candidate_rule_violation_response_audit_completion_boundary_proposed"
        ]
        is True
    )
    assert (
        proposal[
            "candidate_rule_violation_response_audit_completion_boundary_review_gate_ready_for_human_review_only"
        ]
        is True
    )
    assert (
        proposal[
            "source_star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate_valid"
        ]
        is True
    )
    assert (
        set(
            proposal[
                "star_law_candidate_rule_violation_response_audit_completion_boundary_components"
            ]
        )
        == PROPOSAL_COMPONENTS
    )


def test_proposed_chain_versions_exactly_match_v2_9_0_through_v2_46_0():
    expected = [f"v2.{minor}.0" for minor in range(9, 47)]

    assert PROPOSED_CHAIN_VERSIONS == expected
    assert _build()["proposed_chain_versions"] == expected


def test_proposed_star_hub_chain_versions_exactly_match_v2_19_0_through_v2_46_0():
    expected = [f"v2.{minor}.0" for minor in range(19, 47)]

    assert PROPOSED_STAR_HUB_CHAIN_VERSIONS == expected
    assert _build()["proposed_star_hub_chain_versions"] == expected


def test_blocked_finalization_boundary_review_gate_blocks_proposal():
    report = _valid_review_gate_report()
    report["status"] = "blocked"
    report["blocking_reasons"] = ["source_blocked"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert (
        result[
            "candidate_rule_violation_response_audit_completion_boundary_proposed_for_human_review_only"
        ]
        is False
    )
    proposal = result[
        "star_law_candidate_rule_violation_response_audit_completion_boundary_proposal"
    ]
    assert (
        proposal[
            "candidate_rule_violation_response_audit_completion_boundary_proposed"
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


@pytest.mark.parametrize("field", UNSAFE_FIELDS)
def test_unsafe_claim_blocks_proposal_and_output_stays_safe(field: str):
    report = _valid_review_gate_report()
    report[field] = True

    result = _build(report)

    assert result["status"] == "blocked"
    assert (
        result[
            "candidate_rule_violation_response_audit_completion_boundary_proposed_for_human_review_only"
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


def test_nested_completion_execution_claim_blocks_proposal():
    report = _valid_review_gate_report()
    review_gate = report[
        "star_law_candidate_rule_violation_response_audit_finalization_boundary_review_gate"
    ]
    assert isinstance(review_gate, dict)
    review_gate["candidate_rule_violation_response_audit_completion_executed"] = True

    assert _build(report)["status"] == "blocked"


@pytest.mark.parametrize(
    "field",
    [
        "completion_performed",
        "completion_authorized",
        "completion_executed",
        "completion_record_written",
        "completion_ledger_entry_written",
        "finalization_performed",
        "finalization_authorized",
        "finalization_executed",
        "closure_performed",
        "closure_authorized",
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


def test_malformed_reviewed_chain_versions_blocks_proposal():
    report = _valid_review_gate_report()
    report["reviewed_chain_versions"] = ["v2.9.0", "v2.45.0"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert result["proposed_chain_versions"] == PROPOSED_CHAIN_VERSIONS


def test_malformed_reviewed_star_hub_chain_versions_blocks_proposal():
    report = _valid_review_gate_report()
    report["reviewed_star_hub_chain_versions"] = ["v2.19.0", "v2.45.0"]

    result = _build(report)

    assert result["status"] == "blocked"
    assert (
        result["proposed_star_hub_chain_versions"]
        == PROPOSED_STAR_HUB_CHAIN_VERSIONS
    )


def test_proposed_completion_boundaries_are_proposal_only_and_non_authorizing():
    boundaries = _build()[
        "proposed_candidate_rule_violation_response_audit_completion_boundaries"
    ]

    assert isinstance(boundaries, dict)
    assert (
        set(boundaries)
        == PROPOSED_CANDIDATE_RULE_VIOLATION_RESPONSE_AUDIT_COMPLETION_BOUNDARY_KEYS
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
    serialized = governed_star_law_candidate_rule_violation_response_audit_completion_boundary_proposal_to_json(
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
def test_completion_boundary_proposal_preserves_non_authorization_flags(
    field: str,
):
    proposal = _build()[
        "star_law_candidate_rule_violation_response_audit_completion_boundary_proposal"
    ]
    assert proposal[field] is False


@pytest.mark.parametrize(
    "fields",
    [
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
def test_proposal_does_not_perform_or_create_governed_actions(
    fields: list[str],
):
    result = _build()
    proposal = result[
        "star_law_candidate_rule_violation_response_audit_completion_boundary_proposal"
    ]

    for field in fields:
        assert result[field] is False
        assert proposal[field] is False


def test_proposal_does_not_create_activate_enforce_or_autonomously_execute_rules():
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
    ]:
        assert result[field] is False


def test_proposal_does_not_enter_layers_authorize_handoff_write_openclaw_or_completion():
    result = _build()

    for field in [
        "enters_star_law_layer",
        "enters_star_soul_layer",
        "enters_star_cosmos_layer",
        "enters_star_source_layer",
        "handoff_authorized",
        "star_hub_handoff_authorized",
        "would_write_durable_memory",
        "memory_write_authorized",
        "would_mutate_memory_graph",
        "would_create_operation_ledger_entry",
        "openclaw_execution_authorized",
        "invokes_openclaw",
        "civilization_core_complete_claimed",
    ]:
        assert result[field] is False


def test_layer_mapping_is_correct():
    mapping = _build()["civilization_core_layer_mapping"]

    assert mapping["primary_layer"] == "星律记忆"
    assert mapping["primary_layer_status"] == (
        "Star-Law candidate rule violation response audit completion boundary proposal only, not completion execution, not completion record creation, not completion-ledger creation, not finalization execution, not closure execution, not audit execution, not audit logging, not audit record creation, not audit-ledger creation, not violation response execution, not automated correction, not violation enforcement, and not autonomous execution"
    )
    assert mapping["source_layer"] == "星律记忆"
    assert mapping["source_layer_status"] == (
        "Star-Law candidate rule violation response audit finalization boundary review gate complete for human review only"
    )
    assert all(
        layer in mapping["supporting_layers"]
        for layer in ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"]
    )
    assert mapping["direction"] == (
        "Star-Law candidate rule violation response audit finalization boundary review gate -> Star-Law candidate rule violation response audit completion boundary proposal"
    )


def test_next_allowed_step_is_v2_48_0_completion_boundary_review_gate():
    assert _build()["next_allowed_step"] == READY_NEXT_ALLOWED_STEP
    assert READY_NEXT_ALLOWED_STEP == (
        "v2.48.0 Star-Law candidate rule violation response audit completion boundary review gate"
    )
