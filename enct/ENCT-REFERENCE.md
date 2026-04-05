# ENCT v1.3 — Complete Reference Document

**Version:** v1.3.0  
**Last Updated:** 2026-04-05  
**Status:** Phase 1 Design Baseline

This document is the **canonical source of truth** for all ENCT v1.3 theory, primitives, axioms, the 5-phase Loop, indicators, and verification approaches. All code, designs, and operations must reference this document.

---

## 1. The Four Primitives

ENCT defines four foundational primitives that form the bedrock of the normative control system:

### 1.1 Actant (A)

**Definition:** An entity (AI agent, system component, or human) that can observe environmental state, make decisions, and execute actions. Actants exist within hierarchical clustering structures—a single agent may be decomposed into sub-agents, each with bounded autonomy.

**Properties:**
- **Observability:** Can sense and measure environmental state
- **Agency:** Can initiate and execute actions within bounded scope
- **Hierarchical Nesting:** Actants can be composed of sub-actants
- **Policy Containment:** Each actant operates under a set of normative constraints

**Example:** A policy-bootstrapping agent is an Actant. So is a verification sub-agent that audits a policy before acceptance.

---

### 1.2 Enactive Action (EA)

**Definition:** Purposeful behavior that is both *enacted* (carried out by the Actant) and *responsive* to environment feedback. Unlike passive reactions, Enactive Actions are grounded in environmental coupling and sensorimotor loops.

**Properties:**
- **Bidirectional Coupling:** Action → Environment → Observation → Adaptation
- **Uncertainty Bounds:** Every action carries confidence intervals reflecting epistemic and aleatoric uncertainty
- **Feedback-Driven Iteration:** Actions trigger observations that inform subsequent actions
- **Non-Deterministic Outcome:** Same action in different environmental states may yield different results

**Example:** A bootstrap action takes a user policy, validates it against axioms (observation), calculates confidence score, and either accepts or escalates. The feedback (confidence score, validation result) informs the next action.

---

### 1.3 Normative Constraint (NC)

**Definition:** A rule, axiom, or policy that governs permissible behavior of an Actant. Normative Constraints are *versioned*, *sanction-bearing* (violations trigger consequences), and *explicitly tradable* (multiple norms can be negotiated).

**Properties:**
- **Versioning:** Each constraint has a unique version (v1.0, v1.1, etc.) with Git history
- **Sanctions:** Violations trigger defined consequences (escalation, rollback, human review)
- **Explicitness:** Constraints are encoded as structured rules, never implicit
- **Negotiability:** Multiple constraints can be composed, balanced, or traded in MAS

**Example:** "Bootstrap confidence must exceed 0.7" is a Normative Constraint. "Policies cannot modify Axiom 1" is another. Both are versioned, sanctioned (if violated, escalate), and explicit.

---

### 1.4 Cybernetic Loop (CL)

**Definition:** The feedback mechanism that allows an agent to observe state, measure performance against Normative Constraints, and adaptively adjust behavior to maintain system stability (homeostasis). The loop is continuous, timely, and corrective.

**Properties:**
- **Observability → Measurement → Feedback:** Real-time sensing of state and compliance metrics
- **Corrective Action:** Deviations from norms trigger immediate correction
- **Homeostasis:** The loop maintains the system near a stable target state (e.g., Homeostasis Score ≥0.85)
- **Self-Regulation:** The agent self-corrects without external intervention (unless escalation threshold exceeded)

**Example:** The 5-phase ENCT Loop (below) instantiates the Cybernetic Loop. Each phase feeds into the next; the final "Re-enact & Log" phase re-enters the Sense phase to close the cycle.

---

## 2. The Four Axioms

ENCT v1.3 is governed by four non-negotiable axioms that form the foundation of the system:

### Axiom 1: Foundational Rules Are Immutable

**Axiom:** The core set of foundational rules (axioms themselves, the 5-phase Loop structure, the definitions of the four primitives, the base indicator set) cannot be overridden, modified, or disabled by any policy or bootstrap decision. These form the bedrock.

**Why:** Without immutable foundation, the system collapses into arbitrary rule-making where malicious or erroneous policies can corrupt the normative control mechanism itself.

