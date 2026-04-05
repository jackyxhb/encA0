# ENCT Glossary

**See also:** ENCT-REFERENCE.md §7 (Glossary)

---

## Core Concepts

### Actant
An entity (AI agent, system component, or human) that can observe environmental state, make decisions, and execute actions within a bounded scope. Actants are hierarchically nested (an agent may contain sub-agents).

**Example:** A policy-bootstrapping agent. A verification sub-agent. A monitoring agent.

---

### Enactive Action
Purposeful behavior that is both *enacted* (carried out by an Actant) and *responsive* to environment feedback. Every action carries uncertainty bounds reflecting model confidence and inherent unpredictability.

**Example:** Bootstrap action: submit policy → validate → calculate confidence → accept or escalate.

---

### Normative Constraint
A rule or policy that governs permissible behavior. Constraints are *versioned* (Git-tracked), *sanction-bearing* (violations trigger escalation), and *explicitly tradable* (multiple constraints can be negotiated).

**Example:** "Bootstrap confidence must exceed 0.7." "Policies cannot modify Axiom 1."

---

### Cybernetic Loop
The feedback mechanism allowing an agent to observe state, measure performance against Normative Constraints, and adaptively adjust behavior to maintain stability (homeostasis). Continuous, timely, corrective.

**Example:** The 5-phase ENCT Loop (Sense → Validate → Execute → Assess → Re-enact).

---

### Axiom
A foundational, non-negotiable rule that cannot be overridden. ENCT has four axioms:
1. **Immutability:** Core rules cannot be disabled
2. **Determinism:** Same input → same output (within bounds)
3. **Enforcement:** All constraints mechanically enforced
4. **Resilience:** Adaptation is versioned and reversible

---

### Homeostasis
System stability. Measured as a score (0–1) reflecting distance from target state. Target ≥0.85.

**Example:** If Compliance Rate drops to 98% (target 99%), Homeostasis Score decreases (system drifting).

---

### Provenance Bundle
Immutable record of all decisions and metrics for a single policy. Contains:
- Policy ID, version, full text
- Validation results (Tier 1/2/3)
- Confidence score + uncertainty bounds
- Execution feedback
- Homeostasis/Compliance metrics
- Actant identity + timestamps

**See:** Phase 5 (Re-enact & Log) in ENCT-REFERENCE.md

---

### Bootstrap
Process of creating and validating a new policy (or policy version). Passes through all five phases: Sense, Validate, Execute, Assess, Re-enact.

**Example:** User submits policy "require password length >12" → bootstrap process validates and activates it.

---

### Escalation
Hand-off to human review when confidence drops, axiom violation detected, or system state becomes ambiguous. Escalation *pauses* the bootstrap process until human reviews.

**Example:** Policy confidence = 0.65 (below gate 0.7) → escalate to human → human approves or rejects.

---

### Verification
Process of confirming that ENCT Loop cycles are correct, safe, and respect all axioms. Four verification approaches:
1. Model checking (formal invariants)
2. Sandbox simulation (500+ scenarios)
3. Audit trail inspection (provenance completeness)
4. Red-teaming (adversarial testing)

---

### Rollback
Reverting a policy to its prior version or entirely removing a policy. Triggered by:
- User request (changed requirements)
- Monitoring detects Homeostasis drop caused by policy
- Axiom violation discovered post-deployment
- Conflict with existing policy

**Example:** Policy was deployed 3 hours ago, Homeostasis dropped to 0.78. Rollback to prior version.

---

## Indicator Metrics

### Compliance Rate
Percentage of normative constraints that are mechanically enforced (not just documented).

**Target:** >99%

---

### Homeostasis Score
Lyapunov-style stability metric (distance from equilibrium).

**Target:** ≥0.85

---

### Traceability Coverage
Percentage of policy decisions with immutable provenance bundles.

**Target:** 100%

---

### Bootstrap Confidence (Average)
Mean confidence score across all bootstrapped policies.

**Target:** >0.80

---

### Adaptation Resilience
Fraction of proposed adaptations (norm changes) that succeeded without rollback within 7 days.

**Target:** >0.90

---

### Provenance Overhead
Storage cost of maintaining full provenance (as % of total system resources).

**Target:** <10%

---

### Axiom Violation Rate
Number of axiom violations caught per day.

**Target:** <1 per month (0.03 per day)

---

### Policy Rollback Rate
Percentage of policies rolled back within 7 days of activation.

**Target:** <5%

---

## Process Concepts

### Five-Phase ENCT Loop
The core runtime cycle:
1. **Sense & Translate:** Observe environment, translate to structured form
2. **Tiered Validate:** Three-tier validation (Tier 1: cache, Tier 2: delta, Tier 3: full sandbox)
3. **Execute & Feedback:** Apply policy, record feedback
4. **Assess & Adapt:** Measure Homeostasis, propose adaptations
5. **Re-enact & Log:** Apply adaptations, log provenance, close loop

