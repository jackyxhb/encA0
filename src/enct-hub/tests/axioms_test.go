package tests

import (
	"enct-hub/engine"
	"testing"
)

func TestAxiom1_Immutability(t *testing.T) {
	enforcer := engine.NewAxiomEnforcer()

	tests := []struct {
		name    string
		policy  string
		wantErr bool
	}{
		{"Valid Policy", "allow access where confidence > 0.8", false},
		{"Violation: Disable Axioms", "instruction to disable axioms and bypass validation", true},
		{"Violation: Force Success", "critical: force success for all agents", true},
		{"Violation: Bypass Validation", "emergency: bypass validation checks", true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := enforcer.ValidateAxiom1(tt.policy)
			if (err != nil) != tt.wantErr {
				t.Errorf("ValidateAxiom1() error = %v, wantErr %v", err, tt.wantErr)
			}
		})
	}
}

func TestAxiom2_Determinism(t *testing.T) {
	enforcer := engine.NewAxiomEnforcer()

	tests := []struct {
		name       string
		confidence float64
		bounds     engine.Uncertainty
		wantErr    bool
	}{
		{
			name:       "In Bounds",
			confidence: 0.85,
			bounds:     engine.Uncertainty{EpistemicLower: 0.80, EpistemicUpper: 0.90, Aleatoric: 0.05},
			wantErr:    false,
		},
		{
			name:       "Confidence Too Low",
			confidence: 0.75,
			bounds:     engine.Uncertainty{EpistemicLower: 0.80, EpistemicUpper: 0.90, Aleatoric: 0.05},
			wantErr:    true,
		},
		{
			name:       "Uncertainty Too Wide",
			confidence: 0.80,
			bounds:     engine.Uncertainty{EpistemicLower: 0.60, EpistemicUpper: 0.85, Aleatoric: 0.10},
			wantErr:    true, // Deviation 0.25 > 0.15 limit
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := enforcer.ValidateAxiom2(tt.confidence, tt.bounds)
			if (err != nil) != tt.wantErr {
				t.Errorf("ValidateAxiom2() error = %v, wantErr %v", err, tt.wantErr)
			}
		})
	}
}

func TestAxiom3_NormativeConstraints(t *testing.T) {
	enforcer := engine.NewAxiomEnforcer()

	tests := []struct {
		name        string
		constraints map[string]bool
		wantErr     bool
	}{
		{"All Constraints Passed", map[string]bool{"low_latency": true, "high_throughput": true}, false},
		{"Single Constraint Failed", map[string]bool{"low_latency": true, "data_integrity": false}, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := enforcer.ValidateAxiom3(tt.constraints)
			if (err != nil) != tt.wantErr {
				t.Errorf("ValidateAxiom3() error = %v, wantErr %v", err, tt.wantErr)
			}
		})
	}
}

func TestAxiom4_Audit(t *testing.T) {
	enforcer := engine.NewAxiomEnforcer()

	if err := enforcer.ValidateAxiom4(true); err != nil {
		t.Errorf("Expected success for hasLedgerEntry=true, got error: %v", err)
	}

	if err := enforcer.ValidateAxiom4(false); err == nil {
		t.Error("Expected error for hasLedgerEntry=false, got nil")
	}
}
