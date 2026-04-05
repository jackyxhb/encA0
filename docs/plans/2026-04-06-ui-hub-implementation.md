# ENCT Go Hub & UI Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Scaffold the core Go-based Hub that will serve the HTMX dashboard, manage the Socratic policy form, and handle SSE telemetry broadcasts.

**Architecture:** A single `net/http` Go binary running internally on port 8080. It embeds HTMX and Pico.css templates. It exposes `/` for the UI, `/api/telemetry` for agent POSTs, and `/api/stream` for the UI SSE connection.

**Tech Stack:** Go (Standard Library), HTMX, Pico.css

---
### Task 1: Initialize Go Module and Core Directory

**Files:**
- Create: `src/enct-hub/go.mod`
- Create: `src/enct-hub/main.go`
- Create: `src/enct-hub/main_test.go`

**Step 1: Write the failing test**
```go
package main
import (
	"net/http"
	"net/http/httptest"
	"testing"
)
func TestHealthCheckHandler(t *testing.T) {
	req, err := http.NewRequest("GET", "/health", nil)
	if err != nil { t.Fatal(err) }
	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(healthCheckHandler)
	handler.ServeHTTP(rr, req)
	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}
}
```

**Step 2: Run test to verify it fails**
Run: `cd src/enct-hub && go test -v`
Expected: FAIL with "undefined: healthCheckHandler"

**Step 3: Write minimal implementation**
```go
package main
import (
	"fmt"
	"net/http"
)
func healthCheckHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	fmt.Fprint(w, "OK")
}
func main() {
	http.HandleFunc("/health", healthCheckHandler)
	http.ListenAndServe(":8080", nil)
}
```

**Step 4: Run test to verify it passes**
Run: `cd src/enct-hub && go mod init enct-hub && go test -v`
Expected: PASS

**Step 5: Commit**
```bash
git add src/enct-hub/
git commit -m "feat: initialize Go enct-hub and healthcheck"
```

---
### Task 2: Implement Embedded HTMX Frontend

**Files:**
- Create: `src/enct-hub/templates/index.html`
- Modify: `src/enct-hub/main.go:1-20`
- Modify: `src/enct-hub/main_test.go`

**Step 1: Write the failing test**
Create test ensuring the `/` route returns HTML containing "HTMX".

**Step 2: Run test to verify it fails**
Run: `cd src/enct-hub && go test -v`

**Step 3: Write minimal implementation**
Create `templates/index.html` loading Pico.css and HTMX via CDN.
Modify `main.go` to use Go 1.16 `//go:embed templates/*` to serve the index upon navigating to `/`.

**Step 4: Run test to verify it passes**
Run: `cd src/enct-hub && go test -v`
Expected: PASS

**Step 5: Commit**
```bash
git add src/enct-hub/
git commit -m "feat: embed htmx templates in hub"
```

---
### Task 3: Implement SSE Broker Pattern

**Files:**
- Create: `src/enct-hub/broker.go`
- Create: `src/enct-hub/broker_test.go`

**Step 1: Write the failing test**
Test that clients can connect to a mock broker and receive a test event.

**Step 2: Run test to verify it fails**
Run: `cd src/enct-hub && go test -v`

**Step 3: Write minimal implementation**
Create a `Broker` struct with `clients`, `broadcast`, `register`, `unregister` channels. Implement the `ServeHTTP` method to write SSE headers (`Content-Type: text/event-stream`).

**Step 4: Run test to verify it passes**
Run: `cd src/enct-hub && go test -v`
Expected: PASS

**Step 5: Commit**
```bash
git add src/enct-hub/
git commit -m "feat: implement SSE broker for realtime telemetry"
```
