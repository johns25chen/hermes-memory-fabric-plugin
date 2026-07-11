# Civilization Core Associative Recall Candidate Design / 文明之核关联召回候选设计

## 1. Candidate Status / 候选状态

This document is docs-only, design-only, candidate-only, recall-methodology-study-only, and evidence-path-modeling-only. It is based on the sealed `v6.16.0` Civilization Core Stable Kernel and governed by `docs/CIVILIZATION_CORE_V7_DESIGN_ONLY_CHARTER.md`. The following source set also constrains its interpretation:

- `docs/CIVILIZATION_CORE_KNOWLEDGE_COMPILATION_CANDIDATE_DESIGN.md`
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

This candidate changes no existing document, code, test, dependency, or package version. It creates no tag: there is no `v6.17` and no `v7.0.0` release authorization. It grants no recall runtime, vector runtime, graph runtime, storage, or product implementation authorization. It creates no automatic persistence and no automatic Memory Graph mutation.

`Associative Recall Candidate` is a design workstream label, not an implemented recall engine, vector search, graph search, service, module, runtime, or product; this candidate design is not implementation permission.

## 2. Candidate Purpose / 候选目的

This candidate treats recall as source- and evidence-path candidate reconstruction. It distinguishes query, source, evidence, Episode, Facet, Entity, and Recall Candidate; establishes provenance-preserving associative recall discipline; and describes explainable Associative Evidence Paths and Path-Cost Notes without automatic decision scores. It keeps conflicts, gaps, scope, and uncertainty visible while forming a Context Reconstruction Candidate for human review and later decision.

Recall output must not enter long-term memory automatically. A semantic relation must not enter the Memory Graph automatically. Associative recall is candidate reconstruction, not memory truth.

## 3. Problem Definition / 问题定义

- Keyword match is not relevance; similarity is not correctness; high rank is not trust.
- Retrieved context is not complete context, and context reconstruction is not an original source.
- An Episode is not adopted long-term memory.
- A Facet is not a factual attribute, and a FacetPoint is not proof.
- An Entity mention is not entity confirmation.
- A Semantic Edge Candidate is not a graph edge.
- Path cost is not an approval score.
- A recall result is not authorization.
- Automatic recall can cause source loss, scope leakage, false association, conflict suppression, and stale-context reuse.
- Unreviewed association can cause drift, overreach, and false certainty.

## 4. Design Principles / 设计原则

1. Preserve source identity.
2. Preserve provenance.
3. Separate retrieval from truth.
4. Keep recall output candidate-only.
5. Make query scope explicit.
6. Make association paths explainable.
7. Make uncertainty visible.
8. Preserve conflicts and gaps.
9. Keep review human-controlled.
10. Prevent automatic persistence.
11. Prevent automatic Memory Graph mutation.
12. Preserve rejection, deferral, and expiry evidence.

Provenance outranks recall convenience. Source fidelity outranks answer fluency. Explainability outranks opaque ranking. Recall breadth does not outrank scope, and more retrieved context is not automatically better context. Lower path cost is not automatically better evidence.

## 5. Recall Scope and Query Model / 召回范围与查询模型

These are conceptual vocabulary candidates only.

| # | Object | Conceptual purpose | Minimum provenance or scope | Human review role | Non-authoritative boundary |
|---:|---|---|---|---|---|
| 1 | Recall Scope | Bound the permitted question space | owner, purpose, inclusions, exclusions, expiry | Confirm the exact boundary | Scope is not retrieval authorization |
| 2 | Recall Query | State the reviewable information request | scope reference, author, time, wording | Check faithful framing | Query is not an execution command |
| 3 | Query Intent | Explain why recall is requested | human purpose and intended use | Check purpose fit | Query intent is not execution intent |
| 4 | Query Context | Supply temporary framing | source, session scope, omissions | Check relevance and sensitivity | Query context is not durable memory |
| 5 | Query Constraint | Restrict sources, time, audience, or interpretation | constraint owner and rationale | Confirm enforceability | Constraint does not grant wider access |
| 6 | Source Boundary | Identify permitted source set | source identities, access scope, exclusions | Approve source fitness | It cannot expand automatically |
| 7 | Time Boundary | Bound valid or relevant periods | start/end or explicit open bound, owner | Check temporal fit | Time proximity is not relevance proof |
| 8 | Audience Boundary | Bound who may review or use output | audience identity and restrictions | Confirm permitted handoff | Audience naming is not disclosure permission |
| 9 | Exclusion Rule | Record material or interpretations to omit | rule owner, reason, affected scope | Verify exclusions and side effects | Exclusion is not source deletion |
| 10 | Human Owner | Identify accountable decision authority | named owner and review route | Scope, hold, defer, reject, or escalate | Ownership is not automatic authorization |

