# Harness Engineering Implementation Plan — ENCT v1.3

## Protocol Refresh — 2026-04-09

The original implementation plan below assumes the repo is still greenfield. Do not execute it literally against the current repository. Use the selective mutation batch below for the next safe remediation pass.

### Selective Mutation Batch A — Contract And Status Sync

#### A1. Normalize canonical layout references
- Update `AGENTS.md`, `.claude.md`, and `RULES.md` so they agree on the live source layout and the current portable surface.
- Preserve the ENCT-vs-harness separation rule.
- Verify that README, scripts, and workflows still match the same declared layout after the sync.

#### A2. Repair live planning truth
- Update `ENCT-TASK-HIERARCHY.md` or replace it with a current-state status ledger that reflects completed Phase 1 work and actual Phase 2 progress.
- Remove or explicitly mark stale `Pending` markers that contradict current repo claims.
- Ensure the chosen planning surface is the one referenced by agent instructions.

#### A3. Refresh harness documents
- Update `/harness/HE-SCOPE.md`, `HE-CLUES.md`, `HE-PRIORITIES.md`, `HE-IMPLEMENTATION-PLAN.md`, and `AUDIT-SUMMARY.md` so they classify the repo as mature-but-drifted rather than greenfield.
- If the historical greenfield audit is retained, mark it as historical context.

### Selective Mutation Batch B — Enforcement Portability

#### B1. Make local gate installation discoverable
- Document or version the local pre-commit setup so the repo does not depend on an invisible machine-local hook.
- Keep CI as the upstream collective gate.

#### B2. Map rules to actual gates
- For each important rule surface, state whether it is enforced by CI, by local hooks, or by convention only.
- Prefer binary pass/fail gates for high-risk rules.

### Verification For The Refresh Batch

- Re-run structure validation after any contract sync.
- Re-run CI-relevant local commands for the touched surfaces.
- Confirm agent-facing docs and enforcement scripts point to the same directories.

### What Not To Do

- Do not rebuild the repo as if it still lacks requirements, CI, or a harness folder.
- Do not create a second harness audit area when `/harness` already exists.
- Do not add new governance surfaces until the existing ones agree on current truth.

**Project Scope:** ENCT v1.3 (Enactive Normative Control Theory) Full Agent Software Product  
**Scale:** SAS (Single Agent System) with MAS readiness  
**Complexity:** Complex System (full agent product with normative control, monitoring, deployment)  
**Plan Generated:** 2026-04-05  
**Plan Status:** READY FOR USER REVIEW — Tier 1 and Tier 2 Early execution items detailed below

---

## Tier 1 (Immediate Execution) — Phase 1 Design Completion

### 1-1. P0-2 Filesystem & Git Workspace
- **Remediation Level:** Medium (setup + initial structure)
- **Prevention Active:** "Prevent State and File Conflicts" — Without Git, normative constraint versioning is impossible
- **Dependencies:** None
- **Action Items** _(from P0-2 Options):_
  - `git init` — Initialize repository in `/Users/macbook1/work/ENCT/encA0/`
  - `mkdir -p /axioms /indicators /bootstrap-logs /enct-configs /test-results /scripts /framework` — Create directory structure
  - `git add .gitkeep` — Track empty directories
  - `.gitignore` — Exclude artifacts: `*.log`, `*.tmp`, `__pycache__/`, `.DS_Store`
  - `git commit -m "Initial ENCT repository structure"` — First commit
- **Remediation Tier:** Tier 1 — Complete Week 1 of Phase 1
- **Verification:** `git log` shows initial commit; `git status` shows clean tree; directory structure matches above

**Owner:** Bootstrap Agent (Claude Code session)  
**Timeline:** 30 minutes  
**Definition of Done:** Git repo ready; standard directory layout in place; all future work Git-tracked

---

