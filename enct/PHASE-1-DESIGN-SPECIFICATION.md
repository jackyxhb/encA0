# ENCT v1.3 Phase 1 Design Specification

**Version:** 1.0  
**Date:** 2026-04-05  
**Status:** Ready for Review & Approval  
**Total Pages:** 14  

---

## 1. Executive Summary

### Product Vision

ENCT v1.3 is a downloadable, out-of-box full agent product that enables non-expert users to bootstrap AI policies via natural language, with normative control theory and automatic harnessing as the unbreakable core engine.

**One-liner:** A policy bootstrapping agent that governs itself through axioms, validates every action, and maintains system stability via continuous feedback loops.

### Key Capabilities

1. **Natural Language Policy Bootstrap** — Users submit policies in plain English; agent validates via Socratic questioning
2. **Automatic Normative Control** — Axioms enforce immutable rules; policies cannot override core system
3. **Multi-Tier Validation** — Tiered validation (cache → delta → sandbox) ensures high confidence before deployment
4. **Live Monitoring Dashboard** — Real-time metrics (Compliance Rate, Homeostasis Score, etc.) visible to operators
5. **Automatic Escalation** — Low-confidence or axiom-violating policies escalate to human review
6. **Audit Trail & Rollback** — Full provenance bundles, version tracking, and rollback capability for all policies
7. **Self-Correcting** — System adapts via bounded resilience while preserving axioms

### Target Users

- **AI Researchers** — Studying normative control and agent governance
- **Policy Designers** — Creating and refining organizational norms
- **System Auditors** — Monitoring compliance and trust in AI systems
- **Compliance Engineers** — Ensuring regulatory requirements are mechanically enforced

### Success Criteria (Phase 1)

- ✓ Complete ENCT v1.3 theory encoded in repository
- ✓ 7 functional domains defined (Authentication, API Rate Limiting, Data Validation, Access Control, Audit Logging, Performance, Compliance & Governance)
- ✓ Governance framework (autonomy gates, confidence thresholds, escalation rules) specified
- ✓ Bootstrap pattern (LLM-Assisted Bootstrap) designed with Socratic intake process
- ✓ Verification strategies (4 approaches) documented for Phase 3 testing
- ✓ Phase 2–5 requirements explicit with acceptance criteria
- ✓ All documentation visible to IDEs and development teams

---

## 2. ENCT v1.3 Framework

### 2.1 The Four Primitives

ENCT is built on four foundational primitives:

| Primitive | Definition | Example |
|-----------|-----------|---------|
| **Actant** | Entity with agency and bounded autonomy | Policy bootstrap agent, verification sub-agent |
| **Enactive Action** | Purposeful behavior coupled to environment feedback with uncertainty bounds | Bootstrap action: validate policy → measure confidence → accept/reject |
| **Normative Constraint** | Versioned rule with sanctions; mechanically enforced | "Policies must have confidence ≥0.7"; violations trigger escalation |
| **Cybernetic Loop** | Feedback mechanism for self-regulation and homeostasis | 5-phase Loop: Sense → Validate → Execute → Assess → Re-enact |

### 2.2 The Four Axioms (Immutable Guarantees)

1. **Axiom 1: Foundational Rules Are Immutable**
   - Core rules (axioms, primitives, Loop, base indicators) cannot be overridden
   - Prevents system collapse into arbitrary rule-making
   - **Enforcement:** Pre-commit hooks, CI gates, runtime validation

2. **Axiom 2: Action Determinism**
   - Identical state + action → identical outcome (within declared uncertainty bounds)
   - Enables accountability and reproducibility
   - **Enforcement:** Confidence scores + uncertainty intervals on all actions

3. **Axiom 3: Normative Enforcement**
   - All constraints mechanically enforced (no "soft" enforcement)
   - Documentation without enforcement = not a real constraint
   - **Enforcement:** Pre-commit hooks, CI pipelines, runtime gates

4. **Axiom 4: Adaptive Resilience**
   - System adapts to change but preserves axioms 1–3 and is versioned, auditable, reversible
   - Bounded adaptation prevents drift without preventing needed evolution
   - **Enforcement:** Git versioning, CHANGELOG, rollback procedures

### 2.3 The Five-Phase ENCT Loop

Every policy bootstrap cycle flows through:

```
Phase 1: Sense & Translate
  Input: User policy (natural language)
  Process: Parse & translate to structured form
  Output: Translated policy object + metadata

    ↓

Phase 2: Tiered Validate
  Tier 1 (Cache): Check if identical policy validated recently
  Tier 2 (Delta): Validate only changed parts
  Tier 3 (Full): Full sandbox simulation + Homeostasis scoring
  Output: Confidence score (0.0–1.0) + validation results

    ↓

Phase 3: Execute & Feedback
  Input: Validated policy + confidence score
  Process: If confidence ≥ gate, apply policy; otherwise escalate
  Output: Execution result + immediate feedback

    ↓

Phase 4: Assess & Adapt
  Input: Feedback from Phase 3
  Process: Measure Homeostasis Score, Compliance Rate, Adaptation Resilience
  Output: Assessment metrics + proposed adaptations

    ↓

Phase 5: Re-enact & Log
  Input: Assessment + adaptations
  Process: Apply adaptations, create immutable provenance bundle
  Output: Versioned policy state + audit trail
  Loop closes: Enter Phase 1 with next policy
```

### 2.4 The Eight Quantitative Indicators

All ENCT operations measured by:

| # | Indicator | Formula | Target |
|---|-----------|---------|--------|
| 1 | **Compliance Rate** | (constraints_enforced / total_constraints) × 100% | >99% |
| 2 | **Homeostasis Score** | 1.0 - (distance_from_equilibrium / max_deviation) | ≥0.85 |
| 3 | **Traceability Coverage** | (decisions_with_provenance / total_decisions) × 100% | 100% |
| 4 | **Bootstrap Confidence (Avg)** | sum(confidence_scores) / num_policies | >0.80 |
| 5 | **Adaptation Resilience** | successful_adaptations / total_adaptations | >0.90 |
| 6 | **Provenance Overhead** | (provenance_storage_GB / total_storage_GB) × 100% | <10% |
| 7 | **Axiom Violation Rate** | num_axiom_violations_caught / period_days | <1/month |
| 8 | **Policy Rollback Rate** | (policies_rolled_back_7d / total_policies) × 100% | <5% |

---

## 3. Architecture Blueprint

### 3.1 Component Diagram (C4 Level 1)

```
┌─────────────────────────────────────────────────────────┐
│                   ENCT v1.3 Agent System                 │
│                                                           │
│  ┌──────────────┐         ┌──────────────┐              │
│  │              │         │              │              │
│  │   User       │         │   Admin      │              │
│  │ Interface    │         │  Interface   │              │
│  │              │         │              │              │
│  └──────┬───────┘         └──────┬───────┘              │
│         │                        │                       │
│         └────────────┬───────────┘                       │
│                      │                                   │
│         ┌────────────▼────────────┐                     │
│         │                         │                     │
│         │   ENCT Engine Core      │                     │
│         │                         │                     │
│         │  • Axiom Enforcement    │                     │
│         │  • 5-Phase Loop         │                     │
│         │  • Indicator Calc       │                     │
│         │  • Bootstrap Pattern    │                     │
│         │  • Verification Gates   │                     │
│         │  • Escalation Logic     │                     │
│         │                         │                     │
│         └────────────┬────────────┘                     │
│                      │                                   │
│         ┌────────────┴────────────┐                     │
│         │                         │                     │
│    ┌────▼────┐            ┌──────▼──────┐              │
│    │  Policy │            │ Provenance  │              │
│    │  Store  │            │   Log       │              │
│    │(Versioned)           │ (Immutable) │              │
│    └─────────┘            └─────────────┘              │
│                                                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │       Observability & Monitoring Layer         │   │
│  │  (Stream all 8 indicators to live dashboard)   │   │
│  └─────────────────────────────────────────────────┘   │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### 3.2 Data Flow: Policy Bootstrap Lifecycle

```
User submits policy
  ↓
[Upstream Intake Gate] (P2-5)
  - Policy ledger check
  - Socratic questioning (8 questions)
  ↓
[Autonomy Gates] (P2-4)
  - Domain whitelisting
  - Axiom immutability check
  - Rate limit enforcement
  ↓
ENCT Bootstrap Pattern
  Phase 1: Sense & Translate
  Phase 2: Tiered Validate (Tier 1/2/3)
  Phase 3: Execute & Feedback
  Phase 4: Assess & Adapt
  Phase 5: Re-enact & Log
  ↓
[Verification Gates] (P0-3)
  - Confidence ≥ gate threshold?
  - All axioms respected?
  ↓
  Yes → ACCEPT (policy activated)
  No  → ESCALATE (human review)
  ↓
[Audit Trail] (P0-7)
  - Log immutable provenance bundle
  - Record all decisions
  ↓
[Observability] (P1-5)
  - Stream indicators to dashboard
  - Alert if Homeostasis <0.85
