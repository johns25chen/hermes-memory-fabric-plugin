from __future__ import annotations

import argparse
import io
import json
import tomllib
from pathlib import Path

from hermes_memory_fabric.p4_m0_subspace_operator import build_parser, run_operator_command
from hermes_memory_fabric.p4_m2_execution_decision_silence_non_consent_map import (
    EXECUTION_DECISION_SILENCE_NON_CONSENT_MAP_BOUNDARY,
    ExecutionDecisionSilenceNonConsentMapField,
    execution_decision_silence_non_consent_map_as_dicts,
    execution_decision_silence_non_consent_map_field_ids,
    execution_decision_silence_non_consent_map_report,
    list_execution_decision_silence_non_consent_map_fields,
    render_execution_decision_silence_non_consent_map_markdown,
)


FIELD_IDS = (
    "execution-decision-silence-non-consent-map-id",
    "execution-decision-default-denial-boundary-map-reference",
    "execution-decision-recommendation-prohibition-map-reference",
    "execution-decision-non-equivalence-map-reference",
    "manual-decision-reference",
    "operator-reference",
    "human-confirmation-snapshot-reference",
    "manual-authorization-evidence-envelope-reference",
    "execution-preconditions-snapshot-map-reference",
    "execution-risk-acknowledgement-map-reference",
    "execution-risk-acceptance-prohibition-map-reference",
    "execution-risk-waiver-prohibition-map-reference",
    "execution-surface-reference",
    "execution-contract-validation-matrix-reference",
    "silence-non-consent-boundary-category",
    "missing-evidence-as-consent-prohibition-signal",
    "consent-semantics-disabled",
)

DATACLASS_FIELDS = {
    "field_order",
    "field_id",
    "field_name",
    "field_purpose",
    "silence_non_consent_boundary_category",
    "missing_evidence_as_consent_prohibition_signal",
    "consent_semantics_disabled",
    "non_consent_execution_semantics_disabled",
}

EXPECTED_MEMORY_LOOP_COMMANDS = {
    "checklist",
    "review-status",
    "recall-verification-status",
    "lifecycle-verification-status",
    "do-not-retry-verification-status",
    "source-provenance-verification-status",
    "decision-readiness-status",
    "manual-decision-preview",
    "governance-pack-export",
    "final-boundary-audit",
    "manual-execution-hardening",
    "execution-surface-contract",
    "execution-contract-validation-matrix",
    "manual-authorization-evidence-envelope",
    "human-confirmation-snapshot-contract",
    "execution-preconditions-snapshot-map",
    "execution-risk-acknowledgement-map",
    "execution-risk-acceptance-prohibition-map",
    "execution-risk-waiver-prohibition-map",
    "execution-decision-non-equivalence-map",
    "execution-decision-recommendation-prohibition-map",
    "execution-decision-default-denial-boundary-map",
    "execution-decision-silence-non-consent-map",
    "execution-decision-negative-evidence-non-override-map",
    "execution-decision-conflicting-evidence-isolation-map",
    "execution-decision-evidence-precedence-prohibition-map",
    "final-non-execution-boundary-audit",
    "p4-m2-closure-handoff-contract",
    "governed-transition-intake-boundary-contract",
    "governed-transition-intake-request-envelope-contract",
    "governed-transition-intake-evidence-reference-envelope-contract",
    "governed-transition-intake-declared-human-context-envelope-contract",
    "governed-transition-intake-target-phase-envelope-contract",
    "governed-transition-intake-declared-transition-reason-envelope-contract",
    "governed-transition-intake-declared-transition-constraint-envelope-contract",
        "governed-transition-intake-declared-transition-dependency-envelope-contract",
    "governed-transition-intake-declared-transition-impact-envelope-contract",
    "governed-transition-intake-declared-transition-risk-envelope-contract",
    "governed-transition-intake-declared-transition-assumption-envelope-contract",
    "governed-transition-intake-declared-transition-safeguard-envelope-contract",
    "governed-transition-intake-package-assembly-envelope-contract",
    "governed-transition-intake-final-non-validation-boundary-audit",
    "governed-transition-intake-closure-handoff-contract",
    "governed-transition-intake-phase-closure-review",
    "governed-transition-intake-final-phase-handoff-summary",
    "entry-gate-design-boundary-contract",
    "entry-gate-design-request-envelope-contract",
    "evidence-reference-envelope-contract",
    "declared-human-context-envelope-contract",
    "target-phase-envelope-contract",
    "declared-transition-reason-envelope-contract",
    "declared-transition-constraint-envelope-contract",
    "declared-transition-dependency-envelope-contract",
}

