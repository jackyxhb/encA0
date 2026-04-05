"""
Unit Tests for ENCT Indicator Calculation Engine

Tests verify:
- Determinism: same cycle state → same indicator values
- All 8 indicators calculate correctly from cycle state
- Edge cases handled properly
- Trend analysis works
- Health scores computed correctly

Target: >95% code coverage of indicator calculator.
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from enct.indicators import (
    IndicatorName,
    IndicatorSnapshot,
    IndicatorCalculator,
    INDICATOR_DEFINITIONS,
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def indicator_calculator():
    """Create IndicatorCalculator instance."""
    return IndicatorCalculator()


@pytest.fixture
def complete_cycle_state():
    """Complete successful cycle state with all phases."""
    return {
        "cycle_id": "cycle_123",
        "status": "complete",
        "current_phase": "complete",
        "sense_output": {
            "timestamp": "2026-04-05T10:30:00Z",
            "observations": {"system_load": 0.65},
            "policy_request": {"domain": "auth", "constraint": "confidence > 0.75"},
        },
        "validate_output": {
            "timestamp": "2026-04-05T10:30:01Z",
            "constraint_checks": {"immutability": True, "enforceability": True, "determinism": True},
            "confidence": 0.85,
            "uncertainty_bounds": {
                "epistemic_lower": 0.80,
                "epistemic_upper": 0.90,
                "aleatoric": 0.03,
            },
            "passed": True,
        },
        "execute_output": {
            "timestamp": "2026-04-05T10:30:02Z",
            "action_taken": "activate_policy",
            "outcome": "POLICY_ACTIVATED",
            "side_effects": ["Constraint added", "Version incremented"],
        },
        "assess_output": {
            "timestamp": "2026-04-05T10:30:03Z",
            "metrics": {
                "compliance_rate": 0.95,
                "homeostasis_score": 0.88,
            },
            "violations_detected": [],
            "system_health": 0.88,
        },
        "reenact_output": {
            "timestamp": "2026-04-05T10:30:04Z",
            "adaptations_made": [],
            "version_updated": False,
            "rollback_decision": None,
        },
    }


@pytest.fixture
def failed_validation_cycle_state():
    """Cycle state that fails validation (Axiom 1 violation)."""
    return {
        "cycle_id": "cycle_456",
        "status": "axiom_violation",
        "current_phase": "validate",
        "sense_output": {
            "timestamp": "2026-04-05T10:31:00Z",
            "observations": {"system_load": 0.72},
            "policy_request": {"action": "disable axiom enforcement"},
        },
        "validate_output": None,
        "execute_output": None,
        "assess_output": None,
        "reenact_output": None,
    }


@pytest.fixture
def partial_cycle_state():
    """Cycle state that completed Execute but not Assess/Re-enact."""
    return {
        "cycle_id": "cycle_789",
        "status": "complete",
        "sense_output": {"timestamp": "2026-04-05T10:32:00Z"},
        "validate_output": {
            "passed": True,
            "confidence": 0.75,
            "constraint_checks": {"test": True},
        },
        "execute_output": {
            "timestamp": "2026-04-05T10:32:02Z",
            "action_taken": "test_action",
            "outcome": "SUCCESS",
        },
        "assess_output": None,
        "reenact_output": None,
    }


# ============================================================================
# Test: Indicator Definitions
# ============================================================================

class TestIndicatorDefinitions:
    """Test indicator definitions are complete and consistent."""

    def test_all_8_indicators_defined(self):
        """All 8 indicators should be defined."""
        assert len(INDICATOR_DEFINITIONS) == 8

    def test_each_indicator_has_definition(self):
        """Each indicator name should have a definition."""
        for name in IndicatorName:
            assert name in INDICATOR_DEFINITIONS

    def test_indicator_targets_are_valid(self):
        """Target thresholds should be logical."""
        for name, defn in INDICATOR_DEFINITIONS.items():
            # Min should be <= max
            assert defn.target_min <= defn.target_max
            # Critical should be < warning (approximately)
            if name != IndicatorName.AXIOM_VIOLATION_RATE:  # This one is special
                assert defn.critical_threshold <= defn.warning_threshold


# ============================================================================
# Test: Determinism
# ============================================================================

class TestIndicatorDeterminism:
    """Test indicators are deterministic: same input → same output."""

    def test_same_cycle_state_yields_same_indicators(
        self,
        indicator_calculator,
        complete_cycle_state
    ):
        """Same cycle state should produce identical indicator values."""
        snap1 = indicator_calculator.calculate_snapshot("cycle_1", complete_cycle_state)
        snap2 = indicator_calculator.calculate_snapshot("cycle_1", complete_cycle_state)

        # All indicators should match exactly
        assert snap1.compliance_rate == snap2.compliance_rate
        assert snap1.homeostasis_score == snap2.homeostasis_score
        assert snap1.traceability_coverage == snap2.traceability_coverage
        assert snap1.bootstrap_confidence == snap2.bootstrap_confidence
        assert snap1.adaptation_resilience == snap2.adaptation_resilience
        assert snap1.provenance_overhead == snap2.provenance_overhead
        assert snap1.axiom_violation_rate == snap2.axiom_violation_rate
        assert snap1.policy_rollback_rate == snap2.policy_rollback_rate

    def test_multiple_calculations_are_reproducible(
        self,
        indicator_calculator,
        complete_cycle_state
    ):
        """Running indicator calculation 100x on same state should produce identical values."""
        first_snapshot = indicator_calculator.calculate_snapshot("cycle", complete_cycle_state)

        for _ in range(100):
            snapshot = indicator_calculator.calculate_snapshot("cycle", complete_cycle_state)
            assert snapshot.compliance_rate == first_snapshot.compliance_rate
            assert snapshot.homeostasis_score == first_snapshot.homeostasis_score
            assert snapshot.bootstrap_confidence == first_snapshot.bootstrap_confidence


# ============================================================================
# Test: Individual Indicator Calculations
# ============================================================================

class TestIndicatorCalculations:
    """Test each of the 8 indicators calculates correctly."""

    def test_compliance_rate_with_passed_validation(self, indicator_calculator):
        """Compliance rate should be 1.0 when validation passes."""
        state = {
            "validate_output": {"passed": True},
        }
        snap = indicator_calculator.calculate_snapshot("cycle", state)
        assert snap.compliance_rate == 1.0

    def test_compliance_rate_with_failed_validation(self, indicator_calculator):
        """Compliance rate should be 0.0 when validation fails."""
        state = {
            "validate_output": {"passed": False},
        }
        snap = indicator_calculator.calculate_snapshot("cycle", state)
        assert snap.compliance_rate == 0.0

    def test_compliance_rate_with_no_validation(self, indicator_calculator):
        """Compliance rate should be 0.0 if no validation output."""
        state = {}
        snap = indicator_calculator.calculate_snapshot("cycle", state)
        assert snap.compliance_rate == 0.0

    def test_homeostasis_score_all_constraints_pass(self, indicator_calculator):
        """Homeostasis should be 1.0 when all constraints pass."""
        state = {
            "validate_output": {
                "constraint_checks": {"c1": True, "c2": True, "c3": True},
            }
        }
        snap = indicator_calculator.calculate_snapshot("cycle", state)
        assert snap.homeostasis_score == 1.0

    def test_homeostasis_score_partial_constraints_pass(self, indicator_calculator):
        """Homeostasis should reflect proportion of passing constraints."""
        state = {
            "validate_output": {
                "constraint_checks": {"c1": True, "c2": False, "c3": True},
            }
        }
        snap = indicator_calculator.calculate_snapshot("cycle", state)
        assert snap.homeostasis_score == pytest.approx(2.0 / 3.0, abs=0.01)

    def test_homeostasis_score_no_constraints(self, indicator_calculator):
        """Homeostasis should be 1.0 if no constraints."""
        state = {
            "validate_output": {"constraint_checks": {}},
        }
        snap = indicator_calculator.calculate_snapshot("cycle", state)
        assert snap.homeostasis_score == 1.0

    def test_traceability_coverage_with_execute(self, indicator_calculator):
        """Traceability should be 1.0 when Execute phase completes."""
        state = {
            "execute_output": {"action_taken": "test", "outcome": "SUCCESS"},
        }
        snap = indicator_calculator.calculate_snapshot("cycle", state)
        assert snap.traceability_coverage == 1.0

    def test_traceability_coverage_without_execute(self, indicator_calculator):
        """Traceability should be 0.0 if no Execute phase."""
        state = {}
        snap = indicator_calculator.calculate_snapshot("cycle", state)
        assert snap.traceability_coverage == 0.0

    def test_bootstrap_confidence_uses_validate_confidence(self, indicator_calculator):
        """Bootstrap confidence should match validation confidence."""
        state = {
            "validate_output": {"confidence": 0.82},
        }
        snap = indicator_calculator.calculate_snapshot("cycle", state)
        assert snap.bootstrap_confidence == pytest.approx(0.82, abs=0.01)

    def test_bootstrap_confidence_no_validation(self, indicator_calculator):
        """Bootstrap confidence should be 0.0 if no validation."""
        state = {}
        snap = indicator_calculator.calculate_snapshot("cycle", state)
        assert snap.bootstrap_confidence == 0.0

    def test_adaptation_resilience_no_adaptations(self, indicator_calculator):
        """Resilience should be 1.0 if no adaptations needed."""
        state = {
            "reenact_output": {"adaptations_made": []},
        }
        snap = indicator_calculator.calculate_snapshot("cycle", state)
        assert snap.adaptation_resilience == 1.0

    def test_adaptation_resilience_with_adaptations(self, indicator_calculator):
        """Resilience should be 1.0 if all adaptations succeed."""
        state = {
            "reenact_output": {"adaptations_made": ["adapt1", "adapt2"]},
        }
        snap = indicator_calculator.calculate_snapshot("cycle", state)
        assert snap.adaptation_resilience == 1.0

    def test_axiom_violation_rate_no_violation(self, indicator_calculator):
        """Violation rate should be 0.0 if no axiom violations."""
        state = {"status": "complete"}
        snap = indicator_calculator.calculate_snapshot("cycle", state)
        assert snap.axiom_violation_rate == 0.0

    def test_axiom_violation_rate_with_violation(self, indicator_calculator):
        """Violation rate should be 1.0 if axiom violation detected."""
        state = {"status": "axiom_violation"}
        snap = indicator_calculator.calculate_snapshot("cycle", state)
        assert snap.axiom_violation_rate == 1.0

    def test_policy_rollback_rate_no_rollback(self, indicator_calculator):
        """Rollback rate should be 0.0 if no rollback."""
        state = {
            "reenact_output": {"rollback_decision": None},
        }
        snap = indicator_calculator.calculate_snapshot("cycle", state)
        assert snap.policy_rollback_rate == 0.0

    def test_policy_rollback_rate_with_rollback(self, indicator_calculator):
        """Rollback rate should be 1.0 if rollback triggered."""
        state = {
            "reenact_output": {"rollback_decision": "rolled_back_policy_v1"},
        }
        snap = indicator_calculator.calculate_snapshot("cycle", state)
        assert snap.policy_rollback_rate == 1.0

    def test_provenance_overhead_scaled_to_phases(self, indicator_calculator):
        """Provenance overhead should scale with phase count."""
        # Minimal phases
        state_minimal = {
            "sense_output": {},
            "validate_output": None,
        }
        snap_minimal = indicator_calculator.calculate_snapshot("cycle", state_minimal)

        # All phases
        state_full = {
            "sense_output": {},
            "validate_output": {},
            "execute_output": {},
            "assess_output": {},
            "reenact_output": {},
        }
        snap_full = indicator_calculator.calculate_snapshot("cycle", state_full)

        # Full should have higher overhead
        assert snap_full.provenance_overhead > snap_minimal.provenance_overhead


# ============================================================================
# Test: Snapshot Operations
# ============================================================================

class TestIndicatorSnapshot:
    """Test IndicatorSnapshot data structure and operations."""

    def test_snapshot_to_dict(self, indicator_calculator, complete_cycle_state):
        """Snapshot should serialize to dict."""
        snap = indicator_calculator.calculate_snapshot("cycle", complete_cycle_state)
        snap_dict = snap.to_dict()

        assert isinstance(snap_dict, dict)
        assert "cycle_id" in snap_dict
        assert "timestamp" in snap_dict
        assert "indicators" in snap_dict

    def test_snapshot_get_indicator(self, indicator_calculator, complete_cycle_state):
        """Should retrieve individual indicator by name."""
        snap = indicator_calculator.calculate_snapshot("cycle", complete_cycle_state)

        compliance = snap.get_indicator(IndicatorName.COMPLIANCE_RATE)
        assert isinstance(compliance, float)
        assert 0.0 <= compliance <= 1.0

    def test_snapshot_all_indicators(self, indicator_calculator, complete_cycle_state):
        """Should get all indicators as dict."""
        snap = indicator_calculator.calculate_snapshot("cycle", complete_cycle_state)
        all_ind = snap.all_indicators()

        assert len(all_ind) == 8
        assert all(isinstance(v, float) for v in all_ind.values())

    def test_snapshot_health_score(self, indicator_calculator, complete_cycle_state):
        """Health score should be average of all indicators."""
        snap = indicator_calculator.calculate_snapshot("cycle", complete_cycle_state)
        health = snap.health_score()

        assert 0.0 <= health <= 1.0
        # Manually verify it's the average
        all_ind = snap.all_indicators()
        expected_health = sum(all_ind.values()) / len(all_ind)
        assert health == pytest.approx(expected_health, abs=0.01)

    def test_snapshot_check_violations(self, indicator_calculator, complete_cycle_state):
        """Should detect indicators below warning threshold."""
        snap = indicator_calculator.calculate_snapshot("cycle", complete_cycle_state)
        violations = snap.check_violations()

        assert isinstance(violations, dict)
        assert len(violations) == 8
        # Most should not be violated in a complete cycle
        violated = sum(1 for v in violations.values() if v)
        assert violated <= 2


# ============================================================================
# Test: Edge Cases
# ============================================================================

class TestIndicatorEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_cycle_state(self, indicator_calculator):
        """Empty cycle state should not crash."""
        snap = indicator_calculator.calculate_snapshot("cycle", {})
        assert snap is not None
        assert snap.compliance_rate == 0.0

    def test_none_values_in_state(self, indicator_calculator):
        """None values in state should be handled."""
        state = {
            "validate_output": None,
            "execute_output": None,
        }
        snap = indicator_calculator.calculate_snapshot("cycle", state)
        assert snap is not None

    def test_missing_fields_in_outputs(self, indicator_calculator):
        """Missing fields in phase outputs should be handled."""
        state = {
            "validate_output": {},  # Missing 'passed' field
        }
        snap = indicator_calculator.calculate_snapshot("cycle", state)
        assert snap.compliance_rate == 0.0

    def test_axiom_violation_state(self, indicator_calculator, failed_validation_cycle_state):
        """Cycle that fails with axiom violation should handle gracefully."""
        snap = indicator_calculator.calculate_snapshot("cycle", failed_validation_cycle_state)
        assert snap.compliance_rate == 0.0
        assert snap.axiom_violation_rate == 1.0


# ============================================================================
# Test: Completeness
# ============================================================================

class TestIndicatorCompleteness:
    """Test that all indicators are calculated in every snapshot."""

    def test_complete_cycle_snapshot_has_all_indicators(
        self,
        indicator_calculator,
        complete_cycle_state
    ):
        """Complete cycle should calculate all 8 indicators."""
        snap = indicator_calculator.calculate_snapshot("cycle", complete_cycle_state)

        assert snap.compliance_rate is not None
        assert snap.homeostasis_score is not None
        assert snap.traceability_coverage is not None
        assert snap.bootstrap_confidence is not None
        assert snap.adaptation_resilience is not None
        assert snap.provenance_overhead is not None
        assert snap.axiom_violation_rate is not None
        assert snap.policy_rollback_rate is not None

    def test_failed_cycle_snapshot_has_all_indicators(
        self,
        indicator_calculator,
        failed_validation_cycle_state
    ):
        """Failed cycle should still calculate all 8 indicators."""
        snap = indicator_calculator.calculate_snapshot("cycle", failed_validation_cycle_state)

        # All should be present (even if 0.0)
        assert snap.compliance_rate is not None
        assert snap.axiom_violation_rate is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src/enct/indicators", "--cov-report=term-missing"])
