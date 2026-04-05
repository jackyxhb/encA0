# ENCT Axioms — Detailed Reference

**See also:** ENCT-REFERENCE.md §2 (The Four Axioms)

---

## Axiom 1: Foundational Rules Are Immutable

### Definition
The core set of foundational rules cannot be overridden, modified, or disabled by any policy or bootstrap decision.

### What Is Foundational?
- The four ENCT primitives (Actant, Enactive Action, Normative Constraint, Cybernetic Loop)
- The five-phase Loop structure (Sense → Validate → Execute → Assess → Re-enact)
- The four axioms themselves (Axioms 1–4)
- The base indicator set (Compliance Rate, Homeostasis Score, etc.)
- The three-tier validation framework (Tier 1/2/3)
- Provenance recording (Phase 5)

### What Is NOT Foundational (Can Change)
- Confidence thresholds (can be 0.7 or 0.8 depending on domain)
- Specific Normative Constraints applied to a domain (can be added, versioned, modified)
- Indicator formulas can evolve (but only via versioning and audit)
- Escalation thresholds can be tuned

### Enforcement Mechanisms
1. **Bootstrap Gate:** Every policy submission is checked: "Does this policy attempt to override axiom X?" If yes, reject and escalate.
2. **CI Gate:** No code commit is accepted that disables axiom enforcement.
3. **Audit Trail:** Any attempted axiom override is logged as critical incident.

### Example: What Violates Axiom 1?

❌ User submits: "Policies can be applied without the Tiered Validate phase"
- **Violation:** Attempts to modify the 5-phase Loop structure (foundational)
- **Action:** Reject, escalate to human

❌ Code change: `if should_skip_verification: return True`
- **Violation:** Bypasses Axiom 3 enforcement (foundational)
- **Action:** CI blocks merge

❌ Policy: "This domain does not require confidence scores"
- **Violation:** Attempts to disable Enactive Action uncertainty bounds (Axiom 2 related)
- **Action:** Reject, escalate

### Example: What Complies with Axiom 1?

✓ User submits: "Policies in domain X must have confidence >0.75"
- **Compliance:** Adds Normative Constraint (allowed), does not modify axioms
- **Action:** Accept if passes validation

✓ Code change: Implement new metric (9th indicator) alongside base eight
- **Compliance:** Extends system, does not override axiom enforcement
- **Action:** CI accepts (if other gates pass)

✓ Policy: "Rollback this policy if Homeostasis drops below 0.80"
- **Compliance:** Uses Axiom 4 (adaptive resilience), does not override it
- **Action:** Accept

---

## Axiom 2: Action Determinism

### Definition
Given the same Normative Constraints, the same environmental state, and the same Actant, applying the same action twice yields the same outcome (within declared uncertainty bounds).

### Why Determinism Matters
- **Accountability:** If outcomes are random, agents cannot be held responsible.
- **Testability:** Non-deterministic systems cannot be thoroughly tested.
- **Reproducibility:** Investigators cannot replay failures and understand root causes.
- **Governance:** Policy cannot govern non-deterministic behavior.

### What Determinism Covers
- Policy validation (same policy, same environment → same confidence score)
- Axiom enforcement (axiom check applied identically each time)
- Metric calculations (Homeostasis formula applies same way each cycle)
- Escalation decisions (same violation → same escalation action)

### What Is NOT Required to Be Deterministic
- User behavior (different users may submit different policies)
- Environmental state (systems change over time)
- Randomness in LLM outputs (LLMs are inherently stochastic)

**BUT:** All randomness MUST be bounded and declared as uncertainty intervals.

### Enforcement: Uncertainty Bounds

Every Enactive Action outputs:
```
{
  "outcome": <result>,
  "confidence": <0.0-1.0>,
  "uncertainty_bounds": {
    "epistemic_lower": <0.0-1.0>,
    "epistemic_upper": <0.0-1.0>,
    "aleatoric": <0.0-1.0>
  }
}
```

