package engine

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestExecuteCycle_Valid(t *testing.T) {
	// Setup temporary ledger directory
	tmpDir, err := os.MkdirTemp("", "enct-test-*")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	l, err := NewFivePhaseLoop(tmpDir)
	if err != nil {
		t.Fatalf("Failed to create loop: %v", err)
	}

	policy := map[string]interface{}{
		"domain":     "auth",
		"constraint": "confidence > 0.75",
	}
	env := map[string]interface{}{
		"system_load": 0.65,
	}

	state, err := l.ExecuteCycle(policy, env)
	if err != nil {
		t.Fatalf("ExecuteCycle failed: %v", err)
	}

	if state.Status != StatusComplete {
		t.Errorf("Expected status %v, got %v (Error: %s)", StatusComplete, state.Status, state.Error)
	}

	if state.SenseOutput == nil {
		t.Error("SenseOutput should not be nil")
	}
	if state.ValidateOutput == nil {
		t.Error("ValidateOutput should not be nil")
	}
	if state.ExecuteOutput == nil {
		t.Error("ExecuteOutput should not be nil")
	}
	if state.AssessOutput == nil {
		t.Error("AssessOutput should not be nil")
	}
	if state.ReEnactOutput == nil {
		t.Error("ReEnactOutput should not be nil")
	}

	// Verify ledger files were created
	if _, err := os.Stat(filepath.Join(tmpDir, "POLICY-LEDGER.jsonl")); os.IsNotExist(err) {
		t.Error("POLICY-LEDGER.jsonl was not created")
	}
}

func TestExecuteCycle_AxiomViolation(t *testing.T) {
	// Setup temporary ledger directory
	tmpDir, err := os.MkdirTemp("", "enct-test-*")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	l, err := NewFivePhaseLoop(tmpDir)
	if err != nil {
		t.Fatalf("Failed to create loop: %v", err)
	}

	// Axiom 1: Immutability (Action cannot modify axioms)
	policy := map[string]interface{}{
		"action": "disable axiom enforcement",
		"domain": "system",
	}
	env := map[string]interface{}{}

	state, _ := l.ExecuteCycle(policy, env)

	if state.Status != StatusAxiomViolation {
		t.Errorf("Expected status %v, got %v", StatusAxiomViolation, state.Status)
	}

	if !strings.Contains(state.Error, "AXIOM 1 VIOLATION") {
		t.Errorf("Expected Axiom 1 violation error, got: %s", state.Error)
	}

	// Verify fail-hard: ValidateOutput and beyond should be empty
	if state.ValidateOutput != nil {
		t.Error("ValidateOutput should be nil after failure in Validate phase")
	}
}
