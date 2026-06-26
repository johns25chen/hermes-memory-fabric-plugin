# Civilization Core Memory Evaluation Candidates / 文明之核记忆评测候选方案

## 2. Candidate Status

This is a docs-only candidate methodology document.

It is based on the sealed `v6.16.0` Civilization Core Stable Kernel.

It is based on the merged Memory Systems Landscape Report.

It is evaluation-candidate only.

It creates no benchmark implementation.

It creates no evaluation runner.

It adds no tests.

It makes no code changes.

It makes no README changes.

It makes no existing doc changes.

It makes no package version change.

It creates no tag.

It creates no `v6.17`.

It creates no v7 implementation authorization.

It does not start P4.

It creates no product implementation authorization.

It creates no MVP.

It creates no runtime / dependency / adapter activation.

It creates no MCP/API operation surface.

It mutates no Memory Graph.

It adds no durable writer.

It adds no authorization/execution semantics.

The evaluation language in this document is candidate vocabulary only. It does not approve implementation, productization, connector adoption, dependency adoption, external project behavior, durable memory writing, graph mutation, automatic authorization, or automatic execution.

## 3. Why Memory Evaluation Comes First

Temporal validity, lifecycle, failed-attempt memory, explainable recall, connector governance, and P4 all need evaluation language first.

Without evaluation language, later docs can become concept lists: temporal facts, stale records, recall traces, rejected memories, connector risks, and human-review decisions may be named without a shared way to judge whether they are good enough to trust.

Evaluation here means reviewable criteria, not automated testing.

The goal is to judge memory quality before trusting, promoting, or using memory.

A benchmark score is not governance approval.

An evaluation note is not approval.

Human review remains required before any future memory is trusted, promoted, written, updated, deleted, connected, or used as decision input.

## 4. Evaluation Boundary

| Area | Included? | Reason | Boundary |
| --- | --- | --- | --- |
| recall quality | yes | The Landscape Report highlights recall relevance, temporal retrieval, associative paths, and evidence visibility as recurring memory-system concerns. | Evaluate recall as candidate evidence only; do not activate retrieval behavior. |
| provenance quality | yes | Source traceability is central to `llm_wiki`, OpenMemory, Graphiti / Zep, Cognee, LlamaIndex, Onyx, and local governance docs. | Provenance supports review; it is not truth, approval, or Memory Graph mutation. |
| temporal validity | yes | Graphiti / Zep, mem0, MemoryOS, and the v6 Star-Source lineage make time scope and evolving facts explicit evaluation needs. | Define review criteria only; do not create the later Temporal Validity Model here. |
| confidence / uncertainty | yes | agentmemory, memory lifecycle language, and governance review all require visible uncertainty before trust. | Confidence notes remain qualitative and human-reviewed. |
| lifecycle state | yes | MemoryOS, MemOS, GBrain, and local docs need candidate / approved / rejected / stale / superseded distinctions. | Lifecycle labels are candidate vocabulary, not durable state implementation. |
| write proposal quality | yes | Boundary docs separate proposal from mutation; memory systems need clear write justification before adoption. | Proposal quality review does not write memory. |
| update / deletion proposal quality | yes | Memory lifecycle work must judge supersession, removal safety, and audit preservation. | No automatic update, deletion, or durable writer follows. |
| failed-attempt memory quality | yes | Projectmem and coding-agent memory patterns make failed attempts and do-not-retry rules important. | Failed-attempt memory remains bounded and reviewable; it must not become automatic authority. |
| explainable recall trace | yes | M-Flow, Graphiti / Zep, Cognee, OpenMemory, and Onyx suggest source paths and trace visibility. | Trace explains why a candidate surfaced; it does not authorize action. |
| connector-source risk | yes | LlamaIndex and Onyx provide connector taxonomy and enterprise source-risk inspiration. | Connector review adds no connector, adapter, sync, action, or MCP/API surface. |
| human review readiness | yes | LangGraph, GBrain, and local governance docs emphasize gates and operator review. | Readiness is candidate status only; reviewer decisions remain human-scoped. |
| privacy / local-first posture | yes | OpenMemory, Projectmem, EverOS, Khoj, and AnythingLLM provide local-first and user-control inspiration. | Privacy posture is reviewed qualitatively; no storage or sync behavior is added. |
| benchmark / replay reference | limited | GBrain, Awesome-AI-Memory, Agent Memory Techniques, and the Landscape Report make benchmark and replay useful as references. | References may guide questions; they do not create local benchmark implementation or approval. |
| automated scoring | no | Automated scoring could be mistaken for governance decision authority. | Excluded; qualitative labels are human-review vocabulary only. |
| benchmark runner | no | A runner would be implementation, not a candidate methodology document. | Excluded; no runner, suite, harness, dependency, or score execution is created. |
| code implementation | no | The sealed `v6.16.0` boundary and post-terminal docs block source changes. | Excluded; no source, test, script, config, or runtime changes. |
| P4 gate activation | no | P4 requires explicit human confirmation later. | Excluded; this document may prepare language for a future checklist only. |

