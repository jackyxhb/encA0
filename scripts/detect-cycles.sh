#!/bin/bash
# Detect circular dependencies in Go code
# Prevents architectural debt before it compounds

set -e

echo "🔄 Checking for circular dependencies..."
echo ""

# Use Go's built-in cycle detection
echo "✓ Analyzing import graph..."
cd src/enct-hub

# Check if any packages import each other (circular)
CYCLES=$(go list -deps ./... 2>&1 | grep -i "cycle\|circular" | wc -l)

if [ "$CYCLES" -gt 0 ]; then
  echo "  ❌ FAIL: Circular dependencies detected"
  echo ""
  go list -deps ./... 2>&1 | grep -i "cycle\|circular" || true
  exit 1
else
  echo "  ✅ No circular dependencies found"
fi

# Verify boundary separation (ENCT cannot import harness)
echo "✓ Verifying architectural boundaries..."
cd ..
VIOLATIONS=$(find src/enct-hub -name "*.go" ! -name "*_test.go" -type f | xargs grep "harness\|/src/harness" | wc -l)

if [ "$VIOLATIONS" -gt 0 ]; then
  echo "  ❌ FAIL: Architecture boundary violations"
  exit 1
else
  echo "  ✅ ENCT-HE boundary maintained"
fi

echo ""
echo "✅ Dependency analysis complete — no cycles detected"
exit 0
