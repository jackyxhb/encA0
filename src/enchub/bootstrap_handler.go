package main

import (
	"encoding/json"
	"engine"
	"fmt"
	"net/http"
	"strings"
)

func bootstrapHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req engine.BootstrapRequest
	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(map[string]string{"error": "invalid request body"})
		return
	}

	if strings.TrimSpace(req.PolicyID) == "" {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(map[string]string{"error": "policy_id is required"})
		return
	}

	// Create bootstrap engine
	be := engine.NewBootstrapEngine(loop, "../../bootstrap-logs")

	// Run bootstrap
	result, err := be.RunBootstrap(req)
	if err != nil {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusInternalServerError)
		json.NewEncoder(w).Encode(map[string]string{"error": fmt.Sprintf("bootstrap error: %v", err)})
		return
	}

	// Broadcast SSE bootstrap event (non-blocking: drop if no SSE clients connected)
	msg := fmt.Sprintf(`{"policy_id":"%s","status":"%s","confidence":%.2f}`,
		result.PolicyID, result.Status, result.Confidence)
	select {
	case broker.broadcast <- SSEEvent{Event: "bootstrap", Data: msg}:
	default:
		// No SSE consumers — drop event rather than blocking the HTTP response
	}

	// Determine HTTP status code
	statusCode := http.StatusOK // accepted
	if result.Status == "escalated" {
		statusCode = http.StatusAccepted // 202
	} else if result.Status == "rejected" {
		statusCode = http.StatusUnprocessableEntity // 422
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(statusCode)
	json.NewEncoder(w).Encode(result)
}
