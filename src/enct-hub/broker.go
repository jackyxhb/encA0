package main

import (
	"fmt"
	"net/http"
)

type SSEEvent struct {
	Event string
	Data  string
}

type Broker struct {
	clients    map[chan SSEEvent]bool
	broadcast  chan SSEEvent
	register   chan chan SSEEvent
	unregister chan chan SSEEvent
}

func NewBroker() *Broker {
	return &Broker{
		clients:    make(map[chan SSEEvent]bool),
		broadcast:  make(chan SSEEvent),
		register:   make(chan chan SSEEvent),
		unregister: make(chan chan SSEEvent),
	}
}

func (b *Broker) Start() {
	for {
		select {
		case client := <-b.register:
			b.clients[client] = true
		case client := <-b.unregister:
			if _, ok := b.clients[client]; ok {
				delete(b.clients, client)
				close(client)
			}
		case event := <-b.broadcast:
			for client := range b.clients {
				select {
				case client <- event:
				default:
					// Drop event if client is too slow or disconnected
				}
			}
		}

	}
}

func (b *Broker) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/event-stream")
	w.Header().Set("Cache-Control", "no-cache")
	w.Header().Set("Connection", "keep-alive")

	flusher, ok := w.(http.Flusher)
	if !ok {
		http.Error(w, "Streaming unsupported", http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
	flusher.Flush()

	clientChan := make(chan SSEEvent, 100)

	b.register <- clientChan

	notify := r.Context().Done()

	go func() {
		<-notify
		b.unregister <- clientChan
	}()

	for {
		event, ok := <-clientChan
		if !ok {
			break
		}
		if event.Event != "" {
			fmt.Fprintf(w, "event: %s\n", event.Event)
		}
		fmt.Fprintf(w, "data: %s\n\n", event.Data)
		flusher.Flush()
	}
}
