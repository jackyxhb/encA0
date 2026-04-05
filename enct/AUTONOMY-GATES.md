# Autonomy Gates Specification — ENCT v1.3

**Purpose:** Define explicit scope boundaries and access controls for the bootstrap agent so it cannot exceed its authority or create unsafe policies.

**See Also:** P2-4 (Bounded Autonomy & Access Control), AXIOMS.md (Axiom 1: Immutability)

---

## 1. Domain Boundaries

The bootstrap agent can ONLY create policies within predefined domains. Any policy targeting an undefined domain is REJECTED.

### Defined Domains (Phase 1 Baseline)

| Domain | Scope | Examples | Approval Gate |
| --- | --- | --- | --- |
| **Authentication** | Login, credential validation | Password complexity, MFA rules, session timeout | Security team approval |
| **API Rate Limiting** | Request throttling, quota enforcement | Rate limit = 1000 req/min, exponential backoff | Ops approval |
| **Data Validation** | Input constraints, type checking | Field format rules, length constraints | Product team approval |
| **Access Control** | Permission enforcement | Role-based access, resource ownership checks | Security team approval |
| **Audit Logging** | Event recording, compliance trails | Log all policy changes, user actions | Compliance team approval |
| **Performance** | Latency, resource constraints | Max response time 500ms, memory limit 1GB | Ops approval |
| **Compliance & Governance** | Regulatory rules, policy enforcement | GDPR rules, data retention, deletion | Legal team approval |

### How Domains Work

1. **User submits policy:** "Require password length >12"
2. **Domain check:** Is "Authentication" in defined domains? YES → Continue
3. **Domain ownership:** Does Authentication domain have an approval authority? YES → Route to Security team for Socratic review
4. **Approval:** Security team reviews Q1–Q8, approves or rejects
5. **If approved:** Policy enters Tier 1 validation

### Out-of-Scope Domains (REJECTED)

- [ ] "General system policies" (too broad)
- [ ] "Business logic" (vague)
- [ ] "Arbitrary runtime changes" (unconstrained)
- [ ] Anything not in the defined list above

**Action on Out-of-Scope:** Automatically reject policy and escalate to human with message: "This policy targets domain XYZ, which is not in the approved domain list. Please redefine within one of: [list]. Or request domain expansion (requires security review)."

---

## 2. Axiom Immutability Gate

The bootstrap agent CANNOT create policies that override or disable any axiom. This gate is PERMANENT and cannot be loosened.

### What Cannot Be Changed (Immutable Forever)

- [ ] Axiom 1: Foundational rules (immutability, 5-phase Loop, four primitives, base indicator set)
- [ ] Axiom 2: Action determinism (uncertainty bounds required, non-determinism forbidden)
- [ ] Axiom 3: Normative enforcement (all constraints must be mechanical, not soft)
- [ ] Axiom 4: Adaptive resilience (all adaptations versioned, auditable, reversible)

### How the Gate Works

1. **Policy submitted:** "Allow bootstrap without confidence score requirement"
2. **Axiom check:** Does this policy violate an axiom? YES (would disable Axiom 2 uncertainty bounds)
3. **Action:** REJECT immediately and escalate to human with message: "This policy violates Axiom 2 (Action Determinism). All actions must have confidence scores and uncertainty bounds. Policy REJECTED."

### Examples of Violations (All REJECTED)

- ✗ "Policies can be applied without the Tiered Validate phase" → Violates Axiom 1 (Loop structure immutable)
- ✗ "Allow non-deterministic actions without bounds" → Violates Axiom 2 (determinism required)
- ✗ "Constraints only need to be documented, not enforced" → Violates Axiom 3 (enforcement required)
- ✗ "Norm changes don't need versioning" → Violates Axiom 4 (versioning required)
- ✗ "Disable confidence scoring" → Violates Axiom 2

### Examples of Compliant Changes (All ALLOWED)

- ✓ "Tighten confidence gate from 0.7 to 0.8" → Adds constraint, doesn't override axiom
- ✓ "Add new indicator: policy rollback rate" → Extends metrics, doesn't disable base set
- ✓ "Require escalation for policies <24h old" → Adds domain-specific rule
- ✓ "New domain: Data Retention" → Expands domains, doesn't disable existing ones

---

## 3. Confidence Threshold Gate

The bootstrap agent accepts policies with Confidence ≥ threshold, escalates policies with Confidence < threshold.

### Threshold Configuration

**Default (Phase 1):** Confidence ≥ 0.7 (configurable per domain)

