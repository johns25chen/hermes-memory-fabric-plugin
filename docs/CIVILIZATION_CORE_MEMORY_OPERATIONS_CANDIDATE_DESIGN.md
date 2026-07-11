# Civilization Core Memory Operations Candidate Design / 文明之核记忆操作候选设计

## 1. Candidate Status / 候选状态

This document is docs-only, design-only, candidate-only, operations-methodology-study-only, operation-request-modeling-only, and evidence-and-impact-modeling-only. It is based on the sealed `v6.16.0` Civilization Core Stable Kernel and governed by `docs/CIVILIZATION_CORE_V7_DESIGN_ONLY_CHARTER.md`. It changes no existing document, code, test, dependency, or package version. It creates no tag: there is no `v6.17` and no `v7.0.0` release authorization.

It grants no operation runtime implementation authorization, memory writer implementation authorization, storage implementation authorization, graph mutation implementation authorization, or product implementation authorization. It creates no automatic persistence, automatic durable memory write, or automatic Memory Graph mutation; this candidate design is not implementation permission.

`Memory Operations Candidate` is a design workstream label. It is not an implemented memory operator, memory writer, mutation engine, workflow engine, service, module, runtime, or product.

## 2. Candidate Purpose / 候选目的

This candidate treats a memory operation as a reviewable candidate request. It separates operation request, operation subject, evidence, impact, review, decision, authorization, and execution. It defines provenance-preserving operation discipline that exposes preconditions, conflicts, gaps, risks, reversibility, and uncertainty.

Its output is an Operation Outcome Candidate for human review, not a direct memory change. It prepares evidence for later human decisions; preserves rejection, deferral, expiry, and supersession history; prevents candidates from entering durable memory or modifying the Memory Graph automatically; and prevents tools from executing operations merely because this document exists.

Memory operation is a reviewable candidate request, not a memory mutation.

## 3. Problem Definition / 问题定义

- A detected change is not an authorized revision.
- New evidence is not memory admission.
- Conflict is not an automatic merge.
- Duplication is not automatic deletion.
- Similarity is not the same memory identity.
- A newer source is not automatic supersession.
- A stale signal is not automatic expiry.
- A privacy concern is not automatic redaction.
- Accepted review is not executed mutation.
- An operation request is not approval.
- Approval is not authorization.
- Authorization is not automatic execution.
- An Operation Outcome Candidate is not durable state.
- A graph relation proposal is not Memory Graph mutation.

Automatic operations can cause provenance loss, scope leakage, identity collision, history erasure, overmerge, overdelete, and irreversible drift. Memory operations without human review can defeat governance and manufacture false certainty.

## 4. Design Principles / 设计原则

1. **Preserve source identity.** Do not collapse distinguishable sources into one identity.
2. **Preserve provenance.** Keep origin, extraction context, time, and derivation visible.
3. **Separate proposal from mutation.** A candidate request changes no memory.
4. **Keep operation output candidate-only.** Outcomes remain review material.
5. **Make operation scope explicit.** State subjects, sources, time, exclusions, and owner.
6. **Make impact visible.** Describe affected audiences and downstream interpretations.
7. **Make reversibility visible.** State restoration limits without promising rollback.
8. **Preserve conflicts and gaps.** Do not silently resolve or fill them.
9. **Keep review human-controlled.** Models and tools do not decide authority.
10. **Prevent automatic durable writes.** Candidate creation never persists memory.
11. **Prevent automatic Memory Graph mutation.** Candidate relations create no nodes or edges.
12. **Preserve rejection, deferral, supersession, expiry, and rollback evidence.** Retain the review history.

Provenance outranks operational convenience. Source fidelity outranks consolidation fluency. Reviewability outranks automation speed. Reversible analysis outranks irreversible mutation. Newer evidence does not automatically outrank older evidence. More operation candidates do not imply more required changes. Lower operational risk does not create authorization. Successful validation does not create execution permission.

## 5. Operation Scope and Request Model / 操作范围与请求模型

