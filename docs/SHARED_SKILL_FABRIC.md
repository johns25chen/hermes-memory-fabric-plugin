# Shared Skill Fabric

The Skill Fabric stores one canonical copy of approved Codex skills and projects
thin runtime views into Codex and OpenClaw. Hermes remains the memory owner and
governance surface; this module writes local Skill Fabric registry, lock,
projection, and operation ledger files only. These files are local Skill Fabric
state, not Hermes memory.

## v2.3.0 Release Integrity Audit Note

v2.3.0 adds `run_release_integrity_audit(repo_root)` as a deterministic local
proof that the v2.0.0, v2.1.0, and v2.2.0 release-chain boundaries still hold in
the installed source tree. It checks local package metadata, local tag metadata,
expected files, provider tools, the authority contract dry run, temporary-root
Skill Fabric verification, the local archive simulation, and unsafe source
surfaces.

The audit does not fetch from remote services, call remote APIs, publish
releases, write Hermes memory, modify Hermes Agent state, execute external app
actions, or expose provider tools. Documentation-only historical references are
reported separately from source-code safety hits.

## v2.2.0 Local GitHub Archive Simulation

v2.2.0 adds a deterministic end-to-end simulation for the Shared Skill Fabric
GitHub archive flow. The simulation creates a fake GitHub-style zip archive in
a temporary local directory, places one valid `SKILL.md` under a scoped path
such as `skills/demo-skill/SKILL.md`, computes the archive SHA-256, plans the
GitHub import, imports only from that local archive, projects the imported skill
to a temporary Codex skills directory, verifies the managed projection marker,
unprojects it, confirms unmanaged Codex paths were left untouched, and runs
`verify`.

This remains a local proof only:

- No network fetch is performed.
- No GitHub API or write action is performed.
- No Composio execution is performed.
- No Hermes memory is written.
- No Hermes Agent files or configuration are modified.
- No provider tools are exposed.
- All files are created under temporary local directories chosen by the
  simulation caller.

Run the smoke simulation:

```bash
PYTHONPATH="$PWD/src:$PWD" python3 scripts/smoke_skill_fabric_simulation.py
```

Expected output:

```text
skill_fabric_github_archive_simulation=passed
```

Programmatic callers can use
`run_skill_fabric_github_archive_simulation(temp_root)` and serialize the report
with `skill_fabric_simulation_to_json(result)`.

## v2.1.0 Safety Boundary

v2.1.0 is strict local-only Shared Skill Fabric Governance:

- Local registry only: `registry.json` under the explicit `--root` or default
  Skill Fabric root.
- Local operation ledger only: `audit/skill_operation_ledger.jsonl` under the
  same Skill Fabric root.
- No network fetch behavior.
- No GitHub write actions.
- No Composio execution.
- No Hermes memory write.
- No Hermes Agent modification.
- No provider tool exposure.
- No Codex projection unless explicitly invoked with `project-codex` or
  `project-codex-all`.
- Codex projection creates only a symlink or copy under the explicit Codex
  skills directory and always writes a managed projection marker. Unprojection
  refuses unmanaged paths.

## Layout

```text
~/.openclaw/skill-fabric/
  registry.json
  skills/<skill-name>/<sha-prefix>/
  locks/skills.lock.json
  audit/skill_operation_ledger.jsonl
  openclaw/registry.json
```

## Commands

```bash
python3 scripts/skill_fabric.py init
python3 scripts/skill_fabric.py status
python3 scripts/skill_fabric.py audit ./path/to/skill
python3 scripts/skill_fabric.py audit-repo ./path/to/extracted-repo
python3 scripts/skill_fabric.py lint-triggers ./path/to/a ./path/to/b
python3 scripts/skill_fabric.py import ./path/to/skill --approved-by manual-review
python3 scripts/skill_fabric.py versions <skill-name>
python3 scripts/skill_fabric.py activate <skill-name> <version>
python3 scripts/skill_fabric.py rollback <skill-name>
python3 scripts/skill_fabric.py project-codex <skill-name>
python3 scripts/skill_fabric.py project-codex-all
python3 scripts/skill_fabric.py unproject-codex <skill-name>
python3 scripts/skill_fabric.py project-openclaw
python3 scripts/skill_fabric.py verify
python3 scripts/skill_fabric.py governance-report
```

Plan a GitHub import without network or writes:

```bash
python3 scripts/skill_fabric.py plan-github-import \
  ComposioHQ/awesome-codex-skills/gh-fix-ci \
  --ref 0123456789abcdef0123456789abcdef01234567
```

Import from an already-present local GitHub archive:

```bash
python3 scripts/skill_fabric.py import-github-archive \
  ComposioHQ/awesome-codex-skills/gh-fix-ci \
  --ref <40-char-commit-sha> \
  --path gh-fix-ci \
  --archive-path /path/to/archive.zip \
  --expected-archive-sha256 <archive-sha256> \
  --approved-by manual-review
```

`plan-github-import` is a deterministic planning helper only. It never fetches
or writes. `import-github-archive` accepts only a local archive path already
present on disk and requires explicit owner/repo/path/ref metadata, an expected
archive SHA-256 digest, and `--approved-by` manual approval. The archive is
checked for unsafe zip paths, audited locally, and then imported into the
canonical local Skill Fabric store.

## Governance Rules

- Codex is the runtime. OpenClaw reads `openclaw/registry.json` for routing.
- Hermes memory and OpenClaw config are not modified by these commands.
- GitHub import planning is dry-run only. Archive import is local-only and
  requires commit metadata, scoped paths, expected SHA-256, and manual approval.
- `audit-repo` recursively finds local `SKILL.md` directories, summarizes risk,
  runs trigger lint, and separates low-risk import candidates from
  review-required skills.
- `verify` recomputes hashes and fails on registry or lock mismatch.
- `activate` refuses to switch to a version whose stored files no longer match
  the registry hash.
- `rollback` switches back to the last recorded active version and still uses
  the same hash verification path as activation.
- `governance-report` emits integrity status, artifact paths, and explicit
  no-write boundaries for Hermes memory and OpenClaw config.
- `unproject-codex` removes only managed symlinks or managed copy projections;
  it refuses to delete unmanaged Codex skills directories.
- Codex projection refuses to overwrite unmanaged skill directories.
- Audits produce a structured `capability_manifest` with read, write, and
  execution surfaces.
