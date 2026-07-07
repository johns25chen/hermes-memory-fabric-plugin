from __future__ import annotations

import argparse
import io
import json
import tomllib
from pathlib import Path

from hermes_memory_fabric.p4_m0_subspace_operator import build_parser, run_operator_command
from hermes_memory_fabric.p4_m2_execution_contract_validation_matrix import (
    EXECUTION_CONTRACT_VALIDATION_MATRIX_BOUNDARY,
    ExecutionContractValidationMatrixRow,
    execution_contract_validation_matrix_as_dicts,
    execution_contract_validation_matrix_field_ids,
    execution_contract_validation_matrix_report,
    list_execution_contract_validation_matrix_rows,
    render_execution_contract_validation_matrix_markdown,
)
from hermes_memory_fabric.p4_m2_execution_surface_contract_definition import (
    execution_surface_contract_field_ids,
)


FIELD_IDS = (
    "execution-surface-id",
    "human-authorization-reference",
    "manual-decision-reference",
    "execution-intent-declaration",
    "target-record-reference",
    "allowed-operation-envelope",
    "precondition-evidence",
    "risk-and-blocking-signals",
    "audit-trace-id",
    "operator-confirmation-placeholder",
    "execution-preview-output",
    "rollback-consideration",
    "side-effect-boundary",
    "external-system-boundary",
    "authorization-semantics-disabled",
    "execution-semantics-disabled",
)

DATACLASS_FIELDS = {
    "row_order",
    "field_id",
    "validation_dimension",
    "required_presence_signal",
    "schema_closure_signal",
    "trace_completeness_signal",
    "prohibited_semantics",
    "blocking_signal",
    "future_validation_note",
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
}

TRUE_STATUS_FLAGS = (
    "p4_m2_started",
    "execution_surface_contract_definition_available",
    "execution_contract_validation_matrix_started",
    "validation_matrix_definition_only",
    "schema_validation_rules_defined",
    "trace_completeness_rules_defined",
    "blocking_signal_rules_defined",
    "inspection_only",
)

DISABLED_STATUS_FLAGS = (
    "live_contract_validation_enabled",
    "input_validation_enabled",
    "record_validation_enabled",
    "validation_verdict_enabled",
    "readiness_verdict_enabled",
    "actual_decision_execution_enabled",
    "automatic_decision_execution_enabled",
    "manual_execution_command_enabled",
    "execute_command_enabled",
    "approval_enabled",
    "rejection_enabled",
    "automatic_decision_recommendation_enabled",
    "decision_ranking_enabled",
    "automatic_readiness_verdict_enabled",
    "authorization_semantics_granted",
    "execution_semantics_granted",
    "memory_write_enabled",
    "memory_record_mutation_enabled",
    "proposal_mutation_enabled",
    "lifecycle_mutation_enabled",
    "do_not_retry_guard_mutation_enabled",
    "retry_policy_mutation_enabled",
    "source_fetching_enabled",
    "source_provenance_mutation_enabled",
    "provenance_write_enabled",
    "memory_injection_enabled",
    "bulk_import_enabled",
    "auto_ingest_enabled",
    "agent_call_enabled",
    "api_mcp_connector_enabled",
    "p4_m3_started",
    "p4_m4_started",
    "p4_m5_started",
    "v7_started",
    "productization_started",
)

