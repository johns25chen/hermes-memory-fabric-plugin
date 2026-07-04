from __future__ import annotations

import argparse
import io
import json
import tomllib
from pathlib import Path

from hermes_memory_fabric.p4_m0_subspace_operator import build_parser, run_operator_command
from hermes_memory_fabric.p4_m2_closure_handoff_contract import (
    BOUNDARY_PHRASE_LINES,
    CLOSURE_HANDOFF_CONTRACT_BOUNDARY,
    ClosureHandoffContractField,
    closure_handoff_contract_as_dicts,
    closure_handoff_contract_field_ids,
    closure_handoff_contract_report,
    list_closure_handoff_contract_fields,
    render_closure_handoff_contract_markdown,
)


FIELD_IDS = (
    "p4-m2-closure-handoff-contract-id",
    "p4-m2-closure-source-reference",
    "p4-m2-final-non-execution-boundary-audit-reference",
    "p4-m2-prior-definition-layer-reference-set",
    "p4-m3-target-label-reference",
    "p4-m3-not-started-boundary",
    "closure-handoff-contract-scope",
    "closure-handoff-non-execution-boundary",
    "closure-handoff-non-authorization-boundary",
    "closure-handoff-non-confirmation-boundary",
    "closure-handoff-non-approval-boundary",
    "closure-handoff-non-recommendation-boundary",
    "closure-handoff-non-ranking-boundary",
    "closure-handoff-non-verdict-boundary",
    "closure-handoff-non-override-boundary",
    "closure-handoff-non-mutation-boundary",
    "closure-handoff-contract-category",
    "closure-handoff-semantics-disabled",
)

DATACLASS_FIELDS = {
    "field_order",
    "field_id",
    "field_name",
    "field_purpose",
    "closure_handoff_contract_category",
    "closure_handoff_semantics_disabled",
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
    "declared-transition-impact-envelope-contract",
    "declared-transition-risk-envelope-contract",
    "declared-transition-assumption-envelope-contract",
    "declared-transition-safeguard-envelope-contract",
    "declared-transition-package-assembly-envelope-contract",
    "entry-gate-design-final-non-validation-boundary-audit",
    "entry-gate-design-closure-handoff-contract",
    "entry-gate-design-phase-closure-review",
    "entry-gate-design-final-phase-handoff-summary",
    "entry-gate-design-phase-terminal-closure-seal",
    "p4-m4-final-closure-index-entry-planning-gate",
    "p4-m4-final-closure-evidence-index",
    "p4-m4-final-closure-operator-handoff-index",
    "p4-m4-final-closure-transition-readiness-non-start-index",
    "p4-m4-final-closure-non-start-bridge-index",
    "p4-m4-final-closure-boundary-freeze-index",
    "p4-m4-final-closure-roadmap-alignment-snapshot",
}

PREVIOUS_P4_M2_16_READ_ONLY_COMMANDS = EXPECTED_MEMORY_LOOP_COMMANDS - {
    "p4-m2-closure-handoff-contract"
}

PROHIBITED_MEMORY_LOOP_COMMANDS = {
    "confirm",
    "authorization",
    "approve",
    "reject",
    "execute",
    "recommend-decision",
    "rank-decision",
    "suggest-next-action",
    "validate-evidence",
    "validate-consent",
    "rank-evidence",
    "score-evidence",
    "rank-source",
    "select-winning-evidence",
    "choose-evidence-precedence",
    "arbitrate-evidence",
    "resolve-conflict",
    "merge-evidence",
    "reconcile-evidence",
    "create-evidence-precedence-record",
    "create-evidence-ranking-record",
    "create-evidence-score-record",
    "create-evidence-winner-record",
    "create-evidence-arbitration-record",
    "create-conflict-resolution-record",
    "create-evidence-merge-record",
    "create-evidence-override-record",
    "create-approval-override-record",
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
    "mutate-roadmap",
    "transition",
    "transition-execution",
    "phase-transition-action",
    "handoff-execution",
    "handoff-authorization",
    "handoff-approval",
    "handoff-recommendation",
    "handoff-ranking",
    "handoff-readiness-verdict",
    "handoff-validation-verdict",
    "handoff-override-verdict",
    "call-agent",
    "API",
    "MCP",
    "connector",
    "start-p4-m3",
    "p4-m3",
    "p4-m3-command",
    "activate-p4-m3",
    "implement-p4-m3",
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
    "p4_m2_started",
    "p4_m2_closure_handoff_contract_started",
    "p4_m2_closure_handoff_contract_definition_only",
    "p4_m2_1_through_p4_m2_16_references_defined",
    "p4_m2_closure_handoff_contract_defined",
    "p4_m2_to_p4_m3_boundary_documented",
    "p4_m3_start_deferred",
    "p4_m2_execution_semantics_prohibited",
    "p4_m2_authorization_semantics_prohibited",
    "p4_m2_confirmation_semantics_prohibited",
    "p4_m2_approval_semantics_prohibited",
    "p4_m2_recommendation_semantics_prohibited",
    "p4_m2_ranking_semantics_prohibited",
    "p4_m2_validation_verdict_semantics_prohibited",
    "p4_m2_precedence_verdict_semantics_prohibited",
    "p4_m2_override_semantics_prohibited",
    "p4_m2_transition_semantics_prohibited",
    "p4_m2_mutation_semantics_prohibited",
)

