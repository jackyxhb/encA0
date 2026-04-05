# Harness Engineering Scope & Baseline — ENCT v1.3 Agent Product

**Date:** 2026-04-05  
**Audit Type:** Full Audit (Phase 0 Pre-Flight + Phase 1 Gap Analysis)  
**Project Status:** Greenfield (no infrastructure yet)

---

## Project Identification

**Name:** ENCT v1.3 (Enactive Normative Control Theory) — Full Agent Software Product  
**Objective:** Transform abstract ENCT theory into a downloadable, out-of-box full agent product with natural-language policy bootstrapping and normative control as unbreakable core.

**Architecture:** Single Agent System (SAS) with MAS-Readiness pathway (transitionable to Multi-Agent via P0-5 Orchestration and P2-3 AI Auditors).

**Tech Stack:** (TBD during Phase 1 Design)
- ENCT Engine: Axioms, 5-phase Loop, indicators, verification approaches
- LLM-Assisted Bootstrap Pattern: CandidateModule, quality gates, sandbox
- Deployment: Docker/installer + cloud SaaS option (Phase 4)
- Observability: Real-time ENCT Loop monitoring with adaptive sampling

**Complexity Level:** Complex System  
- Involves normative constraint versioning (Git-backed)
- Multi-phase ALM lifecycle (Design → Train → Test → Deploy → Monitor)
- Live governance dashboards and automation
- Verification and audit trails

---

## Quick-Start Evaluation Results

### Foundation (Can the agent execute safely?)
- [ ] P0-1 Bash Sandboxes
- [ ] P0-2 Filesystem & Git
- [ ] P0-3 Verification (Self & Collective)
- [ ] P0-4 Ralph Loops
- [ ] P0-5 Orchestration
- [ ] P0-6 Rippable Middleware
- [ ] P0-7 Escalation Policies & Audit Trails
- [ ] P0-8 Harness Versioning
- [ ] P0-9 Smart Command Wrappers
- [ ] P0-10 Inter-Agent Communication

**Current State:** 0/10 — No foundational infrastructure  
**Risk:** Without these, agent cannot safely execute or verify work before user deployment.

### Pillar 1 (Inform) — Does the agent know what it needs to know?
- [ ] P1-1 Repository as Truth
- [ ] P1-2 Context Compaction & Memory Management
- [ ] P1-3 Tool Offloading
- [ ] P1-4 Progressive Skills
- [ ] P1-5 Observability / Dashboards
- [ ] P1-6 Web Search & MCP
- [ ] P1-7 Planning, Task Lists & Blackboards
- [ ] P1-8 Context Anchoring
- [ ] P1-9 Branch-Based Memory
- [ ] P1-10 Requirements Ledger
- [ ] P1-11 Socratic Questioning

**Current State:** 0/11 — No context infrastructure  
**Risk:** Agent lacks access to ENCT axioms, indicators, verification approaches, and user requirements.

### Pillar 2 (Constrain) — Is the agent mechanically prevented from bad output?
- [ ] P2-1 Automated Linters
- [ ] P2-2 Dependency Enforcement
- [ ] P2-3 AI Auditors & Collaboration Channels
- [ ] P2-4 Bounded Autonomy & Access Control
- [ ] P2-5 Upstream Intake Gate

**Current State:** 0/5 — No constraints  
**Risk:** Without gates, agent can bootstrap unsafe policies or overwrite versioned norms.

### Pillar 3 (Maintain) — Does the system clean up after itself?
- [ ] P3-1 Scheduled Cleanups
- [ ] P3-2 Documentation Sync
- [ ] P3-3 Pattern Auditing
- [ ] P3-4 Consolidation Loop

**Current State:** 0/4 — No maintenance automation  
**Risk:** Normative drift, stale axiom versions, indicator metric misalignment.

---

## Harness Maturity Level

**Baseline:** Level 0 (Pre-Infrastructure)  
- No sandboxes, no Git tracking, no verification gates  
- No context management, no observability, no automation  
- No constraints, no auditors, no maintenance loops

**Target (Phase 4 Deployment):** Level 3+ (Functional, Autonomous)  
- All P0 foundations in place and passing CI  
- All P1 context features active (ENCT axioms, indicators, memory)  
- All P2 constraints mechanically enforced (bootstrap gates, audit trails)  
- All P3 maintenance loops running (versioning, observability, consolidation)

---

## ENCT-Specific Harness Priorities

The ALM pathway (Design → Train → Test → Deploy → Monitor) depends critically on:

1. **P0-2 Filesystem & Git:** Versioning of normative constraints, axiom updates, bootstrap outcomes
2. **P0-3 Verification:** Tiered validation gates (Tier 1/2/3) must pass before bootstrap completion
3. **P1-1 Repository as Truth:** All ENCT primitives, axioms, indicators live in repo (not human heads)
4. **P1-5 Observability:** Live ENCT Loop metrics (Compliance Rate, Homeostasis score) streamed to dashboards
5. **P2-3 AI Auditors:** Secondary agent verifies normative constraint changes before accepting
6. **P2-5 Upstream Intake Gate:** User policies screened via Socratic questioning before bootstrap
7. **P3-4 Consolidation Loop:** Axiom versions, indicators, bootstrap results stay synced

---

## Next Steps

This scope document establishes baseline (Level 0). Phase 1 (Gap Analysis) will:
1. Map all 30 features against ENCT design requirements
2. Identify critical path dependencies for Phases 1–5 ALM
3. Score gaps across 6 evaluation dimensions
4. Tier remediation into Tier 1 (Immediate), Tier 2 (Mid-term), Tier 3 (Long-term)
5. Generate concrete implementation plan with action items
