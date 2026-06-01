import json
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import socket
from zipfile import ZipFile

import pytest

from hermes_memory_fabric.skill_fabric import (
    PROJECTION_MARKER,
    SkillFabricError,
    SkillFabricPaths,
    audit_skill_repository,
    audit_skill_directory,
    activate_skill_version,
    import_github_archive,
    import_skill_directory,
    list_skill_versions,
    lint_skill_triggers,
    plan_github_skill_import,
    project_all_skills_to_codex,
    project_skill_to_codex,
    rollback_skill_version,
    skill_fabric_governance_report,
    skill_fabric_status,
    unproject_skill_from_codex,
    verify_skill_fabric,
)


def _paths(tmp_path: Path) -> SkillFabricPaths:
    return SkillFabricPaths(tmp_path / "skill-fabric")


def _skill(tmp_path: Path, name: str = "example-skill", body: str = "Use local files only.") -> Path:
    skill_dir = tmp_path / name
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        f"""---
name: {name}
description: Test skill for shared fabric routing.
---

# Test Skill

{body}
""",
        encoding="utf-8",
    )
    return skill_dir


def _github_archive(tmp_path: Path, root: str = "repo-commit", skill_path: str = "skills/demo") -> Path:
    archive = tmp_path / "repo.zip"
    with ZipFile(archive, "w") as zip_file:
        zip_file.writestr(
            f"{root}/{skill_path}/SKILL.md",
            """---
name: demo
description: Demo skill from a pinned GitHub archive.
---

# Demo
""",
        )
    return archive


def test_audit_skill_directory_extracts_manifest_and_risk(tmp_path):
    risky_action = "composio" + " execute GITHUB_CREATE_ISSUE"
    audit = audit_skill_directory(_skill(tmp_path, body=f"Run `{risky_action}` only after review."))

    assert audit.name == "example-skill"
    assert audit.risk_level == "review"
    assert "external_app_actions" in audit.capabilities
    assert "github_write" in audit.capabilities
    assert audit.capability_manifest["writes"]["github_write"] is True


def test_import_status_verify_and_projection_flow(tmp_path):
    paths = _paths(tmp_path)
    imported = import_skill_directory(_skill(tmp_path), paths=paths, approved_by="human")

    status = skill_fabric_status(paths)
    assert status["skill_count"] == 1
    assert status["risk_counts"] == {"low": 1}
    assert verify_skill_fabric(paths)["status"] == "pass"

    codex_dir = tmp_path / "codex-skills"
    projected = project_skill_to_codex("example-skill", paths=paths, codex_skills_dir=codex_dir, mode="copy")
    assert Path(projected["target"], "SKILL.md").exists()
    marker = json.loads((Path(projected["target"]) / PROJECTION_MARKER).read_text(encoding="utf-8"))
    assert marker["version"] == imported["version"]


def test_project_refuses_unmanaged_codex_directory(tmp_path):
    paths = _paths(tmp_path)
    import_skill_directory(_skill(tmp_path), paths=paths)
    unmanaged = tmp_path / "codex-skills" / "example-skill"
    unmanaged.mkdir(parents=True)
    (unmanaged / "SKILL.md").write_text("unmanaged", encoding="utf-8")

    with pytest.raises(SkillFabricError, match="unmanaged"):
        project_skill_to_codex("example-skill", paths=paths, codex_skills_dir=tmp_path / "codex-skills", mode="copy")


def test_verify_detects_tampering(tmp_path):
    paths = _paths(tmp_path)
    imported = import_skill_directory(_skill(tmp_path), paths=paths)
    stored = Path(imported["path"]) / "SKILL.md"
    stored.write_text(stored.read_text(encoding="utf-8") + "\nTampered.\n", encoding="utf-8")

    result = verify_skill_fabric(paths)

    assert result["status"] == "fail"
    assert result["failures"][0]["reason"] == "registry hash mismatch"


def test_lint_skill_triggers_flags_duplicate_and_broad(tmp_path):
    first = _skill(tmp_path, "first")
    second = _skill(tmp_path, "second")
    (second / "SKILL.md").write_text(
        """---
name: first
description: Use for any task.
---
# Broad
""",
        encoding="utf-8",
    )

    result = lint_skill_triggers([first, second])

    assert result["status"] == "review"
    assert result["broad_triggers"]
    assert result["overlaps"][0]["type"] == "duplicate_name"


