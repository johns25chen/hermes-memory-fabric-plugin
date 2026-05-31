# Executor Surface Lockdown Audit

v1.6.0 adds a read-only audit layer before any Approval Intent work. The v1.5
chain already proved that Codex task summaries can become candidate JSONL and
proposal dry-run previews without durable writes. The next risk is accidental
wiring from approval, token, executor, write-lock, ledger, or tool-wrapper code
into real proposal creation or token execution. v1.6 locks that surface down
first.

## Why This Comes Before Approval Intent

Approval Intent should not be added while executor-adjacent modules can
accidentally drift into real writes. The v1.6 audit is intentionally a static
checkpoint:

- it does not create human approval intent;
- it does not create approval tokens;
- it does not implement or call a real write executor;
- it does not create proposal, ledger, token, audit, graph, config, SQLite, or
  memory files;
- it does not expose provider tools.

## Audited Surfaces

The audit reads repository Python source files with `Path.read_text` and parses
them with `ast`. It skips `__pycache__` and does not import the modules being
audited.

Audited source groups:

- approval modules;
- token modules;
- executor modules;
- write-lock modules;
- ledger modules;
- tool wrapper modules under `src/hermes_memory_fabric/tools`;
- the v1.5 proposal dry-run boundary;
- the `MemoryFabricProvider` tool exposure boundary.

## Forbidden Files And Calls

The audit fails if these files exist outside `__pycache__`:

- `memory_human_approval_token_real_write_executor.py`
- `test_memory_human_approval_token_real_write_executor.py`

The audit also fails on any Python call to:

- `memory_fabric_bridge.create_memory_write_proposal`
- `create_memory_write_proposal`

This keeps v1.5 and v1.6 dry-run paths separate from the real bridge proposal
writer.

## Forbidden Write Surfaces

Executor-adjacent target groups are checked for direct write APIs:

- `open(..., "w")`, `open(..., "a")`, `open(..., "x")`, or `+` modes;
- `Path.open(...)` with write/append/exclusive/update modes;
- `Path.write_text(...)`;
- `Path.write_bytes(...)`;
- SQLite write statements such as `INSERT`, `UPDATE`, `DELETE`, `CREATE`,
  `DROP`, `ALTER`, or `REPLACE`;
- operation-ledger append/write helper calls.

The normal v1.6 report must contain:

```json
"forbidden_write_surfaces": []
```

## Required No-write Flags

Every discovered real-write-executor planning or review module must statically
contain these false flags:

```json
{
  "invokes_real_token_write_executor": false,
  "implements_real_token_write_executor": false,
  "issues_real_approval_tokens": false,
  "writes_operation_ledger": false,
  "writes_token_files": false,
  "writes_approval_audit": false,
  "applies_proposals": false
}
```

Missing flags are reported in `missing_no_write_flags` and fail the audit.

## v1.5 Proposal Dry-run Boundary

The audit verifies that `memory_candidate_proposal_dry_run.py` still exposes the
v1.5 no-write boundary:

```json
{
  "created_real_proposal": false,
  "writes_proposal_files": false,
  "writes_operation_ledger": false,
  "writes_memory": false,
  "writes_graph": false,
  "writes_config": false,
  "writes_sqlite": false,
  "writes_token_files": false,
  "writes_approval_audit": false,
  "applies_proposals": false,
  "provider_tools": []
}
```

This ties v1.6 directly to the v1.5 proposal dry-run preview: v1.5 can still
produce in-memory proposal previews, but no dry-run path may call the real bridge
writer or expose provider tools.

## Usage

Print JSON to stdout:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/audit_executor_surface_lockdown.py
```

Write to one explicit output path:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/audit_executor_surface_lockdown.py \
  --output /tmp/executor-surface-lockdown-audit.json \
  --print-summary
```

The CLI refuses output paths under `HERMES_HOME` or `~/.hermes`.

Run the smoke:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/smoke_executor_surface_lockdown_audit.py
```

## What This Proves

The audit proves the checked source tree currently preserves the preview-only
boundary for provider exposure, v1.5 proposal previews, executor-adjacent write
APIs, forbidden executor filenames, and real-write-executor no-write flags.

The smoke additionally proves the audit can run without creating files under a
temporary `HERMES_HOME`.

## What This Does Not Prove

The audit is static. It does not prove that every possible runtime path outside
the scanned source groups is side-effect free, and it does not validate future
code generated after the audit runs. It also does not implement governance,
approval intent, approval token issuance, real executor execution, ledger
appends, proposal application, or any durable memory write.
