"""
ENCT Phase 3: Synthetic Scenario Definitions

Defines scenario structure, metadata, and categorization for 500+ test scenarios.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, Callable
from datetime import datetime


class ScenarioCategory(Enum):
    """Categories of test scenarios."""
    AXIOM_1_IMMUTABILITY = "axiom_1_immutability"
    AXIOM_2_DETERMINISM = "axiom_2_determinism"
    AXIOM_3_ENFORCEMENT = "axiom_3_enforcement"
    AXIOM_4_RESILIENCE = "axiom_4_resilience"
    DOMAIN_AUTH = "domain_auth"
    DOMAIN_RATE_LIMITING = "domain_rate_limiting"
    DOMAIN_DATA_VALIDATION = "domain_data_validation"
    DOMAIN_ACCESS_CONTROL = "domain_access_control"
    DOMAIN_COMPLIANCE = "domain_compliance"
    EDGE_CASE = "edge_case"


class ExpectedOutcome(Enum):
    """Expected outcome of a scenario."""
    PASS = "pass"
    AXIOM_VIOLATION = "axiom_violation"
    CONSTRAINT_VIOLATION = "constraint_violation"
    DETERMINISM_VIOLATION = "determinism_violation"
    ENFORCEMENT_VIOLATION = "enforcement_violation"
    RESILIENCE_VIOLATION = "resilience_violation"
    REJECTED = "rejected"
    EXCEPTION = "exception"


class SeverityLevel(Enum):
    """Severity of scenario."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Scenario:
    """
    Single test scenario definition.

    Each scenario:
    - Has unique ID
    - Belongs to category
    - Has setup/execute/verify functions
    - Specifies expected outcome
    - Tracks execution results
    """
    scenario_id: str
    category: ScenarioCategory
    description: str
    severity: SeverityLevel
    expected_outcome: ExpectedOutcome

    # Setup and execution
    setup_fn: Optional[Callable] = None  # Prepare test environment
    execute_fn: Optional[Callable] = None  # Run the scenario
    verify_fn: Optional[Callable] = None  # Verify results

    # Metadata
    tags: list[str] = field(default_factory=list)
    axiom_related: Optional[int] = None  # Which axiom (1-4) or None
    domain: Optional[str] = None  # Auth, rate-limiting, etc.
    dependencies: list[str] = field(default_factory=list)  # Other scenario IDs

    # Execution tracking
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    executed_at: Optional[str] = None
    result_status: Optional[str] = None
    result_message: Optional[str] = None
    execution_time_ms: float = 0.0

    def __post_init__(self):
        """Validate scenario on creation."""
        if not self.scenario_id:
            raise ValueError("scenario_id required")
        if not self.execute_fn:
            raise ValueError("execute_fn required")

    @property
    def full_id(self) -> str:
        """Full unique identifier for scenario."""
        return f"{self.category.value}_{self.scenario_id}"

    def to_dict(self) -> dict[str, Any]:
        """Serialize scenario to dict."""
        return {
            "scenario_id": self.scenario_id,
            "full_id": self.full_id,
            "category": self.category.value,
            "description": self.description,
            "severity": self.severity.value,
            "expected_outcome": self.expected_outcome.value,
            "tags": self.tags,
            "axiom_related": self.axiom_related,
            "domain": self.domain,
            "created_at": self.created_at,
            "executed_at": self.executed_at,
            "result_status": self.result_status,
            "result_message": self.result_message,
            "execution_time_ms": self.execution_time_ms,
        }


@dataclass
class ScenarioResult:
    """Result of scenario execution."""
    scenario_id: str
    full_id: str
    status: str  # "PASS", "FAIL", "ERROR", "SKIP"
    expected_outcome: str
    actual_outcome: str
    message: str = ""
    error_details: Optional[dict[str, Any]] = None
    execution_time_ms: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def passed(self) -> bool:
        """Check if scenario passed."""
        return self.status == "PASS"

    def failed(self) -> bool:
        """Check if scenario failed."""
        return self.status in ("FAIL", "ERROR")

    def to_dict(self) -> dict[str, Any]:
        """Serialize result to dict."""
        return {
            "scenario_id": self.scenario_id,
            "full_id": self.full_id,
            "status": self.status,
            "expected_outcome": self.expected_outcome,
            "actual_outcome": self.actual_outcome,
            "message": self.message,
            "error_details": self.error_details,
            "execution_time_ms": self.execution_time_ms,
            "timestamp": self.timestamp,
        }


@dataclass
class ScenarioRunSummary:
    """Summary of complete scenario run."""
    total_scenarios: int = 0
    passed: int = 0
    failed: int = 0
    errors: int = 0
    skipped: int = 0
    start_time: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    end_time: Optional[str] = None
    total_time_ms: float = 0.0
    results_by_category: dict[str, dict[str, int]] = field(default_factory=dict)

    @property
    def pass_rate(self) -> float:
        """Calculate pass rate (0.0-1.0)."""
        if self.total_scenarios == 0:
            return 0.0
        return self.passed / (self.passed + self.failed + self.errors)

    @property
    def success(self) -> bool:
        """Check if run was successful (≥95% pass rate)."""
        return self.pass_rate >= 0.95

    def to_dict(self) -> dict[str, Any]:
        """Serialize summary to dict."""
        return {
            "total_scenarios": self.total_scenarios,
            "passed": self.passed,
            "failed": self.failed,
            "errors": self.errors,
            "skipped": self.skipped,
            "pass_rate": f"{self.pass_rate:.2%}",
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_time_ms": self.total_time_ms,
            "results_by_category": self.results_by_category,
        }