- **Confidence:** Best-guess outcome probability
- **Epistemic Uncertainty:** Reducible via more data/better models
- **Aleatoric Uncertainty:** Irreducible randomness in the problem itself

### Example: Axiom 2 Compliance

✓ **Deterministic with Bounds:**
```
Policy validation result:
  outcome: ACCEPT
  confidence: 0.82
  epistemic_uncertainty: [0.78, 0.86]  (model confidence range)
  aleatoric_uncertainty: 0.03           (inherent policy ambiguity)
```
Interpretation: "This policy will be accepted with 82% confidence. Given more training data, we expect 78–86%. The policy itself is slightly ambiguous (3% inherent variability)."

✗ **Non-Deterministic (Violates Axiom 2):**
```
First run:  ACCEPT (confidence 0.82)
Second run: REJECT (confidence 0.45)
Same policy, same state → different outcome → NOT DETERMINISTIC
```

### Enforcement Mechanisms
1. **Test Suite:** Run validation 100x on same input → all results identical (within declared bounds)
2. **Reproducibility Tests:** Replay old decisions, verify they'd be made identically today
3. **CI Gate:** Block code that introduces non-determinism without bounds

---

## Axiom 3: Normative Enforcement

### Definition
Every Normative Constraint is actively enforced. A constraint that is documented but not mechanically enforced is not a real constraint.

### What "Mechanically Enforced" Means
- Pre-commit hooks reject non-compliant commits
- CI/CD pipelines fail builds on violation
- Runtime gates block non-compliant actions
- Linters flag violations with fix suggestions
- Tests explicitly validate the constraint

### What "Not Mechanically Enforced" Looks Like (❌ Forbidden)
- Documentation only: "Policies should have confidence >0.5" (NOT enforced → not a constraint)
- Manual review: "Ask auditor to check" (humans can be bypassed → not enforced)
- Logging only: "Log violations, but allow them" (NOT enforced)
- Soft nudges: "Warn user about low confidence" (user can ignore → NOT enforced)

### Three Tiers of Enforcement

| Tier | Mechanism | When | Example |
| --- | --- | --- | --- |
| Tier 1 | Pre-commit hook | During development | `git commit` blocked if test coverage drops |
| Tier 2 | CI pipeline | On PR submission | `pytest` fails; merge blocked until tests pass |
| Tier 3 | Runtime gate | At runtime/deployment | `if confidence < 0.7: escalate()` inside code |

### Example: Axiom 3 Compliance

✓ **Enforced:** "All policies must have confidence >0.7"
```
Mechanism:
  - Tier 1: Pre-commit hook checks confidence before commit
  - Tier 2: CI validates all bootstraps have confidence field populated
  - Tier 3: Runtime: if confidence <0.7, immediately escalate to human
Compliance: This constraint is real and enforced.
```

✗ **Not Enforced:** "All policies should be audited"
```
Current:
  - Audit agent logs recommendation (no gate)
  - Policies accepted even if audit fails
Violation: Audit is documented but not mechanically enforced.
Fix: Add gate: `if audit_fails: reject_policy()`
```

### Enforcement Mechanisms (How We Ensure Axiom 3)

1. **Linter:** Custom script scans ENCT-REFERENCE.md for all Normative Constraints
2. **Mapping:** Every constraint must have corresponding test/hook/gate
3. **CI Check:** `find . -name "*.py" | xargs grep -l "constraint_X"` must find enforcement code
4. **Audit Trail:** All constraints logged in CONSTRAINTS.md with enforcement method

---

## Axiom 4: Adaptive Resilience

### Definition
The system adapts in response to external change, but adaptation must preserve Axioms 1–3 and be versioned, audited, and reversible.

### Adaptive vs. Rigid
- **Too Rigid:** System cannot change → breaks when environment changes
- **Too Adaptive:** System changes arbitrarily → loses coherence and trust
- **Axiom 4:** Bounded adaptation that preserves core stability

