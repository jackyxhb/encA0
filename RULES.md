# Project Rules — ENCT v1.3 Development

**Visible to:** All IDEs, GitHub Copilot, code editors, LLM tools

---

## 1. Directory Organization Rule

### Documentation Folders

**`/enct/`** — All ENCT theory and design documents
- ENCT-REFERENCE.md (master theory document)
- AXIOMS.md (axiom definitions)
- INDICATORS.md (metric specifications)
- VERIFICATION.md (verification approaches)
- REQUIREMENTS.md (functional requirements)
- POLICY-INTAKE-TEMPLATE.md (Socratic framework)
- AUTONOMY-GATES.md (governance specification)
- ENCT-VERSION.md (versioning scheme)
- POLICY-LEDGER.md (policy registry)
- FAILURE-LEDGER.md (incident log)
- GLOSSARY.md (terminology)
- PHASE-*-COMPLETION-REPORT.md (phase milestones)

**`/harness/`** — All harness engineering documents (development methodology only)
- HE-SCOPE.md (audit scope)
- HE-CLUES.md (gap analysis)
- HE-PRIORITIES.md (prioritization)
- HE-IMPLEMENTATION-PLAN.md (implementation plan)
- AUDIT-SUMMARY.md (audit summary)

**Root Level** — Project-level structure
- ENCT-TASK-HIERARCHY.md (task structure + critical path)
- RULES.md (this file)
- .cursorrules (IDE instructions)

### Data Folders

- `/axioms/` — Axiom configuration files
- `/indicators/` — Indicator definitions
- `/bootstrap-logs/` — Bootstrap operation logs (Phase 4+)
- `/test-results/` — Test execution outputs
- `/enct-configs/` — ENCT configuration files
- `/enct-logs/` — Provenance bundles (Phase 4+)
- `/enct-decisions/` — Decision logs (Phase 5+)
- `/scripts/` — CLI utility scripts (Phase 2+)
- `/framework/` — Harness framework code (Phase 2+)

---

## 2. Code Organization Rule

### `/src/` Folder Structure — All Implementation Code

**`/src/enct/`** — ENCT engine implementation
- `/src/enct/primitives/` — Actant, Enactive Action, Normative Constraint, Cybernetic Loop
- `/src/enct/axioms/` — Axiom 1–4 enforcement code
- `/src/enct/loop/` — 5-phase Loop implementation (sense, validate, execute, assess, reenact)
- `/src/enct/indicators/` — 8 indicator calculations
- `/src/enct/verification/` — Verification approaches (model checking, sandbox, audit, red-team)
- `/src/enct/bootstrap/` — LLM-Assisted Bootstrap Pattern implementation

**`/src/harness/`** — Harness infrastructure (development-time only, NOT shipped)
- `/src/harness/gates/` — Autonomy gates, confidence thresholds, rate limiting
- `/src/harness/linters/` — Custom linters for spec validation
- `/src/harness/enforcement/` — Pre-commit hooks, CI gates
- `/src/harness/wrappers/` — Smart CLI wrappers (bootstrap, verify, rollback)

**`/src/api/`** — API endpoints (Phase 4+)
**`/src/ui/`** — User interface and dashboards (Phase 4+)
**`/src/storage/`** — Database and provenance storage (Phase 4+)
**`/src/monitoring/`** — Observability and alerting (Phase 5+)
**`/src/tests/`** — All test suites (Phase 2+)

### Code Placement Examples

| Code | Folder | Why |
|------|--------|-----|
| `axiom_1_enforcement.py` | `src/enct/axioms/` | Axiom implementation |
| `5_phase_loop.py` | `src/enct/loop/` | Loop orchestration |
| `homeostasis_score.py` | `src/enct/indicators/` | Indicator calculation |
| `confidence_gate.py` | `src/harness/gates/` | Gate enforcement |
| `bootstrap_pattern.py` | `src/enct/bootstrap/` | Bootstrap logic |
| `test_axiom_1.py` | `src/tests/` | Unit tests |

---

## 3. ENCT vs Harness Engineering Separation Rule

### ENCT (The Product)
**Scope:** The agent system itself
- 4 primitives, 4 axioms, 5-phase Loop, 8 indicators
- Bootstrap pattern for policy ingestion
- Everything the agent does operationally
- **Deployed to users**