These are conceptual objects, not implemented records, commands, or schemas.

| # | Conceptual object | Conceptual purpose | Minimum provenance or scope information | Human review role | Non-authoritative boundary |
| --- | --- | --- | --- | --- | --- |
| 1 | Operation Scope | Bounds the proposed analysis | Named subjects, sources, time, exclusions, owner | Confirm the exact boundary | Operation scope is not mutation authorization |
| 2 | Operation Request | Frames the proposed operation for review | Requester, date, scope, subject, rationale | Accept for review, return, defer, or reject | Operation request is not an execution command |
| 3 | Operation Intent | Explains the requested review purpose | Stated purpose, expected question, non-goals | Check purpose and overreach | Operation intent is not execution intent |
| 4 | Operation Subject Candidate | Identifies what may be considered | Source-local identifier, disambiguation, known aliases | Resolve identity ambiguity | It is not durable memory identity |
| 5 | Source Boundary | Limits eligible origin material | Source references, owners, collection context | Approve source fitness and exclusions | It cannot expand automatically |
| 6 | Time Boundary | Limits temporal applicability | Observation time, valid interval, known gaps | Interpret time relevance | It does not prove current truth |
| 7 | Evidence Requirement | States evidence needed for review | Evidence types, provenance needs, missing items | Judge sufficiency and uncertainty | It does not certify correctness |
| 8 | Exclusion Rule | States material outside review | Excluded sources, subjects, interpretations, reason | Confirm exclusions are justified | It does not delete source material |
| 9 | Human Owner | Names responsibility for scope and decisions | Named owner, role, transfer record if any | Own or explicitly transfer review | Missing Human Owner produces `HOLD` |
| 10 | Expiry Boundary | Ends the validity of the request scope | Expiry date or event, owner, renewal condition | Decide whether to renew scope | Expired scope requires new explicit human scope |

Tools may not infer missing scope. Source boundaries may not expand automatically. An evidence requirement does not certify correctness, and an exclusion rule does not delete source material.

## 6. Memory Operation Candidate Object Model / 记忆操作候选对象模型

These objects express proposed memory operations without performing them.

| # | Candidate object | Conceptual purpose | Source/provenance requirement | Human review role | Non-authoritative boundary |
| --- | --- | --- | --- | --- | --- |
| 1 | Inspection Candidate | Frames bounded, read-oriented examination | Subject and source references, known state, gaps | Review findings and next disposition | Inspection candidate is not mutation |
| 2 | Admission Candidate | Submits content for durable-adoption review | Original sources, candidate derivation, conflicts | Decide whether a separate adoption decision is warranted | Admission candidate is not adopted memory |
| 3 | Revision Candidate | Proposes a controlled change for review | Existing-state reference, new evidence, proposed wording | Compare current and proposed states | Revision candidate is not applied revision |
| 4 | Supersession Candidate | Proposes a successor relationship | Existing and proposed sources, time and scope comparison | Assess succession and preservation | Supersession candidate is not historical erasure |
| 5 | Merge Candidate | Proposes identity consolidation review | All subject sources, identity and conflict evidence | Determine whether identity is genuinely shared | Merge candidate is not merged memory |
| 6 | Split Candidate | Proposes identity separation review | Parent sources, distinction evidence, ambiguity | Determine whether distinctions justify separation | Split candidate is not split memory |
| 7 | Link Candidate | Proposes a relation hypothesis | Both subject sources, direction, supporting and conflicting evidence | Judge relation meaning and scope | Link candidate is not graph edge |
| 8 | Unlink Candidate | Proposes relation-removal review | Current relation reference and historical evidence | Review whether relation should remain represented | Unlink candidate is not graph deletion |
| 9 | Archive Candidate | Proposes removal from an active view | Subject, trigger, preservation and audience scope | Review visibility and preservation | Archive candidate is not deletion |
| 10 | Expiry Candidate | Proposes time/scope inapplicability review | Subject, validity evidence, time boundary | Decide whether applicability ended | Expiry candidate is not automatic removal |
| 11 | Redaction Candidate | Proposes controlled visibility restriction | Sensitive fragment, source, policy context, audience | Decide lawful and governed handling | Redaction candidate is not automatic redaction |
| 12 | Operation Outcome Candidate | Summarizes a reviewed candidate result | Inputs, evidence, review state, decision references, gaps | Decide whether any separate adoption or mutation process is warranted | Operation outcome candidate is not durable state |