**Enforcement:**
- All bootstrap policies are checked against Axiom 1 before acceptance
- Any policy that attempts to override an axiom is immediately escalated
- Axiom 1 violations are logged as critical incidents

**Example of Violation:**
- User tries to bootstrap policy: "Allow any policy without verification" → BLOCKED (violates Axiom 1: violates 5-phase Loop structure)
- User tries to disable Axiom 3 (normative enforcement): BLOCKED (violates Axiom 1)

**Example of Compliance:**
- User bootstraps: "Policies in domain X must have Confidence >0.8" → ALLOWED (adds constraint, does not override axioms)

---

### Axiom 2: Action Determinism

**Axiom:** Given the same Normative Constraints, the same environmental state, and the same Actant, applying the same action twice yields the same outcome (within uncertainty bounds specified by confidence intervals). Non-determinism must be explicitly declared and bounded.

**Why:** Without determinism, agents cannot be held accountable for their actions. Governance requires predictability.

**Enforcement:**
- All Enactive Actions must include uncertainty bounds (confidence intervals, aleatoric uncertainty ranges)
- Test suite validates that same input → same output (with declared variance)
- Non-deterministic actions are sandboxed and monitored separately

**Example of Violation:**
- Agent bootstraps policy with no confidence score or uncertainty bounds → REJECTED (violates Axiom 2)
- Agent's verification sometimes passes a policy, sometimes rejects identical policy → FAILED (violates Axiom 2)

**Example of Compliance:**
- Agent bootstraps policy with Confidence = 0.75 (±0.05), meaning outcome deterministic within 5% → ALLOWED
- Verification gate always applies same rules in same order → COMPLIANT

---

### Axiom 3: Normative Enforcement

**Axiom:** Every Normative Constraint is actively enforced. A constraint that is documented but not mechanically enforced is not a real constraint—it is merely documentation. Mechanical enforcement is non-negotiable.

**Why:** Without enforcement, norms become "nice to haves" that agents ignore. Real governance requires real gating.

**Enforcement:**
- Every Normative Constraint has a corresponding test, linter, or gating rule
- Pre-commit hooks, CI pipelines, and verification gates mechanically reject non-compliance
- Violations trigger escalation (P0-7)

**Example of Violation:**
- Policy says "All bootstraps must have Confidence >0.5" but code does not check it → NOT ENFORCED (violates Axiom 3)
- Audit agent recommends a policy but does not block unsafe policies → NOT ENFORCED

**Example of Compliance:**
- Bootstrap gate: `if confidence < 0.7: escalate_to_human()` → ENFORCED mechanically
- CI check: fails merge if test coverage drops → ENFORCED mechanically

---

### Axiom 4: Adaptive Resilience

**Axiom:** The system adapts in response to external change, but adaptation must preserve homeostasis and not compromise Axioms 1–3. Adaptation is bounded: changes to Normative Constraints themselves are versioned, audited, and reversible.

**Why:** Systems that cannot adapt die when environments change. But adaptation without guardrails becomes chaos. Bounded adaptation balances stability and flexibility.

**Enforcement:**
- All norm changes are versioned (Git-tracked with CHANGELOG)
- Norm updates are auditable (who, what, when, rationale)
- Rollback procedures exist for all adaptive changes
- Adaptive mechanisms themselves (e.g., Homeostasis Score calculation) are immutable (Axiom 1)

**Example of Violation:**
- Agent modifies Homeostasis Score formula without versioning or audit trail → violates Axiom 4
- Agent adapts to an emergency by disabling Axiom 2 (determinism) → violates Axioms 1 & 4

**Example of Compliance:**
- Monitoring agent detects drift in Homeostasis Score (now 0.79, target 0.85) and recommends tightening Confidence gate to 0.8 → proposes versioned change
- Change is logged: date, rationale, formula delta, previous version link → versioned and auditable
- If new setting causes problems, easy rollback to previous version → reversible

---

## 3. The Five-Phase ENCT Loop

The core runtime cycle that instantiates normative control. Every agent iteration flows through these five phases:

### Phase 1: Sense & Translate
**Input:** Raw environmental observation (user policy submission, system metric, log entry)  
**Process:**
- Observe environment state
- Parse/interpret observation into structured form
- Translate into internal representation (policy intent, metric value, decision state)

