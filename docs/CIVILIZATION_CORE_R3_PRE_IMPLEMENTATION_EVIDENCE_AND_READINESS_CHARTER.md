# Civilization Core R3 Pre-Implementation Evidence and Readiness Charter

## 1. Charter Status and Roadmap Position

### Current facts

- The repository-effective baseline is `13e307bca6095487c95dcf20d143c5e7293d2332`.
- R0, R1, and R2 are complete. R2 closed at PR #336 and the repository-effective baseline above.
- R3 is the current roadmap stage. R4 through R13 remain `NOT-STARTED`.
- This documentation-only charter becomes effective only upon merge. Its merge completes only R3.0.
- Package version remains `6.16.0`; V6 continuation remains `NEVER`; V7 runtime implementation remains `DEFER`.

### Current authority and readiness boundary

R3 evidence work does not start merely because an evidence category or substage is named here. Each evidence task requires a separate bounded task. Implementation readiness remains `NOT-ESTABLISHED`, product implementation remains `NOT-AUTHORIZED`, and implementation authority remains `NONE`. R4 does not begin automatically.

## 2. Inherited R2 Decision

This charter preserves the R2 decision without reopening, replacing, or expanding it.

### Primary product direction and target user

- **Primary product direction:** Civilization Core Governed Memory Control Plane.
- **Target user:** a human operator or small technical team responsible for long-running, AI-assisted, multi-project or multi-agent memory workflows.

### Five inherited MVP workflows

1. **Source and Provenance Inspection:** inspect source identity, derivation, evidence, counterevidence, uncertainty, conflicts, limits, scope, and the human disposition without treating recalled or visible material as true, approved, adopted, durable, or executable.
2. **Candidate Memory Creation:** create a distinguishable, scoped, source-linked proposal for review without automatic approval, adoption, authoritative persistence, Memory Graph mutation, or execution authority.
3. **Human Review and Conflict Assessment:** evaluate a candidate against its evidence, counterevidence, adopted memory, uncertainty, conflicts, and scope while keeping review distinct from resolution, approval, rejection, adoption, lifecycle action, or execution.
4. **Explicit Scoped Approval or Rejection:** record an attributable human approval, rejection, or withheld decision with its scope, basis, exclusions, authority limits, and unresolved limits; approval is not execution authority and does not automatically cause adoption or action.
5. **Audit, Correction, Revocation, and Deletion:** inspect history and record governed, scoped human lifecycle dispositions with prior-state and deletion traceability, without silent model or agent mutation or execution.

### Bounded MVP scope

The bounded MVP may eventually provide source and provenance visibility; a candidate-memory queue; evidence and uncertainty display; human review state; explicit approval or rejection; a project- or role-scoped adoption record; audit history; and correction, revocation, and deletion controls. These are subjects for validation and possible separately authorized implementation, not existing capabilities or prescribed technical designs.

### Explicit non-goals

The first MVP and the inherited decision exclude:

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

### Provisional R3 validation targets

- 100% visible source provenance for adopted records.
- 100% explicit human-decision trace for adopted records.
- Zero unauthorized durable adoption in controlled evaluation.
- Auditable correction, revocation, and deletion.
- Users can distinguish evidence, candidate, review, approval, adoption, and execution states.
- Measurable value over an ungoverned memory workflow.

These are inherited, provisional, and unachieved targets. Section 11 preserves their evidence boundary.

### Product hypothesis requiring R3 validation

> Human operators will trust and use AI memory more effectively when provenance, candidate state, uncertainty, human decisions, and reversible lifecycle controls are visible in one governed control plane.

This remains a hypothesis requiring R3 validation, not a validated claim.

## 3. R3 Purpose

R3 is the stage that must establish substantive, traceable, decision-relevant evidence for:

- product need and user value;
- technical feasibility;
- operating model and recovery;
- security and privacy; and
- concrete external dependencies when they actually exist.

R3 must distinguish observed facts from interpretations, future requirements, and unachieved thresholds. Additional internal narrative alone cannot establish readiness. R3 creates an evidence basis for later independent consideration; it does not itself make a readiness or implementation decision.

## 4. Evidence Quality Standard

Every R3 evidence artifact must identify:

