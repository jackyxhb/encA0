package main

import (
	"embed"
	"fmt"
	"html/template"
	"net/http"
	"strconv"
	"strings"
	"time"
)

//go:embed templates/*
var content embed.FS

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

	// Check for violation
	if strings.Contains(strings.ToLower(answer), "(violation)") {
		fmt.Fprintf(w, `<article class="error"><h3>Policy Rejected</h3><p>Your answer indicates a violation of Axiom %d. This incident has been logged.</p><button hx-get="/api/socratic/start" hx-target="#socratic-content" hx-swap="outerHTML">Try Again</button></article>`, qID)
		return
	}

	// Move to next question or finish
	if qID < len(Axioms) {
		nextQ := Axioms[qID] // Index is qID because Axioms are 0-indexed and qID is 1-indexed
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

	response := HandleCommand(agentID, cmd)
	agent := GetAgent(agentID)
	agentName := "Unknown"
	if agent != nil {
		agentName = agent.Name
	}

	msg := ConsoleMessage{
		Timestamp: time.Now().Format("15:04:05"),
		AgentName: agentName,
		Message:   response,
	}

	tmpl, _ := template.ParseFS(content, "templates/console.html")
	var buf strings.Builder
	tmpl.Execute(&buf, msg)

	b.broadcast <- SSEEvent{
		Event: "console",
		Data:  buf.String(),
	}

	w.WriteHeader(http.StatusAccepted)
}

func telemetryHandler(w http.ResponseWriter, r *http.Request, b *Broker) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}
	b.broadcast <- SSEEvent{Event: "message", Data: "Custom Telemetry Update"}
	w.WriteHeader(http.StatusAccepted)
}

func main() {
	broker := NewBroker()
	go broker.Start()
	go simulateTelemetry(broker)

	http.HandleFunc("/health", healthCheckHandler)
	http.HandleFunc("/api/socratic/start", socraticStartHandler)
	http.HandleFunc("/api/socratic/evaluate", socraticEvaluateHandler)
	http.HandleFunc("/api/command", func(w http.ResponseWriter, r *http.Request) {
		commandHandler(w, r, broker)
	})
	http.HandleFunc("/api/stream", broker.ServeHTTP)
	http.HandleFunc("/", indexHandler)
	http.ListenAndServe(":8080", nil)
}

func simulateTelemetry(b *Broker) {
	for {
		time.Sleep(2 * time.Second)
		for _, ind := range CurrentIndicators {
			b.broadcast <- SSEEvent{
				Event: fmt.Sprintf("indicator-%d", ind.ID),
				Data:  ind.RenderHTML(),
			}
		}
	}
}
