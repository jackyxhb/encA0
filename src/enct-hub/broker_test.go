package main

import (
	"bufio"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

func TestBroker(t *testing.T) {
	broker := NewBroker()
	go broker.Start()

	ts := httptest.NewServer(broker)
	defer ts.Close()

	resp, err := http.Get(ts.URL)
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()

	if ct := resp.Header.Get("Content-Type"); ct != "text/event-stream" {
		t.Errorf("expected Content-Type text/event-stream, got %v", ct)
	}

	go func() {
		time.Sleep(50 * time.Millisecond)
		broker.broadcast <- []byte("test event")
	}()

	reader := bufio.NewReader(resp.Body)
	line, err := reader.ReadString('\n')
	if err != nil {
		t.Fatal("error reading stream:", err)
	}

	expected := "data: test event\n"
	if line != expected {
		t.Errorf("expected %q, got %q", expected, line)
	}
}
