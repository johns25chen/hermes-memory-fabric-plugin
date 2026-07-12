# Civilization Core R5 Contract Decomposition Candidate Design

## 1. Candidate Status

This document is documentation-only, design-only, candidate-only, and non-executing.

| Decision | Status | Meaning |
| --- | --- | --- |
| R5.2 candidate status | `DESIGN-ONLY` | This candidate is available only for documentary review. |
| contract decomposition activity | `GO` | Bounded documentary decomposition may proceed; GO is not implementation permission. |
| implementation authority | `NONE` | No implementation authority is granted. |
| runtime implementation | `DEFER` | Runtime work remains deferred. |

## 2. Purpose

This candidate decomposes R5 documentary governance responsibilities so that source, evidence, provenance, scope, candidate objects, lifecycle and disposition, human review, approval requests, approval, authorization, adoption, mutation, execution, and non-execution boundaries can be reviewed independently. It creates no runtime contract, API contract, schema, enum, validator, workflow definition, state machine, storage model, or executable interface.

## 3. Scope

The Human Owner is repository maintainer Han. Scope is limited to this candidate document and the preserved source corpus. The work is technology-neutral and non-normative. Field-like vocabulary is conceptual and not stored fields. State-like vocabulary is conceptual and not runtime state.

This candidate creates no runtime; executable contract; schema; enum; parser; validator; linter runtime; state machine; workflow engine; contract engine; policy engine; rule engine; approval engine; authorization engine; adoption engine; mutation engine; execution engine; evaluator runtime; evaluation runner; benchmark runner; scoring engine; ranking engine; verdict engine; storage; persistence; database; graph database; API; MCP; Connector; Agent; UI; deployment; dependency; adapter; network integration; automatic durable memory write; or automatic Memory Graph mutation.

## 4. Source Corpus

This candidate reads and preserves exactly these 11 source documents without rewriting, renaming, normalizing, migrating, or updating them:

1. `docs/CIVILIZATION_CORE_R5_DESIGN_ONLY_WORKSTREAM_CHARTER.md`
2. `docs/CIVILIZATION_CORE_R4_FINAL_CLOSURE_AND_R5_DESIGN_ONLY_ENTRY_REVIEW.md`
3. `docs/CIVILIZATION_CORE_V7_DESIGN_ONLY_CHARTER.md`
4. `docs/CIVILIZATION_CORE_KNOWLEDGE_COMPILATION_CANDIDATE_DESIGN.md`
5. `docs/CIVILIZATION_CORE_ASSOCIATIVE_RECALL_CANDIDATE_DESIGN.md`
6. `docs/CIVILIZATION_CORE_MEMORY_OPERATIONS_CANDIDATE_DESIGN.md`
7. `docs/CIVILIZATION_CORE_MEMORY_EVALUATION_CANDIDATE_CLOSURE_REVIEW.md`
8. `docs/CIVILIZATION_CORE_EVALUATION_VOCABULARY_NORMALIZATION_REVIEW.md`
9. `docs/CIVILIZATION_CORE_DECISION_GATE_CHECKLIST.md`
10. `docs/CIVILIZATION_CORE_PRODUCT_NARRATIVE_PACKAGE.md`
11. `docs/CIVILIZATION_CORE_EXTERNAL_CANDIDATE_COMPARISON.md`

## 5. Inherited R5 Charter Decisions

The following decisions remain controlling:

- `R5 workstream status: OPEN-DESIGN`.
- `R5 design-only activity: GO`.
- `R5 implementation authority: NONE`.
- `R5 runtime implementation: DEFER`.
- GO is not implementation permission.
- Civilization Core is the governance kernel and memory constitution.
- Subspace Memory System is the engineering carrier.
- Hermes Memory Fabric is the current repository carrier.
- Codex, OpenClaw, and Hermes are tools or carriers, not authority.
- `v6.16.0` remains sealed; there is no `v6.17`, no `v7.0.0` release, and no tag.
- R4 corridor closure remains `CLOSE`.
- T9 remains GO for future v7 design-only exploration, while v7 runtime implementation remains DEFER.
- T10 productization remains roadmap-only.
- Automatic durable memory writing remains prohibited.
- Automatic Memory Graph mutation remains prohibited.

