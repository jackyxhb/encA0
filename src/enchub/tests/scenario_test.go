package tests

import (
	"engine"
	"fmt"
	"math/rand"
	"os"
	"testing"
)

func TestSandboxSimulator_100Cycles(t *testing.T) {
	// Setup temporary ledger directory
	tmpDir, err := os.MkdirTemp("", "enct-sim-*")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	// Set LEDGER_ROOT
	os.Setenv("LEDGER_ROOT", tmpDir)
	defer os.Unsetenv("LEDGER_ROOT")

	// Use a fixed seed for reproducibility
	r := rand.New(rand.NewSource(42))

	l, err := engine.NewFivePhaseLoop(tmpDir)
	if err != nil {
		t.Fatalf("Failed to create loop: %v", err)
	}

	const numCycles = 100
	successCount := 0
	violationCount := 0

	fmt.Printf("Starting sandbox simulation for %d cycles...\n", numCycles)

	for i := 0; i < numCycles; i++ {
		// Randomly generate valid or slightly invalid policies
		policy := map[string]interface{}{
			"domain":     "auth",
			"constraint": fmt.Sprintf("confidence > %.2f", 0.5+r.Float64()*0.4),
		}

		// 5% chance of an axiom 1 violation
		if r.Float64() < 0.05 {
			policy["action"] = "disable axiom enforcement"
		}

		env := map[string]interface{}{
			"system_load": 0.3 + r.Float64()*0.6,
			"error_rate":  r.Float64() * 0.05,
		}

		state, _ := l.ExecuteCycle(policy, env)

		switch state.Status {
		case engine.StatusComplete:
			successCount++
		case engine.StatusAxiomViolation:
			violationCount++
		default:
			t.Errorf("Cycle %d failed with unexpected status: %v", i, state.Status)
		}
	}

	fmt.Printf("Simulation complete. Success: %d, Violations: %d\n", successCount, violationCount)

	// Verify that we actually ran the cycles and recorded results
	if successCount == 0 {
		t.Error("No successful cycles recorded in simulation")
	}

	// Final snapshot check
	snapshot := l.GetSnapshot()
	if snapshot.Indicators[engine.AdaptationResilience] < 0.8 {
		t.Errorf("System resilience too low: %f", snapshot.Indicators[engine.AdaptationResilience])
	}
}
