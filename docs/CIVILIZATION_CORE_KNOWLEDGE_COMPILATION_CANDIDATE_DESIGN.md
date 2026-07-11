# Civilization Core Knowledge Compilation Candidate Design / 文明之核知识编译候选设计

## 1. Candidate Status / 候选状态

This document is docs-only, design-only, candidate-only, methodology-study-only, and evidence-modeling-only. It is based on the sealed `v6.16.0` Civilization Core Stable Kernel and governed by `docs/CIVILIZATION_CORE_V7_DESIGN_ONLY_CHARTER.md`. The following source set also constrains its interpretation:

- `docs/CIVILIZATION_CORE_V7_PRE_DESIGN_DECISION.md`
- `docs/CIVILIZATION_CORE_EXTERNAL_CANDIDATE_COMPARISON.md`
- `docs/CIVILIZATION_CORE_DECISION_GATE_CHECKLIST.md`
- `docs/CIVILIZATION_CORE_BOUNDARY_CONSTITUTION.md`
- `docs/CIVILIZATION_CORE_PRODUCTIZATION_ROADMAP.md`
- `docs/CIVILIZATION_CORE_PRODUCT_NARRATIVE_PACKAGE.md`
- `docs/CIVILIZATION_CORE_FINAL_ROADMAP.md`
- `docs/CIVILIZATION_CORE_COMPREHENSIVE_AUDIT_REPORT.md`
- `docs/CIVILIZATION_CORE_ARCHITECTURE_ATLAS.md`
- `docs/CIVILIZATION_CORE_WHITEPAPER.md`
- `docs/CIVILIZATION_CORE_ONE_PAGE_OVERVIEW.md`
- `docs/CIVILIZATION_CORE_FAQ.md`
- `docs/CIVILIZATION_CORE_READER_PATH.md`
- `docs/CIVILIZATION_CORE_HANDOFF_PACKAGE.md`
- `docs/CIVILIZATION_CORE_RELEASE_BOOK.md`
- `docs/CIVILIZATION_CORE_DOCUMENT_INDEX.md`

This candidate changes no existing document, code, test, dependency, or package version. It creates no tag: there is no `v6.17` and no `v7.0.0` release authorization. It grants no runtime implementation authorization, storage implementation authorization, or product implementation authorization. It creates no automatic persistence and no Memory Graph mutation.

`Knowledge Compilation Candidate` is a design workstream label, not an implemented compiler, service, module, runtime, or product; this candidate design is not implementation permission.

## 2. Candidate Purpose / 候选目的

The purpose is to preserve raw sources through raw source preservation; distinguish sources, evidence, derivations, and a compiled knowledge candidate; establish provenance-preserving compilation discipline; describe the conceptual responsibilities of a purpose registry, schema registry, index discipline, and compilation log; form a human review queue; and frame corpus lint and graph insight candidate concepts. The design aims to reduce unreviewed knowledge entering long-term memory and to prepare evidence for later human decisions.

Knowledge compilation is candidate preparation, not memory adoption.

## 3. Problem Definition / 问题定义

- A raw source must not be overwritten by a compiled result.
- A summary is not a fact, and derived text is not its source.
- Successful compilation is not trustworthiness.
- Schema conformity is not knowledge correctness.
- Building an index does not authorize retrieval results.
- A corpus lint pass is not approval.
- A graph insight is not a graph fact.
- A review queue is not an adoption queue.
- Automatic ingest can lose sources, compress context, inherit errors, and contaminate later candidates.
- Unreviewed compilation can cause drift, overreach, and loss of traceability.

## 4. Design Principles / 设计原则

1. Preserve raw sources.
2. Preserve provenance.
3. Separate evidence from derivation.
4. Keep compiled output candidate-only.
5. Make purpose explicit.
6. Make transformation traceable.
7. Make uncertainty visible.
8. Keep review human-controlled.
9. Prevent automatic persistence.
10. Prevent automatic Memory Graph mutation.
11. Prefer reversible design records.
12. Preserve rejection and deferral evidence.

Source preservation outranks presentation convenience. Traceability outranks compression. Compilation completeness does not outrank governance. More compiled knowledge is not automatically better knowledge.

## 5. Source and Evidence Model / 来源与证据模型

These are vocabulary candidates, not implemented records.

