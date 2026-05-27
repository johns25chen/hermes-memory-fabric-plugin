from __future__ import annotations

import io
import json
from pathlib import Path

from hermes_memory_fabric import MemoryFabricProvider
from hermes_memory_fabric.candidate_jsonl_source import load_candidate_jsonl_source
from hermes_memory_fabric.codex_task_summary_ingestion import (
    DEFAULT_PROJECT_ID,
    candidates_to_jsonl,
    cli_main,
    generate_codex_task_summary_candidates,
    parse_codex_task_summary,
    write_candidates_jsonl,
)


def _summary() -> str:
    return """# v1.3.0 Codex Task Summary Ingestion Dry Run

Goal / Purpose
Implement Codex task summary ingestion dry run for Memory Fabric candidates.

Included / Changed files
- src/hermes_memory_fabric/codex_task_summary_ingestion.py
- scripts/ingest_codex_task_summary_dry_run.py

Validation
- PYTHONPATH="$PWD/src:$PWD" /Users/han/.hermes/hermes-agent/.venv/bin/python -m pytest -o addopts='' tests/test_codex_task_summary_ingestion.py -q
- PYTHONPATH="$PWD/src:$PWD" /Users/han/.hermes/hermes-agent/.venv/bin/python scripts/smoke_codex_task_summary_ingestion.py

Boundary
- Dry-run candidate generation only.
- No model calls.
- No network calls.
- No provider tools.

Version
1.3.0

Result
Generated JSONL candidates from explicit Codex task summary sections.
"""


def _candidate_by_kind(candidates, kind):
    return next(candidate for candidate in candidates if kind in candidate["tags"])


def test_parses_structured_sections():
    parsed = parse_codex_task_summary(_summary())

    keys = [section["key"] for section in parsed["sections"]]
    assert keys == ["goal", "changed_files", "validation", "boundary", "version", "result"]
    assert parsed["section_map"]["goal"][0]["content"].startswith("Implement Codex task summary ingestion")
    assert parsed["section_map"]["validation"][0]["line_start"] > parsed["section_map"]["goal"][0]["line_start"]


def test_emits_deterministic_candidate_ids():
    first = generate_codex_task_summary_candidates(_summary())
    second = generate_codex_task_summary_candidates(_summary())

    assert [candidate["id"] for candidate in first] == [candidate["id"] for candidate in second]
    assert candidates_to_jsonl(first) == candidates_to_jsonl(second)


def test_preserves_validation_evidence():
    candidates = generate_codex_task_summary_candidates(_summary())
    validation = _candidate_by_kind(candidates, "validation")

    assert "tests/test_codex_task_summary_ingestion.py -q" in validation["content"]
    assert "scripts/smoke_codex_task_summary_ingestion.py" in validation["content"]


def test_preserves_boundary_limitations():
    candidates = generate_codex_task_summary_candidates(_summary())
    boundary = _candidate_by_kind(candidates, "boundary")

    assert "Dry-run candidate generation only." in boundary["content"]
    assert "No model calls." in boundary["content"]
    assert "No network calls." in boundary["content"]
    assert "No provider tools." in boundary["content"]


def test_defaults_to_low_risk_for_normal_summaries():
    candidates = generate_codex_task_summary_candidates(_summary())

    assert {candidate["risk_level"] for candidate in candidates} == {"low"}


def test_escalates_risk_when_high_risk_terms_appear():
    text = """Goal
Review auth token credential handling and executor migration approval deletion behavior.

Result
Captured the risky terms in an explicit summary section.
"""

    candidates = generate_codex_task_summary_candidates(text)

    assert _candidate_by_kind(candidates, "capability")["risk_level"] == "high"


def test_stdout_mode_does_not_write_files(tmp_path):
    input_path = tmp_path / "summary.txt"
    input_path.write_text(_summary(), encoding="utf-8")
    stdout = io.StringIO()
    stderr = io.StringIO()
    before = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*"))

    exit_code = cli_main(["--input", str(input_path)], stdout=stdout, stderr=stderr)

    after = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*"))
    assert exit_code == 0
    assert after == before == [Path("summary.txt")]
    assert stdout.getvalue().strip()
    assert stderr.getvalue() == ""
    assert all(json.loads(line)["governance"]["dry_run"] is True for line in stdout.getvalue().splitlines())


def test_explicit_output_writes_only_to_requested_path(tmp_path):
    input_path = tmp_path / "summary.txt"
    output_path = tmp_path / "generated.jsonl"
    input_path.write_text(_summary(), encoding="utf-8")
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = cli_main(
        ["--input", str(input_path), "--output", str(output_path), "--print-summary"],
        stdout=stdout,
        stderr=stderr,
    )

    assert exit_code == 0
    assert sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*")) == [
        Path("generated.jsonl"),
        Path("summary.txt"),
    ]
    assert stdout.getvalue() == ""
    assert "codex_task_summary_ingestion_summary=" in stderr.getvalue()
    assert output_path.read_text(encoding="utf-8").strip()


def test_no_writes_to_home_hermes(tmp_path, monkeypatch):
    input_path = tmp_path / "summary.txt"
    home = tmp_path / "home"
    hermes_home = home / ".hermes"
    input_path.write_text(_summary(), encoding="utf-8")
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))

    exit_code = cli_main(["--input", str(input_path)], stdout=io.StringIO(), stderr=io.StringIO())

    assert exit_code == 0
    assert not hermes_home.exists()


def test_generated_jsonl_can_be_loaded_by_existing_candidate_jsonl_source(tmp_path):
    candidates = generate_codex_task_summary_candidates(_summary())
    output_path = tmp_path / "generated.jsonl"

    write_candidates_jsonl(candidates, output_path)
    loaded = load_candidate_jsonl_source(output_path, required_fields=["id", "content"])

    assert loaded == candidates
    assert {field for candidate in loaded for field in candidate} >= {
        "id",
        "content",
        "project_id",
        "entity_ids",
        "source",
        "provenance",
        "risk_level",
        "governance",
        "created_at",
        "tags",
    }


def test_generated_candidates_can_feed_memory_fabric_provider_prefetch(tmp_path):
    candidates = generate_codex_task_summary_candidates(_summary())
    output_path = tmp_path / "generated.jsonl"
    write_candidates_jsonl(candidates, output_path)
    provider = MemoryFabricProvider(
        runtime_config={
            "project_scope": DEFAULT_PROJECT_ID,
            "candidate_jsonl_path": str(output_path),
            "candidate_jsonl_required_fields": ["id", "content"],
            "memory_limit": 5,
            "context_budget_chars": 2400,
        }
    )

    context = provider.prefetch("Codex task summary ingestion dry run Memory Fabric candidates")

    assert "Implement Codex task summary ingestion dry run for Memory Fabric candidates." in context
    assert provider.get_tool_schemas() == []
