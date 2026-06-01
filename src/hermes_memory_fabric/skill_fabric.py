"""Governed shared Skill Fabric for Codex and OpenClaw projections.

The fabric stores one canonical copy of approved Codex skills, projects thin
runtime views into Codex/OpenClaw, and records operation metadata. It does not
write Hermes memory or mutate OpenClaw config.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
from typing import Any, Iterable, Mapping
from urllib.parse import urlparse
from zipfile import ZipFile


REGISTRY_VERSION = 2
PROJECTION_MARKER = ".skill-fabric-projection.json"

RISK_PATTERNS: Mapping[str, tuple[str, str]] = {
    "curl_pipe_shell": ("high", "curl piped to shell"),
    "composio_cli": ("review", "Composio CLI action surface"),
    "slack_send": ("review", "Slack write surface"),
    "github_write": ("review", "GitHub write surface"),
    "memory_write": ("review", "Hermes governed memory write surface"),
    "shell_exec": ("review", "shell execution guidance"),
    "network": ("review", "network access guidance"),
}


class SkillFabricError(Exception):
    """Raised when a governed skill operation cannot proceed."""


@dataclass(frozen=True)
class SkillFabricPaths:
    root: Path

    @property
    def skills_dir(self) -> Path:
        return self.root / "skills"

    @property
    def locks_dir(self) -> Path:
        return self.root / "locks"

    @property
    def audit_dir(self) -> Path:
        return self.root / "audit"

    @property
    def openclaw_dir(self) -> Path:
        return self.root / "openclaw"

    @property
    def registry_path(self) -> Path:
        return self.root / "registry.json"

    @property
    def lock_path(self) -> Path:
        return self.locks_dir / "skills.lock.json"

    @property
    def ledger_path(self) -> Path:
        return self.audit_dir / "skill_operation_ledger.jsonl"

    @property
    def openclaw_projection_path(self) -> Path:
        return self.openclaw_dir / "registry.json"


@dataclass(frozen=True)
class SkillAudit:
    name: str
    description: str
    sha256: str
    file_count: int
    capabilities: tuple[str, ...]
    capability_manifest: dict[str, Any]
    risk_level: str
    findings: tuple[dict[str, str], ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "sha256": self.sha256,
            "file_count": self.file_count,
            "capabilities": list(self.capabilities),
            "capability_manifest": self.capability_manifest,
            "risk_level": self.risk_level,
            "findings": list(self.findings),
        }


def default_fabric_paths(home: Path | None = None) -> SkillFabricPaths:
    base_home = Path.home() if home is None else home
    return SkillFabricPaths(base_home / ".openclaw" / "skill-fabric")


def initialize_skill_fabric(paths: SkillFabricPaths) -> dict[str, Any]:
    for directory in (paths.root, paths.skills_dir, paths.locks_dir, paths.audit_dir, paths.openclaw_dir):
        directory.mkdir(parents=True, exist_ok=True)
    registry = _read_json(paths.registry_path, _empty_registry())
    lock = _read_json(paths.lock_path, _empty_lock())
    _write_json(paths.registry_path, registry)
    _write_json(paths.lock_path, lock)
    _write_json(paths.openclaw_projection_path, _openclaw_projection(registry))
    _append_ledger(paths, "skill_fabric_initialized", {"root": str(paths.root)})
    return {"registry": registry, "lock": lock, "paths": _paths_dict(paths)}


def audit_skill_directory(source_dir: Path, *, name: str | None = None) -> SkillAudit:
    source = source_dir.resolve()
    if not source.is_dir():
        raise SkillFabricError(f"Skill source directory does not exist: {source_dir}")
    skill_md = source / "SKILL.md"
    if not skill_md.is_file():
        raise SkillFabricError(f"SKILL.md not found in skill source: {source_dir}")

    metadata, body = _read_skill_metadata(skill_md)
    skill_name = name or str(metadata.get("name") or source.name)
    _validate_skill_name(skill_name)
    description = str(metadata.get("description") or "")
    digest, file_count, text_blob = _hash_directory(source)
    findings = _scan_risks(text_blob)
    if "Claude" in description or "Claude" in body[:500]:
        findings.append({"id": "claude_residue", "severity": "review", "message": "Skill text appears to contain Claude-specific residue."})
    manifest = _capability_manifest(findings, text_blob)
    return SkillAudit(
        name=skill_name,
        description=description,
        sha256=digest,
        file_count=file_count,
        capabilities=tuple(sorted(manifest["declared"])),
        capability_manifest=manifest,
        risk_level=_risk_level(findings),
        findings=tuple(findings),
    )


def import_skill_directory(
    source_dir: Path,
    *,
    paths: SkillFabricPaths,
    name: str | None = None,
    source: Mapping[str, Any] | None = None,
    approved_by: str | None = None,
) -> dict[str, Any]:
    initialize_skill_fabric(paths)
    audit = audit_skill_directory(source_dir, name=name)
    version_id = audit.sha256[:16]
    destination = paths.skills_dir / audit.name / version_id
    if destination.exists():
        raise SkillFabricError(f"Skill version already exists: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_dir, destination, ignore=shutil.ignore_patterns(".git", "__pycache__", ".DS_Store"))

    registry = _read_json(paths.registry_path, _empty_registry())
    lock = _read_json(paths.lock_path, _empty_lock())
    now = _now()
    version_entry = {
        "path": str(destination),
        "sha256": audit.sha256,
        "description": audit.description,
        "capabilities": list(audit.capabilities),
        "capability_manifest": audit.capability_manifest,
        "risk_level": audit.risk_level,
        "findings": list(audit.findings),
        "source": dict(source or {"type": "local_directory", "path": str(source_dir)}),
        "approved_by": approved_by,
        "installed_at": now,
    }
    skills = registry.setdefault("skills", {})
    if audit.name not in skills:
        skills[audit.name] = {"name": audit.name, "versions": {}, "created_at": now}
    previous_active_version = skills[audit.name].get("active_version")
    skills[audit.name].setdefault("versions", {})[version_id] = version_entry
    skills[audit.name]["active_version"] = version_id
    skills[audit.name]["previous_active_version"] = previous_active_version
    skills[audit.name]["updated_at"] = now
    registry["updated_at"] = now
    _write_json(paths.registry_path, registry)

    lock.setdefault("skills", {})[audit.name] = {
        "active_version": version_id,
        "sha256": audit.sha256,
        "path": str(destination),
        "risk_level": audit.risk_level,
        "capability_manifest": audit.capability_manifest,
        "updated_at": now,
    }
    lock["updated_at"] = now
    _write_json(paths.lock_path, lock)
    _write_json(paths.openclaw_projection_path, _openclaw_projection(registry))
    _append_ledger(paths, "skill_imported", {"skill": audit.name, "version": version_id, "sha256": audit.sha256, "risk_level": audit.risk_level})
    return {"skill": audit.name, "version": version_id, "audit": audit.to_dict(), "path": str(destination)}


def lint_skill_triggers(skill_dirs: Iterable[Path]) -> dict[str, Any]:
    audits = [audit_skill_directory(path) for path in skill_dirs]
    by_name: dict[str, list[SkillAudit]] = {}
    broad: list[dict[str, str]] = []
    overlaps: list[dict[str, Any]] = []
    for audit in audits:
        by_name.setdefault(audit.name, []).append(audit)
        reason = _broad_trigger_reason(audit.description)
        if reason:
            broad.append({"skill": audit.name, "description": audit.description, "reason": reason})
    for name, group in sorted(by_name.items()):
        if len(group) > 1:
            overlaps.append({"type": "duplicate_name", "skill": name, "count": len(group)})
    for left_index, left in enumerate(audits):
        for right in audits[left_index + 1 :]:
            score = _description_overlap_score(left.description, right.description)
            if score >= 0.55:
                overlaps.append({"type": "description_overlap", "left": left.name, "right": right.name, "score": round(score, 3)})
    return {"status": "pass" if not broad and not overlaps else "review", "skill_count": len(audits), "broad_triggers": broad, "overlaps": overlaps}


def audit_skill_repository(root_dir: Path, *, max_depth: int = 3) -> dict[str, Any]:
    root = root_dir.resolve()
    if not root.is_dir():
        raise SkillFabricError(f"Repository directory does not exist: {root_dir}")
    if max_depth < 0:
        raise SkillFabricError("max_depth must be non-negative.")
    skill_dirs = _find_skill_dirs(root, max_depth=max_depth)
    audits = []
    risk_counts: dict[str, int] = {}
    import_candidates = []
    review_required = []
    for skill_dir in skill_dirs:
        audit = audit_skill_directory(skill_dir)
        audit_dict = audit.to_dict()
        audit_dict["relative_path"] = skill_dir.relative_to(root).as_posix()
        audits.append(audit_dict)
        risk_counts[audit.risk_level] = risk_counts.get(audit.risk_level, 0) + 1
        target = import_candidates if audit.risk_level == "low" else review_required
        target.append({"name": audit.name, "relative_path": audit_dict["relative_path"], "risk_level": audit.risk_level})
    trigger_lint = lint_skill_triggers(skill_dirs) if skill_dirs else {"status": "pass", "skill_count": 0, "broad_triggers": [], "overlaps": []}
    return {
        "status": "pass" if trigger_lint["status"] == "pass" and not review_required else "review",
        "root": str(root),
        "skill_count": len(audits),
        "risk_counts": risk_counts,
        "skills": audits,
        "trigger_lint": trigger_lint,
        "import_candidates": import_candidates,
        "review_required": review_required,
    }


def plan_github_skill_import(url_or_spec: str, *, ref: str | None = None, path: str | None = None) -> dict[str, Any]:
    parsed = _parse_github_skill_spec(url_or_spec)
    requested_ref = ref or parsed.get("ref")
    requested_path = path or parsed.get("path")
    findings: list[dict[str, str]] = []
    if not requested_ref:
        findings.append({"id": "missing_ref", "severity": "block", "message": "GitHub skill import planning requires an explicit branch, tag, or commit."})
    elif not _looks_like_commit_sha(requested_ref):
        findings.append({"id": "unpinned_commit", "severity": "review", "message": "Ref is not a full commit SHA; resolve and pin the commit before import."})
    if not requested_path:
        findings.append({"id": "missing_skill_path", "severity": "block", "message": "Skill path is required so the importer does not ingest an entire repository."})
    if requested_path and (requested_path.startswith("/") or ".." in Path(requested_path).parts):
        findings.append({"id": "unsafe_skill_path", "severity": "block", "message": "Skill path must be a safe relative path inside the repository."})
    status = "ready_for_local_archive_import" if not any(f["severity"] == "block" for f in findings) else "blocked"
    if status == "ready_for_local_archive_import" and any(f["severity"] == "review" for f in findings):
        status = "needs_pin_resolution"
    source = {"type": "github", "owner": parsed["owner"], "repo": parsed["repo"], "ref": requested_ref, "path": requested_path, "url": f"https://github.com/{parsed['owner']}/{parsed['repo']}"}
    return {
        "status": status,
        "source": source,
        "dry_run": True,
        "would_fetch": False,
        "would_write": False,
        "required_next_steps": _github_plan_next_steps(status),
        "findings": findings,
    }


def import_github_archive(
    url_or_spec: str,
    *,
    paths: SkillFabricPaths,
    ref: str | None = None,
    path: str | None = None,
    archive_path: Path,
    expected_archive_sha256: str,
    approved_by: str,
    temp_dir: Path | None = None,
) -> dict[str, Any]:
    plan = plan_github_skill_import(url_or_spec, ref=ref, path=path)
    if plan["status"] != "ready_for_local_archive_import":
        return {"status": "blocked", "plan": plan, "imported": None}
    if not archive_path:
        raise SkillFabricError("A local GitHub archive path is required.")
    if not expected_archive_sha256 or not re.fullmatch(r"[0-9a-fA-F]{64}", expected_archive_sha256):
        raise SkillFabricError("Expected archive sha256 is required and must be a 64-character hex digest.")
    if not approved_by:
        raise SkillFabricError("Manual approval is required for local GitHub archive import.")

    source = plan["source"]
    work_parent = temp_dir or Path(tempfile.mkdtemp(prefix="skill-fabric-github-"))
    work_parent.mkdir(parents=True, exist_ok=True)
    archive = archive_path.expanduser().resolve()
    if not archive.is_file():
        raise SkillFabricError(f"Local GitHub archive does not exist: {archive_path}")
    archive_sha256 = _file_sha256(archive)
    if archive_sha256.lower() != expected_archive_sha256.lower():
        raise SkillFabricError("GitHub archive sha256 did not match expected hash.")
    extracted_root = _extract_github_archive(archive, work_parent / "extracted")
    skill_path = extracted_root / str(source["path"])
    if not skill_path.is_dir():
        raise SkillFabricError(f"Skill path not found inside GitHub archive: {source['path']}")
    imported = import_skill_directory(skill_path, paths=paths, source=source, approved_by=approved_by)
    _append_ledger(paths, "github_archive_skill_imported", {"owner": source["owner"], "repo": source["repo"], "ref": source["ref"], "path": source["path"], "skill": imported["skill"], "version": imported["version"], "archive_sha256": archive_sha256})
    return {"status": "imported", "plan": plan, "archive_sha256": archive_sha256, "imported": imported}


def fetch_github_skill_import(*_args: Any, **_kwargs: Any) -> dict[str, Any]:
    raise SkillFabricError("fetch-github-import is disabled; use import-github-archive with an existing local archive, explicit metadata, expected sha256, and manual approval.")


def project_skill_to_codex(skill_name: str, *, paths: SkillFabricPaths, codex_skills_dir: Path, mode: str = "symlink") -> dict[str, Any]:
    if mode not in {"symlink", "copy"}:
        raise SkillFabricError("Projection mode must be 'symlink' or 'copy'.")
    source_path, version_id = _active_skill_path(paths, skill_name)
    codex_skills_dir.mkdir(parents=True, exist_ok=True)
    target = codex_skills_dir / skill_name
    _remove_managed_projection(target)
    if mode == "symlink":
        target.symlink_to(source_path, target_is_directory=True)
        _write_json(codex_skills_dir / f".{skill_name}.skill-fabric-projection.json", _projection_marker(paths, skill_name, version_id))
    else:
        shutil.copytree(source_path, target)
        _write_json(target / PROJECTION_MARKER, _projection_marker(paths, skill_name, version_id))
    _append_ledger(paths, "skill_projected_to_codex", {"skill": skill_name, "version": version_id, "mode": mode, "target": str(target)})
    return {"skill": skill_name, "version": version_id, "target": str(target), "mode": mode}


def project_all_skills_to_codex(*, paths: SkillFabricPaths, codex_skills_dir: Path, mode: str = "symlink") -> dict[str, Any]:
    registry = _read_json(paths.registry_path, _empty_registry())
    projected, failures = [], []
    for name in sorted((registry.get("skills") or {}).keys()):
        try:
            projected.append(project_skill_to_codex(name, paths=paths, codex_skills_dir=codex_skills_dir, mode=mode))
        except SkillFabricError as exc:
            failures.append({"skill": name, "reason": str(exc)})
    status = "pass" if not failures else "partial"
    _append_ledger(paths, "all_skills_projected_to_codex", {"status": status, "projected_count": len(projected), "failure_count": len(failures)})
    return {"status": status, "projected": projected, "failures": failures}


def list_skill_versions(paths: SkillFabricPaths, skill_name: str) -> dict[str, Any]:
    registry = _read_json(paths.registry_path, _empty_registry())
    skill = registry.get("skills", {}).get(skill_name)
    if not isinstance(skill, dict):
        raise SkillFabricError(f"Skill is not registered: {skill_name}")
    active_version = skill.get("active_version")
    versions = []
    for version_id, version in sorted((skill.get("versions") or {}).items()):
        if not isinstance(version, dict):
            continue
        versions.append(
            {
                "version": version_id,
                "active": version_id == active_version,
                "sha256": version.get("sha256"),
                "risk_level": version.get("risk_level"),
                "path": version.get("path"),
                "path_exists": Path(str(version.get("path"))).is_dir(),
                "installed_at": version.get("installed_at"),
                "source": version.get("source"),
            }
        )
    return {"skill": skill_name, "active_version": active_version, "versions": versions}


def activate_skill_version(paths: SkillFabricPaths, skill_name: str, version_id: str) -> dict[str, Any]:
    registry = _read_json(paths.registry_path, _empty_registry())
    lock = _read_json(paths.lock_path, _empty_lock())
    skill = registry.get("skills", {}).get(skill_name)
    if not isinstance(skill, dict):
        raise SkillFabricError(f"Skill is not registered: {skill_name}")
    version = (skill.get("versions") or {}).get(version_id)
    if not isinstance(version, dict):
        raise SkillFabricError(f"Skill version is not registered: {skill_name}@{version_id}")
    path = Path(str(version.get("path") or ""))
    if not path.is_dir():
        raise SkillFabricError(f"Skill version path is missing: {path}")
    digest, _count, _text = _hash_directory(path)
    if digest != version.get("sha256"):
        raise SkillFabricError("Refusing to activate skill version with mismatched content hash.")

    now = _now()
    previous_active_version = skill.get("active_version")
    skill["active_version"] = version_id
    skill["previous_active_version"] = previous_active_version
    skill["updated_at"] = now
    registry["updated_at"] = now
    _write_json(paths.registry_path, registry)
    lock.setdefault("skills", {})[skill_name] = {
        "active_version": version_id,
        "sha256": version["sha256"],
        "path": version["path"],
        "risk_level": version.get("risk_level"),
        "capability_manifest": version.get("capability_manifest", {}),
        "updated_at": now,
    }
    lock["updated_at"] = now
    _write_json(paths.lock_path, lock)
    _write_json(paths.openclaw_projection_path, _openclaw_projection(registry))
    _append_ledger(paths, "skill_version_activated", {"skill": skill_name, "version": version_id, "sha256": version["sha256"]})
    return {"skill": skill_name, "active_version": version_id, "sha256": version["sha256"], "path": version["path"]}


def rollback_skill_version(paths: SkillFabricPaths, skill_name: str) -> dict[str, Any]:
    registry = _read_json(paths.registry_path, _empty_registry())
    skill = registry.get("skills", {}).get(skill_name)
    if not isinstance(skill, dict):
        raise SkillFabricError(f"Skill is not registered: {skill_name}")
    previous_version = str(skill.get("previous_active_version") or "")
    if not previous_version:
        raise SkillFabricError(f"No rollback version recorded for skill: {skill_name}")
    current_version = str(skill.get("active_version") or "")
    result = activate_skill_version(paths, skill_name, previous_version)
    result["rolled_back_from"] = current_version
    result["status"] = "rolled_back"
    _append_ledger(paths, "skill_version_rolled_back", {"skill": skill_name, "from": current_version, "to": previous_version})
    return result


def unproject_skill_from_codex(skill_name: str, *, paths: SkillFabricPaths, codex_skills_dir: Path) -> dict[str, Any]:
    target = codex_skills_dir / skill_name
    sidecar = codex_skills_dir / f".{skill_name}.skill-fabric-projection.json"
    removed = []
    if target.is_symlink():
        target.unlink()
        removed.append(str(target))
    elif target.exists() and (target / PROJECTION_MARKER).is_file():
        shutil.rmtree(target)
        removed.append(str(target))
    elif target.exists():
        raise SkillFabricError(f"Refusing to remove unmanaged Codex skill directory: {target}")
    if sidecar.is_file():
        sidecar.unlink()
        removed.append(str(sidecar))
    _append_ledger(paths, "skill_unprojected_from_codex", {"skill": skill_name, "removed": removed})
    return {"skill": skill_name, "removed": removed, "status": "removed" if removed else "not_projected"}


def export_openclaw_projection(paths: SkillFabricPaths) -> dict[str, Any]:
    registry = _read_json(paths.registry_path, _empty_registry())
    projection = _openclaw_projection(registry)
    _write_json(paths.openclaw_projection_path, projection)
    _append_ledger(paths, "openclaw_skill_registry_projected", {"target": str(paths.openclaw_projection_path)})
    return projection


def skill_fabric_status(paths: SkillFabricPaths) -> dict[str, Any]:
    registry = _read_json(paths.registry_path, _empty_registry())
    lock = _read_json(paths.lock_path, _empty_lock())
    active, risk_counts = [], {}
    for name, entry in sorted((registry.get("skills") or {}).items()):
        version_id = entry.get("active_version")
        version = (entry.get("versions") or {}).get(version_id)
        if not isinstance(version, dict):
            continue
        risk = str(version.get("risk_level") or "unknown")
        risk_counts[risk] = risk_counts.get(risk, 0) + 1
        active.append({"name": name, "active_version": version_id, "risk_level": risk, "capabilities": version.get("capabilities", []), "path_exists": Path(str(version.get("path"))).is_dir()})
    return {"registry_version": registry.get("registry_version"), "root": str(paths.root), "skill_count": len(active), "risk_counts": risk_counts, "skills": active, "lock_skill_count": len(lock.get("skills", {}) if isinstance(lock.get("skills"), dict) else {}), "openclaw_projection_exists": paths.openclaw_projection_path.exists()}


def skill_fabric_governance_report(paths: SkillFabricPaths) -> dict[str, Any]:
    status = skill_fabric_status(paths)
    verification = verify_skill_fabric(paths)
    report = {
        "registry_version": REGISTRY_VERSION,
        "status": verification["status"],
        "root": str(paths.root),
        "skill_count": status["skill_count"],
        "risk_counts": status["risk_counts"],
        "verification": verification,
        "boundaries": {
            "writes_hermes_memory": False,
            "writes_openclaw_config": False,
            "network_fetch_enabled": False,
            "github_write_actions_enabled": False,
            "composio_execution_enabled": False,
            "codex_projection_requires_explicit_command": True,
            "codex_projection_refuses_unmanaged_overwrite": True,
            "codex_unprojection_refuses_unmanaged_delete": True,
            "github_import_requires_local_archive": True,
            "github_import_requires_scoped_skill_path": True,
            "github_import_requires_expected_sha256": True,
            "github_import_requires_manual_approval": True,
            "github_archive_import_checks_unsafe_paths": True,
        },
        "artifacts": {
            "registry": str(paths.registry_path),
            "lock": str(paths.lock_path),
            "operation_ledger": str(paths.ledger_path),
            "openclaw_readonly_projection": str(paths.openclaw_projection_path),
        },
    }
    _append_ledger(paths, "skill_fabric_governance_reported", {"status": report["status"], "skill_count": report["skill_count"]})
    return report


def verify_skill_fabric(paths: SkillFabricPaths) -> dict[str, Any]:
    registry = _read_json(paths.registry_path, _empty_registry())
    lock = _read_json(paths.lock_path, _empty_lock())
    verified, failures = [], []
    for name, entry in sorted((registry.get("skills") or {}).items()):
        versions = entry.get("versions") or {}
        if not isinstance(versions, dict):
            failures.append({"skill": name, "version": "", "reason": "registry versions missing"})
            continue
        active_version = str(entry.get("active_version") or "")
        if active_version not in versions:
            failures.append({"skill": name, "version": active_version, "reason": "active version missing"})
        lock_entry = (lock.get("skills") or {}).get(name) if isinstance(lock.get("skills"), dict) else None
        if active_version and not isinstance(lock_entry, dict):
            failures.append({"skill": name, "version": active_version, "reason": "lock entry missing"})
        elif isinstance(lock_entry, dict) and lock_entry.get("active_version") != active_version:
            failures.append({"skill": name, "version": active_version, "reason": "lock active version mismatch"})
        for version_id, version in sorted(versions.items()):
            if not isinstance(version, dict):
                failures.append({"skill": name, "version": version_id, "reason": "registry version invalid"})
                continue
            path = Path(str(version.get("path") or ""))
            if not path.is_dir():
                failures.append({"skill": name, "version": version_id, "reason": "canonical path missing"})
                continue
            digest, _count, _text = _hash_directory(path)
            if digest != version.get("sha256"):
                failures.append({"skill": name, "version": version_id, "reason": "registry hash mismatch"})
            elif version_id == active_version and isinstance(lock_entry, dict) and digest != str(lock_entry.get("sha256") or ""):
                failures.append({"skill": name, "version": version_id, "reason": "lock hash mismatch"})
            else:
                verified.append({"skill": name, "version": version_id, "sha256": digest})
    for name in sorted((lock.get("skills") or {}).keys() if isinstance(lock.get("skills"), dict) else []):
        if name not in (registry.get("skills") or {}):
            failures.append({"skill": name, "version": "", "reason": "lock skill missing from registry"})
    status = "pass" if not failures else "fail"
    _append_ledger(paths, "skill_fabric_verified", {"status": status, "verified_count": len(verified), "failure_count": len(failures)})
    return {"status": status, "verified": verified, "failures": failures}


def _active_skill_path(paths: SkillFabricPaths, skill_name: str) -> tuple[Path, str]:
    registry = _read_json(paths.registry_path, _empty_registry())
    skill = registry.get("skills", {}).get(skill_name)
    if not isinstance(skill, dict):
        raise SkillFabricError(f"Skill is not registered: {skill_name}")
    version_id = str(skill.get("active_version") or "")
    version = skill.get("versions", {}).get(version_id)
    if not isinstance(version, dict):
        raise SkillFabricError(f"Active version is missing for skill: {skill_name}")
    source_path = Path(str(version["path"]))
    if not source_path.is_dir():
        raise SkillFabricError(f"Registered skill path is missing: {source_path}")
    return source_path, version_id


def _extract_github_archive(archive_path: Path, destination: Path) -> Path:
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    with ZipFile(archive_path) as archive:
        members = archive.infolist()
        if not members:
            raise SkillFabricError("GitHub archive is empty.")
        roots = {Path(member.filename).parts[0] for member in members if Path(member.filename).parts}
        if len(roots) != 1:
            raise SkillFabricError("GitHub archive must contain one top-level directory.")
        root = next(iter(roots))
        for member in members:
            member_path = Path(member.filename)
            if member_path.is_absolute() or ".." in member_path.parts:
                raise SkillFabricError("GitHub archive contains an unsafe path.")
        archive.extractall(destination)
    return destination / root


def _find_skill_dirs(root: Path, *, max_depth: int) -> list[Path]:
    skill_dirs: list[Path] = []
    for current, dirs, files in os.walk(root):
        current_path = Path(current)
        rel_parts = current_path.relative_to(root).parts
        if len(rel_parts) > max_depth:
            dirs[:] = []
            continue
        dirs[:] = sorted(d for d in dirs if d not in {".git", "__pycache__", "node_modules", ".venv"})
        if "SKILL.md" in files:
            skill_dirs.append(current_path)
            dirs[:] = []
    return sorted(skill_dirs)


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _remove_managed_projection(target: Path) -> None:
    if target.is_symlink():
        target.unlink()
    elif not target.exists():
        return
    elif (target / PROJECTION_MARKER).is_file():
        shutil.rmtree(target)
    else:
        raise SkillFabricError(f"Refusing to overwrite unmanaged Codex skill directory: {target}")


def _projection_marker(paths: SkillFabricPaths, skill_name: str, version_id: str) -> dict[str, Any]:
    return {"managed_by": "hermes-memory-fabric-plugin.skill_fabric", "fabric_root": str(paths.root), "skill": skill_name, "version": version_id, "projected_at": _now()}


def _empty_registry() -> dict[str, Any]:
    return {"registry_version": REGISTRY_VERSION, "skills": {}, "updated_at": None}


def _empty_lock() -> dict[str, Any]:
    return {"registry_version": REGISTRY_VERSION, "skills": {}, "updated_at": None}


def _openclaw_projection(registry: Mapping[str, Any]) -> dict[str, Any]:
    projected: dict[str, Any] = {"registry_version": REGISTRY_VERSION, "skills": {}, "updated_at": registry.get("updated_at")}
    for name, entry in sorted((registry.get("skills") or {}).items()):
        version_id = entry.get("active_version")
        version = (entry.get("versions") or {}).get(version_id)
        if isinstance(version, dict):
            projected["skills"][name] = {"active_version": version_id, "description": version.get("description"), "capabilities": version.get("capabilities", []), "capability_manifest": version.get("capability_manifest", {}), "risk_level": version.get("risk_level"), "path": version.get("path")}
    return projected


def _read_skill_metadata(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    metadata: dict[str, str] = {}
    for line in text[4:end].strip().splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata, text[end + 4 :]


def _hash_directory(path: Path) -> tuple[str, int, str]:
    digest = hashlib.sha256()
    file_count = 0
    text_parts: list[str] = []
    for file_path in _iter_files(path):
        rel = file_path.relative_to(path).as_posix()
        payload = file_path.read_bytes()
        digest.update(rel.encode("utf-8"))
        digest.update(payload)
        file_count += 1
        if file_path.suffix.lower() in {".md", ".py", ".txt", ".json", ".yaml", ".yml", ".toml", ".sh"}:
            text_parts.append(payload.decode("utf-8", errors="ignore"))
    return digest.hexdigest(), file_count, "\n".join(text_parts)


def _iter_files(path: Path) -> Iterable[Path]:
    for root, dirs, files in os.walk(path):
        dirs[:] = sorted(d for d in dirs if d not in {".git", "__pycache__"})
        for file_name in sorted(files):
            if file_name != ".DS_Store":
                yield Path(root) / file_name


def _scan_risks(text: str) -> list[dict[str, str]]:
    lowered = text.lower()
    checks = {
        "curl_pipe_shell": "curl" in lowered and ("| bash" in lowered or "| sh" in lowered),
        "composio_cli": "composio " in lowered,
        "slack_send": "slack" in lowered and ("send" in lowered or "post" in lowered),
        "github_write": "github" in lowered and any(token in lowered for token in ("create issue", "github_create", "post", "push", "merge", "write")),
        "memory_write": "memory_write_proposal" in lowered or "write memory" in lowered,
        "shell_exec": any(token in lowered for token in ("subprocess", "shell", "bash", "exec_command")),
        "network": any(token in lowered for token in ("http://", "https://", "network", "oauth")),
    }
    return [{"id": fid, "severity": RISK_PATTERNS[fid][0], "message": RISK_PATTERNS[fid][1]} for fid, present in checks.items() if present]


def _capability_manifest(findings: Iterable[Mapping[str, str]], text: str) -> dict[str, Any]:
    declared = _capabilities_from_findings(findings)
    lowered = text.lower()
    reads = {"filesystem_read": any(token in lowered for token in ("read_text", "cat ", "sed -n", "open(")), "github_read": "github" in lowered or "gh pr view" in lowered, "browser_read": "browser" in lowered or "screenshot" in lowered}
    writes = {"filesystem_write": any(token in lowered for token in ("write_text", "apply_patch", "tee ", "copytree")), "github_write": "github_write" in declared, "slack_write": "slack_write" in declared, "memory_proposal": "memory_proposal" in declared, "external_app_actions": "external_app_actions" in declared}
    execution = {"shell": "shell" in declared, "network": "network" in declared, "oauth": "oauth" in lowered}
    return {"declared": sorted(declared), "reads": {k: v for k, v in reads.items() if v}, "writes": {k: v for k, v in writes.items() if v}, "execution": {k: v for k, v in execution.items() if v}, "requires_review": bool(declared)}


def _capabilities_from_findings(findings: Iterable[Mapping[str, str]]) -> set[str]:
    mapping = {"curl_pipe_shell": "network", "composio_cli": "external_app_actions", "slack_send": "slack_write", "github_write": "github_write", "memory_write": "memory_proposal", "shell_exec": "shell", "network": "network"}
    return {mapping[f["id"]] for f in findings if f.get("id") in mapping}


def _risk_level(findings: Iterable[Mapping[str, str]]) -> str:
    severities = {finding.get("severity") for finding in findings}
    return "high" if "high" in severities else "review" if "review" in severities else "low"


def _broad_trigger_reason(description: str) -> str | None:
    text = description.strip().lower()
    if len(text) < 20:
        return "description is too short to route safely"
    for phrase in ("use when the user asks for anything", "use for any task", "always use", "all tasks", "general purpose"):
        if phrase in text:
            return f"contains overly broad trigger phrase: {phrase}"
    if len(_description_tokens(text)) < 5:
        return "description has too few routing tokens"
    return None


def _description_overlap_score(left: str, right: str) -> float:
    left_tokens, right_tokens = _description_tokens(left), _description_tokens(right)
    return 0.0 if not left_tokens or not right_tokens else len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def _description_tokens(text: str) -> set[str]:
    stopwords = {"a", "an", "and", "for", "in", "of", "on", "or", "the", "to", "use", "when", "with", "user", "asks"}
    return {token for token in re.findall(r"[a-z0-9_+-]{3,}", text.lower()) if token not in stopwords}


def _parse_github_skill_spec(spec: str) -> dict[str, str | None]:
    parsed = urlparse(spec)
    if parsed.netloc and parsed.netloc.lower() != "github.com":
        raise SkillFabricError("Only github.com skill import plans are supported.")
    if parsed.netloc:
        parts = [part for part in parsed.path.split("/") if part]
        if len(parts) < 2:
            raise SkillFabricError("GitHub URL must include owner and repo.")
        ref, path = None, None
        if len(parts) >= 5 and parts[2] in {"tree", "blob"}:
            ref, path = parts[3], "/".join(parts[4:])
        return {"owner": parts[0], "repo": parts[1].removesuffix(".git"), "ref": ref, "path": path}
    parts = spec.split("/", 2)
    if len(parts) < 2:
        raise SkillFabricError("GitHub spec must be owner/repo or a github.com URL.")
    return {"owner": parts[0], "repo": parts[1].removesuffix(".git"), "ref": None, "path": parts[2] if len(parts) == 3 else None}


def _looks_like_commit_sha(ref: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-fA-F]{40}", ref))


def _github_plan_next_steps(status: str) -> list[str]:
    if status == "blocked":
        return ["Provide an explicit ref and safe skill path before local archive import."]
    if status == "needs_pin_resolution":
        return ["Resolve the branch or tag to a full commit SHA.", "Provide an existing local archive path.", "Verify the archive sha256 before import."]
    return ["Provide an existing local archive path.", "Verify the archive sha256.", "Run local skill audit before import."]


def _validate_skill_name(name: str) -> None:
    if not name or name in {".", ".."} or "/" in name or "\\" in name:
        raise SkillFabricError("Skill name must be a single non-empty path segment.")


def _read_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    return dict(default) if not path.exists() else json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _append_ledger(paths: SkillFabricPaths, event: str, payload: Mapping[str, Any]) -> None:
    paths.audit_dir.mkdir(parents=True, exist_ok=True)
    with paths.ledger_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"event": event, "created_at": _now(), "payload": dict(payload)}, ensure_ascii=False, sort_keys=True) + "\n")


def _paths_dict(paths: SkillFabricPaths) -> dict[str, str]:
    return {"root": str(paths.root), "registry": str(paths.registry_path), "lock": str(paths.lock_path), "ledger": str(paths.ledger_path), "openclaw_projection": str(paths.openclaw_projection_path)}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
