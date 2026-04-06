package main

import (
	"fmt"
	"sync"
	"time"
	"engine"
)

type AlertRule struct {
	WarningThreshold  float64
	CriticalThreshold float64
	HigherIsBetter    bool
}

type AlertEvent struct {
	Level       string    `json:"level"`
	Type        string    `json:"type"`
	Indicator   string    `json:"indicator"`
	Value       float64   `json:"value"`
	Message     string    `json:"message"`
	Timestamp   time.Time `json:"timestamp"`
	BGColor     string    `json:"-"`
	TextColor   string    `json:"-"`
	BorderColor string    `json:"-"`
}

var AlertRules = map[engine.IndicatorName]AlertRule{
	engine.ComplianceRate:       {WarningThreshold: 0.95, CriticalThreshold: 0.90, HigherIsBetter: true},
	engine.HomeostasisScore:     {WarningThreshold: 0.85, CriticalThreshold: 0.70, HigherIsBetter: true},
	engine.TraceabilityCoverage: {WarningThreshold: 0.99, CriticalThreshold: 0.95, HigherIsBetter: true},
	engine.BootstrapConfidence:  {WarningThreshold: 0.75, CriticalThreshold: 0.60, HigherIsBetter: true},
	engine.AdaptationResilience: {WarningThreshold: 0.85, CriticalThreshold: 0.70, HigherIsBetter: true},
	engine.ProvenanceOverhead:   {WarningThreshold: 0.10, CriticalThreshold: 0.20, HigherIsBetter: false},
	engine.AxiomViolationRate:   {WarningThreshold: 0.03, CriticalThreshold: 0.10, HigherIsBetter: false},
	engine.PolicyRollbackRate:   {WarningThreshold: 0.05, CriticalThreshold: 0.10, HigherIsBetter: false},
}

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
			CurrentIndicators[j].Status = "green"

			// Check against alert rules
			if rule, exists := AlertRules[ind.Name]; exists {
				if rule.HigherIsBetter {
					// For metrics where higher is better (compliance, resilience, etc.)
					if val < rule.CriticalThreshold {
						CurrentIndicators[j].Status = "red"
					} else if val < rule.WarningThreshold {
						CurrentIndicators[j].Status = "yellow"
					}
				} else {
					// For metrics where lower is better (violation rate, overhead, etc.)
					if val > rule.CriticalThreshold {
						CurrentIndicators[j].Status = "red"
					} else if val > rule.WarningThreshold {
						CurrentIndicators[j].Status = "yellow"
					}
				}
			}
		}
	}
}

func CheckAlerts(metrics map[engine.IndicatorName]float64) []AlertEvent {
	var alerts []AlertEvent

	for indicatorName, val := range metrics {
		if rule, exists := AlertRules[indicatorName]; exists {
			var level string
			var triggered bool

			if rule.HigherIsBetter {
				if val < rule.CriticalThreshold {
					level = "critical"
					triggered = true
				} else if val < rule.WarningThreshold {
					level = "warning"
					triggered = true
				}
			} else {
				if val > rule.CriticalThreshold {
					level = "critical"
					triggered = true
				} else if val > rule.WarningThreshold {
					level = "warning"
					triggered = true
				}
			}

			if triggered {
				alerts = append(alerts, AlertEvent{
					Level:     level,
					Type:      "threshold_breach",
					Indicator: string(indicatorName),
					Value:     val,
					Message:   fmt.Sprintf("%s at %.2f", indicatorName, val),
					Timestamp: time.Now(),
				})
			}
		}
	}

	return alerts
}

func (a AlertEvent) RenderHTML() string {
	bgColor := "#fff3e0"
	textColor := "#e65100"
	borderColor := "#ff9800"

	if a.Level == "critical" {
		bgColor = "#ffebee"
		textColor = "#c62828"
		borderColor = "#d32f2f"
	}

	indicatorHTML := ""
	if a.Indicator != "" {
		indicatorHTML = fmt.Sprintf(`<div style="font-size: 0.9em; color: #666; margin-top: 5px;">Indicator: <code>%s</code> = %.2f</div>`, a.Indicator, a.Value)
	}

	timestamp := a.Timestamp.Format("15:04:05")
	return fmt.Sprintf(`<div style="padding: 10px; border-bottom: 1px solid #ddd; margin-bottom: 5px; background: %s; color: %s; border-left: 4px solid %s;">
  <div style="display: flex; justify-content: space-between; align-items: center;">
    <div>
      <strong style="font-size: 1.1em;">%s</strong>
      <span style="margin-left: 10px; font-weight: normal;">%s</span>
    </div>
    <span style="font-size: 0.85em; color: #666; white-space: nowrap;">%s</span>
  </div>
  %s
</div>`, bgColor, textColor, borderColor, a.Level, a.Message, timestamp, indicatorHTML)
}

