package main

import (
	"encoding/json"
	"net/http"
	"os"
	"path/filepath"
	"sort"
	"strconv"
	"engine"
)

func auditProvenanceListHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	n := 20
	if nStr := r.URL.Query().Get("n"); nStr != "" {
		if nVal, err := strconv.Atoi(nStr); err == nil && nVal > 0 {
			n = nVal
		}
	}

	entries, err := os.ReadDir(bootstrapLogsPath)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Sort by modification time descending
	sort.Slice(entries, func(i, j int) bool {
		iInfo, _ := entries[i].Info()
		jInfo, _ := entries[j].Info()
		return iInfo.ModTime().After(jInfo.ModTime())
	})

	var bundles []engine.ProvenanceBundle
	for i, entry := range entries {
		if i >= n || !entry.IsDir() {
			continue
		}

		if !contains(entry.Name(), "provenance_") {
			continue
		}

		data, err := os.ReadFile(filepath.Join(bootstrapLogsPath, entry.Name()))
		if err != nil {
			continue
		}

		var bundle engine.ProvenanceBundle
		if err := json.Unmarshal(data, &bundle); err != nil {
			continue
		}

		bundles = append(bundles, bundle)
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(bundles)
}

func auditProvenanceByIDHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	cycleID := r.URL.Query().Get("id")
	if cycleID == "" {
		http.Error(w, "id parameter required", http.StatusBadRequest)
		return
	}

	filePath := filepath.Join(bootstrapLogsPath, "provenance_"+cycleID+".json")
	data, err := os.ReadFile(filePath)
	if err != nil {
		http.Error(w, "Provenance not found", http.StatusNotFound)
		return
	}

	var bundle engine.ProvenanceBundle
	if err := json.Unmarshal(data, &bundle); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(bundle)
}

func auditViolationsHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	n := 10
	if nStr := r.URL.Query().Get("n"); nStr != "" {
		if nVal, err := strconv.Atoi(nStr); err == nil && nVal > 0 {
			n = nVal
		}
	}

	entries, err := os.ReadDir(ledgerPath)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Sort by modification time descending
	sort.Slice(entries, func(i, j int) bool {
		iInfo, _ := entries[i].Info()
		jInfo, _ := entries[j].Info()
		return iInfo.ModTime().After(jInfo.ModTime())
	})

	var violations []map[string]interface{}
	for i, entry := range entries {
		if i >= n || entry.IsDir() {
			continue
		}

		if !contains(entry.Name(), "failure_") {
			continue
		}

		data, err := os.ReadFile(filepath.Join(ledgerPath, entry.Name()))
		if err != nil {
			continue
		}

		var obj map[string]interface{}
		if err := json.Unmarshal(data, &obj); err != nil {
			continue
		}

		violations = append(violations, obj)
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(violations)
}

func contains(s, substr string) bool {
	for i := 0; i < len(s)-len(substr)+1; i++ {
		match := true
		for j := 0; j < len(substr); j++ {
			if s[i+j] != substr[j] {
				match = false
				break
			}
		}
		if match {
			return true
		}
	}
	return false
}
