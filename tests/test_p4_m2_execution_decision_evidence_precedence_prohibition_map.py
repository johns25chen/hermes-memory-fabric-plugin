from __future__ import annotations

import argparse
import io
import json
import tomllib
from pathlib import Path

from hermes_memory_fabric.p4_m0_subspace_operator import build_parser, run_operator_command
from hermes_memory_fabric.p4_m2_execution_decision_evidence_precedence_prohibition_map import (
    BOUNDARY_PHRASE_LINES,
    EXECUTION_DECISION_EVIDENCE_PRECEDENCE_PROHIBITION_MAP_BOUNDARY,
    ExecutionDecisionEvidencePrecedenceProhibitionMapField,
    execution_decision_evidence_precedence_prohibition_map_as_dicts,
    execution_decision_evidence_precedence_prohibition_map_field_ids,
    execution_decision_evidence_precedence_prohibition_map_report,
    list_execution_decision_evidence_precedence_prohibition_map_fields,
    render_execution_decision_evidence_precedence_prohibition_map_markdown,
)


FIELD_IDS = (
    "execution-decision-evidence-precedence-prohibition-map-id",
    "execution-decision-conflicting-evidence-isolation-map-reference",
    "execution-decision-negative-evidence-non-override-map-reference",
    "execution-decision-silence-non-consent-map-reference",
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
    "evidence-precedence-prohibition-boundary-category",
    "evidence-precedence-semantics-disabled",
)

DATACLASS_FIELDS = {
    "field_order",
    "field_id",
    "field_name",
    "field_purpose",
    "evidence_precedence_prohibition_boundary_category",
    "evidence_precedence_semantics_disabled",
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
    "p4-m5-0-api-mcp-connector-readiness-audit-boundary-contract",
    "p4-m5-1-api-readiness-audit-surface-map",
    "p4-m5-2-mcp-readiness-audit-surface-map",
    "p4-m5-3-connector-readiness-audit-surface-map",
    "p4-m5-4-cross-surface-alignment-map",
    "p4-m5-5-readiness-audit-closure-non-start-boundary-seal",
    "p4-m5-6-final-closure-handoff-next-corridor-non-start-index",
    "p4-m6-0-next-corridor-entry-boundary-contract",
    "p4-m6-1-entry-preconditions-definition-surface",
    "p4-m6-2-entry-acceptance-non-evidence-surface",
    "p4-m6-3-entry-deferral-non-execution-surface",
    "p4-m6-4-entry-rejection-non-execution-surface",
    "p4-m6-5-entry-escalation-non-routing-surface",
    "p4-m6-6-entry-exception-non-override-surface",
    "p4-m6-7-entry-conflict-non-resolution-surface",
    "p4-m6-8-entry-ambiguity-non-inference-surface",
    "p4-m6-9-entry-dependency-non-activation-surface",
}

