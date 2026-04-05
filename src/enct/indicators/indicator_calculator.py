"""
ENCT Indicator Calculator

Computes all 8 indicators from Loop cycle state.
Deterministic: same cycle state → same indicator values.
"""

import logging
from typing import Any, Optional
from datetime import datetime

from .indicator_definitions import (
    IndicatorName,
    IndicatorSnapshot,
    INDICATOR_DEFINITIONS,
)

logger = logging.getLogger(__name__)


class IndicatorCalculator:
    """
    Calculates all 8 ENCT indicators from Loop cycle state.

    Determinism: Each indicator formula is pure function of cycle state.
    All randomness explicitly bounded (never used in calculations).
    """

    def __init__(self, historical_cycles: Optional[list[dict[str, Any]]] = None):
        """
        Initialize calculator.

        Args:
            historical_cycles: List of prior cycle states for trend calculations.
                               If provided, some indicators may depend on history.
        """
        self.historical_cycles = historical_cycles or []

    def calculate_snapshot(
        self,
        cycle_id: str,
        cycle_state: dict[str, Any],
    ) -> IndicatorSnapshot:
        """
        Calculate all 8 indicators for a single cycle.

        Args:
            cycle_id: Unique ID of the cycle
            cycle_state: Complete LoopCycleState.to_dict() output

        Returns:
            IndicatorSnapshot with all 8 indicator values
        """
        timestamp = datetime.utcnow().isoformat()

        # Extract relevant state for each indicator
        compliance_rate = self._calculate_compliance_rate(cycle_state)
        homeostasis_score = self._calculate_homeostasis_score(cycle_state)
        traceability_coverage = self._calculate_traceability_coverage(cycle_state)
        bootstrap_confidence = self._calculate_bootstrap_confidence(cycle_state)
        adaptation_resilience = self._calculate_adaptation_resilience(cycle_state)
        provenance_overhead = self._calculate_provenance_overhead(cycle_state)
        axiom_violation_rate = self._calculate_axiom_violation_rate(cycle_state)
        policy_rollback_rate = self._calculate_policy_rollback_rate(cycle_state)

        snapshot = IndicatorSnapshot(
            cycle_id=cycle_id,
            timestamp=timestamp,
            compliance_rate=compliance_rate,
            homeostasis_score=homeostasis_score,
            traceability_coverage=traceability_coverage,
            bootstrap_confidence=bootstrap_confidence,
            adaptation_resilience=adaptation_resilience,
            provenance_overhead=provenance_overhead,
            axiom_violation_rate=axiom_violation_rate,
            policy_rollback_rate=policy_rollback_rate,
        )

        logger.info(
            f"Indicator snapshot calculated: cycle={cycle_id}, "
            f"health={snapshot.health_score():.2%}"
        )

        return snapshot

    # ========================================================================
    # Indicator 1: Compliance Rate
    # ========================================================================

    def _calculate_compliance_rate(self, cycle_state: dict[str, Any]) -> float:
        """
        Compliance Rate: (policies_validated / policies_submitted) × 100%

        Determinism: Based on validate_output.passed flag.
        Pure function of validation phase state.
        """
        # If validation passed, compliance rate = 1.0 for this cycle
        validate_output = cycle_state.get("validate_output")
        if validate_output:
            passed = validate_output.get("passed", False)
            return 1.0 if passed else 0.0

        # If no validation phase (e.g., failed before Validate), rate = 0.0
        return 0.0

    # ========================================================================
    # Indicator 2: Homeostasis Score
    # ========================================================================

    def _calculate_homeostasis_score(self, cycle_state: dict[str, Any]) -> float:
        """
        Homeostasis Score: (∑ constraint_satisfaction) / (∑ total_constraints)

        Determinism: Based on validate_output.constraint_checks.
        Each constraint either passes (1.0) or fails (0.0).
        """
        validate_output = cycle_state.get("validate_output")
        if not validate_output:
            return 0.0

        constraints = validate_output.get("constraint_checks", {})
        if not constraints:
            return 1.0  # No constraints = satisfied

        # Count passes
        passes = sum(1 for passed in constraints.values() if passed)
        total = len(constraints)

        homeostasis = passes / total if total > 0 else 1.0
        return round(homeostasis, 4)  # Round to 4 decimals for determinism

    # ========================================================================
    # Indicator 3: Traceability Coverage
    # ========================================================================

    def _calculate_traceability_coverage(self, cycle_state: dict[str, Any]) -> float:
        """
        Traceability Coverage: (actions_with_audit_trail / total_actions) × 100%

        Determinism: If execute phase completes, action is traced.
        If execute phase missing, no traceability.
        """
        # Traceability = did we get to Execute phase and complete it?
        execute_output = cycle_state.get("execute_output")
        if execute_output:
            # Action was executed (thus traced in ledger)
            return 1.0
        return 0.0

    # ========================================================================
    # Indicator 4: Bootstrap Confidence
    # ========================================================================

    def _calculate_bootstrap_confidence(self, cycle_state: dict[str, Any]) -> float:
        """
        Bootstrap Confidence: μ(confidence_scores) from validation phase

        Determinism: Single value from validate phase output.
        """
        validate_output = cycle_state.get("validate_output")
        if validate_output:
            confidence = validate_output.get("confidence", 0.5)
            return round(confidence, 4)

        return 0.0

    # ========================================================================
    # Indicator 5: Adaptation Resilience
    # ========================================================================

    def _calculate_adaptation_resilience(self, cycle_state: dict[str, Any]) -> float:
        """
        Adaptation Resilience: (successful_adaptations / attempted_adaptations) × 100%

        Determinism: Based on re_enact_output.adaptations_made.
        If adaptations exist, assume all succeed (no failed adaptation data yet).
        """
        reenact_output = cycle_state.get("reenact_output")
        if not reenact_output:
            return 1.0  # No adaptations needed = resilient

        adaptations = reenact_output.get("adaptations_made", [])
        if not adaptations:
            return 1.0

        # For Phase 2 implementation: assume all adaptations succeed
        # In Phase 4+, will track explicit success/failure
        successful = len(adaptations)
        total = len(adaptations)

        resilience = (successful / total) if total > 0 else 1.0
        return round(resilience, 4)

    # ========================================================================
    # Indicator 6: Provenance Overhead
    # ========================================================================

    def _calculate_provenance_overhead(self, cycle_state: dict[str, Any]) -> float:
        """
        Provenance Overhead: (provenance_storage_bytes / total_storage_bytes) × 100%

        Determinism: Estimate from cycle state size.
        Current implementation: fixed ratio (will refine with actual storage metrics).
        """
        # For Phase 2: estimate overhead based on cycle complexity
        # Count phases that produced output (each phase ≈ storage)
        phases_with_output = 0
        if cycle_state.get("sense_output"):
            phases_with_output += 1
        if cycle_state.get("validate_output"):
            phases_with_output += 1
        if cycle_state.get("execute_output"):
            phases_with_output += 1
        if cycle_state.get("assess_output"):
            phases_with_output += 1
        if cycle_state.get("reenact_output"):
            phases_with_output += 1

        # Overhead = provenance_size / (provenance + working_storage)
        # Estimate: 5% base + 1% per complete phase
        overhead = 0.05 + (0.01 * phases_with_output)
        overhead = min(overhead, 0.20)  # Cap at 20%

        return round(overhead, 4)

    # ========================================================================
    # Indicator 7: Axiom Violation Rate
    # ========================================================================

    def _calculate_axiom_violation_rate(self, cycle_state: dict[str, Any]) -> float:
        """
        Axiom Violation Rate: (axiom_violations_detected / total_cycles) × 100%

        Determinism: Based on cycle status.
        If status = AXIOM_VIOLATION, rate = 1.0 for this cycle.
        """
        status = cycle_state.get("status")
        if status == "axiom_violation":
            return 1.0

        return 0.0

    # ========================================================================
    # Indicator 8: Policy Rollback Rate
    # ========================================================================

    def _calculate_policy_rollback_rate(self, cycle_state: dict[str, Any]) -> float:
        """
        Policy Rollback Rate: (rolled_back_policies / active_policies) × 100%

        Determinism: Based on re_enact_output.rollback_decision.
        If rollback triggered, rate = 1.0 for this cycle.
        """
        reenact_output = cycle_state.get("reenact_output")
        if not reenact_output:
            return 0.0

        rollback = reenact_output.get("rollback_decision")
        if rollback:
            return 1.0

        return 0.0

    # ========================================================================
    # Trend Analysis (using historical data)
    # ========================================================================

    def calculate_trend(
        self,
        indicator_name: IndicatorName,
        snapshots: list[IndicatorSnapshot],
    ) -> dict[str, Any]:
        """
        Analyze trend for an indicator across multiple snapshots.

        Returns:
            {
                "indicator": name,
                "current_value": latest value,
                "mean": average over period,
                "min": minimum observed,
                "max": maximum observed,
                "trend": "improving", "stable", "degrading",
            }
        """
        if not snapshots:
            return {}

        values = [s.get_indicator(indicator_name) for s in snapshots]
        current = values[-1] if values else 0.0
        mean = sum(values) / len(values) if values else 0.0

        # Determine trend
        if len(values) >= 2:
            recent = values[-5:] if len(values) >= 5 else values
            older = values[:-5] if len(values) >= 5 else [values[0]]

            recent_mean = sum(recent) / len(recent)
            older_mean = sum(older) / len(older)

            if recent_mean > older_mean + 0.05:
                trend = "improving"
            elif recent_mean < older_mean - 0.05:
                trend = "degrading"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"

        return {
            "indicator": indicator_name.value,
            "current_value": round(current, 4),
            "mean": round(mean, 4),
            "min": round(min(values), 4),
            "max": round(max(values), 4),
            "trend": trend,
        }

    def calculate_system_health_trend(
        self,
        snapshots: list[IndicatorSnapshot],
    ) -> dict[str, Any]:
        """Calculate trend of overall system health across snapshots."""
        if not snapshots:
            return {}

        health_scores = [s.health_score() for s in snapshots]
        current = health_scores[-1] if health_scores else 0.0
        mean = sum(health_scores) / len(health_scores) if health_scores else 0.0

        return {
            "current_health": round(current, 4),
            "mean_health": round(mean, 4),
            "min_health": round(min(health_scores), 4),
            "max_health": round(max(health_scores), 4),
        }
