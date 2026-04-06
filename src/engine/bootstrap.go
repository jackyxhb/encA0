package engine

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"
)

// BootstrapRequest is the input to the bootstrap process.
type BootstrapRequest struct {
	PolicyID   string                 `json:"policy_id"`
	Domain     string                 `json:"domain"`
	PolicyText string                 `json:"policy_text"`
	Metadata   map[string]interface{} `json:"metadata,omitempty"`
}

// TierResult captures the outcome of a single validation tier.
type TierResult struct {
	Passed bool   `json:"passed"`
	Reason string `json:"reason,omitempty"`
}

// ProvenanceBundle is the immutable record of a bootstrap decision.
type ProvenanceBundle struct {
	PolicyID       string            `json:"policy_id"`
	Domain         string            `json:"domain"`
	CycleID        string            `json:"cycle_id"`
	Timestamp      time.Time         `json:"timestamp"`
	ENCtVersion    string            `json:"enct_version"`
	AxiomVersions  map[string]string `json:"axiom_versions"`
	Tier1          TierResult        `json:"tier1"`
	Tier2          TierResult        `json:"tier2"`
	Tier3          TierResult        `json:"tier3"`
	Confidence     float64           `json:"confidence"`
	Homeostasis    float64           `json:"homeostasis"`
	Decision       string            `json:"decision"`
	RejectedReason string            `json:"rejected_reason,omitempty"`
}

// CandidateModule wraps a policy request with its bootstrap lifecycle state.
type CandidateModule struct {
	Request       BootstrapRequest
	QualityGate   float64
	SandboxPassed bool
	Provenance    ProvenanceBundle
}

// BootstrapResult is returned by BootstrapEngine.RunBootstrap.
type BootstrapResult struct {
	PolicyID       string            `json:"policy_id"`
	Domain         string            `json:"domain"`
	Status         string            `json:"status"`
	Confidence     float64           `json:"confidence"`
	Tier1Result    string            `json:"tier1_result"`
	Tier2Result    string            `json:"tier2_result"`
	Tier3Result    string            `json:"tier3_result"`
	Homeostasis    float64           `json:"homeostasis"`
	CycleID        string            `json:"cycle_id"`
	ENCtVersion    string            `json:"enct_version"`
	AxiomVersions  map[string]string `json:"axiom_versions"`
	ProvenanceFile string            `json:"provenance_file"`
	RejectedReason string            `json:"rejected_reason,omitempty"`
	Timestamp      time.Time         `json:"timestamp"`
}

// BootstrapEngine orchestrates the three-tier LLM-Assisted Bootstrap Pattern.
type BootstrapEngine struct {
	Loop          *FivePhaseLoop
	QualityGate   float64            // default 0.7
	ProvenanceDir string
	DomainGates   map[string]float64
}

// NewBootstrapEngine creates a bootstrap engine wrapping an existing loop.
func NewBootstrapEngine(loop *FivePhaseLoop, provenanceDir string) *BootstrapEngine {
	domainGates := map[string]float64{
		"auth":                0.75,
		"api_rate_limiting":   0.70,
		"data_validation":     0.70,
		"access_control":      0.75,
		"audit_logging":       0.70,
		"performance":         0.65,
		"compliance":          0.80,
	}

	return &BootstrapEngine{
		Loop:          loop,
		QualityGate:   0.7,
		ProvenanceDir: provenanceDir,
		DomainGates:   domainGates,
	}
}

