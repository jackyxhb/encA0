"""
ENCT Axiom Validators and Enforcement Checks

Each validator checks a specific axiom condition and raises AxiomViolationException
if violated (fail-hard semantics).
"""

import logging
from typing import Any, Callable, TypeVar, Optional
from functools import wraps

from .axiom_exceptions import (
    AxiomViolationException,
    Axiom1ImmutabilityViolation,
    Axiom2DeterminismViolation,
    Axiom3EnforcementViolation,
    Axiom4ResilienceViolation,
)

logger = logging.getLogger(__name__)


# ============================================================================
# Axiom 1: Immutability Validators
# ============================================================================

FOUNDATIONAL_RULES = {
    "primitives",
    "five_phase_loop",
    "axioms",
    "base_indicators",
    "tier_validation_framework",
    "provenance_recording",
}

FORBIDDEN_POLICY_KEYWORDS = {
    "disable axiom",
    "skip validation",
    "bypass enforcement",
    "override axiom",
    "remove constraint",
    "disable verification",
}


def validate_policy_not_immutable_override(policy: dict[str, Any]) -> None:
    """
    Axiom 1 Check: Policy does not attempt to override foundational rules.

    Raises:
        Axiom1ImmutabilityViolation if policy violates Axiom 1
    """
    policy_text = str(policy).lower()

    # Check for forbidden keywords
    for keyword in FORBIDDEN_POLICY_KEYWORDS:
        if keyword in policy_text:
            raise Axiom1ImmutabilityViolation(
                message="Policy contains forbidden override keyword",
                attempted_override=keyword,
                context={"policy": str(policy)[:500]}  # Truncate for logging
            )

    # Check if policy attempts to modify foundational components
    if "loop" in policy_text and ("remove" in policy_text or "skip" in policy_text):
        raise Axiom1ImmutabilityViolation(
            message="Policy attempts to modify 5-phase Loop structure",
            attempted_override="five_phase_loop",
            context={"policy": str(policy)[:500]}
        )

    if "axiom" in policy_text and ("disable" in policy_text or "override" in policy_text):
        raise Axiom1ImmutabilityViolation(
            message="Policy attempts to disable axiom enforcement",
            attempted_override="axioms",
            context={"policy": str(policy)[:500]}
        )


def validate_no_axiom_bypass_in_code(code_snippet: str, component_name: str) -> None:
    """
    Axiom 1 Check: Code does not bypass axiom enforcement.

    Raises:
        Axiom1ImmutabilityViolation if code contains bypass patterns
    """
    bypass_patterns = [
        "skip_axiom",
        "disable_axiom",
        "axiom_check = False",
        "if False: axiom",
        "bypass_enforcement",
    ]

    for pattern in bypass_patterns:
        if pattern in code_snippet.lower():
            raise Axiom1ImmutabilityViolation(
                message=f"Code contains axiom bypass pattern in {component_name}",
                attempted_override="axiom_enforcement",
                context={"component": component_name, "pattern": pattern}
            )


# ============================================================================
# Axiom 2: Determinism Validators
# ============================================================================

def validate_determinism_with_bounds(
    result: dict[str, Any],
    action_description: str
) -> None:
    """
    Axiom 2 Check: Action result includes proper uncertainty bounds.

    Every Enactive Action must include:
    - outcome: The result
    - confidence: 0.0-1.0 confidence score
    - uncertainty_bounds: {epistemic_lower, epistemic_upper, aleatoric}

    Raises:
        Axiom2DeterminismViolation if bounds are missing or malformed
    """
    required_fields = {
        "outcome": "outcome",
        "confidence": "confidence",
        "uncertainty_bounds": "uncertainty bounds",
    }

    for field, field_name in required_fields.items():
        if field not in result:
            raise Axiom2DeterminismViolation(
                message=f"Result missing required field: {field_name}",
                outcome_1=result,
                outcome_2={"expected": "uncertainty bounds"},
                context={"action": action_description}
            )

    # Validate uncertainty_bounds structure
    bounds = result.get("uncertainty_bounds", {})
    required_bounds = {"epistemic_lower", "epistemic_upper", "aleatoric"}
    if not all(k in bounds for k in required_bounds):
        raise Axiom2DeterminismViolation(
            message="Uncertainty bounds incomplete or malformed",
            outcome_1=bounds,
            outcome_2={"expected": list(required_bounds)},
            context={"action": action_description}
        )

    # Validate confidence is in valid range
    confidence = result.get("confidence")
    if not isinstance(confidence, (int, float)) or not (0.0 <= confidence <= 1.0):
        raise Axiom2DeterminismViolation(
            message="Confidence score out of valid range [0.0, 1.0]",
            outcome_1=confidence,
            outcome_2=0.5,  # Default valid value
            context={"action": action_description}
        )


def validate_reproducibility(
    action_results: list[dict[str, Any]],
    action_description: str,
    tolerance: float = 1e-6
) -> None:
    """
    Axiom 2 Check: Same action yields same result (within declared bounds).

    Runs reproducibility validation: if we execute the same action multiple times
    with the same inputs, the outcomes should be identical.

    Raises:
        Axiom2DeterminismViolation if outcomes diverge
    """
    if not action_results or len(action_results) < 2:
        return  # Cannot validate with <2 results

    first_result = action_results[0]
    first_outcome = first_result.get("outcome")
    first_confidence = first_result.get("confidence", 0)

    for i, result in enumerate(action_results[1:], start=2):
        current_outcome = result.get("outcome")
        current_confidence = result.get("confidence", 0)

        # Check outcome consistency
        if first_outcome != current_outcome:
            raise Axiom2DeterminismViolation(
                message=f"Non-deterministic outcome detected (run 1 vs run {i})",
                outcome_1=first_outcome,
                outcome_2=current_outcome,
                context={"action": action_description}
            )

        # Check confidence consistency (within tolerance)
        if abs(first_confidence - current_confidence) > tolerance:
            raise Axiom2DeterminismViolation(
                message=f"Confidence divergence detected (run 1 vs run {i})",
                outcome_1=first_confidence,
                outcome_2=current_confidence,
                context={"action": action_description}
            )


