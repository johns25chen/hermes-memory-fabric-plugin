# Civilization Core R2 Product Direction and MVP Decision

## 1. Decision Status and Roadmap Position

### Repository-established facts and boundaries

- R0 is complete.
- R1 is complete at PR #335, and its repository-effective baseline is `b2576e4d9de1088de3fd7f4f8dfb53f127a44f41`.
- The post-IDG master execution roadmap places R2 after R1 and before R3.
- The package version remains `6.16.0`; V6 continuation remains `NEVER`; V7 runtime implementation remains `DEFER`.
- Implementation readiness is not established, and implementation, deployment, launch, release, version, and tag authority remain absent.

### New R2 decision

R2 is the current bounded documentary decision stage. This document selects the product direction and bounded MVP scope stated below. The decision becomes repository-effective only upon merge.

### Downstream boundary

R3 does not start automatically. This decision creates no implementation authority and authorizes no evidence gathering, research, testing, prototype, runtime, security execution, deployment, release, version, or tag work.

## 2. Product Direction Decision

The selected primary product direction is **Civilization Core Governed Memory Control Plane**.

`PRIMARY_PRODUCT_DIRECTION=CIVILIZATION-CORE-GOVERNED-MEMORY-CONTROL-PLANE`

This direction defines one governed human-control product, not three unrelated products. Its initial product surfaces may eventually combine:

- Operator Console;
- Memory Governance UI; and
- Evidence / Review / Approval Dashboard.

These names describe possible surfaces within the selected product direction. They do not claim that any surface is designed, implemented, validated, operational, or authorized for implementation.

## 3. Target User

The primary target user is **a human operator or small technical team responsible for long-running, AI-assisted, multi-project or multi-agent memory workflows**.

More precisely, the initial user is someone who must inspect, approve, correct, revoke, and audit memory without surrendering authority to an AI system. This is the selected target-user definition for R2, not evidence of current users, interviews, adoption, or validation.

## 4. Concrete User Problem

Existing AI memory workflows often make it difficult to distinguish:

- source evidence;
- recalled material;
- candidate memory;
- reviewed memory;
- approved memory;
- durable adoption; and
- execution authority.

The product must make these states visible and prevent hidden promotion from one state to another. Visibility does not collapse their meanings: evidence is not approval, review is not approval, approval is not execution authority, and adoption does not itself authorize action.

## 5. Five Core MVP Workflows

These workflows are conceptual product behavior only. They create no technical API, schema, storage format, or code contract.

### 1. Source and Provenance Inspection

- **User goal:** Understand where recalled or proposed material came from, how it was derived, and what uncertainty, conflicts, or limits accompany it.
- **Conceptual input:** Source-linked material, provenance context, derivation context, relevant evidence, counterevidence, uncertainty, and scope.
- **Required human decision:** Determine whether the source basis is sufficient to continue to candidate creation, needs more context, or should be held or rejected.
- **Expected governed output:** A visible, scoped inspection record that preserves source identity, derivation, uncertainty, conflicts, limits, and the human disposition.
- **Prohibited automatic behavior:** No source is treated as true, approved, adopted, written durably, or made executable merely because it is visible or recalled.

### 2. Candidate Memory Creation

- **User goal:** Form a reviewable memory proposal without prematurely turning it into adopted memory.
- **Conceptual input:** Inspected source material, provenance, proposed memory content, intended scope, uncertainty, conflicts, and rationale.
- **Required human decision:** Decide whether to create a bounded candidate for review and identify its intended project or role scope.
- **Expected governed output:** A distinguishable candidate-memory item linked to its source basis, intended scope, uncertainty, and creation decision.
- **Prohibited automatic behavior:** Candidate creation must not automatically approve, adopt, persist as authoritative durable memory, mutate the Memory Graph, or grant execution authority.

### 3. Human Review and Conflict Assessment

- **User goal:** Evaluate a candidate against its evidence, counterevidence, existing memory, uncertainty, and conflicts.
- **Conceptual input:** The candidate, provenance, evidence, counterevidence, relevant adopted memory, uncertainty, conflict context, and scope.
- **Required human decision:** Assess whether the candidate is supportable, conflicting, incomplete, out of scope, or ready for an explicit approval or rejection decision.
- **Expected governed output:** A visible review state that records findings, unresolved conflicts, uncertainty, limits, and the reviewing human or delegated human decision trace.
- **Prohibited automatic behavior:** Review must not resolve truth, select a conflict winner, approve, reject, adopt, correct, revoke, delete, or trigger action automatically.

### 4. Explicit Scoped Approval or Rejection

