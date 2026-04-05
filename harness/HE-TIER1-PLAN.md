# HE Tier 1 Implementation Plan
**ENCT v1.3 Go Hub — Mechanical Enforcement Layer**

**Execution Time:** ~90 minutes  
**Complexity:** Light (config + hooks)  
**Scope:** P0-3, P2-1, P2-2, P0-11, P1-8, CI/CD  
**Owner:** Developer  
**Approval:** User explicit approval required before execution

---

## Pre-Implementation Checklist

- [ ] User approves this plan
- [ ] All 6 action items understood
- [ ] Backup/rollback strategy clear (git reset --hard)
- [ ] Test environment ready (local machine)

---

## Action 1: Pre-Commit Test Gating (P0-3)

**Feature:** Verification — Self & Collective  
**Feature Reference:** `references/features-foundation.md` → P0-3  
**Gap Addressed:** Tests exist but aren't gated; broken tests can commit

**What to Do:** Ensure tests pass before commits can proceed  
**Don't Do:** Don't skip test failures via `--no-verify` (tempting, defeats the gate)  
**Options:**
- Pre-commit hook (local, immediate)
- CI/CD gate (upstream, slower feedback)
- Both (recommended)

### Implementation

**Step 1:** Install husky for pre-commit hooks

```bash
cd /Users/macbook1/work/ENCT/encA0/src/enct-hub
npm init -y  # If no package.json exists
npm install husky --save-dev
npx husky install
```

**Step 2:** Add pre-commit hook for Go tests

```bash
npx husky add .husky/pre-commit "cd /Users/macbook1/work/ENCT/encA0/src/enct-hub && go test ./..."
```

**Step 3:** Verify hook is executable

```bash
ls -la .husky/pre-commit
# Should be executable (-rwx...)
```

**Step 4:** Test the gate

```bash
# Make a breaking change to a test
cd /Users/macbook1/work/ENCT/encA0
git add -A
git commit -m "test: break a test"
# Should fail with test output
```

**Rollback:** `rm .husky/pre-commit && npm uninstall husky`

**Metrics:** Commits now blocked if tests fail. Zero broken-test commits.

---

## Action 2: Automated Linting Setup (P2-1)

**Feature:** Constrain — Automated Linters  
**Feature Reference:** `references/features-pillar2-3.md` → P2-1  
**Gap Addressed:** No style or security linting; code quality opaque

**What to Do:** Lint Go code on commit using industry-standard linter  
**Don't Do:** Don't auto-fix during commit (only lint, let developer decide)  
**Options:**
- golangci-lint (recommended, batteries-included)
- Custom rules (if specific patterns needed)

### Implementation

**Step 1:** Install golangci-lint

```bash
# macOS
brew install golangci-lint

# Or from source
curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin
```

**Step 2:** Create `.golangci.yml` in project root

```yaml
# /Users/macbook1/work/ENCT/encA0/.golangci.yml
run:
  timeout: 5m
  tests: true

linters:
  enable:
    - gofmt
    - golint
    - gosimple
    - govet
    - ineffassign
    - misspell
    - staticcheck
    - typecheck
    - unused
  disable:
    - revive  # Too noisy for initial setup

output:
  format: colored-line-number

issues:
  exclude-rules:
    - path: _test\.go
      linters:
        - unused
```

**Step 3:** Test locally

```bash
cd /Users/macbook1/work/ENCT/encA0
golangci-lint run ./...
# Should pass initially or show warnings only
```

**Step 4:** Add to pre-commit hook

```bash
npx husky add .husky/pre-commit "cd /Users/macbook1/work/ENCT/encA0 && golangci-lint run ./src/enct-hub/..."
```

**Rollback:** `rm .golangci.yml && npm uninstall golangci-lint`

**Metrics:** All commits pass linting; code style consistent across team.

---

## Action 3: Import Boundary Enforcement (P2-2)

**Feature:** Constrain — Dependency Enforcement  
**Feature Reference:** `references/features-pillar2-3.md` → P2-2  
**Gap Addressed:** RULES.md says "/src/enct/ must NOT import /src/harness/", but no linter enforces it

**What to Do:** Prevent ENCT code from importing harness code  
**Don't Do:** Don't assume imports are correct; verify mechanically  
**Options:**
- golangci-lint custom rule (if available)
- Custom Go analysis tool
- Simple grep-based check in pre-commit

