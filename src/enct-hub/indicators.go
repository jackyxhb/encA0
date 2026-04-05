package main

import (
	"fmt"
)

type Indicator struct {
	ID     int
	Name   string
	Value  float64
	Unit   string
	Target string
	Status string // "green", "yellow", "red"
}

var CurrentIndicators = []Indicator{
	{ID: 1, Name: "Compliance Rate", Value: 99.5, Unit: "%", Target: ">99%", Status: "green"},
	{ID: 2, Name: "Homeostasis Score", Value: 0.92, Unit: "", Target: "≥0.85", Status: "green"},
	{ID: 3, Name: "Traceability Coverage", Value: 100, Unit: "%", Target: "100%", Status: "green"},
	{ID: 4, Name: "Bootstrap Confidence", Value: 0.83, Unit: "", Target: ">0.80", Status: "green"},
	{ID: 5, Name: "Adaptation Resilience", Value: 0.95, Unit: "", Target: ">0.90", Status: "green"},
	{ID: 6, Name: "Provenance Overhead", Value: 4.2, Unit: "%", Target: "<10%", Status: "green"},
	{ID: 7, Name: "Axiom Violation Rate", Value: 0, Unit: "/d", Target: "<0.03", Status: "green"},
	{ID: 8, Name: "Policy Rollback Rate", Value: 1.2, Unit: "%", Target: "<5%", Status: "green"},
}

func (i Indicator) RenderHTML() string {
	valStr := fmt.Sprintf("%.1f%s", i.Value, i.Unit)
	if i.ID == 2 || i.ID == 4 || i.ID == 5 {
		valStr = fmt.Sprintf("%.2f%s", i.Value, i.Unit)
	}
	
	statusIcon := "✓"
	if i.Status == "yellow" {
		statusIcon = "⚠"
	} else if i.Status == "red" {
		statusIcon = "✘"
	}

	return fmt.Sprintf(`<div id="indicator-%d" sse-swap="indicator-%d" class="status-%s">%s %s</div>`, 
		i.ID, i.ID, i.Status, valStr, statusIcon)
}