Recall scope is not retrieval authorization. Query intent is not execution intent. Query context is not durable memory. A source boundary cannot expand automatically. A missing Human Owner produces `HOLD`; tools may not infer missing scope.

## 6. Associative Recall Object Model / 关联召回对象模型

| # | Object | Conceptual purpose | Source or provenance requirement | Human review role | Non-authoritative boundary |
|---:|---|---|---|---|---|
| 1 | Episode Candidate | Frame a bounded event or interaction | source, time, scope, assembly rationale | Review framing and omissions | Episode candidate is not adopted memory |
| 2 | Facet Candidate | Name a candidate observation dimension | parent evidence and derivation | Review the dimension | Facet candidate is not verified attribute |
| 3 | FacetPoint Candidate | State a bounded observation under a Facet | source reference and extraction context | Review support and uncertainty | Facet point is not proof |
| 4 | Entity Candidate | Name a possibly referenced subject | mentions, sources, aliases, disambiguation evidence | Resolve or preserve ambiguity | Entity candidate is not entity confirmation |
| 5 | Recall Candidate | Package a possible answer context | query, scope, sources, evidence path | Assess relevance and limits | Recall is not truth or authorization |
| 6 | Semantic Edge Candidate | Express a relation hypothesis | endpoint candidates and supporting/conflicting evidence | Review the hypothesis | Semantic edge candidate is not graph edge |
| 7 | Associative Evidence Path | Explain transformations and associations | ordered references and inference labels | Inspect every path step | Associative evidence path is not authorization path |
| 8 | Path-Cost Note | Describe interpretive burdens | path identity and dimension observations | Interpret without thresholds | Path-cost note is not approval score |
| 9 | Context Reconstruction Candidate | Assemble reviewable context | source segments, candidates, rationale, gaps | Compare with sources | Context reconstruction candidate is not authoritative source |
| 10 | Provenance Trail | Preserve origin and transformation continuity | source identities, locators, transformations | Verify traceability | Provenance is not correctness certification |
| 11 | Recall Gap | Record absent or unavailable context | affected scope and expected evidence | Decide whether to hold or narrow | A gap must not be silently filled |
| 12 | Recall Conflict | Record incompatible evidence or interpretations | competing references and scopes | Review without silent resolution | A conflict must not be silently resolved |

All objects remain conceptual, candidate-only, and non-persistent.

## 7. Episode Candidate / 情境片段候选

An Episode Candidate may express a bounded event or interaction context, source scope, temporal scope, involved Entity Candidates, relevant Evidence Items, omitted context, uncertainty, conflict, candidate owner, review state, and expiry or staleness signal.

Episode is candidate-only. Episode is not durable memory and is not automatically persisted. Episode assembly is not adoption; Episode ordering is not causal proof; Episode similarity is not identity. No persistent memory may receive an automatically created Episode.

The governing shorthand is: episode candidate is not adopted memory.

## 8. Facet and FacetPoint Candidates / 切面与切面点候选

### Facet Candidate

A Facet Candidate represents a candidate observation dimension of an Episode or Entity.

### FacetPoint Candidate

A FacetPoint Candidate represents a specific candidate observation under a Facet. Each Facet or FacetPoint should preserve its source reference, extraction context, derivation description, uncertainty, conflicting evidence, scope, reviewer, and expiry.

Facet is not schema and is not a verified property. FacetPoint is not fact, and FacetPoint is not proof. Multiple FacetPoints do not automatically create a Facet truth. Neither object may cause automatic persistence or automatic graph or memory mutation.

The governing shorthand is: facet candidate is not verified attribute; facet point is not proof.

## 9. Entity Candidate and Disambiguation / 实体候选与消歧

