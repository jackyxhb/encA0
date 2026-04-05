"""
ENCT Loop State Definitions

Defines state objects for each phase of the 5-phase Loop.
Sense → Validate → Execute → Assess → Re-enact
"""

from dataclasses import dataclass, field
from typing import Any, Optional
from enum import Enum
from datetime import datetime


class LoopPhase(Enum):
    """Enumeration of 5-phase Loop phases."""
    SENSE = "sense"
    VALIDATE = "validate"
    EXECUTE = "execute"
    ASSESS = "assess"
    RE_ENACT = "re_enact"
    COMPLETE = "complete"


class LoopStatus(Enum):
    """Status of Loop execution."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    FAILED = "failed"
    AXIOM_VIOLATION = "axiom_violation"


@dataclass
class SensePhaseOutput:
    """Output from Sense phase: environmental observations."""
    timestamp: str
    observations: dict[str, Any]
    policy_request: Optional[dict[str, Any]] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "observations": self.observations,
            "policy_request": self.policy_request,
        }


@dataclass
class ValidatePhaseOutput:
    """Output from Validate phase: validation results with confidence bounds."""
    timestamp: str
    constraint_checks: dict[str, bool]  # {constraint_name: passed}
    confidence: float  # 0.0-1.0
    uncertainty_bounds: dict[str, float]  # epistemic_lower, epistemic_upper, aleatoric
    validation_details: dict[str, Any] = field(default_factory=dict)
    passed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "constraint_checks": self.constraint_checks,
            "confidence": self.confidence,
            "uncertainty_bounds": self.uncertainty_bounds,
            "validation_details": self.validation_details,
            "passed": self.passed,
        }


@dataclass
class ExecutePhaseOutput:
    """Output from Execute phase: action outcomes."""
    timestamp: str
    action_taken: str
    outcome: Any
    side_effects: list[str] = field(default_factory=list)
    escalation_required: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "action_taken": self.action_taken,
            "outcome": str(self.outcome),
            "side_effects": self.side_effects,
            "escalation_required": self.escalation_required,
        }


@dataclass
class AssessPhaseOutput:
    """Output from Assess phase: metric calculations and assessments."""
    timestamp: str
    metrics: dict[str, float]  # {metric_name: score}
    violations_detected: list[str] = field(default_factory=list)
    system_health: float = 0.85  # 0.0-1.0
    assessment: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "metrics": self.metrics,
            "violations_detected": self.violations_detected,
            "system_health": self.system_health,
            "assessment": self.assessment,
        }


@dataclass
class ReEnactPhaseOutput:
    """Output from Re-enact phase: adaptations and versioning."""
    timestamp: str
    adaptations_made: list[str] = field(default_factory=list)
    version_updated: bool = False
    new_version: Optional[str] = None
    rollback_decision: Optional[str] = None  # If rollback triggered

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "adaptations_made": self.adaptations_made,
            "version_updated": self.version_updated,
            "new_version": self.new_version,
            "rollback_decision": self.rollback_decision,
        }


@dataclass
class LoopCycleState:
    """Complete state of a Loop cycle."""
    cycle_id: str
    status: LoopStatus = LoopStatus.NOT_STARTED
    current_phase: LoopPhase = LoopPhase.SENSE
    start_time: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    end_time: Optional[str] = None

    # Phase outputs (populated as Loop progresses)
    sense_output: Optional[SensePhaseOutput] = None
    validate_output: Optional[ValidatePhaseOutput] = None
    execute_output: Optional[ExecutePhaseOutput] = None
    assess_output: Optional[AssessPhaseOutput] = None
    reenact_output: Optional[ReEnactPhaseOutput] = None

    # Error state (if axiom violation or other error occurs)
    error: Optional[str] = None
    error_phase: Optional[LoopPhase] = None
    error_details: dict[str, Any] = field(default_factory=dict)

    # Ledger references (written after each phase)
    policy_ledger_entry_id: Optional[str] = None
    failure_ledger_entry_id: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert state to dictionary for serialization."""
        return {
            "cycle_id": self.cycle_id,
            "status": self.status.value,
            "current_phase": self.current_phase.value,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "sense_output": self.sense_output.to_dict() if self.sense_output else None,
            "validate_output": self.validate_output.to_dict() if self.validate_output else None,
            "execute_output": self.execute_output.to_dict() if self.execute_output else None,
            "assess_output": self.assess_output.to_dict() if self.assess_output else None,
            "reenact_output": self.reenact_output.to_dict() if self.reenact_output else None,
            "error": self.error,
            "error_phase": self.error_phase.value if self.error_phase else None,
            "error_details": self.error_details,
            "policy_ledger_entry_id": self.policy_ledger_entry_id,
            "failure_ledger_entry_id": self.failure_ledger_entry_id,
        }
