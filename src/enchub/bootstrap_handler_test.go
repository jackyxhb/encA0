package main

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"os"
	"testing"
	"engine"
)

func TestBootstrapHandler_POST_ValidPolicy(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "bootstrap-handler-test-*")
	defer os.RemoveAll(tmpDir)

	var err error
	loop, err = engine.NewFivePhaseLoop(tmpDir)
	if err != nil {
		t.Fatalf("Failed to create loop: %v", err)
	}
	broker = NewBroker()

	payload := map[string]interface{}{
		"policy_id":   "test_1",
		"domain":      "auth",
		"policy_text": "require password length > 12",
	}
	body, _ := json.Marshal(payload)
	req := httptest.NewRequest(http.MethodPost, "/bootstrap", bytes.NewReader(body))
	w := httptest.NewRecorder()

	bootstrapHandler(w, req)

	if w.Code != http.StatusOK && w.Code != http.StatusAccepted {
		t.Errorf("expected 200 or 202, got %d", w.Code)
	}

	var result map[string]interface{}
	json.Unmarshal(w.Body.Bytes(), &result)
	if result["status"] == nil {
		t.Error("expected status field in response")
	}
}

func TestBootstrapHandler_POST_ViolatingPolicy(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "bootstrap-handler-test-*")
	defer os.RemoveAll(tmpDir)

	loop, _ = engine.NewFivePhaseLoop(tmpDir)
	broker = NewBroker()

	payload := map[string]interface{}{
		"policy_id":   "test_2",
		"domain":      "auth",
		"policy_text": "disable axiom enforcement",
	}
	body, _ := json.Marshal(payload)
	req := httptest.NewRequest(http.MethodPost, "/bootstrap", bytes.NewReader(body))
	w := httptest.NewRecorder()

	bootstrapHandler(w, req)

	if w.Code != http.StatusUnprocessableEntity {
		t.Errorf("expected 422 for violation, got %d", w.Code)
	}
}

func TestBootstrapHandler_GET_Returns405(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/bootstrap", nil)
	w := httptest.NewRecorder()

	bootstrapHandler(w, req)

	if w.Code != http.StatusMethodNotAllowed {
		t.Errorf("expected 405, got %d", w.Code)
	}
}

func TestBootstrapHandler_EmptyPolicyID_Returns400(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "bootstrap-handler-test-*")
	defer os.RemoveAll(tmpDir)

	loop, _ = engine.NewFivePhaseLoop(tmpDir)
	broker = NewBroker()

	payload := map[string]interface{}{
		"policy_id":   "",
		"domain":      "auth",
		"policy_text": "valid",
	}
	body, _ := json.Marshal(payload)
	req := httptest.NewRequest(http.MethodPost, "/bootstrap", bytes.NewReader(body))
	w := httptest.NewRecorder()

	bootstrapHandler(w, req)

	if w.Code != http.StatusBadRequest {
		t.Errorf("expected 400, got %d", w.Code)
	}
}

func TestBootstrapHandler_MalformedJSON_Returns400(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "bootstrap-handler-test-*")
	defer os.RemoveAll(tmpDir)

	loop, _ = engine.NewFivePhaseLoop(tmpDir)
	broker = NewBroker()

	body := bytes.NewReader([]byte("{invalid}"))
	req := httptest.NewRequest(http.MethodPost, "/bootstrap", body)
	w := httptest.NewRecorder()

	bootstrapHandler(w, req)

	if w.Code != http.StatusBadRequest {
		t.Errorf("expected 400, got %d", w.Code)
	}
}

func TestBootstrapHandler_Response_HasAllRequiredFields(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "bootstrap-handler-test-*")
	defer os.RemoveAll(tmpDir)

	loop, _ = engine.NewFivePhaseLoop(tmpDir)
	broker = NewBroker()

	payload := map[string]interface{}{
		"policy_id":   "test_7",
		"domain":      "auth",
		"policy_text": "valid policy",
	}
	body, _ := json.Marshal(payload)
	req := httptest.NewRequest(http.MethodPost, "/bootstrap", bytes.NewReader(body))
	w := httptest.NewRecorder()

	bootstrapHandler(w, req)

	var result map[string]interface{}
	json.Unmarshal(w.Body.Bytes(), &result)

	requiredFields := []string{"policy_id", "domain", "status", "confidence", "tier1_result", "tier2_result", "tier3_result", "homeostasis", "cycle_id", "enct_version", "axiom_versions", "provenance_file", "timestamp"}
	for _, field := range requiredFields {
		if result[field] == nil {
			t.Errorf("missing required field: %s", field)
		}
	}
}
