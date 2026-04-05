# Gap Prioritization & Tiers — ENCT v1.3 Agent Product

**Audit Date:** 2026-04-05  
**Methodology:** 6-Dimension Evaluation + Impact Weight + Cascade Analysis  
**Result:** 30 features sorted into Tier 1 (Critical), Tier 2 (Important), Tier 3 (Enhancement)

---

## Scoring Methodology

Each feature scored 0–5 across 6 dimensions:
1. **Implementation Maturity** — How fully built?
2. **Operational Effectiveness** — Does it work in practice?
3. **Risk Exposure** — What breaks if absent?
4. **Cost-Efficiency** — Is investment proportional?
5. **Scalability (SAS→MAS)** — Will it survive multi-agent?
6. **Human Role Evolution** — Does it shift from code to design?

**Priority Score Formula:**  
`(5 - Composite Score) × Impact Weight × Cascade Length`

- **Composite Score:** Average across 6 dimensions
- **Impact Weight:** Count of downstream dependent features (from `dependencies.md`)
- **Cascade Length:** 1 (isolated), 2 (moderate), 3 (systemic failure)

---

## Tier 1 (Immediate Execution) — Critical Path for Phase 1

These features MUST be in place before Phase 1 Design completes and Phase 2 Training begins. Without them, agent cannot reliably build or verify ENCT engine.

### 1-1. P0-2 Filesystem & Git Workspace
- **Composite Score:** 0/5 (absent)
- **Impact Weight:** 5 (downstream: P1-8, P1-9, P1-10, P3-2, P3-4)
- **Cascade Length:** 3 (all versioning, memory, documentation fails without Git)
- **Priority Score:** (5 - 0) × 5 × 3 = **75** ← Highest priority
- **Rationale:** Without Git, ENCT normative constraint versioning is impossible. Foundation for all upstream work.
- **Target:** Week 1 of Phase 1

### 1-2. P1-1 Repository as Truth
- **Composite Score:** 0/5 (absent)
- **Impact Weight:** 3 (downstream: P2-2, P2-3, P1-8)
- **Cascade Length:** 3 (agent cannot operate without access to axioms)
- **Priority Score:** (5 - 0) × 3 × 3 = **45**
- **Rationale:** All ENCT axioms, indicators, verification approaches must be in code. If they're only in human design docs, agent is blind.
- **Target:** Week 1 of Phase 1 (parallel with P0-2)

### 1-3. P1-10 Requirements Ledger
- **Composite Score:** 1/5 (partial — ALM framework exists, but Phase 1 design requirements missing)
- **Impact Weight:** 2 (downstream: P2-5, P1-7)
- **Cascade Length:** 2 (blocks intake gate and task planning)
- **Priority Score:** (5 - 1) × 2 × 2 = **16**
- **Rationale:** Phase 1 deliverables (spec, wireframes, architecture) need explicit acceptance criteria. Otherwise, design is unfinished.
- **Target:** Week 1–2 of Phase 1

### 1-4. P1-11 Socratic Questioning
- **Composite Score:** 1/5 (partial — used at project intake, needs formalization)
- **Impact Weight:** 3 (downstream: P1-10, P1-8, P1-7)
- **Cascade Length:** 2 (affects requirements clarity and decision quality)
- **Priority Score:** (5 - 1) × 3 × 2 = **24**
- **Rationale:** User policies submitted in Phase 4 must be questioned before bootstrap. Template needed now.
- **Target:** Week 1–2 of Phase 1

### 1-5. P2-4 Bounded Autonomy & Access Control
- **Composite Score:** 0/5 (absent)
- **Impact Weight:** 1 (downstream: P0-7)
- **Cascade Length:** 3 (if unbounded, agent can bootstrap unsafe policies)
- **Priority Score:** (5 - 0) × 1 × 3 = **15**
- **Rationale:** Autonomy Gates spec (Phase 1 Design deliverable) must define domain boundaries, rate limits, axiom immutability.
- **Target:** Week 2 of Phase 1 (design phase completion)

### 1-6. P1-7 Planning, Task Lists & Blackboards
- **Composite Score:** 2/5 (partial — Claude Code tasks available, but ENCT-specific orchestration missing)
- **Impact Weight:** 2 (downstream: P0-4, P1-4)
- **Cascade Length:** 2 (affects all phase transitions)
- **Priority Score:** (5 - 2) × 2 × 2 = **12**
- **Rationale:** ALM phases must be tracked as explicit tasks with dependencies. Otherwise, phases bleed together.
- **Target:** Week 1 of Phase 1