## 6. Contract Decomposition Identity

| ID | Contract decomposition principle | Review meaning |
| --- | --- | --- |
| CDP-01 | A contract is a documentary responsibility boundary. | It allocates documentary accountability only. |
| CDP-02 | A contract is not automatically an API contract and is not an execution command. | No callable or executable surface follows. |
| CDP-03 | A contract is not a schema or enum. | Conceptual terms do not define stored or typed representations. |
| CDP-04 | A contract is not a validator. | Documentary satisfaction is not machine enforcement. |
| CDP-05 | A contract is not a state machine or workflow. | Descriptive order and lifecycle language create no transitions. |
| CDP-06 | Field-like vocabulary is conceptual and not stored fields; state-like vocabulary is conceptual and not runtime state. | Tables remain review aids. |
| CDP-07 | Contract composition is not runtime inheritance, and contract dependency is not software dependency. | Documentary relationships create no code relationship. |
| CDP-08 | Contract satisfaction is not approval; completeness is not authorization; closure is not execution permission. | Human authority remains separate. |

## 7. Contract as Documentary Boundary

Each contract family identifies who must document a concern, what evidence makes it reviewable, what a human reviews, what must not be inferred, and why the concern remains non-runtime. A boundary may be complete as prose while every implementation question remains deferred. Documentary responsibility does not create a record type, field set, transition system, command, enforcement mechanism, or permission.

## 8. Cross-Workstream Contract Layers

| ID | Layer | Documentary responsibility | Required evidence | Human review role | Prohibited overread | Non-runtime boundary |
| --- | --- | --- | --- | --- | --- | --- |
| CCL-01 | Source identity and preservation | Name and preserve source identity and meaning. | Stable references and preservation notes. | Confirm identity and fidelity. | Source existence proves evidence. | No ingest or source registry. |
| CCL-02 | Evidence extraction and packaging | Distinguish extracts, context, gaps, and conflicts. | Reviewable evidence packet. | Judge relevance and sufficiency. | Packaging proves truth or approval. | No parser, evaluator, or storage. |
| CCL-03 | Provenance and derivation | Explain origin and interpretive steps. | Lineage, derivation, and uncertainty notes. | Review traceability. | Provenance proves correctness. | No graph write or lineage engine. |
| CCL-04 | Scope and ownership | Bound project, audience, time, trust, files, and Human Owner. | Explicit scope statement. | Confirm ownership and exclusions. | Scope grants authority beyond itself. | No access-control or policy engine. |
| CCL-05 | Candidate-object framing | Describe non-adopted documentary objects. | Purpose, inputs, outputs, non-goals. | Review conceptual fitness. | Candidate means implemented type. | No schema, enum, or stored object. |
| CCL-06 | Lifecycle and disposition | Describe human-owned documentary status and disposition. | Review record and rationale. | Choose or defer disposition. | Labels are runtime states. | No state machine or workflow. |
| CCL-07 | Human review | Define review questions and accountable reviewer role. | Evidence, dissent, gaps, and review notes. | Assess without automatic judgment. | Review equals approval. | No validator, scorer, or verdict engine. |
| CCL-08 | Approval request and approval | Keep a request distinct from a human decision. | Bounded request and separate decision record. | Request, approve, reject, or defer explicitly. | Request automatically becomes approval. | No approval engine or automated gate. |
| CCL-09 | Authorization, adoption, and mutation separation | Document distinct authority decisions and effects. | Separate human records for each concern. | Confirm every non-automatic step. | One decision implies later steps. | No authorization, adoption, or mutation engine. |
| CCL-10 | Execution and non-execution boundary | State what remains non-executing and deferred. | Explicit prohibitions and stop evidence. | Confirm no execution permission. | Document completion permits action. | No command, runner, deployment, or integration. |

