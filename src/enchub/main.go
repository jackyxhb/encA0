package main

import (
	"context"
	"embed"
	"fmt"
	"html/template"
	"io/fs"
	"net/http"
	"os"
	"os/signal"
	"strconv"
	"strings"
	"syscall"
	"time"
	"engine"
)

//go:embed templates/* static/*
var content embed.FS

var loop *engine.FivePhaseLoop
var broker *Broker
var bootstrapLogsPath string

func healthCheckHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	fmt.Fprint(w, "OK")
}

func indexHandler(w http.ResponseWriter, r *http.Request) {
	tmpl, err := template.ParseFS(content, "templates/index.html")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	tmpl.Execute(w, nil)
}

func socraticStartHandler(w http.ResponseWriter, r *http.Request) {
	if len(Axioms) == 0 {
		http.Error(w, "No axioms defined", http.StatusInternalServerError)
		return
	}
	tmpl, err := template.ParseFS(content, "templates/axiom.html")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	tmpl.Execute(w, Axioms[0])
}

func socraticEvaluateHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}
	r.ParseForm()
	qID, _ := strconv.Atoi(r.FormValue("question_id"))
	answer := r.FormValue("answer")

	// Trigger a loop cycle for bootstrap validation
	loop.ExecuteCycle(map[string]interface{}{"command": "bootstrap_axiom_" + strconv.Itoa(qID), "answer": answer}, nil)

	// Check for violation
	if strings.Contains(strings.ToLower(answer), "(violation)") {
		fmt.Fprintf(w, `<article class="error"><h3>Policy Rejected</h3><p>Your answer indicates a violation of Axiom %d. This incident has been logged.</p><button hx-get="/api/socratic/start" hx-target="#socratic-content" hx-swap="outerHTML">Try Again</button></article>`, qID)
		return
	}

	// Move to next question or finish
	if qID < len(Axioms) {
		nextQ := Axioms[qID] 
		tmpl, _ := template.ParseFS(content, "templates/axiom.html")
		tmpl.Execute(w, nextQ)
	} else {
		fmt.Fprintf(w, `<article class="success"><h3>Policy Accepted</h3><p>All ENCT Axioms verified. Policy has been bootstrapped and activated.</p><button hx-get="/api/socratic/start" hx-target="#socratic-content" hx-swap="outerHTML">Bootstrap Another Policy</button></article>`)
	}
}

type ConsoleMessage struct {
	Timestamp string
	AgentName string
	Message   string
}

func commandHandler(w http.ResponseWriter, r *http.Request, b *Broker) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}
	r.ParseForm()
	agentID := r.FormValue("agent_id")
	cmd := r.FormValue("command")

	// 1. Run real ENCT cycle
	state, err := loop.ExecuteCycle(map[string]interface{}{"agent_id": agentID, "command": cmd}, map[string]interface{}{"env": "production"})
	
	agent := GetAgent(agentID)
	agentName := "Unknown"
	if agent != nil {
		agentName = agent.Name
	}

	message := fmt.Sprintf("Command: %s | Result: %s", cmd, state.Status)
	if err != nil {
		message = fmt.Sprintf("Axiom Violation: %v", err)
	}

	msg := ConsoleMessage{
		Timestamp: time.Now().Format("15:04:05"),
		AgentName: agentName,
		Message:   message,
	}

	tmpl, _ := template.ParseFS(content, "templates/console.html")
	var buf strings.Builder
	tmpl.Execute(&buf, msg)

	select {
	case b.broadcast <- SSEEvent{Event: "console", Data: buf.String()}:
	default:
	}

	// 2. Trigger immediate UI update for indicators
	snapshot := loop.GetSnapshot()
	UpdateIndicators(snapshot.Indicators)
	indicatorsMu.RLock()
	indicators := make([]Indicator, len(CurrentIndicators))
	copy(indicators, CurrentIndicators)
	indicatorsMu.RUnlock()
	for _, ind := range indicators {
		select {
		case b.broadcast <- SSEEvent{Event: fmt.Sprintf("indicator-%d", ind.ID), Data: ind.RenderHTML()}:
		default:
		}
	}

	w.WriteHeader(http.StatusAccepted)
}

func main() {
	var err error

	// Read configuration from environment variables with defaults
	ledgerPath := os.Getenv("LEDGER_PATH")
	if ledgerPath == "" {
		ledgerPath = "ledger"
	}

	bootstrapLogsPath = os.Getenv("BOOTSTRAP_LOGS_PATH")
	if bootstrapLogsPath == "" {
		bootstrapLogsPath = "bootstrap-logs"
	}

	port := os.Getenv("PORT")
	if port == "" {
		port = "8081"
	}

	// Initialize engine with ledger path
	loop, err = engine.NewFivePhaseLoop(ledgerPath)
	if err != nil {
		panic(err)
	}

	broker = NewBroker()
	go broker.Start()
	go simulateTelemetry(broker)

	// Static files (CSS, JS)
	staticFS, err := fs.Sub(content, "static")
	if err == nil {
		http.Handle("/static/", http.StripPrefix("/static/", http.FileServer(http.FS(staticFS))))
	}

	http.HandleFunc("/health", healthCheckHandler)
	http.HandleFunc("/api/socratic/start", socraticStartHandler)
	http.HandleFunc("/api/socratic/evaluate", socraticEvaluateHandler)
	http.HandleFunc("/api/command", func(w http.ResponseWriter, r *http.Request) {
		commandHandler(w, r, broker)
	})
	http.HandleFunc("/bootstrap", bootstrapHandler)
	http.HandleFunc("/api/stream", broker.ServeHTTP)
	http.HandleFunc("/", indexHandler)

	// Set up graceful shutdown
	ctx, cancel := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer cancel()

	server := &http.Server{
		Addr:         ":" + port,
		Handler:      nil, // Use DefaultServeMux
	}

	// Start server in a goroutine
	go func() {
		fmt.Printf("Starting ENCT enchub server on %s\n", server.Addr)
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			fmt.Printf("Server error: %v\n", err)
		}
	}()

	// Wait for interrupt signal
	<-ctx.Done()

	// Graceful shutdown with 10s timeout
	shutdownCtx, shutdownCancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer shutdownCancel()

	fmt.Println("Shutting down server...")
	if err := server.Shutdown(shutdownCtx); err != nil {
		fmt.Printf("Shutdown error: %v\n", err)
	}
}

func simulateTelemetry(b *Broker) {
	interval := 5 * time.Second
	stableCycles := 0

	for {
		// Run a "heartbeat" cycle to maintain homeostasis
		state, _ := loop.ExecuteCycle(map[string]interface{}{"command": "heartbeat"}, nil)

		// Adaptive sampling: adjust interval based on system state
		if state.Status == engine.StatusAxiomViolation {
			interval = 1 * time.Second // Fast mode on violation
			stableCycles = 0
		} else {
			stableCycles++
			if stableCycles >= 10 {
				interval = 10 * time.Second // Slow mode when stable
			} else if interval == 1*time.Second {
				interval = 5 * time.Second // Back to base if violation cleared
			}
		}

		snapshot := loop.GetSnapshot()
		UpdateIndicators(snapshot.Indicators)
		indicatorsMu.RLock()
		indicators := make([]Indicator, len(CurrentIndicators))
		copy(indicators, CurrentIndicators)
		indicatorsMu.RUnlock()
		for _, ind := range indicators {
			b.broadcast <- SSEEvent{
				Event: fmt.Sprintf("indicator-%d", ind.ID),
				Data:  ind.RenderHTML(),
			}
		}

		time.Sleep(interval)
	}
}


