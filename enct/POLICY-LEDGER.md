# Policy Ledger — ENCT v1.3

**Purpose:** Centralized registry of all policy submissions. Acts as upstream intake gate (P2-5) preventing unregistered policies from bootstrap.

**Status:** Empty (to be populated starting Phase 4 Deployment)

**See Also:** POLICY-INTAKE-TEMPLATE.md (Socratic framework), AUTONOMY-GATES.md (gates and escalation)

---

## Policy Ledger Structure

Each entry follows this template:

```
### Policy ID: [domain]_[name]_v[number]

**Submission Date:** YYYY-MM-DD HH:MM UTC  
**Submitter:** [user name / agent]  
**Domain:** [Authentication | API_RateLimit | DataValidation | AccessControl | AuditLogging | Performance | Compliance]  
**Status:** [Draft | Queued | Bootstrapped | Active | Rolled Back]  
**Confidence Score:** [0.0-1.0] (only after validation)  

**Policy Intent:**  
[1-2 sentences describing what the policy does]

**Rationale (Why):**  
[Why is this policy needed? What failure does it prevent?]

**Success Metric:**  
[How will you measure if this policy works?]

**Dependencies:**  
[List of existing policies this depends on, if any]

**Failure Modes:**  
[What could go wrong? What are the symptoms if it breaks?]

**Testing Status:**  
[Yes/No/Partial — has it been tested before submission?]

**Risks & Mitigations:**  
[What are the downsides? How are they mitigated?]

**Validation Timeline:**  
- Submitted: [date]
- Tier 1 (cache): [result] [date]
- Tier 2 (delta): [result] [date]
- Tier 3 (sandbox): [result] [date]
- Decision: [ACCEPT/REJECT/ESCALATE] [date]
- Escalation (if any): [reason, human decision, date]

**Git Provenance:**  
[Link to provenance bundle in /enct-logs/provenance.jsonl]

**Notes:**  
[Any additional context]

---
```

---

## Entry States & Transitions

```
                    ┌─────────────────────────────────┐
                    ↓                                 ↑
                [Draft] ←─ User fills Socratic Q's, saved to ledger
                    ↓
            (Enter bootstrap queue)
                    ↓
                [Queued] ←─ Awaiting validation (Tier 1/2/3)
                    ↓
        ┌─────────────────────────────────┐
        ↓                                 ↓
    [Bootstrapped]                   [Rejected]
        ↓                                 ↑
        │         (Escalation path)      │
        │             ↓                   │
        │         [Escalated] ──────────→ (Human review)
        │             ↑
        │             └─────────────────────┐
        │                                   │
        ↓                              (Decision)
    [Active]
        ↓
    [Rolled Back] ←─ User/system triggered rollback
        ↓
    [Archived]    ←─ Policy retired
```

### State Definitions

- **Draft:** User submitted, waiting to enter validation queue. Not yet validated.
- **Queued:** In validation queue. Tier 1/2/3 checks in progress.
- **Bootstrapped:** Passed all validations, confidence ≥ gate, policy activated.
- **Escalated:** Human review required (low confidence, axiom check, conflict, etc.). Awaiting decision.
- **Rejected:** Validation failed or human rejected. Policy not activated. Can be resubmitted as new entry.
- **Active:** Policy successfully bootstrapped and currently enforced.
- **Rolled Back:** Policy was active, then reverted to prior version or removed. Reason documented.
- **Archived:** Policy very old, no longer referenced. Moved to archive for historical record.

---

## Example Entries

### Example 1: Approved & Active