## 7. Inspection Candidate / 检视候选

An Inspection Candidate may express a bounded inspection purpose, subject candidate, source references, current known state, suspected issue, missing evidence, conflict evidence, scope, Human Owner, review state, expiry, and decision reference.

Inspection is read-oriented candidate analysis. It does not authorize mutation, certify truth, create durable memory, or create graph state. It may end in `HOLD`, `REJECT`, `DEFER`, or no-change. No automatic follow-on operation may be created.

## 8. Admission and Revision Candidates / 准入与修订候选

### Admission Candidate

An Admission Candidate is a candidate request that submits content as an object of durable memory adoption review. It is not an adopted memory.

### Revision Candidate

A Revision Candidate is a candidate request for a controlled review of a proposed change to an existing memory. It is not an applied revision.

Both candidates must show source references, current-state reference when applicable, proposed candidate content, rationale, evidence, conflicts, scope, Human Owner, impact note, reversibility note, expiry, and review state.

New evidence does not automatically replace existing memory. Accepted wording is not a durable write. Review completion is not mutation. There is no automatic admission, automatic revision, automatic durable memory write, or automatic Memory Graph mutation.

## 9. Supersession Candidate / 取代候选

A Supersession Candidate may express an existing memory reference, proposed successor candidate, source and evidence comparison, temporal relation, scope relation, conflict, historical preservation requirement, Human Owner, impact note, reversibility note, review state, expiry, and decision reference.

Supersession is not deletion. Newer is not automatically better. A successor candidate is not adopted memory. Superseded history must remain visible, and the candidate does not overwrite source evidence. There is no automatic supersession, automatic history erasure, or automatic durable write.

## 10. Merge and Split Candidates / 合并与拆分候选

### Merge Candidate

A Merge Candidate proposes that multiple memory subject candidates may require consolidation review.

### Split Candidate

A Split Candidate proposes that one memory subject candidate may require separation review.

Both must show subject identities, source references, identity evidence, conflicting evidence, scope, temporal validity, merge or split rationale, retained distinctions, Human Owner, impact note, reversibility note, expiry, and review state.

Similarity is not identity, and shared attributes are not merge proof. A merge candidate is not merged memory; a split candidate is not split memory. Ambiguity remains visible. Merge must not erase conflicts, and split must not fabricate identities. There is no automatic merge, automatic split, automatic graph node merge, or automatic graph node creation.

## 11. Link and Unlink Candidates / 关联与解除关联候选

Link and Unlink Candidates are conceptual only. Each must identify the source subject candidate, target subject candidate, relation hypothesis, current relation reference when present, supporting evidence, conflicting evidence, direction note, temporal scope, Human Owner, impact note, reversibility note, expiry, rejection reason when applicable, and decision reference.

A link candidate is not graph edge. An unlink candidate is not graph deletion. A relation hypothesis is not a graph fact, and an accepted interpretation is not Memory Graph mutation. Unlink review must preserve historical evidence. No edge writer is created. There is no automatic link, automatic unlink, automatic graph edge creation, automatic graph edge deletion, or automatic Memory Graph mutation.

## 12. Archive, Expiry, and Redaction Candidates / 归档、失效与脱敏候选

### Archive Candidate

An Archive Candidate proposes moving content outside a current active view for review. Archive is not deletion.

### Expiry Candidate

An Expiry Candidate proposes that content may no longer apply to a stated scope or time. Expiry is not automatic removal, and a stale signal is not expiry authorization.

### Redaction Candidate

A Redaction Candidate proposes controlled hiding or restriction of a sensitive fragment. It may not automatically modify the original source. A redaction candidate is not automatic redaction.