PROHIBITED_MEMORY_LOOP_COMMANDS = {
    "authorize",
    "authorization",
    "authorize-decision",
    "decision-authorization",
    "grant-authorization",
    "revoke-authorization",
    "validate-authorization-envelope",
    "live-authorization-validation",
    "decide",
    "decision",
    "execute-decision",
    "decision-execute",
    "manual-execute",
    "execute-manual-decision",
    "approve",
    "reject",
    "approve-all",
    "reject-all",
    "approve-proposal",
    "reject-proposal",
    "approve-memory",
    "reject-memory",
    "recommend-decision",
    "decision-recommendation",
    "rank-decision",
    "readiness-verdict",
    "automatic-readiness",
    "validation-verdict",
    "validate-contract",
    "validate-execution-contract",
    "live-validation",
    "input-validation",
    "record-validation",
    "mark-ready",
    "mark-not-ready",
    "write-memory",
    "create-memory",
    "update-memory",
    "delete-memory",
    "mutate-proposal",
    "update-proposal",
    "lifecycle-set",
    "lifecycle-update",
    "lifecycle-mutate",
    "do-not-retry",
    "mark-do-not-retry",
    "guard-set",
    "guard-update",
    "retry-policy-set",
    "retry-policy-update",
    "fetch-source",
    "source-fetch",
    "lookup-source",
    "source-lookup",
    "browse-source",
    "web-fetch",
    "web-search",
    "verify-source",
    "trust-source",
    "score-source",
    "write-provenance",
    "provenance-write",
    "mutate-source",
    "mutate-provenance",
    "mutate-evidence",
    "mutate-citation",
    "archive",
    "stale",
    "cleanup",
    "delete",
    "import",
    "bulk-import",
    "ingest",
    "auto-ingest",
    "auto-approve",
    "auto-reject",
    "inject",
    "inject-memory",
    "call-agent",
    "execute",
    "deploy",
    "API",
    "MCP",
    "connector",
    "start-p4-m3",
    "start-p4-m4",
    "start-p4-m5",
    "start-v7",
    "productize",
}


def test_validation_matrix_row_order_is_deterministic():
    assert [
        row.row_order
        for row in list_execution_contract_validation_matrix_rows()
    ] == list(range(1, 17))
    assert execution_contract_validation_matrix_field_ids() == FIELD_IDS
    assert (
        execution_contract_validation_matrix_field_ids()
        == execution_contract_validation_matrix_field_ids()
    )


def test_validation_matrix_has_exactly_16_rows():
    assert len(list_execution_contract_validation_matrix_rows()) == 16


def test_matrix_field_ids_match_p4_m2_1_execution_surface_contract_field_ids():
    assert execution_contract_validation_matrix_field_ids() == FIELD_IDS
    assert execution_contract_validation_matrix_field_ids() == execution_surface_contract_field_ids()


def test_every_row_has_required_non_empty_values():
    for row in list_execution_contract_validation_matrix_rows():
        assert row.validation_dimension.strip()
        assert row.required_presence_signal.strip()
        assert row.schema_closure_signal.strip()
        assert row.trace_completeness_signal.strip()
        assert row.prohibited_semantics.strip()
        assert row.blocking_signal.strip()
        assert row.future_validation_note.strip()


def test_markdown_render_contains_all_16_field_ids():
    markdown = render_execution_contract_validation_matrix_markdown()

    for field_id in FIELD_IDS:
        assert field_id in markdown


def test_markdown_render_contains_required_boundary_statements():
    markdown = render_execution_contract_validation_matrix_markdown()

    assert "P4-M2.2 execution contract validation matrix" in markdown
    assert "Read-only validation matrix definition only" in markdown
    assert "Inspection-only" in markdown
    assert "Not P4-M3" in markdown
    assert "P4-M2.1 execution surface contract definition remains the source field contract" in markdown
    assert "Live contract validation is disabled" in markdown
    assert "Input validation is disabled" in markdown
    assert "Record validation is disabled" in markdown
    assert "Validation verdicts are disabled" in markdown
    assert "Readiness verdicts are disabled" in markdown
    assert "Actual decision execution is disabled" in markdown
    assert "Automatic decision execution is disabled" in markdown
    assert "Manual execution command is disabled" in markdown
    assert "Execute command is disabled" in markdown
    assert "No authorization semantics are granted by this validation matrix." in markdown
    assert "No execution semantics are granted by this validation matrix." in markdown
    assert "No memory writing is performed by this validation matrix." in markdown
    assert "No mutation is performed by this validation matrix." in markdown
    assert "No API/MCP/connector behavior is performed by this validation matrix." in markdown
    assert "No agent call is performed by this validation matrix." in markdown


def test_dict_conversion_is_deterministic():
    first = execution_contract_validation_matrix_as_dicts()
    second = execution_contract_validation_matrix_as_dicts()

    assert first == second
    assert [item["field_id"] for item in first] == list(FIELD_IDS)
    assert set(first[0]) == DATACLASS_FIELDS