| Object | Conceptual purpose | Minimum provenance | Human review role | Non-authoritative boundary |
|---|---|---|---|---|
| Source | Identify original supplied material | origin, locator, observed time, scope | Confirm identity and permitted scope | Presence does not establish truth |
| Source Snapshot | Refer to a bounded observed source state | source reference, observation context, capture description | Assess fidelity and relevance | Source snapshot is not persistent storage implementation |
| Source Segment | Identify a reviewable portion | snapshot reference, segment locator, surrounding context | Check selection and omitted context | Source segment is not an adopted memory unit |
| Evidence Item | Package a cited observation | segment reference, extraction description, owner | Judge support for a candidate claim | Evidence item is not approval |
| Extraction Context | Explain why and how evidence was selected | purpose, scope, constraints, omissions | Detect framing or selection bias | Context does not certify extraction correctness |
| Provenance Link | Relate a derived object to evidence | source and target identities, relation, transformation reference | Verify trace continuity | Provenance link is not truth certification |
| Source Gap | Record missing or unavailable support | affected scope, expected evidence, discovery context | Decide return, defer, reject, or escalate | A gap is not permission to infer |
| Source Conflict | Record incompatible source statements | competing references, scope, conflict description | Evaluate rather than suppress disagreement | Conflict recording does not resolve conflict |
| Source Scope | Bound intended source use | purpose, audience, exclusions, expiry | Confirm use stays within scope | Scope does not authorize broader reuse |
| Source Owner | Name accountable human ownership | owner identity, responsibility context, review route | Clarify accountability and escalation | Source owner is not automatic authorization |

## 6. Compiled Knowledge Candidate Model / 编译知识候选模型

| Object | Conceptual responsibility | Required boundary |
|---|---|---|
| Compiled Knowledge Candidate | Assemble reviewable derived knowledge | Compiled candidate is not adopted memory |
| Candidate Claim | State a bounded proposition | Candidate claim is not verified fact |
| Candidate Summary | Condense candidate material | Candidate summary is not authoritative source |
| Candidate Structure | Organize candidate elements | Structure does not establish correctness |
| Candidate Citation Set | Connect claims to source evidence | Citations do not eliminate review |
| Candidate Gap Set | Preserve known missing support | Gaps may not be silently filled |
| Candidate Conflict Set | Preserve unresolved contradictions | Conflicts may not be suppressed |
| Candidate Confidence Note | Describe uncertainty and basis | Confidence note is not approval score |
| Candidate Scope | Bound purpose, audience, and use | Scope cannot expand itself |
| Candidate Expiry | Signal staleness or review horizon | Expiry is not automatic deletion |
| Candidate Review State | Record human review disposition | Review state is not execution state |

Every candidate should retain source references, a transformation description, omitted context, uncertainty, conflicts, scope, owner, review state, and an expiry or staleness signal. In every interpretation, compiled candidate is not adopted memory.

## 7. Conceptual Compilation Lifecycle / 概念编译生命周期

`source registration → source preservation → evidence extraction → transformation record → candidate assembly → lint review → boundary review → human review → decision record`

No step may be skipped automatically. Source preservation precedes candidate assembly. Evidence extraction must not overwrite a source. Transformation must remain traceable. Lint must not approve automatically; boundary review must not authorize automatically; human review must not execute automatically; and a decision record must not persist a candidate automatically.

Stopped work preserves evidence. A rejected candidate remains rejected. A deferred candidate remains deferred. Expired scope requires new explicit human scope.

## 8. Purpose Registry Candidate / 目的注册表候选

The purpose registry is conceptual only. Its field concepts are `purpose_id`, `purpose_name`, `human_owner`, `intended_use`, `forbidden_use`, `source_scope`, `audience_scope`, `retention expectation`, `review requirement`, `expiry condition`, `authorization boundary`, and `execution boundary`.

A registry entry is not permission. Purpose declaration is not authorization. Intended use does not allow forbidden use. Missing purpose produces `HOLD`; tools may not infer missing purpose. No registry is implemented.

## 9. Schema Registry Candidate / 模式注册表候选

The conceptual schema registry would describe schema identity, schema purpose, required fields, optional fields, provenance requirements, validation expectations, a version note, a compatibility note, review owner, and forbidden interpretation.

The schema registry is not implemented; schema validity is not semantic correctness. Schema conformance is not approval. Schema version is not package version. Schema declaration is not storage authorization. No database schema is created.

## 10. Index Discipline Candidate / 索引纪律候选

Index discipline considers index purpose, source-to-index traceability, field-selection rationale, excluded fields, stale-index indication, conflict visibility, scope isolation, query interpretation boundary, review ownership, and index retirement condition.

The governing interpretation is that index is not memory. An index hit is not evidence. Similarity is not correctness. Retrieval rank is not approval. Index creation is not authorized. No vector database is selected and no search runtime is activated.

## 11. Compilation Log Candidate / 编译日志候选

A conceptual compilation log would identify a compilation event, source inputs, transformation description, omitted material, warnings, conflicts, gaps, candidate outputs, human owner, review status, timestamps as conceptual metadata, stop reason, and decision reference.

