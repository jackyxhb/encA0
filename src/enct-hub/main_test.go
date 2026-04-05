package main

import (
	"enct-hub/engine"
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"testing"
)

func TestMain(m *testing.M) {
	// Setup temporary ledger directory for tests
	tmpDir, err := os.MkdirTemp("", "enct-main-test-*")
	if err != nil {
		panic(err)
	}
	defer os.RemoveAll(tmpDir)

	// Initialize the global loop variable
	loop, err = engine.NewFivePhaseLoop(tmpDir)
	if err != nil {
		panic(err)
	}

	// Run tests
	os.Exit(m.Run())
}

func TestHealthCheckHandler(t *testing.T) {
	req, err := http.NewRequest("GET", "/health", nil)
	if err != nil {
		t.Fatal(err)
	}
	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(healthCheckHandler)
	handler.ServeHTTP(rr, req)
	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}
}

func TestIndexHandler(t *testing.T) {
	req, err := http.NewRequest("GET", "/", nil)
	if err != nil {
		t.Fatal(err)
	}
	rr := httptest.NewRecorder()
	
	// Create a new ServeMux and register our routes the same way main() does
	mux := http.NewServeMux()
	mux.HandleFunc("/", indexHandler)
	mux.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}

	body := rr.Body.String()
	// Should contain HTMX
	if !strings.Contains(body, "htmx") {
		t.Errorf("expected HTML to contain 'htmx', got: %v", body)
	}
}

func TestSocraticStart(t *testing.T) {
	req, err := http.NewRequest("GET", "/api/socratic/start", nil)
	if err != nil {
		t.Fatal(err)
	}
	rr := httptest.NewRecorder()

	mux := http.NewServeMux()
	mux.HandleFunc("/api/socratic/start", socraticStartHandler)
	mux.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}

	body := rr.Body.String()
	// Should contain the first axiom question
	if !strings.Contains(body, "Axiom 1") {
		t.Errorf("expected HTML to contain 'Axiom 1', got: %v", body)
	}
}

func TestSocraticEvaluate(t *testing.T) {
	// Test moving from Axiom 1 to Axiom 2
	data := "question_id=1&answer=No,+it+follows+foundational+rules"
	req, err := http.NewRequest("POST", "/api/socratic/evaluate", strings.NewReader(data))
	if err != nil {
		t.Fatal(err)
	}
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	rr := httptest.NewRecorder()

	mux := http.NewServeMux()
	mux.HandleFunc("/api/socratic/evaluate", socraticEvaluateHandler)
	mux.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}

	body := rr.Body.String()
	// Should contain Axiom 2
	if !strings.Contains(body, "Axiom 2") {
		t.Errorf("expected HTML to contain 'Axiom 2', got: %v", body)
	}
}

func TestSendCommand(t *testing.T) {
	broker := NewBroker()
	go broker.Start()

	data := "agent_id=aura-1&command=/status"
	req, err := http.NewRequest("POST", "/api/command", strings.NewReader(data))
	if err != nil {
		t.Fatal(err)
	}
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	rr := httptest.NewRecorder()

	mux := http.NewServeMux()
	mux.HandleFunc("/api/command", func(w http.ResponseWriter, r *http.Request) {
		commandHandler(w, r, broker)
	})
	mux.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusAccepted {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusAccepted)
	}
}
