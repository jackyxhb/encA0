#!/bin/bash
# Validate that RULES.md specification matches actual code structure
# Prevents doc-code divergence from accumulating

set -e

echo "📋 Validating RULES.md vs actual structure..."
echo ""

MISMATCHES=0

# Rule 1: /src/enct-hub/ must exist
echo "✓ Checking RULE #2: Code in /src/enct-hub/"
if [ ! -d "src/enct-hub" ]; then
  echo "  ❌ MISMATCH: RULES.md says /src/enct-hub/ exists, but not found"
  MISMATCHES=$((MISMATCHES + 1))
else
  echo "  ✅ /src/enct-hub/ exists as specified"
fi

# Rule 2: /enct/ docs must exist
echo "✓ Checking RULE #1: ENCT docs in /enct/"
if [ ! -d "enct" ] || [ $(find enct -name "*.md" 2>/dev/null | wc -l) -eq 0 ]; then
  echo "  ❌ MISMATCH: RULES.md requires /enct/ docs"
  MISMATCHES=$((MISMATCHES + 1))
else
  DOC_COUNT=$(find enct -name "*.md" | wc -l)
  echo "  ✅ /enct/ docs present ($DOC_COUNT files)"
fi

# Rule 3: /harness/ docs must exist
echo "✓ Checking RULE #1: Harness docs in /harness/"
if [ ! -d "harness" ] || [ $(find harness -name "*.md" 2>/dev/null | wc -l) -eq 0 ]; then
  echo "  ❌ MISMATCH: RULES.md requires /harness/ docs"
  MISMATCHES=$((MISMATCHES + 1))
else
  DOC_COUNT=$(find harness -name "*.md" | wc -l)
  echo "  ✅ /harness/ docs present ($DOC_COUNT files)"
fi

# Rule 4: No code at root
echo "✓ Checking RULE #2: No code at root"
ILLEGAL_CODE=$(find . -maxdepth 1 \( -name "*.go" -o -name "*.py" -o -name "*.rs" \) -type f 2>/dev/null | wc -l)
if [ "$ILLEGAL_CODE" -gt 0 ]; then
  echo "  ❌ MISMATCH: Found code at root (RULES.md forbids this)"
  MISMATCHES=$((MISMATCHES + 1))
else
  echo "  ✅ No code at root (as specified)"
fi

# Rule 5: Tests in /src/enct-hub/tests/
echo "✓ Checking RULE #2: Tests in /src/enct-hub/tests/"
if [ ! -d "src/enct-hub/tests" ] && [ ! -d "src/tests" ]; then
  echo "  ❌ MISMATCH: RULES.md requires tests in /src/"
  MISMATCHES=$((MISMATCHES + 1))
else
  echo "  ✅ Test directories exist as specified"
fi

# Rule 6: RULES.md and AGENTS.md at root
echo "✓ Checking RULE #1: Root-level rules files"
if [ ! -f "RULES.md" ] || [ ! -f "AGENTS.md" ]; then
  echo "  ❌ MISMATCH: Missing RULES.md or AGENTS.md"
  MISMATCHES=$((MISMATCHES + 1))
else
  echo "  ✅ RULES.md and AGENTS.md present"
fi

# Rule 7: IDE configuration files
echo "✓ Checking RULE #1: IDE config files"
if [ ! -f ".cursorrules" ] || [ ! -f ".claude.md" ]; then
  echo "  ❌ MISMATCH: Missing IDE config files"
  MISMATCHES=$((MISMATCHES + 1))
else
  echo "  ✅ IDE config files present"
fi

echo ""
if [ "$MISMATCHES" -eq 0 ]; then
  echo "✅ RULES.md sync check PASSED — documentation matches code"
  exit 0
else
  echo "❌ RULES.md sync check FAILED — $MISMATCHES mismatch(es)"
  echo ""
  echo "Action: Review RULES.md and update to match actual structure, or update code to match RULES.md"
  exit 1
fi