**Output:** Translated state ready for validation  
**Axiom Compliance:** Observation must be complete and unbiased (feeds Axiom 2 determinism)  
**Example:** User submits policy text "require password length >12". Agent translates to structured object: `Policy{domain="auth", rule="pwd_min_length=12", confidence=?}`.

---

### Phase 2: Tiered Validate
**Input:** Translated state from Phase 1  
**Process:** Apply three-tier validation hierarchy:
- **Tier 1 (Cache):** Quick check against cached validation results. If identical policy was validated recently (within 1 hour), reuse result.
- **Tier 2 (Delta):** Check only the *changed* parts of the policy. If policy is a modification of an existing policy, validate only the delta.
- **Tier 3 (Full):** Full sandbox simulation. Execute the policy in an isolated environment and measure Homeostasis Score (Lyapunov-style stability metric ≥0.85 required).

**Output:**
- Validation status (Pass/Fail)
- Confidence score (0.0–1.0)
- Failure reason (if any)
- Uncertainty bounds (Axiom 2)

**Axiom Compliance:** All three tiers mechanically enforce Axioms 1–3. Tier 3 sandbox proves Axiom 2 determinism and Axiom 3 enforcement.  
**Example:** Policy confidence=0.92 (passes Tier 1), delta check shows safe modification (passes Tier 2), sandbox shows Homeostasis≥0.85 (passes Tier 3) → ACCEPT.

---

### Phase 3: Execute & Feedback
**Input:** Validated policy + Confidence score  
**Process:**
- If Confidence ≥ 0.7: Apply the policy (activate norm)
- If Confidence < 0.7: Escalate to human review (P0-7)
- Record Enactive Action with uncertainty bounds
- Measure immediate feedback (did policy take effect? any errors?)

**Output:**
- Policy activation status
- Feedback measurement (success/failure)
- Timestamp + Actant identity (who executed?)
- Escalation flag (if triggered)

**Axiom Compliance:** Execution is deterministic (Axiom 2), feedback is mechanically measured (Axiom 3), and escalation preserves system stability (Axiom 4).  
**Example:** Confidence=0.75 → Execute. Policy applied. Feedback: "Auth system accepted new rule. 50 users affected." → Move to Phase 4.

---

### Phase 4: Assess & Adapt
**Input:** Feedback from Phase 3  
**Process:**
- Measure current system state against Normative Constraints
- Calculate Homeostasis Score (how stable is the system? target ≥0.85)
- Detect metric changes: Compliance Rate (% of policies actually enforced), Adaptation Resilience (how well did the system absorb the new norm?)
- If Homeostasis < 0.85 or Compliance < 99%: prepare adaptation
- Propose corrective action (tighten gate, rollback policy, increase monitoring)

**Output:**
- Homeostasis Score
- Compliance Rate
- Adaptation Resilience metric
- Proposed corrective action (if any)

**Axiom Compliance:** Adaptation proposals preserve Axioms 1–3 and are logged for audit (Axiom 4 versioning).  
**Example:** Policy applied 2 hours ago. Homeostasis=0.82 (below target). Compliance Rate=98% (below 99% target). Propose: tighten confidence gate to 0.8 for similar policies in same domain.

---

### Phase 5: Re-enact & Log
**Input:** Assessment from Phase 4 + corrective action (if any)  
**Process:**
- Apply corrective action (if proposed)
- Create immutable provenance bundle:
  - Policy ID, version, text
  - All validation results (Tier 1/2/3)
  - Confidence score + uncertainty bounds
  - Execution feedback
  - Homeostasis/Compliance/Resilience metrics
  - All decisions (accept/reject/escalate)
  - Actant identity (who made decision?)
  - Timestamps (when each phase occurred?)
- Log to `/enct-logs/provenance.jsonl` (append-only)
- Close the loop by re-entering Phase 1 with the next observation

**Output:**
- Immutable provenance bundle (JSON)
- Updated system state (ready for Phase 1 of next cycle)