PREVIOUS_P4_M2_11_READ_ONLY_COMMANDS = EXPECTED_MEMORY_LOOP_COMMANDS - {
    "execution-decision-silence-non-consent-map"
}

BOUNDARY_PHRASES = (
    "P4-M2.12",
    "Execution Decision Silence Non-Consent Map",
    "read-only",
    "definition-only",
    "inspection-only",
    "silence is not consent",
    "non-response is not consent",
    "missing record is not consent",
    "missing evidence is not consent",
    "missing objection is not approval",
    "missing rejection is not approval",
    "missing denial is not permission",
    "no execution",
    "no decision execution",
    "no confirmation",
    "no decision confirmation",
    "no authorization",
    "no decision authorization",
    "no approval",
    "no default approval",
    "no decision approval",
    "no rejection",
    "no live rejection",
    "no active denial",
    "no decision rejection",
    "no consent validation",
    "no live consent validation",
    "no consent record creation",
    "no non-consent record creation",
    "no risk acceptance",
    "no risk waiver",
    "no implied risk acceptance",
    "no implied risk waiver",
    "no acknowledgement-as-acceptance",
    "no acknowledgement-as-waiver",
    "no acceptance-prohibition-as-waiver",
    "no absence-of-acceptance-as-waiver",
    "no silence-as-consent",
    "no silence-as-authorization",
    "no silence-as-confirmation",
    "no silence-as-approval",
    "no silence-as-recommendation",
    "no silence-as-readiness",
    "no silence-as-validation",
    "no silence-as-risk-acceptance",
    "no silence-as-risk-waiver",
    "no non-response-as-consent",
    "no missing-record-as-consent",
    "no missing-evidence-as-consent",
    "no missing-objection-as-approval",
    "no missing-rejection-as-approval",
    "no missing-denial-as-permission",
    "no missing-confirmation-as-confirmation",
    "no missing-authorization-as-authorization",
    "no missing-recommendation-as-recommendation",
    "no missing-readiness-as-readiness",
    "no missing-validation-as-validation",
    "no missing-risk-acceptance-as-risk-acceptance",
    "no missing-risk-waiver-as-risk-waiver",
    "no absence-as-permission",
    "no absence-as-approval",
    "no absence-as-recommendation",
    "no absence-as-readiness",
    "no absence-as-validation",
    "no absence-as-authorization",
    "no absence-as-confirmation",
    "no absence-as-risk-acceptance",
    "no absence-as-risk-waiver",
    "no waiver evidence creation",
    "no waiver approval",
    "no waiver authorization",
    "no manual-decision-as-execution",
    "no manual-decision-as-authorization",
    "no manual-decision-as-confirmation",
    "no manual-decision-as-approval",
    "no manual-decision-as-recommendation",
    "no operator-as-authorization",
    "no operator-as-confirmation",
    "no operator-as-approval",
    "no operator-as-recommendation",
    "no risk-map-as-readiness",
    "no risk-map-as-validation",
    "no risk-map-as-recommendation",
    "no non-equivalence-map-as-recommendation",
    "no recommendation-map-as-approval",
    "no recommendation-map-as-readiness",
    "no default-denial-map-as-consent",
    "no default-denial-map-as-execution",
    "no reference-as-verdict",
    "no reference-as-execution",
    "no reference-as-authorization",
    "no reference-as-confirmation",
    "no reference-as-approval",
    "no reference-as-recommendation",
    "no reference-as-consent",
    "no decision recommendation",
    "no decision ranking",
    "no suggested next action",
    "no default readiness",
    "no default allow",
    "no default permit",
    "no default continue",
    "no default execute",
    "no default mutate",
    "no auto-pass",
    "no auto-execution hint",
    "no advisory verdict",
    "no execution hint",
    "no authorization hint",
    "no confirmation hint",
    "no readiness hint",
    "no validation hint",
    "no live risk acknowledgement",
    "no memory mutation",
    "no memory record creation",
    "no memory record update",
    "no memory record deletion",
    "no proposal mutation",
    "no lifecycle mutation",
    "no retry policy mutation",
    "no source fetching",
    "no provenance writing",
    "no evidence mutation",
    "no citation mutation",
    "no live confirmation validation",
    "no live authorization validation",
    "no live contract validation",
    "no input validation",
    "no record validation",
    "no validation verdict",
    "no readiness verdict",
    "no automatic readiness verdict",
    "no consent semantics",
    "no non-consent execution semantics",
    "no decision equivalence semantics",
    "no recommendation semantics",
    "no ranking semantics",
    "no next-action semantics",
    "no default-allowance semantics",
    "no permission semantics",
    "no denial execution semantics",
    "no rejection execution semantics",
    "no acceptance semantics",
    "no waiver semantics",
    "no acknowledgement semantics",
    "no confirmation semantics",
    "no authorization semantics",
    "no execution semantics",
    "no API",
    "no MCP",
    "no connector",
    "no agent call",
    "no Codex/Hermes/ChatGPT product-code auto-call",
    "no P4-M3",
    "no P4-M4",
    "no P4-M5",
    "no v7",
    "no productization",
    "no UI",
    "no Operator Console",
    "no MVP",
    "no deploy",
    "no full Memory Graph",
)

