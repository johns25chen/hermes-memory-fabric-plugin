# Civilization Core P4 Decision Record Candidate / 文明之核 P4 决策记录候选

## 1. Candidate Status

This is a docs-only P4 Decision Record Candidate.

This is a candidate record only. It is not the final decision record.

This candidate is based on the sealed `v6.16.0` Civilization Core Stable Kernel. The v6 line remains sealed. There is no `v6.17`. Post-terminal docs do not create tags.

This candidate is based on:

- `docs/CIVILIZATION_CORE_P4_DECISION_GATE_CHECKLIST.md`
- `docs/CIVILIZATION_CORE_P4_DISCUSSION_SCOPE_CANDIDATE.md`
- `docs/CIVILIZATION_CORE_P4_PROPOSAL_SCOPE_CANDIDATE.md`
- `docs/CIVILIZATION_CORE_P4_PROPOSAL_CANDIDATE.md`

It uses the Memory Systems Landscape Report and downstream memory-methodology candidate docs as local methodology evidence only.

This document is not P4 start. It is not P4 approval. It is not P4 authorization. It is not P4 implementation authorization.

This document is not v7 start. It is not v7 implementation authorization.

This document is not product, MVP, or deployment authorization.

This document creates no code, tests, runtime capability, dependencies, adapters, API/MCP operation surface, connector operation, Memory Graph behavior, durable writer, or authorization/execution semantics.

This document creates no version change, no tag, and no `v6.17`.

## 2. Decision Record Candidate Purpose

This document gives a safe candidate structure for a possible future human decision record.

It does not make the decision. It does not select approval. It does not select implementation.

It records the current safe default as paused / not approved / not authorized.

It gives reviewers a structured object to reject, defer, narrow, or convert later only by explicit human instruction.

It preserves sealed `v6.16.0`. It preserves human sovereignty. It prevents a candidate record from being misread as a phase transition, product decision, connector decision, graph decision, durable-memory decision, or implementation decision.

## 3. Current Candidate Decision Summary

| Field | Candidate value | Boundary |
| --- | --- | --- |
| Subject | Civilization Core / Subspace Memory System P4 decision-record candidate | Candidate structure only; not a final decision. |
| Repository state | Docs-only candidate file may exist for review | No existing file, source, test, script, config, README, package, dependency, or tag change is authorized. |
| Version state | `6.16.0` remains the reviewed package version | No version change and no `v6.17`. |
| Tag state | No post-terminal tag is created | Merge or docs maturity does not create a tag. |
| P4 state | P4 remains not started | Candidate record is not phase transition. |
| P4 approval state | P4 remains not approved | Candidate record does not select yes. |
| P4 implementation state | P4 implementation remains not authorized | No implementation plan follows. |
| v7 state | v7 remains not started | v7 mentions remain boundary context only. |
| product/MVP/deployment state | Product/MVP/deployment remains not authorized | Roadmap and explanation docs remain non-build artifacts. |
| API/MCP/connector state | API/MCP/connector operation remains not authorized | Connector taxonomy remains vocabulary only. |
| Memory Graph state | Memory Graph behavior and mutation remain not authorized | Ontology mapping remains vocabulary only. |
| durable writer state | Durable memory writing remains not authorized | No writer, persistence, promotion, or automatic memory action. |
| external methodology candidate state | External methodology candidates remain local docs evidence only | No dependency, adapter, connector, import, or product adoption. |
| selected default outcome | Remain paused | Default remains no / not approved / not authorized. |

## 4. Candidate Decision Question

Should Civilization Core move from P4 proposal-candidate review into a future explicitly human-approved P4 phase decision?

This candidate does not answer yes.

This candidate does not approve yes.

This candidate records that the default answer remains no / paused.

Any yes requires a separate explicit human approval record.

Any yes still does not automatically authorize implementation unless explicitly stated later.

## 5. Decision Inputs Reviewed