### Harness Engineering (Development Methodology)
**Scope:** How we build ENCT safely and correctly
- Project auditing, gap analysis, priorities, implementation plans
- Verification gates during development
- Development process guidance
- **NOT part of deployed agent**
- **Discarded after Phase 5**

### The Relationship
**ENCT is the TARGET object; HE is the METHODOLOGY applied to it.**

They are **orthogonal, not partners.**

- Do NOT add HE features to ENCT at runtime
- Do NOT have ENCT code call HE code
- Do NOT ship HE code with deployed ENCT agent
- HE is purely a development-time tool

**When ENCT ships:**
- Include: `/src/enct/`, `/enct/` docs
- Exclude: `/src/harness/`, `/harness/` docs (development-only)

---

## 4. File Naming Convention

### Documentation
- `ENCT-*.md` — ENCT-specific docs (ENCT-REFERENCE.md, ENCT-VERSION.md, ENCT-TASK-HIERARCHY.md)
- `HE-*.md` — Harness engineering docs (HE-SCOPE.md, HE-CLUES.md, HE-PRIORITIES.md, HE-IMPLEMENTATION-PLAN.md)
- `PHASE-*-*.md` — Phase completion reports (PHASE-1-COMPLETION-REPORT.md, etc.)
- `*-TEMPLATE.md` — Templates (POLICY-INTAKE-TEMPLATE.md, etc.)

### Code
- `axiom_*.py` — Axiom implementations
- `*_loop.py` — Loop phase implementations
- `*_indicator.py` — Indicator calculations
- `*_gate.py` — Gate implementations
- `test_*.py` — Test files

---

## 5. Version Control Rule

### Commit Messages
Reference the folder when organizing:
```
git commit -m "Move ENCT docs to /enct folder"
git commit -m "Implement axiom enforcement in /src/enct/axioms/"
git commit -m "Add linters to /src/harness/linters/"
```

### Git Tags
Tag by phase:
```
git tag -a v1.3.0-phase1-complete
git tag -a v1.3.0-phase2-complete
```

### Branches
Branch by phase:
```
git branch enct-design     (Phase 1)
git branch enct-train      (Phase 2)
git branch enct-test       (Phase 3)
git branch enct-deploy     (Phase 4)
git branch enct-monitor    (Phase 5)
```

---

## 6. Enforcement

### Pre-commit Hook Check
```bash
# Reject code outside /src/ (except allowed configs)
# Reject docs outside /enct/ or /harness/
# Warn if HE code tries to integrate with ENCT code
```

### CI/CD Gate
```bash
# Run linters only on /src/ code
# Run tests only on /src/tests/
# Validate ENCT docs match /enct/ only
```

### Code Review
```
- Flag docs in wrong folder
- Flag code outside /src/
- Flag ENCT-HE integration attempts
- Ensure /src/harness/ not shipped with product
```

---

## 7. What IDEs Should Know

**For GitHub Copilot, VS Code, JetBrains, Cursor, etc.:**

When suggesting code or edits:
1. **Documentation:** Place in `/enct/` or `/harness/`, not root
2. **Code:** Place in `/src/enct/`, `/src/harness/`, `/src/tests/`, etc., not root
3. **ENCT work:** Suggest code in `/src/enct/`; suggest docs in `/enct/`
4. **Harness work:** Suggest code in `/src/harness/`; suggest docs in `/harness/`
5. **Do NOT mix:** ENCT code should not import from HE code
6. **Do NOT ship:** HE artifacts should not be in deployment package

---

## Summary

| Category | Location | Visible To | Purpose |
|----------|----------|-----------|---------|
| ENCT Docs | `/enct/` | All IDEs, GitHub, users | Specification |
| HE Docs | `/harness/` | All IDEs, GitHub, dev team | Methodology |
| ENCT Code | `/src/enct/` | All IDEs, GitHub, users | Product implementation |
| HE Code | `/src/harness/` | All IDEs, GitHub, dev team | Development tooling (not shipped) |
| Tests | `/src/tests/` | All IDEs, GitHub, CI/CD | Verification |
| Project Rules | RULES.md (this file) | All IDEs, GitHub | Convention enforcement |

---

**Last Updated:** 2026-04-05  
**Applies To:** Phases 1–5 and all contributors