## 5. Evaluation Object Types

| Object type | What it is | Evaluation question | Required evidence | Prohibited inference |
| --- | --- | --- | --- | --- |
| memory candidate | A proposed memory item that has not been approved. | Is the claim relevant, evidenced, bounded, and worth review? | Source reference, claim text, context, temporal scope, risk flags. | Do not infer approved memory, durable write, or truth. |
| approved memory record | A future memory item that a human may approve under separate governance. | Does the approval scope match the evidence and intended use? | Approval note, source path, reviewer scope, lifecycle state, conflict notes. | Do not infer broad future authority or unrelated use. |
| rejected memory record | A memory candidate rejected by review. | Is the rejection reason visible and reusable without hiding useful evidence? | Rejection reason, source reference, reviewer note, risk flags. | Do not infer deletion of audit trail or permanent impossibility. |
| stale memory record | A record whose time scope or context no longer appears current. | Is staleness explained and bounded? | Observed time, stale reason, conflict source, review requirement. | Do not infer automatic deletion or automatic replacement. |
| superseded memory record | A record replaced or narrowed by later evidence. | Is the successor visible and the prior claim preserved for audit? | Superseding reference, old claim, new claim, reviewer note. | Do not infer hidden overwrite or loss of provenance. |
| recall result | A surfaced memory candidate or record in response to a need. | Is it relevant, traceable, temporally scoped, and uncertainty-aware? | Query/reason, source path, recall reason, confidence note. | Do not infer action permission or durable adoption. |
| recall trace | The explanation path for why a recall surfaced. | Can a reviewer inspect the evidence path and reasoning boundary? | Source path, source type, inference markers, uncertainty notes. | Do not infer authorization, execution, or graph mutation. |
| write proposal | A future proposal to add a durable memory. | Does the claim belong in memory and is the source strong enough? | Source reference, claim, reason for memory, risk flags, reviewer note. | Do not infer automatic durable writer or automatic promotion. |
| update proposal | A future proposal to change an existing memory record. | What does it supersede, narrow, correct, or clarify? | Existing record reference, proposed update, conflict notes, reviewer note. | Do not infer silent overwrite. |
| deletion proposal | A future proposal to remove or hide a memory record. | Why is removal safe and what audit trail remains? | Record reference, removal reason, risk flags, reviewer note, audit-preservation note. | Do not infer erasure without governance. |
| failed attempt record | A bounded record of a failed action, approach, command, design, or assumption. | Is the failure specific enough to prevent repeated waste without freezing improvement? | Attempt summary, evidence, failure condition, retry risk, scope. | Do not infer permanent prohibition outside the stated scope. |
| do-not-retry candidate | A candidate rule that a specific failed path should not be repeated under stated conditions. | Is the blocked behavior precise, evidenced, and reviewable? | Failed attempt record, risk note, scope, exception condition. | Do not infer automatic authority or indefinite ban. |
| external source candidate | A source or external project considered for methodology inspiration. | Is the source role clear and not overread as adoption? | Source name, source type, observed methodology, risk flags. | Do not infer dependency, adapter, runtime behavior, or identity transfer. |
| connector/source candidate | A possible source class or connector idea to evaluate later. | What are trust, sync, action, credential, and privacy risks? | Source type, trust level, capability class, operator approval requirement. | Do not infer connector implementation or API surface. |
| temporal claim | A claim whose validity depends on time, version, observation date, or supersession. | Is the time scope visible and reviewable? | `valid_from`, `valid_until`, `observed_at`, stale or conflict notes. | Do not infer timeless truth. |
| human review decision | A future human-scoped candidate decision about memory quality. | Can the reviewer accept, reject, mark stale, block, or defer without side effect? | Evidence packet, reviewer note, risk flags, recommended next state. | Do not infer execution, write, deployment, or P4 activation. |

## 6. Core Evaluation Dimensions

