# Civilization Core P4 Discussion Scope Candidate / 文明之核 P4 讨论范围候选

## 2. Discussion Scope Status

This is a docs-only P4 discussion scope candidate.

It is based on the sealed `v6.16.0` Civilization Core Stable Kernel.

It is based on the merged P4 Decision Gate Checklist.

It is based on the merged External Product Explanation Candidate.

It is based on the merged Memory Ontology Mapping.

It is based on the merged Connector Governance Taxonomy.

It is based on the merged Explainable Recall Trace Template.

It is based on the merged Failed Attempt Memory / Do-Not-Retry Rules.

It is based on the merged Memory Lifecycle Taxonomy.

It is based on the merged Temporal Validity Model.

It is based on the merged Memory Evaluation Candidates.

It is discussion-scope candidate only.

It creates or authorizes:

- no P4 start
- no P4 approval
- no P4 implementation plan
- no v7 start
- no v7 implementation authorization
- no product implementation authorization
- no MVP
- no deployment
- no product launch
- no pricing
- no public website final copy
- no sales copy
- no API/MCP operation surface
- no connector operation
- no Memory Graph behavior
- no Memory Graph mutation
- no runtime capability
- no dependency activation
- no durable writer
- no authorization/execution semantics
- no tests
- no code changes
- no README changes
- no existing doc changes
- no package version change
- no tag
- no `v6.17`

This document defines a possible discussion frame only. It does not make Civilization Core / Subspace Memory System more executable, deployable, commercial, operable, or implementation-ready.

## 3. What "P4 Discussion" Means Here

P4 discussion is a possible future human-reviewed discussion frame.

P4 discussion is not P4 start.

P4 discussion is not P4 approval.

P4 discussion is not P4 implementation.

P4 discussion is not v7 start.

P4 discussion is not product, MVP, or deployment work.

P4 discussion may only examine whether a future scoped P4 proposal should be drafted.

P4 discussion cannot authorize implementation.

P4 discussion cannot authorize productization.

P4 discussion cannot authorize API/MCP/connector operation.

P4 discussion cannot authorize Memory Graph behavior or mutation.

P4 discussion cannot authorize durable memory writing.

P4 discussion requires explicit human review later.

If any reader treats P4 discussion as phase transition, approval, implementation permission, product work, v7 work, connector work, graph work, or durable memory writing permission, the discussion must stop.

## 4. Discussion Scope Purpose

This document defines safe discussion boundaries.

It prevents discussion from becoming authorization.

It prevents roadmap language from becoming implementation.

It prevents candidate docs from becoming active capability.

It preserves sealed `v6.16.0`.

It preserves human sovereignty.

It makes stop conditions visible before any future discussion.

It makes `fail`, `defer`, and `discussion-only` valid outcomes.

It makes P4 discussion safer, narrower, and more auditable. It does not make P4 easier to start.

## 5. Allowed Discussion Topics

| Topic | Allowed? | What may be discussed | Required boundary |
| --- | --- | --- | --- |
| whether P4 should even be discussed later | yes | Whether enough local governance evidence exists to justify a later human-reviewed P4 discussion. | Discussion readiness only; no P4 start. |
| what evidence is missing before P4 discussion | yes | Missing docs, missing human decision records, missing blocker checks, or missing source grounding. | Missing evidence leads to `defer` or `fail`, not approval. |
| what docs-only clarification is still needed | yes | Whether a separate future docs-only clarification should be scoped. | Clarification is not implementation. |
| whether P4 Decision Gate Checklist has blockers | yes | Blockers, unknowns, failed preconditions, and stop conditions from the checklist. | Checklist review does not start P4. |
| whether External Product Explanation Candidate overclaims | yes | Candidate wording that could imply product availability, launch, customers, pricing, install path, or final public copy. | Product wording remains candidate-only. |
| whether productization wording remains safe | yes | Whether Productization Roadmap language is still non-authorization. | Roadmap remains non-implementation. |
| whether v7 boundary remains safe | yes | Whether v7 Pre-Design Decision remains pre-design context only. | v7 mention is not v7 start. |
| whether connector/source governance remains taxonomy-only | yes | Whether connector, source, API, credential, permission, sync, and freshness words remain evidence vocabulary. | No connector operation or API/MCP surface. |
| whether ontology/Memory Graph wording remains vocabulary-only | yes | Whether object types, relationship labels, and attributes remain mapping vocabulary. | No schema, graph behavior, graph traversal, inference, or mutation. |
| whether evaluation/benchmark wording remains candidate-only | yes | Whether evaluation questions and benchmark references remain review vocabulary. | No runner, scores, superiority claim, or guarantee. |
| whether human review records are sufficient | yes | Whether a later reviewer can see participant, evidence, claim, inference, blocker, and outcome scope. | Readiness is not approval. |
| whether future P4 proposal scope should be drafted later | yes | Whether a separate future P4 Proposal Scope Candidate should be considered if explicitly approved later. | Proposal-scope drafting only; no P4 start. |