- **User goal:** Make an explicit human disposition for a reviewed candidate within a defined scope.
- **Conceptual input:** The reviewed candidate, source and evidence context, review findings, conflicts, uncertainty, intended scope, and applicable authority limits.
- **Required human decision:** Explicitly approve or reject the candidate for a stated project or role scope, or withhold a decision when requirements are not met.
- **Expected governed output:** A traceable approval or rejection record containing the responsible Human Owner or delegated human decision trace, scope, basis, exclusions, and unresolved limits. Approval may support a separately governed adoption record; it is not execution authority.
- **Prohibited automatic behavior:** No automatic approval, scope expansion, durable adoption, authority transfer, execution, routing, or agent action may follow from review status or model output.

### 5. Audit, Correction, Revocation, and Deletion

- **User goal:** Inspect memory history and retain human control over mistakes, changed circumstances, withdrawn decisions, and deletion needs.
- **Conceptual input:** Adopted memory and its provenance, decision history, lifecycle history, correction or revocation context, deletion request, scope, risks, and authority context.
- **Required human decision:** Decide whether a scoped correction, revocation, or deletion should be authorized under the applicable later-established policy and authority, or whether the request must be held or rejected.
- **Expected governed output:** An auditable lifecycle record preserving the request, human decision, scope, prior state reference, resulting governed disposition, and deletion traceability.
- **Prohibited automatic behavior:** No model or agent may silently correct, revoke, delete, rewrite, hide, detach, mutate, or execute against memory; this R2 decision does not itself authorize any lifecycle operation.

## 6. MVP Scope

The bounded MVP may eventually provide:

- source and provenance visibility;
- candidate-memory queue;
- evidence and uncertainty display;
- human review state;
- explicit approval or rejection;
- project- or role-scoped adoption record;
- audit history; and
- correction, revocation, and deletion controls.

This is a product decision scope, not implemented capability. The listed functions are bounded subjects for later validation and possible separately authorized implementation; they are not architecture or implementation requirements.

## 7. Explicit Non-Goals

The first MVP and this R2 decision expressly exclude:

- autonomous durable memory write;
- self-authorization;
- automatic approval;
- hidden execution or agent action;
- unrestricted Memory Graph mutation;
- enterprise multi-tenancy in the first MVP;
- cross-organization federation in the first MVP;
- any compliance certification claim;
- an active Layer 15 or Star-Source runtime;
- a full Personal Brain, Team Memory, Agent Constitution, or Enterprise suite in the first MVP;
- package-version change, release, deployment, or tag;
- implementation architecture, APIs, schemas, storage formats, dependencies, schedules, pricing, or launch decisions; and
- any claim of product completion, product-market fit, readiness, security, reliability, performance, deployment, or release.

## 8. Product Value Hypothesis

The bounded product value hypothesis is:

> Human operators will trust and use AI memory more effectively when provenance, candidate state, uncertainty, human decisions, and reversible lifecycle controls are visible in one governed control plane.

This is a hypothesis requiring R3 evidence, not a validated claim.

## 9. Provisional R3 Validation Targets

The following are provisional evidence targets for a separately authorized R3, not current achievements:

- 100% of adopted memory records must retain visible source provenance.
- 100% of adopted memory records must retain an explicit Human Owner or delegated human decision trace.
- Unauthorized durable adoption target: zero in controlled evaluation.
- Correction, revocation, and deletion operations must remain auditable.
- Target users must be able to distinguish evidence, candidate, review, approval, adoption, and execution states during usability evaluation.
- The governed workflow must show measurable value over an ungoverned memory workflow.

No measurements, study results, users, revenue, performance, or market evidence are claimed or inferred here. Measurement methods and success thresholds beyond these provisional targets remain subjects for the bounded R3 charter.

## 10. Data, Permission, and Governance Boundaries

The product direction requires conceptual separation among:

- **Source:** Originating material or context, kept distinguishable from later interpretation.
- **Evidence:** Source-linked support, counterevidence, derivation, uncertainty, conflicts, gaps, and limits used for inspection and review.
- **Candidate memory:** A proposed memory item that is neither approved nor adopted merely by existing.
- **Review:** Human inspection and conflict assessment that does not itself approve, authorize, adopt, mutate, or execute.
- **Human decision:** An explicit, attributable, scoped human disposition whose effect does not exceed its recorded authority.
- **Adopted memory:** Memory accepted within an explicit project or role scope through a governed process, without gaining execution authority.
- **Lifecycle event:** A traceable correction, revocation, deletion, or other bounded lifecycle disposition performed only under separately established authority.
- **Audit record:** A preserved account of provenance, review, decisions, scope, and lifecycle history; it is not permission to act.

