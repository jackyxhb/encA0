#!/bin/bash
# Check that /src/enct-hub does not import /src/harness/

set -e

ENCT_FILES=$(find /Users/macbook1/work/ENCT/encA0/src/enct-hub -type f -name "*.go" | grep -v _test.go)

VIOLATIONS=0
for file in $ENCT_FILES; do
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