The compilation log is not audit authority. Log presence is not correctness. Log completion is not approval. Logging is not automatic persistence permission. No runtime logger is created.

## 12. Review Queue Candidate / 审查队列候选

The static review queue concept contains candidate identity, purpose, source scope, evidence completeness, unresolved gaps, conflicts, staleness, reviewer, review-priority rationale, allowed disposition, and forbidden automatic transition.

Allowed human dispositions are `REVIEWED`, `RETURNED`, `DEFERRED`, `REJECTED`, and `ESCALATED`. There is no automatic `APPROVED` disposition.

The review queue is not memory adoption. Queue priority is not approval priority. Review completion is not authorization. Disposition is not execution. The queue does not write memory.

## 13. Corpus Lint Candidate / 语料检查候选

The design-only lint categories are:

1. Missing provenance.
2. Broken source reference.
3. Ambiguous ownership.
4. Scope mismatch.
5. Unsupported claim.
6. Citation gap.
7. Unresolved conflict.
8. Stale candidate.
9. Duplicated candidate.
10. Forbidden interpretation.
11. Review-state inconsistency.
12. Boundary violation.

The governing interpretation is that corpus lint is not verdict. A lint pass is not approval. Lint failure does not trigger automatic repair. A lint result does not authorize deletion. Lint does not rewrite sources or mutate memory. No lint runtime is created.

## 14. Graph Insight Candidate / 图谱洞察候选

A graph insight candidate may describe a relationship hypothesis, supporting evidence, conflicting evidence, inference label, source scope, confidence note, reviewer, expiry, rejection reason, and decision reference.

The governing interpretation is that graph insight is candidate-only. A relationship hypothesis is not a graph edge. An entity mention is not graph node creation. Insight acceptance is not Memory Graph mutation. No graph database is selected, no automatic semantic edge is written, and there is no automatic Memory Graph mutation.

## 15. Human Review and Decision Boundary / 人工审查与决策边界

| Stage | Meaning | Does not mean |
|---|---|---|
| Source review | Examine source identity, scope, and fidelity | Evidence acceptance |
| Evidence review | Examine cited support and extraction context | Candidate approval |
| Candidate review | Examine claims, derivation, gaps, and conflicts | Authorization |
| Lint review | Interpret lint observations | Verdict or repair |
| Boundary review | Check governance constraints | Permission to act |
| Approval request | Ask a human authority for a decision | Approval |
| Approval | Record a scoped human decision | Automatic authorization |
| Authorization | Permit a specifically scoped later action | Automatic memory adoption |
| Memory adoption | Separately govern candidate acceptance into memory | Execution |
| Execution | Perform an independently authorized operation | A consequence of this design |

Review is not approval. An approval request is not approval. Approval is not automatic authorization. Authorization is not automatic adoption. Adoption is not execution. No model may self-authorize. No tool output may become implementation permission. No document completion may trigger persistence.

No compiler, model, registry, index, log, lint result, queue state, test, audit, branch, commit, or pull request may act as the authorization source.

## 16. External Methodology Boundary / 外部方法论边界

From `llm_wiki`, this candidate may study knowledge compilation discipline, raw source preservation, source-aware packaging, purpose organization, schema and index discipline, compilation logs, corpus lint, and review queue concepts.

`llm_wiki` must not become a dependency, adapter, runtime, implementation base, product module, approved integration, ingest engine, memory writer, storage system, authorization source, completion condition, or Civilization Core identity.

M-Flow belongs to the Associative Recall Candidate. GBrain belongs to Memory Operations / Evaluation methodology candidates. This task does not expand into those workstreams.

Methodology absorption is not runtime adoption.

## 17. Risks and Failure Modes / 风险与失败模式

No item below defines automatic repair or remediation.