## 9. Source and Evidence Contract Family

| ID | Source and evidence contract requirement |
| --- | --- |
| SER-01 | Identify each material source by exact, stable documentary reference. |
| SER-02 | Preserve source wording, identity, context, and historical status. |
| SER-03 | State that source is not evidence by existence alone. |
| SER-04 | Describe the bounded extraction or selection that makes material candidate evidence. |
| SER-05 | Separate direct evidence from interpretation, assumption, question, and analogy. |
| SER-06 | Package sufficient context for independent human review. |
| SER-07 | Expose missing, conflicting, stale, or uncertain evidence. |
| SER-08 | Bind evidence to applicable project, audience, temporal, and trust scope. |
| SER-09 | Keep evidence non-authoritative: evidence is not candidate approval. |
| SER-10 | Require preservation and review without ingest, parsing, validation, persistence, or execution. |

## 10. Candidate Object Contract Family

| ID | Candidate object contract requirement |
| --- | --- |
| COR-01 | Name the documentary candidate object and its bounded purpose. |
| COR-02 | Identify the Human Owner and intended reviewers. |
| COR-03 | Identify source and evidence inputs without treating them as authority. |
| COR-04 | Describe conceptual contents without defining stored fields. |
| COR-05 | Describe conceptual status without defining runtime state. |
| COR-06 | State scope, exclusions, assumptions, uncertainty, conflicts, and gaps. |
| COR-07 | State that a candidate is not proposal acceptance. |
| COR-08 | Keep candidate composition documentary and non-inheriting. |
| COR-09 | Keep candidate dependencies documentary and non-software. |
| COR-10 | Require human review before any separate proposal or disposition. |
| COR-11 | Prohibit automatic adoption, persistence, graph mutation, or execution. |
| COR-12 | Preserve the candidate as non-normative prose rather than a schema, API, validator, or interface. |

## 11. Human Review Contract Family

| ID | Human review contract requirement |
| --- | --- |
| HRC-01 | Name the accountable human reviewer or Human Owner. |
| HRC-02 | Present exact scope, sources, evidence, provenance, and candidate purpose. |
| HRC-03 | Present uncertainties, conflicts, dissent, gaps, and expiry concerns. |
| HRC-04 | Ask bounded documentary questions rather than machine-decidable predicates. |
| HRC-05 | Record review rationale and unresolved concerns. |
| HRC-06 | State that review is not approval. |
| HRC-07 | Prevent scores, labels, tests, or model output from becoming automatic judgment. |
| HRC-08 | Allow defer, reject, revise, or request-evidence dispositions without automatic transitions. |
| HRC-09 | Require a separate approval request when approval is sought. |
| HRC-10 | Keep review informational and non-executing, with no validator, workflow, or verdict behavior. |

## 12. Approval and Authorization Separation

The preserved chain is `source → evidence → candidate → proposal → review → approval request → approval → authorization → adoption → mutation → execution`. No arrow is automatic.

| ID | Approval and authorization separation rule |
| --- | --- |
| AAS-01 | Candidate is not proposal acceptance, and a proposal is not mutation. |
| AAS-02 | Review is not approval. |
| AAS-03 | An approval request is not approval. |
| AAS-04 | Approval is not authorization. |
| AAS-05 | Authorization is not adoption. |
| AAS-06 | Authorization is not mutation. |
| AAS-07 | Authorization is not execution. |
| AAS-08 | Every request, approval, and authorization requires a separate explicit human record and bounded scope. |

## 13. Adoption, Mutation, and Execution Separation

| ID | Adoption, mutation, and execution separation rule |
| --- | --- |
| AME-01 | Adoption is not mutation. |
| AME-02 | Mutation is not execution unless separately authorized. |
| AME-03 | Document completion is not execution permission. |
| AME-04 | Adoption requires a distinct human decision after authorization. |
| AME-05 | Mutation requires its own exact target, authority, and safety boundary. |
| AME-06 | Execution requires separate authorization after any permitted mutation. |
| AME-07 | No documentary status, completeness claim, closure, or handoff can trigger a later step. |
| AME-08 | This candidate performs and authorizes no adoption, mutation, durable write, graph change, or execution. |