### What Can Adapt?
- Normative Constraints (e.g., tighten confidence gate from 0.7 to 0.8)
- Indicator thresholds (e.g., raise Homeostasis target from 0.85 to 0.87)
- Validation strategies (e.g., use Tier 2 delta validation for domain X)
- Escalation rules (e.g., escalate if response time >30s instead of 60s)

### What Cannot Adapt?
- Axioms 1–3 themselves
- The 5-phase Loop structure
- The four primitives
- The base indicator set

### Three Requirements for Adaptation

#### 1. Versioning
Every adaptive change has a version number:
```
constraint_v1: confidence >0.7
constraint_v1.1: confidence >0.75  (note: change reason, date, author)
constraint_v1.2: confidence >0.80  (note: change reason, date, author)
```
Git tracks all versions. Rollback to any prior version possible.

#### 2. Audit Trail
Every adaptation is logged with:
- **Who:** Actant/person proposing change
- **What:** Specific constraint changed and how
- **Why:** Rationale (e.g., "Homeostasis dropped below 0.85")
- **When:** Timestamp
- **Reversibility:** Link to prior version for rollback

#### 3. Reversibility
Every adaptation can be rolled back:
```
# Adaptation: tighten confidence gate
git commit -m "Constraint v1.1 → confidence >0.75"
git tag v1.1-prod-2026-04-05

# Later, if fails:
git revert <commit-hash>  # Back to v1.0: confidence >0.7
```

### Example: Axiom 4 Compliance

✓ **Compliant Adaptation:**
```
Situation: Homeostasis Score dropped to 0.79 (below target 0.85)
Proposal: Tighten bootstrap confidence gate from 0.7 to 0.8
Process:
  1. Propose change with rationale (Homeostasis drift)
  2. Version: constraint_v2.0 → confidence >0.8
  3. Log in CHANGELOG: "2026-04-05: Tighten gate due to Homeostasis <0.85"
  4. Git commit with version tag
  5. Monitor new Homeostasis Score
  6. If still <0.85 after 24h: rollback to v1.9 (confidence >0.7)
Result: Bounded, audited, reversible → Compliant with Axiom 4
```

✗ **Non-Compliant Adaptation:**
```
Situation: Agent decides Homeostasis Score formula is "inconvenient"
Action: Modifies formula in code without version, audit, or test
Result: New Homeostasis Score calculated differently; no way to rollback
Violation: Violates Axiom 4 (not audited/versioned/reversible)
Fix: Propose version change, audit, add test, then commit
```

---

## Axiom Interaction Table

How the four axioms reinforce each other:

| Axiom | Reinforced By | Breaks If | Critical For |
| --- | --- | --- | --- |
| 1 (Immutability) | 3 (Enforcement), 4 (No override) | Axiom 3 enforcement missing | System coherence |
| 2 (Determinism) | Tests, reproducibility checks | Randomness without bounds | Accountability |
| 3 (Enforcement) | 1 (no escape), 2 (testable) | "Soft" enforcement allowed | Governance |
| 4 (Adaptation) | 1 (cannot override core), 2 (all changes deterministic), 3 (changes enforced) | Uncontrolled drift | Resilience |

---

## Axiom Violation Escalation

When any axiom is violated, the response is:

1. **Immediate:** Escalate to human review (no override)
2. **Logged:** Critical incident logged in `/enct-logs/`
3. **Investigated:** Root cause analysis (see FAILURE-LEDGER.md)
4. **Remediated:** Fix and version the enforcement mechanism
5. **Prevented:** Add test/gate to prevent recurrence

---

## Summary

The four axioms form a coherent system:
- **Axiom 1** (Immutable foundation) prevents chaos
- **Axiom 2** (Determinism) enables accountability
- **Axiom 3** (Enforcement) makes governance real
- **Axiom 4** (Bounded adaptation) allows resilience without collapse

Together, they define ENCT's non-negotiable guarantees.
