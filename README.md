# Hermes Memory Fabric Plugin

This repository is the standalone plugin extraction of the in-tree Hermes Memory Fabric prototype. The original prototype lived inside `hermes-agent`; this package is laid out so the memory provider and evidence-repair modules do not depend on being imported from the Hermes main repository.

## Install

Editable install from this directory:

```bash
cd /Users/han/hermes-memory-fabric-plugin
python3 -m pip install -e .
```

With `uv`:

```bash
cd /Users/han/hermes-memory-fabric-plugin
uv pip install -e .
```

## Hermes Integration

Hermes memory provider runtime loads providers through its directory-based
`plugins.memory` loader. Install the v0.8.0 shim after installing this package:

```bash
python scripts/install_memory_fabric_shim.py
```

Then run the no-model smoke:

```bash
PYTHON=/Users/han/.hermes/hermes-agent/.venv/bin/python bash scripts/smoke_memory_fabric_hermes.sh
```

See [docs/HERMES_INTEGRATION.md](docs/HERMES_INTEGRATION.md) for the loader
details, optional real chat smoke, and rollback instructions.

## Shared Skill Fabric

This repository includes a governed Skill Fabric for storing one canonical copy
of approved Codex skills and projecting them into Codex/OpenClaw without
duplicating installs. It writes registry, lock, projection, and audit files only;
it does not write Hermes memory or modify OpenClaw config.

### v2.2.0 Skill Fabric Real-World Import Simulation

v2.2.0 adds a deterministic local simulation for the GitHub archive import path.
It creates a fake GitHub-style skill archive under a temporary directory,
computes the archive SHA-256, runs the no-network import plan, imports from the
local archive only, projects the skill to a temporary Codex skills directory,
checks the managed projection marker, unprojects it, confirms unmanaged paths
were not touched, and runs Skill Fabric verification.

The simulation is not real GitHub import, network fetch, Composio execution,
Hermes memory write, Hermes Agent modification, or provider tool exposure. It
uses temporary local directories only.

```bash
PYTHONPATH="$PWD/src:$PWD" python3 scripts/smoke_skill_fabric_simulation.py
```

Expected output:

```text
skill_fabric_github_archive_simulation=passed
```

### v2.1.0 Shared Skill Fabric Governance

v2.1.0 hardens the Shared Skill Fabric to strict local-only boundaries. GitHub
planning remains available as a deterministic no-network helper, but active
network fetching is disabled. GitHub archive import accepts only an explicit
local archive already present on disk, with owner/repo/path/ref metadata,
expected SHA-256, and manual approval. Registry and ledger writes are local
Skill Fabric state under explicit `--root` or the default OpenClaw Skill Fabric
root; they are not Hermes memory.

The v2.1.0 boundary excludes network fetch, GitHub write actions, Composio
execution, Hermes memory writes, Hermes Agent modification, provider tool
exposure, and implicit Codex projection. Codex projection must be explicitly
invoked and writes only a managed symlink/copy plus projection marker under the
chosen Codex skills directory.

```bash
python3 scripts/skill_fabric.py init
python3 scripts/skill_fabric.py status
python3 scripts/skill_fabric.py audit ./path/to/skill
python3 scripts/skill_fabric.py audit-repo ./path/to/extracted-repo
python3 scripts/skill_fabric.py lint-triggers ./path/to/skill ./path/to/other-skill
python3 scripts/skill_fabric.py import ./path/to/skill --approved-by manual-review
python3 scripts/skill_fabric.py versions <skill-name>
python3 scripts/skill_fabric.py activate <skill-name> <version>
python3 scripts/skill_fabric.py rollback <skill-name>
python3 scripts/skill_fabric.py plan-github-import <owner>/<repo>/<path> --ref <ref>
python3 scripts/skill_fabric.py import-github-archive <owner>/<repo>/<path> --ref <ref> --path <path> --archive-path <archive.zip> --expected-archive-sha256 <sha256> --approved-by <reviewer>
python3 scripts/skill_fabric.py project-codex <skill-name>
python3 scripts/skill_fabric.py unproject-codex <skill-name>
python3 scripts/skill_fabric.py verify
python3 scripts/skill_fabric.py governance-report
```

See [docs/SHARED_SKILL_FABRIC.md](docs/SHARED_SKILL_FABRIC.md) for the
Codex/OpenClaw/Hermes boundary and gated GitHub import flow.

## v2.0.0 Token Authority Boundary Contract Dry Run

v2.0.0 adds a deterministic authority boundary contract dry-run layer on top of
the v1.9.0 approval token issuance dry run. It converts a safe v1.9 token
issuance draft candidate into a declarative boundary contract candidate with a
stable `authority_contract_id`.

Run it with stdout JSON:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/build_token_authority_boundary_contract_dry_run.py \
  --input /tmp/approval-token-issuance-dry-run.json
