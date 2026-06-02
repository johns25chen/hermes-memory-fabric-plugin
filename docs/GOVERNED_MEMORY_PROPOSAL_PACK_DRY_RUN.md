# Governed Memory Proposal Pack Dry Run

v2.4.0 adds a deterministic local proposal pack builder for
`docs/CIVILIZATION_CORE_VIDEO_AI_SKILLS_MEMORY_PROPOSAL.md`.

The builder parses the Markdown staging artifact into structured entries for:

- Long-term memory candidates.
- Short-term memory candidates.
- Operation ledger candidates.
- Knowledge surface candidates.
- Do-not-persist material.
- Risk notes.

Each entry receives a stable `proposal_id`, target surface, status, content,
non-durable classification, and explicit no-write safety flags.

This is a dry run only. It does not write Hermes memory, mutate the Memory
Graph, append an operation ledger entry, change config, write SQLite state,
invoke an executor, expose provider tools, call model/provider APIs, or use the
network. It also does not create a real governed memory write proposal.

Temporary command authorizations, one-off temporary state, API keys or secrets,
raw credentials, Docker logs, temporary paths, and PIDs are classified as
non-durable and rejected from durable-memory persistence.

Run the smoke check:

```bash
PYTHONPATH="$PWD/src:$PWD" python3 scripts/smoke_governed_memory_proposal_pack_dry_run.py
```

Expected output:

```text
governed_memory_proposal_pack_dry_run=passed
```