Each must show subject reference, source reference, trigger evidence, scope, affected audience, preservation requirement, a legal or policy note if one exists without manufacturing a legal conclusion, Human Owner, impact note, reversibility note, expiry, review state, and decision reference.

Redaction must not silently rewrite source history. Privacy concern does not permit autonomous deletion. There is no automatic archive, automatic expiry, automatic redaction, automatic deletion, or automatic durable mutation.

## 13. Evidence, Impact, and Reversibility Notes / 证据、影响与可逆性说明

| # | Explanatory dimension | Question made visible |
| --- | --- | --- |
| 1 | Provenance completeness | Are origin, context, derivation, owner, and time traceable? |
| 2 | Source authority uncertainty | What is unknown or disputed about source fitness? |
| 3 | Current-state visibility | Is the state being compared complete and identifiable? |
| 4 | Conflict visibility | Which sources or interpretations disagree? |
| 5 | Identity ambiguity | Could subjects be conflated or improperly separated? |
| 6 | Temporal validity | For what time is the evidence applicable? |
| 7 | Scope mismatch risk | Could the conclusion escape its source, audience, or project boundary? |
| 8 | Downstream impact | Which interpretations, users, or dependent candidates could be affected? |
| 9 | Reversibility limitation | What history, context, or identity may be difficult to restore? |
| 10 | Historical preservation risk | Could the operation obscure earlier evidence or decisions? |

An impact note is explanatory metadata, not an approval score. A reversibility note is not rollback execution. Low impact is not automatic approval; high impact is not automatic rejection. Complete evidence is not automatic authorization. No scoring engine, auto-approval threshold, auto-rejection threshold, or rollback engine is implemented. All interpretation remains human-controlled.

## 14. Conceptual Memory Operation Lifecycle / 概念记忆操作生命周期

The static path is:

`explicit human scope → operation request framing → subject and source boundary review → evidence assembly → precondition review → operation candidate construction → impact and reversibility annotation → conflict review → boundary review → human review → approval request → approval → separate authorization decision → operation outcome candidate → separate adoption or mutation decision record`

No step may be skipped automatically. Request framing may not expand scope. Source boundary review precedes candidate construction. Evidence assembly may not overwrite sources. Preconditions may not be deemed satisfied automatically. Candidate construction may not modify memory. Impact annotation may not rank a candidate into approval. Conflict review may not silently resolve conflict. Boundary review may not authorize. Human review may not execute. An approval request may not approve itself. Approval may not authorize automatically. Authorization may not execute automatically. An Operation Outcome Candidate may not persist automatically. Adoption or mutation requires a separate human decision.

Stopped work preserves evidence. A rejected candidate remains rejected. A deferred candidate remains deferred. Expired scope requires new explicit human scope.

## 15. Human Review and Decision Boundary / 人工审查与决策边界

The following remain separate: request review, scope review, source review, evidence review, precondition review, impact review, reversibility review, conflict review, operation candidate review, approval request, approval, authorization, memory adoption, memory mutation, graph adoption, graph mutation, and execution.

Review is not approval. An approval request is not approval. Approval is not automatic authorization. Authorization is not automatic memory adoption, memory mutation, graph adoption, or graph mutation. Adoption is not execution. Mutation is not execution unless separately authorized. No model may self-authorize. No tool output may become implementation permission. Document completion may not trigger persistence, and no operation candidate may trigger memory or graph mutation.

No memory operator, model, operation candidate, impact note, reversibility note, validation result, test, audit, branch, commit, or pull request may act as the authorization source.

## 16. External Methodology Boundary / 外部方法论边界

GBrain may be studied only as a methodology candidate. Possible research directions include memory operation abstractions, memory update proposal patterns, consolidation concepts, revision and supersession concepts, merge and split concepts, lifecycle state concepts, evaluation hooks, goal-oriented review concepts, operation evidence packaging, and human-governed operation design.