### 1-2. P1-1 Repository as Truth
- **Remediation Level:** Light (meta-doc creation)
- **Prevention Active:** "Prevent Human-Only Documentation" — Agent must have access to all axioms in code
- **Dependencies:** P0-2 (Git workspace must exist)
- **Action Items** _(from P1-1 Options):_
  - `ENCT-REFERENCE.md` — Create master reference document with:
    - Full text of all 4 axioms (from v1.3 design doc)
    - Definition of 4 primitives (Actant, Enactive Action, Normative Constraint, Cybernetic Loop)
    - Exact 5-phase ENCT Loop definition (Sense & Translate → Tiered Validate → Execute & Feedback → Assess & Adapt → Re-enact & Log)
    - All quantitative indicators (§8)
    - All verification approaches (§9)
  - `AXIOMS.md` — Separate file documenting Axiom 1–4 with examples and failure cases
  - `INDICATORS.md` — Separate file listing all metrics with formulas
  - `VERIFICATION.md` — Separate file describing Tier 1/2/3 validation gates
  - `FAILURE-LEDGER.md` — Blank file for documenting past axiom violations and fixes (to be filled in Phases 2+)
  - `GLOSSARY.md` — Terminology from v1.3 design (from §14)
- **Remediation Tier:** Tier 1 — Complete Week 1–2 of Phase 1
- **Verification:** Agent can run `grep -r "Axiom 1" /Users/macbook1/work/ENCT/encA0/` and get multiple hits in repo docs

**Owner:** Bootstrap Agent (Claude Code session)  
**Timeline:** 2–3 hours  
**Definition of Done:** All ENCT theory encoded in repo; no external design docs required to understand architecture

---

### 1-3. P1-10 Requirements Ledger
- **Remediation Level:** Light (meta-doc)
- **Prevention Active:** "Prevent Implicit Requirements" — Design requirements must be explicit before Phase 1 spec is finalized
- **Dependencies:** P1-1 (axioms must be available)
- **Action Items** _(from P1-10 Options):_
  - `REQUIREMENTS.md` — Create with sections:
    - **Phase 1 Design Goals:** Product vision, user personas, success criteria, architectural constraints
    - **Phase 2 Training Goals:** Prototype scope, axiom implementation targets, indicator calculation methods
    - **Phase 3 Testing Goals:** Scenario count (500+), verification target scores (Compliance >99%, Homeostasis ≥0.85)
    - **Phase 4 Deployment Goals:** Installer format, user onboarding flow, rollback procedures
    - **Phase 5 Monitoring Goals:** Live metric streaming, alert thresholds, audit trail immutability
  - Cross-link each requirement to ENCT-REFERENCE.md axioms/indicators it validates
- **Remediation Tier:** Tier 1 — Complete Week 1–2 of Phase 1
- **Verification:** Phase 1 design spec references REQUIREMENTS.md; all design decisions link to requirements

**Owner:** Bootstrap Agent (Claude Code session)  
**Timeline:** 1–2 hours  
**Definition of Done:** Explicit acceptance criteria for all ALM phases; no ambiguity on Phase 1 spec completeness

---

### 1-4. P1-11 Socratic Questioning
- **Remediation Level:** Light (template + procedure)
- **Prevention Active:** "Prevent Unexamined Assumptions" — User policies submitted in Phase 4 must be questioned before bootstrap
- **Dependencies:** P1-10 (requirements ledger for context)
- **Action Items** _(from P1-11 Options):_
  - `POLICY-INTAKE-TEMPLATE.md` — Create Socratic questioning script for Phase 4 UI:
    - "What domain does this policy enforce?" (intent scope)
    - "What behavior should it prevent?" (failure mode)
    - "What is the success criterion?" (metric for compliance)
    - "Does this policy depend on other existing norms?" (dependency check)
    - "How would you know if this policy broke?" (failure detection)
  - `CLAUDDE.md` — Add instruction: "Before bootstrap, run Socratic questioning. Agent should not proceed without clear answers."
  - Integrate template into Phase 4 UI design wireframes
- **Remediation Tier:** Tier 1 — Complete Week 1–2 of Phase 1
- **Verification:** Phase 4 UI includes Socratic form; policy submission blocked until form answered

**Owner:** Bootstrap Agent (Claude Code session) + Phase 1 Design task  
**Timeline:** 1 hour  
**Definition of Done:** Template in repo; Phase 1 design spec references template; Phase 4 wireframes include form

---

