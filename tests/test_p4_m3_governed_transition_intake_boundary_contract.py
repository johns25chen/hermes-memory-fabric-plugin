from __future__ import annotations

import argparse
import io
import json
import tomllib
from pathlib import Path

from hermes_memory_fabric.p4_m0_subspace_operator import build_parser, run_operator_command
from hermes_memory_fabric.p4_m3_governed_transition_intake_boundary_contract import (
    BOUNDARY_PHRASE_LINES,
    GOVERNED_TRANSITION_INTAKE_BOUNDARY_CONTRACT_BOUNDARY,
    GovernedTransitionIntakeBoundaryContractField,
    governed_transition_intake_boundary_contract_as_dicts,
    governed_transition_intake_boundary_contract_field_ids,
    governed_transition_intake_boundary_contract_report,
    list_governed_transition_intake_boundary_contract_fields,
    render_governed_transition_intake_boundary_contract_markdown,
)


FIELD_IDS = (
    "p4-m3-governed-transition-intake-boundary-contract-id",
    "p4-m2-closure-handoff-contract-reference",
    "p4-m2-final-non-execution-boundary-audit-reference",
    "p4-m3-intake-boundary-source-reference",
    "p4-m3-intake-boundary-scope",
    "p4-m3-transition-target-label-reference",
    "p4-m3-transition-not-executed-boundary",
    "p4-m3-transition-non-authorization-boundary",
    "p4-m3-transition-non-approval-boundary",
    "p4-m3-transition-non-confirmation-boundary",
    "p4-m3-transition-non-recommendation-boundary",
    "p4-m3-transition-non-ranking-boundary",
    "p4-m3-transition-non-readiness-verdict-boundary",
    "p4-m3-transition-non-validation-verdict-boundary",
    "p4-m3-transition-non-override-boundary",
    "p4-m3-transition-non-mutation-boundary",
    "p4-m3-intake-boundary-contract-category",
    "p4-m3-intake-boundary-semantics-disabled",
)

DATACLASS_FIELDS = {
    "field_order",
    "field_id",
    "field_name",
    "field_purpose",
    "p4_m3_intake_boundary_contract_category",
    "p4_m3_intake_boundary_semantics_disabled",
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
}

PREVIOUS_P4_M2_17_READ_ONLY_COMMANDS = EXPECTED_MEMORY_LOOP_COMMANDS - {
    "governed-transition-intake-boundary-contract"
}

PROHIBITED_MEMORY_LOOP_COMMANDS = {
    "confirm",
    "authorization",
    "approve",
    "reject",
    "execute",
    "recommend-transition",
    "rank-transition",
    "suggest-next-action",
    "validate-transition-readiness",
    "readiness-verdict",
    "validation-verdict",
    "override-verdict",
    "choose-precedence",
    "resolve-conflict",
    "accept-risk",
    "waive-risk",
    "create-transition-record",
    "create-transition-readiness-record",
    "create-transition-validation-record",
    "create-transition-approval-record",
    "create-transition-authorization-record",
    "create-transition-confirmation-record",
    "create-transition-execution-record",
    "create-transition-recommendation-record",
    "create-transition-ranking-record",
    "create-transition-next-action-record",
    "write-memory",
    "create-memory",
    "update-memory",
    "delete-memory",
    "mutate-proposal",
    "mutate-lifecycle",
    "fetch-source",
    "write-provenance",
    "mutate-evidence",
    "mutate-citation",
    "mutate-roadmap",
    "API",
    "MCP",
    "connector",
    "call-agent",
    "p4-m3-1",
    "start-p4-m3-1",
    "start-p4-m4",
    "start-p4-m5",
    "start-v7",
    "productize",
    "operator-console",
    "ui",
    "deploy",
}

