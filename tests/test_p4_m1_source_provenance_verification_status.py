from __future__ import annotations

import argparse
import io
import json
import tomllib
from pathlib import Path

from hermes_memory_fabric.p4_m0_subspace_operator import build_parser, run_operator_command
from hermes_memory_fabric.p4_m1_source_provenance_verification_status import (
    SOURCE_PROVENANCE_VERIFICATION_STATUS_BOUNDARY,
    SourceProvenanceVerificationStatusItem,
    list_source_provenance_verification_status_items,
    render_source_provenance_verification_status_markdown,
    source_provenance_verification_status_as_dicts,
    source_provenance_verification_status_ids,
    source_provenance_verification_status_report,
)


VERIFICATION_IDS = (
    "source-presence-visible",
    "source-type-visible",
    "provenance-chain-visible",
    "evidence-context-visible",
    "citation-boundary-visible",
    "unverified-source-not-trusted",
    "provenance-write-not-taken",
    "manual-review-required",
    "automation-boundary-intact",
)

DATACLASS_FIELDS = {
    "verification_order",
    "verification_id",
    "verification_name",
    "human_verification_question",
    "allowed_system_output",
    "prohibited_automation",
    "ready_signal",
    "blocking_signal",
    "p4_m0_or_p4_m1_dependency",
}

DISABLED_STATUS_FLAGS = (
    "source_fetching_enabled",
    "external_source_lookup_enabled",
    "source_trust_judgment_enabled",
    "source_verification_verdict_enabled",
    "evidence_acceptance_enabled",
    "evidence_rejection_enabled",
    "provenance_write_enabled",
    "source_record_mutation_enabled",
    "evidence_record_mutation_enabled",
    "citation_record_mutation_enabled",
    "lifecycle_mutation_enabled",
    "do_not_retry_guard_mutation_enabled",
    "memory_write_enabled",
    "approval_enabled",
    "rejection_enabled",
    "proposal_mutation_enabled",
    "memory_injection_enabled",
    "bulk_import_enabled",
    "auto_ingest_enabled",
    "agent_call_enabled",
    "api_mcp_connector_enabled",
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
    "fetch-source",
    "source-fetch",
    "lookup-source",
    "source-lookup",
    "browse-source",
    "web-fetch",
    "web-search",
    "verify-source",
    "source-verdict",
    "trust-source",
    "score-source",
    "accept-evidence",
    "reject-evidence",
    "write-provenance",
    "provenance-write",
    "create-provenance",
    "update-provenance",
    "delete-provenance",
    "mutate-source",
    "update-source",
    "mutate-evidence",
    "update-evidence",
    "mutate-citation",
    "update-citation",
    "approve",
    "reject",
    "approve-all",
    "reject-all",
    "archive",
    "stale",
    "cleanup",
    "delete",
    "lifecycle-set",
    "lifecycle-update",
    "lifecycle-mutate",
    "do-not-retry",
    "mark-do-not-retry",
    "guard-set",
    "guard-update",
    "import",
    "bulk-import",
    "ingest",
    "auto-ingest",
    "auto-approve",
    "auto-reject",
    "write-memory",
    "mutate-proposal",
    "update-proposal",
    "inject",
    "inject-memory",
    "call-agent",
    "execute",
    "deploy",
    "api",
    "mcp",
    "connector",
}


def test_source_provenance_verification_status_order_is_deterministic():
    assert [
        item.verification_order
        for item in list_source_provenance_verification_status_items()
    ] == list(range(1, 10))
    assert source_provenance_verification_status_ids() == VERIFICATION_IDS
    assert (
        source_provenance_verification_status_ids()
        == source_provenance_verification_status_ids()
    )


def test_source_provenance_verification_status_has_exactly_9_items():
    assert len(list_source_provenance_verification_status_items()) == 9


def test_verification_ids_match_required_verification_ids():
    assert source_provenance_verification_status_ids() == VERIFICATION_IDS


def test_every_item_has_required_non_empty_fields():
    for item in list_source_provenance_verification_status_items():
        assert item.verification_name.strip()
        assert item.human_verification_question.strip()
        assert item.allowed_system_output.strip()
        assert item.prohibited_automation.strip()
        assert item.ready_signal.strip()
        assert item.blocking_signal.strip()
        assert item.p4_m0_or_p4_m1_dependency.strip()


def test_markdown_render_contains_all_9_verification_ids():
    markdown = render_source_provenance_verification_status_markdown()

    for verification_id in VERIFICATION_IDS:
        assert verification_id in markdown