### 1-7. P0-8 Harness Versioning
- **Composite Score:** 0/5 (absent)
- **Impact Weight:** 1 (foundational, not many direct dependents in checklist)
- **Cascade Length:** 2 (breaks rollback and axiom management)
- **Priority Score:** (5 - 0) × 1 × 2 = **10**
- **Rationale:** Axioms, indicators, verification methods must have versions (v1.0.0, v1.0.1) with Git tags and CHANGELOG.
- **Target:** Week 2 of Phase 1

### 1-8. P2-5 Upstream Intake Gate
- **Composite Score:** 0/5 (absent, but design exists in policy-submission form)
- **Impact Weight:** 1 (leaf constraint)
- **Cascade Length:** 2 (blocks unsafe policies from entering system)
- **Priority Score:** (5 - 0) × 1 × 2 = **10**
- **Rationale:** User policies must be pre-registered in ledger before bootstrap. Gate prevents untracked work.
- **Target:** Phase 4 UI design (but needs specification now)

**Tier 1 Sub-total:** 8 features  
**Tier 1 Timeline:** Weeks 1–2 of Phase 1 Design. All must complete before Phase 2 Training begins.

---

## Tier 2 (Mid-term Execution) — Phase 2–3 Support

These features are important for Phases 2–3 but can be iterated post-Phase 1. Agent can work without them, but with reduced safety and clarity.

### 2-1. P0-3 Verification (Self & Collective)
- **Composite Score:** 0/5 (absent)
- **Impact Weight:** 2 (downstream: P2-1, P2-2)
- **Cascade Length:** 3 (all constraint enforcement depends on verification)
- **Priority Score:** (5 - 0) × 2 × 3 = **30** ← Within Tier 2, highest priority
- **Rationale:** Before Phase 2 prototype can be tested, tiered validation gates (Tier 1/2/3) must exist. Otherwise, Phase 3 testing is impossible.
- **Target:** Week 1 of Phase 2

### 2-2. P0-7 Escalation Policies & Audit Trails
- **Composite Score:** 0/5 (absent)
- **Impact Weight:** 1
- **Cascade Length:** 2 (affects human trust in agent)
- **Priority Score:** (5 - 0) × 1 × 2 = **10**
- **Rationale:** Define escalation thresholds (bootstrap confidence <0.5, axiom violations). Audit trails are immutable (JSON provenance).
- **Target:** Week 2 of Phase 1 (complete by Phase 2 start)

### 2-3. P0-9 Smart Command Wrappers
- **Composite Score:** 1/5 (partial — Claude Code tools exist, ENCT-specific wrappers missing)
- **Impact Weight:** 2 (downstream: P0-3, P1-9)
- **Cascade Length:** 1 (localized to command execution)
- **Priority Score:** (5 - 1) × 2 × 1 = **8**
- **Rationale:** Create `enct-bootstrap`, `enct-verify`, `enct-rollback` CLI wrappers so agent cannot misconfigure bootstraps.
- **Target:** Week 1 of Phase 2

### 2-4. P0-5 Orchestration Logic
- **Composite Score:** 0/5 (absent for MAS, not needed for Phase 1–3 SAS)
- **Impact Weight:** 2 (downstream: P2-3, P0-6)
- **Cascade Length:** 2 (becomes critical in Phase 4 with audit agents)
- **Priority Score:** (5 - 0) × 2 × 2 = **20** ← Phase 4 blocker
- **Rationale:** Audit agents (Phase 4) need routing topology (Supervisor for bootstrap, Peer-to-Peer for review).
- **Target:** Week 1–2 of Phase 4 Design

### 2-5. P1-2 Context Compaction & Memory Management
- **Composite Score:** 0/5 (absent for Phases 1–3, critical for Phase 4+)
- **Impact Weight:** 2 (foundational for context management)
- **Cascade Length:** 2 (affects all long-running tasks)
- **Priority Score:** (5 - 0) × 2 × 2 = **20**
- **Rationale:** Bootstrap logs and test transcripts will accumulate. Must summarize and offload to disk.
- **Target:** Week 2 of Phase 4

### 2-6. P1-3 Tool Offloading
- **Composite Score:** 2/5 (partial — Claude Code handles outputs, Phase 4 deployment must offload)
- **Impact Weight:** 1
- **Cascade Length:** 2 (affects context window efficiency)
- **Priority Score:** (5 - 2) × 1 × 2 = **6**
- **Rationale:** Phase 3 test runs (500+ scenarios) will generate huge logs. Must save to disk, summarize for agent.
- **Target:** Week 2 of Phase 2

### 2-7. P1-8 Context Anchoring
- **Composite Score:** 1/5 (partial — memory system exists, but ENCT decision logs missing)
- **Impact Weight:** 1
- **Cascade Length:** 2 (affects knowledge retention across sessions)
- **Priority Score:** (5 - 1) × 1 × 2 = **8**
- **Rationale:** Critical decisions (axiom updates, bootstrap escalations, rollbacks) must be logged to persistent memory.
- **Target:** Week 2 of Phase 1 (integrate with memory system)