| Dimension | Question | Candidate evidence | Source inspiration from Landscape Report | Safe next document | Prohibited action |
| --- | --- | --- | --- | --- | --- |
| relevance | Does the memory answer the actual review need? | Claim, recall reason, reviewer note. | mem0, M-Flow, Agent Memory Techniques. | Explainable Recall Trace Template. | Do not activate retrieval behavior. |
| correctness | Is the claim supported by cited local or future-approved source evidence? | Source reference, claim/evidence distinction, conflict notes. | OpenMemory, Cognee, `llm_wiki`. | Memory Lifecycle Taxonomy. | Do not treat citation as truth by itself. |
| provenance completeness | Can the source path and source type be inspected? | Source path, source type, provenance path. | Graphiti / Zep, Cognee, LlamaIndex, Onyx. | Explainable Recall Trace Template. | Do not mutate Memory Graph. |
| temporal validity | Is the time scope clear enough to avoid stale use? | `observed_at`, `valid_from`, `valid_until`, stale reason. | Graphiti / Zep, mem0, MemoryOS. | Temporal Validity Model. | Do not create time-based runtime behavior. |
| conflict awareness | Are competing claims surfaced rather than hidden? | Conflict source, conflict notes, superseded-by reference. | Cognee, Graphiti / Zep, Awesome-AI-Memory. | Memory Lifecycle Taxonomy. | Do not silently resolve conflicts. |
| confidence calibration | Is uncertainty stated in a way a reviewer can judge? | Confidence note, unknown fields, blocked reason. | agentmemory, MemoryOS, GBrain. | Memory Lifecycle Taxonomy. | Do not convert confidence into approval. |
| lifecycle clarity | Is the memory candidate, approved, rejected, stale, superseded, or blocked? | Lifecycle state, recommended next state, reviewer note. | MemoryOS, MemOS, GBrain, LangMem. | Memory Lifecycle Taxonomy. | Do not implement durable lifecycle storage. |
| recall explainability | Can the reviewer see why the memory surfaced? | Recall reason, source trace, inference markers. | M-Flow, Graphiti / Zep, OpenMemory, Cognee. | Explainable Recall Trace Template. | Do not treat explanation as authorization. |
| write safety | Is a proposed memory write justified and bounded? | Source reference, why it belongs in memory, risk flags. | mem0, LangMem, GBrain. | Memory Lifecycle Taxonomy. | Do not add a durable writer. |
| update safety | Does the update show what it supersedes or corrects? | Prior record reference, proposed change, conflict notes. | MemOS, MemoryOS, LangMem. | Memory Lifecycle Taxonomy. | Do not silently overwrite records. |
| deletion safety | Is removal safe while preserving auditability? | Deletion reason, audit trail, reviewer note. | MemOS, MemoryOS, OpenMemory. | Memory Lifecycle Taxonomy. | Do not erase evidence without governance. |
| failed-attempt usefulness | Does the failure record prevent repeated waste while keeping scope bounded? | Failed attempt summary, evidence, retry risk. | Projectmem, agentmemory, Agent Memory Techniques. | Failed Attempt Memory / Do-Not-Retry Rules. | Do not freeze future improvement. |
| do-not-retry precision | Is the prohibited retry path specific enough? | Blocked behavior, conditions, exception notes. | Projectmem, coding-agent memory patterns. | Failed Attempt Memory / Do-Not-Retry Rules. | Do not create automatic authority. |
| connector risk clarity | Are source, trust, sync, action, credential, and privacy risks visible? | Source type, trust level, risk flags, approval requirement. | LlamaIndex, Onyx, Khoj. | Connector Governance Taxonomy. | Do not add connectors, adapters, or MCP/API operation surface. |
| privacy/locality clarity | Is the local-first or remote exposure posture clear? | Local/remote note, credential risk, privacy risk. | OpenMemory, Projectmem, EverOS, Khoj, AnythingLLM. | Connector Governance Taxonomy. | Do not create storage, sync, or cloud behavior. |
| human review readiness | Can a reviewer make a bounded decision from visible evidence? | Evidence packet, reviewer note, risk flags, recommended next state. | LangGraph, GBrain, Onyx. | P4 Decision Gate Checklist. | Do not start P4. |
| regression/replay usefulness | Could the evidence be replayed or compared later in docs? | Replay reference, scenario description, expected review question. | GBrain, Awesome-AI-Memory, Agent Memory Techniques. | P4 Decision Gate Checklist. | Do not implement benchmark or evaluation runner. |
| operator usability | Can a human operator understand the memory state without hidden assumptions? | Plain-language reason, risk flags, source trace, next state. | AnythingLLM, Khoj, EverOS, GBrain. | External Product Explanation Candidate. | Do not build Operator Console or MVP. |