### Implementation

**Step 1:** Add custom import boundary check script

Create `/Users/macbook1/work/ENCT/encA0/scripts/check-import-boundaries.sh`:

```bash
#!/bin/bash
# Check that /src/enct-hub does not import /src/harness

set -e

ENCT_FILES=$(find /Users/macbook1/work/ENCT/encA0/src/enct-hub -type f -name "*.go" | grep -v _test.go)

VIOLATIONS=0
for file in $ENCT_FILES; do
  if grep -q "enct-hub/harness\|/src/harness" "$file"; then
    echo "❌ VIOLATION: $file imports harness code"
    VIOLATIONS=$((VIOLATIONS + 1))
  fi
done

if [ $VIOLATIONS -gt 0 ]; then
  echo "❌ Import boundary check failed: $VIOLATIONS violation(s)"
  exit 1
else
  echo "✅ Import boundary check passed"
  exit 0
fi
```

**Step 2:** Make executable and test

```bash
chmod +x /Users/macbook1/work/ENCT/encA0/scripts/check-import-boundaries.sh
/Users/macbook1/work/ENCT/encA0/scripts/check-import-boundaries.sh
# Should output: ✅ Import boundary check passed
```

**Step 3:** Add to pre-commit hook

```bash
npx husky add .husky/pre-commit "/Users/macbook1/work/ENCT/encA0/scripts/check-import-boundaries.sh"
```

**Rollback:** `rm scripts/check-import-boundaries.sh`

**Metrics:** Zero harness imports in ENCT code. Architecture protected.

---

## Action 4: Create AGENTS.md (P0-11)

**Feature:** Foundation — Portable Agent Surface  
**Feature Reference:** `references/features-foundation.md` → P0-11  
**Gap Addressed:** Rules only in .cursorrules (Cursor-specific); other AI agents have no rules

**What to Do:** Extract rules to IDE-agnostic AGENTS.md  
**Don't Do:** Don't duplicate; make .cursorrules import from AGENTS.md  

### Implementation

**Step 1:** Create AGENTS.md

Create `/Users/macbook1/work/ENCT/encA0/AGENTS.md`:

```markdown
# AGENTS.md — Portable Rules for All AI Agents

This file defines project rules for **all AI agents and LLM-based tools** (Claude, GitHub Copilot, Cursor, etc.). 
It is IDE-agnostic and portable.

---

## Critical Rules

### 1. Folder Organization (MANDATORY)

**ENCT Documentation** → `/enct/` folder ONLY
- Theory docs, specifications, ledgers, reports
- See /RULES.md for full list

**Harness Engineering Documentation** → `/harness/` folder ONLY
- Audit docs, implementation plans, HE reports
- Development methodology only (not shipped)

**Project-Level Documentation** → Root only
- ENCT-TASK-HIERARCHY.md
- RULES.md
- README.md

### 2. Code Organization (MANDATORY)

All implementation code in `/src/`:
- `/src/enct-hub/` — ENCT engine (Go)
- `/src/harness/` — Harness tooling (NOT shipped)
- `/src/tests/` — All tests

**NO code at root** (except build configs)

### 3. ENCT vs Harness Engineering (CRITICAL)

**They are orthogonal, NOT partners.**
- Do NOT integrate HE features into ENCT at runtime
- Do NOT have ENCT code import from harness code
- HE is purely development-time scaffolding
- When ENCT ships, HE code is completely removed

### 4. Git Commits

Include folder context:
```
"Add axiom enforcement to /src/enct-hub/engine/"
"Implement linters in /src/harness/"
"Move docs to /enct/"
```

---

## When Making Suggestions

**For ENCT work:**
- Suggest code placement: `/src/enct-hub/[component]/`
- Suggest docs placement: `/enct/`
- Do NOT reference HE code

**For Harness work:**
- Suggest code placement: `/src/harness/[component]/`
- Suggest docs placement: `/harness/`

**Never:**
- Suggest code at root (except configs)
- Mix ENCT and HE code
- Include HE code in deployment

---

## Reference Documents

See `/RULES.md` for complete project rules.
See `/README.md` for project overview.
```

**Step 2:** Update .cursorrules to reference AGENTS.md