An Entity Candidate should keep the entity mention, candidate identity, alias set, source references, disambiguation evidence, conflicting identity evidence, temporal validity, scope, reviewer, and unresolved identity state.

An entity mention is not entity confirmation. Alias similarity is not identity, and shared attributes are not identity proof. An Entity Candidate does not create a graph node. Unresolved identity remains unresolved. Entity merging requires explicit human review; there is no automatic entity merge or automatic graph node write.

The governing shorthand is: entity candidate is not entity confirmation.

## 10. Semantic Edge Candidate / 语义边候选

A Semantic Edge Candidate is a conceptual relation candidate only. It may contain a source Entity Candidate, target Entity Candidate, relation hypothesis, supporting evidence, conflicting evidence, direction note, temporal scope, confidence note, reviewer, expiry, rejection reason, and decision reference.

Semantic edge candidate is candidate-only. A relation hypothesis is not graph fact, and a semantic edge candidate is not graph edge. An accepted interpretation is not Memory Graph mutation. A confidence note is not an approval score. No graph database is selected, no edge writer is created, and no automatic semantic edge write or automatic Memory Graph mutation is permitted.

## 11. Associative Evidence Path / 关联证据路径

The static path structure is:

`query scope → source boundary → evidence item → episode candidate → facet or entity candidate → semantic relation hypothesis → recall candidate`

Each path should preserve path identity, query scope, source references, evidence sequence, transformation notes, inference labels, conflicts, gaps, excluded alternatives, reviewer, expiry, and decision reference.

An evidence path is not an execution path or authorization path. Path existence is not correctness. A longer path is not automatically weaker; a shorter path is not automatically stronger. Repeated evidence is not independent evidence. No path may write memory or graph state.

## 12. Path-Cost Recall Candidate / 路径成本召回候选

A Path-Cost Note may describe exactly these explanatory dimensions:

1. Provenance distance.
2. Inference count.
3. Unresolved conflict count.
4. Scope mismatch risk.
5. Temporal staleness.
6. Source authority uncertainty.
7. Omitted-context risk.
8. Identity ambiguity.
9. Duplication risk.
10. Review incompleteness.

Path cost is explanatory metadata, not a truth score, not a confidence score by default, and not an approval score. Lower cost is not automatic correctness; higher cost is not automatic rejection. No scoring or ranking engine is implemented. No threshold may auto-approve or auto-reject. All interpretation remains human-controlled.

## 13. Context Reconstruction Candidate / 上下文重建候选

A Context Reconstruction Candidate may contain recalled source segments, Episode Candidates, Facet Candidates, Entity Candidates, supporting evidence, conflicting evidence, missing context, temporal ordering, a scope note, uncertainty note, reconstruction rationale, reviewer, and expiry.

Context reconstruction is candidate-only. Reconstruction is not original context or an authoritative source. Fluent reconstruction is not correctness, and chronological order is not causal proof. Missing context must remain visible. Reconstruction must neither overwrite sources nor persist automatically.

## 14. Conceptual Recall Lifecycle / 概念召回生命周期

The static lifecycle is:

`explicit human scope → query framing → source boundary review → evidence selection → episode candidate assembly → facet and entity review → associative path construction → path-cost annotation → context reconstruction candidate → boundary review → human review → decision record`

No step may be skipped automatically. Query framing cannot expand scope automatically. Source boundary review precedes a Recall Candidate. Evidence selection cannot overwrite a source. Entity ambiguity cannot be resolved automatically. Path construction cannot create a graph edge. Path-cost annotation cannot rank a candidate into approval. Context reconstruction cannot persist automatically. Boundary review cannot authorize automatically; human review cannot execute automatically; and a decision record cannot write long-term memory automatically.

Stopped work preserves evidence. A rejected Recall Candidate remains rejected; a deferred candidate remains deferred. Expired scope requires new explicit human scope.

## 15. Human Review and Decision Boundary / 人工审查与决策边界