## 14. Lifecycle and Disposition Contract Family

| ID | Lifecycle and disposition rule |
| --- | --- |
| LDR-01 | Lifecycle vocabulary describes documentary review context only. |
| LDR-02 | Disposition is a recorded human interpretation, not a runtime transition. |
| LDR-03 | Candidate, proposed, reviewed, deferred, rejected, and closed language is conceptual, not an enum. |
| LDR-04 | A lifecycle description creates no state machine or workflow. |
| LDR-05 | Each disposition names its Human Owner, scope, evidence, rationale, and date context without a generated timestamp here. |
| LDR-06 | Deferred material remains non-adopted and non-authoritative. |
| LDR-07 | Rejected material is preserved as historical evidence without automatic deletion. |
| LDR-08 | Revision preserves lineage and does not erase prior dissent or gaps. |
| LDR-09 | Closure means documentary review closure only, not authorization or execution permission. |
| LDR-10 | No disposition automatically creates a proposal, request, approval, adoption, mutation, persistence, or execution. |

## 15. Evidence and Provenance Requirements

| ID | Evidence and provenance requirement |
| --- | --- |
| EPR-01 | Identify every material source by stable document reference. |
| EPR-02 | Preserve raw-source meaning and historical wording. |
| EPR-03 | Record extraction or derivation context for every candidate claim. |
| EPR-04 | Distinguish direct evidence, interpretation, assumption, analogy, and open question. |
| EPR-05 | Make conflicting evidence and dissent visible. |
| EPR-06 | Make missing evidence, uncertainty, staleness, and coverage gaps visible. |
| EPR-07 | Record applicable project, audience, temporal, and trust scope. |
| EPR-08 | Name the Human Owner and intended human review role. |
| EPR-09 | Preserve lineage across revisions, deferrals, rejections, and handoffs. |
| EPR-10 | Treat provenance as traceability, not correctness, approval, authorization, adoption, mutation, or execution. |

## 16. Vocabulary and Naming Requirements

| ID | Vocabulary and naming rule |
| --- | --- |
| VNR-01 | Use R5 for the roadmap workstream, never a version, release, layer, or runtime state. |
| VNR-02 | Use contract for a documentary responsibility boundary, not automatically an API contract. |
| VNR-03 | Use candidate for non-adopted, non-authoritative documentary material. |
| VNR-04 | Keep source, evidence, candidate, proposal, review, approval request, approval, authorization, adoption, mutation, and execution distinct. |
| VNR-05 | Treat field-like and state-like terms as conceptual, not stored fields, enums, or runtime states. |
| VNR-06 | Preserve historical wording; do not normalize or migrate source terminology. |
| VNR-07 | Keep Civilization Core, Subspace Memory System, Hermes Memory Fabric, and tool identities distinct. |
| VNR-08 | Mark external names as methodology candidates only, never authority, system identity, dependency, or completion condition. |

## 17. External Methodology Boundary

`llm_wiki`, M-Flow, and GBrain may inform documentary methodology only. They are not dependencies, adapters, runtimes, writers, storage systems, contract engines, validators, schemas, authorities, identities, or completion conditions. Methodology absorption is not runtime adoption. Their names create no import, integration, operation surface, persistence, graph behavior, authority transfer, or execution path.

## 18. Contract Composition and Non-Inheritance Rules

