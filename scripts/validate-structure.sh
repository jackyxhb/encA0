#!/bin/bash
# Validate that code structure matches RULES.md specification

set -e

echo "🔍 Validating project structure against RULES.md..."
echo ""

ERRORS=0

# Check 1: /src/ folder exists and has expected subdirectories
echo "✓ Checking /src/ structure..."
if [ ! -d "src/engine" ]; then
  echo "  ❌ FAIL: src/engine/ not found"
  ERRORS=$((ERRORS + 1))
else
  echo "  ✅ src/engine/ exists"
fi

if [ ! -d "src/enchub" ]; then
  echo "  ❌ FAIL: src/enchub/ not found"
  ERRORS=$((ERRORS + 1))
else
  echo "  ✅ src/enchub/ exists"
fi

# Check 2: No code at root (except configs)
echo "✓ Checking root directory..."
ILLEGAL_GO_FILES=$(find . -maxdepth 1 -name "*.go" -type f | wc -l)
if [ "$ILLEGAL_GO_FILES" -gt 0 ]; then
  echo "  ❌ FAIL: Found .go files at root (should be in /src/)"
  ERRORS=$((ERRORS + 1))
else
  echo "  ✅ No .go files at root"
fi

# Check 3: Documentation in correct folders
echo "✓ Checking documentation placement..."
ENCT_DOCS=$(find enct/ -name "*.md" 2>/dev/null | wc -l)
if [ "$ENCT_DOCS" -eq 0 ]; then
  echo "  ❌ FAIL: No docs found in /enct/"
  ERRORS=$((ERRORS + 1))
else
  echo "  ✅ Found $ENCT_DOCS docs in /enct/"
fi

HARNESS_DOCS=$(find harness/ -name "*.md" 2>/dev/null | wc -l)
if [ "$HARNESS_DOCS" -eq 0 ]; then
  echo "  ❌ FAIL: No docs found in /harness/"
  ERRORS=$((ERRORS + 1))
else
  echo "  ✅ Found $HARNESS_DOCS docs in /harness/"
fi

# Check 4: RULES.md and AGENTS.md exist at root
echo "✓ Checking project-level rules..."
if [ ! -f "RULES.md" ]; then
  echo "  ❌ FAIL: RULES.md not found at root"
  ERRORS=$((ERRORS + 1))
else
  echo "  ✅ RULES.md exists"
fi

if [ ! -f "AGENTS.md" ]; then
  echo "  ❌ FAIL: AGENTS.md not found at root"
  ERRORS=$((ERRORS + 1))
else
  echo "  ✅ AGENTS.md exists"
fi

# Check 5: Tests in /src/engine/, /src/enchub/tests/, and/or /src/tests/
echo "✓ Checking test placement..."
TEST_COUNT=$(find src/engine src/enchub/tests src/tests -name "*_test.go" 2>/dev/null | wc -l)
if [ "$TEST_COUNT" -eq 0 ]; then
  echo "  ❌ FAIL: No tests found in /src/engine/, /src/enchub/tests/, or /src/tests/"
  ERRORS=$((ERRORS + 1))
else
  echo "  ✅ Found $TEST_COUNT test files"
fi

# Check 6: .cursorrules and .claude.md exist (IDE rules)
echo "✓ Checking IDE configuration files..."
if [ ! -f ".cursorrules" ]; then
  echo "  ❌ FAIL: .cursorrules not found"
  ERRORS=$((ERRORS + 1))
else
  echo "  ✅ .cursorrules exists"
fi

if [ ! -f ".claude.md" ]; then
  echo "  ❌ FAIL: .claude.md not found"
  ERRORS=$((ERRORS + 1))
else
  echo "  ✅ .claude.md exists"
fi

echo ""
if [ "$ERRORS" -eq 0 ]; then
  echo "✅ Structure validation PASSED — code matches RULES.md"
  exit 0
else
  echo "❌ Structure validation FAILED — $ERRORS error(s) found"
  echo ""
  echo "Please check RULES.md for correct folder structure:"
  echo "  - ENCT docs → /enct/"
  echo "  - HE docs → /harness/"
  echo "  - Code → /src/"
  echo "  - Rules → RULES.md, AGENTS.md (root)"
  exit 1
fi