TRUE_STATUS_FLAGS = (
    "definition_only",
    "inspection_only",
    "p4_m2_started",
    "execution_surface_contract_definition_available",
    "execution_contract_validation_matrix_available",
    "manual_authorization_evidence_envelope_available",
    "human_confirmation_snapshot_contract_available",
    "execution_preconditions_snapshot_map_available",
    "execution_risk_acknowledgement_map_available",
    "execution_risk_acceptance_prohibition_map_available",
    "execution_risk_waiver_prohibition_map_available",
    "execution_decision_non_equivalence_map_available",
    "execution_decision_recommendation_prohibition_map_available",
    "execution_decision_default_denial_boundary_map_available",
    "execution_decision_silence_non_consent_map_started",
    "execution_decision_silence_non_consent_map_definition_only",
    "decision_silence_non_consent_map_fields_defined",
    "silence_as_consent_prohibited",
    "non_response_as_consent_prohibited",
    "missing_record_as_consent_prohibited",
    "missing_evidence_as_consent_prohibited",
    "missing_objection_as_approval_prohibited",
    "missing_rejection_as_approval_prohibited",
    "missing_denial_as_permission_prohibited",
    "missing_confirmation_as_confirmation_prohibited",
    "missing_authorization_as_authorization_prohibited",
    "missing_recommendation_as_recommendation_prohibited",
    "missing_readiness_as_readiness_prohibited",
    "missing_validation_as_validation_prohibited",
    "missing_risk_acceptance_as_risk_acceptance_prohibited",
    "missing_risk_waiver_as_risk_waiver_prohibited",
    "consent_semantics_disabled",
    "non_consent_execution_semantics_disabled",
    "default_denial_map_as_consent_prohibited",
    "default_denial_map_as_execution_prohibited",
    "reference_as_consent_prohibited",
)

