# ENCT Verification Approaches

**See also:** ENCT-REFERENCE.md §5 (Verification Approaches)

The specific methods used to verify that ENCT Loop cycles are correct and safe.

---

## 1. Model Checking

**Objective:** Formal verification that the ENCT Loop satisfies invariant properties (axioms)

**Invariants Checked:**
1. **Axiom 1 (Immutability):** No axiom override occurs. State transition never moves to "Axiom 1 disabled"
2. **Axiom 2 (Determinism):** Identical state + identical action → identical outcome
3. **Axiom 3 (Enforcement):** All Normative Constraints are mechanically enforced
4. **Axiom 4 (Resilience):** Homeostasis maintained (Score ≥0.85 after adaptation)

**Tools:**
- Temporal logic checkers (TLA+, SPIN)
- State machine simulators
- Theorem provers (for critical paths)

**Test Strategy (Phase 2–3):**
- Model 5-phase Loop as finite state machine
- Define state transitions for each phase
- Verify no path violates axiom invariants
- Cover all edge cases (concurrent submissions, rollbacks, escalations)

**Success Criterion:**
- All invariants proven true across all possible state transitions
- No counterexamples found

**Example Verification:**
```
INVARIANT: If policy enters Phase 2 Tier 3 validation, it exits with either:
  (a) Homeostasis ≥0.85 AND confidence >0.7 → ACCEPT, OR
  (b) Homeostasis <0.85 OR confidence ≤0.7 → REJECT

Proof: Verify no path exits Phase 2 with undefined state or Homeostasis <0.85 AND confidence >0.7
```

---

## 2. Sandbox Simulation

**Objective:** Execute the 5-phase Loop in isolated environment with synthetic workloads (500+ scenarios)

**Test Scenarios:**

### 2.1 Normal Operations
- Single policy submission (normal case)
- Sequence of benign policies (standard workflow)
- Policy revisions (update existing policy)

**Success Criterion:** All pass Tier 1/2/3 validation; Homeostasis ≥0.85

### 2.2 Stress Testing
- 1000 concurrent policy submissions
- Rapid-fire escalations
- Large policy documents (100+ KB)
- High-frequency metrics updates

**Success Criterion:** System handles load without deadlock; Homeostasis ≥0.85

### 2.3 Adversarial Testing (Red Team)
- Policy attempting to violate Axiom 1 (should be blocked)
- Two identical policies submitted simultaneously (should not duplicate)
- Malformed confidence score (should be rejected)
- Request to disable Axiom 3 enforcement (should escalate immediately)
- Race condition: modify policy while it's being validated

**Success Criterion:** All adversarial inputs handled correctly (blocked, escalated, or logged)

### 2.4 Recovery Testing
- System failure during Phase 3 (execution)
- Rollback of failed policy
- Resume interrupted validation chain
- Restore from provenance bundle

**Success Criterion:** System recovers to consistent state; no policies lost; all decisions replay identically

**Execution Plan (Phase 3):**
```python
# pseudocode
scenarios = [
    ("normal_single", validate_policy(sample_policy)),
    ("stress_1000", submit_policies_concurrent(1000)),
    ("adversarial_axiom1_override", policy_attempting_axiom_violation()),
    ("recovery_phase3_failure", simulate_crash_during_execution()),
    ...
]

for scenario_name, scenario_logic in scenarios:
    result = run_in_sandbox(scenario_logic)
    assert result.homeostasis_score >= 0.85, f"{scenario_name} failed"
    assert result.compliance_rate > 0.99, f"{scenario_name} lost enforcement"
```

**Success Criterion for Phase 3:**
- ✓ All 500+ scenarios pass
- ✓ Homeostasis ≥0.85 for 100% of scenarios
- ✓ Zero non-deterministic outcomes (identical input → identical output, within bounds)
- ✓ Zero axiom violations (all four axioms respected in all scenarios)

---

## 3. Audit Trail Inspection

**Objective:** Examine immutable provenance bundles for completeness and correctness

**Checks Performed:**

### 3.1 Completeness Check
Every provenance bundle must contain:
- ✓ Policy ID (unique identifier)
- ✓ Policy version (linked to prior versions via Git)
- ✓ Full policy text (exact as submitted)
- ✓ Timestamp (when submitted)
- ✓ Actant identity (who/what submitted?)
- ✓ Phase 1 output: translated state
- ✓ Phase 2 output: Tier 1/2/3 results, confidence score
- ✓ Phase 3 output: execution status, feedback
- ✓ Phase 4 output: Homeostasis, Compliance, Resilience
- ✓ Phase 5 output: versioned constraint, rollback link

### 3.2 Consistency Check
- Confidence score matches Tier validation results (if Tier 3 Homeostasis=0.88, confidence should be high)
- Escalation reason recorded if policy rejected
- All timestamps in order (Phase 1 < Phase 2 < Phase 3 < Phase 4 < Phase 5)
- Provenance version matches ENCT-VERSION.md

### 3.3 Integrity Check
- Provenance bundle is append-only (no modifications post-creation)
- No provenance bundles missing from `/enct-logs/provenance.jsonl`
- All policies in POLICY-LEDGER.md have corresponding provenance

**Tools:**
- `grep`, `jq` for JSON inspection
- Python scripts for consistency checking
- Git log for version history

