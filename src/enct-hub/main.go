package main

import (
	"embed"
	"fmt"
	"html/template"
	"net/http"
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

func main() {
	http.HandleFunc("/health", healthCheckHandler)
	http.HandleFunc("/", indexHandler)
	http.ListenAndServe(":8080", nil)
}