| Input family | Documents / evidence | How used | What must not be inferred |
| --- | --- | --- | --- |
| P4 gate chain | P4 Decision Gate Checklist, P4 Discussion Scope Candidate, P4 Proposal Scope Candidate, P4 Proposal Candidate | Provides the candidate-review sequence and non-authorization boundaries. | Do not infer P4 start, approval, authorization, or implementation. |
| release / closure | Release Book, Version Chronicle, Terminal Closure Pack, git tags | Grounds sealed `v6.16.0`, v6 closure, no `v6.17`, and no post-terminal tag. | Do not infer a new release or tag. |
| boundary constitution | Boundary Constitution | Grounds human authority, memory boundary, evidence boundary, execution boundary, and post-terminal boundary. | Do not infer autonomous authority or action permission. |
| handoff / operator guidance | Handoff Package, Operator Guide where applicable | Grounds receiver/operator safety and future-work caution. | Do not infer operator tooling or active execution. |
| Memory Systems Landscape Report | Landscape Report | Supplies the locked external methodology candidate pool and borrowable essence map. | Do not infer current live ranking, adoption, import, dependency, adapter, connector, or product claim. |
| memory evaluation | Memory Evaluation Candidates | Supplies evaluation vocabulary and evidence dimensions. | Do not infer benchmark runner, score, pass rate, or evaluation authority. |
| temporal validity | Temporal Validity Model | Supplies staleness, validity, conflict, and supersession vocabulary. | Do not infer temporal engine, automatic correction, or graph behavior. |
| lifecycle taxonomy | Memory Lifecycle Taxonomy | Supplies candidate/review/reject/stale lifecycle vocabulary. | Do not infer durable writer, lifecycle automation, or approval engine. |
| failed-attempt / do-not-retry | Failed Attempt Memory / Do-Not-Retry Rules | Supplies failure-record and retry-risk vocabulary. | Do not infer automatic blocklist, coding-agent hook, or execution rule. |
| explainable recall | Explainable Recall Trace Template | Supplies evidence-path and recall-reason vocabulary. | Do not infer recall engine, trace persistence, retrieval, or ranking. |
| connector governance | Connector Governance Taxonomy | Supplies source, connector, sync, permission, and trust vocabulary. | Do not infer connector logic, API/MCP surface, adapter, storage, sync, or action. |
| ontology mapping | Memory Ontology Mapping | Supplies object and relationship vocabulary. | Do not infer schema, graph edge, graph database behavior, Memory Graph mutation, or traversal. |
| external product explanation | External Product Explanation Candidate | Supplies safe explanation wording. | Do not infer website final copy, sales copy, launch, MVP, pricing, or product availability. |
| productization roadmap | Productization Roadmap | Supplies roadmap-only productization context. | Do not infer product requirements, build authorization, deployment, Operator Console, UI, or demo app. |
| v7 pre-design | v7 Pre-Design Decision | Supplies pre-design context only. | Do not infer v7 start, v7 branch, v7 technical design, or v7 implementation authorization. |
| document index / overview / FAQ / audit | Document Index, One-Page Overview, FAQ, Comprehensive Audit Report | Supplies reader path, project identity, FAQ boundaries, and audit warnings. | Do not infer capability, product readiness, or implementation readiness. |
| local git state | Local branch, log, tags, status | Grounds branch, HEAD, prior merged docs, and tag surface. | Do not infer unverified remote state beyond local git evidence. |
| package version state | `pyproject.toml` | Confirms reviewed package version remains `6.16.0`. | Do not infer package release or version change. |
| tag state | Local `git tag` and `git tag --points-at HEAD` | Confirms no tag at current post-terminal HEAD during local verification. | Do not infer tag creation from docs. |

## 6. Locked External Methodology Candidate Pool

The candidate pool remains locked to the already documented local pool.

Mature/popular:

- mem0
- Letta / MemGPT
- LangGraph
- LlamaIndex
- AnythingLLM
- Quivr
- Khoj
- Graphiti / Zep
- Cognee
- Haystack

Appendix:

- Onyx

Rising/new-paradigm:

- MemOS / MemTensor
- MemoryOS / BAI-LAB
- OpenMemory
- Projectmem
- EverOS
- agentmemory
- LangMem
- Awesome-AI-Memory
- Awesome-Memory-for-Agents
- Agent Memory Techniques

There is no live re-ranking, no new online research, no expansion, no import, no dependency, no adapter, no connector adoption, no MCP/API adoption, no Memory Graph mutation, and no productization.

These external candidates are methodology evidence only.

## 7. Borrowable Essence Already Converted to Local Candidate Docs

| External essence | Source examples | Local candidate doc | Boundary |
| --- | --- | --- | --- |
| Memory Evaluation | mem0, MemoryOS, Projectmem, Awesome-AI-Memory, Agent Memory Techniques | Memory Evaluation Candidates | Docs-only evaluation vocabulary, not runner or score authority. |
| Temporal Validity | Graphiti / Zep, mem0, LangMem, Awesome-Memory-for-Agents | Temporal Validity Model | Docs-only validity vocabulary, not temporal engine or graph behavior. |
| Memory Lifecycle | MemOS, MemoryOS, agentmemory, LangMem, Projectmem | Memory Lifecycle Taxonomy | Docs-only state vocabulary, not durable writer or lifecycle automation. |
| Failed Attempt Memory / Do-Not-Retry | Projectmem, agentmemory, Agent Memory Techniques | Failed Attempt Memory / Do-Not-Retry Rules | Docs-only failure and retry-risk vocabulary, not automatic blocking. |
| Explainable Recall | OpenMemory, Graphiti / Zep, Cognee, LlamaIndex | Explainable Recall Trace Template | Docs-only trace vocabulary, not recall engine or trace persistence. |
| Connector Governance | LlamaIndex, Onyx, Haystack, Khoj, Cognee | Connector Governance Taxonomy | Docs-only connector/source vocabulary, not API/MCP or connector operation. |
| Ontology / Taxonomy | Cognee, Graphiti / Zep, Awesome-Memory-for-Agents, Awesome-AI-Memory | Memory Ontology Mapping | Docs-only vocabulary, not schema, graph edge, or Memory Graph mutation. |
| External Product Explanation | AnythingLLM, Quivr, Khoj, Onyx, EverOS | External Product Explanation Candidate | Candidate wording only, not product claim or launch copy. |
| Product Mental Model | AnythingLLM, Quivr, Khoj, Onyx, Letta | Productization Roadmap and External Product Explanation Candidate | Roadmap/explanation only, not MVP or deployment. |
| Markdown Source of Truth | EverOS, local Civilization Core docs, llm_wiki as already documented locally | Document Index and local docs stack | Diffable docs only, not durable memory writer. |
| Human Review Gate | LangGraph, Haystack, MemoryOS, local governance docs | P4 Decision Gate Checklist | Review structure only, not approval. |
| Evidence / Claim / Inference separation | Local governance docs plus landscape methodology | P4 chain, Explainable Recall Trace Template, Memory Ontology Mapping | Review discipline only, not authorization or capability. |

These are already docs-only candidate transformations. They are not implementation.

## 8. Candidate Decision Preconditions

The following preconditions must hold before any future human decision-record review:

- A human explicitly requests decision-record review.
- Main branch is clean.
- Version remains `6.16.0` unless separately approved.
- `v6.16.0` remains sealed.
- No `v6.17` continuation exists.
- No post-terminal tag is created.
- No `uv.lock` exists.
- No source/test/script/config drift exists.
- All required P4 chain docs exist.
- All required methodology docs exist.
- No active runtime capability claim exists.
- No active Star-Source Memory runtime claim exists.
- No active Layer 15 runtime claim exists.
- No active external dependency/adapter/connector claim exists.
- No active Memory Graph mutation claim exists.
- No autonomous authority/personhood/life/legal/religious claim exists.
- An explicit human record states what is and is not authorized.

## 9. Candidate Evidence Findings