### 1-5. P2-4 Bounded Autonomy & Access Control
- **Remediation Level:** Medium (specification + design)
- **Prevention Active:** "Prevent Prompt Injections and Data Leakage" — Agent must not bootstrap unsafe policies
- **Dependencies:** P1-1 (axioms), P1-10 (requirements)
- **Action Items** _(from P2-4 Options):_
  - `AUTONOMY-GATES.md` — Create specification with:
    - **Domain Boundary:** Policies can only target pre-defined domains (e.g., "user login", "API rate limiting", "data validation")
    - **Axiom Immutability:** Axioms 1–4 cannot be overridden; policies cannot contradict them
    - **Rate Limits:** Max N bootstraps per hour, max M policies per session
    - **Escalation Rules:** If confidence <0.5, escalate to human review
    - **Rollback Scope:** Agent can rollback policies up to 24 hours old; older policies require human approval
  - Wire into Phase 1 design as Autonomy Gates section (2–3 pages)
  - Add to CLAUDE.md: "Reject any policy that modifies axioms or exceeds domain boundaries"
- **Remediation Tier:** Tier 1 — Complete Week 2 of Phase 1 (design phase finalization)
- **Verification:** Phase 1 spec includes AUTONOMY-GATES.md; Phase 4 bootstrap code references gates; CI checks gates are enforced

**Owner:** Bootstrap Agent (Claude Code session) + Phase 1 Design task  
**Timeline:** 2–3 hours  
**Definition of Done:** Autonomy Gates spec in Phase 1 design; no bootstrap can exceed boundaries

---

### 1-6. P1-7 Planning, Task Lists & Blackboards
- **Remediation Level:** Light (procedure + memory integration)
- **Prevention Active:** "Prevent Untracked Work" — Each ALM phase must be an explicit tracked task with dependencies
- **Dependencies:** None (uses existing Claude Code TaskCreate)
- **Action Items** _(from P1-7 Options):_
  - `ENCT-TASK-HIERARCHY.md` — Document in project memory:
    - Phase 1 Design → (generates Phase 2 Training requirements)
    - Phase 2 Training → (generates Phase 3 Testing plan)
    - Phase 3 Testing → (generates Phase 4 Deployment checklist)
    - Phase 4 Deployment → (enables Phase 5 Monitoring)
    - Phase 5 Monitoring → (feeds optimization loop)
  - Create Task template: `[Phase] [Objective] — [ALM Phase dependencies]`
  - Update memory system: save task hierarchy to `/Users/macbook1/.claude/projects/-Users-macbook1-work-ENCT-encA0/memory/enct_task_hierarchy.md`
- **Remediation Tier:** Tier 1 — Complete Week 1 of Phase 1
- **Verification:** Project memory accessible; TaskCreate calls use phase-specific templates; dependencies tracked

**Owner:** Bootstrap Agent (Claude Code session)  
**Timeline:** 30 minutes  
**Definition of Done:** Task hierarchy in memory; all ALM phase work tracked via Tasks; no implicit dependencies

---

### 1-7. P0-8 Harness Versioning
- **Remediation Level:** Light (versioning scheme + tracking)
- **Prevention Active:** "Prevent Axiom Drift" — Updated axioms or norms must have version numbers for rollback
- **Dependencies:** P0-2 (Git), P1-1 (axioms in repo)
- **Action Items** _(from P0-8 Options):_
  - `ENCT-VERSION.md` — Create with:
    - Current version: v1.3.0 (from design doc)
    - Changelog section: date, version, change description, breaking changes (if any)
    - Axiom versions: each axiom tied to ENCT version
    - Indicator versions: formula changes tracked separately
  - `git tag -a v1.3.0-phase1 -m "Phase 1 Design complete"` — Tag Phase 1 completion
  - Use semantic versioning: MAJOR.MINOR.PATCH (Axiom changes = MINOR; indicator tweaks = PATCH)
  - Wire into Phase 2 CI: block code commits that don't update ENCT-VERSION.md when axioms/indicators change
- **Remediation Tier:** Tier 1 — Complete Week 2 of Phase 1
- **Verification:** `git describe --tags` shows version; CHANGELOG updated on each phase completion; CI gates version consistency

