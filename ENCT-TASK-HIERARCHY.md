# ENCT Task Hierarchy & Dependencies

**Purpose:** Document the task structure and dependencies across ALM Phases 1–5.

**How to Use:** Reference this hierarchy when using Claude Code TaskCreate/TaskUpdate. Each phase is a top-level task; sub-tasks track phase-specific deliverables.

---

## Top-Level Task Structure

```
[Main] ENCT v1.3 ALM Execution
  ├─ Phase 1: Design (Weeks 1–2)
  │   ├─ 1-1. Git & Repository Setup
  │   ├─ 1-2. ENCT Theory Documentation
  │   ├─ 1-3. Requirements Specification
  │   ├─ 1-4. Socratic Questioning Framework
  │   ├─ 1-5. Autonomy Gates Design
  │   ├─ 1-6. Task Hierarchy & Planning
  │   ├─ 1-7. Versioning Scheme
  │   ├─ 1-8. Policy Ledger Template
  │   └─ 1-9. Phase 1 Design Spec (10–15 pages)
  │
  ├─ Phase 2: Train (Weeks 3–6)
  │   ├─ 2-1. Bootstrap Pattern Implementation
  │   ├─ 2-2. Axiom Enforcement (Code)
  │   ├─ 2-3. Unit Tests (Axioms)
  │   ├─ 2-4. Integration Tests (Loop)
  │   ├─ 2-5. Linters & Enforcement
  │   ├─ 2-6. Smart Command Wrappers
  │   └─ 2-7. Phase 2 Prototype Complete
  │
  ├─ Phase 3: Test (Weeks 7–10)
  │   ├─ 3-1. Model Checking
  │   ├─ 3-2. Sandbox Simulation (500+ scenarios)
  │   ├─ 3-3. Audit Trail Inspection
  │   ├─ 3-4. Red-Teaming
  │   ├─ 3-5. Regression Testing
  │   └─ 3-6. Test Report & Certification
  │
  ├─ Phase 4: Deploy (Weeks 11–14)
  │   ├─ 4-1. Installer Packaging
  │   ├─ 4-2. UI/UX Implementation
  │   ├─ 4-3. Audit & Escalation Workflows
  │   ├─ 4-4. Audit Agent (Secondary)
  │   ├─ 4-5. Documentation & Help
  │   └─ 4-6. Phase 4 Release
  │
  ├─ Phase 5: Monitor (Weeks 15–18)
  │   ├─ 5-1. Observability Dashboard
  │   ├─ 5-2. Alerting & Thresholds
  │   ├─ 5-3. Cleanup & Consolidation Loops
  │   ├─ 5-4. Monitoring Agent
  │   └─ 5-5. Phase 5 Go-Live
  │
  └─ Optimization (Post-MVP)
      ├─ O-1. Performance Tuning
      ├─ O-2. Scalability (SAS→MAS)
      └─ O-3. Feature Enhancements
```

---

## Phase 1: Design — Task Details

### 1-1. Git & Repository Setup
**Status:** Pending → In Progress → Completed  
**Duration:** 30 minutes  
**Depends on:** None  
**Blocks:** 1-2, 1-3, 1-6, 1-7  
**Deliverables:** `.git/` initialized, directory structure created, initial commit

### 1-2. ENCT Theory Documentation
**Status:** Pending  
**Duration:** 2–3 hours  
**Depends on:** 1-1  
**Blocks:** 1-3, 1-5, 2-1 (axiom implementation)  
**Deliverables:** ENCT-REFERENCE.md, AXIOMS.md, INDICATORS.md, VERIFICATION.md, FAILURE-LEDGER.md, GLOSSARY.md

### 1-3. Requirements Specification
**Status:** Pending  
**Duration:** 1–2 hours  
**Depends on:** 1-2  
**Blocks:** 1-9 (design spec)  
**Deliverables:** REQUIREMENTS.md (Phase 1–5 requirements, acceptance criteria)

