# Harness Engineering Gap Analysis — ENCT v1.3

**Audit Date:** 2026-04-05  
**Project:** ENCT v1.3 Agent Product (Greenfield)  
**Assessment Method:** 3-Step Chain (What to Do → Don't Do → Options) per feature

---

## Foundation (P0) — Can the agent execute safely?

### P0-1. Bash Sandboxes

**Area:** Foundation  
**Feature:** P0-1 Bash Sandboxes  
**Current State:** None — no isolated execution environment yet. Agent code will run within Claude Code harness but requires explicit sandbox declaration.  
**Prevention Active:** "Isolate Execution Environments" — Running agent logic directly on developer machines or without declared isolation risks contaminating local state.  
**Recommended Options:**
- **Action:** Provision safe, isolated, on-demand execution environments with language runtimes and test runners.
- **Tool:** Claude Code harness sandbox support (built-in)
- **Tool:** Docker containers for Phase 4 deployment isolation
- **Tier 1:** Declare all agent work happens within Claude Code sandbox (cannot run arbitrary commands on host machine).
- **Tier 2:** Add Phase 4 deployment as Docker-based SAS → MAS ready containers.

**Severity:** Critical  
**Remediation Level:** Light (declaration) + Heavy (Phase 4 deployment packaging)

---

### P0-2. Filesystem & Git Workspace

**Area:** Foundation  
**Feature:** P0-2 Filesystem & Git Workspace  
**Current State:** Repository exists but is empty. No Git initialization, no tracking, no worktrees.  
**Prevention Active:** "Prevent State and File Conflicts" — Normative constraint versioning, axiom updates, and bootstrap outcomes must be Git-tracked and rollback-able. Without Git, conflicting policy versions or failed bootstraps cannot be recovered.  
**Recommended Options:**
- **Action:** Initialize Git repository and establish the filesystem as the core collaboration surface.
- **Action:** Create structured directory layout: `/axioms/`, `/indicators/`, `/bootstrap-logs/`, `/ENCT-configs/`
- **Action:** Implement file locking for MAS readiness (concurrent agent branches).
- **Tool:** Git (version control) + per-agent worktrees (P0-2 Tier 2)
- **Tier 1:** Initialize `.git`, create directory structure, add initial ENCT configs to source control.
- **Tier 2:** Implement file locking for multi-agent concurrent updates.

**Severity:** Critical  
**Remediation Level:** Medium (setup) + Heavy (MAS locking)

---

### P0-3. Verification (Self & Collective)

**Area:** Foundation  
**Feature:** P0-3 Verification (Self & Collective)  
**Current State:** None — no test suites, no pre-completion verification gates, no tiered validation.  
**Prevention Active:** "Prevent Cascading Hallucinations" — Bootstrap pattern must not commit unsafe policies. Without verification gates (Tier 1 cache, Tier 2 delta, Tier 3 full), failed bootstraps corrupt downstream norms.  
**Recommended Options:**
- **Action:** Ground all ENCT Loop cycles in verification before task completion.
- **Action:** Implement tiered validation gates (Tier 1: cache-check, Tier 2: delta-check, Tier 3: full sandbox).
- **Action:** Build test suite for ENCT engine axioms, indicator calculations, normative constraint application.
- **Tool:** Test execution suites (Unit tests for axioms, integration tests for Loop cycles)
- **Tool:** Pre-completion checklists (§6.5 LLM-Assisted Bootstrap Pattern gating)
- **Tool:** Sandbox validators (Lyapunov-style homeostasis scoring ≥0.85)
- **Tier 1:** Create test suite validating axiom enforcement (Axiom 1, 2, 3, 4).
- **Tier 2:** Add pre-bootstrap verification gates with >0.7 confidence thresholds.

**Severity:** Critical  
**Remediation Level:** Medium (features + hooks)

---

### P0-4. Ralph Loops

**Area:** Foundation  
**Feature:** P0-4 Ralph Loops  
**Current State:** Not applicable in Phase 1 (Design). Agent work is within Claude Code harness which handles context resets.  
**Prevention Active:** N/A — Claude Code handles long-horizon task reinjection natively.  
**Recommended Options:**
- **Action:** When Phase 4 deployment moves to standalone binary/SaaS, implement prompt reinjection with state summaries for long-running policy bootstraps.
- **Tool:** Custom reinjection middleware (Phase 4+)
- **Tier 1 (Phase 4):** Add state checkpoint and reinjection logic for tasks >30k tokens.

**Severity:** Enhancement  
**Remediation Level:** Light (Phase 4 only)

---

### P0-5. Orchestration Logic

**Area:** Foundation  
**Feature:** P0-5 Orchestration Logic  
**Current State:** None — SAS-only for Phases 1–3. Phase 4 deployment will spawn audit agents; Phase 5 monitoring may use inspector agents.  
**Prevention Active:** "Prevent Quadratic Coordination Overhead" — When Phase 5 monitoring scales to multi-agent validation, must avoid over-communication. Must prevent Supervisor Bottlenecks (one audit agent cannot be the single gate).  
**Recommended Options:**
- **Action:** Define how audit agents (P2-3) and monitoring agents are spawned and how tasks are handed off.
- **Action:** Use Peer-to-Peer or Blackboard topology for multi-agent norm review (not Supervisor bottleneck).
- **Tool:** Agent topologies (Supervisor for bootstrap, Peer-to-Peer for audit review, Blackboard for monitoring)
- **Tier 1 (Phase 4):** Implement basic supervisor pattern for bootstrap → deployment handoff.
- **Tier 2 (Phase 5):** Upgrade to Peer-to-Peer audit review topology.

**Severity:** Important  
**Remediation Level:** Medium (Phase 4+)

---

### P0-6. Rippable Middleware

**Area:** Foundation  
**Feature:** P0-6 Rippable Middleware  
**Current State:** None — all features are core-required for ENCT. No "extraneous logic" to disable.  
**Prevention Active:** N/A — All harness features are essential; none are optional middleware.  
**Recommended Options:**
- **Action:** Design Phase 1 architecture so non-critical features (e.g., optional dashboard themes, audit transcript formatting) can be toggled via `.cursorrules` without breaking core ENCT engine.
- **Tier 1:** Ensure core ENCT Loop (§5) cannot be bypassed or disabled.

**Severity:** Enhancement  
**Remediation Level:** Light

---

### P0-7. Escalation Policies & Audit Trails

**Area:** Foundation  
**Feature:** P0-7 Escalation Policies & Audit Trails  
**Current State:** None — no automatic escalation, no immutable provenance bundles.  
**Prevention Active:** "Stuck agents" or norm violations must trigger escalation to humans (Phase 5 monitoring). Audit trails must be immutable (§9 verification approaches).  
**Recommended Options:**
- **Action:** Define escalation thresholds (e.g., if bootstrap Confidence < 0.5, escalate to human review).
- **Action:** Capture immutable provenance bundles for every norm change (who, what, when, lineage).
- **Tool:** Automated alerting (Phase 5 monitoring service)
- **Tool:** Immutable event logs (append-only, Git-backed)
- **Tier 1:** Define escalation policies in CLAUDE.md (bootstrap failures, axiom violations).
- **Tier 2:** Implement immutable provenance tracking in Phase 5 observability layer.

**Severity:** Important  
**Remediation Level:** Light (policies) + Medium (Phase 5 implementation)

---

### P0-8. Harness Versioning

**Area:** Foundation  
**Feature:** P0-8 Harness Versioning  
**Current State:** None — ENCT configurations, prompts, axioms not yet versioned.  
**Prevention Active:** "Prevent Axiom Drift" — Without versioning, updated axioms or normative constraints could silently break existing policies.  
**Recommended Options:**
- **Action:** Track all ENCT engine configs, axiom definitions, indicator formulas, and verification approaches in Git.
- **Action:** Use semantic versioning for axiom sets (v1.0.0, v1.0.1, etc.) with breaking-change annotations.
- **Tool:** Git tags and CHANGELOG.md
- **Tool:** Version pinning in bootstrap logs (which axiom v× was used for policy X)
- **Tier 1:** Create ENCT-VERSION.md documenting axioms, indicators, verification methods with Git history.
- **Tier 2:** Implement rollback procedures for axiom breaking changes.

**Severity:** Important  
**Remediation Level:** Light

---

### P0-9. Smart Command Wrappers

**Area:** Foundation  
**Feature:** P0-9 Smart Command Wrappers  
**Current State:** Partial — Claude Code provides high-level tools (TaskCreate, Read, Edit, Bash). ENCT-specific wrappers needed for bootstrap, verify, and rollback.  
**Prevention Active:** "Prevent Manual Errors" — Common tasks (bootstrap policy, verify axiom compliance, rollback norm version) must be wrapped so agents cannot accidentally misconfigure them.  
**Recommended Options:**
- **Action:** Create ENCT-specific smart wrappers: `enct-bootstrap`, `enct-verify`, `enct-rollback`.
- **Tool:** Bash functions or Python CLI with built-in validation.
- **Tier 1:** Create wrapper scripts in `/scripts/` for bootstrap, verify, rollback.
- **Tier 2:** Wire wrappers into .cursorrules for automatic discovery.

**Severity:** Important  
**Remediation Level:** Light

---

### P0-10. Inter-Agent Communication

**Area:** Foundation  
**Feature:** P0-10 Inter-Agent Communication  
**Current State:** None — SAS for Phases 1–3. Audit agents (Phase 4) and monitoring agents (Phase 5) will need communication.  
**Prevention Active:** "Prevent Silent Failures" — When audit agent reviews bootstrap, must communicate pass/fail synchronously (not via logs alone).  
**Recommended Options:**
- **Action:** Define message format for audit feedback (pass/fail + violations list + remediation suggestions).
- **Action:** Implement blackboard or shared file system for inter-agent sync (Phase 4+).
- **Tool:** Shared task list (P1-7) + provenance bundles (JSON files)
- **Tier 1:** Design message format in AGENTS.md.
- **Tier 2 (Phase 4):** Implement file-based blackboard for audit → bootstrap handoff.

**Severity:** Enhancement  
**Remediation Level:** Light (design) + Medium (Phase 4)

---

## Pillar 1 (P1) — Does the agent know what it needs to know?

### P1-1. Repository as Truth

**Area:** Pillar 1  
**Feature:** P1-1 Repository as Truth  
**Current State:** None — ENCT axioms, indicators, verification approaches not yet encoded in repo.  
**Prevention Active:** "Prevent Human-Only Documentation" — Without axioms in the repo, agent is blind to ENCT's normative control rules. If axioms live only in human heads or external design docs, agent cannot reliably apply them.  
**Recommended Options:**
- **Action:** Encode all ENCT primitives, axioms (Axioms 1–4), the exact 5-phase Loop definition, indicators, and verification approaches directly into the codebase.
- **Action:** Create `ENCT-REFERENCE.md` with full axiom text, definitions, and examples.
- **Action:** Create Failure Ledger documenting past axiom violations and their consequences.
- **Tool:** ENCT-REFERENCE.md, AXIOMS.md, INDICATORS.md, VERIFICATION.md in root
- **Tier 1:** Write ENCT-REFERENCE.md documenting primitives, 5-phase Loop, axioms, indicators, verification.
- **Tier 2:** Create Failure Ledger linking past incidents to axiom improvements.

**Severity:** Critical  
**Remediation Level:** Light

---

### P1-2. Context Compaction & Memory Management

**Area:** Pillar 1  
**Feature:** P1-2 Context Compaction & Memory Management  
**Current State:** None — Long bootstrap tasks or policy reviews will eventually exceed context limits without compression.  
**Prevention Active:** "Prevent Context Rot" — As bootstrap logs, audit transcripts, and indicator traces accumulate, context window fills. Must actively offload to long-term memory.  
**Recommended Options:**
- **Action:** Summarize bootstrap outcomes after each phase (Design, Train, Test, Deploy, Monitor).
- **Action:** Archive full bootstrap transcripts to `/bootstrap-logs/` and pass only summaries into next context.
- **Tool:** Conversation summarization (Phase 5+)
- **Tool:** Vector database for searching past bootstrap outcomes (Phase 5+)
- **Tier 1:** Create bootstrap summary templates in Phase 4.
- **Tier 2:** Implement long-term memory for policy search (Phase 5).

**Severity:** Important  
**Remediation Level:** Medium (Phase 4+)

---

### P1-3. Tool Offloading

**Area:** Pillar 1  
**Feature:** P1-3 Tool Offloading  
**Current State:** Partial — Claude Code handles tool outputs natively. But Phase 4 standalone deployment must offload large test outputs.  
**Prevention Active:** "Prevent Context Rot" — Large test runs (500+ scenario verification) generate huge logs. Must save full results to disk and keep only head/tail tokens.  
**Recommended Options:**
- **Action:** Save full ENCT Loop test outputs to `/test-results/` with only summary stats in context.
- **Action:** Save bootstrap transcripts, provenance bundles, and audit reports to filesystem.
- **Tool:** File-based offloading (Tier 1) + vector database (Tier 2, Phase 5)
- **Tier 1:** Wire test runners to save full output to disk, summarize for agent.
- **Tier 2:** Index results for later retrieval.

**Severity:** Important  
**Remediation Level:** Medium

---

### P1-4. Progressive Skills

**Area:** Pillar 1  
**Feature:** P1-4 Progressive Skills  
**Current State:** Partial — Skill loading is handled by Claude Code. But ENCT engine features (bootstrap, verify, monitor) should be role-specific.  
**Prevention Active:** "Prevent Context Rot" — Loading all features at startup (bootstrap + testing + monitoring + auditing) overwhelms context. Must load progressively.  
**Recommended Options:**
- **Action:** Organize ENCT features by role: bootstrap-agent loads §6.5 only; test-agent loads §9 verification; monitor-agent loads §8 indicators.
- **Tool:** Role-based skill modules in `.cursorrules`
- **Tier 1:** Define roles in AGENTS.md (bootstrap-agent, verifier-agent, monitor-agent).
- **Tier 2:** Create conditional skill loading based on task assignment.

**Severity:** Enhancement  
**Remediation Level:** Medium

---

### P1-5. Observability / Dashboards

**Area:** Pillar 1  
**Feature:** P1-5 Observability / Dashboards  
**Current State:** None — No real-time ENCT Loop metrics, Compliance Rate, Homeostasis score, etc.  
**Prevention Active:** "Prevent Vanity Metrics" — Without observability, agent optimizes for wrong targets (policy count, bootstrap speed) instead of Compliance Rate, Homeostasis, Adaptation Resilience.  
**Recommended Options:**
- **Action:** Create live dashboards streaming all quantitative indicators (§8): Compliance Rate, Homeostasis score, Adaptation Resilience, Provenance Overhead, Traceability Coverage.
- **Action:** Expose ENCT Loop cycle logs and metrics in real-time.
- **Tool:** Time-series database (InfluxDB, Prometheus) for Phase 5 monitoring
- **Tool:** Dashboard UI (Grafana, custom) for user-facing monitoring (Phase 5)
- **Tier 1 (Phase 5):** Create monitoring service capturing all §8 indicators.
- **Tier 2 (Phase 5):** Build live dashboards in Phase 4 UI.

**Severity:** Critical  
**Remediation Level:** Heavy (Phase 5)

---

### P1-6. Web Search & MCP Integration

**Area:** Pillar 1  
**Feature:** P1-6 Web Search & MCP Integration  
**Current State:** Partial — Claude Code supports Web Search natively. Phase 5 monitoring may need external integration (Grafana, alerting APIs).  
**Prevention Active:** N/A — ENCT v1.3 is self-contained; external data (web, APIs) optional for later integration.  
**Recommended Options:**
- **Action:** For Phase 5, integrate with alerting APIs (PagerDuty, Slack) to escalate axiom violations.
- **Tool:** MCP integrations (Phase 5+)
- **Tier 2 (Phase 5):** Wire alerts to external channels.

**Severity:** Enhancement  
**Remediation Level:** Light

---

### P1-7. Planning, Task Lists & Blackboards

**Area:** Pillar 1  
**Feature:** P1-7 Planning, Task Lists & Blackboards  
**Current State:** Partial — Claude Code TaskCreate/TaskList available. But ENCT-specific task orchestration (bootstrap phases, verification batches) not yet structured.  
**Prevention Active:** "Prevent Untracked Work" — Bootstrap phases (Sense, Validate, Execute, Assess, Re-enact) must be tracked as explicit tasks with dependencies.  
**Recommended Options:**
- **Action:** Use Claude Code tasks to track each ALM phase and ENCT Loop cycle.
- **Action:** Create task templates for bootstrap (design, train, test, deploy, monitor).
- **Tool:** TaskCreate/TaskUpdate for ENCT-specific phases
- **Tool:** Blackboard for audit review feedback (Phase 4+)
- **Tier 1:** Define task hierarchy for ALM Phases 1–5 in project memory.
- **Tier 2:** Implement blackboard format for audit agent feedback (Phase 4).

**Severity:** Important  
**Remediation Level:** Light

---

### P1-8. Context Anchoring

**Area:** Pillar 1  
**Feature:** P1-8 Context Anchoring  
**Current State:** Partial — Memory system in place. But critical ENCT decisions (axiom updates, bootstrap policy acceptance, rollback decisions) must be permanently logged.  
**Prevention Active:** "Prevent Lost Context" — Without anchoring decisions to persistent memory, critical choices (why axiom v1.0.1 was rejected, which bootstrap policy triggered escalation) are lost between sessions.  
**Recommended Options:**
- **Action:** Create decision logs for all critical ENCT choices: axiom updates, policy acceptances, escalations.
- **Action:** Use memory system to record "Why" behind each decision.
- **Tool:** Memory files + decision logs in `/enct-decisions/`
- **Tier 1:** Establish pattern for decision logging in CLAUDE.md.
- **Tier 2:** Build automated decision capture into Phase 5 monitoring.

**Severity:** Important  
**Remediation Level:** Light

---

### P1-9. Branch-Based Memory

**Area:** Pillar 1  
**Feature:** P1-9 Branch-Based Memory  
**Current State:** Planned (P0-2 Git workspace) — Each bootstrap phase creates a Git branch with memory of progress.  
**Prevention Active:** "Prevent Lost Work" — Long bootstrap processes (Design → Deploy phases) need intermediate checkpoints so work survives context resets.  
**Recommended Options:**
- **Action:** Create per-phase branches: `enct-design`, `enct-train`, `enct-test`, `enct-deploy`, `enct-monitor`.
- **Action:** Commit memory snapshots after each phase with "Progress: X% complete" messages.
- **Tool:** Git branches + auto-commit memory snapshots
- **Tier 1:** Design branch strategy in CLAUDE.md.
- **Tier 2:** Automate memory snapshots via CI hooks.

**Severity:** Important  
**Remediation Level:** Medium

---

### P1-10. Requirements Ledger

**Area:** Pillar 1  
**Feature:** P1-10 Requirements Ledger  
**Current State:** Exists as ALM framework document (HE-SCOPE.md). But functional requirements for Phase 1 Design need explicit ledger.  
**Prevention Active:** "Prevent Implicit Requirements" — Bootstrap design, axiom definitions, indicator calculations all need explicit requirements (user personas, success criteria, architectural constraints).  
**Recommended Options:**
- **Action:** Create REQUIREMENTS.md documenting all user stories, acceptance criteria, and design constraints for each ALM phase.
- **Action:** For Phase 1: define personas (AI researcher, policy designer, auditor), use cases, success criteria.
- **Tool:** Markdown requirements ledger with phase breakdown
- **Tier 1:** Create REQUIREMENTS.md for Phase 1 Design work.
- **Tier 2:** Extend for Phases 2–5.

**Severity:** Important  
**Remediation Level:** Light

---

### P1-11. Socratic Questioning

**Area:** Pillar 1  
**Feature:** P1-11 Socratic Questioning  
**Current State:** Partial — Used at project intake (ALM pathway confirmation at start of this conversation). Needs formalization for bootstrap intake.  
**Prevention Active:** "Prevent Unexamined Assumptions" — User policies fed to bootstrap must be questioned before validation. Otherwise, agent accepts malformed or contradictory norms.  
**Recommended Options:**
- **Action:** Define Socratic template for questioning bootstrap policy submissions (What does this norm enforce? What behavior should it prevent? What are failure cases?).
- **Action:** Wire template into Phase 4 bootstrap UI.
- **Tool:** Structured questioning prompts in CLAUDE.md
- **Tier 1:** Create Socratic template for policy validation in Phase 4 bootstrap interface.
- **Tier 2:** Automate via LLM-Assisted Bootstrap Pattern validation gate (§6.5).

**Severity:** Important  
**Remediation Level:** Light

---

## Pillar 2 (P2) — Is the agent mechanically prevented from bad output?

### P2-1. Automated Linters

**Area:** Pillar 2  
**Feature:** P2-1 Automated Linters  
**Current State:** None — No ENCT-specific linters yet. But Phase 1 design outputs (architecture blueprint, wireframes, specs) need validation.  
**Prevention Active:** "Prevent Malformed Specs" — Design outputs must follow strict format (sections, wireframe dimensions, schema definitions). Without linters, Phase 1 spec may be incomplete.  
**Recommended Options:**
- **Action:** Create ENCT-specific linters for spec validation: Section presence check, YAML schema validation, axiom reference completeness.
- **Action:** Wire linters into Phase 1 CI as pre-commit hooks + CI checks.
- **Tool:** Custom Python linters or JSON/YAML schema validators
- **Tier 1:** Create Phase 1 spec template with validation schema.
- **Tier 2 (Phase 2):** Add axiom syntax validation (Tier 1 cache format, Tier 2 delta format, Tier 3 full validation).

**Severity:** Important  
**Remediation Level:** Medium

---

### P2-2. Dependency Enforcement

**Area:** Pillar 2  
**Feature:** P2-2 Dependency Enforcement  
**Current State:** Partial — ENCT reference docs (ENCT-REFERENCE.md) are the source of truth. But Phase 4 code must not contradict them.  
**Prevention Active:** "Prevent Architecture Violations" — Phase 2 prototype code or Phase 4 deployment must implement ENCT exactly as defined. No deviations allowed.  
**Recommended Options:**
- **Action:** Create structural tests validating that code implements all axioms, all indicators, full 5-phase Loop.
- **Action:** CI check: count of axiom-enforcement code paths must match ENCT-REFERENCE.md.
- **Tool:** Custom linters scanning code for axiom implementations
- **Tier 1 (Phase 2):** Create checklist: all 4 axioms → code paths documented.
- **Tier 2 (Phase 2+):** Automated count validation in CI.

**Severity:** Important  
**Remediation Level:** Medium

---

### P2-3. AI Auditors & Collaboration Channels

**Area:** Pillar 2  
**Feature:** P2-3 AI Auditors & Collaboration Channels  
**Current State:** None — Planned for Phase 4 (second agent reviews bootstrap outcomes). Not needed for Phases 1–3.  
**Prevention Active:** "Prevent Policy Corruption" — Unsafe bootstraps could corrupt downstream norms. Secondary agent must audit before acceptance.  
**Recommended Options:**
- **Action:** Deploy second LLM-based agent in Phase 4 to review bootstrap outputs (policy text, confidence score, axiom compliance).
- **Action:** Audit agent compares policy against ENCT axioms and existing norms.
- **Action:** Use Peer-to-Peer topology (both audit and bootstrap agents vote on acceptance).
- **Tool:** Claude Agent SDK for secondary audit agent (Phase 4)
- **Tool:** Collaboration channel: shared task lists + provenance bundles
- **Tier 1 (Phase 4):** Deploy audit agent with checklist: axiom compliance, confidence >0.7, no conflicts with existing policies.
- **Tier 2 (Phase 5):** Add competitive debate mode (audit agent challenges bootstrap rationale).

**Severity:** Critical  
**Remediation Level:** Heavy (Phase 4)

---

### P2-4. Bounded Autonomy & Access Control

**Area:** Pillar 2  
**Feature:** P2-4 Bounded Autonomy & Access Control  
**Current State:** None — No access controls on bootstrap, no rate limits on norm updates.  
**Prevention Active:** "Prevent Malicious Policies" — Agent must not bootstrap policies that exceed predefined scope (e.g., policies that modify non-target domains, policies that disable axioms).  
**Recommended Options:**
- **Action:** Define Autonomy Boundaries: agent can bootstrap policies within predefined domain only (e.g., "user login flow").
- **Action:** Implement rate limits: max N bootstraps/hour, max M norms per session.
- **Action:** Block policies that contradict Axiom 1 (foundational rules cannot change).
- **Tool:** Whitelist/blacklist in bootstrap validator
- **Tool:** Rate-limiting middleware in Phase 4 deployment
- **Tier 1:** Define domain boundaries in Autonomy Gates spec (Phase 1 Design).
- **Tier 2 (Phase 4):** Implement enforcement in bootstrap UI + backend.

**Severity:** Critical  
**Remediation Level:** Medium

---

### P2-5. Upstream Intake Gate

**Area:** Pillar 2  
**Feature:** P2-5 Upstream Intake Gate  
**Current State:** Partial — User policies will be submitted in Phase 4 (Deploy), but no validation gate exists yet.  
**Prevention Active:** "Prevent Unregistered Work" — Bootstrap policies must be pre-registered in REQUIREMENTS.md or a policy ledger before processing.  
**Recommended Options:**
- **Action:** Require users to fill a policy submission form (name, domain, intent, expected behavior).
- **Action:** Sync form submission to a Policy Ledger (like Requirements Ledger for policies).
- **Action:** Bootstrap gate: check ledger entry exists before proceeding.
- **Tool:** Phase 4 UI form + POLICY-LEDGER.md
- **Tier 1:** Create policy submission form template (Phase 4).
- **Tier 2:** Implement ledger check gate in bootstrap workflow.

**Severity:** Important  
**Remediation Level:** Medium

---

## Pillar 3 (P3) — Does the system clean up after itself?

### P3-1. Scheduled Cleanups

**Area:** Pillar 3  
**Feature:** P3-1 Scheduled Cleanups  
**Current State:** None — No scheduled agents running garbage collection. Needed for Phase 5 monitoring.  
**Prevention Active:** "Prevent Codebase Entropy" — Stale bootstrap logs, old test artifacts, abandoned norm versions accumulate. Must sweep automatically.  
**Recommended Options:**
- **Action:** Create weekly cleanup sweep (via cron or CI schedule) to remove logs >30 days old, test results for reverted policies, unused axiom versions.
- **Action:** Generate cleanup report listing dead code/configs found.
- **Tool:** Cron job or GitHub Actions schedule
- **Tool:** Cleanup agent that reports findings (Phase 5+)
- **Tier 1 (Phase 5):** Schedule weekly sweep of `/bootstrap-logs/` and `/test-results/`.
- **Tier 2 (Phase 5):** Deploy cleanup agent that also reconciles conflicting norm versions.

**Severity:** Enhancement  
**Remediation Level:** Light

---

### P3-2. Documentation Sync

**Area:** Pillar 3  
**Feature:** P3-2 Documentation Sync  
**Current State:** None — ENCT axioms and indicators must stay synced with code (Tier 2 axiom updates must update ENCT-REFERENCE.md).  
**Prevention Active:** "Prevent Documentation Disconnects" — If code implements Axiom 2 but ENCT-REFERENCE.md still lists old axiom text, user is confused.  
**Recommended Options:**
- **Action:** CI check: whenever axiom code changes, verify ENCT-REFERENCE.md updated in same commit.
- **Action:** Create documentation agent (Phase 5) that validates indicator formula docs match code calculations.
- **Tool:** Pre-commit hook: block commits that change code but not matching docs.
- **Tier 1:** Add doc-sync requirement to CLAUDE.md.
- **Tier 2 (Phase 5):** Deploy documentation consistency agent.

**Severity:** Important  
**Remediation Level:** Medium

---

### P3-3. Pattern Auditing

**Area:** Pillar 3  
**Feature:** P3-3 Pattern Auditing  
**Current State:** None — No dead code or pattern deviation detection yet (Phase 2+).  
**Prevention Active:** "Prevent Codebase Entropy" — As Phase 2 training and Phase 4 deployment code grows, dead code paths and circular dependencies will accumulate.  
**Recommended Options:**
- **Action:** Create pattern linter: flag unused axiom enforcement code, circular norm dependencies, unreachable verification paths.
- **Action:** Wire into CI as optional warning (Tier 2).
- **Tool:** Static analysis tools (dependency-cruiser, dead-code-finder)
- **Tier 2 (Phase 2+):** Create pattern audit report monthly.

**Severity:** Enhancement  
**Remediation Level:** Light

---

### P3-4. Consolidation Loop

**Area:** Pillar 3  
**Feature:** P3-4 Consolidation Loop  
**Current State:** None — Meta-docs (ENCT-REFERENCE.md, axiom versions, indicator definitions, verification methods) must stay synced automatically.  
**Prevention Active:** "Prevent Meta-Doc Drift" — ENCT-REFERENCE.md, AXIOMS.md, INDICATORS.md, VERIFICATION.md are the source of truth. If they drift from code, agent is confused.  
**Recommended Options:**
- **Action:** Create consolidation agent (Phase 5) that runs weekly to reconcile meta-docs against code.
- **Action:** Generate "Meta-Doc Drift Report" listing inconsistencies.
- **Action:** Auto-fix simple inconsistencies (axiom count mismatch, indicator formula difference).
- **Tool:** Consolidation agent + automated drift detection
- **Tier 1:** Create drift detection script checking axiom counts, indicator counts against code.
- **Tier 2 (Phase 5):** Deploy consolidation agent to auto-fix drifts.

**Severity:** Important  
**Remediation Level:** Medium

---

## Gap Summary Table

| Feature ID | Name | Current State | Severity | Remediation Level | Phase Dependency |
| --- | --- | --- | --- | --- | --- |
| P0-1 | Bash Sandboxes | Light (declared) | Critical | Light + Heavy | Phase 1 (design), Phase 4 (deploy) |
| P0-2 | Filesystem & Git | Setup needed | Critical | Medium + Heavy | Phase 1 (immediate) |
| P0-3 | Verification | None | Critical | Medium | Phase 2 (train) |
| P0-4 | Ralph Loops | N/A (Claude Code native) | Enhancement | Light | Phase 4 (phase 4+) |
| P0-5 | Orchestration | None | Important | Medium | Phase 4 (deploy) |
| P0-6 | Rippable Middleware | N/A (all core) | Enhancement | Light | Phase 1 (design) |
| P0-7 | Escalation & Audit | None | Important | Light + Medium | Phase 1 + Phase 5 |
| P0-8 | Harness Versioning | None | Important | Light | Phase 1 (immediate) |
| P0-9 | Smart Wrappers | Partial | Important | Light | Phase 1 (design) |
| P0-10 | Inter-Agent Comm | None | Enhancement | Light + Medium | Phase 4 (deploy) |
| P1-1 | Repository as Truth | None | Critical | Light | Phase 1 (immediate) |
| P1-2 | Context Compaction | None | Important | Medium | Phase 4+ |
| P1-3 | Tool Offloading | Partial | Important | Medium | Phase 2+ |
| P1-4 | Progressive Skills | Partial | Enhancement | Medium | Phase 2+ |
| P1-5 | Observability | None | Critical | Heavy | Phase 5 (monitor) |
| P1-6 | Web Search & MCP | Partial | Enhancement | Light | Phase 5+ |
| P1-7 | Planning & Tasks | Partial | Important | Light | Phase 1 (design) |
| P1-8 | Context Anchoring | Partial | Important | Light | Phase 1 (design) |
| P1-9 | Branch Memory | Planned | Important | Medium | Phase 2+ |
| P1-10 | Requirements Ledger | Partial | Important | Light | Phase 1 (design) |
| P1-11 | Socratic Questioning | Partial | Important | Light | Phase 1 (design) |
| P2-1 | Automated Linters | None | Important | Medium | Phase 1+ |
| P2-2 | Dependency Enforcement | Partial | Important | Medium | Phase 2+ |
| P2-3 | AI Auditors | None | Critical | Heavy | Phase 4 (deploy) |
| P2-4 | Bounded Autonomy | None | Critical | Medium | Phase 1 (design) + Phase 4 |
| P2-5 | Upstream Intake | None | Important | Medium | Phase 4 (deploy) |
| P3-1 | Scheduled Cleanups | None | Enhancement | Light | Phase 5+ |
| P3-2 | Documentation Sync | None | Important | Medium | Phase 1+ |
| P3-3 | Pattern Auditing | None | Enhancement | Light | Phase 2+ |
| P3-4 | Consolidation Loop | None | Important | Medium | Phase 5 |

---

## Next Step

This gap analysis (HE-CLUES) maps all 30 features to the greenfield ENCT project. Proceed to **Phase 2: Gap Scoring** to prioritize by impact, then **Phase 3: Implementation Planning** to sequence execution across ALM Phases 1–5.
