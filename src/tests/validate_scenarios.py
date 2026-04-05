"""
Quick validation: Verify scenario generator creates 500+ scenarios.

Run this to validate Phase 3 test infrastructure before running full test suite.

Usage:
    python validate_scenarios.py
"""

import sys
from pathlib import Path
from collections import defaultdict

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scenario_generator import SyntheticScenarioGenerator
from scenario_definitions import ScenarioCategory


def validate_scenarios():
    """Validate scenario generation."""
    print("=" * 80)
    print("Phase 3 Scenario Generator Validation")
    print("=" * 80)

    # Generate all scenarios
    print("\n[1/3] Generating scenarios...")
    gen = SyntheticScenarioGenerator()
    scenarios = gen.generate_all_scenarios()
    print(f"✅ Generated {len(scenarios)} scenarios (target: ≥500)")

    # Count by category
    print("\n[2/3] Verifying category coverage...")
    category_counts = defaultdict(int)
    domain_counts = defaultdict(int)
    axiom_counts = defaultdict(int)

    for scenario in scenarios:
        category_counts[scenario.category.value] += 1
        if scenario.domain:
            domain_counts[scenario.domain] += 1
        if scenario.axiom_related:
            axiom_counts[scenario.axiom_related] += 1

    # Axiom coverage
    print("\n  Axiom Coverage:")
    for axiom_num in [1, 2, 3, 4]:
        count = axiom_counts.get(axiom_num, 0)
        target = 40
        status = "✅" if count >= target else "❌"
        print(f"    {status} Axiom {axiom_num}: {count}/{target} scenarios")

    # Domain coverage
    print("\n  Domain Coverage:")
    domains = ["auth", "rate_limiting", "data_validation", "access_control", "compliance"]
    for domain in domains:
        count = domain_counts.get(domain, 0)
        target = 50
        status = "✅" if count >= target else "❌"
        print(f"    {status} {domain}: {count}/{target} scenarios")

    # Edge cases
    edge_count = sum(1 for s in scenarios if s.category == ScenarioCategory.EDGE_CASE)
    print(f"\n  Edge Cases:")
    status = "✅" if edge_count >= 40 else "❌"
    print(f"    {status} Edge cases: {edge_count}/40 scenarios")

    # Category summary
    print("\n  Category Summary:")
    for cat_name, count in sorted(category_counts.items()):
        print(f"    • {cat_name}: {count}")

    # Verify all scenarios have required fields
    print("\n[3/3] Validating scenario structure...")
    errors = []
    for scenario in scenarios:
        if not scenario.scenario_id:
            errors.append(f"Missing scenario_id: {scenario}")
        if not scenario.execute_fn:
            errors.append(f"Missing execute_fn: {scenario.scenario_id}")
        if not scenario.verify_fn:
            errors.append(f"Missing verify_fn: {scenario.scenario_id}")

    if errors:
        print("❌ Validation errors found:")
        for error in errors:
            print(f"   - {error}")
        return False

    print("✅ All scenarios have required fields")

    # Final status
    print("\n" + "=" * 80)
    total_valid = len(scenarios)
    if total_valid >= 500:
        print(f"✅ SUCCESS: {total_valid} scenarios ready for Phase 3")
        print("\nNext steps:")
        print("  1. Run: pytest src/tests/test_scenarios_phase3.py -v --continue-on-failure")
        print("  2. Generate: PHASE-3-TEST-REPORT.md")
        print("  3. Analyze failures and rerun if needed")
        return True
    else:
        print(f"❌ FAILURE: Only {total_valid} scenarios (need ≥500)")
        return False


if __name__ == "__main__":
    success = validate_scenarios()
    sys.exit(0 if success else 1)