**Owner:** Bootstrap Agent (Claude Code session)  
**Timeline:** 1 hour  
**Definition of Done:** Version numbering scheme in place; Git tags for each phase; rollback procedures documented

---

### 1-8. P2-5 Upstream Intake Gate
- **Remediation Level:** Medium (specification + UI design)
- **Prevention Active:** "Prevent Unregistered Work" — User policies must be registered in ledger before bootstrap
- **Dependencies:** P1-10 (requirements ledger pattern), P1-11 (Socratic template)
- **Action Items** _(from P2-5 Options):_
  - `POLICY-LEDGER.md` — Create template for Phase 4 UI:
    - Policy ID, name, domain, intent, success metric
    - Submission date, submitter, Socratic answers
    - Status: [Draft | Queued | Bootstrapped | Active | Rolled Back]
    - Link to bootstrap transcripts (once generated)
  - Design Phase 4 bootstrap flow:
    - User submits policy via form → Socratic questioning → Policy added to ledger → Confidence gate → Verification (P0-3)
    - If any step fails, escalate (P0-7) and update ledger status
  - Add gate to CLAUDE.md: "Never bootstrap a policy not in POLICY-LEDGER.md with status [Draft | Queued]"
- **Remediation Tier:** Tier 1 spec (implementation in Phase 4)
- **Verification:** Phase 1 design includes policy intake flow; Phase 4 code implements gate; all policies in ledger before bootstrap

**Owner:** Bootstrap Agent (Claude Code session) + Phase 1 Design task  
**Timeline:** 2 hours (design only; implementation Phase 4)  
**Definition of Done:** Policy ledger template in repo; Phase 1 spec includes intake flow diagram; no unregistered bootstraps possible

---

## Tier 2 (Phase 2–3 Support) — Key Features for Training & Testing

### 2-1. P0-3 Verification (Self & Collective)
- **Remediation Level:** Medium (feature + test suite)
- **Prevention Active:** "Prevent Cascading Hallucinations" — All ENCT Loop cycles must pass verification before completion
- **Dependencies:** P0-2 (Git), P1-1 (axioms in repo)
- **Action Items** _(from P0-3 Options):_
  - `tests/test_axioms.py` — Unit tests for all 4 axioms:
    - Axiom 1 (foundational): test that invariants cannot be violated
    - Axiom 2 (determinism): test that same input → same output
    - Axiom 3 (normative): test that norms are enforced
    - Axiom 4 (adaptive): test that adaptation preserves homeostasis
  - `tests/test_loop_cycles.py` — Integration tests for 5-phase Loop:
    - Sense & Translate: test input parsing
    - Tiered Validate: test Tier 1/2/3 gates (confidence thresholds)
    - Execute & Feedback: test action application
    - Assess & Adapt: test metric calculations
    - Re-enact & Log: test provenance recording
  - `tests/test_verification_gates.py` — Test tiered validation:
    - Tier 1: cache hit check
    - Tier 2: delta validation
    - Tier 3: full sandbox simulation with Lyapunov scoring ≥0.85
  - `scripts/verify.sh` — Wrapper script: run all tests, report pass/fail, exit code 2 if any fail
- **Remediation Tier:** Tier 1 Phase 2 — Implement Week 1 of Phase 2 Training
- **Verification:** All tests pass; CI shows 100% coverage for axiom enforcement; Lyapunov score ≥0.85 in sandbox

**Owner:** Training Agent (Claude Code session Phase 2)  
**Timeline:** 1–2 weeks (Phase 2 Week 1)  
**Definition of Done:** Test suite covers all axioms + Loop stages; CI gates test results; Phase 3 testing is possible

---