Edit `/Users/macbook1/work/ENCT/encA0/.cursorrules` (line 1):

```
# .cursorrules — ENCT v1.3 Project Rules for Cursor IDE
# For portable rules across all IDEs, see /AGENTS.md

[rest of file unchanged...]
```

**Rollback:** `rm AGENTS.md`

**Metrics:** All AI agents (Cursor, Claude, Copilot) now follow same rules. Consistency across tools.

---

## Action 5: Create Decision Ledger (P1-8)

**Feature:** Inform — Context Anchoring  
**Feature Reference:** `references/features-pillar1.md` → P1-8  
**Gap Addressed:** Design decisions made but not recorded; knowledge lost between sessions

**What to Do:** Record all HE audit and design decisions with rationale  
**Don't Do:** Don't lose decisions to session memory; write them down  

### Implementation

**Step 1:** Create HE-DECISIONS.md

Create `/Users/macbook1/work/ENCT/encA0/harness/HE-DECISIONS.md`:

```markdown
# HE Decisions — Design & Audit Log

**Phase:** v1.3 Go Hub (Phase 2)  
**Last Updated:** 2026-04-06

---

## Decision 1: Pre-Commit Test Gating

**Date:** 2026-04-06  
**Category:** P0-3 Verification  
**Decision:** Implement pre-commit hook for `go test ./...`  
**Rationale:** Tests exist but aren't gated. Broken code can merge. Hook provides immediate feedback.  
**Alternative Considered:** CI/CD-only gating (slower feedback loop)  
**Impact:** Zero broken-test commits; faster development cycle  
**Reversible:** Yes (git reset --hard)

---

## Decision 2: golangci-lint for Code Quality

**Date:** 2026-04-06  
**Category:** P2-1 Linting  
**Decision:** Use golangci-lint with conservative linting rules  
**Rationale:** Industry standard, batteries-included, low configuration burden  
**Alternative Considered:** Custom linters (too much maintenance)  
**Impact:** Code quality baseline; consistent style  
**Reversible:** Yes

---

## Decision 3: Import Boundary Protection

**Date:** 2026-04-06  
**Category:** P2-2 Dependency Enforcement  
**Decision:** Custom shell script in pre-commit hook checks for `/src/harness/` imports in ENCT code  
**Rationale:** Prevents ENCT-HE contamination; protects core architecture  
**Alternative Considered:** golangci-lint custom rule (not mature enough)  
**Impact:** Architecture violation impossible without explicit commit bypass  
**Reversible:** Yes

---

## Decision 4: AGENTS.md for Portability

**Date:** 2026-04-06  
**Category:** P0-11 Portable Agent Surface  
**Decision:** Extract project rules to IDE-agnostic AGENTS.md  
**Rationale:** Future agents (Claude, Copilot, etc.) need rules. IDE-specific files insufficient.  
**Alternative Considered:** Cursor-only rules (not portable)  
**Impact:** Consistent agent behavior across all tools  
**Reversible:** Yes

---

## Decision 5: Tier 1 Implementation Prioritization

**Date:** 2026-04-06  
**Category:** Harness Planning  
**Decision:** Prioritize P0-3, P2-1, P2-2 in Tier 1; defer P3-1/P3-2 to Tier 2  
**Rationale:** Tier 1 features are critical (tests, linting, architecture). Tier 2 features are maintenance.  
**Alternative Considered:** All features in Tier 1 (90-minute session too short)  
**Impact:** Baseline harness in place; foundation for future layers  
**Reversible:** N/A (layered approach)

---

## Next Session: Record New Decisions Here

Track all audit findings and design choices. Use this format:

- **Date:** YYYY-MM-DD
- **Category:** [HE Feature | Design | Architecture | Process]
- **Decision:** What was decided?
- **Rationale:** Why?
- **Alternative Considered:** What else was considered?
- **Impact:** What changes?
- **Reversible:** Can this be undone?

---

```

**Rollback:** `rm HE-DECISIONS.md`

**Metrics:** All decisions recorded. Knowledge persists across sessions. Future audits reference this.

---

## Action 6: GitHub Actions CI/CD Workflow (P0-3 Collective)

**Feature:** Foundation — Verification (Collective)  
**Feature Reference:** `references/features-foundation.md` → P0-3  
**Gap Addressed:** Tests don't run on PR; no upstream gate