**Execution Plan (Phase 3–5):**
```bash
# Check all bundles have all required fields
jq '.phases | keys' /enct-logs/provenance.jsonl | \
  grep -c "sense_translate\|tiered_validate\|execute_feedback\|assess_adapt\|reenact_log"

# Verify no modifications to append-only log
git log --oneline -- /enct-logs/provenance.jsonl | wc -l  # should only show appends, no resets
```

**Success Criterion:**
- 100% of provenance bundles complete
- 100% of bundles consistent
- Zero integrity violations

---

## 4. Red-Teaming

**Objective:** Adversarially test the system by trying to break it

**Red-Team Test Cases (Phase 3):**

| Test | Attack | Expected Result | Pass/Fail |
| --- | --- | --- | --- |
| RT-1 | Policy: "disable Axiom 1" | Blocked, escalated | Pass |
| RT-2 | Policy: "skip Tiered Validate phase" | Blocked (violates Axiom 1) | Pass |
| RT-3 | Submit identical policies 2x concurrently | Only 1 accepted; 2nd rejected | Pass |
| RT-4 | Confidence score: "undefined" | Rejected, escalated | Pass |
| RT-5 | Malformed JSON in policy | Parsed error logged, rejected | Pass |
| RT-6 | Attempt to rollback immutable policy (>24h old) | Escalated to human | Pass |
| RT-7 | Policy that violates Axiom 2 (non-deterministic) | Rejected (uncertainty bounds required) | Pass |
| RT-8 | Request Homeostasis formula change without versioning | Rejected, escalated | Pass |
| RT-9 | Modify provenance bundle retroactively | Detected (append-only violation), alert | Pass |
| RT-10 | Escalation threshold manipulation | Blocked (protected in code) | Pass |

**Tools:**
- Custom Python test harness
- Fuzzing (generate random invalid policies)
- Symbolic execution (find edge cases)

**Success Criterion:**
- All 10+ red-team tests pass
- No attacks succeed
- All violations detected and logged

---

## 5. Automated Test Suite (Phase 2–3)

**Framework:** pytest (or equivalent)

### 5.1 Unit Tests (Axioms)
```
tests/
  test_axiom1.py       # Immutability checks
  test_axiom2.py       # Determinism checks
  test_axiom3.py       # Enforcement checks
  test_axiom4.py       # Resilience checks
  test_indicators.py   # Indicator calculations
```

**Example:**
```python
def test_axiom1_immutability():
    """Verify axioms cannot be overridden"""
    policy = Policy(text="disable Axiom 1")
    with pytest.raises(AxiomViolationError):
        validate_and_accept(policy)
```

### 5.2 Integration Tests (Loop)
```
tests/
  test_sense_translate.py
  test_tiered_validate.py
  test_execute_feedback.py
  test_assess_adapt.py
  test_reenact_log.py
```

### 5.3 Scenario Tests (Sandbox)
```
tests/
  scenarios/
    test_normal_operations.py     # 50 scenarios
    test_stress.py                # 100 scenarios
    test_adversarial.py           # 150 scenarios
    test_recovery.py              # 100+ scenarios
```

### 5.4 Regression Tests
```
tests/
  test_provenance_integrity.py    # Audit trail checks
  test_no_axiom_violations.py     # Historical check (scan past logs)
  test_rollback_reversibility.py  # All rollbacks replay identically
```

**CI Integration:**
```yaml
# .github/workflows/test.yml
- run: pytest tests/ -v --cov=src/ --cov-report=term
- run: pytest tests/scenarios/ --timeout=60s  # Sandbox tests with timeout
- run: python scripts/verify_provenance.py    # Audit trail checks
- fail-if: coverage < 95%
```

**Success Criteria (Phase 3):**
- ✓ All tests pass
- ✓ >95% code coverage
- ✓ No flaky tests (same test run 10x = same result)
- ✓ Sandbox tests complete in <1 minute each

---

## Verification Checklist (Phase 3 Testing)

### Before Phase 4 Deployment, Verify:

- [ ] Model checking: All 4 axiom invariants proven
- [ ] Sandbox simulation: 500+ scenarios all pass with Homeostasis ≥0.85
- [ ] Audit trail: 100% of provenance bundles complete and consistent
- [ ] Red-teaming: All 10+ red-team tests pass
- [ ] Unit tests: >95% coverage, all pass
- [ ] Integration tests: All 5 Loop phases tested
- [ ] Scenario tests: All categories (normal, stress, adversarial, recovery) pass
- [ ] Regression: No new axiom violations introduced
- [ ] Determinism: Identical input → identical output (within declared bounds) for 100% of tests
- [ ] No skipped tests (all critical paths covered)

**If all checks pass:** Phase 4 Deployment is safe. System is proven correct to sufficient confidence.

**If any check fails:** Do not proceed to Phase 4. Investigate and fix root cause. Re-run entire verification suite.

---

## Success Metrics for Phase 3

| Metric | Target | Pass Condition |
| --- | --- | --- |
| Model checking coverage | 100% | All axiom invariants verified |
| Scenario coverage | 500+ | All pass, all Homeostasis ≥0.85 |
| Provenance integrity | 100% | No missing or corrupted bundles |
| Red-team success rate | 0% | No attacks succeed |
| Test coverage | >95% | All critical code paths covered |
| Determinism | 100% | Identical input → identical output |
| Axiom compliance | 100% | Zero axiom violations detected |

**Phase 3 COMPLETE when all metrics met and team confirms readiness for Phase 4.**