def test_markdown_render_contains_required_boundary_statements():
    markdown = render_source_provenance_verification_status_markdown()

    assert "read-only source/provenance verification status only" in markdown
    assert "advisory only" in markdown
    assert "does not fetch sources" in markdown
    assert "does not browse the web" in markdown
    assert "does not call external APIs" in markdown
    assert "does not call connectors" in markdown
    assert "does not create API/MCP/connector behavior" in markdown
    assert "does not automatically trust a source" in markdown
    assert "does not automatically verify a source" in markdown
    assert "does not automatically score a source" in markdown
    assert "does not automatically accept evidence" in markdown
    assert "does not automatically reject evidence" in markdown
    assert "does not write provenance" in markdown
    assert "does not create provenance records" in markdown
    assert "does not update provenance records" in markdown
    assert "does not delete provenance records" in markdown
    assert "does not mutate source records" in markdown
    assert "does not mutate evidence records" in markdown
    assert "does not mutate citation records" in markdown
    assert "does not mutate lifecycle records" in markdown
    assert "does not mutate do-not-retry guard state" in markdown
    assert "does not write memory" in markdown
    assert "does not approve memory" in markdown
    assert "does not reject memory" in markdown
    assert "does not mutate proposal records" in markdown
    assert "No source fetching is performed by this status." in markdown
    assert "No external source lookup is performed by this status." in markdown
    assert "No source trust judgment is performed by this status." in markdown
    assert "No source verification verdict is performed by this status." in markdown
    assert "No evidence acceptance or rejection is performed by this status." in markdown
    assert "No provenance writing is performed by this status." in markdown
    assert "No source/evidence/citation mutation is performed by this status." in markdown
    assert "No memory or proposal mutation is performed by this status." in markdown


def test_dict_conversion_is_deterministic():
    first = source_provenance_verification_status_as_dicts()
    second = source_provenance_verification_status_as_dicts()

    assert first == second
    assert [item["verification_id"] for item in first] == list(VERIFICATION_IDS)
    assert set(first[0]) == DATACLASS_FIELDS


def test_status_report_is_deterministic():
    first = source_provenance_verification_status_report()
    second = source_provenance_verification_status_report()

    assert first == second
    assert first["phase"] == "P4-M1.5"
    assert first["feature"] == "Source / Provenance Verification Status"
    assert first["mode"] == "read-only"
    assert first["verification_item_count"] == 9
    assert first["boundary"] == SOURCE_PROVENANCE_VERIFICATION_STATUS_BOUNDARY


def test_status_report_has_advisory_flag_true():
    assert (
        source_provenance_verification_status_report()[
            "source_provenance_verification_status_advisory_only"
        ]
        is True
    )


def test_status_report_has_all_disabled_flags_set_to_false():
    status = source_provenance_verification_status_report()

    for flag in DISABLED_STATUS_FLAGS:
        assert status[flag] is False


def test_status_report_package_version_is_6_16_0():
    assert source_provenance_verification_status_report()["package_version"] == "6.16.0"


def test_operator_memory_loop_source_provenance_verification_status_returns_markdown(
    tmp_path,
):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "source-provenance-verification-status",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M1.5 Source / Provenance Verification Status\n")
    assert "## Status Report" in stdout
    assert SOURCE_PROVENANCE_VERIFICATION_STATUS_BOUNDARY in stdout
    assert "No source fetching is performed by this status." in stdout
    assert "No external source lookup is performed by this status." in stdout
    assert "No source trust judgment is performed by this status." in stdout
    assert "No source verification verdict is performed by this status." in stdout
    assert "No evidence acceptance or rejection is performed by this status." in stdout
    assert "No provenance writing is performed by this status." in stdout
    assert "No source/evidence/citation mutation is performed by this status." in stdout
    assert "No memory or proposal mutation is performed by this status." in stdout


def test_operator_memory_loop_source_provenance_verification_status_format_markdown_returns_markdown(
    tmp_path,
):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "source-provenance-verification-status",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "markdown",
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M1.5 Source / Provenance Verification Status\n")