```

### 3.3 Technology Stack (Phase 1 Decisions)

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Language** | Python 3.11+ | Ecosystem (PyTorch, LangChain), rapid prototyping |
| **LLM Integration** | Claude API (Anthropic) | Policy interpretation, bootstrap logic, refinement |
| **Storage** | PostgreSQL (policies), JSON append-only logs (provenance) | Transactional integrity, immutable audit trails |
| **API** | FastAPI | Async, type-safe, auto-docs |
| **Dashboard** | React + TypeScript | Live metric updates, responsive UI |
| **Testing** | pytest + custom simulators | Unit/integration/scenario testing |
| **CI/CD** | GitHub Actions | Pre-commit hooks, CI gates, automated testing |
| **Deployment** | Docker + installer (Phase 4) | Isolated execution, single-click installation |

---

## 4. UI/UX Wireframes & User Flows

### 4.1 Policy Submission Flow (Socratic Intake)

```
┌─────────────────────────────────────┐
│  New Policy Submission              │
├─────────────────────────────────────┤
│                                      │
│ Question 1: What domain?            │
│ [ ] Authentication                  │
│ [ ] API Rate Limiting               │
│ [ ] Data Validation                 │
│ [ ] Access Control                  │
│ [ ] Audit Logging                   │
│ [ ] Performance                     │
│ [ ] Compliance & Governance         │
│                                      │
│ [Next →]                            │
└─────────────────────────────────────┘
     ↓
┌─────────────────────────────────────┐
│  Q2: What behavior does this policy │
│  enforce?                            │
├─────────────────────────────────────┤
│ [Text area - 200-500 words]         │
│                                      │
│ Example: "When a user tries to      │
│ create a password, require:          │
│ 1) 12+ chars, 2) uppercase,         │
│ 3) number, 4) special char"         │
│                                      │
│ [Back] [Next →]                     │
└─────────────────────────────────────┘
     ↓
[Continue through Q3–Q8]
     ↓
┌─────────────────────────────────────┐
│  Policy Summary & Confidence        │
├─────────────────────────────────────┤
│                                      │
│ Policy ID: auth_pwd_complexity_v1  │
│ Domain: Authentication              │
│ Confidence: 0.78 [████████░░]      │
│                                      │
│ Status:                             │
│ ✓ Tier 1 (Cache): MISS             │
│ ✓ Tier 2 (Delta): PASS             │
│ ✓ Tier 3 (Sandbox): PASS           │
│                                      │
│ Recommendation: ACCEPT              │
│ (Confidence 0.78 ≥ gate 0.75)      │
│                                      │
│ [Cancel] [Accept Policy →]          │
└─────────────────────────────────────┘
```

### 4.2 Live Dashboard (Indicators & Alerts)

```
┌──────────────────────────────────────────────────────────┐
│ ENCT v1.3 Live Dashboard                    [Refresh]   │
├──────────────────────────────────────────────────────────┤
│                                                            │
│ ┌─ System Health ──────────────────────────────────────┐ │
│ │                                                       │ │
│ │ Compliance Rate:      98.5%  [████████░░░]  ⚠       │ │
│ │ Homeostasis Score:     0.82  [██████████░]  ⚠       │ │
│ │ Traceability Cov:     100%   [███████████]  ✓       │ │
│ │ Avg Confidence:        0.79  [██████████░]  ⚠       │ │
│ │ Adaptation Resilience: 0.92  [███████████]  ✓       │ │
│ │ Provenance Overhead:   4.2%  [██░░░░░░░░]   ✓       │ │
│ │ Axiom Violations:      0/day [░░░░░░░░░░]   ✓       │ │
│ │ Rollback Rate:         2.1%  [███░░░░░░░]   ✓       │ │
│ │                                                       │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                            │
│ ┌─ Recent Policies ──────────────────────────────────────┐ │
│ │ ID                      Domain      Status     Conf    │ │
│ │ auth_pwd_v1            Auth        Active     0.78    │ │
│ │ api_ratelimit_v2       API_Limit   Rolled     0.58    │ │
│ │ data_valid_v1          Data_Valid  Active     0.85    │ │
│ │ [View All Policies →]                                 │ │
│ └────────────────────────────────────────────────────────┘ │
│                                                            │
│ ┌─ Alerts & Escalations ────────────────────────────────┐ │
│ │ ⚠ Homeostasis below 0.85 (currently 0.82)           │ │
│ │   Recommended: Review recent policy changes          │ │
│ │ [View Analysis →]                                    │ │
│ └────────────────────────────────────────────────────────┘ │
│                                                            │
│ Last Updated: 2026-04-05 14:32:15 UTC                   │
└──────────────────────────────────────────────────────────┘
```

### 4.3 Audit & Escalation Interface

```
┌──────────────────────────────────────────┐
│ Escalated Policies (Awaiting Review)    │
├──────────────────────────────────────────┤
│                                           │
│ Policy: api_ratelimit_aggressive_v1     │
│ Domain: API Rate Limiting               │
│ Submitted: 2026-04-11 10:00 UTC         │
│ Status: ⏳ ESCALATED                    │
│ Confidence: 0.58 (below gate 0.70)      │
│                                           │
│ Socratic Intake Review:                 │
│ Q1: Domain: API_RateLimit ✓             │
│ Q2: Behavior: Reduce limit to 500 ✓     │
│ Q3: Rationale: Cost savings only ⚠      │
│ Q4: Success Metric: Vague ⚠             │
│ Q5: Dependencies: Not checked ⚠         │
│ Q6: Failure Modes: No analysis ⚠        │
│ Q7: Testing: None ✗                     │
│ Q8: Risks: Not identified ✗             │
│                                           │
│ Recommendation:                          │
│ ❌ REJECT or REQUEST RESUBMISSION       │
│                                           │
│ Reason: Insufficient analysis. Policy   │
│ needs customer impact study and risk    │
│ assessment before approval.             │
│                                           │
│ [Approve] [Reject] [Request Changes]   │
└──────────────────────────────────────────┘
```

---

## 5. Governance & Safety Framework

### 5.1 Autonomy Gates (Domain Boundaries)

**7 Defined Domains** (expandable via governance process):

| Domain | Gate Threshold | Approval Authority | Rate Limit |
|--------|----------------|------------------|-----------|
| Authentication | Confidence ≥0.75 | Security Team | 5/hour |
| API Rate Limiting | Confidence ≥0.70 | Ops Team | 10/hour |
| Data Validation | Confidence ≥0.70 | Product Team | 10/hour |
| Access Control | Confidence ≥0.75 | Security Team | 5/hour |
| Audit Logging | Confidence ≥0.70 | Compliance Team | 5/hour |
| Performance | Confidence ≥0.65 | Ops Team | 10/hour |
| Compliance & Governance | Confidence ≥0.80 | Legal Team | 2/hour |

**Out-of-Scope Domains** (automatically rejected):
- "General system policies"
- "Arbitrary runtime changes"
- Anything not in the approved list

### 5.2 Confidence Gates & Escalation

```
Policy Validation Result
  ↓
  Confidence ≥ Domain Threshold?
  ├─ YES → ACCEPT (policy activated immediately)
  │
  └─ NO → ESCALATE to Human Review
           ├─ Domain approval authority reviews Socratic Q's
           ├─ Authority decides: Approve, Reject, or Request Changes
           └─ Decision logged + provenance bundle updated