Any future realization must require explicit scope, least authority, human approval, provenance preservation, reversible correction and revocation, deletion traceability, and no hidden authority transfer. These are conceptual product and governance boundaries, not implementation schemas. The mechanisms, policies, and authorities needed to realize them remain undecided and unauthorized.

## 11. R3 Validation Plan

If separately chartered, R3 may gather future evidence in these categories only as specifically authorized:

- target-user problem interviews;
- workflow and usability validation;
- technical feasibility assessment;
- prototype or controlled demonstration only if separately authorized;
- safety, privacy, security, and threat-model evidence;
- operating-model and recovery evidence;
- comparative controlled evaluation; and
- success-threshold decision.

R3 must preserve provenance, disclose gaps and limitations, and distinguish demonstrations from production capability. No R3 evidence work starts through this document.

## 12. Stage Exit Criteria

R2 is complete upon merge only when all of the following are fixed by the repository-effective decision:

- primary product direction;
- target user;
- concrete problem;
- five core workflows;
- MVP scope;
- non-goals;
- provisional success metrics;
- data, permission, and governance boundaries;
- product hypothesis; and
- R3 validation plan.

Completion of R2 means completion of this bounded documentary decision only. It does not establish product, evidence, readiness, implementation, operational, security, deployment, or release completion.

## 13. R2 Closeout and R3 Boundary

Merge completes R2 and makes R3 the next planned stage. R3 does not start automatically and requires a separate bounded evidence-and-readiness charter. R5 implementation authorization cannot be considered before R3 and R4 have completed through their separate gates. No implementation code is authorized by this decision.

Historical productization recommendations and historical decision frames remain source context rather than silently approved requirements. Only the bounded selections expressly stated in this document become the R2 product decision upon merge; future mechanisms and implementation work remain unauthorized.

## 14. Final Machine State

```text
ROADMAP_ID=POST-IDG-MASTER-EXECUTION-ROADMAP
ROADMAP_BASE_COMMIT=b2576e4d9de1088de3fd7f4f8dfb53f127a44f41
R0_STATUS=COMPLETE
R1_STATUS=COMPLETE
R2_STATUS=COMPLETE-UPON-MERGE
CURRENT_STAGE=R2
PRIMARY_PRODUCT_DIRECTION=CIVILIZATION-CORE-GOVERNED-MEMORY-CONTROL-PLANE
TARGET_USER=HUMAN-OPERATOR-OF-AI-MEMORY-WORKFLOWS
CORE_WORKFLOW_COUNT=5
MVP_SCOPE=BOUNDED
NON_GOALS=DEFINED
SUCCESS_METRICS=PROVISIONAL-R3-VALIDATION-TARGETS
DATA_PERMISSION_GOVERNANCE_BOUNDARIES=DEFINED
PRODUCT_HYPOTHESIS=REQUIRES-R3-VALIDATION
R3_VALIDATION_PLAN=DEFINED-NOT-STARTED
NEXT_PLANNED_STAGE=R3
R3_STATUS=NOT-STARTED
R3_AUTOMATIC_START=NO
R4_STATUS=NOT-STARTED
R5_STATUS=NOT-STARTED
R6_STATUS=NOT-STARTED
R7_STATUS=NOT-STARTED
R8_STATUS=NOT-STARTED
R9_STATUS=NOT-STARTED
R10_STATUS=NOT-STARTED
R11_STATUS=NOT-STARTED
R12_STATUS=NOT-STARTED
R13_STATUS=NOT-STARTED
HUMAN_OWNER_IMPLEMENTATION_DECISION=DEFER
IMPLEMENTATION_READINESS=NOT-ESTABLISHED
IMPLEMENTATION_START=NO
PRODUCT_IMPLEMENTATION=NOT-AUTHORIZED
IMPLEMENTATION_AUTHORITY=NONE
DEPLOYMENT_AUTHORITY=NONE
LAUNCH_AUTHORITY=NONE
RELEASE_AUTHORITY=NONE
VERSION_AUTHORITY=NONE
TAG_AUTHORITY=NONE
PACKAGE_VERSION=6.16.0
V6_CONTINUATION=NEVER
V7_RUNTIME_IMPLEMENTATION=DEFER
AUTOMATIC_SUCCESSOR_WORK=NONE
NEXT_REPOSITORY_TASK_CLASS=R3-PRE-IMPLEMENTATION-EVIDENCE-AND-READINESS
ROADMAP_DRIFT_CONTROL=ACTIVE
```
