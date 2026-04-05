#!/bin/bash
# Detect dead code patterns (unused files, empty stubs, orphaned tests)
# Runs as scheduled CI job (weekly) to fight entropy
# Note: go vet catches unused variables/imports at compile time

set -e

echo "🔎 Scanning for dead code patterns..."
echo ""

WARNINGS=0

# Check 1: Empty functions (stubs without TODO)
echo "✓ Checking for empty function stubs..."
EMPTY_FUNCS=$(find src/enct-hub -name "*.go" -type f | while read f; do
  # Find empty function bodies (func name() { } or func name() {\n})
  grep -c "func.*{[[:space:]]*}$" "$f" 2>/dev/null || echo 0
done | awk '{s+=$1} END {print s}')

if [ "$EMPTY_FUNCS" -gt 0 ]; then
  echo "  ⚠️  WARNING: Found $EMPTY_FUNCS empty function stub(s)"
  echo "      Review: find src/enct-hub -name '*.go' -exec grep 'func.*{}' {} +"
  WARNINGS=$((WARNINGS + 1))
else
  echo "  ✅ No empty function stubs found"
fi

# Check 2: Unused test files (no corresponding .go source)
echo "✓ Checking for orphaned test files..."
ORPHAN_TESTS=$(find src/enct-hub -name "*_test.go" -type f | while read test; do
  base=${test%_test.go}
  if [ ! -f "$base.go" ]; then
    echo "$test"
  fi
done | wc -l)

if [ "$ORPHAN_TESTS" -gt 0 ]; then
  echo "  ⚠️  WARNING: Found $ORPHAN_TESTS orphaned test file(s)"
  echo "      Review: find src/enct-hub -name '*_test.go' -type f"
  WARNINGS=$((WARNINGS + 1))
else
  echo "  ✅ No orphaned test files"
fi

# Check 3: Commented-out code blocks (dead code indicator)
echo "✓ Checking for large commented code blocks..."
LARGE_COMMENTS=$(find src/enct-hub -name "*.go" -type f | while read f; do
  # Count lines with //, /*, */ patterns
  grep -c "^[[:space:]]*//" "$f" 2>/dev/null || echo 0
done | awk '{if($1 > 10) c++} END {print c}')

if [ "$LARGE_COMMENTS" -gt 0 ]; then
  echo "  ⚠️  WARNING: $LARGE_COMMENTS file(s) have large commented blocks"
  echo "      Review and either delete or uncomment"
  WARNINGS=$((WARNINGS + 1))
else
  echo "  ✅ No large commented code blocks detected"
fi

# Check 4: Files with only imports (stubs)
echo "✓ Checking for stub files (imports only)..."
STUB_FILES=$(find src/enct-hub -name "*.go" ! -name "*_test.go" -type f | while read f; do
  lines=$(wc -l < "$f")
  imports=$(grep -c "^import" "$f" || echo 0)
  # If file < 20 lines and has imports, might be a stub
  if [ "$lines" -lt 20 ] && [ "$imports" -gt 0 ]; then
    funcs=$(grep -c "^func " "$f" || echo 0)
    if [ "$funcs" -eq 0 ]; then
      echo "$f"
    fi
  fi
done | wc -l)

if [ "$STUB_FILES" -gt 0 ]; then
  echo "  ⚠️  WARNING: Found $STUB_FILES potential stub file(s)"
  echo "      Review: find src/enct-hub -name '*.go' ! -name '*_test.go' -type f"
  WARNINGS=$((WARNINGS + 1))
else
  echo "  ✅ No stub files detected"
fi

echo ""
if [ "$WARNINGS" -eq 0 ]; then
  echo "✅ Dead code scan complete — no issues found"
  exit 0
else
  echo "⚠️  Dead code scan found $WARNINGS warning(s)"
  echo ""
  echo "Note: This is informational (exit code 0). Check regularly:"
  echo "  • Implement empty stubs or remove them"
  echo "  • Delete orphaned test files"
  echo "  • Remove dead commented code"
  echo ""
  exit 0
fi