## 7. Qualitative Score Candidate

Future docs may use this non-implemented qualitative vocabulary:

| Label | Candidate meaning |
| --- | --- |
| `0 = not evidenced` | No usable evidence is present for the evaluation question. |
| `1 = weak / incomplete evidence` | Some evidence exists, but it is missing key source, time, conflict, or risk detail. |
| `2 = adequate candidate evidence` | Evidence is sufficient for candidate review, but still requires human judgment. |
| `3 = strong review-ready evidence` | Evidence is clear, bounded, traceable, and ready for human review. |
| `blocked = must not proceed` | A boundary, safety, scope, or evidence gap prevents progress. |
| `unknown = not enough information` | The reviewer cannot judge without more source context. |

This is not an automated score.

This is not a benchmark runner.

This is not approval.

This is not execution permission.

Human operator review remains required.

## 8. Evidence Packet Candidate

Future docs may use this evidence packet shape as a document template only:

| Field | Candidate purpose |
| --- | --- |
| `candidate_id` | Stable candidate identifier for discussion. |
| `memory_type` | Object type such as recall result, write proposal, stale record, or failed attempt record. |
| `claim` | The memory claim or proposed memory content. |
| `source_reference` | The local or future-approved source being cited. |
| `source_timestamp` | Timestamp or date associated with the source when available. |
| `provenance_path` | Human-readable path from source to claim. |
| `temporal_scope` | Time period, version scope, or unknown time scope. |
| `conflict_notes` | Known conflicts, missing comparisons, or supersession risks. |
| `confidence_note` | Qualitative uncertainty and evidence-strength note. |
| `lifecycle_state` | Candidate, approved, rejected, stale, superseded, blocked, or unknown. |
| `recall_reason` | Why the memory surfaced or why it may be useful. |
| `reviewer_note` | Human review comment or review request note. |
| `risk_flags` | Boundary, privacy, connector, conflict, staleness, or authority risks. |
| `recommended_next_state` | Proposed next review state, not automatic transition. |
| `blocked_reason` | Reason progress must stop, if blocked. |

This is a document template only, not schema implementation.

It creates no storage format, parser, validation rule, runner, API, writer, or graph mutation.

## 9. Recall Evaluation Candidates

Future docs may evaluate recall with questions such as:

- was the recall relevant?
- was the source trace visible?
- was temporal scope clear?
- was conflict or staleness surfaced?
- was confidence explained?
- was the recall actionable only after review?
- did it avoid fabricating unsupported facts?
- did it avoid over-retrieval?
- did it avoid hiding uncertainty?

Recall evaluation should preserve the boundary that recall is not write.

Recall traces should distinguish evidence from inference.

Recall results should remain candidate evidence until human review.

This document creates no retrieval implementation.

## 10. Write / Update / Delete Evaluation Candidates

Future docs may evaluate memory mutation proposals with these candidate rules:

- write proposal must show source;
- write proposal must show why it belongs in memory;
- update proposal must show what it supersedes;
- deletion proposal must show why removal is safe;
- stale marking must preserve audit trail;
- rejected memory must remain explainable;
- no automatic durable writer;
- no automatic promotion.

Write, update, deletion, stale marking, rejection, and promotion are governance concepts here.

They are not active mutation behavior.

They require explicit future human scope before any implementation discussion.

## 11. Failed Attempt / Do-Not-Retry Evaluation Candidates

Future docs may evaluate failed-attempt memory with these candidate rules:

- failure must be specific;
- retry risk must be stated;
- evidence must be attached;
- scope must be bounded;
- blocked behavior must be reviewable;
- do-not-retry must not become automatic authority;
- failed attempt memory must not freeze future improvement.

A failed attempt record should explain what failed, under what conditions, and why repeating the same path is risky.

A do-not-retry candidate should name the blocked retry path narrowly enough that future improvements, changed environments, or human-approved exceptions remain possible.

Failed-attempt memory is useful only when it reduces repeated waste without creating hidden law.

## 12. Temporal Validity Evaluation Candidates

Future docs may evaluate temporal claims with these candidate fields:

| Field | Candidate question |
| --- | --- |
| `valid_from` | When did the claim begin to apply? |
| `valid_until` | When should the claim stop being trusted, if known? |
| `observed_at` | When was the claim observed or sourced? |
| `superseded_by` | What later record or source replaced it? |
| `stale_reason` | Why may it no longer be current? |
| `conflict_source` | What source conflicts with it? |
| `review_required` | What human review is needed before use? |
| `unknown_time_scope` | What time uncertainty remains? |

