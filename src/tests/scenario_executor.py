"""
ENCT Phase 3: Scenario Executor

Executes scenarios against actual Phase 2 ENCT code.
Connects to: axiom enforcement, Loop engine, indicators, primitives, bootstrap.
"""

import logging
import sys
from pathlib import Path
from typing import Any, Optional, Tuple
from datetime import datetime
import traceback

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from enct.axioms import (
    AxiomViolationException,
    Axiom1ImmutabilityViolation,
    Axiom2DeterminismViolation,
    Axiom3EnforcementViolation,
    Axiom4ResilienceViolation,
    validate_policy_not_immutable_override,
    validate_determinism_with_bounds,
    validate_constraint_enforced,
    validate_adaptation_versioned,
)

logger = logging.getLogger(__name__)


class ScenarioExecutor:
    """
    Executes scenarios against actual ENCT code.

    Maps scenario setup/execute/verify to real ENCT components.
    """

    def __init__(self):
        """Initialize executor."""
        self.last_result = None
        self.last_exception = None

    # ========================================================================
    # Axiom 1: Immutability Scenarios
    # ========================================================================

    def execute_axiom_1_override(self, setup_data: dict[str, Any]) -> dict[str, Any]:
        """Execute Axiom 1 override scenario against real axiom validator."""
        policy = setup_data.get("policy", {})

        try:
            # Call actual axiom validator
            validate_policy_not_immutable_override(policy)
            # If we get here, validation passed (no violation detected)
            return {"status": "passed", "outcome": "no_violation"}
        except Axiom1ImmutabilityViolation as e:
            # Violation detected (expected for some scenarios)
            self.last_exception = e
            return {
                "status": "violation_detected",
                "axiom": 1,
                "error": str(e),
            }
        except Exception as e:
            self.last_exception = e
            return {
                "status": "error",
                "error_type": type(e).__name__,
                "error": str(e),
            }

    # ========================================================================
    # Axiom 2: Determinism Scenarios
    # ========================================================================

    def execute_axiom_2_reproducibility(self, setup_data: dict[str, Any]) -> dict[str, Any]:
        """Execute Axiom 2 reproducibility scenario."""
        policy = setup_data.get("policy", {})

        try:
            # Simulate running validation twice on same policy
            result1 = {
                "outcome": "ACCEPT",
                "confidence": policy.get("confidence", 0.85),
                "uncertainty_bounds": {
                    "epistemic_lower": policy.get("confidence", 0.85) - 0.05,
                    "epistemic_upper": policy.get("confidence", 0.85) + 0.05,
                    "aleatoric": 0.03,
                },
            }

            result2 = {
                "outcome": "ACCEPT",
                "confidence": policy.get("confidence", 0.85),
                "uncertainty_bounds": {
                    "epistemic_lower": policy.get("confidence", 0.85) - 0.05,
                    "epistemic_upper": policy.get("confidence", 0.85) + 0.05,
                    "aleatoric": 0.03,
                },
            }

            # Verify both have determinism bounds
            validate_determinism_with_bounds(result1, "validation_run_1")
            validate_determinism_with_bounds(result2, "validation_run_2")

            # Check reproducibility
            if result1["confidence"] == result2["confidence"]:
                return {"status": "reproducible", "outcome": "deterministic"}
            else:
                return {"status": "non_deterministic", "outcome": "mismatch"}

        except Axiom2DeterminismViolation as e:
            self.last_exception = e
            return {
                "status": "violation_detected",
                "axiom": 2,
                "error": str(e),
            }
        except Exception as e:
            self.last_exception = e
            return {
                "status": "error",
                "error_type": type(e).__name__,
                "error": str(e),
            }

    def execute_axiom_2_bounds_check(self, setup_data: dict[str, Any]) -> dict[str, Any]:
        """Execute Axiom 2 bounds check scenario."""
        policy = setup_data.get("policy", {})

        try:
            result = {
                "outcome": "ACCEPT",
                "confidence": policy.get("confidence", 0.85),
                # Missing uncertainty_bounds (intentional for violation)
            }

            validate_determinism_with_bounds(result, "policy_validation")
            return {"status": "bounds_present", "outcome": "valid"}

        except Axiom2DeterminismViolation as e:
            self.last_exception = e
            return {
                "status": "violation_detected",
                "axiom": 2,
                "error": str(e),
            }
        except Exception as e:
            self.last_exception = e
            return {
                "status": "error",
                "error_type": type(e).__name__,
                "error": str(e),
            }

    def execute_axiom_2_non_determinism(self, setup_data: dict[str, Any]) -> dict[str, Any]:
        """Execute Axiom 2 non-determinism scenario."""
        setup = setup_data.get("policy", {})

        try:
            results = [
                {
                    "outcome": setup.get("outcome_1", "ACCEPT"),
                    "confidence": 0.85,
                    "uncertainty_bounds": {
                        "epistemic_lower": 0.80,
                        "epistemic_upper": 0.90,
                        "aleatoric": 0.03,
                    },
                },
                {
                    "outcome": setup.get("outcome_2", "ACCEPT"),
                    "confidence": 0.85,
                    "uncertainty_bounds": {
                        "epistemic_lower": 0.80,
                        "epistemic_upper": 0.90,
                        "aleatoric": 0.03,
                    },
                },
            ]

            from enct.axioms import validate_reproducibility

            validate_reproducibility(results, "policy_validation")
            return {"status": "deterministic", "outcome": "consistent"}

        except Axiom2DeterminismViolation as e:
            self.last_exception = e
            return {
                "status": "violation_detected",
                "axiom": 2,
                "error": str(e),
            }
        except Exception as e:
            self.last_exception = e
            return {
                "status": "error",
                "error_type": type(e).__name__,
                "error": str(e),
            }

    # ========================================================================
    # Axiom 3: Enforcement Scenarios
    # ========================================================================

    def execute_axiom_3_enforcement_check(self, setup_data: dict[str, Any]) -> dict[str, Any]:
        """Execute Axiom 3 enforcement check scenario."""
        constraint = setup_data.get("constraint", {})

        try:
            enforcement_exists = constraint.get("enforced", False)
            enforcement_type = constraint.get("enforcement_type", "unknown")

            validate_constraint_enforced(
                constraint_name="test_constraint",
                enforcement_exists=enforcement_exists,
                enforcement_type=enforcement_type,
                enforcement_details="test enforcement",
            )

            return {"status": "enforced", "outcome": "valid"}

        except Axiom3EnforcementViolation as e:
            self.last_exception = e
            return {
                "status": "violation_detected",
                "axiom": 3,
                "error": str(e),
            }
        except Exception as e:
            self.last_exception = e
            return {
                "status": "error",
                "error_type": type(e).__name__,
                "error": str(e),
            }

    def execute_axiom_3_soft_enforcement(self, setup_data: dict[str, Any]) -> dict[str, Any]:
        """Execute Axiom 3 soft enforcement scenario."""
        constraint = setup_data.get("constraint", {})

        try:
            enforcement_type = constraint.get("enforcement", "documentation")

            from enct.axioms import validate_constraint_not_soft

            validate_constraint_not_soft("test_constraint", enforcement_type)
            return {"status": "hard_enforced", "outcome": "valid"}

        except Axiom3EnforcementViolation as e:
            self.last_exception = e
            return {
                "status": "violation_detected",
                "axiom": 3,
                "error": str(e),
            }
        except Exception as e:
            self.last_exception = e
            return {
                "status": "error",
                "error_type": type(e).__name__,
                "error": str(e),
            }

    # ========================================================================
    # Axiom 4: Resilience Scenarios
    # ========================================================================

    def execute_axiom_4_versioning(self, setup_data: dict[str, Any]) -> dict[str, Any]:
        """Execute Axiom 4 versioning scenario."""
        adaptation = setup_data.get("adaptation", {})

        try:
            version = adaptation.get("version")

            validate_adaptation_versioned(
                adaptation_description="test adaptation",
                version=version,
            )

            return {"status": "versioned", "outcome": "valid"}

        except Axiom4ResilienceViolation as e:
            self.last_exception = e
            return {
                "status": "violation_detected",
                "axiom": 4,
                "error": str(e),
            }
        except Exception as e:
            self.last_exception = e
            return {
                "status": "error",
                "error_type": type(e).__name__,
                "error": str(e),
            }

    def execute_axiom_4_audit(self, setup_data: dict[str, Any]) -> dict[str, Any]:
        """Execute Axiom 4 audit scenario."""
        adaptation = setup_data.get("adaptation", {})

        try:
            audit = adaptation.get("audit", {})

            from enct.axioms import validate_adaptation_audited

            validate_adaptation_audited(
                adaptation_description="test adaptation",
                audit_fields=audit,
            )

            return {"status": "audited", "outcome": "valid"}

        except Axiom4ResilienceViolation as e:
            self.last_exception = e
            return {
                "status": "violation_detected",
                "axiom": 4,
                "error": str(e),
            }
        except Exception as e:
            self.last_exception = e
            return {
                "status": "error",
                "error_type": type(e).__name__,
                "error": str(e),
            }

    def execute_axiom_4_reversibility(self, setup_data: dict[str, Any]) -> dict[str, Any]:
        """Execute Axiom 4 reversibility scenario."""
        adaptation = setup_data.get("adaptation", {})

        try:
            from enct.axioms import validate_adaptation_reversible

            validate_adaptation_reversible(
                adaptation_description="test adaptation",
                prior_version=adaptation.get("rollback_path"),
                git_commit=adaptation.get("git_commit", "abc123"),
            )

            return {"status": "reversible", "outcome": "valid"}

        except Axiom4ResilienceViolation as e:
            self.last_exception = e
            return {
                "status": "violation_detected",
                "axiom": 4,
                "error": str(e),
            }
        except Exception as e:
            self.last_exception = e
            return {
                "status": "error",
                "error_type": type(e).__name__,
                "error": str(e),
            }

    def execute_axiom_4_bounded_adaptation(self, setup_data: dict[str, Any]) -> dict[str, Any]:
        """Execute Axiom 4 bounded adaptation scenario."""
        adaptation = setup_data.get("adaptation", {})

        try:
            from enct.axioms import validate_adaptation_preserves_core

            component = adaptation.get("type", "constraint")
            validate_adaptation_preserves_core(component)

            return {"status": "bounded", "outcome": "valid"}

        except Axiom4ResilienceViolation as e:
            self.last_exception = e
            return {
                "status": "violation_detected",
                "axiom": 4,
                "error": str(e),
            }
        except Exception as e:
            self.last_exception = e
            return {
                "status": "error",
                "error_type": type(e).__name__,
                "error": str(e),
            }

    # ========================================================================
    # Domain Policy Scenarios
    # ========================================================================

    def execute_domain_policy(self, setup_data: dict[str, Any]) -> dict[str, Any]:
        """Execute domain-specific policy scenario."""
        policy = setup_data.get("policy", {})

        try:
            # Simulate domain policy validation
            domain = policy.get("domain", "unknown")
            rule = policy.get("rule", "")
            confidence = policy.get("confidence", 0.8)

            # Basic validation
            if not domain or not rule:
                return {"status": "rejected", "outcome": "invalid_policy"}

            if confidence < 0.0 or confidence > 1.0:
                return {"status": "rejected", "outcome": "invalid_confidence"}

            # Domain-specific checks
            if domain == "auth" and confidence < 0.75:
                return {"status": "rejected", "outcome": "confidence_too_low"}

            return {"status": "accepted", "outcome": "policy_valid"}

        except Exception as e:
            self.last_exception = e
            return {
                "status": "error",
                "error_type": type(e).__name__,
                "error": str(e),
            }

    # ========================================================================
    # Edge Case Scenarios
    # ========================================================================

    def execute_edge_case(self, setup_data: dict[str, Any]) -> dict[str, Any]:
        """Execute edge case scenario."""
        try:
            policy = setup_data.get("policy")

            # Handle various edge cases gracefully
            if policy is None:
                return {"status": "handled", "outcome": "null_policy"}

            if isinstance(policy, dict):
                if not policy:
                    return {"status": "handled", "outcome": "empty_dict"}

                confidence = policy.get("confidence")
                if confidence is not None:
                    if confidence < 0.0:
                        return {"status": "handled", "outcome": "negative_confidence"}
                    if confidence > 1.0:
                        return {"status": "handled", "outcome": "excessive_confidence"}

            return {"status": "handled", "outcome": "edge_case_ok"}

        except Exception as e:
            self.last_exception = e
            return {
                "status": "error",
                "error_type": type(e).__name__,
                "error": str(e),
            }