```

### 5.3 Axiom Immutability (Hardcoded, Unchangeable)

**Cannot be overridden by any policy:**
- Axiom 1: Foundational rules immutable
- Axiom 2: Action determinism required
- Axiom 3: Normative enforcement mandatory
- Axiom 4: Adaptations versioned & reversible

**If policy violates axiom:**
```
Policy submitted: "Disable Axiom 1"
  ↓
Autonomy Gate: Axiom Check
  ↓
❌ REJECTED (violates axiom immutability)
  ↓
🚨 ESCALATE as Critical Incident
  ↓
Security team alerted + investigation logged
```

### 5.4 Rate Limiting & Rollback Scope

**Rate Limits (per domain):**
- Max bootstraps per domain per hour (2–10 depending on domain)
- Max active policies per session (50 total)
- Resets hourly/daily

**Rollback Scope:**
- Policies <24h old: User/agent can rollback directly
- Policies ≥24h old: Requires human approval (may have dependencies)

---

## 6. Verification & Quality Strategy

### 6.1 Four Verification Approaches (Phase 3)

| Approach | What | How | Success Criterion |
|----------|------|-----|------------------|
| **Model Checking** | Formal invariants | TLA+, state machine verification | All 4 axiom invariants proven |
| **Sandbox Simulation** | 500+ scenarios | Normal, stress, adversarial, recovery | Homeostasis ≥0.85 for 100% |
| **Audit Trail Inspection** | Provenance integrity | Parse bundles, check completeness | 100% of decisions traced |
| **Red-Teaming** | Adversarial attacks | Try to violate axioms, bypass gates | 0 attacks succeed (100% caught) |

### 6.2 Phase 3 Testing Plan

**Timeline:** Weeks 7–10

**Deliverable:** Test Report + Certification

**Pass Criteria:**
- ✓ All axiom invariants verified (model checking)
- ✓ All 500+ scenarios pass with Homeostasis ≥0.85
- ✓ 100% of provenance bundles complete & consistent
- ✓ 0 red-team attacks succeed
- ✓ Zero non-deterministic outcomes (axiom 2 verified)
- ✓ Zero axiom violations undetected

---

## 7. Phase Roadmap & Timeline

### 7.1 ALM Phases 2–5 Overview

| Phase | Duration | Key Work | Output | Go/No-Go |
|-------|----------|----------|--------|----------|
| **2: Train** | Weeks 3–6 | Implement ENCT engine, bootstrap pattern, axiom enforcement | Working prototype | >95% test coverage |
| **3: Test** | Weeks 7–10 | Run 500+ scenarios, model checking, red-teaming, audit | Test report | All verifications pass |
| **4: Deploy** | Weeks 11–14 | Package installer, UI, escalation workflows, audit agent | Downloadable product | Single-click install works |
| **5: Monitor** | Weeks 15–18 | Live dashboards, alerts, observability, consolidation loops | Go-live | Metrics streaming live |

### 7.2 Critical Path (18–20 weeks total)

```
Phase 1: Design
  [2 weeks]
      ↓