| Evidence item | Candidate finding | Confidence | Boundary |
| --- | --- | --- | --- |
| P4 Decision Gate Checklist exists | Present in local docs during candidate drafting. | High for local repo state. | Existence is not P4 start. |
| P4 Discussion Scope Candidate exists | Present in local docs during candidate drafting. | High for local repo state. | Existence is not P4 approval. |
| P4 Proposal Scope Candidate exists | Present in local docs during candidate drafting. | High for local repo state. | Existence is not implementation authorization. |
| P4 Proposal Candidate exists | Present in local docs during candidate drafting. | High for local repo state. | Proposal candidate is not decision. |
| Landscape Report exists | Present in local docs during candidate drafting. | High for local repo state. | Landscape is methodology evidence only. |
| memory evaluation candidate exists | Present in local docs during candidate drafting. | High for local repo state. | Evaluation vocabulary is not runner or score. |
| temporal validity model exists | Present in local docs during candidate drafting. | High for local repo state. | Temporal vocabulary is not engine behavior. |
| lifecycle taxonomy exists | Present in local docs during candidate drafting. | High for local repo state. | Lifecycle labels are not durable writes. |
| failed-attempt rules exist | Present in local docs during candidate drafting. | High for local repo state. | Rules are not automatic execution constraints. |
| explainable recall template exists | Present in local docs during candidate drafting. | High for local repo state. | Template is not recall implementation. |
| connector governance taxonomy exists | Present in local docs during candidate drafting. | High for local repo state. | Taxonomy is not connector operation. |
| memory ontology mapping exists | Present in local docs during candidate drafting. | High for local repo state. | Mapping is not schema or graph mutation. |
| productization roadmap exists | Present in local docs during candidate drafting. | High for local repo state. | Roadmap is not product authorization. |
| v7 pre-design decision exists | Present in local docs during candidate drafting. | High for local repo state. | Pre-design is not v7 start. |
| boundary constitution exists | Present in local docs during candidate drafting. | High for local repo state. | Constitution does not grant autonomous authority. |
| release book exists | Present in local docs during candidate drafting. | High for local repo state. | Release book does not tag post-terminal docs. |
| version remains 6.16.0 | `pyproject.toml` local verification shows `version = "6.16.0"`. | High for local repo state. | No package version change. |
| v6.16.0 remains sealed | Local docs and git tags ground sealed v6.16.0. | High for local repo docs and git state. | No `v6.17`. |
| no P4 start record exists | No local P4 start record was identified in the inspected P4 chain. | Conservative; requires local verification before future decision. | Absence is not approval. |
| no P4 approval record exists | No local P4 approval record was identified in the inspected P4 chain. | Conservative; requires local verification before future decision. | Absence keeps default paused. |
| no P4 implementation authorization exists | No local P4 implementation authorization was identified in the inspected P4 chain. | Conservative; requires local verification before future decision. | No implementation authority follows. |

## 10. Candidate Decision Outcome

| Outcome field | Candidate value | Meaning |
| --- | --- | --- |
| P4 start | not approved | P4 remains not started. |
| P4 approval | not approved | No yes decision is selected. |
| P4 implementation | not authorized | No implementation plan or work follows. |
| v7 | not started | v7 remains context only. |
| product/MVP/deployment | not authorized | Roadmap/explanation docs remain non-build artifacts. |
| API/MCP/connector | not authorized | No operation surface or connector action follows. |
| Memory Graph behavior/mutation | not authorized | No graph behavior, edge, traversal, or mutation follows. |
| durable memory writing | not authorized | No durable writer or automatic memory writing follows. |
| code/test/source/config changes | not authorized | Docs-only candidate record surface only. |
| package version/tag | not authorized | No package version change and no tag. |
| selected candidate outcome | remain paused | Default remains no / not approved / not authorized. |
| allowed next step | only separately approved docs-only clarification or decision-record revision | No automatic next action. |

## 11. Candidate Allowed Outcomes