GBrain is not a dependency, adapter, runtime, implementation base, product module, approved integration, memory operator, memory writer, mutation engine, graph writer, storage system, evaluation runtime, autonomous agent, authorization source, completion condition, or Civilization Core identity.

`llm_wiki` belongs to the Knowledge Compilation Candidate. M-Flow belongs to the Associative Recall Candidate. This task does not expand into an Evaluation Candidate runtime or any other workstream.

Methodology absorption is not runtime adoption.

## 17. Risks and Failure Modes / 风险与失败模式

| # | Risk | Risk description | Detection evidence | Required human response | Prohibited automatic response |
| --- | --- | --- | --- | --- | --- |
| 1 | Unauthorized admission | Candidate content is treated as adopted memory | Durable-state claim without separate decision | Stop, preserve evidence, review authority | Admit or persist |
| 2 | Unauthorized revision | Proposed wording is treated as applied | Current state changes without authorization record | Restore review boundary and escalate | Revise or write |
| 3 | History erasure | Earlier source or decision becomes invisible | Missing lineage or displaced references | Require preservation analysis | Delete or overwrite |
| 4 | False supersession | Newer evidence is assumed superior | Weak source/scope comparison | Reassess chronology, authority, and scope | Supersede automatically |
| 5 | Identity overmerge | Distinct subjects are conflated | Conflicting identifiers or contexts | Hold and resolve identity manually | Merge nodes or records |
| 6 | Invalid split | One subject is divided without evidence | Fabricated distinctions or weak provenance | Return for identity review | Create new identities |
| 7 | Link overreach | Hypothesis is treated as relation fact | Unsupported direction or temporal mismatch | Review relation evidence | Create graph edge |
| 8 | Unlink evidence loss | Relation history disappears | Missing current relation or rejection history | Preserve lineage and reassess | Delete edge or history |
| 9 | Archive overread | Archive is interpreted as deletion or falsehood | Active-view change obscures preserved source | Clarify audience and preservation | Archive or delete automatically |
| 10 | Premature expiry | Staleness signal becomes removal authority | No explicit validity boundary or owner | Hold for time-scope decision | Expire or remove |
| 11 | Redaction overreach | Sensitive handling silently rewrites history | Source mismatch or excessive audience restriction | Seek governed human decision | Redact or delete |
| 12 | Scope leakage | Operation exceeds subjects, sources, or projects | Out-of-scope evidence or downstream target | Stop and obtain new explicit scope | Expand scope |
| 13 | Conflict suppression | Contradictions disappear from output | One-sided evidence pack or missing dissent | Restore conflicts and gaps | Resolve or discard conflict |
| 14 | Impact underread | Downstream harm is omitted | Missing audience, dependency, or identity analysis | Expand human impact review | Auto-approve as low risk |
| 15 | Automatic persistence drift | Candidate becomes durable state | Write, queue, cache, or registry side effect | Stop and investigate boundary breach | Persist, repair, or remediate |
| 16 | External methodology identity drift | GBrain becomes system identity or implementation base | Dependency, adapter, runtime, or branding claim | Reassert methodology-only boundary | Adopt or integrate |

No automatic repair, remediation, adoption, mutation, merge, split, link, unlink, archive, expiry, redaction, deletion, or persistence is designed.

## 18. Open Design Questions / 开放设计问题

1. **Operation subject identity:** What evidence is sufficient to distinguish one subject candidate from another?
2. **Admission evidence threshold:** What evidence package permits human admission review without implying admission?
3. **Revision granularity:** How small or broad may a revision candidate be while retaining context?
4. **Supersession criteria:** What source, scope, and temporal comparisons should reviewers require?
5. **Historical preservation:** What minimum lineage must remain visible after a later human decision?
6. **Merge identity boundary:** Which distinctions must block or pause consolidation review?
7. **Split granularity:** How can reviewers avoid inventing identities during separation analysis?
8. **Link direction:** How should direction, symmetry, and time be represented without graph assertion?
9. **Unlink preservation:** What relation history must survive a decision not to retain a link?
10. **Archive visibility:** Which audiences should retain access to archived evidence?
11. **Expiry semantics:** Does expiry concern truth, applicability, review scope, or active visibility?
12. **Redaction scope:** How should fragment, audience, source, and policy boundaries be represented?
13. **Impact representation:** Which downstream dependencies and audiences must be named?
14. **Reversibility representation:** How should partial, costly, or impossible restoration be explained?
15. **Conflict ownership:** Who owns unresolved contradictions across sources or projects?
16. **Human Owner transfer:** What evidence makes ownership transfer explicit and bounded?
17. **Rejection preservation:** How should rejected candidates remain discoverable without reactivation?
18. **Multi-source contradiction:** How should evidence packs preserve incompatible claims without forced resolution?