```

Or write the report to one explicit non-Hermes path:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/build_token_authority_boundary_contract_dry_run.py \
  --input /tmp/approval-token-issuance-dry-run.json \
  --scope memory_proposal_apply_preview_only \
  --expiry-seconds 900 \
  --output /tmp/token-authority-boundary-contract-dry-run.json \
  --print-summary
```

The dry run defines future scope, expiry, revocation, audit, ledger, and
executor boundaries only. It does not issue approval tokens, create token
values, write token files, create proposals, append operation ledger files,
write memory/graph/config/SQLite state, write approval audit files, invoke
executors, apply proposals, expose provider tools, call models, or use the
network.

See
[docs/TOKEN_AUTHORITY_BOUNDARY_CONTRACT_DRY_RUN.md](docs/TOKEN_AUTHORITY_BOUNDARY_CONTRACT_DRY_RUN.md)
for status behavior, why `ready` is still not token issuance, and the no-write
boundary.

## v1.9.0 Approval Token Issuance Dry Run

v1.9.0 adds a deterministic token issuance dry-run layer on top of the v1.8.0
approval-intent review outcome. It converts an approved v1.8 review outcome
candidate into a token issuance draft candidate with stable `token_draft_id`
and `token_intent_id` values.

Run it with stdout JSON:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/issue_approval_token_dry_run.py \
  --input /tmp/approval-intent-review-outcome-dry-run.json
```

Or write the report to one explicit non-Hermes path:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/issue_approval_token_dry_run.py \
  --input /tmp/approval-intent-review-outcome-dry-run.json \
  --issuer manual-human-review \
  --reason "reviewed for token issuance draft" \
  --output /tmp/approval-token-issuance-dry-run.json \
  --print-summary
```

The dry run does not issue approval tokens, create usable token values, write
token files, create proposals, append operation ledger files, write
memory/graph/config/SQLite state, write approval audit files, invoke executors,
apply proposals, expose provider tools, call models, or use the network.

See
[docs/APPROVAL_TOKEN_ISSUANCE_DRY_RUN.md](docs/APPROVAL_TOKEN_ISSUANCE_DRY_RUN.md)
for status behavior, why `ready` is still not token issuance, and the no-write
boundary.

## v1.8.0 Approval Intent Review Gate Dry Run

v1.8.0 adds a deterministic review-gate dry-run layer on top of the v1.7.0
approval intent. It converts a ready v1.7 intent plus an explicit reviewer
decision (`approve`, `request_changes`, or `reject`) into a review outcome
candidate with a stable `review_outcome_id` and a required next step.

Run it with stdout JSON:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/review_approval_intent_dry_run.py \
  --input /tmp/approval-intent-dry-run.json \
  --decision approve
```

Or write the report to one explicit non-Hermes path:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/review_approval_intent_dry_run.py \
  --input /tmp/approval-intent-dry-run.json \
  --decision request_changes \
  --reason "needs narrower scope" \
  --output /tmp/approval-intent-review-outcome-dry-run.json \
  --print-summary
```

The dry run does not issue approval tokens, create real proposals, write
proposal files, append operation ledger files, write memory/graph/config/SQLite
state, write token files or approval audit files, invoke executors, apply
proposals, expose provider tools, call models, or use the network.

See
[docs/APPROVAL_INTENT_REVIEW_GATE_DRY_RUN.md](docs/APPROVAL_INTENT_REVIEW_GATE_DRY_RUN.md)
for status behavior, why `approved` is still not token issuance, and the
no-write boundary.

## v1.7.0 Approval Intent Dry Run

v1.7.0 adds a deterministic approval-intent dry-run layer on top of the v1.5.0
proposal preview. It creates an in-memory intent candidate for later human
review only, with a stable `approval_intent_id`, source preview counts, explicit
no-write flags, and a compact v1.6.0 Executor Surface Lockdown Audit snapshot.

Run it with stdout JSON:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/create_approval_intent_dry_run.py \
  --input /tmp/memory-candidate-proposal-dry-run.json
```

Or write the report to one explicit non-Hermes path:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/create_approval_intent_dry_run.py \
  --input /tmp/memory-candidate-proposal-dry-run.json \
  --output /tmp/approval-intent-dry-run.json \
  --print-summary
```

The dry run does not issue approval tokens, create real proposals, write
proposal files, append operation ledger files, write memory/graph/config/SQLite
state, write token files or approval audit files, invoke executors, apply
proposals, expose provider tools, call models, or use the network.

See
[docs/APPROVAL_INTENT_DRY_RUN.md](docs/APPROVAL_INTENT_DRY_RUN.md)
for status behavior, the v1.6 audit gate, and the safety boundary.

## v1.6.0 Executor Surface Lockdown Audit