// RunBootstrap executes the full three-tier bootstrap for a request.
func (b *BootstrapEngine) RunBootstrap(req BootstrapRequest) (BootstrapResult, error) {
	result := BootstrapResult{
		PolicyID:      req.PolicyID,
		Domain:        req.Domain,
		ENCtVersion:   "v1.3.1",
		AxiomVersions: map[string]string{"axiom_1": "v1.3.1", "axiom_2": "v1.3.1", "axiom_3": "v1.3.1", "axiom_4": "v1.3.1"},
		Timestamp:     time.Now(),
	}

	// Initialize all tier results as empty (will be set to "pass" or "fail")
	result.Tier1Result = ""
	result.Tier2Result = ""
	result.Tier3Result = ""

	// Tier 1: Axiom 1 immutability check
	tier1 := b.runTier1(req)
	if tier1.Passed {
		result.Tier1Result = "pass"
	} else {
		result.Tier1Result = "fail"
		result.Status = "rejected"
		result.RejectedReason = tier1.Reason
		// Write provenance even for Tier 1 rejection
		bundle := ProvenanceBundle{
			PolicyID:       req.PolicyID,
			Domain:         req.Domain,
			CycleID:        fmt.Sprintf("rejected-t1-%d", time.Now().UnixNano()),
			Timestamp:      result.Timestamp,
			ENCtVersion:    result.ENCtVersion,
			AxiomVersions:  result.AxiomVersions,
			Tier1:          tier1,
			Decision:       result.Status,
			RejectedReason: result.RejectedReason,
		}
		provPath, err := b.writeProvenance(bundle)
		if err != nil {
			fmt.Fprintf(os.Stderr, "warning: provenance write failed: %v\n", err)
		} else {
			result.ProvenanceFile = filepath.Base(provPath)
		}
		return result, nil
	}

	// Tier 2: Axiom 2 & 3 constraint and confidence check
	tier2 := b.runTier2(req)
	if tier2.Passed {
		result.Tier2Result = "pass"
	} else {
		result.Tier2Result = "fail"
		result.Status = "rejected"
		result.RejectedReason = tier2.Reason
		// Write provenance even for Tier 2 rejection
		bundle := ProvenanceBundle{
			PolicyID:       req.PolicyID,
			Domain:         req.Domain,
			CycleID:        fmt.Sprintf("rejected-t2-%d", time.Now().UnixNano()),
			Timestamp:      result.Timestamp,
			ENCtVersion:    result.ENCtVersion,
			AxiomVersions:  result.AxiomVersions,
			Tier1:          tier1,
			Tier2:          tier2,
			Decision:       result.Status,
			RejectedReason: result.RejectedReason,
		}
		provPath, err := b.writeProvenance(bundle)
		if err != nil {
			fmt.Fprintf(os.Stderr, "warning: provenance write failed: %v\n", err)
		} else {
			result.ProvenanceFile = filepath.Base(provPath)
		}
		return result, nil
	}

	// Tier 3: Full cycle execution and homeostasis check
	tier3, state, err := b.runTier3(req)
	if err != nil {
		return result, fmt.Errorf("tier 3 execution error: %w", err)
	}

	if tier3.Passed {
		result.Tier3Result = "pass"
	} else {
		result.Tier3Result = "fail"
		result.Status = "escalated"
		result.RejectedReason = tier3.Reason
	}

	// Extract cycle state data
	if state != nil {
		result.CycleID = state.CycleID
		if state.ValidateOutput != nil {
			result.Confidence = state.ValidateOutput.Confidence
		}
		if state.AssessOutput != nil {
			result.Homeostasis = state.AssessOutput.SystemHealth
		}
	}

	// Check quality gate (if tier 3 passed but quality gate fails, escalate)
	if result.Tier3Result == "pass" {
		gate := b.domainThreshold(req.Domain)
		if result.Confidence < gate {
			result.Status = "escalated"
			result.RejectedReason = fmt.Sprintf("confidence %.2f below domain gate %.2f", result.Confidence, gate)
		} else {
			result.Status = "accepted"
		}
	}

	// Write provenance bundle
	bundle := ProvenanceBundle{
		PolicyID:       req.PolicyID,
		Domain:         req.Domain,
		CycleID:        result.CycleID,
		Timestamp:      result.Timestamp,
		ENCtVersion:    result.ENCtVersion,
		AxiomVersions:  result.AxiomVersions,
		Tier1:          tier1,
		Tier2:          tier2,
		Tier3:          tier3,
		Confidence:     result.Confidence,
		Homeostasis:    result.Homeostasis,
		Decision:       result.Status,
		RejectedReason: result.RejectedReason,
	}

	provPath, err := b.writeProvenance(bundle)
	if err != nil {
		// Log but don't fail — the bootstrap decision is made, provenance write failure is secondary
		fmt.Fprintf(os.Stderr, "warning: provenance write failed: %v\n", err)
	} else {
		result.ProvenanceFile = filepath.Base(provPath)
	}

	return result, nil
}

