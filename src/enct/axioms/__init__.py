"""
ENCT Axioms Module

Exports axiom exceptions and validators for fail-hard enforcement.

Public API:
- AxiomViolationException: Base exception class
- Axiom1ImmutabilityViolation, Axiom2DeterminismViolation, etc.
- Validators: validate_policy_not_immutable_override, validate_determinism_with_bounds, etc.
"""

from .axiom_exceptions import (
    AxiomViolationException,
    AxiomViolationType,
    Axiom1ImmutabilityViolation,
    Axiom2DeterminismViolation,
    Axiom3EnforcementViolation,
    Axiom4ResilienceViolation,
)

from .axiom_validators import (
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
    enforce_axioms,
)

__all__ = [
    # Exceptions
    "AxiomViolationException",
    "AxiomViolationType",
    "Axiom1ImmutabilityViolation",
    "Axiom2DeterminismViolation",
    "Axiom3EnforcementViolation",
    "Axiom4ResilienceViolation",
    # Validators
    "validate_policy_not_immutable_override",
    "validate_no_axiom_bypass_in_code",
    "validate_determinism_with_bounds",
    "validate_reproducibility",
    "validate_constraint_enforced",
    "validate_constraint_not_soft",
    "validate_adaptation_versioned",
    "validate_adaptation_audited",
    "validate_adaptation_reversible",
    "validate_adaptation_preserves_core",
    "enforce_axioms",
]