**Axiom Compliance:** Provenance is immutable (Axiom 3 enforcement), logged for audit (Axiom 4), and versioned (Git-tracked).  
**Example:** Provenance bundle:
```json
{
  "policy_id": "auth_pwd_v1",
  "timestamp_created": "2026-04-05T10:00:00Z",
  "phases": {
    "sense_translate": {"status": "ok", "policy_text": "require pwd >12"},
    "tiered_validate": {"tier1": "cache_hit", "tier2": "delta_ok", "tier3": "homeostasis=0.88"},
    "execute_feedback": {"status": "applied", "affected_users": 50},
    "assess_adapt": {"homeostasis": 0.82, "compliance": 98.5, "resilience": 0.92},
    "reenact_log": {"action": "tighten_gate_to_0.8", "version": "v1.1"}
  }
}
```

---

## 4. Quantitative Indicators

All ENCT operations are measured by these eight quantitative indicators. These are not vanity metrics—each measures something fundamental to system health.

### 4.1 Compliance Rate
**Definition:** Percentage of normative constraints that are actually enforced in practice (not just documented).  
**Formula:** `(constraints_mechanically_enforced / total_constraints) × 100%`  
**Target:** >99%  
**Rationale:** Documents without enforcement are not real constraints. We measure what's actually mechanically enforced.  
**Example:** 100 total constraints. 99 have pre-commit hooks or CI gates. 1 is only documented. Compliance Rate = 99%.

---

### 4.2 Homeostasis Score
**Definition:** Lyapunov-style stability metric measuring how far the system is from target state. Scores approach 1.0 as system stabilizes.  
**Formula:** `1.0 - (|current_state - target_state| / max_deviation)`  
**Target:** ≥0.85  
**Rationale:** Systems that drift from equilibrium become unstable. We measure distance to stability.  
**Example:** If target Compliance is 99% and current is 98.5%, Homeostasis Score = 1 - (0.5/50) = 0.99 (very stable).

---

### 4.3 Traceability Coverage
**Definition:** Percentage of all policy decisions that have immutable provenance bundles (see Phase 5).  
**Formula:** `(decisions_with_provenance / total_decisions) × 100%`  
**Target:** 100%  
**Rationale:** Without full traceability, we cannot audit or investigate failures.  
**Example:** 500 policies bootstrapped in a month. 500 have provenance bundles. Traceability = 100%.

---

### 4.4 Bootstrap Confidence (Average)
**Definition:** Mean confidence score across all bootstrapped policies.  
**Formula:** `sum(confidence_scores) / num_policies`  
**Target:** >0.80  
**Rationale:** Low average confidence suggests policies are entering system without adequate validation.  
**Example:** 10 policies with confidence [0.92, 0.85, 0.78, 0.88, ...]. Average = 0.83.

---

### 4.5 Adaptation Resilience
**Definition:** Fraction of adaptations (norm changes, gate tightenings) that succeeded without rollback.  
**Formula:** `(successful_adaptations / total_adaptations)`  
**Target:** >0.90  
**Rationale:** Fragile adaptations hurt trust and waste effort.  
**Example:** 20 adaptations proposed. 18 succeeded long-term. 2 were rolled back. Resilience = 0.90.

---

### 4.6 Provenance Overhead
**Definition:** Storage and retrieval cost of maintaining full provenance (as % of total system memory/compute).  
**Formula:** `(provenance_storage_GB / total_storage_GB) × 100%`  
**Target:** <10%  
**Rationale:** Excessive provenance kills performance. We measure the cost-benefit.  
**Example:** 500 policies, provenance is 2GB, total storage is 50GB. Overhead = 4%.

---

### 4.7 Axiom Violation Rate
**Definition:** Number of times an axiom was violated (and caught) per time period.  
**Formula:** `num_axiom_violations / period_length_days`  
**Target:** <1 per month (0.03 per day)  
**Rationale:** Frequent violations suggest lax gates or training problems.  
**Example:** Month 1: 0 violations. Month 2: 2 violations (caught by gate). Month 3: 1 violation. Rate = 1 per month.

---

### 4.8 Policy Rollback Rate
**Definition:** Percentage of policies that were rolled back (reverted to prior version) within 7 days of activation.  
**Formula:** `(policies_rolled_back_in_7d / total_policies_activated) × 100%`  
**Target:** <5%  
**Rationale:** High rollback rate suggests poor validation or user regret. Measure real-world policy quality.  
**Example:** 100 policies deployed. 3 rolled back within 7 days. Rollback Rate = 3%.

