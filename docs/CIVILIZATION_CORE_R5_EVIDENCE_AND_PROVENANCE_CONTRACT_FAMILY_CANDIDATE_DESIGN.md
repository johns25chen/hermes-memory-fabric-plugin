# Civilization Core R5 Evidence and Provenance Contract Family Candidate Design

## 1. Candidate Status

This document is documentation-only, design-only, candidate-only, and non-executing. Its Human Owner is repository maintainer Han.

| Decision | Status | Meaning |
| --- | --- | --- |
| R5.3 candidate status | `DESIGN-ONLY` | Available only for documentary human review. |
| evidence and provenance activity | `GO` | The bounded candidate design may be reviewed; GO is not implementation permission. |
| implementation authority | `NONE` | No implementation authority is granted. |
| runtime implementation | `DEFER` | Runtime implementation remains deferred. |

## 2. Purpose

This candidate expands only the evidence-and-provenance contract family identified by R5.1 and decomposed by R5.2. It assigns documentary responsibilities for source identity and preservation, evidence qualification and packets, provenance and derivation traces, claims and gaps, uncertainty and conflict, human ownership, authority separation, and non-runtime composition.

## 3. Scope

The scope is conceptual documentation for human inspection. It does not fetch, ingest, parse, extract, transform, store, persist, validate, score, rank, approve, authorize, adopt, mutate, or execute anything.

| Principle | Documentary rule |
| --- | --- |
| EPI-01 | Source existence alone does not make evidence; source is not evidence by existence alone. |
| EPI-02 | Evidence supports a claim but does not automatically prove it; evidence is not truth by declaration; relevance is not truth; a citation is not proof by itself. |
| EPI-03 | Evidence is not approval; evidence is not authorization; confidence is not authority. |
| EPI-04 | Provenance is traceability, not correctness; provenance is not approval; provenance is not authorization. |
| EPI-05 | Completeness is not correctness; freshness is not validity; repetition is not independent corroboration. |
| EPI-06 | A derivation is not adoption; a transformation is not mutation permission. |
| EPI-07 | An evidence packet is a documentary review aid; an evidence packet is not a stored runtime object. |
| EPI-08 | Missing evidence must remain visible; conflicting evidence must remain visible; uncertainty must not be silently converted into certainty. |

## 4. Source Corpus

This candidate reads and preserves exactly these 12 sources without rewriting, renaming, normalizing, migrating, superseding, or updating them:

1. `docs/CIVILIZATION_CORE_R5_DESIGN_ONLY_WORKSTREAM_CHARTER.md`
2. `docs/CIVILIZATION_CORE_R5_CONTRACT_DECOMPOSITION_CANDIDATE_DESIGN.md`
3. `docs/CIVILIZATION_CORE_R4_FINAL_CLOSURE_AND_R5_DESIGN_ONLY_ENTRY_REVIEW.md`
4. `docs/CIVILIZATION_CORE_V7_DESIGN_ONLY_CHARTER.md`
5. `docs/CIVILIZATION_CORE_KNOWLEDGE_COMPILATION_CANDIDATE_DESIGN.md`
6. `docs/CIVILIZATION_CORE_ASSOCIATIVE_RECALL_CANDIDATE_DESIGN.md`
7. `docs/CIVILIZATION_CORE_MEMORY_OPERATIONS_CANDIDATE_DESIGN.md`
8. `docs/CIVILIZATION_CORE_MEMORY_EVALUATION_CANDIDATE_CLOSURE_REVIEW.md`
9. `docs/CIVILIZATION_CORE_EVALUATION_VOCABULARY_NORMALIZATION_REVIEW.md`
10. `docs/CIVILIZATION_CORE_DECISION_GATE_CHECKLIST.md`
11. `docs/CIVILIZATION_CORE_PRODUCT_NARRATIVE_PACKAGE.md`
12. `docs/CIVILIZATION_CORE_EXTERNAL_CANDIDATE_COMPARISON.md`

## 5. Inherited R5 Decisions

`R5 workstream status: OPEN-DESIGN`; `R5 design-only activity: GO`; `R5 implementation authority: NONE`; `R5 runtime implementation: DEFER`. GO is not implementation permission.

Civilization Core is the governance kernel and memory constitution. Subspace Memory System is the engineering carrier. Hermes Memory Fabric is the current repository carrier. Codex, OpenClaw, and Hermes are tools or carriers, not authority.

