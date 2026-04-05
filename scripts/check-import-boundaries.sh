#!/bin/bash
# Check that /src/engine and /src/enchub do not import harness code

set -e

# Check engine module
ENGINE_FILES=$(find src/engine -type f -name "*.go" | grep -v _test.go)
# Check enchub app
ENCHUB_FILES=$(find src/enchub -type f -name "*.go" | grep -v _test.go)

VIOLATIONS=0
for file in $ENGINE_FILES $ENCHUB_FILES; do
  if grep -q "harness\|/src/harness" "$file" 2>/dev/null; then
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
