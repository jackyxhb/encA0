package main

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

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