`v6.16.0` remains sealed; there is no `v6.17`, no `v7.0.0` release, and no tag. R4 corridor closure remains `CLOSE`. R5.2 remains design-only and closed as a documentary candidate. T9 remains GO for future v7 design-only exploration, while v7 runtime implementation remains DEFER. T10 productization remains roadmap-only. Automatic durable memory writing and automatic Memory Graph mutation remain prohibited.

## 6. Relationship to R5.2 Contract Decomposition

R5.2 names this family and separates it from candidate-object, lifecycle, evaluation, governance, and composition concerns. This candidate supplies only the documentary responsibilities inside that boundary. It neither reopens R5.2 nor converts decomposition into types, behavior, storage, enforcement, or implementation.

## 7. Evidence and Provenance Contract Family Identity

This family makes the basis, limits, lineage, conflicts, gaps, and human review of documentary claims inspectable. It does not determine truth, make decisions, confer authority, or create capability. Its conceptual attributes and categories are prose responsibilities, not schema fields, database columns, API properties, enums, or stored records.

## 8. Source Preservation Boundary

Raw-source meaning and historical wording remain preserved by reference. Preservation means keeping a reviewable route back to the source context; it does not mean copying, fetching, ingesting, persisting, normalizing, or converting the source. A missing or inaccessible raw-source reference remains visible and is never fabricated.

## 9. Source Identity Requirements

| Requirement | Documentary responsibility |
| --- | --- |
| SIR-01 | Record a human-readable source title. |
| SIR-02 | Describe the source type. |
| SIR-03 | Describe the source origin without implying ownership. |
| SIR-04 | Bound the source scope. |
| SIR-05 | Name the source owner or custodian when known; otherwise preserve the unknown. |
| SIR-06 | Describe collection or observation context when known. |
| SIR-07 | Preserve a raw-source reference without fetching or storing the source. |
| SIR-08 | State source limitations. |
| SIR-09 | State source accessibility status. |
| SIR-10 | State source freshness context without treating freshness as validity. |

These are conceptual documentary attributes only, not schema fields, database columns, API properties, enums, or stored records.

## 10. Evidence Qualification Requirements

| Requirement | Human-review category responsibility |
| --- | --- |
| EQR-01 | Distinguish direct evidence. |
| EQR-02 | Distinguish indirect evidence. |
| EQR-03 | Distinguish derived evidence. |
| EQR-04 | Distinguish contextual evidence. |
| EQR-05 | Distinguish corroborating evidence. |
| EQR-06 | Distinguish conflicting evidence. |
| EQR-07 | Distinguish incomplete evidence. |
| EQR-08 | Distinguish stale evidence. |
| EQR-09 | Distinguish unavailable evidence. |
| EQR-10 | Distinguish rejected evidence and retain the human reason. |
| EQR-11 | Distinguish unknown evidence status. |
| EQR-12 | Distinguish evidence requiring renewed human review. |

These are human-review categories only. They do not create an automatic classifier, score, rank, verdict, validator, or enforcement surface.

## 11. Evidence Packet Candidate Requirements

| Requirement | Documentary responsibility |
| --- | --- |
| EPC-01 | State the bounded question or claim. |
| EPC-02 | List relevant source references. |
| EPC-03 | Present manually extracted or summarized evidence as documentary content. |
| EPC-04 | Show the provenance path. |
| EPC-05 | Record derivation notes. |
| EPC-06 | Expose uncertainty. |
| EPC-07 | Expose gaps. |
| EPC-08 | Expose conflicts. |
| EPC-09 | Name the human reviewer. |
| EPC-10 | Record a documentary disposition that grants no approval or authority. |

An evidence packet candidate does not fetch or ingest sources; scrape; crawl; parse, extract, summarize, or validate automatically; score; rank; produce a verdict; approve; authorize; persist; mutate the Memory Graph; dispatch; or execute work.

## 12. Provenance Chain Requirements

The documentary chain is `source → observation or extraction context → evidence item → derivation or transformation note → claim support → human review`. No arrow is automatic.

