# Contributing Guidelines — ENCT v1.3 Project

## Project Structure

This project develops an agent with ENCT (Enactive Normative Control Theory) framework, guided by Harness Engineering methodology.

### Documentation Folders
- `/enct/` — ENCT theory, specifications, governance (product specification)
- `/harness/` — Harness Engineering audit, gaps, plans (development methodology)

### Code Folders
- `/src/enct/` — ENCT engine implementation (shipped to users)
- `/src/harness/` — Harness tooling (development-time only, NOT shipped)
- `/src/tests/` — All test suites
- `/src/api/`, `/src/ui/`, `/src/storage/`, `/src/monitoring/` — Supporting components

## Key Rules

### 1. Documentation Organization
**Place ENCT docs in `/enct/` folder:**
- ENCT-REFERENCE.md, AXIOMS.md, INDICATORS.md, VERIFICATION.md
- REQUIREMENTS.md, AUTONOMY-GATES.md, POLICY-INTAKE-TEMPLATE.md
- ENCT-VERSION.md, POLICY-LEDGER.md, FAILURE-LEDGER.md, GLOSSARY.md

**Place HE docs in `/harness/` folder:**
- HE-SCOPE.md, HE-CLUES.md, HE-PRIORITIES.md
- HE-IMPLEMENTATION-PLAN.md, AUDIT-SUMMARY.md

**Place project-level docs in root:**
- ENCT-TASK-HIERARCHY.md, RULES.md, README.md

### 2. Code Organization
**All code goes in `/src/` with component subfolders:**
```
/src/enct/              ← ENCT engine
  /axioms/              ← Axiom enforcement
  /loop/                ← 5-phase Loop
  /indicators/          ← Indicator calculations
  /bootstrap/           ← Bootstrap pattern
  /verification/        ← Verification code
  /primitives/          ← Core primitives

/src/harness/           ← HE tooling (dev-time only)
  /gates/
  /linters/
  /enforcement/
  /wrappers/

/src/api/               ← API endpoints (Phase 4+)
/src/ui/                ← UI/dashboards (Phase 4+)
/src/storage/           ← Database (Phase 4+)
/src/monitoring/        ← Observability (Phase 5+)

/src/tests/             ← All tests
```

### 3. ENCT vs Harness Separation (CRITICAL)
- **ENCT** = The agent product (shipped to users)
- **Harness Engineering** = Development methodology (temporary, discarded)

**They are NOT partners; they are orthogonal:**
- Do NOT integrate HE code with ENCT code
- Do NOT have ENCT import from `/src/harness/`
- HE is purely development-time scaffolding
- When deploying ENCT, exclude all HE code

### 4. Naming Conventions

**Docs:**
- `ENCT-*.md` for ENCT-specific docs
- `HE-*.md` for harness docs
- `PHASE-*-*.md` for phase reports
- `*-TEMPLATE.md` for templates

**Code:**
- `axiom_*.py` for axiom code
- `*_loop.py` for loop phase code
- `*_indicator.py` for indicator code
- `*_gate.py` for gate code
- `test_*.py` for tests

### 5. Git Commits
Include folder context in messages:
```
"Add axiom enforcement to /src/enct/axioms/"
"Move ENCT docs to /enct/ folder"
"Implement bootstrap in /src/enct/bootstrap/"
"Add tests to /src/tests/"
```

Use tags for phase milestones:
```
git tag -a v1.3.0-phase1-complete
git tag -a v1.3.0-phase2-complete
```

### 6. When Implementing Features

**ENCT Work:**
- Code location: `/src/enct/[component]/`
- Docs location: `/enct/`
- Reference ENCT-REFERENCE.md for specifications

**Harness Work (Development-Time):**
- Code location: `/src/harness/[component]/`
- Docs location: `/harness/`
- DO NOT ship this code with ENCT product

**Tests:**
- Location: `/src/tests/`
- Test ENCT implementation against `/enct/` specifications
- Do NOT test HE code (dev-time only)

## Phase Context

**Current:** Phase 1 (Design) — COMPLETE
**Next:** Phase 2 (Training) — Implement ENCT engine in `/src/enct/`

See `/ENCT-TASK-HIERARCHY.md` for full phase breakdown.

## Code Review Checklist

- [ ] Docs placed in `/enct/` or `/harness/`, not root
- [ ] Code placed in `/src/`, not root
- [ ] ENCT code in `/src/enct/`, HE code in `/src/harness/`
- [ ] No cross-imports between ENCT and HE
- [ ] Tests in `/src/tests/`
- [ ] Commit message includes folder context
- [ ] `/src/harness/` code is NOT shipped with product (Phase 4+)

## Questions?

Refer to:
- `RULES.md` — Complete project rules
- `ENCT-TASK-HIERARCHY.md` — Task structure
- `/enct/ENCT-REFERENCE.md` — ENCT theory
- `/harness/HE-SCOPE.md` — HE methodology
