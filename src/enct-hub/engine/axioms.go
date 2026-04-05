package engine

import (
	"fmt"
	"strings"
)

// AxiomViolationError is a special error type for axiom violations.
type AxiomViolationError struct {
	AxiomNumber int
	ViolationType string
	Message string
	Context map[string]interface{}
}

func (e *AxiomViolationError) Error() string {
	return fmt.Sprintf("Axiom %d Violation (%s): %s", e.AxiomNumber, e.ViolationType, e.Message)
}

// AxiomEnforcer validates system state and operations against the ENCT axioms.
type AxiomEnforcer struct {
	ImmutableKeywords []string
	MaxUncertainty    float64
}

// NewAxiomEnforcer creates a new enforcer with default rules.
func NewAxiomEnforcer() *AxiomEnforcer {
	return &AxiomEnforcer{
		ImmutableKeywords: []string{"disable axioms", "override engine", "bypass validation", "force success"},
		MaxUncertainty:    0.15,
	}
}

// ValidateAxiom1 checks for immutability violations in policy requests.
func (e *AxiomEnforcer) ValidateAxiom1(policy string) error {
	for _, kw := range e.ImmutableKeywords {
		if strings.Contains(strings.ToLower(policy), kw) {
			return &AxiomViolationError{
				AxiomNumber: 1,
				ViolationType: "immutable_override",
				Message: fmt.Sprintf("Policy contains forbidden keyword: %s", kw),
				Context: map[string]interface{}{"keyword": kw, "policy_fragment": policy},
			}
		}
	}
	return nil
}

// ValidateAxiom2 checks for determinism within uncertainty bounds.
func (e *AxiomEnforcer) ValidateAxiom2(confidence float64, bounds Uncertainty) error {
	deviation := mathAbs(bounds.EpistemicUpper - bounds.EpistemicLower)
	if deviation > e.MaxUncertainty {
		return &AxiomViolationError{
			AxiomNumber: 2,
			ViolationType: "uncertainty_overflow",
			Message: fmt.Sprintf("Uncertainty bound deviation %.3f exceeds limit %.3f", deviation, e.MaxUncertainty),
			Context: map[string]interface{}{"deviation": deviation, "max": e.MaxUncertainty},
		}
	}
	if confidence < bounds.EpistemicLower || confidence > bounds.EpistemicUpper {
		return &AxiomViolationError{
			AxiomNumber: 2,
			ViolationType: "confidence_out_of_bounds",
			Message: fmt.Sprintf("Confidence %.3f falls outside epistemic bounds [%.3f, %.3f]", confidence, bounds.EpistemicLower, bounds.EpistemicUpper),
			Context: map[string]interface{}{"confidence": confidence, "bounds": bounds},
		}
	}
	return nil
}

// ValidateAxiom3 checks for normative constraint enforcement.
func (e *AxiomEnforcer) ValidateAxiom3(constraints map[string]bool) error {
	for name, passed := range constraints {
		if !passed {
			return &AxiomViolationError{
				AxiomNumber: 3,
				ViolationType: "constraint_violation",
				Message: fmt.Sprintf("Normative constraint failed: %s", name),
				Context: map[string]interface{}{"constraint_name": name},
			}
		}
	}
	return nil
}

// ValidateAxiom4 ensures that every state change is audited (placeholder for ledger check).
func (e *AxiomEnforcer) ValidateAxiom4(hasLedgerEntry bool) error {
	if !hasLedgerEntry {
		return &AxiomViolationError{
			AxiomNumber: 4,
			ViolationType: "audit_missing",
			Message: "State transition occurred without ledger entry record",
		}
	}
	return nil
}

func mathAbs(x float64) float64 {
	if x < 0 {
		return -x
	}
	return x
}
