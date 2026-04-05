"""
ENCT Axiom Violation Exception Classes

Fail-hard enforcement: all axiom violations raise exceptions immediately.
No graceful degradation, no fallback logic at this layer.
Exceptions propagate up to Loop phase handlers or agent entrypoints.
"""

import logging
from enum import Enum
from datetime import datetime
from typing import Any, Optional

logger = logging.getLogger(__name__)


class AxiomViolationType(Enum):
    """Types of axiom violations."""
    AXIOM_1_IMMUTABILITY = "axiom_1_immutability"
    AXIOM_2_DETERMINISM = "axiom_2_determinism"
    AXIOM_3_ENFORCEMENT = "axiom_3_enforcement"
    AXIOM_4_RESILIENCE = "axiom_4_resilience"


class AxiomViolationException(Exception):
    """
    Base exception for all axiom violations.

    Fail-hard semantics: raised immediately, logged as critical incident,
    propagates to caller for escalation.
    """

    def __init__(
        self,
        axiom_number: int,
        violation_type: AxiomViolationType,
        message: str,
        context: Optional[dict[str, Any]] = None
    ):
        self.axiom_number = axiom_number
        self.violation_type = violation_type
        self.message = message
        self.context = context or {}
        self.timestamp = datetime.utcnow().isoformat()

        # Log critical incident immediately
        self._log_critical_incident()

        super().__init__(self._format_message())

    def _format_message(self) -> str:
        """Format exception message with full context."""
        return (
            f"AXIOM {self.axiom_number} VIOLATION ({self.violation_type.value}): {self.message} "
            f"[timestamp={self.timestamp}]"
        )

    def _log_critical_incident(self) -> None:
        """Log violation as critical incident for audit trail."""
        logger.critical(
            f"AXIOM VIOLATION: axiom={self.axiom_number}, "
            f"type={self.violation_type.value}, "
            f"message={self.message}, "
            f"context={self.context}, "
            f"timestamp={self.timestamp}"
        )

    def to_incident_dict(self) -> dict[str, Any]:
        """Convert to incident logging format (for FAILURE-LEDGER)."""
        return {
            "type": "axiom_violation",
            "axiom": self.axiom_number,
            "violation_type": self.violation_type.value,
            "message": self.message,
            "context": self.context,
            "timestamp": self.timestamp,
        }


class Axiom1ImmutabilityViolation(AxiomViolationException):
    """
    Axiom 1 Violation: Foundational rules cannot be modified.

    Raised when:
    - Policy attempts to disable axiom enforcement
    - Policy attempts to modify 5-phase Loop structure
    - Policy attempts to override primitives
    - Code tries to bypass foundational components
    """

    def __init__(
        self,
        message: str,
        attempted_override: str,
        context: Optional[dict[str, Any]] = None
    ):
        self.attempted_override = attempted_override
        super().__init__(
            axiom_number=1,
            violation_type=AxiomViolationType.AXIOM_1_IMMUTABILITY,
            message=f"Attempted to override foundational rule: {attempted_override}. {message}",
            context={**(context or {}), "attempted_override": attempted_override}
        )


class Axiom2DeterminismViolation(AxiomViolationException):
    """
    Axiom 2 Violation: Action determinism violated.

    Raised when:
    - Same action yields different outcomes without declared uncertainty bounds
    - Non-determinism detected in validation or policy application
    - Randomness used without epistemic/aleatoric bounds
    """

    def __init__(
        self,
        message: str,
        outcome_1: Any,
        outcome_2: Any,
        context: Optional[dict[str, Any]] = None
    ):
        self.outcome_1 = outcome_1
        self.outcome_2 = outcome_2
        super().__init__(
            axiom_number=2,
            violation_type=AxiomViolationType.AXIOM_2_DETERMINISM,
            message=f"Non-deterministic behavior detected: {message}",
            context={
                **(context or {}),
                "outcome_1": str(outcome_1),
                "outcome_2": str(outcome_2),
            }
        )


class Axiom3EnforcementViolation(AxiomViolationException):
    """
    Axiom 3 Violation: Normative constraint not mechanically enforced.

    Raised when:
    - Constraint is documented but not enforced in code/hooks/CI
    - Constraint is violated at runtime without being caught
    - Enforcement mechanism is missing or disabled
    """

    def __init__(
        self,
        message: str,
        constraint_name: str,
        enforcement_missing: str,
        context: Optional[dict[str, Any]] = None
    ):
        self.constraint_name = constraint_name
        self.enforcement_missing = enforcement_missing
        super().__init__(
            axiom_number=3,
            violation_type=AxiomViolationType.AXIOM_3_ENFORCEMENT,
            message=f"Constraint '{constraint_name}' not enforced: {message}. Missing: {enforcement_missing}",
            context={
                **(context or {}),
                "constraint": constraint_name,
                "missing_enforcement": enforcement_missing,
            }
        )


class Axiom4ResilienceViolation(AxiomViolationException):
    """
    Axiom 4 Violation: Adaptation not versioned/audited/reversible.

    Raised when:
    - Constraint modified without version tracking
    - Adaptation made without audit trail
    - Change not reversible (no prior version preserved)
    - Core axioms 1-3 modified (cannot adapt those)
    """

    def __init__(
        self,
        message: str,
        adaptation_description: str,
        missing_requirement: str,
        context: Optional[dict[str, Any]] = None
    ):
        self.adaptation = adaptation_description
        self.missing = missing_requirement
        super().__init__(
            axiom_number=4,
            violation_type=AxiomViolationType.AXIOM_4_RESILIENCE,
            message=f"Adaptation not properly controlled: {message}. Missing: {missing_requirement}",
            context={
                **(context or {}),
                "adaptation": adaptation_description,
                "missing": missing_requirement,
            }
        )