| Outcome | Meaning | What it allows | What it does not allow |
| --- | --- | --- | --- |
| fail | Candidate is rejected. | Stop or record rejection in a separately approved docs-only context. | P4 start, approval, implementation, v7, productization, API/MCP/connector, Memory Graph, or code change. |
| defer | Candidate is neither accepted nor rejected. | Pause and request later human review. | Automatic progression or implementation. |
| remain paused | Default outcome continues. | Keep P4 not started and not approved. | Any phase transition or build work. |
| request docs-only clarification | Human asks for narrower wording. | Edit docs only under explicit scope. | Runtime capability, dependency, adapter, connector, or source/test/config change. |
| request decision-record revision | Human asks for revised candidate record. | Revise this candidate or a future approved docs-only record under explicit scope. | Final decision or implementation without separate approval. |
| request stronger human decision statement | Human asks for clearer approval/refusal language. | Produce a decision wording candidate for review. | Treat wording draft as approval. |
| approve discussion-only continuation | Human permits discussion-only continuation. | Continue human discussion or docs-only review. | P4 start, implementation, productization, connectors, graph work, or durable memory writing. |
| approve future decision-record revision only | Human permits a later revision. | Draft or revise decision-record text only. | Implementation, v7, product, API/MCP/connector, Memory Graph, dependency, adapter, or tag. |

## 12. Candidate Disallowed Outcomes

| Disallowed outcome | Why disallowed | Required stop response |
| --- | --- | --- |
| P4 started | Candidate record is not phase transition. | Stop; require separate explicit human approval. |
| P4 approved | Candidate record does not select yes. | Stop; require separate final decision record. |
| P4 implementation authorized | Candidate record has no build authority. | Stop; require separate explicit implementation authorization. |
| v7 started | v7 remains not started. | Stop; require separate explicit human approval. |
| v7 implementation authorized | v7 implementation is outside this candidate. | Stop; require separate explicit approval. |
| product/MVP/deployment authorized | Productization remains roadmap-only. | Stop; require separate product decision. |
| API/MCP/connector operation authorized | Connector taxonomy is not operation. | Stop; require separate connector/API/MCP approval. |
| external project integration/adoption authorized | External candidates are methodology evidence only. | Stop; require separate docs-only review and human approval. |
| dependency/adapter authorized | This candidate adds no dependency or adapter. | Stop; require separate explicit approval. |
| Memory Graph behavior/mutation authorized | Ontology mapping is not graph behavior. | Stop; require separate graph decision. |
| durable writer authorized | No durable memory writing is permitted. | Stop; require separate durable-memory decision. |
| code/tests authorized | This is docs-only. | Stop; require separate implementation approval. |
| package version/tag change authorized | Version and tags remain unchanged. | Stop; require separate release approval. |
| autonomous authority granted | Human sovereignty remains required. | Stop; reject autonomous-authority interpretation. |

## 13. P4 Boundary

P4 remains not started.

The P4 Proposal Candidate does not equal a P4 decision.

This decision record candidate does not equal a P4 decision.

Merge is not P4 start. Checklist completeness is not P4 start. Documentation maturity is not P4 start.

Future P4 start requires separate explicit human approval.

P4 implementation requires separate explicit human approval beyond P4 start.

## 14. Productization Boundary

Productization remains roadmap-only.

External product explanation remains candidate wording only.

There is no product requirements document, no MVP, no launch, no pricing, no sales copy, no website final copy, no customer claim, no install path, no deployment, no Operator Console, no product UI, and no demo app.

Any productization work requires separate explicit human approval later.

## 15. v7 Boundary

v7 remains not started.

v7 pre-design remains context only.

This decision record candidate does not create a v7 bridge.

There is no v7 branch, no v7 roadmap execution, no v7 technical design, and no v7 implementation authorization.

Any v7 work requires separate explicit human approval later.

## 16. API / MCP / Connector Boundary

Connector governance remains taxonomy-only.

API response is observation only.

MCP mention is not tool creation.

There is no API/MCP operation surface, no connector logic/storage/sync, no source ingestion, no polling, and no freshness checks.