def test_plan_github_skill_import_requires_ref_and_path():
    result = plan_github_skill_import("https://github.com/ComposioHQ/awesome-codex-skills")

    assert result["status"] == "blocked"
    assert {finding["id"] for finding in result["findings"]} == {"missing_ref", "missing_skill_path"}


def test_plan_github_skill_import_ready_only_for_commit_sha():
    ready = plan_github_skill_import("ComposioHQ/awesome-codex-skills/gh-fix-ci", ref="0123456789abcdef0123456789abcdef01234567")
    needs_pin = plan_github_skill_import("https://github.com/ComposioHQ/awesome-codex-skills/tree/main/skill-installer")

    assert ready["status"] == "ready_for_local_archive_import"
    assert ready["would_fetch"] is False
    assert needs_pin["status"] == "needs_pin_resolution"


def test_plan_github_skill_import_does_not_perform_network(monkeypatch):
    def fail_network(*_args, **_kwargs):
        raise AssertionError("network should not be used by planning")

    monkeypatch.setattr(socket, "create_connection", fail_network)

    result = plan_github_skill_import(
        "ComposioHQ/awesome-codex-skills/gh-fix-ci",
        ref="0123456789abcdef0123456789abcdef01234567",
    )

    assert result["status"] == "ready_for_local_archive_import"
    assert result["would_fetch"] is False


def test_fetch_github_import_cli_command_is_absent(tmp_path):
    completed = _run_cli(["--root", str(tmp_path / "fabric"), "fetch-github-import"], tmp_path)

    assert completed.returncode != 0
    assert "invalid choice" in completed.stderr


def test_source_code_does_not_import_network_clients():
    root = Path(__file__).resolve().parents[1]
    for relative in ("src/hermes_memory_fabric/skill_fabric.py", "scripts/skill_fabric.py"):
        text = (root / relative).read_text(encoding="utf-8")
        assert "url" + "open" not in text
        assert "urllib" + ".request" not in text
        assert "import " + "requ" + "ests" not in text
        assert "from " + "requ" + "ests" not in text


def test_import_github_archive_requires_explicit_archive_metadata_and_approval(tmp_path):
    archive = _github_archive(tmp_path)
    archive_sha256 = hashlib.sha256(archive.read_bytes()).hexdigest()

    with pytest.raises(TypeError):
        import_github_archive(
            "ComposioHQ/awesome-codex-skills/skills/demo",
            paths=_paths(tmp_path),
            ref="0123456789abcdef0123456789abcdef01234567",
            path="skills/demo",
        )

    with pytest.raises(SkillFabricError, match="sha256"):
        import_github_archive(
            "ComposioHQ/awesome-codex-skills/skills/demo",
            paths=_paths(tmp_path),
            ref="0123456789abcdef0123456789abcdef01234567",
            path="skills/demo",
            archive_path=archive,
            expected_archive_sha256="",
            approved_by="test",
        )

    with pytest.raises(SkillFabricError, match="approval"):
        import_github_archive(
            "ComposioHQ/awesome-codex-skills/skills/demo",
            paths=_paths(tmp_path),
            ref="0123456789abcdef0123456789abcdef01234567",
            path="skills/demo",
            archive_path=archive,
            expected_archive_sha256=archive_sha256,
            approved_by="",
        )


def test_import_github_archive_from_local_archive(tmp_path):
    paths = _paths(tmp_path)
    archive = _github_archive(tmp_path)
    archive_sha256 = hashlib.sha256(archive.read_bytes()).hexdigest()

    result = import_github_archive(
        "ComposioHQ/awesome-codex-skills/skills/demo",
        paths=paths,
        ref="0123456789abcdef0123456789abcdef01234567",
        path="skills/demo",
        archive_path=archive,
        expected_archive_sha256=archive_sha256,
        temp_dir=tmp_path / "work",
        approved_by="test",
    )

    assert result["status"] == "imported"
    assert result["archive_sha256"] == archive_sha256
    assert result["imported"]["skill"] == "demo"
    assert verify_skill_fabric(paths)["status"] == "pass"