**Domain-Specific Overrides:**
- Authentication: Confidence ≥ 0.75 (stricter, security-critical)
- API Rate Limiting: Confidence ≥ 0.70 (standard)
- Data Validation: Confidence ≥ 0.70 (standard)
- Access Control: Confidence ≥ 0.75 (stricter, security-critical)
- Audit Logging: Confidence ≥ 0.70 (standard)
- Performance: Confidence ≥ 0.65 (more lenient, operational concern)
- Compliance: Confidence ≥ 0.80 (strictest, legal risk)

### How the Gate Works

1. **Policy passes Tier 3 sandbox validation**
2. **Confidence score calculated** (0.0–1.0)
3. **Compare to threshold**
   - If Confidence ≥ threshold → ACCEPT (policy activated)
   - If Confidence < threshold → ESCALATE (route to human review)

### Example

```
Policy: "API rate limit = 1000 req/min"
Domain: "API Rate Limiting"
Threshold: 0.70

Tier 3 Validation Results:
  - Homeostasis impact: +0.02 (improving)
  - Conflict detection: 0 conflicts found
  - Load testing: Passed all scenarios
  - Confidence Score: 0.72

Confidence (0.72) ≥ Threshold (0.70) → ACCEPT
Policy activated immediately.
```

### Changing the Threshold (Requires Governance)

To change thresholds:
1. Document rationale (why looser/stricter?)
2. Propose new threshold
3. Version the change: `gate_config_v1.0` → `gate_config_v1.1`
4. Commit to Git with CHANGELOG entry
5. CI validates the change doesn't weaken axioms
6. Take effect on next policy submission

---

## 4. Rate Limiting Gates

Prevent agent from flooding the system with bootstraps.

### Bootstrap Rate Limit

**Limit:** Max 10 bootstraps per hour per user/agent

**Action if exceeded:**
```
User attempts 11th bootstrap in 1 hour
→ REJECTED with message: "Rate limit exceeded (10 bootstraps/hour). Please wait 60 minutes or contact admin for override."
```

**Why:** Prevents accidental loop (agent endlessly re-submitting same policy) and resource exhaustion.

### Policy Count Limit

**Limit:** Max 50 active policies per session

**Action if exceeded:**
```
User attempts 51st active policy
→ REJECTED with message: "Too many active policies (max 50). Rollback or deactivate existing policies before adding new ones."
```

**Why:** Prevents cognitive overload and complex policy interactions.

### Reset Window

Both limits reset hourly/daily:
- Hourly: Bootstrap rate limit resets at start of next hour
- Daily: Policy count limit resets at start of next day

### Admin Override

Administrators can temporarily override rates for maintenance/migration:
```bash
# CLI command (authenticated admin only)
./scripts/override-rate-limit --user alice@example.com --duration 1h
```

Overrides are logged and audited.

---

## 5. Rollback Scope Gate

Control which policies can be rolled back and how far back in time.

### Time Window

**Automatic Rollback:** Policies <24 hours old can be rolled back by user or agent
**Human-Required Rollback:** Policies ≥24 hours old require human approval

### How the Gate Works

```
User/agent requests rollback of policy P1
  ↓
Check deployment timestamp
  ↓
  If age < 24 hours:
    ALLOW rollback immediately
    Log rollback reason
  Else (age ≥ 24 hours):
    ESCALATE to human
    Human reviews impact and decides
```

### Why 24 Hours?

- **Short window:** Catches and reverts bad policies quickly (before widespread impact)
- **Long window:** Prevents churning (constantly rolling back and redeploying same policy)
- **Human gate:** For mature policies that have been in production >24h, data may depend on them; rollback needs careful analysis

### Example

```
Policy deployed: 2026-04-05 14:00 UTC
Current time:   2026-04-05 22:00 UTC (8 hours later)
Age: 8 hours < 24 hours
Action on rollback request: ALLOWED (auto-approved)

---

Policy deployed: 2026-04-03 14:00 UTC
Current time:   2026-04-05 22:00 UTC (56 hours later)
Age: 56 hours ≥ 24 hours
Action on rollback request: ESCALATE (human review required)
Human: "This policy is used by 100 active users. Rollback not recommended. Suggest refinement instead."
```

---

## 6. Access Control Matrix

Who can do what?