### 2-8. P1-9 Branch-Based Memory
- **Composite Score:** 0/5 (absent, but Git workspace foundation in place)
- **Impact Weight:** 1
- **Cascade Length:** 2 (affects recovery from context resets)
- **Priority Score:** (5 - 0) × 1 × 2 = **10**
- **Rationale:** Each ALM phase creates branch with progress checkpoints. Survives context resets and long tasks.
- **Target:** Week 1–2 of Phase 2

### 2-9. P2-1 Automated Linters
- **Composite Score:** 0/5 (absent)
- **Impact Weight:** 1 (downstream: P3-3)
- **Cascade Length:** 2 (affects design output quality)
- **Priority Score:** (5 - 0) × 1 × 2 = **10**
- **Rationale:** Phase 1 spec, wireframes, axiom definitions must validate against schema. Prevent malformed outputs.
- **Target:** Week 2 of Phase 1

### 2-10. P2-2 Dependency Enforcement
- **Composite Score:** 0/5 (absent for code, partial for docs)
- **Impact Weight:** 0 (no explicit dependents in checklist)
- **Cascade Length:** 2 (violations break architecture)
- **Priority Score:** (5 - 0) × 1 × 2 = **10** ← Assume Impact Weight 1
- **Rationale:** Code must implement all axioms, all indicators, full 5-phase Loop (from P1-1 Repository as Truth).
- **Target:** Week 1 of Phase 2

### 2-11. P3-2 Documentation Sync
- **Composite Score:** 0/5 (absent)
- **Impact Weight:** 1
- **Cascade Length:** 2 (affects knowledge consistency)
- **Priority Score:** (5 - 0) × 1 × 2 = **10**
- **Rationale:** Whenever axiom code changes, ENCT-REFERENCE.md must update in same commit. Prevent doc drift.
- **Target:** Week 1 of Phase 2 (wire into CI)

**Tier 2 Sub-total:** 11 features  
**Tier 2 Timeline:** Phases 2–3 (Weeks 3–12). Can overlap Phase 1 late weeks. All should complete before Phase 4 begins.

---

## Tier 3 (Long-term Backlog) — Phase 4–5 & Enhancement

These features are nice-to-have or Phase 4–5 specific. Can be deferred without blocking critical path.

### 3-1. P1-5 Observability / Dashboards
- **Composite Score:** 0/5 (absent, but critical for Phase 5)
- **Impact Weight:** 0 (depends on other features, not a dependency source)
- **Cascade Length:** 3 (affects monitoring and user trust)
- **Priority Score:** (5 - 0) × 1 × 3 = **15** ← High but Phase 5-specific
- **Rationale:** Phase 5 Monitor deliverable. Real-time ENCT Loop metrics (Compliance Rate, Homeostasis score) on dashboards.
- **Target:** Week 1–2 of Phase 5

### 3-2. P2-3 AI Auditors & Collaboration Channels
- **Composite Score:** 0/5 (absent, Phase 4 specific)
- **Impact Weight:** 0 (special role, not in checklist dependencies)
- **Cascade Length:** 3 (bootstrap safety depends on audit review)
- **Priority Score:** (5 - 0) × 1 × 3 = **15** ← Critical for Phase 4 but can defer to Phase 4-2
- **Rationale:** Secondary audit agent reviews bootstrap outcomes for axiom compliance. Needed before user-facing Phase 4 deployment.
- **Target:** Week 2 of Phase 4

### 3-3. P0-4 Ralph Loops
- **Composite Score:** 4/5 (Claude Code handles, but Phase 4 standalone needs custom implementation)
- **Impact Weight:** 0
- **Cascade Length:** 1 (localized to long-task reinjection)
- **Priority Score:** (5 - 4) × 1 × 1 = **1** ← Low priority
- **Rationale:** For Phase 4 SaaS deployment, long bootstrap tasks may need prompt reinjection across context resets.
- **Target:** Phase 4-2 (optional)

### 3-4. P0-6 Rippable Middleware
- **Composite Score:** 5/5 (N/A — all features are core)
- **Impact Weight:** 0
- **Cascade Length:** 1 (not applicable)
- **Priority Score:** 0 ← Not applicable
- **Rationale:** No extraneous features to rip out. All harness components are essential for ENCT.
- **Target:** N/A

### 3-5. P0-10 Inter-Agent Communication
- **Composite Score:** 0/5 (absent, Phase 4 specific)
- **Impact Weight:** 0
- **Cascade Length:** 2 (affects audit agent coordination)
- **Priority Score:** (5 - 0) × 1 × 2 = **10**
- **Rationale:** Audit agents and bootstrap agents must communicate via shared task lists and provenance bundles (Phase 4+).
- **Target:** Week 1–2 of Phase 4

