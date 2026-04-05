package engine

import (
	"errors"
	"fmt"
	"time"
	"github.com/google/uuid"
)

// FivePhaseLoop orchestrates the ENCT cycle.
type FivePhaseLoop struct {
	Calculator *IndicatorCalculator
	Enforcer   *AxiomEnforcer
	Ledger     *LedgerWriter
}

// NewFivePhaseLoop initializes the engine.
func NewFivePhaseLoop(rootPath string) (*FivePhaseLoop, error) {
	lw, err := NewLedgerWriter(rootPath)
	if err != nil {
		return nil, err
	}
	return &FivePhaseLoop{
		Calculator: NewIndicatorCalculator(),
		Enforcer:   NewAxiomEnforcer(),
		Ledger:     lw,
	}, nil
}

// ExecuteCycle runs a complete Sense-Validate-Execute-Assess-ReEnact cycle.
func (l *FivePhaseLoop) ExecuteCycle(policyRequest map[string]interface{}, envState map[string]interface{}) (*CycleState, error) {
	cycleID := uuid.New().String()
	state := &CycleState{
		CycleID:     cycleID,
		Status:      StatusInProgress,
		StartTime:   time.Now(),
		SenseOutput: &SenseOutput{
			Timestamp:     time.Now(),
			Observations:  envState,
			PolicyRequest: policyRequest,
		},
	}

	defer func() {
		state.EndTime = time.Now()
		l.Calculator.UpdateState(state)
	}()

	fmt.Printf("[%s] Starting Sense phase\n", cycleID)

	// Phase 1: Sense (observation complete)
	state.CurrentPhase = PhaseSense
	if _, err := l.Ledger.WriteEntry(state); err != nil {
		return nil, l.handleError(state, err)
	}

	// Phase 2: Validate
	state.CurrentPhase = PhaseValidate
	policy, _ := policyRequest["command"].(string)
	
	// Axiom 1: Immutability
	if err := l.Enforcer.ValidateAxiom1(policy); err != nil {
		return state, l.handleError(state, err)
	}

	fmt.Printf("[%s] Starting Validate phase\n", cycleID)

	// Axiom 2: Determinism (Simulated bounds for now)
	valOutput := &ValidateOutput{
		Timestamp:  time.Now(),
		Confidence: 0.90,
		UncertaintyBounds: Uncertainty{
			EpistemicLower: 0.85,
			EpistemicUpper: 0.95,
			Aleatoric:      0.02,
		},
		ConstraintChecks: map[string]bool{
			"immutability":   true,
			"determinism":    true,
			"enforceability": true,
		},
		Passed: true,
	}

	if err := l.Enforcer.ValidateAxiom2(valOutput.Confidence, valOutput.UncertaintyBounds); err != nil {
		valOutput.Passed = false
		state.ValidateOutput = valOutput
		return state, l.handleError(state, err)
	}

	// Axiom 3: Normative Constraints
	if err := l.Enforcer.ValidateAxiom3(valOutput.ConstraintChecks); err != nil {
		valOutput.Passed = false
		state.ValidateOutput = valOutput
		return state, l.handleError(state, err)
	}

	state.ValidateOutput = valOutput
	if _, err := l.Ledger.WriteEntry(state); err != nil {
		return state, l.handleError(state, err)
	}

	// Phase 3: Execute
	state.CurrentPhase = PhaseExecute
	executeOutput := &ExecuteOutput{
		Timestamp:   time.Now(),
		ActionTaken: fmt.Sprintf("Executing command: %s", policy),
		Outcome:     "SUCCESS",
		SideEffects: []string{"State transition recorded", "Ledger updated"},
	}
	state.ExecuteOutput = executeOutput
	if _, err := l.Ledger.WriteEntry(state); err != nil {
		return state, l.handleError(state, err)
	}

	// Phase 4: Assess
	state.CurrentPhase = PhaseAssess
	snapshot := l.Calculator.CalculateSnapshot(cycleID)
	assessOutput := &AssessOutput{
		Timestamp:    time.Now(),
		Metrics:      snapshot.Indicators,
		SystemHealth: snapshot.Indicators[HomeostasisScore],
	}
	state.AssessOutput = assessOutput
	if _, err := l.Ledger.WriteEntry(state); err != nil {
		return state, l.handleError(state, err)
	}

	// Phase 5: Re-Enact
	state.CurrentPhase = PhaseReEnact
	reEnactOutput := &ReEnactOutput{
		Timestamp:      time.Now(),
		VersionUpdated: true,
	}
	state.ReEnactOutput = reEnactOutput
	if _, err := l.Ledger.WriteEntry(state); err != nil {
		return state, l.handleError(state, err)
	}

	state.Status = StatusComplete
	state.CurrentPhase = PhaseComplete
	return state, nil
}

// GetSnapshot returns the current system indicators.
func (l *FivePhaseLoop) GetSnapshot() IndicatorSnapshot {
	return l.Calculator.CalculateSnapshot("latest")
}

func (l *FivePhaseLoop) handleError(state *CycleState, err error) error {
	state.Error = err.Error()
	state.ErrorPhase = state.CurrentPhase

	var axiomErr *AxiomViolationError
	if errors.As(err, &axiomErr) {
		state.Status = StatusAxiomViolation
	} else {
		state.Status = StatusFailed
	}

	l.Ledger.WriteFailureEntry(state.CycleID, err)
	return err
}