| Action | Bootstrap Agent | Audit Agent | Human Admin | Notes |
| --- | --- | --- | --- | --- |
| **Bootstrap new policy** | Yes (with gates) | No | Yes (override) | Agent limited by domain, confidence, rate gates |
| **Validate policy** | Yes | Yes | Yes | Both agents have read-only on validation logic |
| **Escalate to human** | Yes | Yes | N/A | Agents can escalate; humans decide |
| **Accept escalated policy** | No | No | Yes | Only humans approve escalations |
| **Rollback policy** | Yes (<24h) | No | Yes (any age) | Agent limited by time window |
| **Modify axiom code** | No | No | No | Axioms immutable (code review + approval required) |
| **Modify domain list** | No | No | Yes (approval) | Admin can expand/reduce domains with documentation |
| **Modify confidence thresholds** | No | No | Yes (versioned) | Admin can adjust per-domain thresholds |
| **View audit logs** | Read-only | Read-write | Read-write | Bootstrap agent can see own logs |
| **Modify enforcement gates** | No | No | Yes (code review) | Changes to gates require Git + CI approval |

---

## 7. Escalation Rules

When policies are escalated to humans.

### Automatic Escalation Triggers

| Trigger | Reason | Who Reviews |
| --- | --- | --- |
| Confidence <0.7 | Policy failed validation | Domain-specific approval team |
| Axiom violation detected | Policy would break axiom | Security team + architect |
| Unknown domain | Policy targets undefined domain | Product team + security team |
| Rollback age >24h | Rolling back mature policy | Domain owner + stakeholder |
| Conflicting policies | New policy conflicts with existing | Conflict mediation (human) |
| User requests it | User wants explicit review | Domain-specific team |

### Escalation SLA

All escalations must be reviewed within:
- **Critical (security/axiom violations):** 1 hour
- **Standard (confidence <0.7):** 8 hours
- **Non-urgent (user request):** 24 hours

If SLA missed, escalation is auto-approved (user cannot be blocked indefinitely).

---

## 8. Enforcement Mechanism

How these gates are actually enforced in code.

### Pre-Commit Hook

```bash
#!/bin/bash
# hooks/pre-commit

# Check: Is new policy within defined domain?
if ! grep -q "domain: (Authentication|API_RateLimit|...)" policy.json; then
  echo "ERROR: Policy domain not in AUTONOMY-GATES.md approved list"
  exit 1
fi

# Check: Does policy attempt to override axiom?
if grep -q "disable Axiom\|override Axiom\|bypass enforcement" policy.json; then
  echo "ERROR: Policy violates axiom immutability gate"
  exit 1
fi

exit 0
```

### Runtime Gate (Python Pseudocode)

```python
def validate_bootstrap_policy(policy):
    # Gate 1: Domain check
    if policy.domain not in APPROVED_DOMAINS:
        escalate("Domain not approved", policy)
        return
    
    # Gate 2: Axiom check
    if policy.violates_axioms():
        escalate("Axiom violation", policy)
        return
    
    # Gate 3: Confidence threshold
    confidence = run_validation_tiers(policy)
    threshold = DOMAIN_THRESHOLDS[policy.domain]
    if confidence < threshold:
        escalate(f"Confidence {confidence} < {threshold}", policy)
        return
    
    # Gate 4: Rate limit
    if user_bootstrap_count(policy.user) >= 10:
        reject("Rate limit exceeded")
        return
    
    # Gate 5: Policy count
    if active_policy_count(policy.user) >= 50:
        reject("Too many active policies")
        return
    
    # All gates passed
    accept_policy(policy)
```

### CI/CD Check

```yaml
# .github/workflows/policy-gates.yml
- name: Validate Autonomy Gates
  run: |
    python scripts/validate_gates.py
    # Checks: domain list, axiom enforcement, thresholds, rate limits
```

---

## 9. Governance & Changes

### Changing Gates (Process)

1. **Propose change:** Rationale document (why change?)
2. **Review:** Security team + architect + stakeholders
3. **Approve:** Consensus required (no lone decisions)
4. **Version:** Gate config v1.0 → v1.1, Git tag, CHANGELOG
5. **Deploy:** Changes take effect on next policy cycle
6. **Monitor:** Watch Homeostasis for 7 days (ensure change is safe)
7. **Revert if needed:** If Homeostasis drops <0.85, auto-revert to prior version

### No Backdoors, No Overrides

- Gates cannot be disabled by a single user action
- Overrides require human approval (and are logged)
- All changes to gate logic require code review + CI approval
- Audit trail records all gate violations and overrides

---

## Summary

**Autonomy Gates ensure:**
- ✓ Bootstrap agent stays within predefined boundaries (domains)
- ✓ Axioms are never violated (immutability gate)
- ✓ Only high-confidence policies are auto-accepted (confidence gate)
- ✓ System doesn't get flooded (rate limiting)
- ✓ Mature policies aren't casually reverted (rollback scope)
- ✓ All access is controlled and audited (access matrix)
- ✓ Escalations follow process (SLA, team assignments)

**Result:** Agent can operate autonomously within safe bounds, with human oversight for edge cases.