def test_status_report_is_deterministic():
    first = execution_contract_validation_matrix_report()
    second = execution_contract_validation_matrix_report()

    assert first == second
    assert first["phase"] == "P4-M2.2"
    assert first["feature"] == "Execution Contract Validation Matrix"
    assert first["mode"] == "read-only"
    assert first["matrix_row_count"] == 16
    assert first["boundary"] == EXECUTION_CONTRACT_VALIDATION_MATRIX_BOUNDARY


def test_status_report_has_required_true_flags():
    status = execution_contract_validation_matrix_report()

    for flag in TRUE_STATUS_FLAGS:
        assert status[flag] is True


def test_status_report_has_all_disabled_flags_set_to_false():
    status = execution_contract_validation_matrix_report()

    for flag in DISABLED_STATUS_FLAGS:
        assert status[flag] is False


def test_status_report_package_version_is_6_16_0():
    assert execution_contract_validation_matrix_report()["package_version"] == "6.16.0"


def test_operator_memory_loop_execution_contract_validation_matrix_returns_markdown(
    tmp_path,
):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "execution-contract-validation-matrix",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M2.2 Execution Contract Validation Matrix\n")
    assert "## Status Report" in stdout
    assert EXECUTION_CONTRACT_VALIDATION_MATRIX_BOUNDARY in stdout
    for field_id in FIELD_IDS:
        assert field_id in stdout
    assert "P4-M2.2 execution contract validation matrix only." in stdout
    assert "Read-only validation matrix definition only." in stdout
    assert "Inspection-only." in stdout
    assert "Not P4-M3." in stdout
    assert "P4-M2.1 execution surface contract definition remains the source field contract." in stdout
    assert "Live contract validation is disabled." in stdout
    assert "Input validation is disabled." in stdout
    assert "Record validation is disabled." in stdout
    assert "Validation verdicts are disabled." in stdout
    assert "Readiness verdicts are disabled." in stdout
    assert "Actual decision execution is disabled." in stdout
    assert "Automatic decision execution is disabled." in stdout
    assert "Manual execution command is disabled." in stdout
    assert "Execute command is disabled." in stdout
    assert "No authorization semantics are granted by this validation matrix." in stdout
    assert "No execution semantics are granted by this validation matrix." in stdout
    assert "No memory writing is performed by this validation matrix." in stdout
    assert "No mutation is performed by this validation matrix." in stdout
    assert "No API/MCP/connector behavior is performed by this validation matrix." in stdout
    assert "No agent call is performed by this validation matrix." in stdout
    assert not (tmp_path / ".local").exists()


def test_operator_memory_loop_execution_contract_validation_matrix_format_markdown_returns_markdown(
    tmp_path,
):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "execution-contract-validation-matrix",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "markdown",
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M2.2 Execution Contract Validation Matrix\n")


def test_operator_memory_loop_execution_contract_validation_matrix_format_json_returns_deterministic_json(
    tmp_path,
):
    args = [
        "memory-loop",
        "execution-contract-validation-matrix",
        "--workspace-root",
        str(tmp_path),
        "--format",
        "json",
    ]
    exit_code, payload, stderr, stdout = _run_operator(args)
    second_code, second_payload, second_stderr, second_stdout = _run_operator(args)

    assert exit_code == 0
    assert stderr == ""
    assert second_code == 0
    assert second_stderr == ""
    assert stdout == second_stdout
    assert payload == second_payload
    assert payload["boundary"] == EXECUTION_CONTRACT_VALIDATION_MATRIX_BOUNDARY
    assert payload["count"] == 16
    assert payload["status"] == execution_contract_validation_matrix_report()
    assert [item["field_id"] for item in payload["rows"]] == list(FIELD_IDS)
    assert set(payload["rows"][0]) == DATACLASS_FIELDS
    assert not (tmp_path / ".local").exists()