An open question is not a hidden implementation task. Unresolved questions remain unresolved, and tools may not silently choose answers. No default technology selection or mutation policy may be inferred. Every future answer requires explicit human scope.

## 19. Allowed Future Design Handoffs / 允许的后续设计交接

Only these design-only handoff candidates may be proposed:

1. Memory Operation Scope and Request Vocabulary
2. Inspection Candidate Vocabulary
3. Admission and Revision Candidate Detail
4. Supersession Candidate Detail
5. Merge and Split Candidate Detail
6. Link and Unlink Candidate Detail
7. Archive, Expiry, and Redaction Candidate Detail
8. Impact and Reversibility Note Detail
9. Memory Operations Risk Register
10. Memory Operations Candidate Closure Review

This list is not a backlog and creates no task or branch. Every item requires new explicit human scope and remains docs-only, design-only, and candidate-only. Closure review does not authorize implementation, storage, a memory writer, persistence, Memory Graph mutation, or product implementation.

## 20. Stop Conditions / 停止条件

Stop immediately if work creates or implies:

- `v6.17` or a released `v7.0.0`;
- v6 runtime modification or v7 implementation;
- a memory operation runtime, memory operator, memory writer, mutation engine, workflow engine, operation executor, or prototype;
- a schema file, database, vector store, graph database, persistent cache, or storage;
- an API, MCP, Connector, Agent, dependency, or adapter;
- network activation, OAuth, credentials, or secrets;
- automatic admission, revision, supersession, merge, split, link, unlink, archive, expiry, redaction, or deletion;
- automatic persistence of an operation candidate or automatic durable memory write;
- automatic graph node creation, graph edge creation, or Memory Graph mutation;
- automatic approval, authorization, execution, or self-authorization;
- review treated as approval, approval as authorization, or authorization as execution;
- newer evidence treated as automatically better, or similarity treated as identity;
- low impact treated as approval, or an Operation Outcome Candidate treated as durable state;
- GBrain treated as a dependency or system identity;
- a design artifact treated as implementation permission.

Stopping means preserving memory operation design evidence and returning to human review. It does not mean automatic implementation, admission, revision, supersession, merge, split, link, unlink, archive, expiry, redaction, deletion, persistence, mutation, repair, remediation, deployment, or launch.

## 21. Final Candidate Statement / 最终候选声明

Memory Operations Candidate remains `DESIGN-ONLY`, and operation output remains candidate-only: inspection candidate is not mutation; admission candidate is not adopted memory; revision candidate is not applied revision; supersession candidate is not historical erasure; merge candidate is not merged memory; split candidate is not split memory; link candidate is not graph edge; unlink candidate is not graph deletion; archive candidate is not deletion; expiry candidate is not automatic removal; redaction candidate is not automatic redaction; operation outcome candidate is not durable state. Memory operation is not memory mutation.

Provenance remains required. Conflicts and gaps remain visible. Impact and reversibility remain visible. Review remains human-controlled. There is no memory operation runtime, memory writer implementation, mutation engine implementation, storage implementation, dependency adoption, adapter activation, automatic durable memory write, automatic persistence, or automatic Memory Graph mutation.

The sealed `v6.16.0` baseline remains unchanged. There is no `v6.17` and no `v7.0.0` release authorization. Explicit human scope remains required; this candidate design creates no implementation authorization.