PREVIOUS_P4_M2_14_READ_ONLY_COMMANDS = EXPECTED_MEMORY_LOOP_COMMANDS - {
    "execution-decision-evidence-precedence-prohibition-map"
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


def test_evidence_precedence_prohibition_map_field_order_count_and_ids_are_stable():
    fields = list_execution_decision_evidence_precedence_prohibition_map_fields()

    assert [field.field_order for field in fields] == list(range(1, 18))
    assert len(fields) == 17
    assert execution_decision_evidence_precedence_prohibition_map_field_ids() == FIELD_IDS


def test_every_evidence_precedence_prohibition_map_field_has_required_non_empty_values():
    for field in list_execution_decision_evidence_precedence_prohibition_map_fields():
        assert field.field_name.strip()
        assert field.field_purpose.strip()
        assert field.evidence_precedence_prohibition_boundary_category.strip()
        assert field.evidence_precedence_semantics_disabled.strip()


def test_markdown_output_is_stable_and_contains_required_boundaries():
    first = render_execution_decision_evidence_precedence_prohibition_map_markdown()
    second = render_execution_decision_evidence_precedence_prohibition_map_markdown()

    assert first == second
    assert first.startswith(
        "# P4-M2.15 Execution Decision Evidence Precedence Prohibition Map\n"
    )
    assert EXECUTION_DECISION_EVIDENCE_PRECEDENCE_PROHIBITION_MAP_BOUNDARY in first
    for field_id in FIELD_IDS:
        assert field_id in first
    for phrase in BOUNDARY_PHRASE_LINES:
        assert phrase in first


def test_json_output_is_stable_and_contains_required_boundaries(tmp_path):
    args = [
        "memory-loop",
        "execution-decision-evidence-precedence-prohibition-map",
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
    assert first_payload["boundary"] == EXECUTION_DECISION_EVIDENCE_PRECEDENCE_PROHIBITION_MAP_BOUNDARY
    assert first_payload["count"] == 17
    assert first_payload["status"] == execution_decision_evidence_precedence_prohibition_map_report()
    assert [item["field_id"] for item in first_payload["fields"]] == list(FIELD_IDS)
    assert set(first_payload["fields"][0]) == DATACLASS_FIELDS
    for phrase in BOUNDARY_PHRASE_LINES:
        assert phrase in first_stdout
    assert not (tmp_path / ".local").exists()


def test_dict_conversion_and_status_report_are_deterministic():
    first_fields = execution_decision_evidence_precedence_prohibition_map_as_dicts()
    second_fields = execution_decision_evidence_precedence_prohibition_map_as_dicts()
    first_status = execution_decision_evidence_precedence_prohibition_map_report()
    second_status = execution_decision_evidence_precedence_prohibition_map_report()

    assert first_fields == second_fields
    assert [field["field_id"] for field in first_fields] == list(FIELD_IDS)
    assert first_status == second_status
    assert first_status["phase"] == "P4-M2.15"
    assert first_status["feature"] == "Execution Decision Evidence Precedence Prohibition Map"
    assert first_status["mode"] == "read-only"
    assert first_status["execution_decision_evidence_precedence_prohibition_map_field_count"] == 17
    assert first_status["boundary"] == EXECUTION_DECISION_EVIDENCE_PRECEDENCE_PROHIBITION_MAP_BOUNDARY


def test_status_report_locks_true_and_disabled_flags():
    status = execution_decision_evidence_precedence_prohibition_map_report()

    for flag in (
        "definition_only",
        "inspection_only",
        "p4_m2_started",
        "execution_decision_conflicting_evidence_isolation_map_available",
        "execution_decision_negative_evidence_non_override_map_available",
        "execution_decision_evidence_precedence_prohibition_map_started",
        "execution_decision_evidence_precedence_prohibition_map_definition_only",
        "decision_evidence_precedence_prohibition_map_fields_defined",
        "evidence_precedence_prohibited",
        "evidence_source_as_precedence_prohibited",
        "evidence_order_as_precedence_prohibited",
        "evidence_recency_as_precedence_prohibited",
        "evidence_timestamp_as_precedence_prohibited",
        "evidence_confidence_as_precedence_prohibited",
        "evidence_authority_as_precedence_prohibited",
        "evidence_citation_as_precedence_prohibited",
        "positive_reference_as_precedence_prohibited",
        "manual_decision_reference_as_precedence_prohibited",
        "operator_reference_as_precedence_prohibited",
        "prior_definition_reference_as_precedence_prohibited",
        "conflicting_evidence_as_resolved_prohibited",
        "conflicting_evidence_as_precedence_prohibited",
        "negative_evidence_as_approval_prohibited",
        "silence_as_consent_prohibited",
        "reference_as_precedence_prohibited",
    ):
        assert status[flag] is True
    for flag in (
        "execution_enabled",
        "decision_execution_enabled",
        "authorization_enabled",
        "decision_authorization_enabled",
        "approval_enabled",
        "decision_approval_enabled",
        "rejection_enabled",
        "live_rejection_enabled",
        "active_denial_enabled",
        "recommendation_enabled",
        "decision_recommendation_enabled",
        "ranking_enabled",
        "decision_ranking_enabled",
        "suggested_next_action_enabled",
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
        "evidence_precedence_record_creation_enabled",
        "evidence_ranking_record_creation_enabled",
        "evidence_score_record_creation_enabled",
        "evidence_winner_record_creation_enabled",
        "evidence_arbitration_record_creation_enabled",
        "conflict_resolution_enabled",
        "evidence_resolution_enabled",
        "evidence_merge_enabled",
        "evidence_reconciliation_enabled",
        "evidence_validation_enabled",
        "live_evidence_validation_enabled",
        "consent_validation_enabled",
        "live_consent_validation_enabled",
        "evidence_override_record_creation_enabled",
        "approval_override_record_creation_enabled",
        "consent_record_creation_enabled",
        "non_consent_record_creation_enabled",
        "precedence_hint_enabled",
        "precedence_verdict_enabled",
        "evidence_precedence_semantics_granted",
        "source_precedence_semantics_granted",
        "chronological_precedence_semantics_granted",
        "recency_precedence_semantics_granted",
        "confidence_precedence_semantics_granted",
        "authority_precedence_semantics_granted",
        "citation_precedence_semantics_granted",
        "winner_semantics_granted",
        "evidence_ranking_semantics_granted",
        "evidence_scoring_semantics_granted",
        "source_ranking_semantics_granted",
        "evidence_arbitration_semantics_granted",
        "memory_mutation_enabled",
        "p4_m3_started",
        "p4_m4_started",
        "p4_m5_started",
        "v7_started",
        "productization_started",
        "ui_started",
        "operator_console_started",
        "full_memory_graph_started",
    ):
        assert status[flag] is False


def test_operator_markdown_default_is_read_only_and_creates_no_local_storage(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "execution-decision-evidence-precedence-prohibition-map",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith(
        "# P4-M2.15 Execution Decision Evidence Precedence Prohibition Map\n"
    )
    assert "## Status Report" in stdout
    assert EXECUTION_DECISION_EVIDENCE_PRECEDENCE_PROHIBITION_MAP_BOUNDARY in stdout
    for phrase in BOUNDARY_PHRASE_LINES:
        assert phrase in stdout
    assert not (tmp_path / ".local").exists()


def test_operator_markdown_format_is_explicit_and_stable(tmp_path):
    args = [
        "memory-loop",
        "execution-decision-evidence-precedence-prohibition-map",
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
    assert first_stdout.startswith(
        "# P4-M2.15 Execution Decision Evidence Precedence Prohibition Map\n"
    )
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
            "execution-decision-evidence-precedence-prohibition-map",
            "--workspace-root",
            str(tmp_path),
        ]
    )
    json_code, json_payload, json_stderr, _ = _run_operator(
        [
            "memory-loop",
            "execution-decision-evidence-precedence-prohibition-map",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert markdown_code == 0
    assert markdown_stderr == ""
    assert markdown_stdout.startswith("# P4-M2.15")
    assert json_code == 0
    assert json_stderr == ""
    assert json_payload["count"] == 17
    assert not (tmp_path / ".local").exists()


def test_command_creates_no_storage_files_or_state_changes(tmp_path):
    _run_operator(
        [
            "memory-loop",
            "execution-decision-evidence-precedence-prohibition-map",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    storage_root = tmp_path / ".local" / "subspace_memory"
    for filename in (
        "execution_decision_evidence_precedence_prohibition_map.jsonl",
        "evidence_precedence.jsonl",
        "source_precedence.jsonl",
        "chronological_precedence.jsonl",
        "recency_precedence.jsonl",
        "confidence_precedence.jsonl",
        "authority_precedence.jsonl",
        "citation_precedence.jsonl",
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


def test_read_only_allowlist_includes_new_command_and_preserves_previous_p4_m2_14_commands():
    commands = _memory_loop_commands()

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
    assert "execution-decision-evidence-precedence-prohibition-map" in commands
    assert PREVIOUS_P4_M2_14_READ_ONLY_COMMANDS.issubset(commands)
    assert commands.isdisjoint(PROHIBITED_MEMORY_LOOP_COMMANDS)


def test_existing_p4_m1_0_through_p4_m2_14_memory_loop_commands_still_work(tmp_path):
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
        "docs/CIVILIZATION_CORE_P4_M2_15_EXECUTION_DECISION_EVIDENCE_PRECEDENCE_PROHIBITION_MAP.md"
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
    assert "p4_m2_execution_decision_evidence_precedence_prohibition_map" not in entry_points
    assert "execution-decision-evidence-precedence-prohibition-map" not in entry_points


def test_no_uv_lock_is_created():
    assert not Path("uv.lock").exists()


def test_custom_markdown_render_accepts_read_only_fields():
    field = ExecutionDecisionEvidencePrecedenceProhibitionMapField(
        field_order=1,
        field_id="custom-execution-decision-evidence-precedence-prohibition-map",
        field_name="Custom Execution Decision Evidence Precedence Prohibition Map Field",
        field_purpose="Custom inspection-only purpose.",
        evidence_precedence_prohibition_boundary_category=(
            "custom-evidence-precedence-prohibition-boundary"
        ),
        evidence_precedence_semantics_disabled=(
            "Custom evidence precedence semantics are disabled."
        ),
    )

    markdown = render_execution_decision_evidence_precedence_prohibition_map_markdown([field])

    assert "custom-execution-decision-evidence-precedence-prohibition-map" in markdown
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