- the question being tested;
- the method;
- the source or participant;
- the date or bounded observation period;
- the scope;
- the observed result;
- counterevidence;
- uncertainty and limitations;
- provenance; and
- a `PASS`, `HOLD`, `DEFER`, `FAIL`, or `NOT-TESTED` disposition.

The artifact must keep raw observation, analysis, and disposition distinguishable and must make material conflicts traceable. Assertion, opinion, document count, checksum, merge status, and repeated restatement are not substantive evidence by themselves.

## 5. R3 Ordered Substage Map

The substages below are controlling and ordered. A substage name permits no work by itself.

### R3.0 — Evidence and Readiness Charter Adoption

- **Purpose:** Adopt the evidence categories, quality rules, substage order, exit threshold, and authority boundaries governing R3.
- **Entry conditions:** R2 is repository-effective and complete; its product direction and bounded MVP decision are available; the charter task is separately bounded to the single documentation target.
- **Permitted evidence work:** Read the allowed repository sources, reconcile inherited decisions, define future evidence requirements, and validate this charter as documentation.
- **Required outputs:** This self-contained charter, its ordered substage map, anti-drift controls, closeout deliverables, and machine state.
- **Minimum exit criteria:** The charter is merged at the stated baseline without code, evidence gathering, research, testing, implementation, authority change, or scope drift.
- **Prohibited interpretations:** Charter adoption is not substantive evidence, readiness, validation, research, implementation authorization, R3.1 start, or R4 eligibility.
- **Status at charter adoption:** `COMPLETE-UPON-MERGE`.

### R3.1 — Product Problem and User-Value Evidence

- **Purpose:** Determine whether the selected problem, workflows, governed reversibility, governance burden, and comparative value are supported for the target user.
- **Entry conditions:** R3.0 is merged; a separately bounded R3.1 task identifies named questions, methods, participants or sources, authority, evidence handling, and stop conditions.
- **Permitted evidence work:** Separately authorized structured interviews, workflow observation, task walkthroughs, comparative usability evaluation, and clearly labelled Human Owner founder/operator evidence.
- **Required outputs:** A traceable product evidence artifact addressing every requirement in Section 6, including counterevidence, limitations, and criterion dispositions.
- **Minimum exit criteria:** Each mandatory product question has substantive evidence and an explicit disposition; gaps and conflicts remain visible; no single observation is generalized beyond its scope.
- **Prohibited interpretations:** Naming a method is not execution of that method; founder/operator evidence is not broad market validation; documentary coherence, enthusiasm, or workflow plausibility is not user-value proof.
- **Status at charter adoption:** `NEXT` and `NOT-STARTED`.

### R3.2 — Technical Feasibility Evidence

- **Purpose:** Establish bounded evidence about reuse, missing capability, governed-state feasibility, lifecycle auditability, failure modes, and blockers to a future vertical slice.
- **Entry conditions:** R3.1 has completed its bounded work and closeout comparison; a separate R3.2 task fixes questions, allowed repository scope, methods, authority, and stop conditions.
- **Permitted evidence work:** Read-only repository analysis and separately authorized controlled demonstrations that do not become production implementation or persistent runtime work.
- **Required outputs:** A traceable technical feasibility evidence artifact addressing every requirement in Section 7, with reuse findings, absence findings, feasibility gaps, failures, rollback boundaries, counterevidence, limitations, and dispositions.
- **Minimum exit criteria:** All mandatory feasibility questions have evidence-backed dispositions, future-slice blockers are explicit, and demonstrations are clearly distinguished from production capability.
- **Prohibited interpretations:** Repository presence is not reuse proof; a controlled demonstration is not architecture selection, production implementation, reliability, security, or implementation authorization.
- **Status at charter adoption:** `NOT-STARTED`.

### R3.3 — Operating Model and Recovery Evidence