## 6. Prohibited Discussion Topics

| Topic | Why prohibited | Required response | Allowed outcome |
| --- | --- | --- | --- |
| starting P4 | It would convert discussion scope into phase transition. | Stop and require separate explicit human authorization. | fail |
| approving P4 | Approval is outside discussion-scope candidate status. | Stop and require a separate human decision record. | fail |
| implementing P4 | Implementation exceeds docs-only discussion. | Stop. | fail |
| starting v7 | v7 requires separate explicit human scope. | Stop and return to v7 boundary. | fail |
| authorizing v7 implementation | This document cannot authorize v7 work. | Stop and require separate v7 approval evidence. | fail |
| authorizing product implementation | Product implementation is outside discussion scope. | Stop and require product-boundary review. | fail |
| authorizing MVP | MVP implies build scope. | Stop. | fail |
| authorizing deployment | Deployment implies operable system status. | Stop. | fail |
| authorizing product launch | Launch implies public availability. | Stop. | fail |
| creating pricing | Pricing implies commercial availability. | Stop and remove from scope. | fail |
| publishing website final copy | Final public copy can imply launch. | Stop and require separate publication approval. | fail |
| publishing sales copy | Sales copy can imply product availability. | Stop. | fail |
| creating API/MCP operation surface | Operation surface implies tool or service behavior. | Stop and require separate operation-surface proposal. | fail |
| creating connector operation | Connector operation implies source access behavior. | Stop and require separate connector proposal. | fail |
| implementing Memory Graph behavior | Behavior would be implementation. | Stop and require separate graph proposal. | fail |
| mutating Memory Graph | Mutation is durable state change. | Stop and require governed graph-write approval. | fail |
| implementing ontology schema | Schema turns vocabulary into implementation. | Stop and return to vocabulary-only boundary. | fail |
| implementing graph database behavior | Database behavior is implementation. | Stop. | fail |
| implementing benchmark runner | Runner is code/execution scope. | Stop. | fail |
| implementing evaluation runner | Runner is code/execution scope. | Stop. | fail |
| adding tests/code | Tests/code are prohibited by this docs-only scope. | Stop. | fail |
| changing package version | Version change reopens release identity. | Stop. | fail |
| creating tag | Tag creation may imply release continuation. | Stop. | fail |
| creating v6.17 | v6 line is sealed at `v6.16.0`. | Stop. | fail |
| creating uv.lock | Lockfile creation implies dependency/environment drift. | Stop. | fail |
| granting autonomous authority or self-authorization | Violates human sovereignty. | Stop and reject the claim. | fail |

## 7. Required Preconditions for Any Future P4 Discussion

Any future P4 discussion requires all of the following before it begins:

- P4 Decision Gate Checklist exists and remains candidate-only.
- Main branch is clean at the time of future discussion.
- Package version remains `6.16.0` unless separately approved.
- `v6.16.0` remains sealed.
- No `v6.17` continuation exists.
- No post-terminal tag exists.
- No `uv.lock` exists.
- No source/test/script/config drift exists.
- All required input artifacts from P4 Decision Gate Checklist exist.
- All candidate docs remain non-implementation.
- No active Star-Source Memory runtime claim exists.
- No active Layer 15 runtime claim exists.
- No autonomous authority, personhood, life, legal status, or religious status claim exists.
- Explicit human permission exists to discuss P4 scope only.

If any precondition is missing, contradicted, or unknown, the safe outcome is `defer` or `fail`.

## 8. Discussion Entry Conditions

A P4 discussion can begin only when all of the following are true:

- a human explicitly asks for P4 discussion scope;
- discussion scope is docs-only;
- discussion purpose is bounded to whether a later P4 proposal should be drafted;
- no implementation work is authorized;
- no v7 work is authorized;
- no product/MVP/deployment work is authorized;
- no API/MCP/connector work is authorized;
- no Memory Graph work is authorized;
- no durable writer work is authorized;
- no package/version/tag change is authorized;
- all blockers are checked first.

Entry into discussion is not entry into P4.

## 9. Discussion Exit Conditions

A P4 discussion may end only as one of the following:

- stop because hard blocker found;
- defer because evidence missing;
- request additional docs-only clarification;
- produce discussion notes only;
- produce a future P4 Proposal Scope Candidate only if explicitly approved later;
- no decision;
- fail discussion;
- pass-to-proposal-drafting-only.

No exit condition starts P4.

No exit condition approves P4.

No exit condition authorizes P4 implementation.

No exit condition starts v7, authorizes productization, creates API/MCP/connector operation, authorizes Memory Graph behavior, or authorizes durable memory writing.

## 10. Allowed Outcomes

| Outcome | Meaning | What it allows | What it does not allow |
| --- | --- | --- | --- |
| fail | A blocker or boundary violation prevents safe continuation. | Stop and record the blocker. | No P4 start, approval, implementation, or proposal drafting. |
| defer | Evidence, review, or scope is insufficient. | Pause and request missing evidence or clarification. | No hidden approval or implementation. |
| discussion-only-notes | The discussion produced only notes. | Record evidence, claims, inferences, blockers, and uncertainty. | No phase transition or authorization. |
| request-new-docs-only-clarification | A later clarification doc may be useful. | Ask for a separately scoped docs-only artifact. | No existing-doc edit, code, tests, or implementation. |
| request-explicit-human-decision-record | Human decision evidence is required. | Ask for written scoped human decision. | No automatic approval from readiness. |
| pass-to-proposal-drafting-only | A later proposal-scope candidate may be drafted if separately approved. | Prepare for possible future P4 Proposal Scope Candidate only. | No P4 start, P4 approval, P4 implementation, v7 work, product work, or runtime capability. |

## 11. Disallowed Outcomes

| Disallowed outcome | Why disallowed | Required stop response |
| --- | --- | --- |
| P4 started | Discussion scope cannot create phase transition. | Stop and require separate explicit human authorization. |
| P4 approved | Discussion notes cannot approve P4. | Stop and require separate approval record. |
| P4 implementation authorized | Implementation is outside this document. | Stop. |
| v7 started | v7 requires separate explicit human scope. | Stop. |
| v7 implementation authorized | This document cannot authorize v7 implementation. | Stop. |
| productization authorized | Productization requires separate approval. | Stop. |
| MVP authorized | MVP implies build scope. | Stop. |
| deployment authorized | Deployment implies operable system status. | Stop. |
| API/MCP/connector operation authorized | Operation surface is outside discussion scope. | Stop. |
| Memory Graph behavior authorized | Behavior is implementation. | Stop. |
| durable writer authorized | Durable writing requires governed approval. | Stop. |
| code/tests authorized | Code/tests are prohibited here. | Stop. |
| tag/version change authorized | Release identity cannot change from this document. | Stop. |

## 12. Productization Discussion Boundary

Productization Roadmap may be discussed as non-authorization only.

External Product Explanation Candidate may be discussed as candidate wording only.

There is no product plan.

There is no MVP.

There is no launch.

There is no pricing.

There is no sales copy.

There is no public website final copy.

There is no customer claim.

There is no install path.

There is no deployment.

Productization remains blocked unless later explicit human approval exists.

Productization discussion may ask whether wording is too broad, whether candidate status is visible, whether a claim needs removal, or whether a later docs-only clarification is needed. It must not produce build tasks, implementation milestones, packaging steps, launch material, availability claims, customer claims, or commercial claims.

## 13. v7 Discussion Boundary

v7 Pre-Design Decision may be referenced as non-implementation context only.

v7 mention is not v7 start.

P4 discussion does not imply v7.

No v7 branch should be created from this document.

There is no v7 implementation authorization.

There is no v7 roadmap execution.

Any future v7 proposal requires separate explicit human approval.

A future P4 discussion may inspect whether v7 language remains bounded. It must not convert pre-design material into implementation sequence, branch creation, package change, runtime work, dependency work, adapter work, or product work.

## 14. API / MCP / Connector Discussion Boundary

