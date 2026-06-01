#!/usr/bin/env python3
"""Manage the local governed Skill Fabric registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.skill_fabric import (
    SkillFabricError,
    SkillFabricPaths,
    audit_skill_repository,
    audit_skill_directory,
    default_fabric_paths,
    export_openclaw_projection,
    import_github_archive,
    import_skill_directory,
    initialize_skill_fabric,
    lint_skill_triggers,
    activate_skill_version,
    list_skill_versions,
    plan_github_skill_import,
    project_all_skills_to_codex,
    project_skill_to_codex,
    rollback_skill_version,
    skill_fabric_governance_report,
    skill_fabric_status,
    unproject_skill_from_codex,
    verify_skill_fabric,
)


def _paths(args: argparse.Namespace) -> SkillFabricPaths:
    return SkillFabricPaths(Path(args.root).expanduser()) if args.root else default_fabric_paths()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Governed shared Codex/OpenClaw Skill Fabric.")
    parser.add_argument("--root", help="Skill Fabric root; defaults to ~/.openclaw/skill-fabric")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    sub.add_parser("status")
    audit = sub.add_parser("audit")
    audit.add_argument("source_dir")
    audit.add_argument("--name")
    audit_repo = sub.add_parser("audit-repo")
    audit_repo.add_argument("root_dir")
    audit_repo.add_argument("--max-depth", type=int, default=3)
    imp = sub.add_parser("import")
    imp.add_argument("source_dir")
    imp.add_argument("--name")
    imp.add_argument("--approved-by")
    versions = sub.add_parser("versions")
    versions.add_argument("skill_name")
    activate = sub.add_parser("activate")
    activate.add_argument("skill_name")
    activate.add_argument("version")
    rollback = sub.add_parser("rollback")
    rollback.add_argument("skill_name")
    lint = sub.add_parser("lint-triggers")
    lint.add_argument("skill_dirs", nargs="+")
    gh_plan = sub.add_parser("plan-github-import")
    gh_plan.add_argument("url_or_spec")
    gh_plan.add_argument("--ref")
    gh_plan.add_argument("--path")
    gh_archive = sub.add_parser("import-github-archive")
    gh_archive.add_argument("url_or_spec")
    gh_archive.add_argument("--ref", required=True)
    gh_archive.add_argument("--path", required=True)
    gh_archive.add_argument("--archive-path", required=True)
    gh_archive.add_argument("--expected-archive-sha256", required=True)
    gh_archive.add_argument("--approved-by", required=True)
    gh_archive.add_argument("--temp-dir")
    project = sub.add_parser("project-codex")
    project.add_argument("skill_name")
    project.add_argument("--codex-skills-dir", default="~/.codex/skills")
    project.add_argument("--mode", choices=["symlink", "copy"], default="symlink")
    project_all = sub.add_parser("project-codex-all")
    project_all.add_argument("--codex-skills-dir", default="~/.codex/skills")
    project_all.add_argument("--mode", choices=["symlink", "copy"], default="symlink")
    unproject = sub.add_parser("unproject-codex")
    unproject.add_argument("skill_name")
    unproject.add_argument("--codex-skills-dir", default="~/.codex/skills")
    sub.add_parser("project-openclaw")
    sub.add_parser("verify")
    sub.add_parser("governance-report")

    args = parser.parse_args(argv)
    paths = _paths(args)
    try:
        if args.command == "init":
            result = initialize_skill_fabric(paths)
        elif args.command == "status":
            result = skill_fabric_status(paths)
        elif args.command == "audit":
            result = audit_skill_directory(Path(args.source_dir), name=args.name).to_dict()
        elif args.command == "audit-repo":
            result = audit_skill_repository(Path(args.root_dir), max_depth=args.max_depth)
        elif args.command == "import":
            result = import_skill_directory(Path(args.source_dir), paths=paths, name=args.name, approved_by=args.approved_by)
        elif args.command == "versions":
            result = list_skill_versions(paths, args.skill_name)
        elif args.command == "activate":
            result = activate_skill_version(paths, args.skill_name, args.version)
        elif args.command == "rollback":
            result = rollback_skill_version(paths, args.skill_name)
        elif args.command == "lint-triggers":
            result = lint_skill_triggers(Path(skill_dir) for skill_dir in args.skill_dirs)
        elif args.command == "plan-github-import":
            result = plan_github_skill_import(args.url_or_spec, ref=args.ref, path=args.path)
        elif args.command == "import-github-archive":
            result = import_github_archive(
                args.url_or_spec,
                paths=paths,
                ref=args.ref,
                path=args.path,
                archive_path=Path(args.archive_path).expanduser() if args.archive_path else None,
                expected_archive_sha256=args.expected_archive_sha256,
                approved_by=args.approved_by,
                temp_dir=Path(args.temp_dir).expanduser() if args.temp_dir else None,
            )
        elif args.command == "project-codex":
            result = project_skill_to_codex(args.skill_name, paths=paths, codex_skills_dir=Path(args.codex_skills_dir).expanduser(), mode=args.mode)
        elif args.command == "project-codex-all":
            result = project_all_skills_to_codex(paths=paths, codex_skills_dir=Path(args.codex_skills_dir).expanduser(), mode=args.mode)
        elif args.command == "unproject-codex":
            result = unproject_skill_from_codex(args.skill_name, paths=paths, codex_skills_dir=Path(args.codex_skills_dir).expanduser())
        elif args.command == "project-openclaw":
            result = export_openclaw_projection(paths)
        elif args.command == "verify":
            result = verify_skill_fabric(paths)
        elif args.command == "governance-report":
            result = skill_fabric_governance_report(paths)
        else:
            parser.error("unknown command")
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except SkillFabricError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