### 2-2. P0-7 Escalation Policies & Audit Trails
- **Remediation Level:** Light + Medium (policy definition + logging)
- **Prevention Active:** "Stuck agents" must escalate to humans; axiom violations must create immutable logs
- **Dependencies:** P1-1 (axioms), P0-8 (versioning)
- **Action Items** _(from P0-7 Options):_
  - `ESCALATION-POLICY.md` — Define thresholds:
    - Bootstrap confidence <0.5 → escalate to human review
    - Axiom violation detected → escalate immediately
    - Verification timeout >5 min → escalate
    - Policy conflicts with existing norms → escalate
  - `scripts/log_provenance.py` — Create immutable event log (append-only JSON):
    - timestamp, event type (bootstrap/verify/escalate/rollback), policy ID, axiom state, user action
    - Write to `/enct-logs/provenance.jsonl` (one JSON per line, immutable append)
  - `CLAUDE.md` — Add: "On escalation, log event + rationale; wait for human decision before continuing"
  - Phase 5: wire logs to monitoring dashboard
- **Remediation Tier:** Tier 1 policy definition (Week 1–2 Phase 1), Tier 2 implementation (Phase 2)
- **Verification:** Escalation policy in CLAUDE.md; provenance logs created for all events; human review log shows decisions

**Owner:** Bootstrap Agent + Training Agent  
**Timeline:** 2 hours (policy) + 1–2 days (implementation)  
**Definition of Done:** Escalation paths defined; all events logged; logs are immutable and auditable

---

### 2-3. P0-9 Smart Command Wrappers
- **Remediation Level:** Medium (CLI scripts)
- **Prevention Active:** "Prevent Manual Errors" — Agents cannot misconfigure critical commands
- **Dependencies:** P1-1 (reference docs), P0-2 (Git)
- **Action Items** _(from P0-9 Options):_
  - `scripts/enct-bootstrap` — CLI wrapper:
    - Validate policy against POLICY-LEDGER.md
    - Run Socratic questioning (automated)
    - Call tiered validation (P0-3)
    - Log to provenance
    - Usage: `./scripts/enct-bootstrap --policy-id <id> --domain <domain>`
  - `scripts/enct-verify` — CLI wrapper:
    - Run full test suite (Tier 1/2/3)
    - Report pass/fail + metrics
    - Exit code 0 (pass) or 2 (fail)
    - Usage: `./scripts/enct-verify --level [1|2|3]`
  - `scripts/enct-rollback` — CLI wrapper:
    - Revert policy to previous version
    - Update POLICY-LEDGER.md status
    - Log rollback reason
    - Usage: `./scripts/enct-rollback --policy-id <id> --reason <reason>`
  - Add to `.cursorrules`: "Use enct-* wrappers for all bootstrap/verify/rollback operations"
- **Remediation Tier:** Tier 2 — Phase 2 Training Week 1
- **Verification:** Wrappers callable from CLI; error handling for invalid arguments; audit logs updated

**Owner:** Training Agent (Claude Code session Phase 2)  
**Timeline:** 1–2 days (Phase 2)  
**Definition of Done:** All critical ENCT operations wrapped; agents cannot execute unwrapped versions

---

### 2-4. P1-9 Branch-Based Memory
- **Remediation Level:** Medium (Git workflow + automation)
- **Prevention Active:** "Prevent Lost Work" — Long bootstrap processes need intermediate checkpoints
- **Dependencies:** P0-2 (Git), P1-8 (context anchoring)
- **Action Items** _(from P1-9 Options):_
  - Create branch strategy:
    - `enct-design` — Phase 1 design branch (merge to main when complete)
    - `enct-train` — Phase 2 training branch (new from main after design merge)
    - `enct-test` — Phase 3 testing branch (new from main after train merge)
    - `enct-deploy` — Phase 4 deployment branch (new from main after test merge)
    - `enct-monitor` — Phase 5 monitoring branch (new from main after deploy merge)
  - After each major phase milestone, auto-commit progress summary:
    - `.claude-progress.md` — Updated with: phase, % complete, blockers, next steps
    - Commit message: `[Phase] Progress: X% complete — [summary]`
  - Update `.cursorrules`: "After major phase milestone, commit progress snapshot"
- **Remediation Tier:** Tier 2 — Phase 2 Week 1
- **Verification:** Git log shows phase branches merged; progress snapshots at each milestone; work survives context resets

**Owner:** Training Agent + Testing Agent + Deployment Agent  
**Timeline:** Ongoing (each phase)  
**Definition of Done:** Phase branches exist; progress snapshots committed; knowledge persists across sessions

---