| Stage | Meaning | Does not mean |
|---|---|---|
| Query review | Examine scope, intent, framing, and owner | Retrieval authorization |
| Source boundary review | Examine permitted sources | Automatic source expansion |
| Evidence review | Examine support and extraction context | Truth certification |
| Episode review | Examine contextual assembly | Memory adoption |
| Facet review | Examine dimensions and observations | Property verification |
| Entity disambiguation review | Examine identity evidence | Automatic merge |
| Semantic edge candidate review | Examine a relation hypothesis | Graph adoption |
| Path review | Examine association and provenance continuity | Authorization |
| Reconstruction review | Compare reconstruction with sources and gaps | Source replacement |
| Approval request | Ask for a bounded human decision | Approval |
| Approval | Record a scoped human decision | Automatic authorization |
| Authorization | Permit a separately scoped later action | Automatic memory or graph adoption |
| Memory adoption | Separately govern durable memory acceptance | Graph adoption or execution |
| Graph adoption | Separately govern graph acceptance | Memory adoption or execution |
| Execution | Perform an independently authorized operation | A consequence of this design |

Review is not approval. An approval request is not approval. Approval is not automatic authorization. Authorization is not automatic memory adoption or graph adoption. Adoption is not execution. No model may self-authorize; no tool output may become implementation permission; no document completion may trigger persistence; and no recall result may trigger Memory Graph mutation.

No recall engine, model, vector rank, graph path, semantic edge candidate, path-cost note, reconstruction, test, audit, branch, commit, or pull request may act as the authorization source.

## 16. External Methodology Boundary / 外部方法论边界

M-Flow may be studied only as a methodology candidate. Study may cover Episode, Facet, FacetPoint, Entity, associative recall concepts, path-cost recall concepts, semantic relation hypotheses, context reconstruction concepts, explainable evidence paths, and scoped recall design.

M-Flow must not become a dependency, adapter, runtime, implementation base, product module, approved integration, vector engine, graph engine, memory writer, storage system, authorization source, completion condition, or Civilization Core identity.

`llm_wiki` belongs to the Knowledge Compilation Candidate. GBrain belongs to Memory Operations / Evaluation methodology candidates. This task does not expand into another workstream.

Methodology absorption is not runtime adoption.

## 17. Risks and Failure Modes / 风险与失败模式

No item below defines automatic repair, remediation, merge, edge creation, candidate adoption, deletion, or persistence.

| # | Risk | Risk description | Detection evidence | Required human response | Prohibited automatic response |
|---:|---|---|---|---|---|
| 1 | False association | Unrelated items are presented as connected | Unsupported path step or weak scope fit | Hold and inspect sources and inference | Accept or strengthen the association |
| 2 | Source loss | Origin or locator is absent | Broken provenance trail | Stop and request source recovery | Reconstruct or replace the source |
| 3 | Context collapse | Qualifying context is omitted | Segment differs materially from surrounding source | Restore visibility and narrow interpretation | Expand or smooth the claim |
| 4 | Scope leakage | Recall crosses source, time, audience, or purpose scope | Boundary mismatch | Hold for explicit human rescoping | Expand scope |
| 5 | Entity collision | Distinct entities are treated as one | Conflicting identity evidence | Preserve separate candidates | Merge entities |
| 6 | Alias overmerge | Similar aliases imply identity | Alias-only linkage | Request disambiguation review | Merge aliases or nodes |
| 7 | Temporal confusion | Events or claims are assigned the wrong time relation | Conflicting dates or ordering evidence | Preserve uncertainty and review chronology | Infer causality or reorder facts |
| 8 | Stale recall reuse | Expired material is reused as current | Expiry or newer conflicting source | Require fresh scope and review | Refresh or reuse silently |
| 9 | Conflict suppression | Contradictory evidence disappears | Missing competing reference | Restore conflict visibility | Select a winner |
| 10 | Evidence duplication | Repeated evidence appears independent | Shared source or derivation identity | Mark dependence and reassess path | Increase weight or rank |
| 11 | Rank overread | Retrieval order is treated as authority | Rank cited without source review | Return to evidence review | Adopt the top result |
| 12 | Path-cost overread | Cost is treated as truth or approval | Threshold or score used dispositively | Interpret dimensions manually | Auto-approve or auto-reject |
| 13 | Semantic edge overread | Relation hypothesis is treated as graph fact | Candidate label omitted | Restore candidate state and review | Create or update an edge |
| 14 | Reconstruction hallucination | Fluent reconstruction adds unsupported detail | Claim-to-source gap | Mark unsupported, return, or reject | Fill gaps or persist text |
| 15 | Automatic persistence drift | Candidate appears in durable memory | Write evidence without authorization | Stop, preserve evidence, escalate | Normalize or continue the write |
| 16 | External methodology identity drift | M-Flow becomes system identity or implementation | Dependency, adapter, runtime, or branding claim | Restore methodology-only boundary | Integrate, activate, or rebrand |