| # | Risk | Detection evidence | Required human response | Prohibited automatic response |
|---:|---|---|---|---|
| 1 | Source loss: original material becomes unavailable or overwritten | Missing source reference or failed fidelity review | Stop and request source recovery or disposition | Reconstruct or replace source silently |
| 2 | Context collapse: extraction removes qualifying context | Segment/context mismatch or omitted-material warning | Review the full source scope | Expand claims automatically |
| 3 | Unsupported synthesis: derivation exceeds evidence | Claim-to-citation gap | Return, reject, or narrow the claim | Invent support |
| 4 | Citation laundering: citation proximity masks lack of support | Citation does not entail claim | Mark unsupported and escalate if needed | Treat citation count as validity |
| 5 | Scope leakage: candidate crosses purpose or audience scope | Scope mismatch evidence | Hold for explicit rescoping | Broaden purpose automatically |
| 6 | Ownership ambiguity: accountability is unclear | Missing or conflicting owner | Place on `HOLD` for owner assignment | Infer an owner |
| 7 | Stale candidate reuse | Expired source or candidate signal | Request fresh scoped review | Refresh or reuse automatically |
| 8 | Duplicate candidate proliferation | Overlapping identity and evidence sets | Compare and disposition explicitly | Merge or delete automatically |
| 9 | Conflict suppression | Missing recorded contradictory evidence | Restore conflict visibility and review | Select a winner automatically |
| 10 | Review-state confusion | Inconsistent queue and candidate states | Reconcile through human decision record | Promote state automatically |
| 11 | Registry overread | Registry entry interpreted as permission | Return to authorization boundary review | Execute intended use |
| 12 | Index overread | Rank or similarity treated as evidence | Recheck original evidence | Adopt top-ranked result |
| 13 | Lint overread | Pass treated as approval or failure as deletion order | Interpret findings manually | Approve, repair, or delete |
| 14 | Graph insight overread | Hypothesis treated as graph fact | Preserve candidate label and review | Create node or edge |
| 15 | Automatic persistence drift | Candidate appears in durable memory without authorization | Stop, preserve evidence, escalate | Continue or normalize the write |
| 16 | External methodology identity drift | External system name becomes project identity or runtime claim | Restore methodology-only boundary | Integrate or brand automatically |

## 18. Open Design Questions / 开放设计问题

1. What source snapshot granularity preserves sufficient context without implying storage design?
2. What evidence extraction granularity best supports claim-level review?
3. What transformation trace format remains readable and provenance-complete?
4. How should candidate expiry vary by source volatility and purpose?
5. How should conflicts represent incompatible scopes, dates, or authorities?
6. Who owns a purpose when multiple teams or audiences are involved?
7. How should conceptual schema evolution preserve old candidate interpretation?
8. How should index staleness become visible without activating an index?
9. What human rationale may prioritize the review queue?
10. How should lint severity express risk without becoming a verdict?
11. When should a graph insight candidate expire?
12. What evidence is necessary for a separate adoption handoff?
13. How should rejection evidence remain available without reactivating a candidate?
14. How should multi-source contradiction remain visible in summaries and claims?

An open question is not a hidden implementation task. Unresolved questions remain unresolved. Tools may not silently choose answers. Each future answer requires explicit human scope.

## 19. Allowed Future Design Handoffs / 允许的后续设计交接

Only the following design-only handoff candidates may be proposed:

1. Source and Evidence Vocabulary.
2. Compiled Candidate Vocabulary.
3. Purpose Registry Candidate Detail.
4. Schema Registry Candidate Detail.
5. Index Discipline Candidate Detail.
6. Compilation Log Candidate Detail.
7. Review Queue Candidate Detail.
8. Corpus Lint Candidate Detail.
9. Graph Insight Candidate Detail.
10. Knowledge Compilation Candidate Closure Review.

This list is not a backlog. It creates no task or branch automatically. Every item requires new explicit human scope and remains docs-only, design-only, and candidate-only. Closure review does not automatically authorize implementation.

## 20. Stop Conditions / 停止条件

Stop immediately if work would create or imply `v6.17`; create or imply a released `v7.0.0`; modify v6 runtime; start v7 implementation; create a compiler, parser, crawler, ingest path, indexer, prototype, schema file, database, vector store, knowledge graph, registry runtime, storage, memory writer, API, MCP, Connector, Agent, dependency, or adapter; activate network access; use OAuth, credentials, or secrets; automatically persist or adopt candidates; automatically mutate the Memory Graph or create a graph edge; automatically approve, authorize, execute, or self-authorize; treat lint pass as approval, schema conformance as correctness, index hit as evidence, graph insight as graph fact, `llm_wiki` as a dependency or system identity, or a design artifact as implementation permission.

Stopping means preserving compilation design evidence and returning to human review. It does not mean automatic implementation, ingestion, indexing, persistence, repair, remediation, graph mutation, deployment, or launch.

## 21. Final Candidate Statement / 最终候选声明

Knowledge Compilation Candidate remains `DESIGN-ONLY`. Candidate output is not adopted memory; compilation is not adoption. Source preservation remains mandatory, provenance remains required, and review remains human-controlled. Lint pass is not approval. Graph insight is not Memory Graph mutation.

There is no compiler implementation, ingest implementation, schema implementation, index implementation, registry implementation, storage implementation, dependency adoption, adapter activation, runtime activation, automatic durable memory write, or automatic Memory Graph mutation.

`v6.16.0` remains sealed. There is no `v6.17` and no `v7.0.0` release authorization. Explicit human scope remains required; this candidate design creates no implementation authorization.