def test_operator_memory_loop_source_provenance_verification_status_format_json_returns_deterministic_json(
    tmp_path,
):
    args = [
        "memory-loop",
        "source-provenance-verification-status",
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
    assert payload["boundary"] == SOURCE_PROVENANCE_VERIFICATION_STATUS_BOUNDARY
    assert payload["count"] == 9
    assert payload["status"] == source_provenance_verification_status_report()
    assert [item["verification_id"] for item in payload["items"]] == list(VERIFICATION_IDS)
    assert set(payload["items"][0]) == DATACLASS_FIELDS


def test_operator_source_provenance_verification_status_command_is_read_only_and_creates_no_local_storage(
    tmp_path,
):
    markdown_code, _, markdown_stderr, _ = _run_operator(
        [
            "memory-loop",
            "source-provenance-verification-status",
            "--workspace-root",
            str(tmp_path),
        ]
    )
    json_code, _, json_stderr, _ = _run_operator(
        [
            "memory-loop",
            "source-provenance-verification-status",
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


def test_operator_source_provenance_verification_status_command_creates_no_proposals(
    tmp_path,
):
    _run_operator(
        [
            "memory-loop",
            "source-provenance-verification-status",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert not (tmp_path / ".local" / "subspace_memory" / "proposals.jsonl").exists()


def test_operator_source_provenance_verification_status_command_creates_no_approved_memories(
    tmp_path,
):
    _run_operator(
        [
            "memory-loop",
            "source-provenance-verification-status",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert not (tmp_path / ".local" / "subspace_memory" / "memories.jsonl").exists()


def test_operator_source_provenance_verification_status_command_creates_no_provenance_source_evidence_citation_files_or_state_changes(
    tmp_path,
):
    _run_operator(
        [
            "memory-loop",
            "source-provenance-verification-status",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    storage_root = tmp_path / ".local" / "subspace_memory"
    assert not (storage_root / "provenance.jsonl").exists()
    assert not (storage_root / "sources.jsonl").exists()
    assert not (storage_root / "evidence.jsonl").exists()
    assert not (storage_root / "citations.jsonl").exists()
    assert not (storage_root / "audit.jsonl").exists()
    assert not (tmp_path / ".local").exists()


def test_no_prohibited_memory_loop_write_import_agent_api_mcp_connector_source_provenance_mutation_commands_are_exposed():
    commands = _memory_loop_commands()

    assert commands == {
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
    }
    assert commands.isdisjoint(PROHIBITED_MEMORY_LOOP_COMMANDS)


def test_existing_p4_m1_0_memory_loop_checklist_still_works(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        ["memory-loop", "checklist", "--workspace-root", str(tmp_path)]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M1.0 Human-Gated Memory Loop Checklist\n")
    assert not (tmp_path / ".local").exists()


def test_existing_p4_m1_1_memory_loop_review_status_still_works(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        ["memory-loop", "review-status", "--workspace-root", str(tmp_path)]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M1.1 Human-Gated Proposal Review Status\n")
    assert not (tmp_path / ".local").exists()


def test_existing_p4_m1_2_memory_loop_recall_verification_status_still_works(
    tmp_path,
):
    exit_code, payload, stderr, stdout = _run_operator(
        ["memory-loop", "recall-verification-status", "--workspace-root", str(tmp_path)]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M1.2 Human-Gated Recall Verification Status\n")
    assert not (tmp_path / ".local").exists()


def test_existing_p4_m1_3_memory_loop_lifecycle_verification_status_still_works(
    tmp_path,
):
    exit_code, payload, stderr, stdout = _run_operator(
        ["memory-loop", "lifecycle-verification-status", "--workspace-root", str(tmp_path)]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M1.3 Human-Gated Lifecycle Verification Status\n")
    assert not (tmp_path / ".local").exists()


def test_existing_p4_m1_4_memory_loop_do_not_retry_verification_status_still_works(
    tmp_path,
):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "do-not-retry-verification-status",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M1.4 Human-Gated Do-Not-Retry Verification Status\n")
    assert not (tmp_path / ".local").exists()


def test_package_version_remains_6_16_0():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert pyproject["project"]["version"] == "6.16.0"


def test_no_uv_lock_is_created():
    assert not Path("uv.lock").exists()


def test_no_pyproject_entry_point_is_added_for_source_provenance_verification_status():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert "scripts" not in pyproject["project"]
    assert "gui-scripts" not in pyproject["project"]
    assert "console_scripts" not in pyproject["project"].get("entry-points", {})
    entry_points = json.dumps(pyproject["project"].get("entry-points", {}), sort_keys=True)
    assert "p4_m1_source_provenance_verification_status" not in entry_points


def test_custom_markdown_render_accepts_read_only_items():
    item = SourceProvenanceVerificationStatusItem(
        verification_order=1,
        verification_id="custom-verification",
        verification_name="Custom verification",
        human_verification_question="Can the human review the custom source/provenance verification item?",
        allowed_system_output="Source/provenance verification status text only.",
        prohibited_automation="No source fetching or provenance writing.",
        ready_signal="Visible custom verification.",
        blocking_signal="Hidden custom verification.",
        p4_m0_or_p4_m1_dependency="P4-M1 read-only boundary.",
    )

    markdown = render_source_provenance_verification_status_markdown([item])

    assert "custom-verification" in markdown
    assert "Can the human review the custom source/provenance verification item?" in markdown


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