**What to Do:** Run tests on push/PR via GitHub Actions  
**Don't Do:** Don't block master merges yet (warning only first)

### Implementation

**Step 1:** Create GitHub Actions workflow

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on:
  push:
    branches: [master, "feat/*"]
  pull_request:
    branches: [master]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-go@v4
        with:
          go-version: '1.21'
      - name: Run tests
        run: cd src/enct-hub && go test -v ./...
      - name: Run linter
        run: cd src/enct-hub && go vet ./...
```

**Step 2:** Commit and push

```bash
cd /Users/macbook1/work/ENCT/encA0
git add .github/workflows/test.yml
git commit -m "ci: add GitHub Actions test workflow"
git push origin feat/ui-hub-v0.4.0
```

**Step 3:** Verify on GitHub

- Go to github.com/jackyxhb/encA0
- Click "Actions" tab
- Should show "Tests" workflow running on the commit

**Rollback:** `git reset --hard HEAD~1 && git push --force`

**Metrics:** All PRs have test status visible. Broken code visible immediately.

---

## Execution Checklist

### Pre-Flight

- [ ] User approves this plan
- [ ] Git is clean (`git status` shows no uncommitted changes)
- [ ] All tools installed (Go, npm, golangci-lint)
- [ ] Backup branch exists (`git branch backup-$(date +%s)`)

### Actions 1–6 In Order

- [ ] **Action 1:** Pre-commit test gating
  - [ ] husky installed
  - [ ] Hook created and tested
  
- [ ] **Action 2:** golangci-lint setup
  - [ ] Tool installed
  - [ ] .golangci.yml created
  - [ ] Runs without errors
  
- [ ] **Action 3:** Import boundary check
  - [ ] Script created and executable
  - [ ] Passes locally
  - [ ] Added to pre-commit hook
  
- [ ] **Action 4:** AGENTS.md
  - [ ] Created with rules
  - [ ] .cursorrules updated
  
- [ ] **Action 5:** HE-DECISIONS.md
  - [ ] Created with decisions
  
- [ ] **Action 6:** GitHub Actions workflow
  - [ ] `.github/workflows/test.yml` created
  - [ ] Committed and pushed
  - [ ] Verified on GitHub

### Post-Flight

- [ ] All pre-commit hooks working
- [ ] `git status` shows new files (AGENTS.md, HE-DECISIONS.md, .golangci.yml, etc.)
- [ ] Ready to commit and push
- [ ] Audit report committed to `/harness/HE-AUDIT-REPORT.md`

---

## Rollback Strategy

If anything breaks:

```bash
# Full rollback to before Tier 1
git reset --hard <commit-before-tier1>
git push --force origin feat/ui-hub-v0.4.0
```

Or incrementally:

```bash
# Remove specific changes
rm .husky/pre-commit
rm .golangci.yml
rm scripts/check-import-boundaries.sh
rm AGENTS.md
rm harness/HE-DECISIONS.md
rm .github/workflows/test.yml
git reset --hard
```

---

## Success Criteria

After Tier 1 is complete:

- ✅ Tests block commits if failing
- ✅ Code style is validated on commit
- ✅ Import boundaries are enforced
- ✅ Rules are portable (AGENTS.md exists)
- ✅ Decisions are recorded (HE-DECISIONS.md exists)
- ✅ CI/CD reports on PRs

**Estimated Outcome:** Maturity 2.1 → 3.6 / 5 (+1.5 points)

---

## Time Breakdown

| Action | Estimated | Actual |
|--------|-----------|--------|
| 1. Pre-commit tests | 15 min | _ |
| 2. Linting setup | 20 min | _ |
| 3. Import boundaries | 15 min | _ |
| 4. AGENTS.md | 10 min | _ |
| 5. HE-DECISIONS.md | 5 min | _ |
| 6. GitHub Actions | 25 min | _ |
| **TOTAL** | **90 min** | **_ min** |

---

**Next Steps After Tier 1:**
1. Review HE-AUDIT-REPORT.md findings
2. Plan Tier 2 (Task tracking, observability)
3. Phase 3 preparation

---

**Plan Generated:** 2026-04-06  
**Owner:** User approval required before execution  
