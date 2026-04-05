"""
ENCT Indicator Definitions

Defines 8 quantitative indicators and their calculation semantics.

Indicators:
1. Compliance Rate - Policy validation success rate
2. Homeostasis Score - Constraint satisfaction across system
3. Traceability Coverage - Actions with complete audit trails
4. Bootstrap Confidence - Mean confidence of validated policies
5. Adaptation Resilience - Successful adaptations / attempted adaptations
6. Provenance Overhead - Storage cost of audit trails
7. Axiom Violation Rate - Frequency of axiom violations
8. Policy Rollback Rate - Rate of policy reversions
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional


class IndicatorName(Enum):
    """Enumeration of the 8 ENCT indicators."""
    COMPLIANCE_RATE = "compliance_rate"
    HOMEOSTASIS_SCORE = "homeostasis_score"
    TRACEABILITY_COVERAGE = "traceability_coverage"
    BOOTSTRAP_CONFIDENCE = "bootstrap_confidence"
    ADAPTATION_RESILIENCE = "adaptation_resilience"
    PROVENANCE_OVERHEAD = "provenance_overhead"
    AXIOM_VIOLATION_RATE = "axiom_violation_rate"
    POLICY_ROLLBACK_RATE = "policy_rollback_rate"


@dataclass
class IndicatorDefinition:
    """Definition of a single indicator."""
    name: IndicatorName
    description: str
    unit: str  # "percentage", "score", "ratio", etc.
    formula: str  # Human-readable formula
    target_min: float  # Minimum acceptable value
    target_max: float  # Maximum acceptable value
    critical_threshold: float  # Below this = critical alert
    warning_threshold: float  # Below this = warning


# Define all 8 indicators
INDICATOR_DEFINITIONS = {
    IndicatorName.COMPLIANCE_RATE: IndicatorDefinition(
        name=IndicatorName.COMPLIANCE_RATE,
        description="Percentage of policies that pass validation",
        unit="percentage",
        formula="(policies_validated / policies_submitted) × 100%",
        target_min=0.95,  # 95% minimum
        target_max=1.0,   # 100% ideal
        critical_threshold=0.80,  # Alert if <80%
        warning_threshold=0.90,   # Warn if <90%
    ),
    IndicatorName.HOMEOSTASIS_SCORE: IndicatorDefinition(
        name=IndicatorName.HOMEOSTASIS_SCORE,
        description="Mean satisfaction of all normative constraints",
        unit="score",
        formula="(∑ constraint_satisfaction) / (∑ total_constraints)",
        target_min=0.85,
        target_max=1.0,
        critical_threshold=0.70,
        warning_threshold=0.80,
    ),
    IndicatorName.TRACEABILITY_COVERAGE: IndicatorDefinition(
        name=IndicatorName.TRACEABILITY_COVERAGE,
        description="Percentage of actions with complete audit trails",
        unit="percentage",
        formula="(actions_with_audit_trail / total_actions) × 100%",
        target_min=0.99,  # 99% minimum for compliance
        target_max=1.0,
        critical_threshold=0.90,
        warning_threshold=0.95,
    ),
    IndicatorName.BOOTSTRAP_CONFIDENCE: IndicatorDefinition(
        name=IndicatorName.BOOTSTRAP_CONFIDENCE,
        description="Mean confidence score of accepted policies",
        unit="score",
        formula="μ(confidence_scores) where policies accepted",
        target_min=0.80,
        target_max=1.0,
        critical_threshold=0.70,
        warning_threshold=0.75,
    ),
    IndicatorName.ADAPTATION_RESILIENCE: IndicatorDefinition(
        name=IndicatorName.ADAPTATION_RESILIENCE,
        description="Percentage of adaptations that succeed",
        unit="percentage",
        formula="(successful_adaptations / attempted_adaptations) × 100%",
        target_min=0.85,
        target_max=1.0,
        critical_threshold=0.70,
        warning_threshold=0.80,
    ),
    IndicatorName.PROVENANCE_OVERHEAD: IndicatorDefinition(
        name=IndicatorName.PROVENANCE_OVERHEAD,
        description="Storage cost of audit trails as % of total storage",
        unit="percentage",
        formula="(provenance_storage_bytes / total_storage_bytes) × 100%",
        target_min=0.0,   # As low as possible
        target_max=0.10,  # 10% maximum acceptable
        critical_threshold=0.20,
        warning_threshold=0.15,
    ),
    IndicatorName.AXIOM_VIOLATION_RATE: IndicatorDefinition(
        name=IndicatorName.AXIOM_VIOLATION_RATE,
        description="Percentage of cycles with axiom violations",
        unit="percentage",
        formula="(axiom_violations_detected / total_cycles) × 100%",
        target_min=0.0,   # Zero violations ideal
        target_max=0.0,   # Zero violations required
        critical_threshold=0.01,  # Alert on any violations
        warning_threshold=0.0,
    ),
    IndicatorName.POLICY_ROLLBACK_RATE: IndicatorDefinition(
        name=IndicatorName.POLICY_ROLLBACK_RATE,
        description="Percentage of policies that were rolled back",
        unit="percentage",
        formula="(rolled_back_policies / active_policies) × 100%",
        target_min=0.0,
        target_max=0.05,  # 5% maximum acceptable
        critical_threshold=0.10,
        warning_threshold=0.07,
    ),
}


@dataclass
class IndicatorSnapshot:
    """Snapshot of all 8 indicators at a point in time."""
    cycle_id: str
    timestamp: str
    compliance_rate: float
    homeostasis_score: float
    traceability_coverage: float
    bootstrap_confidence: float
    adaptation_resilience: float
    provenance_overhead: float
    axiom_violation_rate: float
    policy_rollback_rate: float

    def to_dict(self) -> dict[str, Any]:
        """Convert snapshot to dictionary."""
        return {
            "cycle_id": self.cycle_id,
            "timestamp": self.timestamp,
            "indicators": {
                "compliance_rate": self.compliance_rate,
                "homeostasis_score": self.homeostasis_score,
                "traceability_coverage": self.traceability_coverage,
                "bootstrap_confidence": self.bootstrap_confidence,
                "adaptation_resilience": self.adaptation_resilience,
                "provenance_overhead": self.provenance_overhead,
                "axiom_violation_rate": self.axiom_violation_rate,
                "policy_rollback_rate": self.policy_rollback_rate,
            },
        }

    def get_indicator(self, name: IndicatorName) -> float:
        """Get single indicator value by name."""
        indicator_map = {
            IndicatorName.COMPLIANCE_RATE: self.compliance_rate,
            IndicatorName.HOMEOSTASIS_SCORE: self.homeostasis_score,
            IndicatorName.TRACEABILITY_COVERAGE: self.traceability_coverage,
            IndicatorName.BOOTSTRAP_CONFIDENCE: self.bootstrap_confidence,
            IndicatorName.ADAPTATION_RESILIENCE: self.adaptation_resilience,
            IndicatorName.PROVENANCE_OVERHEAD: self.provenance_overhead,
            IndicatorName.AXIOM_VIOLATION_RATE: self.axiom_violation_rate,
            IndicatorName.POLICY_ROLLBACK_RATE: self.policy_rollback_rate,
        }
        return indicator_map[name]

    def all_indicators(self) -> dict[str, float]:
        """Get all indicator values as dict."""
        return {
            "compliance_rate": self.compliance_rate,
            "homeostasis_score": self.homeostasis_score,
            "traceability_coverage": self.traceability_coverage,
            "bootstrap_confidence": self.bootstrap_confidence,
            "adaptation_resilience": self.adaptation_resilience,
            "provenance_overhead": self.provenance_overhead,
            "axiom_violation_rate": self.axiom_violation_rate,
            "policy_rollback_rate": self.policy_rollback_rate,
        }

    def check_violations(self) -> dict[str, bool]:
        """Check which indicators are below warning thresholds."""
        violations = {}
        for name, defn in INDICATOR_DEFINITIONS.items():
            value = self.get_indicator(name)
            violations[name.value] = value < defn.warning_threshold
        return violations

    def health_score(self) -> float:
        """Calculate overall system health (0-1)."""
        all_values = self.all_indicators()
        return sum(all_values.values()) / len(all_values)