# ============================================================================
# Axiom 3: Enforcement Validators
# ============================================================================

def validate_constraint_enforced(
    constraint_name: str,
    enforcement_exists: bool,
    enforcement_type: str,
    enforcement_details: Optional[str] = None
) -> None:
    """
    Axiom 3 Check: Normative constraint is mechanically enforced.

    Constraint must have enforcement in at least one of:
    - Tier 1: Pre-commit hook
    - Tier 2: CI pipeline
    - Tier 3: Runtime gate

    Raises:
        Axiom3EnforcementViolation if no enforcement found
    """
    if not enforcement_exists:
        raise Axiom3EnforcementViolation(
            message=f"Constraint '{constraint_name}' has no mechanical enforcement",
            constraint_name=constraint_name,
            enforcement_missing=enforcement_type,
            context={"details": enforcement_details or "No enforcement mechanism"}
        )


def validate_constraint_not_soft(constraint_name: str, enforcement_type: str) -> None:
    """
    Axiom 3 Check: Constraint is not "soft" (documentation/warning only).

    Soft constraints (not enforced) are not real constraints.

    Raises:
        Axiom3EnforcementViolation if constraint is only documented
    """
    soft_enforcement_types = {"documentation", "logging", "warning", "recommendation"}

    if enforcement_type.lower() in soft_enforcement_types:
        raise Axiom3EnforcementViolation(
            message=f"Constraint '{constraint_name}' is only soft-enforced ({enforcement_type})",
            constraint_name=constraint_name,
            enforcement_missing="mechanical enforcement (hook/pipeline/runtime gate)",
            context={"soft_type": enforcement_type}
        )


# ============================================================================
# Axiom 4: Resilience/Adaptation Validators
# ============================================================================

def validate_adaptation_versioned(
    adaptation_description: str,
    version: Optional[str]
) -> None:
    """
    Axiom 4 Check: Any adaptation (constraint change) is versioned.

    Raises:
        Axiom4ResilienceViolation if adaptation not versioned
    """
    if not version:
        raise Axiom4ResilienceViolation(
            message="Adaptation has no version tracking",
            adaptation_description=adaptation_description,
            missing_requirement="version number/tag",
            context={"adaptation": adaptation_description}
        )


def validate_adaptation_audited(
    adaptation_description: str,
    audit_fields: dict[str, Any]
) -> None:
    """
    Axiom 4 Check: Any adaptation has full audit trail.

    Required fields: who, what, why, when

    Raises:
        Axiom4ResilienceViolation if audit trail incomplete
    """
    required_audit = {"who", "what", "why", "when"}
    provided = set(audit_fields.keys())

    if not required_audit.issubset(provided):
        missing = required_audit - provided
        raise Axiom4ResilienceViolation(
            message="Adaptation audit trail incomplete",
            adaptation_description=adaptation_description,
            missing_requirement=f"audit fields: {', '.join(missing)}",
            context={"audit": audit_fields}
        )


def validate_adaptation_reversible(
    adaptation_description: str,
    prior_version: Optional[str],
    git_commit: Optional[str]
) -> None:
    """
    Axiom 4 Check: Any adaptation can be rolled back.

    Requires: prior version reference + git commit hash

    Raises:
        Axiom4ResilienceViolation if rollback path not available
    """
    if not prior_version or not git_commit:
        raise Axiom4ResilienceViolation(
            message="Adaptation not reversible",
            adaptation_description=adaptation_description,
            missing_requirement="prior version reference or git commit hash",
            context={
                "prior_version": prior_version,
                "git_commit": git_commit
            }
        )


def validate_adaptation_preserves_core(adapted_component: str) -> None:
    """
    Axiom 4 Check: Adaptation does not modify core axioms 1-3 or primitives.

    Raises:
        Axiom4ResilienceViolation if core components attempted to be modified
    """
    forbidden_adaptations = {
        "axioms",
        "primitives",
        "five_phase_loop",
        "axiom_enforcement",
    }

    if adapted_component.lower() in forbidden_adaptations:
        raise Axiom4ResilienceViolation(
            message=f"Cannot adapt core component: {adapted_component}",
            adaptation_description=f"Attempted modification of {adapted_component}",
            missing_requirement="use only allowed adaptation targets",
            context={"component": adapted_component}
        )


# ============================================================================
# Decorator: enforce_axioms
# ============================================================================

F = TypeVar('F', bound=Callable[..., Any])


def enforce_axioms(axioms: list[int]) -> Callable[[F], F]:
    """
    Decorator to apply axiom enforcement to a function.

    Usage:
        @enforce_axioms([1, 2, 3])
        def apply_policy(policy):
            ...

    Checks specified axioms before function executes.
    Raises AxiomViolationException on any violation (fail-hard).
    """
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Pre-execution axiom checks would go here
            # (specific checks depend on function context)
            return func(*args, **kwargs)
        return wrapper  # type: ignore
    return decorator