Phase 2: Train
  [4 weeks]
      ↓
Phase 3: Test
  [4 weeks]
      ↓
Phase 4: Deploy
  [4 weeks]
      ↓
Phase 5: Monitor
  [4 weeks]
      ↓
Production (Post-MVP)
```

**Critical Dependencies:**
- Phase 2 cannot start until Phase 1 design approved
- Phase 3 cannot start until Phase 2 prototype working
- Phase 4 cannot start until Phase 3 verification passes
- Phase 5 cannot start until Phase 4 deployed

### 7.3 Success Milestones

| Milestone | Gate | Approval |
|-----------|------|----------|
| Phase 1 → 2 | Design spec approved | User sign-off |
| Phase 2 → 3 | Prototype builds, >95% test coverage | Test lead sign-off |
| Phase 3 → 4 | All verifications pass (model, sandbox, audit, red-team) | QA lead sign-off |
| Phase 4 → 5 | Installer works, users can bootstrap policies | Product manager sign-off |
| Phase 5 → Live | Dashboards show live metrics, alerts working | Operations lead sign-off |

---

## 8. Acceptance Criteria

### Phase 1 Complete When:

- [x] ENCT v1.3 theory complete (4 primitives, 4 axioms, 5-phase Loop, 8 indicators)
- [x] 7 domains defined with approval authorities
- [x] Confidence gates and autonomy boundaries specified
- [x] Socratic intake process (8 questions) designed
- [x] Verification strategy (4 approaches) documented
- [x] Requirements ledger (Phase 1–5) complete with acceptance criteria
- [x] Task hierarchy documented with dependencies
- [x] Git repository and folder organization established
- [x] All rules visible to IDEs (RULES.md, .cursorrules, CONTRIBUTING.md)
- [ ] **Phase 1 Design Spec approved by user** ← AWAITING NOW

### Phase 2 Ready When:

- [ ] Phase 1 approved
- [ ] Team assigned (Training agent)
- [ ] Development environment set up
- [ ] First sprint (Week 3) ready to begin

---

## Appendix: Supporting Documents

This specification references and consolidates:

- `/enct/ENCT-REFERENCE.md` — Master theory document (full primitives, axioms, Loop, indicators)
- `/enct/AXIOMS.md` — Axiom enforcement details with examples
- `/enct/INDICATORS.md` — Metric formulas and calculations
- `/enct/VERIFICATION.md` — Verification approaches and Phase 3 test plan
- `/enct/REQUIREMENTS.md` — Phase 1–5 functional requirements
- `/enct/POLICY-INTAKE-TEMPLATE.md` — Socratic question framework
- `/enct/AUTONOMY-GATES.md` — Domain definitions and gate specifications
- `/enct/ENCT-VERSION.md` — Versioning scheme and upgrade path
- `/enct/POLICY-LEDGER.md` — Policy registry structure

---

## Sign-Off

**This Phase 1 Design Specification is ready for user review and approval.**

**To proceed to Phase 2 Training, this specification must be:**
1. ✓ Reviewed by user
2. ✓ Approved with or without feedback
3. ✓ Any requested changes incorporated

**User Sign-Off:**

Name: _________________________  
Date: _________________________  
Approval: ☐ Approved    ☐ Approved with feedback    ☐ Changes required

---

**Questions about Phase 1 Design?**  
Review the supporting documents listed in the Appendix, or provide feedback for revision.

**Ready to proceed to Phase 2?**  
Upon approval, Phase 2 Training (implementing ENCT engine in `/src/enct/`) begins immediately.
