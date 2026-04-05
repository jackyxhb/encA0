# Policy Intake Template — Socratic Questioning

**Purpose:** Formalize the Socratic questioning process for policy submission (Phase 4 Deployment). Ensures users think clearly about their policies before bootstrap.

**See Also:** P1-11 (Socratic Questioning), POLICY-LEDGER.md

---

## Pre-Submission Checklist

Before submitting a policy, users answer these questions. All answers required.

### 1. **What domain does this policy enforce?**

**Question:** Which functional area or scope does this policy apply to?

**Options:** (Examples)
- [ ] Authentication (login, password, MFA)
- [ ] API Rate Limiting
- [ ] Data Validation
- [ ] Access Control
- [ ] Audit Logging
- [ ] Performance Constraints
- [ ] Compliance & Governance
- [ ] Other: _______________

**Why We Ask:** Autonomy gates restrict which domains agents can bootstrap (P2-4). User must select a defined domain.

**Example Good Answer:** "Authentication — password complexity rules"  
**Example Bad Answer:** "General system stuff"

---

### 2. **What specific behavior does this policy enforce?**

**Question:** Describe exactly what the policy requires the system to do.

**Input Field:** Text area (200–500 words)

**Why We Ask:** If the user can't explain it clearly, the policy is poorly conceived.

**Example Good Answer:**
> "When a user tries to create a password, the system must enforce: 1) minimum 12 characters, 2) at least one uppercase letter, 3) at least one number, 4) at least one special character. If any requirement is not met, reject and display specific error message."

**Example Bad Answer:**
> "Make passwords better"

---

### 3. **What behavior should this policy prevent?**

**Question:** What is the failure mode or threat this policy guards against?

**Input Field:** Text area (100–300 words)

**Why We Ask:** Understanding the *why* distinguishes good policies from overconstrained ones.

**Example Good Answer:**
> "This policy prevents brute-force attacks by raising the bar for password cracking. A 12-character password with mixed case/numbers/symbols is significantly harder to crack than simple passwords. This prevents unauthorized account takeovers."

**Example Bad Answer:**
> "I don't know, seems like a good idea"

---

### 4. **What is your success metric for this policy?**

**Question:** How will you know if the policy works as intended? What data will you measure?

**Input Field:** Text area (100–200 words)

**Why We Ask:** Success metrics help us verify the policy's real-world impact. Without metrics, we can't tell if a policy is actually useful.

**Example Good Answer:**
> "Success metric: 0 successful brute-force attacks on this system per month (measured from auth logs). Secondary metric: percentage of users successfully authenticating on first try (target >95%). If brute-force attempts increase OR legitimate authentication failures increase, policy is not working as intended."

**Example Bad Answer:**
> "I'll just see if it works"

---

### 5. **Does this policy depend on other existing policies or norms?**

**Question:** Are there prerequisite policies that must already be in place for this policy to work?

**Input Field:** Checkbox list of known policies (user can add custom)

**Why We Ask:** Policy conflicts cause Homeostasis to drop. Knowing dependencies prevents silent failures.

**Example Good Answer:**
> "Depends on: 1) User registration policy (must exist before auth policy applies), 2) Password hashing policy (must use strong hash algorithm)"

**Example Bad Answer:**
> "No dependencies" (if this is actually false)

---

### 6. **How would you know if this policy broke?**

**Question:** What would be the observable symptoms if the policy malfunction?

**Input Field:** Text area (100–200 words)

**Why We Ask:** This helps us define escalation criteria and monitoring alerts.

**Example Good Answer:**
> "If this policy broke, we'd see: 1) Users unable to log in with valid credentials (authentication failure rate spikes), 2) Easy-to-guess passwords accepted (security regression), 3) Support tickets complaining about password restrictions (user friction), 4) Homeostasis Score drops due to unexpected policy side effects."

**Example Bad Answer:**
> "It won't break" (overconfidence)

---

### 7. **Have you tested this policy in a safe environment?**

**Question:** Have you validated the policy logic before submitting?

**Options:**
- [ ] Yes, tested on staging/dev environment
- [ ] Yes, tested on paper/in documentation
- [ ] No, submitting untested
- [ ] Not applicable (documentation-only policy)

**Why We Ask:** Untested policies have lower Confidence scores. Pre-testing demonstrates care.

**Example Good Answer:**
> "Tested on staging environment. Created 10 test accounts with various passwords. Verified both compliance (invalid passwords rejected) and usability (legitimate users can still authenticate)."

