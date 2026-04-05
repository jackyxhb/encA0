package engine

import (
	"time"
)

// LoopPhase represents the 5 phases of the ENCT cycle.
type LoopPhase string

const (
	PhaseSense   LoopPhase = "sense"
	PhaseValidate LoopPhase = "validate"
	PhaseExecute  LoopPhase = "execute"
	PhaseAssess   LoopPhase = "assess"
	PhaseReEnact  LoopPhase = "re-enact"
	PhaseComplete LoopPhase = "complete"
)

// LoopStatus represents the overall status of a cycle.
type LoopStatus string

const (
	StatusInProgress     LoopStatus = "in_progress"
	StatusComplete       LoopStatus = "complete"
	StatusFailed         LoopStatus = "failed"
	StatusAxiomViolation LoopStatus = "axiom_violation"
)

// IndicatorName represents the 8 ENCT indicators.
type IndicatorName string

const (
	ComplianceRate        IndicatorName = "compliance_rate"
	HomeostasisScore      IndicatorName = "homeostasis_score"
	TraceabilityCoverage  IndicatorName = "traceability_coverage"
	BootstrapConfidence   IndicatorName = "bootstrap_confidence"
	AdaptationResilience  IndicatorName = "adaptation_resilience"
	ProvenanceOverhead    IndicatorName = "provenance_overhead"
	AxiomViolationRate    IndicatorName = "axiom_violation_rate"
	PolicyRollbackRate    IndicatorName = "policy_rollback_rate"
)

// IndicatorDefinition defines a single indicator's metadata.
type IndicatorDefinition struct {
	Name              IndicatorName `json:"name"`
	Description       string        `json:"description"`
	Unit              string        `json:"unit"`
	Formula           string        `json:"formula"`
	TargetMin         float64       `json:"target_min"`
	TargetMax         float64       `json:"target_max"`
	CriticalThreshold float64       `json:"critical_threshold"`
	WarningThreshold  float64       `json:"warning_threshold"`
}

// IndicatorSnapshot represents a point-in-time calculation of all indicators.
type IndicatorSnapshot struct {
	CycleID              string             `json:"cycle_id"`
	Timestamp            time.Time          `json:"timestamp"`
	Indicators           map[IndicatorName]float64 `json:"indicators"`
}

// CycleState captures the complete state of a Loop cycle.
type CycleState struct {
	CycleID        string         `json:"cycle_id"`
	Status         LoopStatus     `json:"status"`
	CurrentPhase   LoopPhase      `json:"current_phase"`
	StartTime      time.Time      `json:"start_time"`
	EndTime        time.Time      `json:"end_time"`
	SenseOutput    *SenseOutput   `json:"sense_output,omitempty"`
	ValidateOutput *ValidateOutput `json:"validate_output,omitempty"`
	ExecuteOutput  *ExecuteOutput `json:"execute_output,omitempty"`
	AssessOutput   *AssessOutput  `json:"assess_output,omitempty"`
	ReEnactOutput  *ReEnactOutput `json:"reenact_output,omitempty"`
	Error          string         `json:"error,omitempty"`
	ErrorPhase     LoopPhase      `json:"error_phase,omitempty"`
}

type SenseOutput struct {
	Timestamp     time.Time              `json:"timestamp"`
	Observations  map[string]interface{} `json:"observations"`
	PolicyRequest map[string]interface{} `json:"policy_request"`
}

type ValidateOutput struct {
	Timestamp          time.Time       `json:"timestamp"`
	ConstraintChecks   map[string]bool `json:"constraint_checks"`
	Confidence         float64         `json:"confidence"`
	UncertaintyBounds  Uncertainty     `json:"uncertainty_bounds"`
	Passed             bool            `json:"passed"`
}

type Uncertainty struct {
	EpistemicLower float64 `json:"epistemic_lower"`
	EpistemicUpper float64 `json:"epistemic_upper"`
	Aleatoric      float64 `json:"aleatoric"`
}

type ExecuteOutput struct {
	Timestamp    time.Time `json:"timestamp"`
	ActionTaken  string    `json:"action_taken"`
	Outcome      string    `json:"outcome"`
	SideEffects  []string  `json:"side_effects"`
}

type AssessOutput struct {
	Timestamp          time.Time             `json:"timestamp"`
	Metrics            map[IndicatorName]float64 `json:"metrics"`
	ViolationsDetected []string              `json:"violations_detected"`
	SystemHealth       float64               `json:"system_health"`
}

type ReEnactOutput struct {
	Timestamp        time.Time `json:"timestamp"`
	AdaptationsMade  []string  `json:"adaptations_made"`
	VersionUpdated   bool      `json:"version_updated"`
	RollbackDecision string    `json:"rollback_decision,omitempty"`
}