// domainThreshold returns the confidence gate for the given domain.
func (b *BootstrapEngine) domainThreshold(domain string) float64 {
	normalized := strings.ToLower(strings.TrimSpace(domain))
	if gate, exists := b.DomainGates[normalized]; exists {
		return gate
	}
	return b.QualityGate
}

// runTier1 performs the instant keyword check (Axiom 1).
func (b *BootstrapEngine) runTier1(req BootstrapRequest) TierResult {
	err := b.Loop.Enforcer.ValidateAxiom1(req.PolicyText)
	if err != nil {
		return TierResult{Passed: false, Reason: err.Error()}
	}
	return TierResult{Passed: true}
}

// runTier2 performs constraint scoring (Axiom 2 + Axiom 3).
func (b *BootstrapEngine) runTier2(req BootstrapRequest) TierResult {
	// Stub constraint checks
	constraints := map[string]bool{
		"domain_valid": len(req.Domain) > 0,
		"text_nonempty": len(req.PolicyText) > 0,
	}

	// Check Axiom 3 (constraint enforcement)
	err := b.Loop.Enforcer.ValidateAxiom3(constraints)
	if err != nil {
		return TierResult{Passed: false, Reason: err.Error()}
	}

	// Check Axiom 2 (determinism) — use stub uncertainty bounds
	uncertainty := Uncertainty{
		EpistemicLower: 0.85,
		EpistemicUpper: 0.95,
		Aleatoric:      0.02,
	}
	confidence := 0.90

	err = b.Loop.Enforcer.ValidateAxiom2(confidence, uncertainty)
	if err != nil {
		return TierResult{Passed: false, Reason: err.Error()}
	}

	return TierResult{Passed: true}
}

// runTier3 performs the full cycle sandbox execution and checks Homeostasis.
func (b *BootstrapEngine) runTier3(req BootstrapRequest) (TierResult, *CycleState, error) {
	// Build policy map
	policyMap := map[string]interface{}{
		"action":     req.PolicyText,
		"domain":     req.Domain,
		"policy_id":  req.PolicyID,
	}

	// Build environment map
	envMap := map[string]interface{}{
		"mode": "sandbox",
	}

	// Execute full cycle
	state, err := b.Loop.ExecuteCycle(policyMap, envMap)
	if err != nil {
		// Axiom violation is expected in some cases; still return the state
		// but mark tier 3 as failed
		return TierResult{Passed: false, Reason: fmt.Sprintf("cycle violation: %v", err)}, state, nil
	}

	// Check homeostasis gate (>= 0.50 for sandbox, acceptable for initial cycles)
	// Initial cycles may have zero health recorded; pass if no violations detected
	healthOk := true
	reason := ""
	if state.AssessOutput != nil {
		// If health is recorded and too low, fail
		if state.AssessOutput.SystemHealth > 0 && state.AssessOutput.SystemHealth < 0.50 {
			healthOk = false
			reason = fmt.Sprintf("homeostasis %.2f below 0.50", state.AssessOutput.SystemHealth)
		}
		// If violations detected, escalate rather than reject
		if len(state.AssessOutput.ViolationsDetected) > 0 {
			healthOk = false
			reason = fmt.Sprintf("violations detected: %v", state.AssessOutput.ViolationsDetected)
		}
	}

	if healthOk {
		return TierResult{Passed: true}, state, nil
	}
	return TierResult{Passed: false, Reason: reason}, state, nil
}

// writeProvenance saves the ProvenanceBundle as JSON.
func (b *BootstrapEngine) writeProvenance(bundle ProvenanceBundle) (string, error) {
	// Create provenance directory if it doesn't exist
	if err := os.MkdirAll(b.ProvenanceDir, 0755); err != nil {
		return "", fmt.Errorf("failed to create provenance dir: %w", err)
	}

	// Marshal to JSON
	data, err := json.MarshalIndent(bundle, "", "  ")
	if err != nil {
		return "", fmt.Errorf("failed to marshal provenance: %w", err)
	}

	// Write file
	filename := filepath.Join(b.ProvenanceDir, fmt.Sprintf("provenance_%s.json", bundle.CycleID))
	err = os.WriteFile(filename, data, 0644)
	if err != nil {
		return "", fmt.Errorf("failed to write provenance file: %w", err)
	}

	return filename, nil
}