| Requirement | Required distinction |
| --- | --- |
| PCR-01 | Distinguish source from evidence. |
| PCR-02 | Distinguish source location from source ownership. |
| PCR-03 | Distinguish observation from interpretation. |
| PCR-04 | Distinguish extraction from validation. |
| PCR-05 | Distinguish derivation from truth. |
| PCR-06 | Distinguish transformation from mutation. |
| PCR-07 | Distinguish claim support from claim acceptance. |
| PCR-08 | Distinguish traceability from correctness. |
| PCR-09 | Distinguish provenance completeness from authorization. |
| PCR-10 | Distinguish human review from approval. |
| PCR-11 | Distinguish approval from authorization. |
| PCR-12 | Distinguish authorization from adoption or execution. |

## 13. Derivation and Transformation Trace

| Rule | Documentary boundary |
| --- | --- |
| DTR-01 | A derivation note explains how documentary content was produced; it is not executable logic. |
| DTR-02 | A transformation description is not a transformation engine. |
| DTR-03 | Summarization description is not automatic summarization. |
| DTR-04 | Normalization description is not terminology migration. |
| DTR-05 | Mapping description is not schema mapping. |
| DTR-06 | Correlation is not causation. |
| DTR-07 | Aggregation is not independent corroboration. |
| DTR-08 | Inference must remain labeled as inference. |
| DTR-09 | Unknown derivation must remain unknown; unverifiable derivation must not be fabricated. |
| DTR-10 | Transformed evidence must retain links to its source context. |

## 14. Claims, Support, and Gaps

| Rule | Required separation or prohibition |
| --- | --- |
| CSG-01 | Distinguish a claim from supporting evidence. |
| CSG-02 | Distinguish contradicting evidence from unresolved evidence. |
| CSG-03 | Distinguish an evidence gap from a provenance gap. |
| CSG-04 | Distinguish uncertainty from a scope limitation. |
| CSG-05 | Distinguish human judgment from documentary disposition. |
| CSG-06 | Do not silently fill gaps or invent missing provenance. |
| CSG-07 | Do not collapse conflicting evidence or convert unknown to false or true. |
| CSG-08 | Do not convert incomplete to complete; do not treat lack of evidence as evidence of absence without explicit human reasoning. |
| CSG-09 | Do not treat confidence language as authority or review readiness as approval. |
| CSG-10 | Do not treat packet completion as authorization. |

## 15. Uncertainty and Conflict Handling

| Rule | Documentary responsibility |
| --- | --- |
| UCR-01 | Label uncertainty in language suitable for human review. |
| UCR-02 | Keep each material conflict visible. |
| UCR-03 | Keep missing evidence visible. |
| UCR-04 | Keep missing provenance visible. |
| UCR-05 | Preserve unknown status rather than guessing. |
| UCR-06 | Preserve scope and temporal limitations. |
| UCR-07 | Record dissent without collapsing it into consensus. |
| UCR-08 | Require human reasoning for any documentary conflict disposition. |

## 16. Human Review and Ownership

| Rule | Documentary responsibility |
| --- | --- |
| HRO-01 | A named Human Owner controls scope. |
| HRO-02 | A human identifies the bounded review question. |
| HRO-03 | A human determines whether a source is relevant to that question. |
| HRO-04 | A human assigns or revises qualification categories. |
| HRO-05 | A human reviews derivation and transformation notes. |
| HRO-06 | A human reviews uncertainty, conflicts, gaps, and limitations. |
| HRO-07 | A human records documentary disposition. |
| HRO-08 | Documentary review never silently supplies approval or authorization. |
| HRO-09 | Ownership changes require explicit human recording. |
| HRO-10 | Unresolved ownership or review scope stops handoff. |

## 17. Authority Separation

The authority chain is `source → evidence → candidate → proposal → review → approval request → approval → authorization → adoption → mutation → execution`. No arrow is automatic.

| Rule | Authority boundary |
| --- | --- |
| ASR-01 | Source is not evidence by existence alone; evidence is not candidate approval. |
| ASR-02 | Candidate is not proposal acceptance. |
| ASR-03 | Proposal is not mutation. |
| ASR-04 | Review is not approval. |
| ASR-05 | Approval request is not approval. |
| ASR-06 | Approval is not authorization. |
| ASR-07 | Authorization is not adoption. |
| ASR-08 | Authorization is not mutation or execution. |
| ASR-09 | Adoption is not mutation; mutation is not execution unless separately authorized. |
| ASR-10 | Document completion is not execution permission. |