| ID | Contract composition and non-inheritance rule |
| --- | --- |
| CNR-01 | Composition means documentary concerns may be reviewed together while retaining separate responsibilities. |
| CNR-02 | Contract composition is not runtime inheritance. |
| CNR-03 | Contract dependency is not software dependency. |
| CNR-04 | A parent, child, layer, family, or chain metaphor creates no type hierarchy. |
| CNR-05 | Shared vocabulary creates no shared storage model or interface. |
| CNR-06 | Reference to another contract creates no invocation, import, adapter, or network link. |
| CNR-07 | Satisfaction of one contract does not satisfy, approve, or authorize another. |
| CNR-08 | Documentary ordering creates no workflow transition or execution order. |
| CNR-09 | Contract completeness is not authorization, and contract closure is not execution permission. |
| CNR-10 | Any future implementation discussion would require new explicit human scope outside this candidate. |

## 19. Decision Gates

| ID | Decision gate | Passage condition |
| --- | --- | --- |
| DG-01 | Scope gate | Human Owner, exact artifact, sources, purpose, exclusions, and non-goals are explicit. |
| DG-02 | Inheritance gate | R4 closure, R5 charter, v7 design-only, and sealed-version boundaries remain intact. |
| DG-03 | Identity gate | Governance kernel, engineering carrier, repository carrier, tools, and external candidates remain distinct. |
| DG-04 | Evidence gate | Source, evidence, provenance, uncertainty, conflicts, gaps, and scope are independently reviewable. |
| DG-05 | Decomposition gate | Responsibilities are separable without schema, enum, validator, state machine, workflow, or executable interface. |
| DG-06 | Authority gate | Every authority-chain step remains separate and human-owned. |
| DG-07 | Non-runtime gate | No implementation, persistence, mutation, integration, deployment, or execution implication exists. |
| DG-08 | Handoff gate | A human confirms documentary completeness while authority remains NONE and runtime remains DEFER. |

Gate failure yields `HOLD`, `DEFER`, or `STOP` for documentary review only; it never triggers automatic repair, approval, authorization, mutation, or execution.

## 20. Prohibited Interpretations

Each row explicitly prohibits the stated positive claim; none is asserted elsewhere by this candidate.

| ID | Prohibited interpretation |
| --- | --- |
| PI-01 | Do not claim that R5.2 is implemented. |
| PI-02 | Do not claim that the contract model is implemented. |
| PI-03 | Do not claim that contracts are executable. |
| PI-04 | Do not claim that contracts are runtime-enforced. |
| PI-05 | Do not claim that schema implementation exists. |
| PI-06 | Do not claim that enum implementation exists. |
| PI-07 | Do not claim that validator implementation exists. |
| PI-08 | Do not claim that workflow implementation exists. |
| PI-09 | Do not claim that storage implementation exists. |
| PI-10 | Do not claim that production readiness is achieved. |
| PI-11 | Do not claim that deployment is approved. |
| PI-12 | Do not claim that product launch is approved. |
| PI-13 | Do not claim that runtime implementation is authorized. |
| PI-14 | Do not claim that automatic durable memory writing is approved. |
| PI-15 | Do not claim that automatic Memory Graph mutation is approved. |
| PI-16 | Do not claim that Layer 14 is activated. |
| PI-17 | Do not claim that Layer 15 is activated. |
| PI-18 | Do not claim that Starfall Memory or Star-Source Memory is activated. |
| PI-19 | Do not claim that an external candidate has become system identity. |
| PI-20 | Do not interpret documentary GO, satisfaction, completeness, closure, or handoff as implementation permission. |

## 21. Risks and Failure Modes

