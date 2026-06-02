from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from hermes_memory_fabric.governed_memory_proposal_pack_dry_run import (
    build_governed_memory_proposal_pack_dry_run,
    governed_memory_proposal_pack_to_json,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROPOSAL_PATH = PROJECT_ROOT / "docs" / "CIVILIZATION_CORE_VIDEO_AI_SKILLS_MEMORY_PROPOSAL.md"
SMOKE_SCRIPT = PROJECT_ROOT / "scripts" / "smoke_governed_memory_proposal_pack_dry_run.py"


def _result() -> dict[str, object]:
    return build_governed_memory_proposal_pack_dry_run(PROPOSAL_PATH)


def _entries_for(result: dict[str, object], section: str) -> list[dict[str, object]]:
    return [entry for entry in result["entries"] if entry["section"] == section]


def _entry(result: dict[str, object], entry_key: str) -> dict[str, object]:
    return next(entry for entry in result["entries"] if entry["entry_key"] == entry_key)


def _assert_no_write_flags(value: dict[str, object]) -> None:
    assert value["writes_memory"] is False
    assert value["writes_graph"] is False
    assert value["writes_operation_ledger"] is False
    assert value["writes_config"] is False
    assert value["writes_sqlite"] is False
    assert value["invokes_real_executor"] is False
    assert value["provider_tools"] == []


def test_pack_status_ready_and_source_digest_stable():
    first = _result()
    second = _result()

    assert first["version"] == "2.4.0"
    assert first["pack_status"] == "ready"
    assert first["source_sha256"]
    assert first["source_sha256"] == second["source_sha256"]
    assert first == second


def test_required_sections_are_present():
    result = _result()

    assert result["sections_present"] == [
        "long_term_memory_candidates",
        "short_term_memory_candidates",
        "operation_ledger_candidates",
        "knowledge_surface_candidates",
        "do_not_persist",
        "risk_notes",
    ]
    assert result["missing_sections"] == []


def test_counts_are_nonzero():
    result = _result()

    assert result["entry_count"] > 0
    assert result["proposed_count"] > 0
    assert result["rejected_count"] > 0
    assert result["risk_note_count"] > 0


def test_long_term_memory_candidates_are_proposed_but_not_written():
    result = _result()
    entries = _entries_for(result, "long_term_memory_candidates")

    assert entries
    assert any(entry["status"] == "proposed" for entry in entries)
    for entry in entries:
        if entry["status"] == "proposed":
            assert entry["target_surface"] == "long_term_memory"
        _assert_no_write_flags(entry)


def test_short_term_candidates_are_proposed_but_not_written():
    result = _result()
    entries = _entries_for(result, "short_term_memory_candidates")

    assert entries
    assert any(entry["status"] == "proposed" for entry in entries)
    for entry in entries:
        if entry["status"] == "proposed":
            assert entry["target_surface"] == "short_term_memory"
        _assert_no_write_flags(entry)


def test_operation_ledger_candidates_are_proposed_but_not_appended():
    result = _result()
    entries = _entries_for(result, "operation_ledger_candidates")

    assert entries
    assert any(entry["target_surface"] == "operation_ledger" for entry in entries)
    for entry in entries:
        _assert_no_write_flags(entry)
        assert entry["writes_operation_ledger"] is False


def test_knowledge_surface_candidates_are_proposed_but_not_written():
    result = _result()
    entries = _entries_for(result, "knowledge_surface_candidates")

    assert entries
    assert all(entry["status"] == "proposed" for entry in entries)
    assert all(entry["target_surface"] == "knowledge_surface" for entry in entries)
    for entry in entries:
        _assert_no_write_flags(entry)


def test_temporary_command_authorizations_are_rejected_or_non_durable():
    result = _result()
    entry = _entry(result, "temporary_command_authorizations")

    assert entry["status"] == "rejected"
    assert entry["target_surface"] == "rejected_do_not_persist"
    assert entry["must_not_become_durable_memory"] is True
    assert "temporary_command_authorization" in entry["non_durable_reasons"]
    assert entry in result["rejected_entries"]


def test_api_key_or_secret_mention_is_not_persisted_as_durable_memory():
    result = _result()
    rejected = result["rejected_entries"]

    assert any("api_key_or_secret" in entry["non_durable_reasons"] for entry in rejected)
    assert any("raw_credentials" in entry["non_durable_reasons"] for entry in rejected)
    for entry in rejected:
        if "api_key_or_secret" in entry["non_durable_reasons"]:
            assert entry["must_not_become_durable_memory"] is True
            _assert_no_write_flags(entry)


def test_provider_tools_empty_and_all_report_write_flags_false():
    result = _result()

    _assert_no_write_flags(result)
    assert result["creates_real_memory_write_proposal"] is False
    assert result["creates_real_operation_ledger_entry"] is False
    assert result["modifies_hermes_agent"] is False
    assert result["no_network_surface"] is True
    assert result["safety_summary"]["provider_tools"] == []


def test_report_is_json_serializable():
    result = _result()

    payload = governed_memory_proposal_pack_to_json(result)
    decoded = json.loads(payload)

    assert decoded["pack_status"] == "ready"
    assert decoded["entries"] == result["entries"]


def test_smoke_script_exits_zero():
    completed = subprocess.run(
        [sys.executable, str(SMOKE_SCRIPT)],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert completed.stdout == "governed_memory_proposal_pack_dry_run=passed\n"
    assert completed.stderr == ""