## 18. Open Design Questions / 开放设计问题

1. What Episode granularity preserves context without implying storage units?
2. Where should a Facet boundary begin and end?
3. What FacetPoint granularity supports review without implying facts?
4. What evidence should inform Entity disambiguation without creating an automatic threshold?
5. How should aliases be represented while preventing overmerge?
6. How should semantic relation direction remain explicit and contestable?
7. How should evidence-path branching display alternatives and shared evidence?
8. Which Path-Cost dimensions are useful without becoming a composite score?
9. How should incompatible conflicts and scoped disagreements be represented?
10. How should temporal ordering distinguish sequence from causality?
11. How should staleness and expiry vary across source types and scopes?
12. How should reconstruction completeness be described without fluency overread?
13. Who owns Query Scope when several human stakeholders are involved?
14. How may review queues be prioritized without implying approval priority?
15. How should rejection evidence remain visible without reactivating a candidate?
16. How should multi-source contradiction remain visible in a reconstruction?

An open question is not a hidden implementation task. Unresolved questions remain unresolved. Tools may not silently choose answers, and no default technology selection may be inferred. Each future answer requires explicit human scope.

## 19. Allowed Future Design Handoffs / 允许的后续设计交接

Only these design-only handoff candidates may be proposed:

1. Recall Scope and Query Vocabulary.
2. Episode Candidate Vocabulary.
3. Facet and FacetPoint Candidate Vocabulary.
4. Entity Candidate and Disambiguation Detail.
5. Semantic Edge Candidate Detail.
6. Associative Evidence Path Detail.
7. Path-Cost Note Detail.
8. Context Reconstruction Candidate Detail.
9. Associative Recall Risk Register.
10. Associative Recall Candidate Closure Review.

This list is not a backlog and creates no task or branch automatically. Every item requires new explicit human scope and remains docs-only, design-only, and candidate-only. Closure review does not automatically authorize implementation, vector or graph runtime, persistence, or Memory Graph mutation.

## 20. Stop Conditions / 停止条件

Stop immediately if work would create or imply `v6.17`; create or imply a released `v7.0.0`; modify v6 runtime; start v7 implementation; create a recall engine, embedding pipeline, reranker, vector search, graph traversal, graph query runtime, semantic edge writer, prototype, schema file, database, vector store, graph database, persistent cache, storage, memory writer, API, MCP, Connector, Agent, dependency, or adapter; activate network access; use OAuth, credentials, or secrets; automatically persist a Recall Candidate; automatically adopt an Episode, Facet, Entity, or reconstruction; automatically create a graph node or edge; automatically modify the Memory Graph; automatically approve, authorize, execute, or self-authorize; treat similarity as correctness, ranking as authority, path cost as an approval score, a Semantic Edge Candidate as graph fact, a Context Reconstruction Candidate as an authoritative source, M-Flow as a dependency or system identity, or a design artifact as implementation permission.

Stopping means preserving associative recall design evidence and returning to human review. It does not mean automatic implementation, retrieval, ranking, reconstruction, persistence, repair, remediation, graph mutation, deployment, or launch.

## 21. Final Candidate Statement / 最终候选声明

Associative Recall Candidate remains `DESIGN-ONLY`. Recall output is candidate-only, and associative recall is not memory truth. Episode candidate is not adopted memory. Facet candidate is not verified attribute. FacetPoint candidate is not proof. Entity candidate is not entity confirmation. Semantic edge candidate is not graph edge. The governing boundaries are: associative evidence path is not authorization path; path-cost note is not approval score; context reconstruction candidate is not authoritative source.

Provenance remains required; conflicts and gaps remain visible; review remains human-controlled. There is no recall engine, embedding, or reranking implementation; no vector or graph runtime activation; no storage implementation; no dependency adoption; no adapter activation; no automatic durable memory write; and no automatic Memory Graph mutation.

`v6.16.0` remains sealed. There is no `v6.17` and no `v7.0.0` release authorization. Explicit human scope remains required; this candidate design creates no implementation authorization.