### 1-4. Socratic Questioning Framework
**Status:** Pending  
**Duration:** 1 hour  
**Depends on:** 1-3  
**Blocks:** 4-2 (UI implementation)  
**Deliverables:** POLICY-INTAKE-TEMPLATE.md (8-question framework)

### 1-5. Autonomy Gates Design
**Status:** Pending  
**Duration:** 2–3 hours  
**Depends on:** 1-2 (axioms), 1-3 (requirements)  
**Blocks:** 2-5 (enforcement code)  
**Deliverables:** AUTONOMY-GATES.md (domain boundaries, confidence gates, rate limits, escalation)

### 1-6. Task Hierarchy & Planning
**Status:** Pending  
**Duration:** 1 hour  
**Depends on:** 1-3  
**Blocks:** 2-1, 3-1, 4-1, 5-1 (phase execution)  
**Deliverables:** This document (ENCT-TASK-HIERARCHY.md)

### 1-7. Versioning Scheme
**Status:** Pending  
**Duration:** 1 hour  
**Depends on:** 1-1 (Git)  
**Blocks:** 2-1, 3-6 (certification)  
**Deliverables:** ENCT-VERSION.md (semantic versioning, CHANGELOG, Git tags)

### 1-8. Policy Ledger Template
**Status:** Pending  
**Duration:** 30 minutes  
**Depends on:** 1-4 (Socratic template)  
**Blocks:** 4-3 (audit workflow)  
**Deliverables:** POLICY-LEDGER.md (ledger structure, status tracking)

### 1-9. Phase 1 Design Spec (Composite)
**Status:** Pending  
**Duration:** 8 hours (consolidated from 1-1 through 1-8)  
**Depends on:** All of 1-1 through 1-8  
**Blocks:** Phase 2 start  
**Deliverables:** Single 10–15 page design document (Phase 1 spec) + user approval/sign-off

---

## Phase 2: Train — Task Details

### 2-1. Bootstrap Pattern Implementation
**Status:** Pending (after Phase 1)  
**Duration:** 2–3 weeks  
**Depends on:** 1-2 (theory), 1-5 (autonomy gates)  
**Blocks:** 2-3, 2-4 (testing)  
**Deliverables:** Working prototype with bootstrap endpoint, CandidateModule class, quality gates

### 2-2. Axiom Enforcement (Code)
**Status:** Pending (after Phase 1)  
**Duration:** 1–2 weeks  
**Depends on:** 1-2 (axiom definitions)  
**Blocks:** 2-3 (axiom tests)  
**Deliverables:** Code implementing all 4 axioms (Axiom 1–4 enforcement)

### 2-3. Unit Tests (Axioms)
**Status:** Pending (after 2-2)  
**Duration:** 1 week  
**Depends on:** 2-2 (axiom code)  
**Blocks:** 3-1 (verification)  
**Deliverables:** `tests/test_axiom{1,2,3,4}.py` (all passing)

### 2-4. Integration Tests (Loop)
**Status:** Pending (after 2-1)  
**Duration:** 1 week  
**Depends on:** 2-1 (bootstrap implementation)  
**Blocks:** 3-2 (sandbox simulation)  
**Deliverables:** `tests/test_sense_translate.py`, `test_tiered_validate.py`, etc. (all 5 phases)

### 2-5. Linters & Enforcement
**Status:** Pending (after 1-5, 1-2)  
**Duration:** 3–5 days  
**Depends on:** 1-5 (gate specs), 1-2 (reference docs)  
**Blocks:** 3-1 (CI validation)  
**Deliverables:** Custom linters, pre-commit hooks, CI pipeline checks

### 2-6. Smart Command Wrappers
**Status:** Pending (after 2-1, 2-2)  
**Duration:** 2–3 days  
**Depends on:** 2-1, 2-2 (bootstrap & axiom code)  
**Blocks:** 3-5 (regression testing)  
**Deliverables:** `./scripts/enct-{bootstrap,verify,rollback}` CLI tools

