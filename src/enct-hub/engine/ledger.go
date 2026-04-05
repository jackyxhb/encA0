package engine

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sync"
	"time"
)

// LedgerWriter handles synchronous cycle logging to disk.
type LedgerWriter struct {
	RootPath string
	mu       sync.Mutex
}

// NewLedgerWriter creates a new writer for the given directory.
func NewLedgerWriter(root string) (*LedgerWriter, error) {
	if root == "" {
		root = "ledger"
	}
	err := os.MkdirAll(root, 0755)
	if err != nil {
		return nil, err
	}
	return &LedgerWriter{RootPath: root}, nil
}

// WriteEntry saves a cycle state to a JSON file.
func (w *LedgerWriter) WriteEntry(state *CycleState) (string, error) {
	w.mu.Lock()
	defer w.mu.Unlock()

	filename := fmt.Sprintf("cycle_%s_phase_%s.json", state.CycleID, state.CurrentPhase)
	filePath := filepath.Join(w.RootPath, filename)

	data, err := json.MarshalIndent(state, "", "  ")
	if err != nil {
		return "", err
	}

	err = os.WriteFile(filePath, data, 0644)
	if err != nil {
		return "", err
	}

	return filename, nil
}

// WriteFailureEntry logs an error entry.
func (w *LedgerWriter) WriteFailureEntry(cycleID string, err error) (string, error) {
	w.mu.Lock()
	defer w.mu.Unlock()

	filename := fmt.Sprintf("failure_%s_%d.json", cycleID, time.Now().Unix())
	filePath := filepath.Join(w.RootPath, filename)

	data := map[string]interface{}{
		"cycle_id": cycleID,
		"timestamp": time.Now(),
		"error_message": err.Error(),
	}

	raw, _ := json.MarshalIndent(data, "", "  ")
	os.WriteFile(filePath, raw, 0644)

	return filename, nil
}
