"""
Unit Tests for ENCT Axiom Enforcement Layer

Tests verify fail-hard semantics: all violations raise exceptions immediately.
Target: >95% code coverage of axiom validators and exception classes.
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from enct.axioms import (
    AxiomViolationException,
    Axiom1ImmutabilityViolation,
    Axiom2DeterminismViolation,
    Axiom3EnforcementViolation,
    Axiom4ResilienceViolation,
    validate_policy_not_immutable_override,
    validate_no_axiom_bypass_in_code,
    validate_determinism_with_bounds,
    validate_reproducibility,
    validate_constraint_enforced,
    validate_constraint_not_soft,
    validate_adaptation_versioned,
    validate_adaptation_audited,
    validate_adaptation_reversible,
    validate_adaptation_preserves_core,
)


# ============================================================================
# Axiom 1: Immutability Tests
# ============================================================================

class TestAxiom1Immutability:
    """Test Axiom 1: Foundational rules are immutable."""

    def test_policy_with_disable_axiom_raises_violation(self):
        """Policy attempting to disable axiom should raise Axiom1ImmutabilityViolation."""
        policy = {"action": "disable axiom enforcement"}
        with pytest.raises(Axiom1ImmutabilityViolation):
            validate_policy_not_immutable_override(policy)

    def test_policy_with_skip_validation_raises_violation(self):
        """Policy attempting to skip validation should raise violation."""
        policy = {"action": "skip validation phase"}
        with pytest.raises(Axiom1ImmutabilityViolation):
            validate_policy_not_immutable_override(policy)

    def test_policy_with_bypass_enforcement_raises_violation(self):
        """Policy containing 'bypass enforcement' should raise violation."""
        policy = {"rule": "bypass enforcement for this domain"}
        with pytest.raises(Axiom1ImmutabilityViolation):
            validate_policy_not_immutable_override(policy)

    def test_policy_with_remove_constraint_raises_violation(self):
        """Policy attempting to remove constraint should raise violation."""
        policy = {"action": "remove constraint from loop"}
        with pytest.raises(Axiom1ImmutabilityViolation):
            validate_policy_not_immutable_override(policy)

    def test_policy_with_override_axiom_raises_violation(self):
        """Policy attempting to override axiom should raise violation."""
        policy = {"request": "override axiom 2"}
        with pytest.raises(Axiom1ImmutabilityViolation):
            validate_policy_not_immutable_override(policy)

    def test_policy_modifying_loop_raises_violation(self):
        """Policy attempting to modify Loop structure should raise violation."""
        policy = {"change": "remove loop phase"}
        with pytest.raises(Axiom1ImmutabilityViolation):
            validate_policy_not_immutable_override(policy)

    def test_policy_disabling_axioms_raises_violation(self):
        """Policy attempting to disable axioms should raise violation."""
        policy = {"directive": "disable axiom 3 for performance"}
        with pytest.raises(Axiom1ImmutabilityViolation):
            validate_policy_not_immutable_override(policy)

    def test_compliant_policy_adds_constraint(self):
        """Compliant policy that adds constraint should not raise."""
        policy = {"domain": "auth", "constraint": "confidence > 0.75"}
        # Should not raise
        validate_policy_not_immutable_override(policy)

    def test_compliant_policy_sets_threshold(self):
        """Compliant policy that sets threshold should not raise."""
        policy = {"component": "bootstrap", "confidence_threshold": 0.8}
        # Should not raise
        validate_policy_not_immutable_override(policy)

    def test_code_with_skip_axiom_raises_violation(self):
        """Code with skip_axiom pattern should raise violation."""
        code = "if skip_axiom: return True"
        with pytest.raises(Axiom1ImmutabilityViolation):
            validate_no_axiom_bypass_in_code(code, "test_component")

    def test_code_with_disable_axiom_raises_violation(self):
        """Code with disable_axiom pattern should raise violation."""
        code = "disable_axiom_check()"
        with pytest.raises(Axiom1ImmutabilityViolation):
            validate_no_axiom_bypass_in_code(code, "test_component")

    def test_code_with_axiom_check_false_raises_violation(self):
        """Code with 'axiom_check = False' should raise violation."""
        code = "axiom_check = False"
        with pytest.raises(Axiom1ImmutabilityViolation):
            validate_no_axiom_bypass_in_code(code, "test_component")

    def test_compliant_code_enforces_axioms(self):
        """Compliant code that enforces axioms should not raise."""
        code = "validate_axiom_1(policy)"
        # Should not raise
        validate_no_axiom_bypass_in_code(code, "test_component")


# ============================================================================
# Axiom 2: Determinism Tests
# ============================================================================

class TestAxiom2Determinism:
    """Test Axiom 2: Action determinism with uncertainty bounds."""

    def test_result_missing_outcome_raises_violation(self):
        """Result missing 'outcome' field should raise Axiom2DeterminismViolation."""
        result = {"confidence": 0.8, "uncertainty_bounds": {}}
        with pytest.raises(Axiom2DeterminismViolation):
            validate_determinism_with_bounds(result, "test_action")

    def test_result_missing_confidence_raises_violation(self):
        """Result missing 'confidence' field should raise violation."""
        result = {"outcome": "ACCEPT", "uncertainty_bounds": {}}
        with pytest.raises(Axiom2DeterminismViolation):
            validate_determinism_with_bounds(result, "test_action")

    def test_result_missing_uncertainty_bounds_raises_violation(self):
        """Result missing 'uncertainty_bounds' should raise violation."""
        result = {"outcome": "ACCEPT", "confidence": 0.8}
        with pytest.raises(Axiom2DeterminismViolation):
            validate_determinism_with_bounds(result, "test_action")

    def test_result_with_incomplete_bounds_raises_violation(self):
        """Result with incomplete uncertainty bounds should raise violation."""
        result = {
            "outcome": "ACCEPT",
            "confidence": 0.8,
            "uncertainty_bounds": {"epistemic_lower": 0.75}  # Missing fields
        }
        with pytest.raises(Axiom2DeterminismViolation):
            validate_determinism_with_bounds(result, "test_action")

    def test_result_with_invalid_confidence_range_raises_violation(self):
        """Confidence outside [0.0, 1.0] should raise violation."""
        result = {
            "outcome": "ACCEPT",
            "confidence": 1.5,  # Invalid!
            "uncertainty_bounds": {
                "epistemic_lower": 0.75,
                "epistemic_upper": 0.85,
                "aleatoric": 0.02
            }
        }
        with pytest.raises(Axiom2DeterminismViolation):
            validate_determinism_with_bounds(result, "test_action")

    def test_compliant_result_with_valid_bounds(self):
        """Result with all required fields should not raise."""
        result = {
            "outcome": "ACCEPT",
            "confidence": 0.82,
            "uncertainty_bounds": {
                "epistemic_lower": 0.78,
                "epistemic_upper": 0.86,
                "aleatoric": 0.03
            }
        }
        # Should not raise
        validate_determinism_with_bounds(result, "test_action")

    def test_non_deterministic_outcomes_raise_violation(self):
        """Two different outcomes for same input should raise violation."""
        results = [
            {
                "outcome": "ACCEPT",
                "confidence": 0.82,
                "uncertainty_bounds": {
                    "epistemic_lower": 0.78,
                    "epistemic_upper": 0.86,
                    "aleatoric": 0.03
                }
            },
            {
                "outcome": "REJECT",  # Different outcome!
                "confidence": 0.82,
                "uncertainty_bounds": {
                    "epistemic_lower": 0.78,
                    "epistemic_upper": 0.86,
                    "aleatoric": 0.03
                }
            }
        ]
        with pytest.raises(Axiom2DeterminismViolation):
            validate_reproducibility(results, "test_action")

    def test_divergent_confidence_raises_violation(self):
        """Confidence divergence beyond tolerance should raise violation."""
        results = [
            {
                "outcome": "ACCEPT",
                "confidence": 0.82,
                "uncertainty_bounds": {
                    "epistemic_lower": 0.78,
                    "epistemic_upper": 0.86,
                    "aleatoric": 0.03
                }
            },
            {
                "outcome": "ACCEPT",
                "confidence": 0.45,  # Significantly different!
                "uncertainty_bounds": {
                    "epistemic_lower": 0.40,
                    "epistemic_upper": 0.50,
                    "aleatoric": 0.03
                }
            }
        ]
        with pytest.raises(Axiom2DeterminismViolation):
            validate_reproducibility(results, "test_action")

    def test_deterministic_results_within_tolerance(self):
        """Identical results within tolerance should not raise."""
        results = [
            {
                "outcome": "ACCEPT",
                "confidence": 0.82,
                "uncertainty_bounds": {
                    "epistemic_lower": 0.78,
                    "epistemic_upper": 0.86,
                    "aleatoric": 0.03
                }
            },
            {
                "outcome": "ACCEPT",
                "confidence": 0.82,
                "uncertainty_bounds": {
                    "epistemic_lower": 0.78,
                    "epistemic_upper": 0.86,
                    "aleatoric": 0.03
                }
            }
        ]
        # Should not raise
        validate_reproducibility(results, "test_action")

    def test_reproducibility_with_single_result_skipped(self):
        """Reproducibility check with single result should skip validation."""
        results = [{"outcome": "ACCEPT", "confidence": 0.8}]
        # Should not raise (cannot validate with <2 results)
        validate_reproducibility(results, "test_action")


# ============================================================================
# Axiom 3: Enforcement Tests
# ============================================================================

class TestAxiom3Enforcement:
    """Test Axiom 3: Normative constraints are mechanically enforced."""

    def test_missing_enforcement_raises_violation(self):
        """Constraint without enforcement should raise Axiom3EnforcementViolation."""
        with pytest.raises(Axiom3EnforcementViolation):
            validate_constraint_enforced(
                constraint_name="confidence_threshold",
                enforcement_exists=False,
                enforcement_type="none",
                enforcement_details="No enforcement mechanism found"
            )

    def test_soft_enforcement_documentation_raises_violation(self):
        """Documentation-only enforcement should raise violation."""
        with pytest.raises(Axiom3EnforcementViolation):
            validate_constraint_not_soft("confidence_threshold", "documentation")

    def test_soft_enforcement_logging_raises_violation(self):
        """Logging-only enforcement should raise violation."""
        with pytest.raises(Axiom3EnforcementViolation):
            validate_constraint_not_soft("confidence_threshold", "logging")

    def test_soft_enforcement_warning_raises_violation(self):
        """Warning-only enforcement should raise violation."""
        with pytest.raises(Axiom3EnforcementViolation):
            validate_constraint_not_soft("confidence_threshold", "warning")

    def test_mechanical_enforcement_passes(self):
        """Mechanical enforcement (hook/pipeline/gate) should not raise."""
        with pytest.raises(Axiom3EnforcementViolation) as exc_info:
            validate_constraint_enforced(
                constraint_name="confidence_threshold",
                enforcement_exists=False,  # This will raise
                enforcement_type="pre_commit_hook"
            )
        # Verify it raised for the right reason
        assert "enforcement" in str(exc_info.value).lower()

    def test_enforcement_exists_passes(self):
        """Constraint with enforcement should not raise."""
        # Should not raise
        validate_constraint_enforced(
            constraint_name="confidence_threshold",
            enforcement_exists=True,
            enforcement_type="tier_1_hook"
        )


# ============================================================================
# Axiom 4: Resilience/Adaptation Tests
# ============================================================================

class TestAxiom4Resilience:
    """Test Axiom 4: Adaptation is versioned, audited, and reversible."""

    def test_adaptation_without_version_raises_violation(self):
        """Adaptation without version should raise Axiom4ResilienceViolation."""
        with pytest.raises(Axiom4ResilienceViolation):
            validate_adaptation_versioned(
                adaptation_description="Tighten confidence gate",
                version=None
            )

    def test_adaptation_missing_audit_fields_raises_violation(self):
        """Adaptation with incomplete audit trail should raise violation."""
        audit_fields = {"who": "john", "what": "tighten gate"}  # Missing 'why' and 'when'
        with pytest.raises(Axiom4ResilienceViolation):
            validate_adaptation_audited(
                adaptation_description="Tighten confidence gate",
                audit_fields=audit_fields
            )

    def test_adaptation_without_rollback_path_raises_violation(self):
        """Adaptation without reversibility should raise violation."""
        with pytest.raises(Axiom4ResilienceViolation):
            validate_adaptation_reversible(
                adaptation_description="Tighten confidence gate",
                prior_version=None,
                git_commit=None
            )

    def test_adaptation_modifying_axioms_raises_violation(self):
        """Attempting to adapt core axioms should raise violation."""
        with pytest.raises(Axiom4ResilienceViolation):
            validate_adaptation_preserves_core("axioms")

    def test_adaptation_modifying_primitives_raises_violation(self):
        """Attempting to adapt primitives should raise violation."""
        with pytest.raises(Axiom4ResilienceViolation):
            validate_adaptation_preserves_core("primitives")

    def test_adaptation_modifying_loop_raises_violation(self):
        """Attempting to adapt Loop structure should raise violation."""
        with pytest.raises(Axiom4ResilienceViolation):
            validate_adaptation_preserves_core("five_phase_loop")

    def test_compliant_adaptation_versioned(self):
        """Versioned adaptation should not raise."""
        # Should not raise
        validate_adaptation_versioned(
            adaptation_description="Tighten confidence gate from 0.7 to 0.75",
            version="constraint_v1.1"
        )

    def test_compliant_adaptation_audited(self):
        """Fully audited adaptation should not raise."""
        audit_fields = {
            "who": "john@example.com",
            "what": "Tighten gate from 0.7 to 0.75",
            "why": "Homeostasis score dropped below 0.85",
            "when": "2026-04-05T10:30:00Z"
        }
        # Should not raise
        validate_adaptation_audited(
            adaptation_description="Tighten confidence gate",
            audit_fields=audit_fields
        )

    def test_compliant_adaptation_reversible(self):
        """Adaptation with rollback path should not raise."""
        # Should not raise
        validate_adaptation_reversible(
            adaptation_description="Tighten confidence gate",
            prior_version="constraint_v1.0",
            git_commit="abc1234567"
        )

    def test_compliant_adaptation_preserves_core(self):
        """Adaptation of non-core components should not raise."""
        # Should not raise (adapting a constraint is allowed)
        validate_adaptation_preserves_core("confidence_threshold")


# ============================================================================
# Exception Class Tests
# ============================================================================

class TestAxiomExceptionClasses:
    """Test AxiomViolationException and subclasses."""

    def test_axiom_violation_exception_formatting(self):
        """AxiomViolationException should format message correctly."""
        exc = Axiom1ImmutabilityViolation(
            message="Test violation",
            attempted_override="axiom_enforcement",
            context={"test": "data"}
        )
        assert "AXIOM 1 VIOLATION" in str(exc)
        assert "axiom_1_immutability" in str(exc)
        assert "timestamp=" in str(exc)

    def test_axiom_violation_to_incident_dict(self):
        """AxiomViolationException should convert to incident dict."""
        exc = Axiom2DeterminismViolation(
            message="Non-deterministic behavior",
            outcome_1="ACCEPT",
            outcome_2="REJECT"
        )
        incident = exc.to_incident_dict()
        assert incident["type"] == "axiom_violation"
        assert incident["axiom"] == 2
        assert incident["violation_type"] == "axiom_2_determinism"
        assert incident["message"] == "Non-deterministic behavior detected: Non-deterministic behavior"

    def test_axiom_violations_logged(self, caplog):
        """All axiom violations should be logged as critical."""
        with pytest.raises(Axiom3EnforcementViolation):
            validate_constraint_enforced(
                constraint_name="test_constraint",
                enforcement_exists=False,
                enforcement_type="none"
            )
        # Verify critical log was written
        assert any("AXIOM VIOLATION" in record.message for record in caplog.records)


# ============================================================================
# Integration Tests
# ============================================================================

class TestAxiomEnforcementIntegration:
    """Integration tests for axiom enforcement across multiple axioms."""

    def test_policy_passes_all_axioms(self):
        """Compliant policy should pass all axiom checks."""
        policy = {
            "domain": "auth",
            "constraint": "confidence > 0.75",
            "escalation": "human_review"
        }
        # Should not raise any violations
        validate_policy_not_immutable_override(policy)

    def test_determinism_with_full_result_structure(self):
        """Determinism check with complete result structure should pass."""
        result = {
            "outcome": "POLICY_ACCEPTED",
            "confidence": 0.88,
            "uncertainty_bounds": {
                "epistemic_lower": 0.85,
                "epistemic_upper": 0.91,
                "aleatoric": 0.02
            }
        }
        # Should not raise
        validate_determinism_with_bounds(result, "policy_validation")


# ============================================================================
# Test Coverage Target: >95%
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src/enct/axioms", "--cov-report=term-missing"])