Temporal evaluation should prevent timeless use of time-bound facts.

This prepares the later Temporal Validity Model only.

It does not create temporal storage, temporal queries, scheduling, automated expiry, or runtime behavior.

## 13. Provenance and Explainable Recall Evaluation Candidates

Future docs may evaluate provenance and explainable recall with these candidate criteria:

- source path visible;
- source type clear;
- claim/evidence distinction clear;
- inference marked;
- uncertainty visible;
- trace sufficient for human review;
- no explanation treated as authorization.

Provenance should make it possible for a reviewer to answer: what source was used, what claim was taken from it, what inference was added, and what uncertainty remains.

Explainable recall should show why something surfaced without turning the explanation into truth, approval, execution, or graph mutation.

## 14. Connector Governance Evaluation Candidates

Future docs may evaluate external source / connector candidates with these criteria:

| Criterion | Candidate question |
| --- | --- |
| source type | What kind of source is being considered? |
| trust level | How trusted is the source and why? |
| read-only / write-capable distinction | Could the source only be read, or could it change external state? |
| sync risk | Could stale, partial, or repeated sync distort memory? |
| action risk | Could the source or connector trigger external action? |
| credential risk | Would credentials, secrets, or privileged accounts be involved? |
| privacy risk | Could personal, team, enterprise, or sensitive data be exposed? |
| stale-source risk | Could the source become outdated without visible warning? |
| operator approval requirement | What explicit human approval would be needed before any future step? |

This document adds no connector.

It adds no adapter.

It creates no MCP/API surface.

It creates no action behavior.

Connector governance here is review vocabulary only.

## 15. Human Review Gate Evaluation Candidates

Before P4 can be considered in any later document, future candidate review should require:

- reviewer can see evidence;
- reviewer can see risk flags;
- reviewer can see recommended next state;
- reviewer can reject without side effect;
- reviewer can mark stale / superseded / blocked;
- reviewer decision is recorded as candidate only;
- P4 remains paused;
- P4 requires explicit human confirmation later.

Human review readiness means a reviewer can make a bounded candidate decision without hidden mutation, hidden execution, hidden promotion, or hidden product launch.

The decision remains candidate-only unless a separate future human approval explicitly changes scope.

## 16. Candidate Future Sequence

Recommended docs-only sequence:

1. Temporal Validity Model
2. Memory Lifecycle Taxonomy
3. Failed Attempt Memory / Do-Not-Retry Rules
4. Explainable Recall Trace Template
5. Connector Governance Taxonomy
6. Memory Ontology Mapping
7. External Product Explanation Candidate
8. P4 Decision Gate Checklist

This document does not start any of them.

P4 remains paused.

P4 requires explicit human confirmation later.

Each future item must remain docs-only unless the human operator separately and explicitly scopes a different kind of work.

## 17. Prohibited Implementation Rules

Do not implement evaluation runner.

Do not implement benchmark runner.

Do not add tests.

Do not add dependencies.

Do not add adapters.

Do not create runtime-activation bridge.

Do not create MCP/API operation surface.

Do not mutate Memory Graph.

Do not add durable writer.

Do not add authorization/execution semantics.

Do not start v7 implementation.

Do not build MVP.

Do not implement Operator Console.

Do not tag post-terminal docs.

Do not change package version.

Do not change existing docs.

Do not change README.

Do not change source, tests, scripts, or config.

Do not treat evaluation score as approval.

Do not treat benchmark score as governance approval.

Do not treat external project benchmark as Civilization Core benchmark.

## 18. Stop Conditions

If evaluation turns into code, stop.

If evaluation turns into tests, stop.

If evaluation turns into benchmark runner, stop.

If evaluation turns into dependency adoption, stop.

If evaluation turns into adapter work, stop.

If evaluation turns into MCP/API operation surface, stop.

If evaluation turns into Memory Graph mutation, stop.

If evaluation turns into durable writer, stop.

If evaluation turns into authorization/execution semantics, stop.

If evaluation starts P4, stop.

If evaluation starts v7 implementation, stop.

If evaluation starts MVP/product deployment, stop.

If evaluation starts changing old docs, stop.

If pyproject version changes, stop.

If `uv.lock` appears, stop.

If tag creation is suggested, stop.

## 19. Final Candidate Statement

This document defines memory evaluation candidates only.

It does not evaluate live memory.

It does not implement benchmark.

It does not authorize implementation.

`v6.16.0` remains sealed.

Future work must preserve boundary and require explicit human approval.