TRUE_STATUS_FLAGS = (
    "definition_only",
    "inspection_only",
    "p4_m3_boundary_definition_started",
    "p4_m3_0_governed_transition_intake_boundary_contract_started",
    "p4_m3_0_definition_only",
    "p4_m2_17_closure_handoff_contract_reference_defined",
    "p4_m2_final_non_execution_boundary_reference_defined",
    "p4_m3_intake_boundary_contract_defined",
    "p4_m3_transition_intake_scope_defined",
    "p4_m3_transition_execution_semantics_prohibited",
    "p4_m3_transition_authorization_semantics_prohibited",
    "p4_m3_transition_approval_semantics_prohibited",
    "p4_m3_transition_confirmation_semantics_prohibited",
    "p4_m3_transition_recommendation_semantics_prohibited",
    "p4_m3_transition_ranking_semantics_prohibited",
    "p4_m3_transition_readiness_verdict_semantics_prohibited",
    "p4_m3_transition_validation_verdict_semantics_prohibited",
    "p4_m3_transition_override_semantics_prohibited",
    "p4_m3_transition_mutation_semantics_prohibited",
    "p4_m3_1_start_deferred",
)

FALSE_STATUS_FLAGS = (
    "execution_enabled",
    "decision_execution_enabled",
    "transition_execution_enabled",
    "transition_command_execution_enabled",
    "phase_transition_execution_enabled",
    "authorization_enabled",
    "transition_authorization_enabled",
    "approval_enabled",
    "transition_approval_enabled",
    "confirmation_enabled",
    "transition_confirmation_enabled",
    "recommendation_enabled",
    "transition_recommendation_enabled",
    "ranking_enabled",
    "transition_ranking_enabled",
    "suggested_next_action_enabled",
    "next_action_generation_enabled",
    "readiness_verdict_enabled",
    "transition_readiness_verdict_enabled",
    "validation_verdict_enabled",
    "transition_validation_verdict_enabled",
    "override_verdict_enabled",
    "transition_override_verdict_enabled",
    "precedence_verdict_enabled",
    "conflict_resolution_verdict_enabled",
    "automatic_readiness_verdict_enabled",
    "execution_hint_enabled",
    "transition_execution_hint_enabled",
    "authorization_hint_enabled",
    "approval_hint_enabled",
    "confirmation_hint_enabled",
    "recommendation_hint_enabled",
    "readiness_hint_enabled",
    "validation_hint_enabled",
    "override_hint_enabled",
    "transition_hint_enabled",
    "default_readiness_enabled",
    "default_approval_enabled",
    "default_allow_enabled",
    "default_permit_enabled",
    "default_continue_enabled",
    "default_execute_enabled",
    "auto_pass_enabled",
    "transition_auto_pass_enabled",
    "advisory_verdict_enabled",
    "evidence_validation_enabled",
    "live_evidence_validation_enabled",
    "transition_readiness_validation_enabled",
    "live_transition_readiness_validation_enabled",
    "consent_validation_enabled",
    "live_consent_validation_enabled",
    "live_confirmation_validation_enabled",
    "live_authorization_validation_enabled",
    "live_contract_validation_enabled",
    "input_validation_enabled",
    "record_validation_enabled",
    "risk_acceptance_enabled",
    "risk_waiver_enabled",
    "evidence_precedence_enabled",
    "source_precedence_enabled",
    "chronological_precedence_enabled",
    "recency_precedence_enabled",
    "confidence_precedence_enabled",
    "authority_precedence_enabled",
    "citation_precedence_enabled",
    "winning_evidence_enabled",
    "evidence_winner_enabled",
    "evidence_ranking_enabled",
    "evidence_scoring_enabled",
    "source_ranking_enabled",
    "evidence_tie_breaker_enabled",
    "evidence_arbitration_enabled",
    "conflict_resolution_enabled",
    "evidence_resolution_enabled",
    "evidence_merge_enabled",
    "evidence_reconciliation_enabled",
    "evidence_override_enabled",
    "approval_override_enabled",
    "authorization_override_enabled",
    "readiness_override_enabled",
    "execution_override_enabled",
    "transition_override_enabled",
    "consent_override_enabled",
    "risk_acceptance_override_enabled",
    "risk_waiver_override_enabled",
    "transition_record_creation_enabled",
    "transition_readiness_record_creation_enabled",
    "transition_validation_record_creation_enabled",
    "transition_approval_record_creation_enabled",
    "transition_authorization_record_creation_enabled",
    "transition_confirmation_record_creation_enabled",
    "transition_execution_record_creation_enabled",
    "transition_recommendation_record_creation_enabled",
    "transition_ranking_record_creation_enabled",
    "transition_next_action_record_creation_enabled",
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
    "roadmap_mutation_enabled",
    "api_enabled",
    "mcp_enabled",
    "connector_enabled",
    "agent_call_enabled",
    "codex_hermes_chatgpt_product_code_auto_call_enabled",
    "p4_m3_1_started",
    "p4_m3_1_command_enabled",
    "p4_m3_1_activation_enabled",
    "p4_m3_1_implementation_enabled",
    "p4_m4_started",
    "p4_m5_started",
    "v7_started",
    "productization_started",
    "ui_started",
    "operator_console_started",
    "mvp_started",
    "deploy_started",
    "full_memory_graph_started",
    "version_bump_enabled",
    "tag_creation_enabled",
)