```
### Policy ID: auth_pwd_complexity_v1

**Submission Date:** 2026-04-10 14:32 UTC  
**Submitter:** alice@example.com  
**Domain:** Authentication  
**Status:** Active  
**Confidence Score:** 0.82  

**Policy Intent:**  
Enforce minimum password complexity (12 chars, mixed case, number, special char) to prevent brute-force attacks.

**Rationale:**  
Weak passwords are the primary vector for account takeovers. NIST guidelines recommend >12 characters with mixed complexity.

**Success Metric:**  
Zero successful brute-force attacks per month. 95%+ user auth success rate (no legitimate users locked out).

**Dependencies:**  
- User registration policy (pre-existing)
- Password hashing policy (pre-existing, bcrypt-based)

**Failure Modes:**  
If policy breaks: users unable to log in (auth failure rate spikes), support tickets increase, Homeostasis drops.

**Testing Status:**  
Yes. Tested on staging with 10 test accounts, all scenarios passed.

**Risks & Mitigations:**  
- Risk: Strictness frustrates users. Mitigation: Clear guidance in UI, password reset flow.
- Risk: Legacy systems don't support special chars. Mitigation: Phase out legacy, provide alternatives.

**Validation Timeline:**  
- Submitted: 2026-04-10 14:32 UTC
- Tier 1 (cache): MISS (new policy) 2026-04-10 14:35 UTC
- Tier 2 (delta): PASS (safe modification to auth domain) 2026-04-10 14:40 UTC
- Tier 3 (sandbox): PASS (Homeostasis=0.88, all scenarios passed) 2026-04-10 15:00 UTC
- Decision: ACCEPT (Confidence 0.82 ≥ gate 0.75) 2026-04-10 15:05 UTC
- Escalation: None

**Git Provenance:**  
/enct-logs/provenance.jsonl line 42 (2026-04-10T15:05:00Z auth_pwd_complexity_v1)

**Notes:**  
User tested thoroughly. No concerns. Policy activated immediately.
```

### Example 2: Low Confidence, Escalated

```
### Policy ID: api_ratelimit_aggressive_v1

**Submission Date:** 2026-04-11 10:00 UTC  
**Submitter:** bob@example.com  
**Domain:** API_RateLimit  
**Status:** Escalated  
**Confidence Score:** 0.58  

**Policy Intent:**  
Reduce API rate limit from 1000 req/min to 500 req/min to save bandwidth.

**Rationale:**  
Want to reduce infrastructure costs.

**Success Metric:**  
Bandwidth usage drops 50%.

**Dependencies:**  
- None

**Failure Modes:**  
If breaks: legitimate users hit rate limit, API errors increase, customers complain.

**Testing Status:**  
No. Submitting directly without testing.

**Risks & Mitigations:**  
- Risk: Breaks existing integrations. Mitigation: TBD (not thought through)
- Risk: Costs savings negligible vs. customer impact. Mitigation: None identified

**Validation Timeline:**  
- Submitted: 2026-04-11 10:00 UTC
- Tier 1 (cache): MISS (new policy) 2026-04-11 10:05 UTC
- Tier 2 (delta): PASS (within API_RateLimit domain) 2026-04-11 10:10 UTC
- Tier 3 (sandbox): FAIL (Homeostasis=0.72 < target 0.85, multiple customer integrations broke) 2026-04-11 11:00 UTC
- Decision: ESCALATE (Confidence 0.58 < gate 0.70, Homeostasis failure) 2026-04-11 11:05 UTC

**Git Provenance:**  
/enct-logs/provenance.jsonl line 58 (2026-04-11T11:05:00Z api_ratelimit_aggressive_v1)

**Escalation Details:**  
Routed to Ops team for human review. Concern: insufficient analysis. Ops team decides: "Request more customer impact analysis before considering this policy."

**Notes:**  
Policy rejected by Ops. Submitter should re-submit after customer impact analysis and with proposed mitigation for existing integrations.
```

### Example 3: Rolled Back

```
### Policy ID: perf_timeout_strict_v1

**Submission Date:** 2026-04-08 09:00 UTC  
**Submitter:** carol@example.com  
**Domain:** Performance  
**Status:** Rolled Back  
**Confidence Score:** 0.71  

**Policy Intent:**  
Reduce max response time from 1000ms to 200ms.

**Rationale:**  
Improve user experience with faster responses.

**Success Metric:**  
P99 response time <200ms.

**Dependencies:**  
None

**Failure Modes:**  
If breaks: API timeouts increase, error rate spikes, users see errors.

**Testing Status:**  
Yes. Tested on staging for 8 hours.

**Risks & Mitigations:**  
- Risk: Some endpoints can't be that fast (upstream APIs slow). Mitigation: Exemption list for known-slow endpoints.

**Validation Timeline:**  
- Submitted: 2026-04-08 09:00 UTC
- Tier 1 (cache): MISS (new policy) 2026-04-08 09:05 UTC
- Tier 2 (delta): PASS (within Performance domain) 2026-04-08 09:10 UTC
- Tier 3 (sandbox): PASS (Homeostasis=0.86, acceptable impact) 2026-04-08 10:00 UTC
- Decision: ACCEPT (Confidence 0.71 ≥ gate 0.65) 2026-04-08 10:05 UTC

**Activation Date:** 2026-04-08 10:30 UTC  
**Rollback Date:** 2026-04-09 16:00 UTC (age: 30 hours, human approval required and granted)

**Rollback Reason:** Policy activated 30 hours ago. Monitoring detected Homeostasis=0.79 (drop from 0.86). Customer complaints: 5% of requests timing out. Root cause: Upstream API partner slow today. Rollback approved by Ops. Policy reverted to prior (1000ms timeout). Homeostasis recovered to 0.87.

**Analysis:**  
Policy itself was sound (proved in sandbox). But real-world upstream dependency slower than staging. Need to add exemptions for slow partners or increase timeout. Policy can be resubmitted with fixes.

**Git Provenance:**  
- Activation: /enct-logs/provenance.jsonl line 45 (2026-04-08T10:05:00Z perf_timeout_strict_v1)
- Rollback: /enct-logs/provenance.jsonl line 102 (2026-04-09T16:00:00Z rollback_perf_timeout_strict_v1)

**Notes:**  
Well-intentioned policy, but missed real-world dependency complexity. Staged testing didn't match production conditions. Lesson: Need to test with real upstream API traffic, not mocks.
```

