# AGENTS.md — Portable Rules for All AI Agents

This file defines project rules for **all AI agents and LLM-based tools** (Claude, GitHub Copilot, Cursor, etc.).  
It is **IDE-agnostic** and **portable** across all development environments.

---

## Critical Rules

### 1. Folder Organization (MANDATORY)

**ENCT Documentation** → `/enct/` folder ONLY
- Theory docs, specifications, ledgers, reports
- ENCT-REFERENCE.md, AXIOMS.md, INDICATORS.md, VERIFICATION.md
- POLICY-LEDGER.md, FAILURE-LEDGER.md
- PHASE-*-COMPLETION-REPORT.md

**Harness Engineering Documentation** → `/harness/` folder ONLY
- Audit docs, implementation plans, HE reports
- HE-SCOPE.md, HE-CLUES.md, HE-PRIORITIES.md, HE-IMPLEMENTATION-PLAN.md
- **Development methodology only** (NOT shipped with product)

**Project-Level Documentation** → Root only
- ENCT-TASK-HIERARCHY.md (task structure + critical path)
- RULES.md (project rules)
- README.md (project overview)
- .cursorrules, .claude.md (IDE-specific, reference AGENTS.md)

### 2. Code Organization (MANDATORY)

All implementation code in `/src/`:

```
/src/enct-hub/           ← ENCT engine implementation (Go)
  /engine/               ← Core loop, axioms, indicators
  /tests/                ← Test suites
  templates/             ← JSON templates for policies

/src/tests/              ← Additional test code

/src/harness/            ← Harness tooling (NOT shipped, dev-time only)

/src/api/                ← API endpoints (Phase 4+)
/src/ui/                 ← User interface (Phase 4+)
/src/storage/            ← Database & storage (Phase 4+)
/src/monitoring/         ← Observability (Phase 5+)
```

**NO code at root** (except build configs like go.mod, package.json, Makefile, docker-compose.yml)

### 3. ENCT vs Harness Engineering (CRITICAL SEPARATION)

**They are orthogonal, NOT partners.**

- ✅ **ENCT** = The agent product being built (what ships to users)
  - 4 axioms, 5-phase loop, 8 indicators
  - All operational logic
  - Lives in `/src/enct-hub/` and `/enct/`

- ✅ **Harness Engineering (HE)** = Development methodology for building ENCT safely (temporary, discarded post-deployment)
  - Audit infrastructure, verification gates, linters
  - Development-time scaffolding only
  - Lives in `/src/harness/` and `/harness/`

**Enforcement:**
- ❌ Do NOT integrate HE features into ENCT at runtime
- ❌ Do NOT have ENCT code import from harness code
- ❌ Do NOT ship `/src/harness/` or `/harness/` docs with product
- ✅ When ENCT ships, HE code is completely removed

### 4. Git Commits

Include folder context in all commit messages:

```
"feat: add axiom enforcement to /src/enct-hub/engine/axioms.go"
"ci: add GitHub Actions test workflow in .github/workflows/"
"docs: update RULES in /harness/"
"test: add scenario tests to /src/enct-hub/tests/"
```

### 5. Pre-Commit Gates

These checks run **before every commit** (via `.git/hooks/pre-commit`):

1. ✅ **Tests:** `go test ./...` must pass
2. ✅ **Linting:** `go vet ./...` must pass
3. ✅ **Import Boundaries:** `/src/enct-hub/` must NOT import `/src/harness/`

If any check fails, commit is **blocked**. This is intentional.

---

## When Making Suggestions

### For ENCT Work

- **Code placement:** `/src/enct-hub/[component]/`
- **Docs placement:** `/enct/`
- **Do NOT reference HE code** in ENCT suggestions
- **Do NOT suggest features** that require harness integration

### For Harness Work

- **Code placement:** `/src/harness/[component]/`
- **Docs placement:** `/harness/`
- **Mark as development-only** in comments
- **Never export to ENCT**

### General Rules

- ✅ **Do:** Place code/docs in correct folders per organization rule
- ✅ **Do:** Reference RULES.md for conventions
- ✅ **Do:** Include folder context in commit messages
- ❌ **Don't:** Suggest code at root (except configs)
- ❌ **Don't:** Mix ENCT and HE code
- ❌ **Don't:** Ship HE artifacts with product
- ❌ **Don't:** Assume IDE-specific rules are portable

---

## Reference Documents

- **Full Rules:** See `/RULES.md` in repo
- **Project Overview:** See `/README.md`
- **Task Hierarchy:** See `/ENCT-TASK-HIERARCHY.md`
- **Harness Audit:** See `/harness/HE-AUDIT-REPORT.md`
- **Harness Plan:** See `/harness/HE-TIER1-PLAN.md`
- **ENCT Theory:** See `/enct/ENCT-REFERENCE.md`
- **Harness Methodology:** See `/harness/HE-SCOPE.md`

---

## Summary for All AI Agents

| Category | Location | Purpose | Visible To |
|----------|----------|---------|-----------|
| ENCT Docs | `/enct/` | Product spec & governance | All IDEs, GitHub, users |
| HE Docs | `/harness/` | Development methodology | All IDEs, GitHub, dev team |
| ENCT Code | `/src/enct-hub/` | Product implementation | All IDEs, GitHub, deployed |
| HE Code | `/src/harness/` | Dev infrastructure | All IDEs, GitHub (NOT deployed) |
| Tests | `/src/enct-hub/tests/`, `/src/tests/` | Verification | All IDEs, GitHub, CI/CD |
| Portable Rules | **AGENTS.md** (this file) | Rules for all agents | All IDEs, GitHub |

---

**Version:** 1.0  
**Last Updated:** 2026-04-06  
**Applies To:** All phases, all contributors, all AI agents and tools
