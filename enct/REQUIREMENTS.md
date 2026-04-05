# ENCT v1.3 Requirements Ledger

**Purpose:** Explicit specification of all user stories, functional requirements, and acceptance criteria for each ALM phase.

**See Also:** HE-IMPLEMENTATION-PLAN.md (Phase 1–5 execution)

---

## Phase 1: Design — Requirements

### Requirement P1-D-1: Product Vision
**User Story:** As a product manager, I want a clear product vision so users understand what ENCT agent does and why.

**Functional Requirements:**
- Product one-liner: "ENCT v1.3 is a downloadable, out-of-box full agent product that lets users bootstrap AI policies via natural language, with normative control and automatic harnessing as the unbreakable core."
- Key capabilities listed: policy bootstrap, automatic validation, axiom enforcement, live monitoring
- Target users identified: AI researchers, policy designers, system auditors, compliance engineers

**Acceptance Criteria:**
- ✓ Product vision documented in Phase 1 spec (2–3 pages)
- ✓ User personas created (≥3 distinct personas with names, goals, pain points)
- ✓ Use cases documented (≥5 real-world scenarios showing how users will interact)

**References:** ENCT-REFERENCE.md §1–2 (Primitives & Axioms)

---

### Requirement P1-D-2: Architecture Blueprint
**User Story:** As an architect, I want a clear system architecture so I can understand how ENCT primitives map to code components.

**Functional Requirements:**
- Component diagram showing: Bootstrap Agent, Verification Agent, Monitoring Dashboard, Policy Store, Provenance Log
- Data flow: Policy submission → Tiered Validation → Execution → Monitoring
- Technology choices: language (Python/Go?), database (SQL/NoSQL?), deployment (Docker/SaaS?)
- Axiom enforcement layers: Which components ensure each axiom?

**Acceptance Criteria:**
- ✓ Architecture diagram (C4 format) in Phase 1 spec
- ✓ Component descriptions (2 pages)
- ✓ Axiom enforcement mapped to components (table showing Axiom 1–4 ↔ Component responsibilities)

**References:** ENCT-REFERENCE.md §1 (Primitives), §3 (5-phase Loop)

---

### Requirement P1-D-3: UI/UX Wireframes
**User Story:** As a user, I want to understand the user experience so I can evaluate if the product meets my needs.

**Functional Requirements:**
- "New Policy" submission form (Socratic questioning interview)
- Live dashboard showing 8 indicators in real-time
- Policy history browser (past bootstraps, rollbacks)
- Escalation/decision notification system
- Admin panel for confidence gates and constraints

**Acceptance Criteria:**
- ✓ Wireframes for 5+ key screens (low-fidelity is fine)
- ✓ User flows documented (submission → validation → acceptance → monitoring)
- ✓ Socratic question template shown in wireframe

**References:** P1-11 (Socratic Questioning), INDICATORS.md (8 metrics)

---

### Requirement P1-D-4: Autonomy Gates Specification
**User Story:** As a safety engineer, I want explicit bounds on what policies agents can bootstrap so I can confidently deploy without human review overhead.

**Functional Requirements:**
- Domain boundary definition: Policies can target X, Y, Z domains only
- Axiom immutability gate: Policies cannot disable Axioms 1–4
- Confidence threshold: Bootstrap confidence must exceed 0.7 (configurable per domain)
- Rate limits: Max N bootstraps per hour, max M policies per session
- Rollback scope: Can rollback policies <24h old; older policies require human approval

**Acceptance Criteria:**
- ✓ AUTONOMY-GATES.md written and committed (≥3 pages)
- ✓ All gates referenced in Phase 1 spec
- ✓ Phase 4 bootstrap UI design includes these gates

**References:** AXIOMS.md (Axiom 1), P2-4 (Bounded Autonomy)

---

### Requirement P1-D-5: Reference Documentation
**User Story:** As a developer, I want a complete reference document so I can implement ENCT exactly as specified.

**Functional Requirements:**
- Complete ENCT v1.3 theory: primitives, axioms, 5-phase Loop, indicators, verification approaches
- Separate docs for each: AXIOMS.md, INDICATORS.md, VERIFICATION.md, GLOSSARY.md
- Failure Ledger template for documenting incidents
- All theory linked to test/code requirements

**Acceptance Criteria:**
- ✓ ENCT-REFERENCE.md created (comprehensive, all sections present)
- ✓ All companion docs created and linked
- ✓ Every axiom has enforcement test requirement specified

**References:** ENCT-REFERENCE.md (complete)

---

### Requirement P1-D-6: 10–15 Page Design Specification
**User Story:** As a technical lead, I want a complete design spec so I can kick off Phase 2 development with zero ambiguity.

**Functional Requirements:**
- Executive summary (1 page): product vision, key metrics, success criteria
- Primitives & axioms (2 pages): how ENCT theory maps to product
- Architecture blueprint (2 pages): components, data flow, tech stack decisions
- UI/UX wireframes (3 pages): key screens and user flows
- Autonomy Gates (2 pages): domain boundaries, confidence thresholds, rate limits
- Acceptance criteria (1 page): what "Phase 1 complete" looks like