### 3-6. P1-4 Progressive Skills
- **Composite Score:** 2/5 (partial — Claude Code tool loading exists, ENCT-specific role-based loading missing)
- **Impact Weight:** 1 (downstream: P0-4)
- **Cascade Length:** 1 (affects context window efficiency)
- **Priority Score:** (5 - 2) × 1 × 1 = **3**
- **Rationale:** Load bootstrap-agent skills separately from test-agent skills (progressive disclosure). Enhancement for context efficiency.
- **Target:** Phase 2–3 optional improvement

### 3-7. P1-6 Web Search & MCP Integration
- **Composite Score:** 3/5 (partial — Claude Code Web Search available, Phase 5 MCP integrations TBD)
- **Impact Weight:** 0
- **Cascade Length:** 1 (optional, not core)
- **Priority Score:** (5 - 3) × 1 × 1 = **2**
- **Rationale:** Phase 5 monitoring may integrate with alerting APIs (PagerDuty, Slack). Optional enhancement.
- **Target:** Phase 5+ (optional)

### 3-8. P3-1 Scheduled Cleanups
- **Composite Score:** 0/5 (absent, Phase 5 specific)
- **Impact Weight:** 0
- **Cascade Length:** 1 (localized cleanup)
- **Priority Score:** (5 - 0) × 1 × 1 = **5**
- **Rationale:** Weekly sweeps of old logs, test artifacts, stale branches (Phase 5 maintenance).
- **Target:** Phase 5-2

### 3-9. P3-3 Pattern Auditing
- **Composite Score:** 0/5 (absent, Phase 2+ optional)
- **Impact Weight:** 0
- **Cascade Length:** 1 (localized detection)
- **Priority Score:** (5 - 0) × 1 × 1 = **5**
- **Rationale:** Detect dead code paths, circular norm dependencies, unreachable verification (optional pattern audit).
- **Target:** Phase 3+ (optional)

### 3-10. P3-4 Consolidation Loop
- **Composite Score:** 0/5 (absent, Phase 5 specific)
- **Impact Weight:** 0
- **Cascade Length:** 2 (affects meta-doc consistency)
- **Priority Score:** (5 - 0) × 1 × 2 = **10**
- **Rationale:** Phase 5 consolidation agent reconciles ENCT-REFERENCE.md, AXIOMS.md, INDICATORS.md against code. Prevents drift.
- **Target:** Phase 5

**Tier 3 Sub-total:** 10 features  
**Tier 3 Timeline:** Phases 4–5+ (Weeks 13+). Can be deferred post-deployment for optimization.

---

## Timeline Synthesis

| Phase | Key Features (Tier 1 + Tier 2 Early) | Weeks | Output |
| --- | --- | --- | --- |
| **Phase 1 Design** | P0-2 Git, P1-1 Axioms, P1-10 Ledger, P1-11 Socratic, P2-4 Autonomy, P1-7 Tasks, P0-8 Versioning | 1–2 | 10–15 page spec + wireframes + ENCT-REFERENCE.md |
| **Phase 2 Train** | P0-3 Verification, P2-1 Linters, P2-2 Dependencies, P0-9 Wrappers, P1-3 Offloading, P1-9 Branches | 3–6 | Working prototype with bootstrap endpoint |
| **Phase 3 Test** | Extend P0-3 (500+ scenarios), P1-8 Anchoring, P3-2 Docs Sync | 7–10 | Test report + passing CI pipeline |
| **Phase 4 Deploy** | P2-3 Auditors, P0-5 Orchestration, P1-2 Compaction, P2-5 Intake Gate, P0-7 Escalation | 11–14 | Downloadable installer + UI dashboard |
| **Phase 5 Monitor** | P1-5 Observability, P3-1 Cleanups, P3-4 Consolidation, P1-6 MCP | 15–18 | Live monitoring service + alert ruleset |

---

## Critical Path Risk Assessment

**Blocking Dependencies:**
1. **P0-2 (Git)** → must exist before P1-1 (axioms), P1-9 (branches), P0-8 (versioning)
2. **P1-1 (Axioms in repo)** → must exist before P2-2 (dependency enforcement), P0-3 (verification gates)
3. **P1-10 (Ledger)** + **P1-11 (Socratic)** → must exist before P2-5 (intake gate)
4. **P0-3 (Verification)** → must exist before Phase 2 testing begins
5. **P2-4 (Autonomy Gates)** → must exist before Phase 1 design completes

**If any Tier 1 feature is delayed, all dependent Tier 2 features slip 1–2 weeks.**

---

## Next Step

Proceed to **Phase 3: Implementation Planning** to map each tier to concrete action items with owners, timelines, and deliverables.
