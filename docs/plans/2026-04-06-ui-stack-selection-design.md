# ENCT UI Stack & Architecture Design

## Overview
This document outlines the finalized UI stack and architecture for the ENCT agent system, aiming for extreme simplicity, Phase 4 installer compliance (single-binary distribution), and scalability from SAS (Single-Agent) to MAS (Multi-Agent System).

## Architecture

**Language & Runtime:** Go (Golang)
The entire ENCT system (UI Server + Hub + Multi-Agent Engine) will be designed for Go. This allows extreme simplicity in deployment as the entire product compiles down to a single binary executable, completely fulfilling the Phase 4 requirement for easy desktop/Docker installers without needing Python environments.

**Concurrency Model (SAS to MAS):**
Leveraging Go's Goroutines, the Hub and up to thousands of ENCT agents can run within the exact same process memory space without the UI-freezing issues caused by Python's Global Interpreter Lock (GIL). This eliminates the need for complex inter-process communication or external message brokers (like Redis).

## UI/Frontend Stack

**Core Philosophy:** "No-JS" HTML streaming
**Technologies:** HTMX + Server-Sent Events (SSE) + Go `html/template` + Minimal classless CSS (e.g., Pico.css)

**Socratic Policy Intake:**
Dynamic form progression is handled entirely by HTMX. When a user submits an answer, HTMX POSTs to the local Go Hub, which evaluates the ENCT axioms and returns only the HTML snippet for the next Socratic question, creating a seamless conversational flow without any heavy JavaScript frameworks.

**Live 8-Indicator Dashboard:**
The Hub maintains a real-time Server-Sent Events (SSE) connection with the browser. When any Goroutine agent updates its indicators, the Hub pushes an SSE event containing updated HTML to the dashboard, and HTMX automatically swaps the values on screen.

## Interactive Virtual Console

To fulfill the requirement of interacting precisely with specific agent instances:
1. **Selection:** A dropdown allows the user to select any running Agent ID.
2. **Command Input:** The user types a command; HTMX POSTs it to the Go Hub.
3. **Execution & Feedback:** The Hub channels the command to the specific agent goroutine. The agent evaluates it and pushes its response back to the Hub's SSE stream.
4. **Display:** HTMX automatically appends the response directly to the bottom of the virtual console element, mirroring a native command-line interface directly within the web dashboard.