---

## Ledger Queries & Searches

### By Status
- **All Draft policies:** `grep "^Status: Draft" POLICY-LEDGER.md`
- **All Active policies:** `grep "^Status: Active" POLICY-LEDGER.md`
- **All Rolled Back:** `grep "^Status: Rolled Back" POLICY-LEDGER.md`
- **All Escalated (pending decision):** `grep "^Status: Escalated" POLICY-LEDGER.md`

### By Domain
- **All Authentication policies:** `grep "^Domain: Authentication" POLICY-LEDGER.md`
- **All Performance policies:** `grep "^Domain: Performance" POLICY-LEDGER.md`

### By Date Range
- **Policies submitted last 7 days:** `grep "2026-04-0[4-5]" POLICY-LEDGER.md` (if today is 2026-04-11)

### By Confidence
- **Low confidence (< 0.7):** `grep "^Confidence Score: 0\.[0-6]" POLICY-LEDGER.md`
- **High confidence (> 0.8):** `grep "^Confidence Score: 0\.[89]" POLICY-LEDGER.md`

---

## Ledger Statistics (Updated Monthly)

After each month, record summary stats:

```
## Month: April 2026

**Total Submissions:** 12  
**By Status:**
- Active: 9
- Rolled Back: 2
- Rejected: 1
- Escalated (pending): 0

**By Domain:**
- Authentication: 4 (2 active, 1 rolled back, 1 rejected)
- API_RateLimit: 3 (all active)
- Performance: 2 (1 active, 1 rolled back)
- Access Control: 2 (all active)
- DataValidation: 1 (active)

**Confidence Stats:**
- Average: 0.76
- Min: 0.58 (rejected)
- Max: 0.92

**Rollback Rate:** 2/12 = 16.7% (above target 5%, investigate)
**Axiom Violations:** 0
**Escalations (human review):** 1

**Trends:**
- Rollback rate higher than target; investigate domain-specific issues
- Performance domain showing fragility; need staging improvements
```

---

## Integration with Upstream Intake Gate (P2-5)

**Bootstrap workflow with ledger gate:**

```
1. User submits policy → Fills POLICY-INTAKE-TEMPLATE.md
                            ↓
2. Bootstrap system checks: Is this policy in POLICY-LEDGER.md?
                            ↓
              ┌─────────────────────────────────┐
              ↓                                 ↓
           YES (exists)                    NO (not in ledger)
              ↓                                 ↓
        (Continue to                     REJECT with message:
         Tier 1 validate)                "Policy not in ledger. Submit
                                         to ledger first."
                                             ↓
                                      (Redirect to ledger intake)
                                             ↓
                                      (User adds to POLICY-LEDGER.md
                                       as Draft, returns to bootstrap)
```

**Result:** Every policy in production has corresponding ledger entry. 100% traceability.

---

## Maintenance

### Weekly Review
- Check for policies in "Escalated" state >8 hours (SLA breach)
- Tally rollback rate (target <5%)
- Review recent rejections for patterns

### Monthly Archive
- Move "Rolled Back" policies >30 days old to archive
- Summarize statistics (see above)
- Identify trends

### Quarterly Analysis
- Compare rollback rate trend (improving or degrading?)
- Review domain-specific performance (which domains most rollbacks?)
- Update FAILURE-LEDGER.md with learned lessons

---

**Ledger Status:** Empty (will be populated during Phase 4–5 as policies are submitted)  
**First entries expected:** Week 1 of Phase 4 Deployment (user onboarding)
