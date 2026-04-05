# ENCT Indicators — Quantitative Metrics

**See also:** ENCT-REFERENCE.md §4 (Quantitative Indicators)

All ENCT operations are measured by these eight indicators. These are not vanity metrics—each is essential to system health.

---

## 1. Compliance Rate

**Definition:** Percentage of normative constraints that are mechanically enforced (not just documented)

**Formula:**
```
Compliance Rate = (constraints_mechanically_enforced / total_constraints) × 100%
```

**Target:** >99%

**How We Measure It:**
- Count all constraints in CONSTRAINTS.md (source of truth)
- Count code locations with enforcement (pre-commit hooks, CI gates, runtime checks)
- Any constraint without enforcement is counted as non-compliant

**Example:**
- 100 total constraints
- 99 have CI gates or pre-commit hooks
- 1 is only documented (no enforcement)
- **Compliance Rate = 99%** ✓

**Why It Matters:**
Documents without enforcement are not real constraints. Only mechanical enforcement counts.

---

## 2. Homeostasis Score

**Definition:** Lyapunov-style stability metric (system distance from equilibrium)

**Formula:**
```
Homeostasis Score = 1.0 - (|current_state - target_state| / max_possible_deviation)
```

**Target:** ≥0.85

**What It Measures:**
- Current Compliance Rate vs. 99% target
- Current Confidence (average) vs. 0.80 target
- Current Rollback Rate vs. 5% target
- Current Homeostasis momentum (is it improving or drifting?)

**Combined Formula (Simplified):**
```
HS = 1.0 - avg([
  |compliance - 0.99| / 0.10,
  |avg_confidence - 0.80| / 0.20,
  |rollback_rate - 0.05| / 0.10
])
```

**Example:**
- Compliance = 98.5% (target 99%) → deviation 0.5 / 10 = 0.05
- Avg Confidence = 0.78 (target 0.80) → deviation 0.02 / 20 = 0.001
- Rollback Rate = 3% (target 5%) → deviation 2 / 10 = 0.02
- **HS = 1.0 - avg(0.05, 0.001, 0.02) = 1.0 - 0.023 = 0.977** ✓ (Very stable)

**Why It Matters:**
Homeostasis tells us if the system is drifting or stable. Drift indicates problems (inadequate validation, unstable policies, Axiom violations).

---

## 3. Traceability Coverage

**Definition:** Percentage of all policy decisions with immutable provenance bundles

**Formula:**
```
Traceability Coverage = (decisions_with_provenance_bundles / total_decisions) × 100%
```

**Target:** 100%

**What Provenance Includes:**
- Policy ID, version, full text
- All validation results (Tier 1/2/3 pass/fail)
- Confidence score + uncertainty bounds
- Execution feedback (applied/rejected/escalated)
- Homeostasis/Compliance/Resilience metrics at time of decision
- Actant identity (who made decision)
- Timestamps (when each phase occurred)

**Example:**
- 500 policies bootstrapped in a month
- 500 have complete provenance bundles in `/enct-logs/provenance.jsonl`
- **Traceability Coverage = 100%** ✓

**Why It Matters:**
Without full traceability, we cannot audit decisions, investigate failures, or prove policy safety.

---

## 4. Bootstrap Confidence (Average)

**Definition:** Mean confidence score across all bootstrapped policies

**Formula:**
```
Avg Bootstrap Confidence = sum(confidence_scores) / num_policies
```

**Target:** >0.80

**Example:**
- 10 policies with confidence [0.92, 0.85, 0.78, 0.88, 0.81, 0.79, 0.84, 0.87, 0.82, 0.86]
- **Average = 0.832** ✓

**Why It Matters:**
Low average confidence suggests policies are entering the system without adequate validation. High confidence suggests rigorous gating.

---

## 5. Adaptation Resilience

**Definition:** Fraction of proposed adaptations (norm changes, gate adjustments) that succeeded without rollback within 7 days

**Formula:**
```
Adaptation Resilience = successful_adaptations / total_adaptations
```

**Target:** >0.90

**What Counts as "Successful":**
- Proposed change (e.g., tighten confidence gate from 0.7 to 0.8)
- Applied to production
- Monitored for 7 days
- Did NOT cause Homeostasis drop below 0.85
- Did NOT cause Compliance drop below 99%
- Did NOT require rollback

**Example:**
- 20 adaptations proposed in a month
- 18 succeeded (remained stable 7+ days)
- 2 were rolled back (caused problems)
- **Resilience = 18/20 = 0.90** ✓

**Why It Matters:**
Fragile adaptations hurt user trust and waste effort. High resilience shows the system is robust and changes are well-thought-out.

---

## 6. Provenance Overhead

**Definition:** Storage and retrieval cost of maintaining full provenance (as % of total system resources)