DISABLED_STATUS_FLAGS = (
    "execution_enabled",
    "decision_execution_enabled",
    "confirmation_enabled",
    "decision_confirmation_enabled",
    "authorization_enabled",
    "decision_authorization_enabled",
    "approval_enabled",
    "default_approval_enabled",
    "decision_approval_enabled",
    "rejection_enabled",
    "live_rejection_enabled",
    "active_denial_enabled",
    "decision_rejection_enabled",
    "consent_validation_enabled",
    "live_consent_validation_enabled",
    "consent_record_creation_enabled",
    "non_consent_record_creation_enabled",
    "risk_acceptance_enabled",
    "risk_waiver_enabled",
    "implied_risk_acceptance_enabled",
    "implied_risk_waiver_enabled",
    "acknowledgement_as_acceptance_enabled",
    "acknowledgement_as_waiver_enabled",
    "acceptance_prohibition_as_waiver_enabled",
    "absence_of_acceptance_as_waiver_enabled",
    "waiver_evidence_creation_enabled",
    "waiver_approval_enabled",
    "waiver_authorization_enabled",
    "live_risk_acknowledgement_enabled",
    "memory_mutation_enabled",
    "memory_record_creation_enabled",
    "memory_record_update_enabled",
    "memory_record_deletion_enabled",
    "proposal_mutation_enabled",
    "lifecycle_mutation_enabled",
    "retry_policy_mutation_enabled",
    "source_fetching_enabled",
    "provenance_writing_enabled",
    "evidence_mutation_enabled",
    "citation_mutation_enabled",
    "live_confirmation_validation_enabled",
    "live_authorization_validation_enabled",
    "live_contract_validation_enabled",
    "input_validation_enabled",
    "record_validation_enabled",
    "validation_verdict_enabled",
    "readiness_verdict_enabled",
    "automatic_readiness_verdict_enabled",
    "decision_recommendation_enabled",
    "decision_ranking_enabled",
    "suggested_next_action_enabled",
    "default_readiness_enabled",
    "auto_pass_enabled",
    "auto_execution_hint_enabled",
    "advisory_verdict_enabled",
    "execution_hint_enabled",
    "authorization_hint_enabled",
    "confirmation_hint_enabled",
    "readiness_hint_enabled",
    "validation_hint_enabled",
    "default_allow_enabled",
    "default_permit_enabled",
    "default_continue_enabled",
    "default_execute_enabled",
    "default_mutate_enabled",
    "consent_semantics_granted",
    "non_consent_execution_semantics_granted",
    "decision_equivalence_semantics_granted",
    "recommendation_semantics_granted",
    "ranking_semantics_granted",
    "next_action_semantics_granted",
    "default_allowance_semantics_granted",
    "permission_semantics_granted",
    "denial_execution_semantics_granted",
    "rejection_execution_semantics_granted",
    "acceptance_semantics_granted",
    "waiver_semantics_granted",
    "acknowledgement_semantics_granted",
    "confirmation_semantics_granted",
    "authorization_semantics_granted",
    "execution_semantics_granted",
    "api_enabled",
    "mcp_enabled",
    "connector_enabled",
    "agent_call_enabled",
    "codex_hermes_chatgpt_product_code_auto_call_enabled",
    "p4_m3_started",
    "p4_m4_started",
    "p4_m5_started",
    "v7_started",
    "productization_started",
    "ui_started",
    "operator_console_started",
    "mvp_started",
    "deploy_started",
    "full_memory_graph_started",
)

PROHIBITED_MEMORY_LOOP_COMMANDS = {
    "confirm",
    "authorization",
    "approve",
    "reject",
    "execute",
    "recommend-decision",
    "rank-decision",
    "suggest-next-action",
    "validate-consent",
    "create-consent-record",
    "create-non-consent-record",
    "write-memory",
    "create-memory",
    "update-memory",
    "delete-memory",
    "mutate-proposal",
    "fetch-source",
    "write-provenance",
    "mutate-evidence",
    "mutate-citation",
    "call-agent",
    "API",
    "MCP",
    "connector",
    "start-p4-m3",
    "start-p4-m4",
    "start-p4-m5",
    "start-v7",
    "productize",
    "operator-console",
    "ui",
    "deploy",
}


def test_silence_non_consent_map_field_order_count_and_ids_are_stable():
    fields = list_execution_decision_silence_non_consent_map_fields()

    assert [field.field_order for field in fields] == list(range(1, 18))
    assert len(fields) == 17
    assert execution_decision_silence_non_consent_map_field_ids() == FIELD_IDS