FALSE_STATUS_FLAGS = (
    "execution_enabled",
    "decision_execution_enabled",
    "authorization_enabled",
    "decision_authorization_enabled",
    "confirmation_enabled",
    "decision_confirmation_enabled",
    "approval_enabled",
    "decision_approval_enabled",
    "rejection_enabled",
    "decision_rejection_enabled",
    "recommendation_enabled",
    "decision_recommendation_enabled",
    "ranking_enabled",
    "decision_ranking_enabled",
    "suggested_next_action_enabled",
    "readiness_verdict_enabled",
    "validation_verdict_enabled",
    "override_verdict_enabled",
    "precedence_verdict_enabled",
    "conflict_resolution_verdict_enabled",
    "automatic_readiness_verdict_enabled",
    "execution_hint_enabled",
    "authorization_hint_enabled",
    "confirmation_hint_enabled",
    "approval_hint_enabled",
    "recommendation_hint_enabled",
    "readiness_hint_enabled",
    "validation_hint_enabled",
    "override_hint_enabled",
    "resolution_hint_enabled",
    "precedence_hint_enabled",
    "default_readiness_enabled",
    "default_approval_enabled",
    "default_allow_enabled",
    "default_permit_enabled",
    "default_continue_enabled",
    "default_execute_enabled",
    "auto_pass_enabled",
    "auto_execution_hint_enabled",
    "advisory_verdict_enabled",
    "evidence_validation_enabled",
    "live_evidence_validation_enabled",
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
    "consent_override_enabled",
    "risk_acceptance_override_enabled",
    "risk_waiver_override_enabled",
    "transition_execution_enabled",
    "transition_command_enabled",
    "phase_transition_action_enabled",
    "handoff_execution_enabled",
    "handoff_authorization_enabled",
    "handoff_approval_enabled",
    "handoff_recommendation_enabled",
    "handoff_ranking_enabled",
    "handoff_readiness_verdict_enabled",
    "handoff_validation_verdict_enabled",
    "handoff_override_verdict_enabled",
    "handoff_mutation_enabled",
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
    "p4_m3_started",
    "p4_m3_command_enabled",
    "p4_m3_activation_enabled",
    "p4_m3_implementation_enabled",
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


def test_closure_handoff_contract_field_order_count_and_ids_are_stable():
    fields = list_closure_handoff_contract_fields()

    assert [field.field_order for field in fields] == list(range(1, 19))
    assert len(fields) == 18
    assert closure_handoff_contract_field_ids() == FIELD_IDS


def test_every_closure_handoff_contract_field_has_required_non_empty_values():
    for field in list_closure_handoff_contract_fields():
        assert field.field_name.strip()
        assert field.field_purpose.strip()
        assert field.closure_handoff_contract_category.strip()
        assert field.closure_handoff_semantics_disabled.strip()


def test_markdown_output_is_stable_and_contains_required_boundaries():
    first = render_closure_handoff_contract_markdown()
    second = render_closure_handoff_contract_markdown()

    assert first == second
    assert first.startswith("# P4-M2.17 P4-M2 Closure Handoff Contract\n")
    assert CLOSURE_HANDOFF_CONTRACT_BOUNDARY in first
    for field_id in FIELD_IDS:
        assert field_id in first
    for phrase in BOUNDARY_PHRASE_LINES:
        assert phrase in first


def test_json_output_is_stable_and_contains_required_boundaries(tmp_path):
    args = [
        "memory-loop",
        "p4-m2-closure-handoff-contract",
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
    assert first_payload["boundary"] == CLOSURE_HANDOFF_CONTRACT_BOUNDARY
    assert first_payload["count"] == 18
    assert first_payload["status"] == closure_handoff_contract_report()
    assert [item["field_id"] for item in first_payload["fields"]] == list(FIELD_IDS)
    assert set(first_payload["fields"][0]) == DATACLASS_FIELDS
    for phrase in BOUNDARY_PHRASE_LINES:
        assert phrase in first_stdout
    assert not (tmp_path / ".local").exists()


def test_dict_conversion_and_status_report_are_deterministic():
    first_fields = closure_handoff_contract_as_dicts()
    second_fields = closure_handoff_contract_as_dicts()
    first_status = closure_handoff_contract_report()
    second_status = closure_handoff_contract_report()

    assert first_fields == second_fields
    assert [field["field_id"] for field in first_fields] == list(FIELD_IDS)
    assert first_status == second_status
    assert first_status["phase"] == "P4-M2.17"
    assert first_status["feature"] == "P4-M2 Closure Handoff Contract"
    assert first_status["mode"] == "read-only"
    assert first_status["closure_handoff_contract_field_count"] == 18
    assert first_status["boundary"] == CLOSURE_HANDOFF_CONTRACT_BOUNDARY


def test_status_report_locks_true_and_disabled_flags():
    status = closure_handoff_contract_report()

    for flag in TRUE_STATUS_FLAGS:
        assert status[flag] is True
    for flag in FALSE_STATUS_FLAGS:
        assert status[flag] is False


def test_operator_markdown_default_is_read_only_and_creates_no_local_storage(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "p4-m2-closure-handoff-contract",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M2.17 P4-M2 Closure Handoff Contract\n")
    assert "## Status Report" in stdout
    assert CLOSURE_HANDOFF_CONTRACT_BOUNDARY in stdout
    for phrase in BOUNDARY_PHRASE_LINES:
        assert phrase in stdout
    assert not (tmp_path / ".local").exists()


def test_operator_markdown_format_is_explicit_and_stable(tmp_path):
    args = [
        "memory-loop",
        "p4-m2-closure-handoff-contract",
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
    assert first_stdout.startswith("# P4-M2.17 P4-M2 Closure Handoff Contract\n")
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
            "p4-m2-closure-handoff-contract",
            "--workspace-root",
            str(tmp_path),
        ]
    )
    json_code, json_payload, json_stderr, _ = _run_operator(
        [
            "memory-loop",
            "p4-m2-closure-handoff-contract",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert markdown_code == 0
    assert markdown_stderr == ""
    assert markdown_stdout.startswith("# P4-M2.17")
    assert json_code == 0
    assert json_stderr == ""
    assert json_payload["count"] == 18
    assert not (tmp_path / ".local").exists()


def test_command_creates_no_storage_files_or_state_changes(tmp_path):
    _run_operator(
        [
            "memory-loop",
            "p4-m2-closure-handoff-contract",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    storage_root = tmp_path / ".local" / "subspace_memory"
    for filename in (
        "closure_handoff_contract.jsonl",
        "execution.jsonl",
        "authorization.jsonl",
        "confirmation.jsonl",
        "approvals.jsonl",
        "rejections.jsonl",
        "recommendations.jsonl",
        "rankings.jsonl",
        "next_actions.jsonl",
        "validation.jsonl",
        "readiness.jsonl",
        "evidence_precedence.jsonl",
        "evidence_rankings.jsonl",
        "evidence_scores.jsonl",
        "evidence_winners.jsonl",
        "evidence_arbitration.jsonl",
        "conflict_resolution.jsonl",
        "evidence_resolution.jsonl",
        "evidence_merge.jsonl",
        "evidence_overrides.jsonl",
        "approval_overrides.jsonl",
        "consent.jsonl",
        "non_consent.jsonl",
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


def test_read_only_allowlist_includes_new_command_and_preserves_previous_p4_m2_16_commands():
    commands = _memory_loop_commands()

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
    assert "p4-m2-closure-handoff-contract" in commands
    assert PREVIOUS_P4_M2_16_READ_ONLY_COMMANDS.issubset(commands)
    assert commands.isdisjoint(PROHIBITED_MEMORY_LOOP_COMMANDS)


def test_existing_p4_m1_0_through_p4_m2_16_memory_loop_commands_still_work(tmp_path):
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
        "docs/CIVILIZATION_CORE_P4_M2_17_CLOSURE_HANDOFF_CONTRACT.md"
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
    assert "p4_m2_closure_handoff_contract" not in entry_points
    assert "p4-m2-closure-handoff-contract" not in entry_points


def test_no_uv_lock_is_created():
    assert not Path("uv.lock").exists()


def test_custom_markdown_render_accepts_read_only_fields():
    field = ClosureHandoffContractField(
        field_order=1,
        field_id="custom-closure-handoff-contract",
        field_name="Custom Closure Handoff Contract Field",
        field_purpose="Custom inspection-only purpose.",
        closure_handoff_contract_category="custom-closure-handoff-contract-category",
        closure_handoff_semantics_disabled="Custom closure handoff semantics are disabled.",
    )

    markdown = render_closure_handoff_contract_markdown([field])

    assert "custom-closure-handoff-contract" in markdown
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