Connector governance remains taxonomy-only.

Connector result is evidence only.

API response is observation only.

MCP mention is not tool creation.

There is no API/MCP operation surface.

There is no connector logic, connector storage, or connector sync.

There is no source ingestion, source polling, or source freshness check.

Permission to read is not permission to act.

Future connector proposal requires separate human approval.

A future P4 discussion may inspect connector/source risk vocabulary, provenance notes, permission boundaries, and API/MCP overread risk. It must not create API calls, MCP tools, adapter behavior, connector behavior, credential handling, permission handling, sync, ingestion, polling, freshness automation, or source promotion.

## 15. Ontology / Memory Graph Discussion Boundary

Ontology mapping remains vocabulary-only.

Relationship label is not graph edge.

Relationship label is not graph traversal.

Object type is not storage schema.

Mapping is not Memory Graph mutation.

There is no Memory Graph behavior.

There is no graph database behavior.

There is no relationship inference.

There is no automatic classification, automatic mapping, automatic promotion, or automatic memory writing.

Future Memory Graph proposal requires separate human approval.

A future P4 discussion may inspect whether ontology words are useful and safe. It must not create schemas, graph storage, graph traversal, inference behavior, classification behavior, mapping behavior, promotion behavior, graph database behavior, Memory Graph behavior, or Memory Graph mutation.

## 16. Evaluation / Benchmark Discussion Boundary

Evaluation candidates remain review vocabulary only.

Evaluation question is not test.

Benchmark reference is not local benchmark approval.

There is no benchmark runner.

There is no evaluation runner.

There are no scores.

There is no performance guarantee.

There is no benchmark superiority.

Future benchmark proposal requires separate human approval.

A future P4 discussion may inspect whether evaluation questions are clear enough for human review. It must not create tests, suites, runners, pass rates, performance claims, benchmark proof, benchmark superiority, automated scoring, or guarantees.

## 17. Human Sovereignty Discussion Boundary

Human review is required before any future P4 discussion.

Human review is required before any phase transition.

Human review is not automatic approval.

Reviewer note is not implementation permission.

System cannot self-authorize.

There is no autonomous authority.

There is no personhood, life, awakening, legal status, or religious status claim.

Explicit human confirmation must be written before any later phase change.

Human sovereignty means that docs, checklists, reviews, tests, smokes, audits, PRs, tags, proposals, decision records, candidate notes, and discussion notes do not silently transfer authority away from the human operator.

## 18. Evidence / Claim / Inference Discussion Boundary

Evidence must be separated from claim.

Claim must be separated from inference.

Inference must not become approval.

Discussion note must not become authorization.

Roadmap must not become build authorization.

Checklist pass must not become P4 start.

Discussion scope must not become implementation scope.

Unresolved uncertainty requires defer or fail.

Unresolved conflict requires defer or fail.

Evidence can show what was observed in local docs, git state, tags, branch state, version state, or human instructions. Evidence does not grant authority. A claim may summarize evidence. An inference may explain a possible meaning. None of these can create P4, v7, product, connector, graph, benchmark, durable writer, or implementation permission.

## 19. Discussion Record Template

Use this template only if a future human explicitly requests P4 discussion scope. This is a discussion record template, not schema implementation.

```text
discussion date:
reviewer / participant:
branch / commit reviewed:
package version reviewed:
docs reviewed:
purpose of discussion:
evidence reviewed:
claims discussed:
inferences discussed:
unresolved conflicts:
unresolved uncertainties:
hard blockers found:
allowed outcome selected:
explicitly prohibited next actions:

explicit statement: "This discussion does / does not start P4"
explicit statement: "This discussion does / does not approve P4"
explicit statement: "This discussion does / does not authorize P4 implementation"
explicit statement: "This discussion does / does not authorize v7 implementation"
explicit statement: "This discussion does / does not authorize product/MVP/deployment"
explicit statement: "This discussion does / does not authorize API/MCP/connector operation"
explicit statement: "This discussion does / does not authorize Memory Graph behavior or mutation"
explicit statement: "This discussion does / does not authorize durable memory writing"

human approval / note:
```

If the template is used, the reviewer must select an allowed outcome from this document. Any attempted disallowed outcome must stop the discussion.

## 20. Candidate Future Sequence

This document does not automatically create any next sequence.

If discussion fails, stop.

If discussion defers, add only missing docs-only clarification if separately scoped.

