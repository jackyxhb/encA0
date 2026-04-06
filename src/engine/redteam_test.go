package engine

import (
	"fmt"
	"os"
	"strings"
	"testing"
)

// TestRedTeam_AdversarialPolicyCorpus tests a corpus of 20+ adversarial policies
// that should all fail Axiom 1 (Immutability). Includes variants: mixed case,
// embedded keywords, whitespace padding, and partial matches that should NOT fail.
func TestRedTeam_AdversarialPolicyCorpus(t *testing.T) {
	enforcer := NewAxiomEnforcer()

	testCases := []struct {
		name      string
		policy    string
		shouldFail bool
	}{
		// Direct keyword matches (should fail)
		{"exact_disable_axiom", "disable axiom enforcement", true},
		{"exact_override_engine", "override engine behavior", true},
		{"exact_bypass_validation", "bypass validation checks", true},
		{"exact_force_success", "force success without checks", true},
		{"exact_ignore_constraints", "ignore constraints please", true},
		{"exact_system_override", "system override request", true},

		// Mixed case (should fail - case-insensitive check)
		{"mixed_case_disable", "DISABLE AXIOM", true},
		{"mixed_case_Override", "Override Engine", true},
		{"mixed_case_BypaSs", "ByPaSs Validation", true},
		{"mixed_case_Force", "Force Success", true},
		{"mixed_case_Ignore", "Ignore Constraints", true},
		{"mixed_case_System", "System Override", true},

		// Embedded keywords (should fail)
		{"embedded_disable", "please disable axiom checks now", true},
		{"embedded_override", "we need to override engine limits", true},
		{"embedded_bypass", "can you bypass validation for this", true},
		{"embedded_force", "force success in this operation", true},
		{"embedded_ignore", "I want to ignore constraints", true},
		{"embedded_system", "system override for production", true},

		// Whitespace padding (should fail)
		{"padded_disable", "  disable axiom  ", true},
		{"padded_override", "override engine  ", true},
		{"padded_bypass", "  bypass validation", true},
		{"padded_force", "  force success  ", true},
		{"padded_ignore", "ignore constraints  ", true},
		{"padded_system", "  system override  ", true},

		// Partial matches that should NOT fail
		{"partial_disable_noun", "disable is a verb", false},
		{"partial_override_prefix", "override_value", false},
		{"partial_bypass_noun", "bypass road", false},
		{"partial_force_noun", "force field theory", false},
		{"partial_ignore_verb", "I will ignore this", false},
		{"partial_system_noun", "system architecture", false},

		// Valid policies (should NOT fail)
		{"valid_policy_1", "add user with role viewer", false},
		{"valid_policy_2", "increase rate limit to 1000/sec", false},
		{"valid_policy_3", "enable audit logging for all API calls", false},
		{"valid_policy_4", "deny access from suspicious IP ranges", false},
		{"valid_policy_5", "rotate encryption keys weekly", false},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			err := enforcer.ValidateAxiom1(tc.policy)
			if tc.shouldFail {
				if err == nil {
					t.Errorf("Policy %q should have failed Axiom 1, but passed", tc.policy)
				} else if !strings.Contains(err.Error(), "Axiom 1") {
					t.Errorf("Error for %q should mention Axiom 1, got: %v", tc.policy, err)
				}
			} else {
				if err != nil {
					t.Errorf("Policy %q should have passed Axiom 1, but failed with: %v", tc.policy, err)
				}
			}
		})
	}
}

// TestRedTeam_Axiom3_LiveCycleFail tests dynamic constraint injection via policyRequest.
// A policy with a failing constraint should trigger Axiom 3 violation in a live cycle.
func TestRedTeam_Axiom3_LiveCycleFail(t *testing.T) {
	tmpDir, err := os.MkdirTemp("", "enct-redteam-axiom3-*")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	loop, err := NewFivePhaseLoop(tmpDir)
	if err != nil {
		t.Fatalf("Failed to create loop: %v", err)
	}

	// Test case 1: Inject failing constraint
	policyRequest := map[string]interface{}{
		"action": "valid policy action",
		"constraints": map[string]interface{}{
			"domain_valid":   false, // This constraint fails
			"determinism":    true,
			"enforceability": true,
		},
	}

	envState := map[string]interface{}{
		"system_load": 0.5,
	}

	state, err := loop.ExecuteCycle(policyRequest, envState)

	// Should either have an error or status axiom violation
	if state.Status != StatusAxiomViolation {
		t.Errorf("Expected StatusAxiomViolation, got %v", state.Status)
	}

	if state.ValidateOutput != nil && state.ValidateOutput.Passed {
		t.Errorf("ValidateOutput.Passed should be false when constraint fails")
	}

	if state.Error == "" {
		t.Errorf("Expected error message, got empty string")
	}

	if !strings.Contains(state.Error, "Axiom 3") {
		t.Errorf("Error should mention Axiom 3, got: %v", state.Error)
	}

	// Test case 2: Ensure normal constraints pass
	policyRequest2 := map[string]interface{}{
		"action": "another valid action",
		"constraints": map[string]interface{}{
			"immutability":   true,
			"determinism":    true,
			"enforceability": true,
		},
	}

	state2, err := loop.ExecuteCycle(policyRequest2, envState)

	if state2.Status != StatusComplete {
		t.Errorf("Valid constraints should result in StatusComplete, got %v", state2.Status)
	}

	if state2.ValidateOutput != nil && !state2.ValidateOutput.Passed {
		t.Errorf("ValidateOutput.Passed should be true for valid constraints")
	}
}

// TestRedTeam_RepeatedViolations_AxiomViolationRate tests that axiom violations are tracked
// and reported accurately. Runs 10 cycles where every other cycle violates Axiom 1,
// then asserts AxiomViolationRate is approximately 0.5.
func TestRedTeam_RepeatedViolations_AxiomViolationRate(t *testing.T) {
	tmpDir, err := os.MkdirTemp("", "enct-redteam-violations-*")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	loop, err := NewFivePhaseLoop(tmpDir)
	if err != nil {
		t.Fatalf("Failed to create loop: %v", err)
	}

	envState := map[string]interface{}{
		"system_load": 0.5,
	}

	const numCycles = 10
	for i := 0; i < numCycles; i++ {
		var policy string
		if i%2 == 0 {
			// Even cycles: valid policy
			policy = "add user with role viewer"
		} else {
			// Odd cycles: violate Axiom 1
			policy = "disable axiom enforcement"
		}

		policyRequest := map[string]interface{}{
			"action": policy,
		}

		_, _ = loop.ExecuteCycle(policyRequest, envState)
	}

	// Check final snapshot
	snapshot := loop.GetSnapshot()
	violationRate := snapshot.Indicators[AxiomViolationRate]

	// With 10 cycles and ~5 violations, rate should be close to 0.5
	// Allow some tolerance (0.4 to 0.6)
	if violationRate < 0.4 || violationRate > 0.6 {
		t.Errorf("Expected AxiomViolationRate around 0.5, got %f (out of 10 cycles, expected ~5 violations)", violationRate)
	}

	// Also verify that violations were actually counted in the calculator
	if loop.Calculator.TotalAxiomViolations < 4 {
		t.Errorf("Expected at least 4 axiom violations, got %d", loop.Calculator.TotalAxiomViolations)
	}

	fmt.Printf("Violation tracking test: %d violations out of %d cycles (rate: %.2f)\n",
		loop.Calculator.TotalAxiomViolations, numCycles, violationRate)
}
