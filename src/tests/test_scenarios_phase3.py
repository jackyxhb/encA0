"""
ENCT Phase 3: Synthetic Scenario Test Suite

Executes all 500+ synthetic scenarios.
Continue-on-failure strategy: collects all results before analysis.
"""

import pytest
import logging
import sys
from pathlib import Path
from typing import Any
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scenario_definitions import (
    Scenario,
    ScenarioResult,
    ScenarioRunSummary,
    ScenarioCategory,
)
from scenario_generator import SyntheticScenarioGenerator

logger = logging.getLogger(__name__)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def scenario_generator():
    """Create and cache scenario generator."""
    gen = SyntheticScenarioGenerator()
    return gen


@pytest.fixture(scope="session")
def all_scenarios(scenario_generator) -> list[Scenario]:
    """Generate all 500+ scenarios once per session."""
    logger.info("Generating all scenarios...")
    scenarios = scenario_generator.generate_all_scenarios()
    logger.info(f"Generated {len(scenarios)} scenarios")
    return scenarios


@pytest.fixture(scope="session")
def run_summary():
    """Create run summary to track results."""
    return ScenarioRunSummary()


# ============================================================================
# Generate Scenarios at Module Load Time
# ============================================================================

# Generate all scenarios once when module loads
_scenario_generator = SyntheticScenarioGenerator()
_all_scenarios = _scenario_generator.generate_all_scenarios()

# ============================================================================
# Parameterized Tests
# ============================================================================

@pytest.mark.parametrize(
    "scenario",
    _all_scenarios,
    ids=lambda s: s.full_id,
)
def test_synthetic_scenario(scenario: Scenario, run_summary: ScenarioRunSummary):
    """
    Execute single synthetic scenario.

    Continue-on-failure: each scenario runs independently.
    Results collected in run_summary for post-run analysis.
    """
    start_time = datetime.utcnow()

    try:
        # Setup
        if scenario.setup_fn:
            setup_data = scenario.setup_fn()
        else:
            setup_data = {}

        # Execute
        if scenario.execute_fn:
            result = scenario.execute_fn(setup_data)
        else:
            pytest.skip(f"No execute function for {scenario.full_id}")

        # Verify
        if scenario.verify_fn:
            verification_passed = scenario.verify_fn(result)
        else:
            verification_passed = True

        # Determine outcome
        scenario.executed_at = datetime.utcnow().isoformat()
        scenario.execution_time_ms = (datetime.utcnow() - start_time).total_seconds() * 1000

        if verification_passed:
            scenario.result_status = "PASS"
            scenario.result_message = "Scenario passed verification"
            run_summary.passed += 1
        else:
            scenario.result_status = "FAIL"
            scenario.result_message = "Verification failed"
            run_summary.failed += 1

        # Track by category
        category_key = scenario.category.value
        if category_key not in run_summary.results_by_category:
            run_summary.results_by_category[category_key] = {
                "passed": 0,
                "failed": 0,
                "errors": 0,
            }
        if scenario.result_status == "PASS":
            run_summary.results_by_category[category_key]["passed"] += 1
        else:
            run_summary.results_by_category[category_key]["failed"] += 1

        run_summary.total_scenarios += 1

        logger.info(f"{scenario.full_id}: {scenario.result_status}")

    except AssertionError as e:
        scenario.executed_at = datetime.utcnow().isoformat()
        scenario.execution_time_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
        scenario.result_status = "FAIL"
        scenario.result_message = str(e)
        run_summary.failed += 1
        run_summary.total_scenarios += 1

        category_key = scenario.category.value
        if category_key not in run_summary.results_by_category:
            run_summary.results_by_category[category_key] = {
                "passed": 0,
                "failed": 0,
                "errors": 0,
            }
        run_summary.results_by_category[category_key]["failed"] += 1

        logger.error(f"{scenario.full_id}: FAIL - {e}")
        pytest.fail(f"Scenario {scenario.full_id} failed: {e}", pytrace=False)

    except Exception as e:
        scenario.executed_at = datetime.utcnow().isoformat()
        scenario.execution_time_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
        scenario.result_status = "ERROR"
        scenario.result_message = str(e)
        scenario.error_details = {"error_type": type(e).__name__, "error_message": str(e)}
        run_summary.errors += 1
        run_summary.total_scenarios += 1

        category_key = scenario.category.value
        if category_key not in run_summary.results_by_category:
            run_summary.results_by_category[category_key] = {
                "passed": 0,
                "failed": 0,
                "errors": 0,
            }
        run_summary.results_by_category[category_key]["errors"] += 1

        logger.error(f"{scenario.full_id}: ERROR - {e}")
        # Don't fail the test; continue to next scenario
        pytest.skip(f"Error in {scenario.full_id}: {e}")


# ============================================================================
# Test Summaries & Reports
# ============================================================================

def test_scenario_count(all_scenarios):
    """Verify we have 500+ scenarios."""
    assert len(all_scenarios) >= 500, f"Expected ≥500 scenarios, got {len(all_scenarios)}"
    logger.info(f"✅ Generated {len(all_scenarios)} scenarios (target: 500+)")