If discussion passes to proposal-drafting-only, the next possible docs-only artifact may be a separate P4 Proposal Scope Candidate.

P4 Proposal Scope Candidate would still not start P4.

No implementation sequence is authorized here.

No v7 sequence is authorized here.

No productization sequence is authorized here.

No API/MCP/connector sequence is authorized here.

No Memory Graph sequence is authorized here.

Any later sequence requires explicit human scope, separate file permission, and a new boundary check.

## 21. Non-Authorization Rules

- discussion scope is not P4 start
- discussion scope is not P4 approval
- discussion scope is not P4 implementation plan
- discussion outcome is not P4 start
- P4 mention is not phase transition
- roadmap is not implementation authorization
- external explanation is not public launch
- v7 mention is not v7 implementation
- productization mention is not productization authorization
- API/MCP mention is not operation surface
- connector mention is not connector adoption
- ontology mention is not graph implementation
- Memory Graph mention is not Memory Graph mutation
- evaluation mention is not benchmark runner
- benchmark mention is not benchmark proof
- human review readiness is not approval
- sealed kernel is not active commercial product
- documentation maturity is not runtime capability
- repository context is not full system identity
- discussion scope is not authorization/execution permission

These rules apply to this document, future discussion notes, possible future proposal-scope candidates, local git evidence, merged docs, and human-review readiness checks.

## 22. Prohibited Implementation Rules

- do not start P4
- do not approve P4 from this document
- do not implement P4 from this document
- do not start v7 implementation
- do not build MVP
- do not implement product UI
- do not implement Operator Console
- do not implement demo app
- do not implement deployment
- do not implement packaging
- do not implement install path
- do not publish website final copy
- do not publish sales copy
- do not create pricing
- do not claim product availability
- do not claim customer deployment
- do not create API/MCP operation surface
- do not implement connector logic
- do not implement connector storage
- do not implement connector sync
- do not implement adapter behavior
- do not implement ontology schema
- do not implement graph database behavior
- do not implement Memory Graph behavior
- do not mutate Memory Graph
- do not implement graph traversal
- do not implement relationship inference
- do not implement automatic classification
- do not implement automatic mapping
- do not implement automatic promotion
- do not implement automatic memory writing
- do not implement durable writer
- do not implement recall engine
- do not implement evaluation runner
- do not implement benchmark runner
- do not add dependencies
- do not add adapters
- do not create runtime-activation bridge
- do not add authorization/execution semantics
- do not tag post-terminal docs
- do not change package version
- do not change existing docs
- do not change README
- do not change source, tests, scripts, or config

These prohibited implementation rules are instructions for interpreting this discussion-scope candidate. They are not implemented enforcement logic.

## 23. Stop Conditions

- if discussion scope is treated as P4 start, stop
- if discussion scope is treated as P4 approval, stop
- if discussion scope is treated as implementation plan, stop
- if discussion scope is treated as v7 start, stop
- if discussion scope turns into product plan, stop
- if discussion scope turns into MVP, stop
- if discussion scope turns into product deployment, stop
- if discussion scope turns into Operator Console, stop
- if discussion scope turns into product UI, stop
- if discussion scope turns into demo app, stop
- if discussion scope turns into install guide, stop
- if discussion scope turns into API/MCP operation surface, stop
- if discussion scope turns into connector implementation, stop
- if discussion scope turns into Memory Graph behavior or mutation, stop
- if discussion scope turns into ontology schema or graph database behavior, stop
- if discussion scope turns into benchmark runner or evaluation runner, stop
- if discussion scope starts changing old docs, stop
- if pyproject version changes, stop
- if `uv.lock` appears, stop
- if tag creation is suggested, stop

Stop means halt the discussion or task and return to explicit human review. It does not mean repair, revert, implement, or continue under a broader scope unless the human separately instructs that scope.

## 24. Final Discussion Scope Statement

This document defines P4 discussion scope candidates only.

It does not start P4.

It does not approve P4.

It does not authorize P4 implementation.

It does not start v7.

It does not authorize v7 implementation.

It does not authorize product/MVP/deployment.

It does not authorize API/MCP/connector operation.

It does not authorize Memory Graph behavior or mutation.

It does not authorize durable memory writing.

It does not authorize implementation.

`v6.16.0` remains sealed.

Future P4 proposal drafting requires explicit human approval.
