# Governed Memory Proposal Review Gate Dry Run

v2.5.0 adds a deterministic review gate for the v2.4.0 governed memory proposal
pack dry run. The gate consumes
`docs/CIVILIZATION_CORE_VIDEO_AI_SKILLS_MEMORY_PROPOSAL.md` through
`build_governed_memory_proposal_pack_dry_run(proposal_path)` and produces a
structured review decision report.

The review gate classifies each proposal-pack entry into one of four decisions:

- `approve_candidate` for proposed entries targeting `long_term_memory`,
  `short_term_memory`, `operation_ledger`, or `knowledge_surface`.
- `reject_locked` for rejected entries and entries marked as non-durable.
- `risk_note_only` for risk-note entries.
- `defer_for_human_review` for unknown statuses or unknown target surfaces.

Non-durable material such as temporary command authorizations, API keys or
secrets, raw credentials, Docker logs, temporary paths, PIDs, and one-off task
state cannot become `approve_candidate`.

## Safety Boundary

This dry run does not perform any real memory action:

- It does not write Hermes memory.
- It does not mutate the Memory Graph.
- It does not append operation ledger entries.
- It does not issue approval tokens.
- It does not create usable tokens.
- It does not execute provider tools.
- It does not expose provider tools.
- It does not modify Hermes Agent.
- It does not use the network.

## Smoke

```bash
PYTHONPATH="$PWD/src:$PWD" python3 scripts/smoke_governed_memory_proposal_review_gate_dry_run.py
```

Expected output:

```text
governed_memory_proposal_review_gate_dry_run=passed
```