def test_governed_transition_intake_boundary_field_order_count_and_ids_are_stable():
    fields = list_governed_transition_intake_boundary_contract_fields()

    assert [field.field_order for field in fields] == list(range(1, 19))
    assert len(fields) == 18
    assert governed_transition_intake_boundary_contract_field_ids() == FIELD_IDS


def test_every_governed_transition_intake_boundary_field_has_required_values():
    for field in list_governed_transition_intake_boundary_contract_fields():
        assert field.field_name.strip()
        assert field.field_purpose.strip()
        assert field.p4_m3_intake_boundary_contract_category.strip()
        assert field.p4_m3_intake_boundary_semantics_disabled.strip()


def test_markdown_output_is_stable_and_contains_required_boundaries():
    first = render_governed_transition_intake_boundary_contract_markdown()
    second = render_governed_transition_intake_boundary_contract_markdown()

    assert first == second
    assert first.startswith("# P4-M3.0 Governed Transition Intake Boundary Contract\n")
    assert GOVERNED_TRANSITION_INTAKE_BOUNDARY_CONTRACT_BOUNDARY in first
    for field_id in FIELD_IDS:
        assert field_id in first
    for phrase in BOUNDARY_PHRASE_LINES:
        assert phrase in first


def test_json_output_is_stable_and_contains_required_boundaries(tmp_path):
    args = [
        "memory-loop",
        "governed-transition-intake-boundary-contract",
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
    assert first_payload["boundary"] == GOVERNED_TRANSITION_INTAKE_BOUNDARY_CONTRACT_BOUNDARY
    assert first_payload["count"] == 18
    assert first_payload["status"] == governed_transition_intake_boundary_contract_report()
    assert [item["field_id"] for item in first_payload["fields"]] == list(FIELD_IDS)
    assert set(first_payload["fields"][0]) == DATACLASS_FIELDS
    for phrase in BOUNDARY_PHRASE_LINES:
        assert phrase in first_stdout
    assert not (tmp_path / ".local").exists()


def test_dict_conversion_and_status_report_are_deterministic():
    first_fields = governed_transition_intake_boundary_contract_as_dicts()
    second_fields = governed_transition_intake_boundary_contract_as_dicts()
    first_status = governed_transition_intake_boundary_contract_report()
    second_status = governed_transition_intake_boundary_contract_report()

    assert first_fields == second_fields
    assert [field["field_id"] for field in first_fields] == list(FIELD_IDS)
    assert first_status == second_status
    assert first_status["phase"] == "P4-M3.0"
    assert first_status["feature"] == "Governed Transition Intake Boundary Contract"
    assert first_status["mode"] == "read-only"
    assert first_status["governed_transition_intake_boundary_contract_field_count"] == 18
    assert first_status["boundary"] == GOVERNED_TRANSITION_INTAKE_BOUNDARY_CONTRACT_BOUNDARY


def test_status_report_locks_true_and_disabled_flags():
    status = governed_transition_intake_boundary_contract_report()

    for flag in TRUE_STATUS_FLAGS:
        assert status[flag] is True
    for flag in FALSE_STATUS_FLAGS:
        assert status[flag] is False


def test_operator_markdown_default_is_read_only_and_creates_no_local_storage(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "governed-transition-intake-boundary-contract",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M3.0 Governed Transition Intake Boundary Contract\n")
    assert "## Status Report" in stdout
    assert GOVERNED_TRANSITION_INTAKE_BOUNDARY_CONTRACT_BOUNDARY in stdout
    for phrase in BOUNDARY_PHRASE_LINES:
        assert phrase in stdout
    assert not (tmp_path / ".local").exists()


def test_operator_markdown_format_is_explicit_and_stable(tmp_path):
    args = [
        "memory-loop",
        "governed-transition-intake-boundary-contract",
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
    assert first_stdout.startswith("# P4-M3.0 Governed Transition Intake Boundary Contract\n")
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
            "governed-transition-intake-boundary-contract",
            "--workspace-root",
            str(tmp_path),
        ]
    )
    json_code, json_payload, json_stderr, _ = _run_operator(
        [
            "memory-loop",
            "governed-transition-intake-boundary-contract",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert markdown_code == 0
    assert markdown_stderr == ""
    assert markdown_stdout.startswith("# P4-M3.0")
    assert json_code == 0
    assert json_stderr == ""
    assert json_payload["count"] == 18
    assert not (tmp_path / ".local").exists()


def test_command_creates_no_storage_files_or_state_changes(tmp_path):
    _run_operator(
        [
            "memory-loop",
            "governed-transition-intake-boundary-contract",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    storage_root = tmp_path / ".local" / "subspace_memory"
    for filename in (
        "governed_transition_intake_boundary_contract.jsonl",
        "transition_records.jsonl",
        "transition_readiness_records.jsonl",
        "transition_validation_records.jsonl",
        "transition_approval_records.jsonl",
        "transition_authorization_records.jsonl",
        "transition_confirmation_records.jsonl",
        "transition_execution_records.jsonl",
        "transition_recommendation_records.jsonl",
        "transition_ranking_records.jsonl",
        "transition_next_action_records.jsonl",
        "execution.jsonl",
        "authorization.jsonl",
        "confirmation.jsonl",
        "approvals.jsonl",
        "recommendations.jsonl",
        "rankings.jsonl",
        "next_actions.jsonl",
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
        "roadmap.jsonl",
        "audit.jsonl",
    ):
        assert not (storage_root / filename).exists()
    assert not (tmp_path / ".local").exists()


def test_read_only_allowlist_includes_new_command_and_preserves_previous_commands():
    commands = _memory_loop_commands()

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
    assert "governed-transition-intake-boundary-contract" in commands
    assert PREVIOUS_P4_M2_17_READ_ONLY_COMMANDS.issubset(commands)
    assert commands.isdisjoint(PROHIBITED_MEMORY_LOOP_COMMANDS)


def test_existing_p4_m1_0_through_p4_m2_17_memory_loop_commands_still_work(tmp_path):
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
        "execution-decision-silence-non-consent-map": "# P4-M2.12 Execution Decision Silence Non-Consent Map\n",
        "execution-decision-negative-evidence-non-override-map": "# P4-M2.13 Execution Decision Negative Evidence Non-Override Map\n",
        "execution-decision-conflicting-evidence-isolation-map": "# P4-M2.14 Execution Decision Conflicting Evidence Isolation Map\n",
        "execution-decision-evidence-precedence-prohibition-map": "# P4-M2.15 Execution Decision Evidence Precedence Prohibition Map\n",
        "final-non-execution-boundary-audit": "# P4-M2.16 Final Non-Execution Boundary Audit\n",
        "p4-m2-closure-handoff-contract": "# P4-M2.17 P4-M2 Closure Handoff Contract\n",
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
        "docs/CIVILIZATION_CORE_P4_M3_0_GOVERNED_TRANSITION_INTAKE_BOUNDARY_CONTRACT.md"
    ).read_text()

    for phrase in BOUNDARY_PHRASE_LINES:
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
    assert "p4_m3_governed_transition_intake_boundary_contract" not in entry_points
    assert "governed-transition-intake-boundary-contract" not in entry_points


def test_no_uv_lock_is_created():
    assert not Path("uv.lock").exists()


def test_custom_markdown_render_accepts_read_only_fields():
    field = GovernedTransitionIntakeBoundaryContractField(
        field_order=1,
        field_id="custom-governed-transition-intake-boundary-contract",
        field_name="Custom Governed Transition Intake Boundary Contract Field",
        field_purpose="Custom inspection-only purpose.",
        p4_m3_intake_boundary_contract_category=(
            "custom-governed-transition-intake-boundary-contract-category"
        ),
        p4_m3_intake_boundary_semantics_disabled=(
            "Custom governed transition intake semantics are disabled."
        ),
    )

    markdown = render_governed_transition_intake_boundary_contract_markdown([field])

    assert "custom-governed-transition-intake-boundary-contract" in markdown
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
