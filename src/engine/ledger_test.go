package engine

import (
	"encoding/json"
	"os"
	"strings"
	"sync"
	"testing"
)

func TestLedger_WriteEntry_CreatesFile(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "ledger-test-*")
	defer os.RemoveAll(tmpDir)

	writer, _ := NewLedgerWriter(tmpDir)
	state := &CycleState{
		CycleID:      "test-write-1",
		Status:       StatusComplete,
		CurrentPhase: PhaseComplete,
	}

	filename, err := writer.WriteEntry(state)
	if err != nil {
		t.Fatalf("WriteEntry failed: %v", err)
	}

	// Construct full path if relative
	fullPath := filename
	if !strings.HasPrefix(filename, "/") {
		fullPath = tmpDir + "/" + filename
	}

	if _, err := os.Stat(fullPath); err != nil {
		t.Fatalf("file not created: %v", err)
	}
}

func TestLedger_WriteEntry_ValidJSON(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "ledger-test-*")
	defer os.RemoveAll(tmpDir)

	writer, _ := NewLedgerWriter(tmpDir)
	state := &CycleState{
		CycleID:      "test-json-1",
		Status:       StatusComplete,
		CurrentPhase: PhaseComplete,
	}

	filename, _ := writer.WriteEntry(state)
	fullPath := tmpDir + "/" + filename
	data, err := os.ReadFile(fullPath)
	if err != nil {
		t.Fatalf("failed to read file: %v", err)
	}

	var decoded CycleState
	if err := json.Unmarshal(data, &decoded); err != nil {
		t.Fatalf("invalid JSON: %v", err)
	}

	if decoded.CycleID != "test-json-1" {
		t.Errorf("expected CycleID test-json-1, got %s", decoded.CycleID)
	}
}

func TestLedger_WriteEntry_AllPhases(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "ledger-test-*")
	defer os.RemoveAll(tmpDir)

	writer, _ := NewLedgerWriter(tmpDir)

	phases := []LoopPhase{PhaseSense, PhaseValidate, PhaseExecute, PhaseAssess, PhaseReEnact, PhaseComplete}
	for _, phase := range phases {
		state := &CycleState{
			CycleID:      "test-phases",
			Status:       StatusInProgress,
			CurrentPhase: phase,
		}
		writer.WriteEntry(state)
	}

	entries, _ := os.ReadDir(tmpDir)
	if len(entries) < 6 {
		t.Errorf("expected at least 6 phase files, got %d", len(entries))
	}
}

func TestLedger_WriteFailureEntry_CreatesFile(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "ledger-test-*")
	defer os.RemoveAll(tmpDir)

	writer, _ := NewLedgerWriter(tmpDir)
	testErr := &AxiomViolationError{
		AxiomNumber:   1,
		ViolationType: "immutability",
		Message:       "forbidden keyword detected",
	}

	filename, err := writer.WriteFailureEntry("test-failure-1", testErr)
	if err != nil {
		t.Fatalf("WriteFailureEntry failed: %v", err)
	}

	// filename is relative, construct full path
	fullPath := tmpDir + "/" + filename
	if _, err := os.Stat(fullPath); err != nil {
		t.Fatalf("failure file not created: %v", err)
	}
}


func TestLedger_Concurrent_WritesDoNotRace(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "ledger-test-*")
	defer os.RemoveAll(tmpDir)

	writer, _ := NewLedgerWriter(tmpDir)
	var wg sync.WaitGroup

	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			state := &CycleState{
				CycleID: "concurrent-" + string(rune(id+65)),
				Status:  StatusComplete,
			}
			writer.WriteEntry(state)
		}(i)
	}

	wg.Wait()

	entries, _ := os.ReadDir(tmpDir)
	if len(entries) < 10 {
		t.Errorf("expected at least 10 concurrent writes, got %d", len(entries))
	}
}