v1.6.0 adds a read-only static audit for approval, token, executor, write-lock,
ledger, and tool-wrapper surfaces. It verifies that real-write-executor planning
and review modules keep explicit no-write flags, that the forbidden real executor
module/test names are absent, that dry-run paths do not call
`memory_fabric_bridge.create_memory_write_proposal`, and that
`MemoryFabricProvider` still exposes no provider tools.

Run the audit with stdout JSON:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/audit_executor_surface_lockdown.py
```

Or write the report to one explicit non-Hermes path:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/audit_executor_surface_lockdown.py \
  --output /tmp/executor-surface-lockdown-audit.json \
  --print-summary
```

The audit does not implement approval intent, issue approval tokens, call a real
write executor, create proposal files, append operation ledger files, write
memory/graph/config/SQLite state, or expose provider tools.

See
[docs/EXECUTOR_SURFACE_LOCKDOWN_AUDIT.md](docs/EXECUTOR_SURFACE_LOCKDOWN_AUDIT.md)
for the audited surfaces, forbidden write APIs, required no-write flags, and
the relationship to the v1.5 proposal dry-run preview.

## v1.5.0 Memory Candidate Proposal Dry Run

v1.5.0 adds a safe isolated dry-run adapter that converts v1.3.1 Memory Fabric
candidate JSONL rows into existing Memory Block and proposal preview chain
objects. It accepts low-risk, read-only, proposal-governed dry-run candidates by
default, maps them to `project_context` Memory Block candidates, and reuses only
in-memory preview modules through `memory_real_proposal_dry_run`.

Run it with stdout output:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/propose_memory_candidates_dry_run.py \
  --input /tmp/codex-task-summary-candidates.jsonl
```

Or write the preview result to one explicit path:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/propose_memory_candidates_dry_run.py \
  --input /tmp/codex-task-summary-candidates.jsonl \
  --output /tmp/memory-candidate-proposal-dry-run.json \
  --print-summary
```

The adapter does not call `memory_fabric_bridge.create_memory_write_proposal`,
human approval token modules, real write executor modules, provider tools,
network calls, or model calls. It does not write proposal files, operation
ledger files, memory, graph state, token files, approval audit files, config, or
SQLite state.

See
[docs/MEMORY_CANDIDATE_PROPOSAL_DRY_RUN.md](docs/MEMORY_CANDIDATE_PROPOSAL_DRY_RUN.md)
for the schema mapping, reused modules, and safety boundary.

## v1.3.1 Codex Task Summary Ingestion Dry Run

v1.3.1 includes a deterministic dry-run ingestion pipeline that converts structured
Codex task summaries into Memory Fabric candidate JSONL records. The parser
recognizes sections such as Goal / Purpose, Included / Changed files,
Validation, Boundary, Commit, PR, Version, and Result. Generated candidates are
grounded in explicit input text, preserve validation and boundary evidence when
present, and are marked read-only, proposal-governed, and dry-run. Negative
safety-boundary statements such as `No token write.` or `No executor call.` stay
low risk by themselves, while affirmative dangerous operations such as writing
token files, creating approval tokens, running executors, deleting credentials,
migrating memory, or modifying auth config still become high risk.

Run it with stdout output:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/ingest_codex_task_summary_dry_run.py \
  --input benchmarks/candidate_ingestion/fixtures/v13_codex_task_summary.txt
```

Or write to an explicit JSONL path for v1.1 `candidate_jsonl_path` loading:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/ingest_codex_task_summary_dry_run.py \
  --input benchmarks/candidate_ingestion/fixtures/v13_codex_task_summary.txt \
  --output /tmp/codex-task-summary-candidates.jsonl \
  --print-summary
```

The dry run does not modify Hermes Agent, implement SQLite, write to
`~/.hermes/memory`, call a model, use the network, expose provider tools, or
create durable writes outside the explicit CLI output path.

See [docs/CODEX_TASK_SUMMARY_INGESTION.md](docs/CODEX_TASK_SUMMARY_INGESTION.md)
for the schema, safety boundary, and `MemoryFabricProvider.prefetch(...)`
usage.

## v1.1.0 Read-only JSONL Candidate Source

v1.1.0 lets `MemoryFabricProvider.prefetch(...)` load candidates from an
existing local JSONL file through `runtime_config["candidate_jsonl_path"]`.
JSONL candidates are bounded by line and byte limits, invalid lines are ignored
by default, runtime candidates can still be supplied explicitly, and duplicate
candidate `id` values prefer explicit runtime candidates over JSONL.

The source remains local and read-only: no SQLite, no Hermes graph DB reads, no
operation ledger reads, no write proposal reads, no session log reads, no model
calls, no network calls, no durable writes, and no provider tools.

