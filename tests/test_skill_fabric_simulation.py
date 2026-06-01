import json
from pathlib import Path

from hermes_memory_fabric.skill_fabric_simulation import (
    skill_fabric_simulation_to_json,
    run_skill_fabric_github_archive_simulation,
)


def test_skill_fabric_github_archive_simulation_passes(tmp_path):
    result = run_skill_fabric_github_archive_simulation(tmp_path)

    assert result["version"] == "2.2.0"
    assert result["simulation_status"] == "pass"
    assert result["verify_status"] == "pass"
    assert result["import_status"] == "imported"
    assert result["imported_skill"] == "demo-skill"


def test_skill_fabric_github_archive_simulation_safety_boundaries(tmp_path):
    result = run_skill_fabric_github_archive_simulation(tmp_path)

    assert result["dry_run_network"] is True
    assert result["used_network"] is False
    assert result["used_local_archive"] is True
    assert result["plan_would_fetch"] is False
    assert result["plan_would_write"] is False
    assert result["provider_tools"] == []
    assert result["writes_hermes_memory"] is False
    assert result["modifies_hermes_agent"] is False
    assert result["executes_composio"] is False
    assert result["performs_github_write"] is False


def test_skill_fabric_projection_marker_and_unprojection(tmp_path):
    result = run_skill_fabric_github_archive_simulation(tmp_path)

    assert result["projected"] is True
    assert result["projection_marker_exists"] is True
    assert result["unprojected"] is True
    assert result["unmanaged_path_touched"] is False
    assert "unmanaged-skill/SKILL.md" in result["codex_projection_files"]
    assert "demo-skill/SKILL.md" not in result["codex_projection_files"]


def test_skill_fabric_simulation_temp_files_are_local_and_safe(tmp_path):
    result = run_skill_fabric_github_archive_simulation(tmp_path)

    assert result["archive_path_traversal"] is False
    assert result["temp_root_files"]
    for relative in result["temp_root_files"]:
        assert not Path(relative).is_absolute()
        assert ".." not in Path(relative).parts
        assert (tmp_path / relative).resolve().is_relative_to(tmp_path.resolve())
    assert "skill-fabric/registry.json" in result["temp_root_files"]
    assert "skill-fabric/audit/skill_operation_ledger.jsonl" in result["temp_root_files"]
    assert "github-skill-archive.zip" in result["temp_root_files"]


def test_skill_fabric_simulation_report_is_json_serializable(tmp_path):
    result = run_skill_fabric_github_archive_simulation(tmp_path)

    payload = skill_fabric_simulation_to_json(result)
    decoded = json.loads(payload)

    assert decoded["simulation_status"] == "pass"
    assert decoded["archive_sha256"] == result["archive_sha256"]
