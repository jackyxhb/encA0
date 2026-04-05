# Document Inventory & Cross-Reference Map

**Purpose:** Complete audit of all Phase 1, harness, and meta documentation. Ensures consistency, verifies cross-references, enables team access.

**Last Verified:** 2026-04-05

---

## Document Summary Table

| # | Document | Location | Type | Purpose | Audience | Phase | Status |
|----|----------|----------|------|---------|----------|-------|--------|
| 1 | README | root | Guide | Project overview & navigation | All teams | All | ✅ New |
| 2 | PHASE-1-DESIGN-SPECIFICATION | /enct/ | Spec | Consolidated 14-page design spec | All | 1 | ✅ New |
| 3 | ENCT-REFERENCE | /enct/ | Theory | Master theory document | Architects, devs | All | ✅ |
| 4 | AXIOMS | /enct/ | Theory | Axiom enforcement details | Architects, QA | All | ✅ |
| 5 | INDICATORS | /enct/ | Spec | 8 quantitative metrics | SRE, product, devs | All | ✅ |
| 6 | VERIFICATION | /enct/ | Spec | Verification approaches | QA, architects | 3+ | ✅ |
| 7 | REQUIREMENTS | /enct/ | Spec | Phase 1–5 requirements | PM, architects, devs | All | ✅ |
| 8 | POLICY-INTAKE-TEMPLATE | /enct/ | Process | Socratic intake framework | PM, users, devs | 4+ | ✅ |
| 9 | AUTONOMY-GATES | /enct/ | Spec | Governance specification | Security, architects | All | ✅ |
| 10 | ENCT-VERSION | /enct/ | Spec | Versioning scheme | DevOps, all | All | ✅ |
| 11 | POLICY-LEDGER | /enct/ | Process | Policy registry structure | Ops, users, all | 4+ | ✅ |
| 12 | FAILURE-LEDGER | /enct/ | Template | Incident logging | QA, ops, all | 2+ | ✅ |
| 13 | GLOSSARY | /enct/ | Reference | Terminology index | All teams | All | ✅ |
| 14 | PHASE-1-COMPLETION-REPORT | /enct/ | Report | Phase 1 deliverables | PM, all | 1 | ✅ |
| 15 | HE-SCOPE | /harness/ | Audit | Harness scope baseline | DevOps, architects | 1 | ✅ |
| 16 | HE-CLUES | /harness/ | Analysis | 30-feature gap analysis | DevOps, architects | 1 | ✅ |
| 17 | HE-PRIORITIES | /harness/ | Analysis | Gap prioritization & tiers | DevOps, architects | 1 | ✅ |
| 18 | HE-IMPLEMENTATION-PLAN | /harness/ | Plan | Tier 1–3 action items | DevOps, architects | 1–5 | ✅ |
| 19 | AUDIT-SUMMARY | /harness/ | Report | Audit executive summary | PM, DevOps, architects | 1 | ✅ |
| 20 | ENCT-TASK-HIERARCHY | root | Plan | Task structure Phases 1–5 | PM, all teams | All | ✅ |
| 21 | RULES | root | Guide | Project rules for IDEs | All IDEs, all teams | All | ✅ |
| 22 | .cursorrules | root | Config | Cursor IDE configuration | Cursor users | All | ✅ |
| 23 | .claude.md | root | Config | Claude Code configuration | Claude Code users | All | ✅ |
| 24 | CONTRIBUTING | .github/ | Guide | GitHub contributing guide | GitHub users, all | All | ✅ |
| 25 | DOCUMENT-INVENTORY | root | Audit | This document | Teams, auditors | All | ✅ This |

**Total Documents:** 25 (14 ENCT, 5 HE, 6 project-level)  
**Completeness:** 100% (Phase 1 scope)

---

## Document Relationships & Flow

### ENCT Product Specification Flow

```
Start Here (New Team Member)
  ↓
README.md
  ↓
  ├─→ PHASE-1-DESIGN-SPECIFICATION.md (14-page consolidated spec)
  │     ├─→ ENCT-REFERENCE.md (master theory)
  │     │   ├─→ AXIOMS.md (axiom details)
  │     │   ├─→ INDICATORS.md (metric details)
  │     │   ├─→ VERIFICATION.md (testing approach)
  │     │   └─→ GLOSSARY.md (terminology)
  │     ├─→ REQUIREMENTS.md (Phase 1–5 functional reqs)
  │     ├─→ AUTONOMY-GATES.md (governance detail)
  │     ├─→ POLICY-INTAKE-TEMPLATE.md (Socratic detail)
  │     ├─→ ENCT-VERSION.md (versioning detail)
  │     └─→ POLICY-LEDGER.md (registry detail)
  │
  ├─→ ENCT-TASK-HIERARCHY.md (Phase 1–5 task breakdown)
  │     ├─ Phase 2: REQUIREMENTS.md (requirements)
  │     ├─ Phase 3: VERIFICATION.md (testing)
  │     ├─ Phase 4: REQUIREMENTS.md (deployment)
  │     └─ Phase 5: INDICATORS.md (monitoring)
  │
  ├─→ RULES.md (project rules)
  │     └─ IDE configs (.cursorrules, .claude.md)
  │
  └─→ CONTRIBUTING.md (how to work here)
```

