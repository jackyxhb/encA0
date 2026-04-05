# Failure Ledger — ENCT Incident Log

**Purpose:** Document all past axiom violations, failed bootstraps, and lessons learned. This ledger is populated iteratively during Phases 2–5 and becomes a knowledge base for improving the system.

**Status:** Empty (to be filled during Phases 2–5)

---

## Entry Template

Each incident is recorded with:

| Field | Purpose |
| --- | --- |
| **Date** | When was the incident detected? |
| **Incident ID** | Unique identifier (e.g., INC-2026-001) |
| **Incident Type** | Axiom violation, failed bootstrap, rollback, escalation, etc. |
| **Axiom Violated** | Which axiom was affected? (1/2/3/4 or N/A if not axiom-specific) |
| **Root Cause** | Why did this happen? (policy gate too loose, test missing, etc.) |
| **Detection Method** | How was it caught? (CI, audit, user report, monitoring) |
| **Impact** | What was affected? (policies rejected, system unstable, user trust) |
| **Resolution** | How was it fixed? |
| **Prevention** | What test/gate was added to prevent recurrence? |
| **Lesson** | What did we learn? |

---

## Incidents (Phase 2–5)

*To be filled as incidents occur*

### INC-2026-XXX: [Incident Title]

**Date:** YYYY-MM-DD  
**Incident ID:** INC-2026-XXX  
**Incident Type:** [Axiom violation | Failed bootstrap | Rollback | Escalation | Other]  
**Axiom Violated:** [1 | 2 | 3 | 4 | N/A]  
**Root Cause:** [Detailed explanation]  
**Detection Method:** [CI failure | Audit trail review | Monitoring alert | User report | Manual testing]  
**Impact:** [Description of what broke]  
**Resolution:** [Steps taken to fix]  
**Prevention:** [New test/gate/enforcement added]  
**Lesson:** [Insight for future improvements]  

**Example Entry:**

```markdown
### INC-2026-001: Bootstrap Gate Allowed Confidence 0.65

**Date:** 2026-04-10  
**Incident ID:** INC-2026-001  
**Incident Type:** Failed Bootstrap (gate too loose)  
**Axiom Violated:** 3 (Enforcement)  
**Root Cause:** Bootstrap gate was `if confidence > 0.6:` but spec says `>0.7`. Code was outdated.  
**Detection Method:** Monitoring alert: Avg Confidence dropped to 0.68 (below target 0.80)  
**Impact:** 3 policies accepted with low confidence; 1 later rolled back  
**Resolution:** Updated gate to `if confidence > 0.7:` in bootstrap.py  
**Prevention:** Added CI check: grep bootstrap.py for confidence threshold; fail if not 0.7  
**Lesson:** Specification-code mismatch is a real problem. Need automated drift detection.  
```

---

## Summary Statistics (Updated Each Phase)

After each phase, tally:
- Total incidents: TBD (Phase 2)
- Axiom 1 violations: TBD
- Axiom 2 violations: TBD
- Axiom 3 violations: TBD
- Axiom 4 violations: TBD
- Detection rate: TBD (% caught before reaching users)
- Average resolution time: TBD (hours from detection to fix)

---

## Patterns to Watch

As incidents accumulate, look for patterns:

- **Gate Creep:** Confidence threshold slowly loosening (indicates pressure to accept more policies)
- **Documentation Drift:** Specs say X, code does Y (systematic misalignment)
- **Edge Cases:** Same validation path fails in specific scenarios (incomplete test coverage)
- **Concurrent Bugs:** Race conditions under load (concurrency model issues)
- **Rollback Clustering:** Specific policy type frequently rolled back (validation weak for that domain)

If a pattern emerges, escalate and design targeted improvement.

---

## Review Cadence

- **After Phase 2:** Review for validation gate weaknesses
- **After Phase 3:** Review for test coverage gaps
- **After Phase 4:** Review for real-world user incident patterns
- **Monthly (Phase 5):** Review for systemic issues

---

**This ledger is a living document. New incidents are added as they occur. Patterns inform system improvements.**
