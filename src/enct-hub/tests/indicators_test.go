package tests

import (
	"enct-hub/engine"
	"testing"
	"time"
)

func TestIndicatorCalculator_ComplianceRate(t *testing.T) {
	calc := engine.NewIndicatorCalculator()
	
	// Initial state (no actions)
	snapshot := calc.CalculateSnapshot("cycle-0")
	if snapshot.Indicators[engine.ComplianceRate] != 1.0 {
		t.Errorf("Expected compliance 1.0 for no actions, got %f", snapshot.Indicators[engine.ComplianceRate])
	}

	// Add compliant and non-compliant actions
	calc.TotalActions = 10
	calc.CompliantActions = 8
	snapshot = calc.CalculateSnapshot("cycle-1")
	if snapshot.Indicators[engine.ComplianceRate] != 0.8 {
		t.Errorf("Expected compliance 0.8, got %f", snapshot.Indicators[engine.ComplianceRate])
	}
}

func TestIndicatorCalculator_HomeostasisScore(t *testing.T) {
	calc := engine.NewIndicatorCalculator()
	calc.TargetStability = 0.95
	calc.CurrentStability = 0.90
	
	snapshot := calc.CalculateSnapshot("cycle-1")
	// diff = 0.05, score = 1.0 - (0.05 / 0.95) = 0.947...
	score := snapshot.Indicators[engine.HomeostasisScore]
	if score < 0.94 || score > 0.95 {
		t.Errorf("Expected Homeostasis score around 0.947, got %f", score)
	}
}

func TestIndicatorCalculator_TraceabilityCoverage(t *testing.T) {
	calc := engine.NewIndicatorCalculator()
	calc.StateTransitions = 20
	calc.TotalLedgerEntries = 18
	
	snapshot := calc.CalculateSnapshot("cycle-1")
	if snapshot.Indicators[engine.TraceabilityCoverage] != 0.9 {
		t.Errorf("Expected Traceability 0.9, got %f", snapshot.Indicators[engine.TraceabilityCoverage])
	}
}

func TestIndicatorCalculator_UpdateState(t *testing.T) {
	calc := engine.NewIndicatorCalculator()
	
	// Mock a successful cycle
	now := time.Now()
	state := &engine.CycleState{
		Status:    engine.StatusComplete,
		StartTime: now.Add(-100 * time.Millisecond),
		EndTime:   now,
		SenseOutput:    &engine.SenseOutput{},
		ValidateOutput: &engine.ValidateOutput{Passed: true},
		ExecuteOutput:  &engine.ExecuteOutput{},
		AssessOutput:   &engine.AssessOutput{},
		ReEnactOutput:  &engine.ReEnactOutput{},
	}
	
	calc.UpdateState(state)
	
	if calc.TotalCycles != 1 {
		t.Errorf("Expected 1 cycle, got %d", calc.TotalCycles)
	}
	if calc.CompliantActions != 1 {
		t.Errorf("Expected 1 compliant action, got %d", calc.CompliantActions)
	}
	if calc.TotalCycleLatency < 100*time.Millisecond {
		t.Errorf("Expected latency >= 100ms, got %v", calc.TotalCycleLatency)
	}
}
