package main

import (
	"fmt"
	"sync"
	"engine"
)

type Indicator struct {
	ID     int
	Name   engine.IndicatorName
	Value  float64
	Unit   string
	Target string
	Status string // "green", "yellow", "red"
}

var (
	CurrentIndicators = []Indicator{
		{ID: 1, Name: engine.ComplianceRate, Value: 99.5, Unit: "%", Target: ">99%", Status: "green"},
		{ID: 2, Name: engine.HomeostasisScore, Value: 0.92, Unit: "", Target: "≥0.85", Status: "green"},
		{ID: 3, Name: engine.TraceabilityCoverage, Value: 100, Unit: "%", Target: "100%", Status: "green"},
		{ID: 4, Name: engine.BootstrapConfidence, Value: 0.83, Unit: "", Target: ">0.80", Status: "green"},
		{ID: 5, Name: engine.AdaptationResilience, Value: 0.95, Unit: "", Target: ">0.90", Status: "green"},
		{ID: 6, Name: engine.ProvenanceOverhead, Value: 4.2, Unit: "%", Target: "<10%", Status: "green"},
		{ID: 7, Name: engine.AxiomViolationRate, Value: 0, Unit: "/d", Target: "<0.03", Status: "green"},
		{ID: 8, Name: engine.PolicyRollbackRate, Value: 1.2, Unit: "%", Target: "<5%", Status: "green"},
	}
	indicatorsMu sync.RWMutex
)

func (i Indicator) RenderHTML() string {
	valStr := fmt.Sprintf("%.1f%s", i.Value, i.Unit)
	if i.Name == engine.HomeostasisScore || i.Name == engine.BootstrapConfidence || i.Name == engine.AdaptationResilience {
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

func UpdateIndicators(metrics map[engine.IndicatorName]float64) {
	indicatorsMu.Lock()
	defer indicatorsMu.Unlock()

	for j, ind := range CurrentIndicators {
		if val, ok := metrics[ind.Name]; ok {
			CurrentIndicators[j].Value = val
			// Simplified status logic
			CurrentIndicators[j].Status = "green"
			if val < 0.90 && (ind.Name == engine.ComplianceRate || ind.Name == engine.HomeostasisScore) {
				CurrentIndicators[j].Status = "yellow"
			}
			if val < 0.80 && (ind.Name == engine.ComplianceRate || ind.Name == engine.HomeostasisScore) {
				CurrentIndicators[j].Status = "red"
			}
		}
	}
}