def test_import_github_archive_uses_existing_local_archive_only(tmp_path):
    with pytest.raises(SkillFabricError, match="does not exist"):
        import_github_archive(
            "ComposioHQ/awesome-codex-skills/skills/demo",
            paths=_paths(tmp_path),
            ref="0123456789abcdef0123456789abcdef01234567",
            path="skills/demo",
            archive_path=tmp_path / "missing.zip",
            expected_archive_sha256="0" * 64,
            approved_by="test",
        )


def test_import_github_archive_rejects_archive_hash_mismatch(tmp_path):
    archive = _github_archive(tmp_path)

    with pytest.raises(SkillFabricError, match="sha256"):
        import_github_archive(
            "ComposioHQ/awesome-codex-skills/skills/demo",
            paths=_paths(tmp_path),
            ref="0123456789abcdef0123456789abcdef01234567",
            path="skills/demo",
            archive_path=archive,
            expected_archive_sha256="0" * 64,
            temp_dir=tmp_path / "work",
            approved_by="test",
        )


def test_import_github_archive_rejects_unsafe_archive_path(tmp_path):
    archive = tmp_path / "bad.zip"
    with ZipFile(archive, "w") as zip_file:
        zip_file.writestr("../escape/SKILL.md", "bad")
    archive_sha256 = hashlib.sha256(archive.read_bytes()).hexdigest()

    with pytest.raises(SkillFabricError, match="unsafe path|top-level"):
        import_github_archive(
            "ComposioHQ/awesome-codex-skills/escape",
            paths=_paths(tmp_path),
            ref="0123456789abcdef0123456789abcdef01234567",
            path="escape",
            archive_path=archive,
            expected_archive_sha256=archive_sha256,
            temp_dir=tmp_path / "work",
            approved_by="test",
        )


def test_project_all_skills_to_codex(tmp_path):
    paths = _paths(tmp_path)
    import_skill_directory(_skill(tmp_path, "alpha"), paths=paths)
    import_skill_directory(_skill(tmp_path, "beta"), paths=paths)

    result = project_all_skills_to_codex(paths=paths, codex_skills_dir=tmp_path / "codex", mode="copy")

    assert result["status"] == "pass"
    assert len(result["projected"]) == 2


