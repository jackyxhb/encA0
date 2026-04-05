package engine

import (
	"math"
	"os"
	"testing"
	"time"
)

func TestIndicator_BootstrapConfidence_WithAnswers(t *testing.T) {
	calc := NewIndicatorCalculator()
	calc.RequiredAnswers = 4
	calc.SocraticAnswers = 3

	snapshot := calc.CalculateSnapshot("test-cycle")

	confidence := snapshot.Indicators[BootstrapConfidence]
	expected := 3.0 / 4.0 // 0.75
	if math.Abs(confidence-expected) > 0.01 {
		t.Errorf("expected BootstrapConfidence ~%.2f, got %.2f", expected, confidence)
	}
}

func TestIndicator_BootstrapConfidence_Capped(t *testing.T) {
	calc := NewIndicatorCalculator()
	calc.RequiredAnswers = 4
	calc.SocraticAnswers = 5

	snapshot := calc.CalculateSnapshot("test-cycle")

	confidence := snapshot.Indicators[BootstrapConfidence]
	if confidence > 1.0 {
		t.Errorf("expected BootstrapConfidence capped at 1.0, got %.2f", confidence)
	}
}

func TestIndicator_AdaptationResilience_WithFailures(t *testing.T) {
	calc := NewIndicatorCalculator()
	calc.TotalCycles = 10
	calc.TotalFailures = 2

	snapshot := calc.CalculateSnapshot("test-cycle")

	resilience := snapshot.Indicators[AdaptationResilience]
	expected := (10.0 - 2.0) / 10.0 // 0.8
	if math.Abs(resilience-expected) > 0.01 {
		t.Errorf("expected AdaptationResilience %.2f, got %.2f", expected, resilience)
	}
}

func TestIndicator_AdaptationResilience_Perfect(t *testing.T) {
	calc := NewIndicatorCalculator()
	calc.TotalCycles = 10
	calc.TotalFailures = 0

	snapshot := calc.CalculateSnapshot("test-cycle")

	resilience := snapshot.Indicators[AdaptationResilience]
	if resilience != 1.0 {
		t.Errorf("expected AdaptationResilience 1.0, got %.2f", resilience)
	}
}

func TestIndicator_ProvenanceOverhead_WithLatency(t *testing.T) {
	calc := NewIndicatorCalculator()
	calc.TotalCycleLatency = 1000 // 1000ms
	calc.TotalLedgerLatency = 100  // 100ms

	snapshot := calc.CalculateSnapshot("test-cycle")

	overhead := snapshot.Indicators[ProvenanceOverhead]
	expected := 100.0 / 1000.0 // 0.1
	if math.Abs(overhead-expected) > 0.01 {
		t.Errorf("expected ProvenanceOverhead %.2f, got %.2f", expected, overhead)
	}
}

func TestIndicator_ProvenanceOverhead_Baseline_WhenNoCycles(t *testing.T) {
	calc := NewIndicatorCalculator()
	// Leave TotalCycleLatency at 0 (default)

	snapshot := calc.CalculateSnapshot("test-cycle")

	overhead := snapshot.Indicators[ProvenanceOverhead]
	// Expected: 5% baseline when no cycles
	if overhead != 0.05 {
		t.Errorf("expected ProvenanceOverhead baseline 0.05, got %.2f", overhead)
	}
}

func TestIndicator_AxiomViolationRate_WithViolations(t *testing.T) {
	calc := NewIndicatorCalculator()
	calc.TotalCycles = 10
	calc.TotalAxiomViolations = 2

	snapshot := calc.CalculateSnapshot("test-cycle")

	violationRate := snapshot.Indicators[AxiomViolationRate]
	expected := 2.0 / 10.0 // 0.2
	if math.Abs(violationRate-expected) > 0.01 {
		t.Errorf("expected AxiomViolationRate %.2f, got %.2f", expected, violationRate)
	}
}

func TestIndicator_AxiomViolationRate_ZeroWhenClean(t *testing.T) {
	calc := NewIndicatorCalculator()
	calc.TotalCycles = 10
	calc.TotalAxiomViolations = 0

	snapshot := calc.CalculateSnapshot("test-cycle")

	violationRate := snapshot.Indicators[AxiomViolationRate]
	if violationRate != 0.0 {
		t.Errorf("expected AxiomViolationRate 0.0, got %.2f", violationRate)
	}
}

func TestIndicator_PolicyRollbackRate_WithRollbacks(t *testing.T) {
	calc := NewIndicatorCalculator()
	calc.TotalPolicies = 5
	calc.TotalRollbacks = 1

	snapshot := calc.CalculateSnapshot("test-cycle")

	rollbackRate := snapshot.Indicators[PolicyRollbackRate]
	expected := 1.0 / 5.0 // 0.2
	if math.Abs(rollbackRate-expected) > 0.01 {
		t.Errorf("expected PolicyRollbackRate %.2f, got %.2f", expected, rollbackRate)
	}
}

func TestIndicator_Snapshot_CycleID_Preserved(t *testing.T) {
	calc := NewIndicatorCalculator()

	snapshot := calc.CalculateSnapshot("my-cycle-123")

	if snapshot.CycleID != "my-cycle-123" {
		t.Errorf("expected CycleID 'my-cycle-123', got '%s'", snapshot.CycleID)
	}
}

func TestIndicator_Snapshot_Timestamp_Recent(t *testing.T) {
	calc := NewIndicatorCalculator()

	before := time.Now()
	snapshot := calc.CalculateSnapshot("test-cycle")
	after := time.Now()

	if snapshot.Timestamp.Before(before) || snapshot.Timestamp.After(after.Add(1*time.Second)) {
		t.Errorf("snapshot timestamp not within expected range")
	}
}

func TestIndicatorCalculator_AxiomViolationRate(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "indicator-test-*")
	defer os.RemoveAll(tmpDir)
	loop, _ := NewFivePhaseLoop(tmpDir)

	// Execute a normal cycle
	state, _ := loop.ExecuteCycle(map[string]interface{}{"action": "test"}, nil)

	// Manually increment violations to simulate axiom violation detection
	if state != nil {
		loop.Calculator.TotalAxiomViolations++
		loop.Calculator.TotalCycles++
	}

	snapshot := loop.GetSnapshot()

	violationRate := snapshot.Indicators[AxiomViolationRate]
	if violationRate <= 0.0 {
		t.Errorf("expected AxiomViolationRate > 0 after increment, got %.2f", violationRate)
	}
}

func TestIndicatorCalculator_PolicyRollbackRate_ViaUpdateState(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "indicator-test-*")
	defer os.RemoveAll(tmpDir)
	loop, _ := NewFivePhaseLoop(tmpDir)

	// Execute a normal cycle
	state, _ := loop.ExecuteCycle(map[string]interface{}{"action": "test"}, nil)

	// Manually set rollback decision
	state.ReEnactOutput.RollbackDecision = "rollback"

	// Update calculator
	loop.Calculator.UpdateState(state)

	snapshot := loop.GetSnapshot()

	rollbackRate := snapshot.Indicators[PolicyRollbackRate]
	if rollbackRate <= 0.0 {
		t.Errorf("expected PolicyRollbackRate > 0 after rollback, got %.2f", rollbackRate)
	}
}