**Formula:**
```
Provenance Overhead = (provenance_storage_GB / total_storage_GB) × 100%
```

**Target:** <10%

**Example:**
- 500 policies, 500 provenance bundles (each ~4KB JSON)
- Total provenance: 500 × 4KB = 2GB
- Total system storage: 50GB
- **Overhead = 2/50 × 100% = 4%** ✓

**Why It Matters:**
Excessive provenance kills performance. We measure cost-benefit: Is full traceability worth 4% overhead? Yes. Is it worth 80% overhead? No.

---

## 7. Axiom Violation Rate

**Definition:** Number of times an axiom was violated and caught (per day)

**Formula:**
```
Axiom Violation Rate = num_axiom_violations_caught / period_days
```

**Target:** <1 per month (0.03 per day)

**What Counts:**
- User tries to bootstrap policy that violates Axiom 1 → Caught and rejected
- Code change attempts to bypass Axiom 3 enforcement → Caught by CI
- Policy would violate Axiom 2 determinism → Caught and escalated

**Example:**
- Month 1 (April 2026): 0 violations caught
- Month 2 (May 2026): 2 violations caught (both low-confidence bootstraps attempting to override axiom 2)
- Month 3 (June 2026): 1 violation caught (code bypass of Axiom 3)
- **Rate = 3 violations / 3 months = 1 per month** ✓

**Why It Matters:**
Frequent violations suggest gate weaknesses. Zero violations over months suggests robust enforcement.

---

## 8. Policy Rollback Rate

**Definition:** Percentage of policies rolled back within 7 days of activation

**Formula:**
```
Policy Rollback Rate = (policies_rolled_back_7d / total_policies_activated) × 100%
```

**Target:** <5%

**What Triggers Rollback:**
- User requests rollback (changed mind)
- Monitoring detects Homeostasis drop caused by policy
- Policy causes unexpected system behavior
- Conflict with existing policies discovered post-deployment

**Example:**
- 100 policies deployed in April 2026
- 3 rolled back within 7 days:
  - Policy A: User request (changed requirements)
  - Policy B: Homeostasis dropped to 0.78 after deployment
  - Policy C: Conflict with Policy X discovered
- **Rollback Rate = 3/100 = 3%** ✓

**Why It Matters:**
High rollback rate suggests poor validation (policies shouldn't need reverting). Low rate suggests validation is effective.

---

## Indicator Monitoring Dashboard (Phase 5)

In Phase 5 (Monitor), all eight indicators stream to a live dashboard with:
- **Real-time values** (updated every cycle)
- **Trend lines** (7-day history)
- **Target bars** (visual "good/warning/critical" zones)
- **Alerts** (automatic notification if metric drops below target)

Example dashboard output:
```
┌─ ENCT v1.3 Live Metrics ─────────────────────┐
│ Compliance Rate:      98.5% [████████░░░] ✓  │
│ Homeostasis Score:     0.82 [██████████░] ⚠  │
│ Traceability Cov:     100%  [███████████] ✓  │
│ Avg Confidence:        0.79 [██████████░] ⚠  │
│ Adaptation Resilience: 0.92 [███████████] ✓  │
│ Provenance Overhead:   4.2% [██░░░░░░░░] ✓  │
│ Axiom Violation Rate:  0.0/d [░░░░░░░░░░] ✓  │
│ Policy Rollback Rate:  2.1% [███░░░░░░░] ✓  │
│                                               │
│ Last Updated: 2026-04-05 14:32:15 UTC       │
│ Status: All Nominal                          │
└───────────────────────────────────────────────┘
```

---

## Indicator Interaction

How indicators reinforce each other:

- **Compliance Rate ↑** → Homeostasis ↑ (more constraints enforced = more stable)
- **Avg Confidence ↑** → Rollback Rate ↓ (higher-confidence policies fail less)
- **Traceability ↑** → Violation Detection ↑ (better auditing finds more issues)
- **Adaptation Resilience ↑** → Homeostasis ↑ (robust changes maintain stability)

All eight together form a coherent health picture of the system.

---

## Thresholds & Alerts

| Indicator | Green | Yellow | Red |
| --- | --- | --- | --- |
| Compliance | >99% | 95–99% | <95% |
| Homeostasis | ≥0.85 | 0.80–0.85 | <0.80 |
| Traceability | 100% | 99–100% | <99% |
| Avg Confidence | >0.80 | 0.75–0.80 | <0.75 |
| Adaptation Resilience | >0.90 | 0.80–0.90 | <0.80 |
| Provenance Overhead | <5% | 5–10% | >10% |
| Axiom Violations | 0/day | <0.5/day | ≥0.5/day |
| Rollback Rate | <3% | 3–5% | >5% |