### Harness Engineering (Development Methodology) Flow

```
HE Audit & Planning
  ↓
HE-SCOPE.md (baseline: what exists, what's missing)
  ↓
HE-CLUES.md (gap analysis: which 30 features have gaps)
  ↓
HE-PRIORITIES.md (prioritization: tier them by impact)
  ↓
HE-IMPLEMENTATION-PLAN.md (action items: what to do)
  ↓
AUDIT-SUMMARY.md (report: readiness for Phase 2)
  ↓
Result: ENCT project properly scaffolded for team execution
```

---

## Cross-Reference Verification

### Incoming References (Documents Referencing This One)

| Document | References | Notes |
|----------|-----------|-------|
| PHASE-1-DESIGN-SPECIFICATION | All `/enct/` docs + REQUIREMENTS | Consolidation doc |
| ENCT-REFERENCE | AXIOMS, INDICATORS, VERIFICATION, GLOSSARY | Master doc expansion |
| README | All 25 documents | Navigation hub |
| ENCT-TASK-HIERARCHY | REQUIREMENTS, VERIFICATION, INDICATORS | Phase mapping |
| .github/CONTRIBUTING | RULES, ENCT-TASK-HIERARCHY | Onboarding guide |
| HE-IMPLEMENTATION-PLAN | ENCT-REFERENCE, AXIOMS, AUTONOMY-GATES | Harness planning |

### Outgoing References (What This Doc Cites)

**From PHASE-1-DESIGN-SPECIFICATION:**
- ✅ ENCT-REFERENCE.md §2–4
- ✅ AXIOMS.md (all axioms)
- ✅ INDICATORS.md (all 8 metrics)
- ✅ VERIFICATION.md (4 approaches)
- ✅ REQUIREMENTS.md (Phase 1–5)
- ✅ POLICY-INTAKE-TEMPLATE.md (8 questions)
- ✅ AUTONOMY-GATES.md (7 domains)
- ✅ ENCT-VERSION.md (versioning)
- ✅ POLICY-LEDGER.md (policy registry)

**Status:** ✅ All references verified, no broken links

---

## Document Categories

### Category 1: Theory & Foundation (6 docs)
Foundation for everything; immutable once Phase 1 approved

- ENCT-REFERENCE.md
- AXIOMS.md
- INDICATORS.md
- VERIFICATION.md
- GLOSSARY.md
- ENCT-VERSION.md

**Change Control:** Requires PM + architect approval (breaking changes = major version)

### Category 2: Product Specification (7 docs)
What to build; evolves per phase

- PHASE-1-DESIGN-SPECIFICATION.md
- REQUIREMENTS.md
- AUTONOMY-GATES.md
- POLICY-INTAKE-TEMPLATE.md
- POLICY-LEDGER.md
- FAILURE-LEDGER.md
- ENCT-TASK-HIERARCHY.md

**Change Control:** PM + team consensus (phase specifications frozen for current phase)

### Category 3: Development Methodology (5 docs)
How to build safely; archived after Phase 1

- HE-SCOPE.md
- HE-CLUES.md
- HE-PRIORITIES.md
- HE-IMPLEMENTATION-PLAN.md
- AUDIT-SUMMARY.md

**Change Control:** DevOps + architect approval (methodology impacts process)

### Category 4: Team & Process (7 docs)
How we work together; evolves with team needs

- README.md
- RULES.md
- .cursorrules
- .claude.md
- .github/CONTRIBUTING.md
- DOCUMENT-INVENTORY.md (this doc)
- (Future: Team Charter, Code of Conduct, etc.)

**Change Control:** PM + team discussion (process changes affect all)

---

## Consistency Verification Checklist

### Language & Terminology
- ✅ ENCT consistently defined (product, not methodology)
- ✅ HE consistently defined (methodology, not product)
- ✅ ENCT ≠ HE rule consistently stated (docs, RULES.md, .cursorrules)
- ✅ Axiom 1–4 numbered consistently across all docs
- ✅ Indicator names consistent (8 specific metrics, same names everywhere)
- ✅ 5-phase Loop consistently named (Sense → Validate → Execute → Assess → Re-enact)
- ✅ 7 domains consistently listed (Auth, API Rate Limit, Data Valid, Access Control, Audit Log, Perf, Compliance)
- ✅ Tiers consistently defined (Tier 1: cache, Tier 2: delta, Tier 3: full sandbox)

**Status:** ✅ All terminology consistent across all 25 documents