**Example Bad Answer:**
> "No, submitting directly to production"

---

### 8. **What are the risks or downsides of this policy?**

**Question:** Nothing is perfect. What could go wrong?

**Input Field:** Text area (100–200 words)

**Why We Ask:** Understanding tradeoffs shows maturity. Policies with understood risks have better chances of success.

**Example Good Answer:**
> "Risks: 1) Overly strict requirements may frustrate users (increased support burden), 2) Password requirements may be forgotten by users (increased reset requests), 3) Special character requirement may not be supported by all legacy systems (compatibility issues). Mitigations: include clear guidance in UI, provide password reset flow, phase out legacy systems."

**Example Bad Answer:**
> "No risks"

---

## Output: Policy Submission Form

After user answers all 8 questions, generate a structured submission:

```json
{
  "policy_id": "auth_pwd_complexity_v1",
  "submission_date": "2026-04-10T14:32:00Z",
  "submitter": "user@example.com",
  "domain": "Authentication",
  "description": "[User answer to Q2]",
  "rationale": "[User answer to Q3]",
  "success_metric": "[User answer to Q4]",
  "dependencies": "[User answer to Q5]",
  "failure_modes": "[User answer to Q6]",
  "testing_status": "[User answer to Q7]",
  "risks": "[User answer to Q8]",
  "status": "Draft",
  "next_step": "Await bootstrap validation (Tier 1/2/3)"
}
```

This submission is saved to `POLICY-LEDGER.md` and passed to Tier 1 validation (Tier 2 in Phase 2 Design).

---

## Evaluation Rubric

**Good Policy Submission:**
- ✓ All 8 questions answered clearly and thoughtfully
- ✓ Success metrics are measurable
- ✓ Risks/downsides acknowledged and mitigated
- ✓ Dependencies explicitly listed
- ✓ Policy scoped to a single domain (not doing too much)

**Poor Policy Submission:**
- ✗ Vague answers (Q2: "make the system better")
- ✗ Unmeasurable success criteria (Q4: "it works fine")
- ✗ Overconfidence (Q8: "no risks")
- ✗ Undefined dependencies
- ✗ Trying to do too much (affects multiple unrelated domains)

Policies with good submissions → higher Confidence scores.  
Policies with poor submissions → escalated to human review (Confidence <0.7).

---

## Integration with Bootstrap Flow (Phase 4)

```
User fills out Socratic template
         ↓
Submission validated (all 8 Q answered)
         ↓
Added to POLICY-LEDGER.md with status "Draft"
         ↓
Passed to Tier 1 Validation (cache check)
         ↓
Passed to Tier 2 Validation (delta check)
         ↓
Passed to Tier 3 Validation (full sandbox)
         ↓
Confidence score calculated
    ↙                    ↘
Conf >0.7          Conf ≤0.7
  ↓                      ↓
ACCEPT              ESCALATE
                  (human reviews Q1–Q8,
                   decides approve/reject)
```

---

## Example: Good Policy Submission

```
Q1: Domain → "Authentication"
Q2: Behavior → "Password must be minimum 12 characters, mixed case, number, special char"
Q3: Prevents → "Weak passwords vulnerable to brute-force attacks"
Q4: Success Metric → "Zero successful brute-force attacks/month; 95%+ auth success rate"
Q5: Dependencies → "User registration policy (pre-existing); password hashing policy (pre-existing)"
Q6: Failure Modes → "Users unable to log in; support spike; Homeostasis drops"
Q7: Testing → "Yes, tested on staging with 10 test accounts"
Q8: Risks → "Strictness may frustrate users (mitigation: clear guidance); legacy system compatibility (mitigation: phase out)"

Result:
  Strong submission → Higher Confidence → More likely to ACCEPT
  High likelihood of real-world success
```

---

## Example: Poor Policy Submission

```
Q1: Domain → "General"  ← Too broad
Q2: Behavior → "Make security better"  ← Vague
Q3: Prevents → "Bad stuff"  ← No specifics
Q4: Success Metric → "It works"  ← Unmeasurable
Q5: Dependencies → "None"  ← Unlikely true, unchecked
Q6: Failure Modes → "Won't happen"  ← Overconfidence
Q7: Testing → "No"  ← Untested
Q8: Risks → "No risks"  ← Unrealistic

Result:
  Weak submission → Lower Confidence → ESCALATE for human review
  High likelihood of problems in real-world
```

---

**This template is non-negotiable. All Phase 4 policy submissions use this form.**