### 2-5. P2-1 Automated Linters
- **Remediation Level:** Medium (linter setup + CI integration)
- **Prevention Active:** "Prevent Malformed Specs" — Design outputs must follow strict format
- **Dependencies:** P1-1 (axioms available for linting), P0-3 (verification framework)
- **Action Items** _(from P2-1 Options):_
  - `linters/schema-validator.py` — Custom linter for ENCT documents:
    - Check ENCT-REFERENCE.md has all axiom sections
    - Check AXIOMS.md has examples for each axiom
    - Check INDICATORS.md has formulas for all metrics
    - Check VERIFICATION.md has Tier 1/2/3 descriptions
  - `.pre-commit-config.yaml` — Add hooks:
    - `schema-validator.py` on `.md` files in `/framework/`
    - `python -m pytest` on all test commits
  - `.github/workflows/lint.yml` — CI pipeline:
    - Run linters on PR
    - Fail PR if linter errors
    - Comment on PR with `↳ Fix:` suggestions (teaching messages)
- **Remediation Tier:** Tier 2 — Phase 2 Week 1–2
- **Verification:** Pre-commit hooks reject malformed specs; CI blocks PRs with linter errors

**Owner:** Training Agent (Claude Code session Phase 2)  
**Timeline:** 1–2 days (Phase 2)  
**Definition of Done:** Linters integrated into CI; pre-commit hooks active; all commits lint-clean

---

### 2-6. P2-2 Dependency Enforcement
- **Remediation Level:** Medium (structural testing)
- **Prevention Active:** "Prevent Architecture Violations" — Code must implement ENCT exactly as defined in P1-1
- **Dependencies:** P1-1 (Repository as Truth), P0-3 (test framework)
- **Action Items** _(from P2-2 Options):_
  - `tests/test_architecture.py` — Structural tests:
    - Count axiom implementations: must match 4
    - Count indicator calculations: must match count in INDICATORS.md
    - Count Loop stages: must match 5
    - All norms must have provenance: no orphaned policies
  - CI check: `python -m pytest tests/test_architecture.py` must pass before merge
  - CLAUDE.md: "Code must pass architecture tests; no deviations from ENCT-REFERENCE.md allowed"
- **Remediation Tier:** Tier 2 — Phase 2 Week 2
- **Verification:** Architecture tests pass; code structure enforces axioms; deviations detected automatically

**Owner:** Training Agent (Claude Code session Phase 2)  
**Timeline:** 1 day (Phase 2)  
**Definition of Done:** Architecture tests passing; dependency violations blocked by CI

---

### 2-7. P3-2 Documentation Sync
- **Remediation Level:** Medium (CI check)
- **Prevention Active:** "Prevent Documentation Disconnects" — When axiom code changes, ENCT-REFERENCE.md must update
- **Dependencies:** P1-1 (reference docs exist), P2-1 (linters in place)
- **Action Items** _(from P3-2 Options):_
  - `.github/workflows/doc-sync.yml` — CI check:
    - If axiom code changes, fail PR unless ENCT-REFERENCE.md also changes
    - If indicator formula code changes, fail PR unless INDICATORS.md also changes
    - Message: "Code change detected — update corresponding docs in ENCT-REFERENCE.md"
  - `scripts/doc-check.py` — Automated check:
    - Compare modified code files with modified doc files
    - Report mismatches
  - CLAUDE.md: "Whenever you modify axiom or indicator code, update ENCT-REFERENCE.md in same commit"
- **Remediation Tier:** Tier 2 — Phase 2 Week 2
- **Verification:** CI blocks doc-code mismatches; all code changes have corresponding doc updates

**Owner:** Training Agent (Claude Code session Phase 2)  
**Timeline:** 1 day (Phase 2)  
**Definition of Done:** CI enforces doc-code sync; no docs drift from code

---

## Tier 3 (Phase 4–5 & Enhancements)

### 3-1. P1-5 Observability / Dashboards _(Phase 5)_
- **Remediation Level:** Heavy (monitoring infrastructure)
- **Prevention Active:** "Prevent Vanity Metrics" — Dashboard must show true ENCT health, not vanity counts
- **Action Items:** (Phase 5 planning document)
- **Timeline:** Phase 5 Weeks 1–2