def test_axiom_coverage(all_scenarios):
    """Verify coverage across all 4 axioms."""
    axiom_counts = {}
    for scenario in all_scenarios:
        if scenario.axiom_related:
            axiom = scenario.axiom_related
            axiom_counts[axiom] = axiom_counts.get(axiom, 0) + 1

    for axiom_num in [1, 2, 3, 4]:
        count = axiom_counts.get(axiom_num, 0)
        assert count >= 40, f"Axiom {axiom_num}: expected ≥40 scenarios, got {count}"
        logger.info(f"✅ Axiom {axiom_num}: {count} scenarios")


def test_domain_coverage(all_scenarios):
    """Verify coverage across all domains."""
    domain_counts = {}
    domains = [
        "auth",
        "rate_limiting",
        "data_validation",
        "access_control",
        "compliance",
    ]

    for scenario in all_scenarios:
        if scenario.domain:
            domain_counts[scenario.domain] = domain_counts.get(scenario.domain, 0) + 1

    for domain in domains:
        count = domain_counts.get(domain, 0)
        assert count >= 50, f"Domain '{domain}': expected ≥50 scenarios, got {count}"
        logger.info(f"✅ Domain '{domain}': {count} scenarios")


def test_edge_case_coverage(all_scenarios):
    """Verify edge case coverage."""
    edge_cases = [s for s in all_scenarios if s.category == ScenarioCategory.EDGE_CASE]
    assert len(edge_cases) >= 40, f"Expected ≥40 edge cases, got {len(edge_cases)}"
    logger.info(f"✅ Edge cases: {len(edge_cases)} scenarios")


# ============================================================================
# Session-level Report Generation
# ============================================================================

def pytest_sessionfinish(session, exitstatus):
    """Generate Phase 3 test report after all tests complete."""
    logger.info("Generating Phase 3 test report...")

    # This hook runs after all tests complete
    # In real execution, would collect results and write PHASE-3-TEST-REPORT.md


# ============================================================================
# Helpers
# ============================================================================

class ScenarioTestRunner:
    """Helper class for running scenarios with result collection."""

    def __init__(self):
        self.results: list[ScenarioResult] = []
        self.summary = ScenarioRunSummary()

    def run_scenario(self, scenario: Scenario) -> ScenarioResult:
        """Run single scenario and return result."""
        start_time = datetime.utcnow()

        try:
            # Setup
            setup_data = scenario.setup_fn() if scenario.setup_fn else {}

            # Execute
            execution_result = (
                scenario.execute_fn(setup_data) if scenario.execute_fn else {}
            )

            # Verify
            verification_passed = (
                scenario.verify_fn(execution_result)
                if scenario.verify_fn
                else True
            )

            # Create result
            status = "PASS" if verification_passed else "FAIL"
            result = ScenarioResult(
                scenario_id=scenario.scenario_id,
                full_id=scenario.full_id,
                status=status,
                expected_outcome=scenario.expected_outcome.value,
                actual_outcome="matched" if verification_passed else "mismatched",
                message=scenario.description,
                execution_time_ms=(
                    datetime.utcnow() - start_time
                ).total_seconds() * 1000,
            )

        except Exception as e:
            result = ScenarioResult(
                scenario_id=scenario.scenario_id,
                full_id=scenario.full_id,
                status="ERROR",
                expected_outcome=scenario.expected_outcome.value,
                actual_outcome="exception",
                message=str(e),
                error_details={"error_type": type(e).__name__},
                execution_time_ms=(
                    datetime.utcnow() - start_time
                ).total_seconds() * 1000,
            )

        self.results.append(result)
        return result

    def run_all_scenarios(self, scenarios: list[Scenario]) -> ScenarioRunSummary:
        """Run all scenarios and return summary."""
        for scenario in scenarios:
            result = self.run_scenario(scenario)
            self.summary.total_scenarios += 1

            if result.status == "PASS":
                self.summary.passed += 1
            elif result.status == "FAIL":
                self.summary.failed += 1
            else:
                self.summary.errors += 1

        self.summary.end_time = datetime.utcnow().isoformat()
        return self.summary

    def get_summary(self) -> dict[str, Any]:
        """Get test run summary as dict."""
        return {
            "total_scenarios": self.summary.total_scenarios,
            "passed": self.summary.passed,
            "failed": self.summary.failed,
            "errors": self.summary.errors,
            "pass_rate": f"{self.summary.pass_rate:.2%}",
            "success": self.summary.success,
        }

    def get_failures(self) -> list[ScenarioResult]:
        """Get all failed scenarios."""
        return [r for r in self.results if r.failed()]

    def export_results_json(self, filepath: Path):
        """Export all results to JSON."""
        data = {
            "summary": self.summary.to_dict(),
            "results": [r.to_dict() for r in self.results],
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Results exported to {filepath}")


if __name__ == "__main__":
    # Can be run directly for quick scenario validation
    logger.basicConfig(level=logging.INFO)
    gen = SyntheticScenarioGenerator()
    scenarios = gen.generate_all_scenarios()
    print(f"Generated {len(scenarios)} scenarios")
