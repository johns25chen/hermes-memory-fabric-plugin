# R10 Local Project Handoff

`scripts/r10_project_handoff.py` is a local, read-only entry for an explicitly
authorized set of UTF-8 text files. It constructs source-linked candidates and
calls the public `MemoryFabricProvider.build_active_context()` API. It does not
read directories recursively, discover sources, use candidate storage, call a
model or network, persist candidates, or create ongoing authorization.

## Required inputs

- Repeat `--source-file` for every file permitted for this one call.
- Give the question and exact `--project`, `--workspace`, and `--namespace`
  values. `--workspace` is a logical absolute scope identifier, not permission
  to read that directory.
- Declare `--caller-risk-level` explicitly. This is the local caller's
  classification, not an independent risk review and never comes from the file
  body. Existing Provider defaults still exclude `high` and `critical` input
  unless its existing allowlist admits them.
- Supply an existing, non-symlink `--output-dir` and
  `--confirm-local-context-use`. Confirmation applies only to the current
  candidate set and invocation.

Each source must be a non-symlink regular UTF-8 file no larger than
`1,048,576` bytes by default. It uses `lstat` before opening and rejects a
non-regular object before it could block on a FIFO; the final descriptor is
opened non-blocking with no-follow where supported, checked by `fstat`, and
must match the pre-open device/inode. It rejects directories, devices, missing
paths, symlinks, invalid UTF-8, empty files, replacements before open, and an
existing result target. This is a local trusted-caller boundary, not a general
filesystem sandbox against a malicious same-host path-racing adversary. File
instructions are data, never executed.

Long text is split deterministically into consecutive original-text segments
(`--max-segment-chars`, default 1600). Each candidate preserves its normalized
absolute file path, SHA-256, line range and character-offset range. Its stable
identity derives from that path, content SHA-256, and character range, not
argument order. Identical content at different paths remains distinct; the
same normalized source path may be supplied only once. The body is never
summarized or rewritten.

The candidate governance declaration is fixed to dry-run/read-only,
proposal-governed and no-memory/no-graph/no-config writes. It describes this
entry's non-write boundary; it is not a proposal approval or a risk-review
finding. The source descriptor is a trusted local caller for the existing
`READ_CANDIDATE` admission boundary only, not a persistence or downstream-use
authorization.

## Example

Create an empty output directory, then run from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD/src:$PWD" .venv/bin/python scripts/r10_project_handoff.py \
  --source-file docs/CIVILIZATION_CORE_R9_FORMAL_CLOSURE_DECISION.md \
  --source-file /Users/han/r8-validation-evidence/R10_ORDINARY_HANDOFF_COMMIT_PR_MERGE_1/FINAL_REPORT.md \
  --question '依据这些材料，文明之核已经完成什么，哪些能力和阶段仍未得到证明，下一项最值得执行的工作是什么？' \
  --project CIVILIZATION-CORE \
  --workspace /governance/civilization-core/r10-local-project-handoff \
  --namespace r10-local-project-handoff \
  --caller-risk-level low \
  --output-dir /absolute/empty/output-directory \
  --confirm-local-context-use
```

The exit status is `0` for `DELIVERED`, `3` for `NO_CONTEXT`, `1` for an
execution or delivery error, and argparse's `2` for invalid arguments or input
paths. `NO_CONTEXT` is a valid absence of deliverable context (including zero
budget or Provider rejection of high/critical risk candidates), not a product
failure. It prints only `NO_CONTEXT` and creates no formal result file. Only
`DELIVERED` prints a result path, after all requested output writes complete.

On `DELIVERED`, the default sole write is `project-handoff-context.json`. It
contains only the actual delivered nonempty `context` and source mappings for
its context items. The Provider packet is validated and every delivered item
is checked against its source before publication. Rejected or budget-excluded
segments and the full packet are not in the default file.

The delivered item body must equal its mapped original segment after the
Provider's surrounding-whitespace trim, even when its ID, source ID and compact
rendering are internally consistent. A body mismatch returns delivery error
`1` before either the formal result or optional diagnostics are published.

Pass `--write-diagnostics` only when explicit diagnostic retention is needed;
it adds the separately named `project-handoff-diagnostics.json` with the raw
packet, all input candidates, and validation/explanation material. This file
may exist with `NO_CONTEXT`, or after a subsequent result publication failure;
its existence never proves delivery. Both files are serialized before writing,
written fully to a task-owned temporary file in the output directory, then
published without overwriting an existing target. A failed write can leave a
previously completed diagnostic, but not a truncated formal result. A nonempty
result does not establish user value, task completion, automatic recall,
persistence, cross-call revocation, or R10 closure.