---

## 5. Verification Approaches

The specific methods used to verify that ENCT Loop cycles are correct and safe:

### 5.1 Model Checking
**Approach:** Formal verification that the ENCT Loop satisfies invariant properties (axioms).  
**Invariants Checked:**
- Axiom 1: No axiom override occurs (state transition never moves to "Axiom 1 disabled")
- Axiom 2: Identical state + identical action → identical outcome (determinism)
- Axiom 3: All Normative Constraints are mechanically enforced (no "soft" enforcement)
- Axiom 4: Homeostasis is maintained (Score ≥0.85 after adaptation)

**Tools:** Temporal logic checkers (TLA+), state machine simulators  
**Example:** Model checker validates: "If policy enters Phase 2 Tier 3 validation, it must exit with Homeostasis ≥0.85 or be rejected."

---

### 5.2 Sandbox Simulation
**Approach:** Execute the 5-phase Loop in an isolated environment with synthetic workloads (500+ scenarios).  
**Scenarios Include:**
- Normal operations: benign policies, standard workflows
- Stress: 1000 concurrent policy submissions
- Adversarial: policies trying to violate axioms, race conditions
- Recovery: system rollback and re-stabilization after failures

**Success Criterion:** Homeostasis Score ≥0.85 for all scenarios  
**Example:** Scenario: User submits 10 conflicting policies simultaneously. System handles tiers, queues, validates in order, achieves Homeostasis=0.88. ✓ Pass.

---

### 5.3 Audit Trail Inspection
**Approach:** Examine immutable provenance bundles for completeness and correctness.  
**Checks:**
- Every policy has full provenance (Phase 1–5 complete)
- Confidence scores justified (tiers passed or failed with reason)
- Escalations logged with rationale
- Versions match ENCT-VERSION.md
- No policies missing from ledger

**Tools:** `grep`, regex scanning, Python analysis scripts  
**Example:** Scan `/enct-logs/provenance.jsonl` for any entry missing "phase_5_reenact_log". Alert if found (missing = bug).

---

### 5.4 Red-Teaming
**Approach:** Adversarial testing: try to break the system by submitting invalid policies, exploiting gates, triggering race conditions.  
**Test Cases:**
- Policy that contradicts Axiom 1 (should be blocked)
- Two identical policies submitted simultaneously (should not be accepted twice)
- Malformed confidence score (should be rejected)
- Request to disable Axiom 3 enforcement (should escalate)

**Success Criterion:** All adversarial inputs handled correctly (blocked, escalated, or logged as attack)  
**Example:** Red-teamer submits policy "allow bootstrap without verification". System detects violation of Axiom 1, escalates to human. ✓ Pass.

---

## 6. Failure Ledger

Documentation of past axiom violations, failed bootstraps, and lessons learned. **Populated iteratively during Phases 2–5.**

| Date | Incident | Axiom Violated | Root Cause | Resolution | Lesson |
| --- | --- | --- | --- | --- | --- |
| (To be filled) | | | | | |

---

## 7. Glossary

**Actant:** An agent or system component with bounded autonomy  
**Enactive Action:** Purpose-driven behavior with feedback coupling  
**Normative Constraint:** A rule with versions, sanctions, and mechanical enforcement  
**Cybernetic Loop:** The feedback mechanism enabling self-regulation  
**Homeostasis:** System stability (Score ≥0.85)  
**Provenance Bundle:** Immutable record of all decisions and metrics for a policy  
**Escalation:** Hand-off to human review when confidence drops or axiom violation detected  
**Bootstrap:** Process of creating and validating a new policy  
**Confidence Score:** Numeric measure (0–1) of validation result quality  
**Rollback:** Reverting a policy to prior version  
**Compliance Rate:** % of constraints mechanically enforced  

---

## 8. Document History

| Version | Date | Change | Status |
| --- | --- | --- | --- |
| v1.3.0 | 2026-04-05 | Initial ENCT v1.3 reference document (Phase 1 baseline) | Published |

---

**This document is immutable. All modifications require version bump and changelog entry.**