Permission to read is not permission to act.

No connector proposal is created here.

Any connector/API/MCP work requires separate explicit human approval later.

## 17. External Methodology Absorption Boundary

External candidates are methodology evidence only.

No external project is adopted. No external project becomes system identity. No external repo is copied. No package/dependency is added. No adapter is added. No connector is activated.

No benchmark score is imported as proof.

No live ranking is preserved as current truth.

No external claim becomes product claim.

Any future absorption requires separate docs-only review first and separate human approval later.

## 18. Ontology / Memory Graph Boundary

Ontology mapping remains vocabulary-only.

Object type is not schema.

Relationship label is not graph edge.

Mapping is not graph mutation.

There is no graph database behavior, no Memory Graph behavior, no Memory Graph mutation, no graph traversal, no relationship inference, no automatic classification, no automatic mapping, no automatic promotion, and no automatic memory writing.

Any graph work requires separate explicit human approval later.

## 19. Evaluation / Benchmark Boundary

Evaluation remains candidate vocabulary only.

Benchmark reference is not benchmark proof.

There is no benchmark runner, no evaluation runner, no scores, no pass rates, no benchmark superiority, and no performance guarantee.

Any benchmark/evaluation implementation requires separate explicit human approval later.

## 20. Human Sovereignty Boundary

Human review is required before any phase transition.

Human review is not automatic approval.

Merge is not approval. Checklist is not approval. Proposal candidate is not approval. Decision record candidate is not approval.

The system cannot self-authorize.

There is no autonomous authority and no personhood/life/awakening/legal/religious claim.

Explicit human confirmation is required for any later change.

## 21. Evidence / Claim / Inference Boundary

Evidence must be separated from claims.

Claims must be separated from inferences.

Inference cannot become approval.

Documentation completeness cannot become capability.

Roadmap cannot become build authorization.

Proposal cannot become implementation.

Decision record candidate cannot become decision.

Unresolved uncertainty requires defer or fail.

Unresolved conflict requires defer or fail.

## 22. Decision Record Template

```text
decision record date:
reviewer / participant:
branch / commit reviewed:
package version reviewed:
docs reviewed:
candidate under review:
decision question:
evidence reviewed:
claims discussed:
inferences discussed:
unresolved blockers:
unresolved conflicts:
unresolved uncertainties:
selected outcome:
explicitly authorized next action:
explicitly prohibited next actions:

statement: "This decision record does / does not start P4"
statement: "This decision record does / does not approve P4"
statement: "This decision record does / does not authorize P4 implementation"
statement: "This decision record does / does not start v7"
statement: "This decision record does / does not authorize product/MVP/deployment"
statement: "This decision record does / does not authorize API/MCP/connector operation"
statement: "This decision record does / does not authorize external project adoption"
statement: "This decision record does / does not authorize Memory Graph behavior or mutation"
statement: "This decision record does / does not authorize durable memory writing"
statement: "This decision record does / does not authorize code/test/source/config changes"
statement: "This decision record does / does not authorize package version or tag changes"

human approval / note:
```

## 23. Candidate Future Sequence

This document creates no automatic next step.

If rejected, stop.

If deferred, only docs-only clarification may be requested later.

If revised, only the same docs-only decision-record-candidate file may be revised under explicit scope.

If a future final decision record is requested, it requires separate explicit human permission.

A future final decision record still does not authorize implementation unless explicitly stated.

No implementation sequence is authorized here.

No v7 sequence is authorized here.

No productization sequence is authorized here.

No API/MCP/connector sequence is authorized here.

No Memory Graph sequence is authorized here.

## 24. Non-Authorization Rules