**Acceptance Criteria:**
- ✓ Single cohesive design document (10–15 pages)
- ✓ All diagrams, wireframes, tables included
- ✓ Signed off by user (approval = move to Phase 2)

**References:** All above requirements

---

## Phase 2: Train — Requirements

### Requirement P2-T-1: Working Prototype
**User Story:** As a developer, I want a working ENCT prototype so I can validate the design and build confidence in the architecture.

**Functional Requirements:**
- Bootable Python/Go codebase with directory structure from HE-SCOPE.md
- Bootstrap endpoint: `POST /bootstrap` accepts policy JSON, returns validated policy + confidence
- All four axioms mechanically enforced in code (not just tested)
- LLM-Assisted Bootstrap Pattern (§6.5) implemented: CandidateModule, quality gates ≥0.7, sandbox, provenance

**Acceptance Criteria:**
- ✓ Prototype repo builds without errors
- ✓ `./scripts/enct-bootstrap --policy-id test_1 --domain auth` succeeds
- ✓ All 4 axioms implemented with tests (see Phase 2-T-2)

**References:** ENCT-REFERENCE.md §6.5, AXIOMS.md

---

### Requirement P2-T-2: Complete Test Suite
**User Story:** As a QA engineer, I want comprehensive tests so I can have confidence the system respects all axioms before Phase 3.

**Functional Requirements:**
- Unit tests for all 4 axioms (Axiom 1–4)
- Integration tests for all 5 Loop phases (Sense → Validate → Execute → Assess → Re-enact)
- Tests for tiered validation (Tier 1, 2, 3 gates)
- Homeostasis score calculation tests
- Confidence score determination tests

**Acceptance Criteria:**
- ✓ `pytest tests/` passes 100%
- ✓ >95% code coverage
- ✓ All axiom invariants have corresponding test
- ✓ CI/CD runs tests automatically on every commit

**References:** VERIFICATION.md §5

---

### Requirement P2-T-3: Integrated Harness Features
**User Story:** As an ops engineer, I want harness features (linters, enforcement, versioning) integrated so the system self-corrects.

**Functional Requirements:**
- P2-1 Automated Linters: Custom linter validates ENCT-REFERENCE.md completeness
- P2-2 Dependency Enforcement: Code checklist verifying all axioms implemented
- P0-8 Harness Versioning: ENCT-VERSION.md with changelog, Git tags
- P0-9 Smart Wrappers: `./scripts/enct-{bootstrap,verify,rollback}` CLI utilities
- P3-2 Documentation Sync: CI gate blocks doc-code mismatches

**Acceptance Criteria:**
- ✓ All scripts in ./scripts/ are executable and documented
- ✓ CI runs linters and enforcement checks
- ✓ ENCT-VERSION.md updated for Phase 2 milestone
- ✓ Git tags mark phase completions

**References:** HE-IMPLEMENTATION-PLAN.md §2-1 through 2-7

---

## Phase 3: Test — Requirements

### Requirement P3-T-1: Full Verification Suite Passes
**User Story:** As a security engineer, I want to run the complete verification suite so I can certify the system is safe for deployment.

**Functional Requirements:**
- Run model checking on ENCT Loop (formal invariant verification)
- Execute sandbox simulation with 500+ scenarios (normal, stress, adversarial, recovery)
- Inspect all provenance bundles for completeness and integrity
- Run red-team tests (10+ adversarial attacks)
- Ensure Homeostasis ≥0.85 in all scenarios, Compliance Rate >99%

**Acceptance Criteria:**
- ✓ Model checking: All 4 axiom invariants proven
- ✓ Sandbox simulation: All 500+ scenarios pass, Homeostasis ≥0.85 for 100%
- ✓ Provenance: 100% of bundles complete and consistent
- ✓ Red-teaming: 0 attacks succeed (100% caught)
- ✓ Determinism: Identical input → identical output for 100% of tests

**References:** VERIFICATION.md §1–4

---

### Requirement P3-T-2: Test Report & Certification
**User Story:** As a program manager, I want a formal test report so I can confidently proceed to Phase 4 deployment.

**Functional Requirements:**
- Executive summary: pass/fail for each verification category
- Detailed results: model checking coverage, scenario results, provenance statistics, red-team outcomes
- Gap analysis: any deviations from Phase 1 spec
- Sign-off checklist: user approval to proceed to Phase 4

**Acceptance Criteria:**
- ✓ Test report generated (5–10 pages)
- ✓ All verification categories show "PASS"
- ✓ User signature/approval on document
- ✓ Phase 3 git tag created (v1.3.0-phase3-complete)

**References:** VERIFICATION.md (all sections)

---

## Phase 4: Deploy — Requirements

### Requirement P4-D-1: Installer & Packaged Product
**User Story:** As an end user, I want to download and run ENCT with one click so I don't need custom engineering.

**Functional Requirements:**
- Single-click installer (macOS .dmg, Windows .exe, Linux .AppImage)
- Embedded UI with policy submission form (Socratic questioning)
- Live dashboard showing all 8 indicators
- Automatic startup on system reboot
- Uninstall capability (clean removal)