## 18. External Methodology Boundary

`llm_wiki`, M-Flow, and GBrain may inform documentary methodology only. Merely naming them does not make them evidence sources. They are not dependencies, adapters, runtimes, writers, storage systems, provenance engines, evidence engines, validators, schemas, authorities, identities, or completion conditions. Methodology absorption is not runtime adoption.

## 19. Contract Composition and Non-Inheritance

| Rule | Documentary boundary |
| --- | --- |
| CNR-01 | Contract composition is documentary composition only; evidence-contract composition is not runtime inheritance. |
| CNR-02 | Provenance dependency is not software dependency. |
| CNR-03 | Source linkage is not network integration. |
| CNR-04 | Evidence linkage is not graph mutation. |
| CNR-05 | Provenance linkage is not database relationship creation. |
| CNR-06 | Packet composition is not object persistence. |
| CNR-07 | Contract satisfaction is not approval; contract completeness is not authorization. |
| CNR-08 | Contract closure is not execution permission. |

## 20. Decision Gates

| Gate | Passage condition |
| --- | --- |
| DG-01 | Scope, Human Owner, sources, and non-goals are explicit. |
| DG-02 | All inherited R5, R4, v7, version, and carrier boundaries remain intact. |
| DG-03 | Source identity and raw-source preservation responsibilities are reviewable. |
| DG-04 | Evidence qualifications, packets, provenance, and derivation remain documentary. |
| DG-05 | Claims, support, uncertainty, conflicts, and gaps remain visibly separate. |
| DG-06 | Human review, approval, authorization, adoption, mutation, and execution remain separate. |
| DG-07 | No runtime, schema, enum, persistence, integration, or automated behavior is implied. |
| DG-08 | Human handoff confirms documentary completeness while authority remains absent and runtime remains deferred. |

Gate failure produces `HOLD`, `DEFER`, or `STOP` for documentary review; it triggers no automatic repair or follow-on work.

## 21. Prohibited Interpretations

| Interpretation | Explicit prohibition |
| --- | --- |
| PI-01 | Do not claim R5.3 is implemented or runtime implementation is authorized. |
| PI-02 | Do not claim an evidence engine or provenance engine exists. |
| PI-03 | Do not claim evidence is automatically extracted, validated, or scored. |
| PI-04 | Do not claim provenance is automatically generated. |
| PI-05 | Do not claim evidence packets are persisted or provenance records are stored. |
| PI-06 | Do not claim schema, enum, validator, workflow, or storage implementation exists. |
| PI-07 | Do not claim production readiness, deployment approval, or product launch approval. |
| PI-08 | Do not claim automatic durable memory writing or automatic Memory Graph mutation is approved. |
| PI-09 | Do not claim Layer 14, Layer 15, Starfall Memory, or Star-Source Memory is activated. |
| PI-10 | Do not claim an external candidate has become system identity. |
| PI-11 | Do not infer a runtime, evidence engine, provenance engine, or source-ingestion engine. |
| PI-12 | Do not infer a scraper, crawler, parser, extractor, summarizer, transformer, normalizer, or mapper. |
| PI-13 | Do not infer a classifier, validator, linter runtime, schema, enum, state machine, workflow engine, or contract engine. |
| PI-14 | Do not infer a policy, rule, approval, authorization, adoption, mutation, or execution engine. |
| PI-15 | Do not infer an evaluator runtime, evaluation runner, benchmark runner, scoring engine, ranking engine, or verdict engine. |
| PI-16 | Do not infer storage, persistence, database, graph database, index, or registry implementation. |
| PI-17 | Do not infer an API, MCP, Connector, Agent, UI, deployment, dependency, adapter, or network integration. |
| PI-18 | Do not infer source fetch, source ingestion, automatic evidence extraction, or automatic provenance generation. |
| PI-19 | Do not infer automatic durable memory write or automatic Memory Graph mutation. |
| PI-20 | Do not infer that evidence, provenance, completeness, confidence, freshness, citation, packet completion, or document completion grants truth or authority. |

## 22. Risks and Failure Modes