- **Purpose:** Test whether the bounded product could be responsibly operated, reviewed, supported, observed, corrected, escalated, and recovered under stated conditions.
- **Entry conditions:** R3.2 has completed its bounded work and closeout comparison; a separate R3.3 task defines operating questions, scenarios, roles, assumptions, methods, and stop conditions.
- **Permitted evidence work:** Bounded analysis, scenario walkthroughs, responsibility validation, recovery-assumption evaluation, and procedure evaluation under separately granted authority.
- **Required outputs:** A traceable operating-model evidence artifact addressing every requirement in Section 8, including unresolved ownership, recovery gaps, support burden, counterevidence, limitations, and dispositions.
- **Minimum exit criteria:** Every mandatory operating and recovery question has an evidence-backed disposition; ownership and escalation gaps are explicit; no assumed procedure is represented as proven.
- **Prohibited interpretations:** A role label, drafted procedure, or plausible recovery narrative does not establish an operating model or recovery capability.
- **Status at charter adoption:** `NOT-STARTED`.

### R3.4 — Security and Privacy Evidence

- **Purpose:** Establish pre-implementation evidence about the selected product direction's material security, privacy, identity, permission, retention, and abuse risks.
- **Entry conditions:** R3.3 has completed its bounded work and closeout comparison; a separate R3.4 task identifies the questions, assessed conceptual scope, evidence methods, authority, and stop conditions.
- **Permitted evidence work:** Separately bounded pre-implementation security and privacy evidence work sufficient to disposition the questions in Section 9, without acting through this charter.
- **Required outputs:** A traceable security/privacy evidence artifact covering every listed risk, with evidence, counterevidence, limitations, unresolved risk, and dispositions.
- **Minimum exit criteria:** Each mandatory risk question has an evidence-backed disposition, material uncertainty and blockers are explicit, and no absence of findings is treated as proof of safety.
- **Prohibited interpretations:** This substage is not the later R8 SEC-GOV review, proof of implemented controls, a security certification, or authority to scan, threat-model, implement, deploy, or release.
- **Status at charter adoption:** `NOT-STARTED`.

### R3.5 — Conditional External Dependency Evidence

- **Purpose:** Resolve only exact unanswered questions tied to concrete named external dependencies that are indispensable to the bounded R3 assessment.
- **Entry conditions:** R3.4 has completed its bounded work and closeout comparison; a concrete dependency exists; and the dependency record required by Section 10 is separately approved. If none exists, the entry record states `R3_EXTERNAL_EVIDENCE=NOT-REQUIRED`.
- **Permitted evidence work:** Time-bounded verification using the pre-recorded permitted sources and freshness requirement, stopping when the exact question or a stop condition is reached.
- **Required outputs:** A traceable external-evidence artifact for each qualifying dependency, or the exact `NOT-REQUIRED` record, with provenance, freshness, limitations, and disposition.
- **Minimum exit criteria:** Every named qualifying dependency is dispositioned without a general research expansion, or absence of any concrete dependency is explicitly recorded.
- **Prohibited interpretations:** Thoroughness is not a reason to research; an unnamed possible dependency does not create a workstream; external information does not authorize dependency adoption or technical selection.
- **Status at charter adoption:** `NOT-STARTED` and conditional.

### R3.6 — Integrated Evidence Synthesis and Exit Assessment

- **Purpose:** Integrate R3.1 through R3.5 evidence without erasing conflicts and determine whether the R3 exit threshold is satisfied for independent R4 consideration.
- **Entry conditions:** R3.1 through R3.4 are complete; R3.5 is complete or explicitly `NOT-REQUIRED`; all substage closeout comparisons and mandatory artifacts are available.
- **Permitted evidence work:** Traceable synthesis, cross-artifact consistency checking, gap registration, target disposition, and bounded exit assessment; no new category may be silently tested inside synthesis.
- **Required outputs:** The integrated evidence matrix, unresolved-gap register, R3 exit assessment, and independent-review-ready evidence package listed in Section 15.
- **Minimum exit criteria:** Section 13 is satisfied; every mandatory question and provisional target has a visible disposition; blockers, failures, conflicts, and missing evidence are explicit.
- **Prohibited interpretations:** Synthesis cannot convert missing, conflicting, deferred, or documentary material into `PASS`; R3 closure is not a `READY` decision, implementation authority, or automatic R4 start.
- **Status at charter adoption:** `NOT-STARTED`.

## 6. R3.1 Product Evidence Requirements

The product evidence artifact must address:

- whether the target user experiences the selected problem;
- whether evidence, candidate, review, approval, adoption, and execution states are difficult to distinguish today;
- whether the five R2 workflows match real operator work;
- whether governed reversibility is valuable;
- whether the added governance burden is acceptable; and
- whether the Control Plane provides measurable value over an ungoverned memory workflow.