| ID | Risk or failure mode | Required control |
| --- | --- | --- |
| RFM-01 | Design GO is overread as runtime GO. | Repeat the four status decisions and non-permission statement. |
| RFM-02 | A documentary contract is overread as an API or executable contract. | Preserve documentary-boundary language. |
| RFM-03 | Conceptual contents harden into schema fields or enums. | Keep field-like and state-like terms conceptual. |
| RFM-04 | Requirements become validator or linter behavior. | Keep satisfaction human-reviewed and non-enforced. |
| RFM-05 | Documentary order becomes workflow or state-machine behavior. | Deny automatic transitions. |
| RFM-06 | Source existence is mistaken for evidence. | Require bounded extraction and review context. |
| RFM-07 | Evidence or provenance becomes authority. | Preserve the complete non-automatic chain. |
| RFM-08 | Review becomes approval or a request becomes approval. | Require distinct human records. |
| RFM-09 | Approval becomes authorization. | Require separately bounded authorization. |
| RFM-10 | Authorization becomes adoption, mutation, or execution. | Require separate decisions for every step. |
| RFM-11 | Adoption becomes automatic durable memory writing. | Preserve the unconditional write prohibition. |
| RFM-12 | Documentary relation becomes Memory Graph mutation. | Preserve the unconditional graph-mutation prohibition. |
| RFM-13 | Composition becomes runtime inheritance or software dependency. | Keep composition documentary only. |
| RFM-14 | External methodology becomes dependency, engine, authority, or identity. | Preserve methodology-only status. |
| RFM-15 | Tool or carrier output becomes authority. | Reassert human sovereignty and named ownership. |
| RFM-16 | Completion silently starts implementation or a follow-on roadmap. | Stop at candidate handoff with no follow-on task. |

## 22. Stop Conditions

| ID | Stop condition |
| --- | --- |
| STP-01 | Work implies R5.2, R5, or v7 runtime implementation, activation, readiness, deployment, or launch. |
| STP-02 | Work implies a version change, release, tag, dependency, adapter, network, or configuration change. |
| STP-03 | Work implies an executable contract, schema, enum, parser, validator, linter runtime, or runtime type. |
| STP-04 | Work implies a state machine, workflow, contract engine, policy engine, rule engine, or automated gate. |
| STP-05 | Work implies approval, authorization, adoption, mutation, execution, evaluation, scoring, ranking, or verdict behavior. |
| STP-06 | Work implies storage, persistence, database, graph database, API, MCP, Connector, Agent, UI, or deployment. |
| STP-07 | Work implies automatic durable memory writing. |
| STP-08 | Work implies automatic Memory Graph mutation. |
| STP-09 | Evidence, review, tools, labels, contracts, or external methodologies are treated as authority or identity. |
| STP-10 | Scope, provenance, Human Owner, inherited boundary, or required human decision is absent or ambiguous. |

Stopping preserves evidence and returns the candidate to human review. It starts no repair, implementation, roadmap, or follow-on task.

## 23. Completion and Handoff Criteria

| ID | Completion and handoff criterion |
| --- | --- |
| CHC-01 | The artifact is explicitly documentation-only, design-only, candidate-only, and non-executing. |
| CHC-02 | Human Owner, bounded purpose, exact source corpus, scope, and non-goals are explicit. |
| CHC-03 | R4 closure, R5 charter decisions, v7 design-only boundaries, and sealed-version constraints are preserved. |
| CHC-04 | System, carrier, tool, and external-methodology identities remain correct. |
| CHC-05 | Contract responsibilities are independently reviewable without runtime-shaped definitions. |
| CHC-06 | Source, evidence, provenance, scope, uncertainty, conflicts, and gaps are visible. |
| CHC-07 | The full authority chain remains explicit and every arrow remains non-automatic. |
| CHC-08 | All decision gates, risks, controls, and stop conditions are resolved or explicitly deferred. |
| CHC-09 | Human review records documentary disposition without approving implementation, adoption, mutation, or execution. |
| CHC-10 | Handoff preserves DESIGN-ONLY, GO, NONE, and DEFER and creates no R5.3 package or follow-on file. |

## 24. Final Candidate Statement

This R5.2 candidate decomposes documentary responsibility boundaries for independent human review only. Contract decomposition activity is GO, and GO is not implementation permission. Implementation authority is NONE. Runtime implementation is DEFER. Contract satisfaction is not approval; contract completeness is not authorization; contract closure is not execution permission.

The source-to-execution chain remains fully separated, and no arrow is automatic. No source, evidence, candidate, proposal, review, approval request, approval, authorization, adoption, mutation, document completion, or tool output supplies execution permission. The candidate creates no implementation artifact, durable memory write, Memory Graph mutation, roadmap extension, or follow-on task.