def test_every_silence_non_consent_map_field_has_required_non_empty_values():
    for field in list_execution_decision_silence_non_consent_map_fields():
        assert field.field_name.strip()
        assert field.field_purpose.strip()
        assert field.silence_non_consent_boundary_category.strip()
        assert field.missing_evidence_as_consent_prohibition_signal.strip()
        assert field.consent_semantics_disabled.strip()
        assert field.non_consent_execution_semantics_disabled.strip()


def test_markdown_output_is_stable_and_contains_required_boundaries():
    first = render_execution_decision_silence_non_consent_map_markdown()
    second = render_execution_decision_silence_non_consent_map_markdown()

    assert first == second
    assert first.startswith("# P4-M2.12 Execution Decision Silence Non-Consent Map\n")
    assert EXECUTION_DECISION_SILENCE_NON_CONSENT_MAP_BOUNDARY in first
    for field_id in FIELD_IDS:
        assert field_id in first
    for phrase in BOUNDARY_PHRASES:
        assert phrase in first


def test_json_output_is_stable_and_contains_required_boundaries(tmp_path):
    args = [
        "memory-loop",
        "execution-decision-silence-non-consent-map",
        "--workspace-root",
        str(tmp_path),
        "--format",
        "json",
    ]
    first_code, first_payload, first_stderr, first_stdout = _run_operator(args)
    second_code, second_payload, second_stderr, second_stdout = _run_operator(args)

    assert first_code == 0
    assert second_code == 0
    assert first_stderr == ""
    assert second_stderr == ""
    assert first_stdout == second_stdout
    assert first_payload == second_payload
    assert first_payload["boundary"] == EXECUTION_DECISION_SILENCE_NON_CONSENT_MAP_BOUNDARY
    assert first_payload["count"] == 17
    assert first_payload["status"] == execution_decision_silence_non_consent_map_report()
    assert [item["field_id"] for item in first_payload["fields"]] == list(FIELD_IDS)
    assert set(first_payload["fields"][0]) == DATACLASS_FIELDS
    for phrase in BOUNDARY_PHRASES:
        assert phrase in first_stdout
    assert not (tmp_path / ".local").exists()


def test_dict_conversion_and_status_report_are_deterministic():
    first_fields = execution_decision_silence_non_consent_map_as_dicts()
    second_fields = execution_decision_silence_non_consent_map_as_dicts()
    first_status = execution_decision_silence_non_consent_map_report()
    second_status = execution_decision_silence_non_consent_map_report()

    assert first_fields == second_fields
    assert [field["field_id"] for field in first_fields] == list(FIELD_IDS)
    assert first_status == second_status
    assert first_status["phase"] == "P4-M2.12"
    assert first_status["feature"] == "Execution Decision Silence Non-Consent Map"
    assert first_status["mode"] == "read-only"
    assert first_status["execution_decision_silence_non_consent_map_field_count"] == 17
    assert first_status["boundary"] == EXECUTION_DECISION_SILENCE_NON_CONSENT_MAP_BOUNDARY


def test_status_report_locks_true_and_disabled_flags():
    status = execution_decision_silence_non_consent_map_report()

    for flag in TRUE_STATUS_FLAGS:
        assert status[flag] is True
    for flag in DISABLED_STATUS_FLAGS:
        assert status[flag] is False