| Risk | Required control |
| --- | --- |
| RFM-01 | Source existence is mistaken for evidence; require qualification and human reasoning. |
| RFM-02 | Source reference loses raw context; preserve a reviewable raw-source reference or visible gap. |
| RFM-03 | Source location is mistaken for ownership; record them separately. |
| RFM-04 | Evidence is mistaken for truth; preserve claim and support separation. |
| RFM-05 | Citation is mistaken for proof; require contextual human review. |
| RFM-06 | Provenance is mistaken for correctness; repeat its traceability-only role. |
| RFM-07 | Complete provenance is mistaken for authorization; preserve the authority chain. |
| RFM-08 | Derivation description hardens into executable logic; keep it documentary. |
| RFM-09 | Transformation language implies mutation permission; state the non-mutation boundary. |
| RFM-10 | Repeated evidence is mistaken for independent corroboration; expose common origin. |
| RFM-11 | Conflict is collapsed or dissent hidden; retain each material conflict. |
| RFM-12 | Unknown or missing evidence is fabricated; stop and preserve the gap. |
| RFM-13 | Qualification becomes automatic scoring or verdict; keep it human-review-only. |
| RFM-14 | Packet completion is mistaken for approval; record documentary disposition only. |
| RFM-15 | Composition becomes runtime inheritance or persistence; preserve non-inheritance rules. |
| RFM-16 | Candidate handoff starts implementation or a roadmap; stop at human documentary review. |

## 23. Stop Conditions

| Condition | Required response |
| --- | --- |
| STP-01 | Stop if scope, Human Owner, or source identity is missing or ambiguous. |
| STP-02 | Stop if raw-source preservation or accessibility status cannot be represented honestly. |
| STP-03 | Stop if evidence qualification is treated as automatic classification, score, rank, or verdict. |
| STP-04 | Stop if gaps, conflicts, uncertainty, or dissent would be hidden or fabricated. |
| STP-05 | Stop if provenance or derivation is treated as correctness, proof, approval, or authority. |
| STP-06 | Stop if review is collapsed into approval, authorization, adoption, mutation, or execution. |
| STP-07 | Stop if contract language is converted into schema, enum, runtime type, workflow, or enforcement. |
| STP-08 | Stop if source or evidence linkage implies fetch, ingestion, storage, network integration, or graph mutation. |
| STP-09 | Stop if version, tag, dependency, adapter, deployment, or runtime activity is proposed. |
| STP-10 | Stop if handoff would create implementation permission or follow-on work. |

Stopping preserves the documentary record for human review and performs no repair, write, mutation, dispatch, or execution.

## 24. Completion and Handoff Criteria

| Criterion | Documentary completion condition |
| --- | --- |
| CHC-01 | The artifact remains documentation-only, design-only, candidate-only, and non-executing. |
| CHC-02 | The exact source corpus is preserved without source-document change. |
| CHC-03 | All inherited R5, R4, v7, version, identity, and carrier boundaries are explicit. |
| CHC-04 | Source identity and raw-source preservation responsibilities are complete for human review. |
| CHC-05 | Evidence qualifications and packet responsibilities remain human-owned and documentary. |
| CHC-06 | Provenance, derivation, transformation, claim support, and acceptance remain separate. |
| CHC-07 | Gaps, conflicts, uncertainty, limitations, and unknowns remain visible. |
| CHC-08 | Review, approval, authorization, adoption, mutation, and execution remain separate. |
| CHC-09 | Composition creates no schema, enum, runtime, persistence, dependency, integration, or graph relationship. |
| CHC-10 | Human handoff records documentary sufficiency only; implementation authority remains absent and runtime remains deferred. |

Completion is a review aid, not approval, authorization, adoption, mutation, execution permission, or permission to begin another task.

## 25. Final Candidate Statement

This candidate defines only the documentary responsibilities of the R5 evidence-and-provenance contract family. It preserves sources, evidence, claims, provenance, review, approval, authorization, adoption, mutation, and execution as separate concepts; no arrow in either documentary chain is automatic.

`R5.3 candidate status: DESIGN-ONLY`. `evidence and provenance activity: GO`. `implementation authority: NONE`. `runtime implementation: DEFER`. `R5 workstream status: OPEN-DESIGN`. `R5 design-only activity: GO`. `R5 implementation authority: NONE`. `R5 runtime implementation: DEFER`. GO is not implementation permission.

This document creates no implementation or runtime capability. Automatic durable memory writing and automatic Memory Graph mutation remain prohibited. It ends at documentary human handoff and creates no roadmap or follow-on task.