**Acceptance Criteria:**
- ✓ Installer builds successfully (`make build-installer`)
- ✓ First-time user can bootstrap a policy in <5 minutes
- ✓ Dashboard displays live metrics immediately after installation
- ✓ Release notes provided with version information

**References:** Phase 4 Deployment planning

---

### Requirement P4-D-2: User Onboarding Wizard
**User Story:** As a new user, I want guided onboarding so I understand how to submit policies safely.

**Functional Requirements:**
- Interactive wizard: Welcome → Domain selection → Policy intent → Socratic Q&A → Confidence review → Submit
- Help text for each step
- Example policies showing good/bad submissions
- Link to documentation and ENCT-REFERENCE.md

**Acceptance Criteria:**
- ✓ Wizard completes in 5–10 minutes for typical user
- ✓ All users can describe what their policy does after wizard
- ✓ 100% of submitted policies have answered Socratic questions

**References:** P1-11 (Socratic Questioning)

---

### Requirement P4-D-3: Audit & Escalation Workflows
**User Story:** As an auditor, I want to see all policy decisions and escalations so I can maintain governance.

**Functional Requirements:**
- Audit log of all bootstrap decisions (accept, reject, escalate)
- Escalation queue showing pending human reviews
- Audit trail inspection UI (browse provenance bundles)
- Approval/rejection workflow for escalated policies

**Acceptance Criteria:**
- ✓ All decisions logged to audit trail (100% traceability)
- ✓ Escalations resolved within 24 hours
- ✓ Audit trail searchable by policy ID, date, decision type

**References:** P0-7 (Escalation), VERIFICATION.md §3 (Audit Trail Inspection)

---

## Phase 5: Monitor — Requirements

### Requirement P5-M-1: Live Observability Dashboard
**User Story:** As an operations engineer, I want real-time visibility into system health so I can detect and respond to issues.

**Functional Requirements:**
- Stream all 8 indicators in real-time (updated every cycle)
- Visual dashboard: metric graphs, status lights, trends
- Alert rules: automatic notifications if metric drops below threshold
- Historical data: last 7 days of metric history
- Drill-down: click metric → see contributing policies, incidents

**Acceptance Criteria:**
- ✓ Dashboard loads and updates in <100ms
- ✓ All 8 indicators visible and correctly calculated
- ✓ Alerts fire within 1 minute of threshold breach
- ✓ Zero false positives (alert only on real problems)

**References:** INDICATORS.md (all 8 metrics), P1-5 (Observability)

---

### Requirement P5-M-2: Consolidation & Maintenance Loops
**User Story:** As a system architect, I want automated maintenance so the system stays healthy without manual intervention.

**Functional Requirements:**
- P3-1 Scheduled Cleanups: Weekly sweep of old logs, test artifacts
- P3-4 Consolidation Loop: Daily reconciliation of ENCT-REFERENCE.md vs. code
- P3-2 Documentation Sync: Automated doc-code consistency checks
- P3-3 Pattern Auditing: Monthly report of dead code, circular dependencies

**Acceptance Criteria:**
- ✓ All cleanup jobs run on schedule (cron/CI-based)
- ✓ No manual intervention needed
- ✓ Drift alerts fire within 24 hours of detection
- ✓ Cleanup reports available for review

**References:** HE-IMPLEMENTATION-PLAN.md §3 (Tier 3 items)

---

## Success Criteria (Overall)

### Phase 1 Complete When:
- ✓ Design spec written and approved (10–15 pages)
- ✓ All 8 Tier 1 requirements met
- ✓ User confident in product vision and direction

### Phase 2 Complete When:
- ✓ Working prototype builds and runs
- ✓ >95% test coverage
- ✓ All axioms enforced in code
- ✓ Phase 1 design spec validated by prototype

### Phase 3 Complete When:
- ✓ All verification approaches pass (model checking, sandbox, audit, red-team)
- ✓ Homeostasis ≥0.85 in all 500+ scenarios
- ✓ Zero axiom violations undetected
- ✓ Test report signed off

### Phase 4 Complete When:
- ✓ User can download and install in <5 minutes
- ✓ First policy bootstrapped and deployed
- ✓ Audit trails complete and queryable
- ✓ Escalation workflows tested

### Phase 5 Complete When:
- ✓ Live dashboard shows all 8 indicators
- ✓ Alerts fire correctly
- ✓ Maintenance loops run without manual work
- ✓ System achieves target Homeostasis ≥0.85 consistently

---

## Traceability Matrix

Each requirement is traced to:
- **ENCT Theory:** Which section of ENCT-REFERENCE.md?
- **Harness Feature:** Which P0/P1/P2/P3 feature?
- **Test:** Which test/verification validates it?
- **Design Spec:** Which section of Phase 1 spec?

Example:
```
P1-D-4 (Autonomy Gates)
  ← P2-4 (Bounded Autonomy)
  ← AXIOMS.md (Axiom 1: Immutability)
  ← VERIFICATION.md (Red-team test RT-1)
  ← Phase 1 Spec §5 (Autonomy Gates section)
```

---

**This ledger is updated as requirements evolve through Phases 2–5. All changes tracked in Git.**