- Decision record candidate is not P4 start.
- Decision record candidate is not P4 approval.
- Decision record candidate is not P4 authorization.
- Decision record candidate is not P4 implementation plan.
- Decision record candidate outcome is not automatic approval.
- Merge is not phase transition.
- P4 mention is not phase transition.
- v7 mention is not v7 start.
- Productization mention is not productization authorization.
- API/MCP mention is not operation surface.
- Connector mention is not connector adoption.
- External candidate mention is not external adoption.
- Ontology mention is not graph implementation.
- Memory Graph mention is not Memory Graph mutation.
- Evaluation mention is not benchmark runner.
- Benchmark mention is not benchmark proof.
- Human review readiness is not approval.
- Sealed kernel is not active commercial product.
- Documentation maturity is not runtime capability.
- Repository context is not full system identity.
- Decision record candidate is not authorization/execution permission.

## 25. Prohibited Implementation Rules

- Do not start P4 from this document.
- Do not approve P4 from this document.
- Do not authorize P4 from this document.
- Do not implement P4 from this document.
- Do not start v7.
- Do not build MVP.
- Do not implement product UI.
- Do not implement Operator Console.
- Do not implement demo app.
- Do not implement deployment.
- Do not implement packaging.
- Do not implement install path.
- Do not publish website final copy.
- Do not publish sales copy.
- Do not create pricing.
- Do not claim product availability.
- Do not claim customer deployment.
- Do not create API/MCP operation surface.
- Do not implement connector logic.
- Do not implement connector storage.
- Do not implement connector sync.
- Do not implement adapter behavior.
- Do not adopt external project.
- Do not add dependency.
- Do not add adapter.
- Do not implement ontology schema.
- Do not implement graph database behavior.
- Do not implement Memory Graph behavior.
- Do not mutate Memory Graph.
- Do not implement graph traversal.
- Do not implement relationship inference.
- Do not implement automatic classification.
- Do not implement automatic mapping.
- Do not implement automatic promotion.
- Do not implement automatic memory writing.
- Do not implement durable writer.
- Do not implement recall engine.
- Do not implement evaluation runner.
- Do not implement benchmark runner.
- Do not create runtime-activation bridge.
- Do not add authorization/execution semantics.
- Do not tag post-terminal docs.
- Do not change package version.
- Do not change existing docs.
- Do not change README.
- Do not change source, tests, scripts, or config.

## 26. Stop Conditions

- If decision record candidate is treated as P4 start, stop.
- If decision record candidate is treated as P4 approval, stop.
- If decision record candidate is treated as P4 authorization, stop.
- If decision record candidate is treated as P4 implementation plan, stop.
- If decision record candidate is treated as final decision, stop.
- If decision record candidate is treated as v7 start, stop.
- If decision record candidate turns into product plan, stop.
- If decision record candidate turns into MVP, stop.
- If decision record candidate turns into product deployment, stop.
- If decision record candidate turns into Operator Console, stop.
- If decision record candidate turns into product UI, stop.
- If decision record candidate turns into demo app, stop.
- If decision record candidate turns into install guide, stop.
- If decision record candidate turns into API/MCP operation surface, stop.
- If decision record candidate turns into connector implementation, stop.
- If decision record candidate turns into external project adoption, stop.
- If decision record candidate turns into Memory Graph behavior or mutation, stop.
- If decision record candidate turns into ontology schema or graph database behavior, stop.
- If decision record candidate turns into benchmark runner or evaluation runner, stop.
- If decision record candidate starts changing old docs, stop.
- If pyproject version changes, stop.
- If `uv.lock` appears, stop.
- If tag creation is suggested, stop.

## 27. Final Candidate Statement

This document is a P4 Decision Record Candidate only.

It is not the final decision record.

It does not start P4.

It does not approve P4.

It does not authorize P4.

It does not authorize P4 implementation.

It does not start v7.

It does not authorize v7 implementation.

It does not authorize product/MVP/deployment.

It does not authorize API/MCP/connector operation.

It does not authorize external project adoption.

It does not authorize Memory Graph behavior or mutation.

It does not authorize durable memory writing.

It does not authorize code/test/source/config changes.

`v6.16.0` remains sealed.

Current candidate outcome remains paused / not approved / not authorized.

Future P4 phase change requires explicit human approval in a separate final decision record.
