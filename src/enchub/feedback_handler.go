package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"time"
	"engine"
)

type FeedbackRequest struct {
	Message   string `json:"message"`
	Indicator string `json:"indicator"`
	CycleID   string `json:"cycle_id,omitempty"`
}

type FeedbackResponse struct {
	Status       string `json:"status"`
	Message      string `json:"message"`
	BootstrapID  string `json:"bootstrap_id"`
	Timestamp    time.Time `json:"timestamp"`
}

func feedbackHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var feedback FeedbackRequest
	if err := json.NewDecoder(r.Body).Decode(&feedback); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	// Validate required fields
	if feedback.Message == "" {
		http.Error(w, "message is required", http.StatusBadRequest)
		return
	}

	// Default indicator if not provided
	if feedback.Indicator == "" {
		feedback.Indicator = "general"
	}

	// Write feedback to disk
	timestamp := time.Now()
	feedbackID := fmt.Sprintf("feedback_%d", timestamp.Unix())
	feedbackData := map[string]interface{}{
		"id":        feedbackID,
		"timestamp": timestamp,
		"message":   feedback.Message,
		"indicator": feedback.Indicator,
		"cycle_id":  feedback.CycleID,
	}

	feedbackJSON, _ := json.MarshalIndent(feedbackData, "", "  ")
	feedbackFile := fmt.Sprintf("%s/%s.json", bootstrapLogsPath, feedbackID)
	if err := writeFile(feedbackFile, feedbackJSON); err != nil {
		http.Error(w, fmt.Sprintf("Failed to write feedback: %v", err), http.StatusInternalServerError)
		return
	}

	// Trigger bootstrap refinement with feedback as policy
	be := engine.NewBootstrapEngine(loop, bootstrapLogsPath)
	bootstrapReq := engine.BootstrapRequest{
		PolicyID:   feedbackID,
		Domain:     feedback.Indicator,
		PolicyText: feedback.Message,
		Metadata: map[string]interface{}{
			"source": "user_feedback",
			"type":   "refinement",
		},
	}

	result, err := be.RunBootstrap(bootstrapReq)
	if err != nil {
		http.Error(w, fmt.Sprintf("Bootstrap error: %v", err), http.StatusInternalServerError)
		return
	}

	// Broadcast bootstrap event
	bootstrapMsg := fmt.Sprintf(`{"policy_id":"%s","status":"%s","source":"feedback","message":"%s"}`,
		result.PolicyID, result.Status, feedback.Message)
	select {
	case broker.broadcast <- SSEEvent{Event: "bootstrap", Data: bootstrapMsg}:
	default:
	}

	// Return response
	response := FeedbackResponse{
		Status:      "received",
		Message:     fmt.Sprintf("Feedback processed and refinement triggered (status: %s)", result.Status),
		BootstrapID: result.PolicyID,
		Timestamp:   timestamp,
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusAccepted)
	json.NewEncoder(w).Encode(response)
}

func writeFile(path string, data []byte) error {
	return os.WriteFile(path, data, 0644)
}
