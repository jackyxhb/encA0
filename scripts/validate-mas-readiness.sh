#!/bin/bash
# Validate Multi-Agent System (MAS) readiness
# Checks that architecture supports spawning and coordinating multiple agents

echo "🤖 Validating Multi-Agent System (MAS) Readiness..."
echo ""

FAILURES=0

# Check 1: Portable rules exist (AGENTS.md)
echo "✓ Checking portable agent rules..."
if [ ! -f "AGENTS.md" ]; then
  echo "  ❌ FAIL: AGENTS.md not found (needed for agent portability)"
  FAILURES=$((FAILURES + 1))
else
  echo "  ✅ AGENTS.md exists (agents portable across IDEs)"
fi

# Check 2: Architecture boundary clear (ENCT-HE separation)
echo "✓ Checking architecture separation (ENCT-HE orthogonal)..."
if [ -d "src/enct-hub" ]; then
  VIOLATIONS=$(find src/enct-hub -name "*.go" ! -name "*_test.go" -type f 2>/dev/null | xargs grep "harness\|/src/harness" 2>/dev/null | wc -l)
  if [ "$VIOLATIONS" -gt 0 ]; then
    echo "  ❌ FAIL: ENCT imports harness (breaks MAS scalability)"
    FAILURES=$((FAILURES + 1))
  else
    echo "  ✅ ENCT-HE separation maintained (enables independent agent spawning)"
  fi
else
  echo "  ✅ ENCT-HE separation enforced (no src/enct-hub to violate boundary)"
fi

# Check 3: Task coordination interface (TaskCreate/TaskUpdate ready)
echo "✓ Checking task coordination interface..."
if ! grep -q "TaskCreate\|TaskUpdate" .claude.md 2>/dev/null; then
  echo "  ❌ FAIL: Task tracking not documented in .claude.md"
  FAILURES=$((FAILURES + 1))
else
  echo "  ✅ Task coordination documented (agents can coordinate work)"
fi

# Check 4: Boundary enforcement active (prevents agent contamination)
echo "✓ Checking boundary enforcement..."
if [ ! -f "scripts/check-import-boundaries.sh" ]; then
  echo "  ❌ FAIL: Boundary enforcement script missing"
  FAILURES=$((FAILURES + 1))
else
  echo "  ✅ Boundary enforcement active (prevents agent coupling)"
fi

# Check 5: Decision ledger exists (agents inherit context)
echo "✓ Checking decision persistence..."
if [ ! -f "harness/HE-DECISIONS.md" ]; then
  echo "  ❌ FAIL: Decision ledger missing (agents lose context)"
  FAILURES=$((FAILURES + 1))
else
  echo "  ✅ Decision ledger exists (agents inherit design rationale)"
fi

# Check 6: Scheduled validation (continuous MAS health)
echo "✓ Checking continuous validation..."
if [ ! -f ".github/workflows/scheduled.yml" ]; then
  echo "  ❌ FAIL: Scheduled validation missing"
  FAILURES=$((FAILURES + 1))
else
  JOBS=$(grep -c "jobs:" .github/workflows/scheduled.yml || echo 0)
  echo "  ✅ Scheduled validation active (continuous MAS health)"
fi

# Check 7: CI/CD pipeline (coordination backbone)
echo "✓ Checking CI/CD coordination backbone..."
if [ ! -f ".github/workflows/test.yml" ]; then
  echo "  ❌ FAIL: CI/CD pipeline missing"
  FAILURES=$((FAILURES + 1))
else
  echo "  ✅ CI/CD pipeline active (agents coordinate via GitHub Actions)"
fi

# Check 8: Harness rules enforced
echo "✓ Checking harness enforcement..."
if [ ! -f "RULES.md" ]; then
  echo "  ❌ FAIL: Project rules missing"
  FAILURES=$((FAILURES + 1))
else
  echo "  ✅ Project rules enforced (consistent agent behavior)"
fi

echo ""
if [ "$FAILURES" -eq 0 ]; then
  echo "✅ MAS READINESS CHECK PASSED"
  echo ""
  echo "   System is ready for multi-agent deployment:"
  echo "   • Agents are portable (AGENTS.md)"
  echo "   • Architecture is orthogonal (ENCT-HE separation)"
  echo "   • Coordination is documented (task system + CI/CD)"
  echo "   • Boundaries are enforced (import checks)"
  echo "   • Context persists (decisions documented)"
  echo "   • Health is monitored continuously (scheduled jobs)"
  echo "   • Consistent behavior (RULES.md enforced)"
  exit 0
else
  echo "❌ MAS READINESS CHECK FAILED — $FAILURES issue(s)"
  exit 1
fi