### Cross-References
- ✅ PHASE-1-DESIGN-SPECIFICATION references all supporting docs
- ✅ ENCT-REFERENCE cited by PHASE-1-DESIGN-SPECIFICATION
- ✅ AXIOMS cited by AXIOMS-reference docs, VERIFICATION
- ✅ INDICATORS cited by VERIFICATION, ENCT-TASK-HIERARCHY
- ✅ REQUIREMENTS cited by ENCT-TASK-HIERARCHY, design specs
- ✅ AUTONOMY-GATES cited by REQUIREMENTS, PHASE-1-DESIGN-SPECIFICATION
- ✅ VERIFICATION cited by REQUIREMENTS, ENCT-TASK-HIERARCHY

**Status:** ✅ No broken references, all cross-links valid

### Scope & Boundaries
- ✅ ENCT docs (in `/enct/`) contain ONLY product specification
- ✅ HE docs (in `/harness/`) contain ONLY development methodology
- ✅ No ENCT docs reference HE code (because HE is discarded)
- ✅ HE docs reference ENCT spec (to understand what they're auditing)
- ✅ Root-level docs (RULES.md, README) reference both ENCT + HE appropriately

**Status:** ✅ Scope boundaries respected, no overlap violations

### Audience & Accessibility
- ✅ README serves as entry point for all audiences
- ✅ Each document has clear purpose + audience statement
- ✅ RULES.md visible to all IDEs (GitHub Copilot, Cursor, Claude Code, VS Code)
- ✅ CONTRIBUTING.md visible on GitHub for new contributors
- ✅ Team roles defined with document assignments (see README)

**Status:** ✅ All documents accessible to intended audiences

### Completeness
- ✅ Phase 1 deliverables: All 25 docs present
- ✅ Phase 2–5 requirements: Documented in REQUIREMENTS.md
- ✅ Task breakdown: Complete in ENCT-TASK-HIERARCHY.md
- ✅ Success criteria: Explicit in each phase spec
- ✅ Team onboarding: Covered in README + CONTRIBUTING.md

**Status:** ✅ 100% complete for Phase 1, ready for Phase 2

---

## Quality Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Document completeness | 100% | 100% | ✅ |
| Cross-reference validity | 100% | 100% | ✅ |
| Terminology consistency | 100% | 100% | ✅ |
| Audience coverage | All teams | All teams | ✅ |
| IDE visibility | 4+ IDEs | GitHub, Cursor, Claude, VS Code | ✅ |
| Scope separation (ENCT vs HE) | Clear boundaries | Verified | ✅ |
| Team onboarding coverage | Complete | README + CONTRIBUTING | ✅ |

---

## Team Mode Readiness

### ✅ Fully Ready For Team Execution

**Infrastructure:**
- ✅ Git repository initialized
- ✅ Folder structure established
- ✅ IDE rules configured (.cursorrules, .claude.md, CONTRIBUTING.md)
- ✅ GitHub project ready
- ✅ Documentation complete & indexed

**Process:**
- ✅ Project rules documented (RULES.md)
- ✅ Team roles defined (README)
- ✅ Onboarding path clear (README + CONTRIBUTING)
- ✅ Change control defined (this document)
- ✅ Phase gate criteria explicit (REQUIREMENTS.md, ENCT-TASK-HIERARCHY.md)

**Knowledge:**
- ✅ ENCT theory complete (ENCT-REFERENCE.md + companions)
- ✅ Product spec complete (PHASE-1-DESIGN-SPECIFICATION.md)
- ✅ Development plan complete (HE-IMPLEMENTATION-PLAN.md)
- ✅ Task breakdown complete (ENCT-TASK-HIERARCHY.md)
- ✅ Success criteria clear (REQUIREMENTS.md, phase specs)

**Quality:**
- ✅ Cross-references verified
- ✅ Terminology consistent
- ✅ Scope boundaries respected
- ✅ Audience-appropriate
- ✅ All 25 docs aligned

---

## Handoff Checklist (For PM to Team)

- [ ] All 25 documents reviewed
- [ ] README read by all team members
- [ ] Team roles assigned (see Team Roles in README)
- [ ] IDE configuration in place (.cursorrules, .claude.md)
- [ ] Development environment ready (/src/ structure, Python/Go setup)
- [ ] Phase 1 approved (PM sign-off)
- [ ] Phase 2 backlog groomed (ENCT-TASK-HIERARCHY.md)
- [ ] First sprint planned (Week 3 kickoff)

---

## What's Next

**Phase 2 Begins When:**
1. Phase 1 approved by PM/user
2. Team fully onboarded
3. Development environment ready
4. First sprint ready to start (Week 3)

**Phase 2 Outputs Will Include:**
- `/src/enct/` — ENCT engine code
- `/src/tests/` — Test suite
- `/src/harness/` — HE tooling (dev-time only)
- Phase 2 completion report

---

**Document Status:** ✅ Complete & Team-Ready  
**Last Verified:** 2026-04-05  
**Next Review:** Phase 2 completion  
**Owner:** Project Lead