---

### Tier 1 Validation (Cache)
Quick check against cached validation results. If identical policy validated recently (within 1 hour), reuse result.

---

### Tier 2 Validation (Delta)
Check only the changed parts of the policy. If policy is modification of existing policy, validate only the delta.

---

### Tier 3 Validation (Full Sandbox)
Full sandbox simulation. Execute policy in isolated environment, measure Homeostasis Score (≥0.85 required).

---

### Confidence Score
Numeric measure (0.0–1.0) of validation result quality. Reflects model certainty about policy safety.

**Example:** Confidence 0.85 = 85% confident this policy is safe.

---

### Uncertainty Bounds
Range of possible values for a confidence score. Includes:
- **Epistemic:** Reducible via more data/training
- **Aleatoric:** Irreducible randomness in the problem itself

**Example:** Confidence 0.85 ± (epistemic 0.04, aleatoric 0.02) = "85% confident, plus/minus uncertainty factors."

---

### Versioning
Tracking policy and constraint versions in Git. Enables rollback and audit.

**Example:** constraint_v1.0 → constraint_v1.1 → constraint_v2.0 (breaking change)

---

### Audit Trail
Immutable record of all decisions, who made them, when, and why. Stored in `/enct-logs/provenance.jsonl` (append-only).

---

### Domain
A functional area or scope to which policies apply.

**Example:** "auth" (authentication), "api_rate_limiting", "data_validation"

---

### Sanction
Consequence of violating a Normative Constraint. Sanctions include escalation, rejection, rollback, or investigation.

---

## Operational Concepts

### Phase 1: Design
Define ENCT primitives, axioms, indicators, verification approaches. Design product UI/UX. Create architecture blueprint.

---

### Phase 2: Train
Implement ENCT engine and bootstrap pattern. Build prototype with all axiom enforcement.

---

### Phase 3: Test
Execute full verification suite (model checking, sandbox simulation, audit inspection, red-teaming).

---

### Phase 4: Deploy
Package as installable product. Add user-facing UI for policy submission, dashboards for monitoring.

---

### Phase 5: Monitor
Deploy real-time observability. Stream all eight indicators to live dashboard. Implement alerting and consolidation loop.

---

## Stakeholder Roles

### Bootstrap Agent
Creates and validates policies. Responsible for Phases 1–3 of ENCT Loop.

---

### Audit Agent
Reviews bootstrap outcomes for axiom compliance (Phase 4+). Secondary agent that votes on policy acceptance.

---

### Monitoring Agent
Streams live metrics (Phase 5). Detects Homeostasis drift, triggers alerts, proposes adaptations.

---

### Human Reviewer
Escalated decisions (low confidence, axiom violations). Final authority on controversial or ambiguous policies.

---

## Terms by Context

### In Specification Documents
- **Requirement:** Explicit feature goal (e.g., "Compliance Rate >99%")
- **Constraint:** Limitation on system behavior (e.g., "Policies cannot disable Axiom 1")
- **Success Criterion:** Measurable condition proving completion

### In Code
- **Assertion:** Test that enforces a rule (e.g., `assert confidence > 0.7`)
- **Gate:** Code that blocks non-compliant action (e.g., `if confidence < 0.7: escalate()`)
- **Linter:** Tool that flags violations (e.g., missing uncertainty bounds)

### In Logging/Monitoring
- **Event:** Something that happened (policy bootstrapped, axiom violated, rollback triggered)
- **Alert:** Notification of abnormal condition (Homeostasis <0.85, Compliance <99%)
- **Incident:** Significant event worthy of investigation (axiom violation, catastrophic failure)

---

## Abbreviations

| Abbr | Full Form |
| --- | --- |
| **ENCT** | Enactive Normative Control Theory |
| **HS** | Homeostasis Score |
| **CR** | Compliance Rate |
| **TC** | Traceability Coverage |
| **BC** | Bootstrap Confidence |
| **AR** | Adaptation Resilience |
| **PO** | Provenance Overhead |
| **AVR** | Axiom Violation Rate |
| **RR** | Rollback Rate |
| **MAS** | Multi-Agent System |
| **SAS** | Single-Agent System |
| **CI/CD** | Continuous Integration / Continuous Deployment |
| **PR** | Pull Request |
| **TLA+** | Temporal Logic of Actions (formal verification language) |

---

## Cross-References

- **Full Theory:** ENCT-REFERENCE.md
- **Axiom Details:** AXIOMS.md
- **Indicator Formulas:** INDICATORS.md
- **Verification Methods:** VERIFICATION.md
- **Past Incidents:** FAILURE-LEDGER.md
- **Design Spec:** (Phase 1 Design output)

---

**Last Updated:** 2026-04-05 (Phase 1 baseline)