Later, separately bounded R3.1 work may use structured interviews, workflow observation, task walkthroughs, and comparative usability evaluation. Human Owner operator evidence may also be used only when clearly labelled as founder/operator evidence rather than broad market validation. This charter neither performs nor claims interviews, observation, evaluation, user validation, measurements, or market evidence.

## 7. R3.2 Technical Feasibility Requirements

The technical feasibility evidence artifact must address:

- which existing repository components are reusable;
- which required capabilities are absent;
- feasibility of source and provenance retention;
- feasibility of candidate-state separation;
- feasibility of explicit human decision tracing;
- feasibility of scoped adoption;
- feasibility of correction, revocation, and deletion auditability;
- failure modes and rollback boundaries; and
- feasibility gaps that would block a future vertical slice.

Read-only repository analysis and separately authorized controlled demonstrations are permitted future methods. This charter does not authorize production implementation, architecture selection, new dependencies, persistent storage, API implementation, runtime work, or a vertical slice. No technical feasibility result is currently established.

## 8. R3.3 Operating Model and Recovery Requirements

The operating-model evidence artifact must address:

- operator responsibilities;
- review and approval ownership;
- incident handling;
- audit review;
- backup and recovery assumptions;
- correction, revocation, and deletion procedures;
- failure escalation;
- data lifecycle;
- observability needs; and
- support burden.

An operating model is not established until the required evidence passes under stated conditions. Current documents, role names, assumptions, or proposed procedures do not establish operating or recovery readiness.

## 9. R3.4 Security and Privacy Requirements

The pre-implementation security and privacy evidence artifact must address:

- memory poisoning;
- source or provenance forgery;
- hidden state promotion;
- approval or authorization bypass;
- prompt injection;
- cross-project or cross-role data leakage;
- unauthorized durable adoption;
- audit-log tampering;
- incomplete revocation or deletion;
- identity and permission boundaries; and
- privacy and retention risks.

This is pre-implementation security and privacy evidence about a selected product direction. It is not the later R8 SEC-GOV review of concrete implemented code. This charter does not perform or authorize a security scan or threat-model exercise, and it records no security or privacy findings.

## 10. R3.5 Conditional External Evidence Rule

External research occurs only when a concrete named dependency actually exists, such as:

- a platform or framework;
- a protocol or standard;
- a legal or regulatory requirement;
- a third-party service;
- an external market or alternative; or
- a security practice requiring current verification.

Before any external research starts, its task record must state the concrete dependency, exact unanswered question, permitted sources, freshness requirement, and stop conditions. Research must remain within that record.

If no concrete external dependency exists, record:

`R3_EXTERNAL_EVIDENCE=NOT-REQUIRED`

No general research workstream may be created merely to appear thorough. A conditional category is not evidence that a dependency exists.

## 11. R3 Provisional Success Thresholds

The following R2 targets are preserved for future evidence-backed disposition:

- 100% visible source provenance for adopted records;
- 100% explicit human-decision trace for adopted records;
- zero unauthorized durable adoption in controlled evaluation;
- auditable correction, revocation, and deletion;
- users can distinguish evidence, candidate, review, approval, adoption, and execution states; and
- measurable value over an ungoverned memory workflow.

All remain unachieved targets until substantive evidence supports their bounded dispositions. Their inclusion in R2 or this charter is not measurement or success.

## 12. Evidence Disposition Rules

- **PASS:** The bounded criterion is supported under stated conditions.
- **HOLD:** Evidence is incomplete, conflicting, or materially limited.
- **DEFER:** The question is valid but outside current bounded work.
- **FAIL:** Evidence contradicts the required criterion.
- **NOT-TESTED:** No substantive evaluation occurred.

Missing evidence is never `PASS`. Documentary completion is never automatic `PASS`. One positive observation is not broad validation. Human Owner selection does not replace factual evidence. Material conflict remains visible in its source artifact, integrated matrix, and exit assessment.

## 13. R3 Exit Threshold

R3 may close only when:

- R3.1 through R3.4 are complete;
- R3.5 is complete or explicitly `NOT-REQUIRED`;
- all mandatory evidence artifacts are traceable;
- provisional success targets have evidence-backed dispositions;
- material blockers and failures are explicit;
- no missing mandatory category is treated as passed;
- an integrated R3.6 synthesis is complete; and
- the evidence package is sufficient for independent R4 consideration.

R3 closure means eligibility for R4 consideration only. It is not a `READY` decision, implementation authorization, R5 eligibility, implementation start, or release, version, deployment, or tag authority. R4 requires its own separately bounded independent readiness reassessment and does not begin automatically.

## 14. Anti-Drift Controls

- Every R3 task must map to one R3 substage.
- Each evidence task must test a named question.
- No evidence question means no task.
- No concrete external dependency means no external research.
- No concrete defect means no GOV-MAINT.
- Internal documentation cannot substitute for evidence.
- There is no automatic successor task.
- After every R3 substage, perform a roadmap closeout comparison against the authorized scope, required outputs, exit criteria, prohibited interpretations, current roadmap state, and next-task boundary.
- Scope expansion requires explicit Human Owner redirection.
- Detected drift must be disclosed and corrected immediately.

## 15. R3 Closeout Deliverables

Before R4 consideration, R3 must provide:

- a product evidence artifact;
- a technical feasibility evidence artifact;
- an operating-model evidence artifact;
- a security/privacy evidence artifact;
- a conditional external-evidence artifact or `NOT-REQUIRED` record;
- an integrated evidence matrix;
- an unresolved-gap register;
- an R3 exit assessment; and
- an independent-review-ready evidence package.

These deliverables must satisfy the evidence quality standard and remain traceable to their substages. They do not prescribe implementation file layouts, APIs, schemas, libraries, or technical solutions.

## 16. Next Task Boundary

Merge of this charter completes only R3.0. The next planned substage is R3.1, but R3.1 does not start automatically. The next repository task must be a separately bounded R3.1 Product Problem and User-Value Evidence task. No code implementation is authorized.

## 17. Final Machine State

```text
ROADMAP_ID=POST-IDG-MASTER-EXECUTION-ROADMAP
ROADMAP_BASE_COMMIT=13e307bca6095487c95dcf20d143c5e7293d2332
R0_STATUS=COMPLETE
R1_STATUS=COMPLETE
R2_STATUS=COMPLETE
R3_STATUS=STARTED-UPON-MERGE
CURRENT_STAGE=R3
CURRENT_SUBSTAGE=R3.0-CHARTER-ADOPTION
PRIMARY_PRODUCT_DIRECTION=CIVILIZATION-CORE-GOVERNED-MEMORY-CONTROL-PLANE
R3_PURPOSE=ESTABLISH-SUBSTANTIVE-EVIDENCE-AND-READINESS
R3_EVIDENCE_MODEL=PRODUCT-TECHNICAL-OPERATING-SECURITY-EXTERNAL-CONDITIONAL
R3_0_CHARTER=COMPLETE-UPON-MERGE
R3_1_PRODUCT_EVIDENCE=NOT-STARTED
R3_2_TECHNICAL_FEASIBILITY_EVIDENCE=NOT-STARTED
R3_3_OPERATING_MODEL_EVIDENCE=NOT-STARTED
R3_4_SECURITY_PRIVACY_EVIDENCE=NOT-STARTED
R3_5_EXTERNAL_EVIDENCE=CONDITIONAL-NOT-STARTED
R3_6_INTEGRATED_SYNTHESIS=NOT-STARTED
R3_EXIT_THRESHOLD=ALL-MANDATORY-EVIDENCE-CRITERIA-PASS-OR-EXPLICITLY-DISPOSED
CURRENT_EVIDENCE_SUFFICIENCY=NOT-ESTABLISHED
IMPLEMENTATION_READINESS=NOT-ESTABLISHED
R4_ELIGIBILITY=NOT-ESTABLISHED
NEXT_PLANNED_SUBSTAGE=R3.1-PRODUCT-PROBLEM-AND-USER-VALUE-EVIDENCE
R3_AUTOMATIC_SUCCESSOR=NO
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
NEXT_REPOSITORY_TASK_CLASS=R3.1-PRODUCT-PROBLEM-AND-USER-VALUE-EVIDENCE
ROADMAP_DRIFT_CONTROL=ACTIVE
```