See [docs/JSONL_CANDIDATE_SOURCE.md](docs/JSONL_CANDIDATE_SOURCE.md) for the
format, safety boundary, and smoke command.

## v1.0.0 Real Active Context Injection Contract

v1.0.0 implements `MemoryFabricProvider.prefetch(...)` for Hermes' existing
real injection path. The provider now composes valid runtime memory candidates
into bounded `compact_context_text`, returns `""` when there is no usable active
context, keeps candidates/config in memory only, performs no durable writes, and
continues to expose no provider tools.

See [docs/REAL_ACTIVE_CONTEXT_INJECTION.md](docs/REAL_ACTIVE_CONTEXT_INJECTION.md)
for the contract, local smoke, and the separate manual real chat smoke boundary.

## v0.9.0 Active Context Quality Harness

v0.9.0 adds a deterministic local harness for validating
`MemoryFabricProvider` active context packets. It proves bounded,
project-scoped, explainable context selection and rejection behavior without
network calls, real model calls, durable writes, graph writes, token writes,
approval-audit writes, operation-ledger writes, executor calls, or provider
tool exposure.

Run it with:

```bash
python scripts/run_active_context_quality_harness.py
```

See [docs/ACTIVE_CONTEXT_QUALITY_HARNESS.md](docs/ACTIVE_CONTEXT_QUALITY_HARNESS.md)
for JSON output, fail-threshold usage, fixture details, and the separate manual
Hermes chat smoke.

## v0.1 Behavior

Version 0.1 is intentionally read-only. The provider lifecycle is available, but it does not perform durable memory writes, does not invoke a real token write executor, and does not expose Memory Fabric tools to the model by default.

`MemoryFabricProvider.get_tool_schemas()` returns an empty list in v0.1. The copied tool modules use a local registry shim for standalone tests and future adapter work, but the provider does not publish those tools until the standalone adapter boundary is reviewed.

Civilization Core / Memory Fabric Subspace Index v0.1 adds deterministic,
read-only project, agent, risk, archive, global, and custom memory domains.
The index validates subspace descriptors and registries, resolves subspaces by
id, selects only context-relevant subspaces, and reports explicit no-write,
no-graph-write, no-token-write, no-executor, and no-provider-tool policy flags.

Hermes Memory Fabric Recall Fusion v2 adds a read-only, deterministic recall
layer over Subspace Index. `fuse_memory_retrieval_v2(...)` activates governed
subspaces when a registry is provided, boosts memories that match selected
subspace ids or project/agent scopes, and explains selected and rejected
memories. Public helpers `explain_memory_retrieval_v2_result(...)` and
`summarize_memory_retrieval_v2_result(...)` expose selection reasons, rejected
subspaces, score components, and no-write/no-executor policy flags. v2 uses
local lexical scoring only; it does not call external APIs, write durable
memory, write graph state, write token files, write approval audits, or expose
provider tools.

Hermes Memory Bench v0.2 adds the `v02` suite under
`benchmarks/hermes_memory_bench/`. It deterministically measures Recall Fusion
v2 selection and rejection quality, Subspace Index isolation, archived and
high-risk gating, temporal/conflict handling, explanation quality, and no-write
safety without network calls or durable memory side effects.

Civilization Core / Hermes Memory Fabric Active Context Composer v0.1 adds a
deterministic context-packet layer over Recall Fusion v2. It composes selected
subspace summaries and the highest-value selected memories into a bounded
`active_context_packet`, explains selected and rejected memories/subspaces, and
keeps the same read-only/no-write/no-token/no-executor/no-provider-tool policy
surface.

Provider Runtime Integration v0.1 wires Active Context Composer into
`MemoryFabricProvider` through provider-level `build_active_context(...)`,
`summarize_active_context(...)`, `explain_active_context(...)`, and
`validate_active_context(...)` methods. The provider keeps conservative local
defaults, exposes no tools by default, and performs no durable memory, graph,
token, approval-audit, config, ledger, or executor writes.

## Layout

- `src/hermes_memory_fabric/`: extracted Memory Fabric and evidence-repair modules.
- `src/hermes_memory_fabric/provider.py`: Hermes-compatible provider wrapper.
- `src/hermes_memory_fabric/tools/`: callable tool wrappers using the local registry shim.
- `tests/`: extracted and standalone-scoped tests.
- `benchmarks/hermes_memory_bench/`: deterministic smoke and v0.2 benchmark fixtures.
- `benchmarks/active_context_quality/`: deterministic v0.9 active context quality fixtures.
- `docs/share-hermes-memory-with-codex-openclaw.md`: copied guide when present in the prototype branch.

## Limitations

- No provider tools are exposed in v0.1.
- Registry registration is local to this package and does not import Hermes core `tools.registry`.
- Hermes core provider-manager and third-party provider tests are copied for reference but excluded from standalone pytest collection.