### 3-2. P2-3 AI Auditors & Collaboration Channels _(Phase 4)_
- **Remediation Level:** Heavy (secondary agent implementation)
- **Prevention Active:** "Prevent Policy Corruption" — Audit agent must review bootstraps before acceptance
- **Action Items:** (Phase 4 planning document)
- **Timeline:** Phase 4 Weeks 2–3

### 3-3. P0-5 Orchestration Logic _(Phase 4)_
- **Remediation Level:** Medium (routing topology design)
- **Prevention Active:** "Prevent Quadratic Coordination Overhead" — Limit communication paths
- **Action Items:** (Phase 4 planning document)
- **Timeline:** Phase 4 Weeks 1–2

*Remaining Tier 3 features (P0-4, P0-6, P0-10, P1-4, P1-6, P3-1, P3-3, P3-4) have detailed planning documents for Phases 4–5. Reference HE-PRIORITIES.md for deferral rationale.*

---

## Execution Checklist — Phase 1 Design (Weeks 1–2)

### Week 1
- [ ] Initialize Git repository (P0-2) — 30 min
- [ ] Create ENCT-REFERENCE.md with axioms, primitives, Loop, indicators, verification (P1-1) — 2 hrs
- [ ] Create REQUIREMENTS.md with Phase 1–5 goals (P1-10) — 1 hr
- [ ] Create task hierarchy in project memory (P1-7) — 30 min
- [ ] Sync HE-SCOPE.md, HE-CLUES.md, HE-PRIORITIES.md to project repo — 30 min

**Week 1 Output:** Git repo + theory documentation fully encoded + requirements clear

### Week 2
- [ ] Create POLICY-INTAKE-TEMPLATE.md + wire into design (P1-11) — 1 hr
- [ ] Create AUTONOMY-GATES.md specification (P2-4) — 2 hrs
- [ ] Create ENCT-VERSION.md with semantic versioning (P0-8) — 1 hr
- [ ] Create POLICY-LEDGER.md template (P2-5) — 1 hr
- [ ] Complete Phase 1 design spec (10–15 pages + wireframes) — 8 hrs
- [ ] Update CLAUDE.md with Phase 1 execution rules — 1 hr

**Week 2 Output:** Phase 1 design spec complete; all requirements documented; Phase 2 can begin

---

## Post-Audit Recommendations

1. **Before Phase 2 begins:** User should review Phase 1 design spec and confirm all 8 Tier 1 items are complete.
2. **During Phase 2:** Tier 2 features should be completed in parallel with prototype development (training agent can wire them while bootstrap agent builds).
3. **During Phase 3:** Phase 3 testing will validate all verification gates; Tier 2 features should be finalized.
4. **Phase 4–5:** Tier 3 features roll in progressively; some can be deferred post-MVP if timeline is tight.

---

## Success Metrics

**Phase 1 Complete when:**
- All 8 Tier 1 features implemented and verified
- Phase 1 design spec passes linting and review
- All requirements in ledger with acceptance criteria
- Project team (user + Bootstrap Agent) agrees Phase 2 can begin

**Phase 2 Complete when:**
- Prototype builds without errors
- All 11 Tier 2 Early features in place
- Test suite passes with Compliance >95%, Homeostasis ≥0.8
- Phase 3 testing can execute 500+ scenarios

**Full ALM Complete when:**
- Phase 5 monitoring shows Compliance Rate >99%, Homeostasis ≥0.85
- All 30 harness features implemented or deferred with documented rationale
- Users can download, install, bootstrap policies, and run agent with zero custom engineering

---

## NEXT STEP: USER REVIEW & APPROVAL

This implementation plan is **ready for user review**. User should:

1. **Review Phase 1 action items** (1-1 through 1-8) and confirm feasibility / timeline
2. **Approve Tier 1 execution order** or propose adjustments
3. **Authorize Phase 1 Design work** to begin (bootstrap agent will create all Phase 1 deliverables)
4. **Optionally review Tier 2 details** for Phase 2 transparency

Once approved, the Bootstrap Agent will execute Phase 1 Design using this plan as the authoritative checklist.
