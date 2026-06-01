"""Local Skill Fabric simulation for GitHub-style archive imports.

This module creates a deterministic local zip archive that looks like a pinned
GitHub repository archive, imports one scoped skill from it, projects it to a
temporary Codex skills directory, and verifies the managed unprojection path.
It never fetches from the network and never writes Hermes memory.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from .skill_fabric import (
    PROJECTION_MARKER,
    SkillFabricPaths,
    import_github_archive,
    initialize_skill_fabric,
    plan_github_skill_import,
    project_skill_to_codex,
    unproject_skill_from_codex,
    verify_skill_fabric,
)


SIMULATION_VERSION = "2.2.0"
_OWNER = "HermesMemoryFabric"
_REPO = "skill-fabric-simulation"
_REF = "0123456789abcdef0123456789abcdef01234567"
_SKILL_PATH = "skills/demo-skill"
_SKILL_NAME = "demo-skill"
_ARCHIVE_ROOT = f"{_REPO}-{_REF[:12]}"
_ZIP_DATE_TIME = (2024, 1, 1, 0, 0, 0)


def run_skill_fabric_github_archive_simulation(temp_root: Path | None = None) -> dict[str, Any]:
    """Run the deterministic local GitHub archive simulation.

    Args:
        temp_root: Optional caller-owned temporary root. If omitted, a
            TemporaryDirectory is used for the duration of the simulation.

    Returns:
        A JSON-serializable report describing the import, projection,
        unprojection, verification, and safety boundary results.
    """

    if temp_root is None:
        with tempfile.TemporaryDirectory(prefix="skill-fabric-simulation-") as directory:
            return _run_simulation(Path(directory))
    return _run_simulation(Path(temp_root))


def skill_fabric_simulation_to_json(result: dict[str, Any]) -> str:
    """Serialize a simulation report with deterministic key ordering."""

    return json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _run_simulation(temp_root: Path) -> dict[str, Any]:
    temp_root = temp_root.resolve()
    temp_root.mkdir(parents=True, exist_ok=True)
    fabric_root = temp_root / "skill-fabric"
    paths = SkillFabricPaths(fabric_root)
    codex_skills_dir = temp_root / "codex-skills"
    unmanaged_dir = codex_skills_dir / "unmanaged-skill"
    unmanaged_dir.mkdir(parents=True, exist_ok=True)
    unmanaged_file = unmanaged_dir / "SKILL.md"
    unmanaged_file.write_text("# Unmanaged\n\nThis file must remain untouched.\n", encoding="utf-8")
    unmanaged_before = unmanaged_file.read_text(encoding="utf-8")

    archive_path = temp_root / "github-skill-archive.zip"
    _write_fake_github_archive(archive_path)
    archive_sha256 = hashlib.sha256(archive_path.read_bytes()).hexdigest()

    initialize_skill_fabric(paths)
    plan = plan_github_skill_import(
        f"{_OWNER}/{_REPO}/{_SKILL_PATH}",
        ref=_REF,
        path=_SKILL_PATH,
    )
    imported = import_github_archive(
        f"{_OWNER}/{_REPO}/{_SKILL_PATH}",
        paths=paths,
        ref=_REF,
        path=_SKILL_PATH,
        archive_path=archive_path,
        expected_archive_sha256=archive_sha256,
        approved_by="skill-fabric-simulation",
        temp_dir=temp_root / "extract-work",
    )
    imported_skill = str(imported["imported"]["skill"])
    imported_version = str(imported["imported"]["version"])
    projected = project_skill_to_codex(imported_skill, paths=paths, codex_skills_dir=codex_skills_dir, mode="copy")
    projection_target = Path(projected["target"])
    projection_marker_exists = (projection_target / PROJECTION_MARKER).is_file()
    unprojected = unproject_skill_from_codex(imported_skill, paths=paths, codex_skills_dir=codex_skills_dir)
    unmanaged_after = unmanaged_file.read_text(encoding="utf-8")
    verify = verify_skill_fabric(paths)
    ledger_events = _ledger_events(paths.ledger_path)
    registry = json.loads(paths.registry_path.read_text(encoding="utf-8"))

    required_files_exist = paths.registry_path.is_file() and paths.lock_path.is_file() and paths.ledger_path.is_file()
    unmanaged_touched = unmanaged_before != unmanaged_after or not unmanaged_file.is_file()
    simulation_passed = (
        plan["status"] == "ready_for_local_archive_import"
        and plan["would_fetch"] is False
        and plan["would_write"] is False
        and imported["status"] == "imported"
        and projected["skill"] == imported_skill
        and projection_marker_exists
        and unprojected["status"] == "removed"
        and not (codex_skills_dir / imported_skill).exists()
        and not unmanaged_touched
        and verify["status"] == "pass"
        and required_files_exist
    )

    return {
        "version": SIMULATION_VERSION,
        "simulation_status": "pass" if simulation_passed else "fail",
        "dry_run_network": True,
        "used_network": False,
        "used_local_archive": True,
        "archive_sha256": archive_sha256,
        "plan_status": plan["status"],
        "plan_would_fetch": plan["would_fetch"],
        "plan_would_write": plan["would_write"],
        "import_status": imported["status"],
        "imported_skill": imported_skill,
        "imported_version": imported_version,
        "registry_version": registry.get("registry_version"),
        "ledger_events": ledger_events,
        "projected": projected["skill"] == imported_skill,
        "projection_marker_exists": projection_marker_exists,
        "unprojected": unprojected["status"] == "removed",
        "verify_status": verify["status"],
        "provider_tools": [],
        "writes_hermes_memory": False,
        "modifies_hermes_agent": False,
        "executes_composio": False,
        "performs_github_write": False,
        "temp_root_files": _relative_files(temp_root, temp_root),
        "codex_projection_files": _relative_files(codex_skills_dir, codex_skills_dir),
        "archive_path_traversal": False,
        "unmanaged_path_touched": unmanaged_touched,
        "safety_summary": {
            "network": "not used; GitHub planning is dry-run only",
            "archive": "local deterministic zip with a single scoped SKILL.md",
            "hermes_memory": "not written",
            "hermes_agent": "not modified",
            "provider_tools": "not exposed",
            "composio": "not executed",
            "github_write": "not performed",
            "archive_path_traversal": "not used",
            "unmanaged_projection": "left untouched",
        },
    }


def _write_fake_github_archive(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    skill_text = """---
name: demo-skill
description: Deterministic local simulation skill for scoped archive import.
---

# Demo Skill

Use temporary local files only.
"""
    with ZipFile(path, "w", compression=ZIP_DEFLATED) as archive:
        info = ZipInfo(f"{_ARCHIVE_ROOT}/{_SKILL_PATH}/SKILL.md", _ZIP_DATE_TIME)
        info.compress_type = ZIP_DEFLATED
        archive.writestr(info, skill_text)


def _ledger_events(path: Path) -> list[str]:
    events: list[str] = []
    if not path.is_file():
        return events
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            events.append(str(json.loads(line)["event"]))
    return events


def _relative_files(root: Path, base: Path) -> list[str]:
    if not root.exists():
        return []
    files = []
    for file_path in sorted(path for path in root.rglob("*") if path.is_file() or path.is_symlink()):
        files.append(file_path.relative_to(base).as_posix())
    return files
