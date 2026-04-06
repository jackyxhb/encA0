package engine

import (
	"math"
	"time"
)

// IndicatorCalculator handles the calculation of the 8 ENCT indicators.
type IndicatorCalculator struct {
	TotalCycles          int
	TotalActions         int
	CompliantActions     int
	TotalLedgerEntries   int
	StateTransitions     int
	SocraticAnswers      int
	RequiredAnswers      int
	TotalFailures        int
	TotalLedgerLatency   time.Duration
	TotalCycleLatency    time.Duration
	TotalAxiomViolations int
	TotalPolicies        int
	TotalRollbacks       int
	
	// Homeostasis state
	TargetStability      float64
	CurrentStability     float64
}

// NewIndicatorCalculator initializes a new calculator with default targets.
func NewIndicatorCalculator() *IndicatorCalculator {
	return &IndicatorCalculator{
		TargetStability: 0.95,
		RequiredAnswers: 4, // Default per Axioms
	}
}

// CalculateSnapshot generates a new IndicatorSnapshot based on the current calculator state.
func (c *IndicatorCalculator) CalculateSnapshot(cycleID string) IndicatorSnapshot {
	indicators := make(map[IndicatorName]float64)

	// 1. Compliance Rate
	if c.TotalActions > 0 {
		indicators[ComplianceRate] = float64(c.CompliantActions) / float64(c.TotalActions)
	} else {
		indicators[ComplianceRate] = 1.0
	}

	// 2. Homeostasis Score
	if c.TargetStability > 0 {
		diff := math.Abs(c.CurrentStability - c.TargetStability)
		score := 1.0 - (diff / c.TargetStability)
		indicators[HomeostasisScore] = math.Max(0, math.Min(1.0, score))
	} else {
		indicators[HomeostasisScore] = 1.0
	}

	// 3. Traceability Coverage
	if c.StateTransitions > 0 {
		coverage := float64(c.TotalLedgerEntries) / float64(c.StateTransitions)
		indicators[TraceabilityCoverage] = math.Min(1.0, coverage)
	} else {
		indicators[TraceabilityCoverage] = 1.0
	}

	// 4. Bootstrap Confidence
	if c.RequiredAnswers > 0 {
		confidence := float64(c.SocraticAnswers) / float64(c.RequiredAnswers)
		indicators[BootstrapConfidence] = math.Min(1.0, confidence)
	} else {
		indicators[BootstrapConfidence] = 1.0
	}

	// 5. Adaptation Resilience
	if c.TotalCycles > 0 {
		resilience := 1.0 - (float64(c.TotalFailures) / float64(c.TotalCycles))
		indicators[AdaptationResilience] = math.Max(0, resilience)
	} else {
		indicators[AdaptationResilience] = 1.0
	}

	// 6. Provenance Overhead
	if c.TotalCycleLatency > 0 {
		overhead := float64(c.TotalLedgerLatency) / float64(c.TotalCycleLatency)
		indicators[ProvenanceOverhead] = math.Min(1.0, overhead)
	} else {
		indicators[ProvenanceOverhead] = 0.05 // Baseline
	}

	// 7. Axiom Violation Rate
	if c.TotalCycles > 0 {
		rate := float64(c.TotalAxiomViolations) / float64(c.TotalCycles)
		indicators[AxiomViolationRate] = math.Min(1.0, rate)
	} else {
		indicators[AxiomViolationRate] = 0.0
	}

	// 8. Policy Rollback Rate
	if c.TotalPolicies > 0 {
		rate := float64(c.TotalRollbacks) / float64(c.TotalPolicies)
		indicators[PolicyRollbackRate] = math.Min(1.0, rate)
	} else {
		indicators[PolicyRollbackRate] = 0.0
	}

	return IndicatorSnapshot{
		CycleID:    cycleID,
		Timestamp:  time.Now(),
		Indicators: indicators,
	}
}

// UpdateState updates the calculator based on the results of a cycle.
func (c *IndicatorCalculator) UpdateState(state *CycleState) {
	c.TotalCycles++
	if state.Status == StatusFailed {
		c.TotalFailures++
	}
	if state.Status == StatusAxiomViolation {
		c.TotalAxiomViolations++
	}

	// Increment metrics based on phases
	if state.SenseOutput != nil {
		c.StateTransitions++
		c.TotalLedgerEntries++ // Assume each phase logs to ledger
	}
	if state.ValidateOutput != nil {
		c.StateTransitions++
		c.TotalLedgerEntries++
		c.TotalActions++
		if state.ValidateOutput.Passed {
			c.CompliantActions++
		}
	}
	if state.ExecuteOutput != nil {
		c.StateTransitions++
		c.TotalLedgerEntries++
	}
	if state.AssessOutput != nil {
		c.StateTransitions++
		c.TotalLedgerEntries++
	}
	if state.ReEnactOutput != nil {
		c.StateTransitions++
		c.TotalLedgerEntries++
		if state.ReEnactOutput.VersionUpdated {
			c.TotalPolicies++
		}
		if state.ReEnactOutput.RollbackDecision != "" {
			c.TotalRollbacks++
		}
	}

	// Update latency
	if !state.StartTime.IsZero() && !state.EndTime.IsZero() {
		cycleDuration := state.EndTime.Sub(state.StartTime)
		c.TotalCycleLatency += cycleDuration
		// Simulate ledger overhead (10ms per log)
		c.TotalLedgerLatency += 10 * time.Millisecond
	}

	// Update CurrentStability as rolling ratio of compliant actions
	if c.TotalActions > 0 {
		stability := float64(c.CompliantActions) / float64(c.TotalActions)
		// Clamp to [0, TargetStability]
		if stability > c.TargetStability {
			c.CurrentStability = c.TargetStability
		} else {
			c.CurrentStability = stability
		}
	}
}