def test_audit_skill_repository_reports_candidates_and_review_required(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    low_parent = repo / "low"
    low_parent.mkdir()
    _skill(low_parent, "low-skill")
    risky_parent = repo / "risky"
    risky_parent.mkdir()
    risky_action = "composio" + " execute GITHUB_CREATE_ISSUE"
    _skill(risky_parent, "risky-skill", body=f"Use {risky_action}.")

    result = audit_skill_repository(repo)

    assert result["status"] == "review"
    assert result["skill_count"] == 2
    assert result["risk_counts"] == {"low": 1, "review": 1}
    assert result["import_candidates"][0]["name"] == "low-skill"
    assert result["review_required"][0]["name"] == "risky-skill"
    risky = result["skills"][1]
    assert "external_app_actions" in risky["capabilities"]
    assert "github_write" in risky["capabilities"]
    assert risky["capability_manifest"]["writes"]["external_app_actions"] is True
    assert risky["capability_manifest"]["writes"]["github_write"] is True


def test_list_and_activate_skill_versions(tmp_path):
    paths = _paths(tmp_path)
    first_dir = _skill(tmp_path, "versioned", body="First body.")
    first = import_skill_directory(first_dir, paths=paths)
    second_dir = tmp_path / "versioned-second"
    second_dir.mkdir()
    (second_dir / "SKILL.md").write_text(
        """---
name: versioned
description: Test skill for shared fabric routing.
---

Second body.
""",
        encoding="utf-8",
    )
    second = import_skill_directory(second_dir, paths=paths)

    versions = list_skill_versions(paths, "versioned")
    assert versions["active_version"] == second["version"]
    assert {entry["version"] for entry in versions["versions"]} == {first["version"], second["version"]}

    activated = activate_skill_version(paths, "versioned", first["version"])
    assert activated["active_version"] == first["version"]
    assert list_skill_versions(paths, "versioned")["active_version"] == first["version"]

    rolled_back = rollback_skill_version(paths, "versioned")
    assert rolled_back["status"] == "rolled_back"
    assert rolled_back["active_version"] == second["version"]
    assert rolled_back["rolled_back_from"] == first["version"]


def test_activate_refuses_tampered_version(tmp_path):
    paths = _paths(tmp_path)
    imported = import_skill_directory(_skill(tmp_path, "tamper"), paths=paths)
    stored = Path(imported["path"]) / "SKILL.md"
    stored.write_text(stored.read_text(encoding="utf-8") + "\nchanged\n", encoding="utf-8")

    with pytest.raises(SkillFabricError, match="mismatched"):
        activate_skill_version(paths, "tamper", imported["version"])


def test_unproject_skill_from_codex_removes_managed_copy_and_symlink(tmp_path):
    paths = _paths(tmp_path)
    import_skill_directory(_skill(tmp_path), paths=paths)
    codex_dir = tmp_path / "codex"

    project_skill_to_codex("example-skill", paths=paths, codex_skills_dir=codex_dir, mode="copy")
    copy_result = unproject_skill_from_codex("example-skill", paths=paths, codex_skills_dir=codex_dir)
    assert copy_result["status"] == "removed"
    assert not (codex_dir / "example-skill").exists()

    project_skill_to_codex("example-skill", paths=paths, codex_skills_dir=codex_dir, mode="symlink")
    symlink_result = unproject_skill_from_codex("example-skill", paths=paths, codex_skills_dir=codex_dir)
    assert symlink_result["status"] == "removed"
    assert not (codex_dir / "example-skill").exists()
    assert not (codex_dir / ".example-skill.skill-fabric-projection.json").exists()


def test_unproject_refuses_unmanaged_directory(tmp_path):
    paths = _paths(tmp_path)
    target = tmp_path / "codex" / "manual"
    target.mkdir(parents=True)
    (target / "SKILL.md").write_text("manual", encoding="utf-8")

    with pytest.raises(SkillFabricError, match="unmanaged"):
        unproject_skill_from_codex("manual", paths=paths, codex_skills_dir=tmp_path / "codex")


def test_cli_init_status_and_verify_work_in_temp_root(tmp_path):
    root = tmp_path / "fabric"

    init = _run_cli(["--root", str(root), "init"], tmp_path)
    status = _run_cli(["--root", str(root), "status"], tmp_path)
    verify = _run_cli(["--root", str(root), "verify"], tmp_path)

    assert init.returncode == 0
    assert status.returncode == 0
    assert verify.returncode == 0
    assert json.loads(status.stdout)["root"] == str(root)
    assert json.loads(verify.stdout)["status"] == "pass"


def test_project_codex_writes_only_managed_projection_marker(tmp_path):
    paths = _paths(tmp_path)
    import_skill_directory(_skill(tmp_path), paths=paths)
    codex_dir = tmp_path / "codex"

    projected = project_skill_to_codex("example-skill", paths=paths, codex_skills_dir=codex_dir, mode="symlink")
    target = Path(projected["target"])
    marker_path = codex_dir / ".example-skill.skill-fabric-projection.json"
    marker = json.loads(marker_path.read_text(encoding="utf-8"))

    assert target.is_symlink()
    assert marker["managed_by"] == "hermes-memory-fabric-plugin.skill_fabric"
    assert marker["skill"] == "example-skill"
    assert sorted(path.name for path in codex_dir.iterdir()) == [".example-skill.skill-fabric-projection.json", "example-skill"]


def test_governance_report_and_cli(tmp_path):
    paths = _paths(tmp_path)
    import_skill_directory(_skill(tmp_path), paths=paths)

    report = skill_fabric_governance_report(paths)
    completed = _run_cli(["--root", str(paths.root), "governance-report"], tmp_path)

    assert report["status"] == "pass"
    assert report["boundaries"]["writes_hermes_memory"] is False
    assert report["boundaries"]["writes_openclaw_config"] is False
    assert report["boundaries"]["codex_projection_refuses_unmanaged_overwrite"] is True
    assert completed.returncode == 0
    assert json.loads(completed.stdout)["status"] == "pass"


def _run_cli(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = f"{Path(__file__).resolve().parents[1] / 'src'}:{Path(__file__).resolve().parents[1]}"
    return subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parents[1] / "scripts" / "skill_fabric.py"), *args],
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