def test_operator_markdown_default_is_read_only_and_creates_no_local_storage(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "execution-decision-silence-non-consent-map",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M2.12 Execution Decision Silence Non-Consent Map\n")
    assert "## Status Report" in stdout
    assert EXECUTION_DECISION_SILENCE_NON_CONSENT_MAP_BOUNDARY in stdout
    for phrase in BOUNDARY_PHRASES:
        assert phrase in stdout
    assert not (tmp_path / ".local").exists()


def test_operator_markdown_format_is_explicit_and_stable(tmp_path):
    args = [
        "memory-loop",
        "execution-decision-silence-non-consent-map",
        "--workspace-root",
        str(tmp_path),
        "--format",
        "markdown",
    ]
    first_code, first_payload, first_stderr, first_stdout = _run_operator(args)
    second_code, second_payload, second_stderr, second_stdout = _run_operator(args)

    assert first_code == 0
    assert second_code == 0
    assert first_payload == {}
    assert second_payload == {}
    assert first_stderr == ""
    assert second_stderr == ""
    assert first_stdout == second_stdout
    assert first_stdout.startswith("# P4-M2.12 Execution Decision Silence Non-Consent Map\n")
    assert not (tmp_path / ".local").exists()


def test_command_does_not_instantiate_writable_store(monkeypatch, tmp_path):
    def fail_store_creation(*_args, **_kwargs):
        raise AssertionError("writable store must not be instantiated")

    monkeypatch.setattr(
        "hermes_memory_fabric.p4_m0_subspace_operator.create_workspace_subspace_memory_store",
        fail_store_creation,
    )

    markdown_code, _, markdown_stderr, markdown_stdout = _run_operator(
        [
            "memory-loop",
            "execution-decision-silence-non-consent-map",
            "--workspace-root",
            str(tmp_path),
        ]
    )
    json_code, json_payload, json_stderr, _ = _run_operator(
        [
            "memory-loop",
            "execution-decision-silence-non-consent-map",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert markdown_code == 0
    assert markdown_stderr == ""
    assert markdown_stdout.startswith("# P4-M2.12")
    assert json_code == 0
    assert json_stderr == ""
    assert json_payload["count"] == 17
    assert not (tmp_path / ".local").exists()


def test_command_creates_no_storage_files_or_state_changes(tmp_path):
    _run_operator(
        [
            "memory-loop",
            "execution-decision-silence-non-consent-map",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    storage_root = tmp_path / ".local" / "subspace_memory"
    for filename in (
        "execution_decision_silence_non_consent_map.jsonl",
        "consent.jsonl",
        "non_consent.jsonl",
        "decisions.jsonl",
        "decision_execution.jsonl",
        "recommendations.jsonl",
        "rankings.jsonl",
        "next_actions.jsonl",
        "confirmation.jsonl",
        "authorization.jsonl",
        "execution.jsonl",
        "approvals.jsonl",
        "rejections.jsonl",
        "risk_acceptance.jsonl",
        "risk_waiver.jsonl",
        "validation.jsonl",
        "readiness.jsonl",
        "memories.jsonl",
        "proposals.jsonl",
        "lifecycle.jsonl",
        "retry_policy.jsonl",
        "sources.jsonl",
        "provenance.jsonl",
        "evidence.jsonl",
        "citations.jsonl",
        "audit.jsonl",
    ):
        assert not (storage_root / filename).exists()
    assert not (tmp_path / ".local").exists()


def test_read_only_allowlist_includes_new_command_and_preserves_previous_p4_m2_11_commands():
    commands = _memory_loop_commands()

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
    assert "execution-decision-silence-non-consent-map" in commands
    assert PREVIOUS_P4_M2_11_READ_ONLY_COMMANDS.issubset(commands)
    assert commands.isdisjoint(PROHIBITED_MEMORY_LOOP_COMMANDS)


def test_existing_p4_m1_0_through_p4_m2_11_memory_loop_commands_still_work(tmp_path):
    expected_prefixes = {
        "checklist": "# P4-M1.0 Human-Gated Memory Loop Checklist\n",
        "review-status": "# P4-M1.1 Human-Gated Proposal Review Status\n",
        "recall-verification-status": "# P4-M1.2 Human-Gated Recall Verification Status\n",
        "lifecycle-verification-status": "# P4-M1.3 Human-Gated Lifecycle Verification Status\n",
        "do-not-retry-verification-status": "# P4-M1.4 Human-Gated Do-Not-Retry Verification Status\n",
        "source-provenance-verification-status": "# P4-M1.5 Source / Provenance Verification Status\n",
        "decision-readiness-status": "# P4-M1.6 Decision Readiness Status\n",
        "manual-decision-preview": "# P4-M1.7 Manual Decision Preview\n",
        "governance-pack-export": "# P4-M1.8 Governance Pack Export\n",
        "final-boundary-audit": "# P4-M1.9 Final Boundary Audit / Closure\n",
        "manual-execution-hardening": "# P4-M2.0 Manual Decision Execution Hardening\n",
        "execution-surface-contract": "# P4-M2.1 Execution Surface Contract Definition\n",
        "execution-contract-validation-matrix": "# P4-M2.2 Execution Contract Validation Matrix\n",
        "manual-authorization-evidence-envelope": "# P4-M2.3 Manual Authorization Evidence Envelope\n",
        "human-confirmation-snapshot-contract": "# P4-M2.4 Human Confirmation Snapshot Contract\n",
        "execution-preconditions-snapshot-map": "# P4-M2.5 Execution Preconditions Snapshot Map\n",
        "execution-risk-acknowledgement-map": "# P4-M2.6 Execution Risk Acknowledgement Map\n",
        "execution-risk-acceptance-prohibition-map": "# P4-M2.7 Execution Risk Acceptance Prohibition Map\n",
        "execution-risk-waiver-prohibition-map": "# P4-M2.8 Execution Risk Waiver Prohibition Map\n",
        "execution-decision-non-equivalence-map": "# P4-M2.9 Execution Decision Non-Equivalence Map\n",
        "execution-decision-recommendation-prohibition-map": "# P4-M2.10 Execution Decision Recommendation Prohibition Map\n",
        "execution-decision-default-denial-boundary-map": "# P4-M2.11 Execution Decision Default Denial Boundary Map\n",
    }

    for command, expected_prefix in expected_prefixes.items():
        exit_code, payload, stderr, stdout = _run_operator(
            ["memory-loop", command, "--workspace-root", str(tmp_path)]
        )
        assert exit_code == 0
        assert payload == {}
        assert stderr == ""
        assert stdout.startswith(expected_prefix)
        assert not (tmp_path / ".local").exists()


def test_doc_contains_required_boundaries():
    doc = Path(
        "docs/CIVILIZATION_CORE_P4_M2_12_EXECUTION_DECISION_SILENCE_NON_CONSENT_MAP.md"
    ).read_text()

    for phrase in BOUNDARY_PHRASES:
        assert phrase in doc
    for field_id in FIELD_IDS:
        assert field_id in doc


def test_package_version_lock_and_no_entry_point():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert pyproject["project"]["version"] == "6.16.0"
    assert "scripts" not in pyproject["project"]
    assert "gui-scripts" not in pyproject["project"]
    assert "console_scripts" not in pyproject["project"].get("entry-points", {})
    entry_points = json.dumps(pyproject["project"].get("entry-points", {}), sort_keys=True)
    assert "p4_m2_execution_decision_silence_non_consent_map" not in entry_points
    assert "execution-decision-silence-non-consent-map" not in entry_points


def test_no_uv_lock_is_created():
    assert not Path("uv.lock").exists()


def test_custom_markdown_render_accepts_read_only_fields():
    field = ExecutionDecisionSilenceNonConsentMapField(
        field_order=1,
        field_id="custom-execution-decision-silence-non-consent-map",
        field_name="Custom Execution Decision Silence Non-Consent Map Field",
        field_purpose="Custom inspection-only purpose.",
        silence_non_consent_boundary_category="custom-silence-non-consent-boundary",
        missing_evidence_as_consent_prohibition_signal="Custom missing evidence is not consent.",
        consent_semantics_disabled="Custom consent semantics are disabled.",
        non_consent_execution_semantics_disabled="Custom non-consent execution semantics are disabled.",
    )

    markdown = render_execution_decision_silence_non_consent_map_markdown([field])

    assert "custom-execution-decision-silence-non-consent-map" in markdown
    assert "Custom inspection-only purpose." in markdown


def _run_operator(argv: list[str]) -> tuple[int, dict[str, object], str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_operator_command(argv, stdout=stdout, stderr=stderr)

    stdout_value = stdout.getvalue()
    payload = json.loads(stdout_value) if stdout_value.startswith("{") else {}
    return exit_code, payload, stderr.getvalue(), stdout_value


def _memory_loop_commands() -> set[str]:
    parser = build_parser()
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            memory_loop_parser = action.choices["memory-loop"]
            break
    else:
        raise AssertionError("memory-loop parser not found")

    for action in memory_loop_parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            return set(action.choices)
    raise AssertionError("memory-loop subcommands not found")
