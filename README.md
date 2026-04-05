# ENCT v1.3 Agent Project

**Status:** Phase 1 Design Complete | Ready for Phase 2 Training  
**Version:** 1.3.0  
**Last Updated:** 2026-04-05  

---

## Quick Start

**New to this project?** Start here:

1. **What is this?** → Read [Project Overview](#project-overview) below
2. **What's the structure?** → See [Project Organization](#project-organization)
3. **What's the plan?** → Check [Phase Roadmap](#phase-roadmap)
4. **How do I contribute?** → Read [Team Roles](#team-roles) and `.github/CONTRIBUTING.md`

---

## Project Overview

ENCT v1.3 is an **agent product** with **Enactive Normative Control Theory** framework—a system that bootstraps AI policies via natural language while governing itself through immutable axioms, continuous validation, and automatic escalation.

### Key Concepts

- **ENCT** = The agent product being built (what ships to users)
- **Harness Engineering (HE)** = Development methodology for building ENCT safely (temporary, discarded post-deployment)
- **ENCT ≠ HE** = They are orthogonal (not integrated at runtime)

### One-Liner

A policy bootstrapping agent that governs itself through axioms, validates every action via multi-tier verification, measures system health via 8 quantitative indicators, and maintains stability through bounded adaptation—all while remaining transparent and auditable to humans.

---

## Project Organization

### Directory Structure

```
/enct/                           (ENCT Product Docs & Specs)
├── PHASE-1-DESIGN-SPECIFICATION.md    ← START HERE (executive summary)
├── ENCT-REFERENCE.md                  (master theory document)
├── AXIOMS.md                          (axiom enforcement details)
├── INDICATORS.md                      (8 quantitative metrics)
├── VERIFICATION.md                    (verification approaches)
├── REQUIREMENTS.md                    (Phase 1–5 requirements)
├── POLICY-INTAKE-TEMPLATE.md          (Socratic framework)
├── AUTONOMY-GATES.md                  (governance specification)
├── ENCT-VERSION.md                    (versioning scheme)
├── POLICY-LEDGER.md                   (policy registry)
├── FAILURE-LEDGER.md                  (incident log template)
├── GLOSSARY.md                        (terminology)
└── PHASE-1-COMPLETION-REPORT.md       (Phase 1 deliverables)

/harness/                        (Harness Engineering Docs—Development Methodology Only)
├── HE-SCOPE.md                        (audit scope)
├── HE-CLUES.md                        (gap analysis)
├── HE-PRIORITIES.md                   (prioritization)
├── HE-IMPLEMENTATION-PLAN.md          (implementation plan)
└── AUDIT-SUMMARY.md                   (audit summary)

/src/                            (Implementation Code—Not Yet Started)
├── enct/                              (ENCT engine—Phase 2+)
├── harness/                           (HE tooling—dev-time only—NOT shipped)
├── api/                               (API endpoints—Phase 4+)
├── ui/                                (UI/dashboards—Phase 4+)
├── storage/                           (Database—Phase 4+)
├── monitoring/                        (Observability—Phase 5+)
└── tests/                             (Test suites—Phase 2+)

/axioms/                         (Data: Axiom configs)
/indicators/                     (Data: Indicator definitions)
/bootstrap-logs/                 (Data: Bootstrap logs—Phase 4+)
/test-results/                   (Data: Test outputs—Phase 3+)
/enct-configs/                   (Data: ENCT configs—Phase 4+)
/enct-logs/                      (Data: Provenance bundles—Phase 4+)
/enct-decisions/                 (Data: Decision logs—Phase 5+)
/scripts/                        (Scripts: CLI wrappers—Phase 2+)
/framework/                      (Harness framework—Phase 2+)

Root Files:
├── README.md                          (this file)
├── RULES.md                           (project rules for all IDEs)
├── ENCT-TASK-HIERARCHY.md             (task structure + critical path)
├── .cursorrules                       (Cursor IDE rules)
├── .claude.md                         (Claude Code rules)
└── .github/CONTRIBUTING.md            (GitHub contributing guide)
```

### Folder Conventions (Permanent Rules)

| Folder | Contents | Visible To | Purpose |
|--------|----------|-----------|---------|
| `/enct/` | ENCT docs, specs, governance | All IDEs, GitHub, users | Product specification |
| `/harness/` | HE audit, gaps, plans | All IDEs, GitHub, dev team | Development methodology |
| `/src/enct/` | ENCT engine code | All IDEs, GitHub, shipped | Product implementation |
| `/src/harness/` | HE tooling code | All IDEs, GitHub, NOT shipped | Dev-time infrastructure |
| `/src/tests/` | Test code | All IDEs, GitHub, CI/CD | Verification |
| Root | Rules, task hierarchy, CI config | All IDEs, GitHub | Project-level |

---

## Document Inventory & Navigation

### Phase 1 Deliverables (Complete)

**ENCT Specification Documents:**
- [PHASE-1-DESIGN-SPECIFICATION.md](enct/PHASE-1-DESIGN-SPECIFICATION.md) ← **Start here** (consolidated 14-page spec)
- [ENCT-REFERENCE.md](enct/ENCT-REFERENCE.md) — Master theory (primitives, axioms, Loop, indicators, verification)
- [AXIOMS.md](enct/AXIOMS.md) — Axiom 1–4 enforcement details
- [INDICATORS.md](enct/INDICATORS.md) — 8 quantitative metrics with formulas
- [VERIFICATION.md](enct/VERIFICATION.md) — 4 verification approaches + Phase 3 test plan
- [REQUIREMENTS.md](enct/REQUIREMENTS.md) — Phase 1–5 functional requirements
- [AUTONOMY-GATES.md](enct/AUTONOMY-GATES.md) — Governance: domains, gates, escalation rules
- [POLICY-INTAKE-TEMPLATE.md](enct/POLICY-INTAKE-TEMPLATE.md) — 8-question Socratic framework
- [ENCT-VERSION.md](enct/ENCT-VERSION.md) — Versioning scheme (SemVer, axiom versions)
- [POLICY-LEDGER.md](enct/POLICY-LEDGER.md) — Policy registry structure + state machine
- [FAILURE-LEDGER.md](enct/FAILURE-LEDGER.md) — Incident logging template
- [GLOSSARY.md](enct/GLOSSARY.md) — 40+ terms indexed

**Completion Reports:**
- [PHASE-1-COMPLETION-REPORT.md](enct/PHASE-1-COMPLETION-REPORT.md) — Phase 1 deliverables & readiness assessment

**Harness Engineering Documents:**
- [HE-SCOPE.md](harness/HE-SCOPE.md) — Audit scope: baseline, features, gaps
- [HE-CLUES.md](harness/HE-CLUES.md) — 30-feature gap analysis with 3-step assessment
- [HE-PRIORITIES.md](harness/HE-PRIORITIES.md) — Gap scoring, tiering (Tier 1–3)
- [HE-IMPLEMENTATION-PLAN.md](harness/HE-IMPLEMENTATION-PLAN.md) — Tier 1–3 action items + checklist
- [AUDIT-SUMMARY.md](harness/AUDIT-SUMMARY.md) — Audit executive summary

**Project-Level Documents:**
- [ENCT-TASK-HIERARCHY.md](ENCT-TASK-HIERARCHY.md) — Task structure Phases 1–5, critical path analysis
- [RULES.md](RULES.md) — Project rules (visible to all IDEs)
- [.cursorrules](.cursorrules) — Cursor IDE configuration
- [.claude.md](.claude.md) — Claude Code configuration
- [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md) — GitHub contributing guidelines

---

## Phase Roadmap

### Current Status: Phase 1 ✅ COMPLETE

**Phase 1: Design** (Weeks 1–2) ✅
- All theory documented
- Specifications finalized
- Governance framework designed
- Phase 2 requirements clear

**Phase 2: Training** (Weeks 3–6) ⏳ Ready to start
- Implement ENCT engine in `/src/enct/`
- Write axiom enforcement, 5-phase Loop, indicators
- Create unit/integration tests in `/src/tests/`
- Build bootstrap pattern
- **Gate:** Working prototype + >95% test coverage

**Phase 3: Testing** (Weeks 7–10) ⏳ Depends on Phase 2
- Run 500+ scenarios in sandbox
- Model checking for axiom invariants
- Audit trail inspection
- Red-teaming (10+ adversarial tests)
- **Gate:** All verification approaches pass

**Phase 4: Deployment** (Weeks 11–14) ⏳ Depends on Phase 3
- Package ENCT as installers (Docker, desktop, SaaS)
- Implement API endpoints in `/src/api/`
- Build UI dashboards in `/src/ui/`
- Create audit workflows
- **Gate:** Single-click installation works

**Phase 5: Monitoring** (Weeks 15–18) ⏳ Depends on Phase 4
- Deploy observability in `/src/monitoring/`
- Stream all 8 indicators to live dashboard
- Implement alerting and escalation
- Create consolidation loops
- **Gate:** Metrics streaming live, system stable

**Post-MVP: Optimization** (Week 19+) ⏳ After Phase 5
- Performance tuning
- SAS→MAS scalability
- Feature enhancements based on user feedback

---

## Team Roles

### Role Definitions

| Role | Responsibilities | Key Documents | Phase |
|------|-----------------|----------------|-------|
| **Product Manager** | Vision, requirements, prioritization | PHASE-1-DESIGN-SPECIFICATION.md, REQUIREMENTS.md | All |
| **ENCT Architect** | System design, axiom enforcement, Loop implementation | ENCT-REFERENCE.md, AXIOMS.md, VERIFICATION.md | All |
| **Training Engineer** | Phase 2 implementation (engine, axioms, tests) | ENCT-REFERENCE.md, `/src/enct/` | 2 |
| **QA/Test Engineer** | Phase 3 verification, test suites | VERIFICATION.md, `/src/tests/` | 3 |
| **DevOps/Deployment** | Packaging, CI/CD, installers | HE-IMPLEMENTATION-PLAN.md, `/src/harness/` | 4 |
| **Operations/SRE** | Phase 5 monitoring, dashboards, alerting | INDICATORS.md, `/src/monitoring/` | 5 |
| **Security Lead** | Governance, audit review, escalation procedures | AUTONOMY-GATES.md, HE-PRIORITIES.md | All |
| **Compliance Officer** | Regulatory requirements, audit trails | POLICY-LEDGER.md, FAILURE-LEDGER.md | All |

### Team Onboarding Checklist

**Week 1 (Orientation):**
- [ ] Read [PHASE-1-DESIGN-SPECIFICATION.md](enct/PHASE-1-DESIGN-SPECIFICATION.md) (30 min)
- [ ] Read [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md) (10 min)
- [ ] Understand folder structure (Project Organization above) (10 min)
- [ ] Read role description (Team Roles above) (5 min)
- [ ] Review [RULES.md](RULES.md) for your IDE (5 min)

**Week 1–2 (Deep Dive - Role Specific):**
- [ ] Product Manager: Read REQUIREMENTS.md, AUTONOMY-GATES.md
- [ ] ENCT Architect: Read ENCT-REFERENCE.md, AXIOMS.md, VERIFICATION.md
- [ ] Training Engineer: Read ENCT-REFERENCE.md, start Phase 2 plan
- [ ] QA Engineer: Read VERIFICATION.md, Phase 3 test plan
- [ ] DevOps: Read HE-IMPLEMENTATION-PLAN.md, RULES.md
- [ ] SRE: Read INDICATORS.md, Phase 5 observability plan
- [ ] Security Lead: Read AUTONOMY-GATES.md, HE-SCOPE.md
- [ ] Compliance: Read POLICY-LEDGER.md, FAILURE-LEDGER.md

**Week 2 (Setup):**
- [ ] Clone repository
- [ ] Install IDE extensions (.cursorrules, Claude Code, GitHub Copilot)
- [ ] Review RULES.md in your IDE
- [ ] Attend project sync (Phase 1 retrospective, Phase 2 kickoff)
- [ ] Set up development environment (Python, Docker, etc.)

---

## Key Documents by Purpose

### If You Want To...

**Understand the product:**
→ [PHASE-1-DESIGN-SPECIFICATION.md](enct/PHASE-1-DESIGN-SPECIFICATION.md)

**Understand ENCT theory:**
→ [ENCT-REFERENCE.md](enct/ENCT-REFERENCE.md)

**Understand axioms:**
→ [AXIOMS.md](enct/AXIOMS.md)

**Understand metrics:**
→ [INDICATORS.md](enct/INDICATORS.md)

**Understand how to verify ENCT works:**
→ [VERIFICATION.md](enct/VERIFICATION.md)

**Understand what to build (Phase 2):**
→ [REQUIREMENTS.md](enct/REQUIREMENTS.md), PHASE-1-DESIGN-SPECIFICATION.md

**Understand governance & safety:**
→ [AUTONOMY-GATES.md](enct/AUTONOMY-GATES.md)

**Understand project rules:**
→ [RULES.md](RULES.md)

**Understand task structure:**
→ [ENCT-TASK-HIERARCHY.md](ENCT-TASK-HIERARCHY.md)

**Understand harness engineering:**
→ [AUDIT-SUMMARY.md](harness/AUDIT-SUMMARY.md)

**Contribute to this project:**
→ [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md)

**Set up your IDE:**
→ [RULES.md](RULES.md), [.cursorrules](.cursorrules), [.claude.md](.claude.md)

---

## Cross-Reference Map

### ENCT v1.3 Specification Hierarchy

```
PHASE-1-DESIGN-SPECIFICATION.md (14-page consolidated spec)
├─ References: ENCT-REFERENCE.md (master theory)
│   ├─ Sections 2–4 reference AXIOMS.md (detailed axioms)
│   ├─ Section 4 references INDICATORS.md (metric details)
│   ├─ Section 5 references VERIFICATION.md (test strategies)
│   └─ Appendix references all supporting docs
├─ References: REQUIREMENTS.md (Phase 1–5 requirements)
├─ References: AUTONOMY-GATES.md (governance detail)
├─ References: POLICY-INTAKE-TEMPLATE.md (Socratic detail)
├─ References: ENCT-VERSION.md (versioning detail)
└─ References: POLICY-LEDGER.md (registry detail)
```

### Phase 2–5 Planning Hierarchy

```
ENCT-TASK-HIERARCHY.md (Phase 1–5 task structure)
├─ Phase 2: Training
│   └─ References: REQUIREMENTS.md (Phase 2 requirements)
│       └─ References: ENCT-REFERENCE.md (what to build)
├─ Phase 3: Testing
│   └─ References: VERIFICATION.md (test approaches)
│       └─ References: AXIOMS.md (invariants to verify)
├─ Phase 4: Deployment
│   └─ References: HE-IMPLEMENTATION-PLAN.md (deployment infrastructure)
│       └─ References: AUTONOMY-GATES.md (gate implementation)
└─ Phase 5: Monitoring
    └─ References: INDICATORS.md (what to monitor)
        └─ References: ENCT-REFERENCE.md (indicator calculations)
```

### Harness Engineering Context

```
HE-SCOPE.md (baseline assessment)
└─ References: HE-CLUES.md (30-feature gap analysis)
    └─ References: HE-PRIORITIES.md (gap prioritization)
        └─ References: HE-IMPLEMENTATION-PLAN.md (action items)
            └─ Maps to: ENCT specification documents
```

---

## Development Workflow

### For Implementation (Phases 2–5)

1. **Read** the spec → [PHASE-1-DESIGN-SPECIFICATION.md](enct/PHASE-1-DESIGN-SPECIFICATION.md)
2. **Check** requirements → [REQUIREMENTS.md](enct/REQUIREMENTS.md) for your phase
3. **Reference** theory → [ENCT-REFERENCE.md](enct/ENCT-REFERENCE.md) + detailed docs
4. **Implement** in → `/src/enct/` (ENCT), `/src/harness/` (HE), `/src/tests/` (tests)
5. **Follow** rules → [RULES.md](RULES.md) and IDE config
6. **Verify** → Commit message format, cross-references, tests pass

### For Governance & Review

1. **Policy submission** → [POLICY-INTAKE-TEMPLATE.md](enct/POLICY-INTAKE-TEMPLATE.md) (Socratic intake)
2. **Check gates** → [AUTONOMY-GATES.md](enct/AUTONOMY-GATES.md) (domain, confidence, rate limit)
3. **Verify axioms** → [AXIOMS.md](enct/AXIOMS.md) (immutability check)
4. **Log decision** → [POLICY-LEDGER.md](enct/POLICY-LEDGER.md) (registry)
5. **Incident tracking** → [FAILURE-LEDGER.md](enct/FAILURE-LEDGER.md) (if issues arise)

---

## Getting Help

**Questions about:**

- **ENCT theory** → See [ENCT-REFERENCE.md](enct/ENCT-REFERENCE.md) + detailed docs
- **Requirements** → See [REQUIREMENTS.md](enct/REQUIREMENTS.md)
- **Implementation** → See [ENCT-TASK-HIERARCHY.md](ENCT-TASK-HIERARCHY.md) + phase docs
- **Project rules** → See [RULES.md](RULES.md)
- **Contributing** → See [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md)
- **Your role** → See [Team Roles](#team-roles) above
- **Verification** → See [VERIFICATION.md](enct/VERIFICATION.md)

---

## Phase 2 Kickoff

**When Phase 1 is approved, Phase 2 begins immediately:**

**Week 3 (Kickoff):**
- [ ] Team assembled (Training engineer, QA lead, DevOps)
- [ ] Development environment ready (`/src/` folders created, Python/Go setup)
- [ ] First sprint planned (axiom enforcement, unit tests)
- [ ] CI/CD pipeline scaffolded

**Week 3–6 (Training):**
- Implement ENCT engine (`/src/enct/`)
- Write axiom enforcement code
- Create unit & integration tests
- Build bootstrap pattern

**Output:** Working prototype + >95% test coverage

---

## Project Links

- **GitHub:** (repo URL when created)
- **Issues/Tickets:** (tracking system when set up)
- **CI/CD Pipeline:** (GitHub Actions when enabled)
- **Monitoring Dashboard:** (Phase 5+)
- **Documentation Site:** (if deployed)

---

## Version History

| Version | Date | Status | Notes |
|---------|------|--------|-------|
| 1.3.0 | 2026-04-05 | Phase 1 Complete | Design phase finalized, ready for Phase 2 |

---

## License & Attribution

ENCT v1.3 Framework  
Developed with Harness Engineering methodology  
Generated with Claude Code  

---

**Last Updated:** 2026-04-05  
**Next Review:** Phase 2 kickoff (Week 3)  
**Owner:** Project Lead / Product Manager
