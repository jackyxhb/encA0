package main

import (
	"fmt"
	"net/http"
)

type Broker struct {
	clients    map[chan []byte]bool
	broadcast  chan []byte
	register   chan chan []byte
	unregister chan chan []byte
}

func NewBroker() *Broker {
	return &Broker{
		clients:    make(map[chan []byte]bool),
		broadcast:  make(chan []byte),
		register:   make(chan chan []byte),
		unregister: make(chan chan []byte),
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
				client <- event
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

	clientChan := make(chan []byte)
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
		fmt.Fprintf(w, "data: %s\n\n", event)
		flusher.Flush()
	}
}