### 2-7. Phase 2 Prototype Complete
**Status:** Pending (after all of 2-1 through 2-6)  
**Duration:** Composite milestone  
**Depends on:** All of 2-1 through 2-6  
**Blocks:** Phase 3 start  
**Deliverables:** Working prototype repo, ready for Phase 3 testing

---

## Phase 3: Test — Task Details

### 3-1. Model Checking
**Status:** Pending (after Phase 2)  
**Duration:** 1–2 weeks  
**Depends on:** 2-2 (axiom code), 2-5 (enforcement)  
**Blocks:** 3-6 (certification)  
**Deliverables:** Formal verification that all axiom invariants hold

### 3-2. Sandbox Simulation (500+ scenarios)
**Status:** Pending (after Phase 2)  
**Duration:** 2–3 weeks  
**Depends on:** 2-4 (integration tests), 2-6 (wrappers)  
**Blocks:** 3-6 (certification)  
**Deliverables:** All 500+ scenarios pass, Homeostasis ≥0.85 in all

### 3-3. Audit Trail Inspection
**Status:** Pending (after 3-2)  
**Duration:** 1 week  
**Depends on:** 3-2 (provenance bundles generated)  
**Blocks:** 3-6 (certification)  
**Deliverables:** 100% provenance integrity verified

### 3-4. Red-Teaming
**Status:** Pending (after Phase 2)  
**Duration:** 1–2 weeks  
**Depends on:** 2-6 (wrappers, gates)  
**Blocks:** 3-6 (certification)  
**Deliverables:** All 10+ red-team attacks blocked/detected

### 3-5. Regression Testing
**Status:** Pending (after 3-2, 3-4)  
**Duration:** 1 week  
**Depends on:** 3-2, 3-4  
**Blocks:** 3-6 (certification)  
**Deliverables:** No new axiom violations introduced post-Phase 2

### 3-6. Test Report & Certification
**Status:** Pending (after all of 3-1 through 3-5)  
**Duration:** 3–5 days  
**Depends on:** All of 3-1 through 3-5  
**Blocks:** Phase 4 start  
**Deliverables:** Test report (5–10 pages), user sign-off to proceed to Phase 4

---

## Phase 4: Deploy — Task Details

### 4-1. Installer Packaging
**Status:** Pending (after Phase 3)  
**Duration:** 1–2 weeks  
**Depends on:** 2-7 (prototype)  
**Blocks:** 4-6 (release)  
**Deliverables:** macOS .dmg, Windows .exe, Linux .AppImage installers

### 4-2. UI/UX Implementation
**Status:** Pending (after Phase 3, 1-4)  
**Duration:** 2–3 weeks  
**Depends on:** 1-4 (Socratic template), 2-7 (prototype)  
**Blocks:** 4-6 (release)  
**Deliverables:** Policy submission form, live dashboard, admin panel

### 4-3. Audit & Escalation Workflows
**Status:** Pending (after Phase 3, 1-8)  
**Duration:** 1 week  
**Depends on:** 1-8 (policy ledger), 1-5 (autonomy gates)  
**Blocks:** 4-6 (release)  
**Deliverables:** Escalation routing, human approval workflows, audit logs

### 4-4. Audit Agent (Secondary)
**Status:** Pending (after Phase 3)  
**Duration:** 2 weeks  
**Depends on:** 2-7 (prototype), 4-3 (workflow design)  
**Blocks:** 4-6 (release)  
**Deliverables:** Secondary agent implementing peer review of bootstrap outcomes

### 4-5. Documentation & Help
**Status:** Pending (after all Phase 4 items)  
**Duration:** 1 week  
**Depends on:** 4-2, 4-3, 4-4  
**Blocks:** 4-6 (release)  
**Deliverables:** User manual, admin guide, troubleshooting docs, help text

### 4-6. Phase 4 Release
**Status:** Pending (after all of 4-1 through 4-5)  
**Duration:** Composite milestone  
**Depends on:** All of 4-1 through 4-5  
**Blocks:** Phase 5 start  
**Deliverables:** Downloadable product installers, user-ready