def test_operator_execution_contract_validation_matrix_command_is_read_only_and_creates_no_local_storage(
    tmp_path,
):
    markdown_code, _, markdown_stderr, _ = _run_operator(
        [
            "memory-loop",
            "execution-contract-validation-matrix",
            "--workspace-root",
            str(tmp_path),
        ]
    )
    json_code, _, json_stderr, _ = _run_operator(
        [
            "memory-loop",
            "execution-contract-validation-matrix",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert markdown_code == 0
    assert markdown_stderr == ""
    assert json_code == 0
    assert json_stderr == ""
    assert not (tmp_path / ".local").exists()


def test_operator_execution_contract_validation_matrix_command_creates_no_proposals(
    tmp_path,
):
    _run_operator(
        [
            "memory-loop",
            "execution-contract-validation-matrix",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert not (tmp_path / ".local" / "subspace_memory" / "proposals.jsonl").exists()


def test_operator_execution_contract_validation_matrix_command_creates_no_approved_memories(
    tmp_path,
):
    _run_operator(
        [
            "memory-loop",
            "execution-contract-validation-matrix",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert not (tmp_path / ".local" / "subspace_memory" / "memories.jsonl").exists()


def test_operator_execution_contract_validation_matrix_command_creates_no_boundary_or_state_changes(
    tmp_path,
):
    _run_operator(
        [
            "memory-loop",
            "execution-contract-validation-matrix",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    storage_root = tmp_path / ".local" / "subspace_memory"
    assert not (storage_root / "decisions.jsonl").exists()
    assert not (storage_root / "execution.jsonl").exists()
    assert not (storage_root / "approvals.jsonl").exists()
    assert not (storage_root / "rejections.jsonl").exists()
    assert not (storage_root / "readiness.jsonl").exists()
    assert not (storage_root / "validation.jsonl").exists()
    assert not (storage_root / "previews.jsonl").exists()
    assert not (storage_root / "governance_pack.jsonl").exists()
    assert not (storage_root / "final_boundary_audit.jsonl").exists()
    assert not (storage_root / "manual_execution_hardening.jsonl").exists()
    assert not (storage_root / "execution_surface_contract.jsonl").exists()
    assert not (storage_root / "execution_contract_validation_matrix.jsonl").exists()
    assert not (storage_root / "closure.jsonl").exists()
    assert not (storage_root / "memories.jsonl").exists()
    assert not (storage_root / "proposals.jsonl").exists()
    assert not (storage_root / "lifecycle.jsonl").exists()
    assert not (storage_root / "do_not_retry.jsonl").exists()
    assert not (storage_root / "sources.jsonl").exists()
    assert not (storage_root / "provenance.jsonl").exists()
    assert not (storage_root / "evidence.jsonl").exists()
    assert not (storage_root / "citations.jsonl").exists()
    assert not (storage_root / "audit.jsonl").exists()
    assert not (tmp_path / ".local").exists()


def test_no_prohibited_memory_loop_write_import_agent_api_mcp_connector_decision_recommendation_readiness_validation_mutation_p4_m3_p4_m4_p4_m5_v7_productization_commands_are_exposed():
    commands = _memory_loop_commands()

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
    assert commands.isdisjoint(PROHIBITED_MEMORY_LOOP_COMMANDS)


def test_existing_p4_m1_0_memory_loop_checklist_still_works(tmp_path):
    _assert_existing_command_still_works(
        tmp_path,
        "checklist",
        "# P4-M1.0 Human-Gated Memory Loop Checklist\n",
    )


def test_existing_p4_m1_1_memory_loop_review_status_still_works(tmp_path):
    _assert_existing_command_still_works(
        tmp_path,
        "review-status",
        "# P4-M1.1 Human-Gated Proposal Review Status\n",
    )


def test_existing_p4_m1_2_memory_loop_recall_verification_status_still_works(
    tmp_path,
):
    _assert_existing_command_still_works(
        tmp_path,
        "recall-verification-status",
        "# P4-M1.2 Human-Gated Recall Verification Status\n",
    )


def test_existing_p4_m1_3_memory_loop_lifecycle_verification_status_still_works(
    tmp_path,
):
    _assert_existing_command_still_works(
        tmp_path,
        "lifecycle-verification-status",
        "# P4-M1.3 Human-Gated Lifecycle Verification Status\n",
    )


def test_existing_p4_m1_4_memory_loop_do_not_retry_verification_status_still_works(
    tmp_path,
):
    _assert_existing_command_still_works(
        tmp_path,
        "do-not-retry-verification-status",
        "# P4-M1.4 Human-Gated Do-Not-Retry Verification Status\n",
    )


def test_existing_p4_m1_5_memory_loop_source_provenance_verification_status_still_works(
    tmp_path,
):
    _assert_existing_command_still_works(
        tmp_path,
        "source-provenance-verification-status",
        "# P4-M1.5 Source / Provenance Verification Status\n",
    )


def test_existing_p4_m1_6_memory_loop_decision_readiness_status_still_works(
    tmp_path,
):
    _assert_existing_command_still_works(
        tmp_path,
        "decision-readiness-status",
        "# P4-M1.6 Decision Readiness Status\n",
    )


def test_existing_p4_m1_7_memory_loop_manual_decision_preview_still_works(
    tmp_path,
):
    _assert_existing_command_still_works(
        tmp_path,
        "manual-decision-preview",
        "# P4-M1.7 Manual Decision Preview\n",
    )


def test_existing_p4_m1_8_memory_loop_governance_pack_export_still_works(
    tmp_path,
):
    _assert_existing_command_still_works(
        tmp_path,
        "governance-pack-export",
        "# P4-M1.8 Governance Pack Export\n",
    )


def test_existing_p4_m1_9_memory_loop_final_boundary_audit_still_works(
    tmp_path,
):
    _assert_existing_command_still_works(
        tmp_path,
        "final-boundary-audit",
        "# P4-M1.9 Final Boundary Audit / Closure\n",
    )


def test_existing_p4_m2_0_memory_loop_manual_execution_hardening_still_works(
    tmp_path,
):
    _assert_existing_command_still_works(
        tmp_path,
        "manual-execution-hardening",
        "# P4-M2.0 Manual Decision Execution Hardening\n",
    )


def test_existing_p4_m2_1_memory_loop_execution_surface_contract_still_works(
    tmp_path,
):
    _assert_existing_command_still_works(
        tmp_path,
        "execution-surface-contract",
        "# P4-M2.1 Execution Surface Contract Definition\n",
    )


def test_package_version_remains_6_16_0():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert pyproject["project"]["version"] == "6.16.0"


def test_no_uv_lock_is_created():
    assert not Path("uv.lock").exists()


def test_no_pyproject_entry_point_is_added_for_execution_contract_validation_matrix():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert "scripts" not in pyproject["project"]
    assert "gui-scripts" not in pyproject["project"]
    assert "console_scripts" not in pyproject["project"].get("entry-points", {})
    entry_points = json.dumps(pyproject["project"].get("entry-points", {}), sort_keys=True)
    assert "p4_m2_execution_contract_validation_matrix" not in entry_points
    assert "execution-contract-validation-matrix" not in entry_points


def test_custom_markdown_render_accepts_read_only_rows():
    row = ExecutionContractValidationMatrixRow(
        row_order=1,
        field_id="custom-execution-contract-validation-matrix",
        validation_dimension="Custom inspection-only dimension.",
        required_presence_signal="Custom presence signal is visible.",
        schema_closure_signal="Custom schema closure signal is visible.",
        trace_completeness_signal="Custom trace completeness signal is visible.",
        prohibited_semantics="No live validation semantics.",
        blocking_signal="Live validation behavior is introduced.",
        future_validation_note="A later path may inspect this custom row.",
    )

    markdown = render_execution_contract_validation_matrix_markdown([row])

    assert "custom-execution-contract-validation-matrix" in markdown
    assert "Custom inspection-only dimension." in markdown


def _assert_existing_command_still_works(
    tmp_path: Path,
    command: str,
    expected_prefix: str,
) -> None:
    exit_code, payload, stderr, stdout = _run_operator(
        ["memory-loop", command, "--workspace-root", str(tmp_path)]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith(expected_prefix)
    assert not (tmp_path / ".local").exists()


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