---

## Phase 5: Monitor — Task Details

### 5-1. Observability Dashboard
**Status:** Pending (after Phase 4)  
**Duration:** 2 weeks  
**Depends on:** 1-2 (indicators), 4-2 (UI foundation)  
**Blocks:** 5-5 (go-live)  
**Deliverables:** Live dashboard streaming all 8 indicators

### 5-2. Alerting & Thresholds
**Status:** Pending (after 5-1)  
**Duration:** 1 week  
**Depends on:** 5-1 (dashboard metrics)  
**Blocks:** 5-5 (go-live)  
**Deliverables:** Alert rules, notification channels, SLA enforcement

### 5-3. Cleanup & Consolidation Loops
**Status:** Pending (after Phase 4)  
**Duration:** 1–2 weeks  
**Depends on:** 4-2 (running system)  
**Blocks:** 5-5 (go-live)  
**Deliverables:** Scheduled cleanup agents, consolidation loop, auto-drift detection

### 5-4. Monitoring Agent
**Status:** Pending (after 5-1, 5-2)  
**Duration:** 1 week  
**Depends on:** 5-1, 5-2 (alerting)  
**Blocks:** 5-5 (go-live)  
**Deliverables:** Agent that monitors live metrics, triggers escalations

### 5-5. Phase 5 Go-Live
**Status:** Pending (after all of 5-1 through 5-4)  
**Duration:** Composite milestone  
**Depends on:** All of 5-1 through 5-4  
**Blocks:** Optimization phase (post-MVP)  
**Deliverables:** Live monitoring system, system declared "production-ready"

---

## Optimization Phase — Post-MVP (Optional)

### O-1. Performance Tuning
**Status:** Deferred (after Phase 5)  
**Duration:** 1–2 weeks  
**Depends on:** 5-5 (production data)  
**Deliverables:** Optimized bootstrap latency, reduced provenance overhead

### O-2. Scalability (SAS→MAS)
**Status:** Deferred (after Phase 5)  
**Duration:** 2–4 weeks  
**Depends on:** 5-5 (system stable)  
**Deliverables:** Multi-agent orchestration, parallel policy review

### O-3. Feature Enhancements
**Status:** Deferred (user feedback driven)  
**Duration:** Varies  
**Depends on:** 5-5 (initial feedback cycle)  
**Deliverables:** Additional indicators, policy templates, integrations

---

## Critical Path Analysis

**Longest dependency chain (critical path):**
```
1-1 (Git setup)
  → 1-2 (Theory docs)
    → 1-5 (Autonomy Gates)
      → 2-5 (Enforcement)
        → 2-7 (Prototype)
          → 3-1 (Model checking)
            → 3-6 (Certification)
              → 4-1 (Installer)
                → 4-6 (Release)
                  → 5-1 (Dashboard)
                    → 5-5 (Go-Live)

Total: ~18–20 weeks (critical path cannot be shortened without parallel work)
```

**Parallel Opportunities:**
- Phase 1: Items 1-1 through 1-8 can run in parallel (except dependencies noted)
- Phase 2: 2-3/2-4/2-5/2-6 can run in parallel after their dependencies
- Phase 3: 3-1/3-2/3-4 can run in parallel (3-3/3-5 depend on earlier items)
- Phase 4: 4-1/4-2/4-3/4-4/4-5 can run mostly in parallel
- Phase 5: 5-1/5-2/5-3 can run in parallel; 5-4 depends on earlier

---

## How to Use This Hierarchy

1. **Planning:** Reference critical path when estimating total timeline
2. **Task Tracking:** Use Claude Code TaskCreate to track each item
3. **Dependencies:** Use TaskUpdate to wire up `addBlockedBy` relationships
4. **Progress:** Update task status (pending → in_progress → completed) as work progresses
5. **Escalation:** If a task is blocked, identify what's blocking it and prioritize that blocker

---

**Last Updated:** 2026-04-05 (Phase 1 baseline)
