package engine

import (
	"encoding/json"
	"os"
	"strings"
	"testing"
	"time"
)

func TestBootstrap_Tier1_BlocksForbiddenKeyword(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "bootstrap-test-*")
	defer os.RemoveAll(tmpDir)
	loop, _ := NewFivePhaseLoop(tmpDir)
	be := NewBootstrapEngine(loop, tmpDir)

	req := BootstrapRequest{
		PolicyID:   "test_1",
		Domain:     "auth",
		PolicyText: "disable axiom enforcement",
	}

	result, _ := be.RunBootstrap(req)

	if result.Status != "rejected" {
		t.Errorf("expected status 'rejected', got '%s'", result.Status)
	}
	if result.Tier1Result != "fail" {
		t.Errorf("expected tier1_result 'fail', got '%s'", result.Tier1Result)
	}
	if result.Tier2Result != "" {
		t.Errorf("expected tier2_result empty (short-circuited), got '%s'", result.Tier2Result)
	}
}

func TestBootstrap_Tier1_PassesValidPolicy(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "bootstrap-test-*")
	defer os.RemoveAll(tmpDir)
	loop, _ := NewFivePhaseLoop(tmpDir)
	be := NewBootstrapEngine(loop, tmpDir)

	req := BootstrapRequest{
		PolicyID:   "test_2",
		Domain:     "auth",
		PolicyText: "require password length > 12",
	}

	result, _ := be.RunBootstrap(req)

	if result.Tier1Result != "pass" {
		t.Errorf("expected tier1_result 'pass', got '%s'", result.Tier1Result)
	}
}

func TestBootstrap_Tier2_PassesWithValidConstraints(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "bootstrap-test-*")
	defer os.RemoveAll(tmpDir)
	loop, _ := NewFivePhaseLoop(tmpDir)
	be := NewBootstrapEngine(loop, tmpDir)

	req := BootstrapRequest{
		PolicyID:   "test_3",
		Domain:     "auth",
		PolicyText: "clean policy text",
	}

	result, _ := be.RunBootstrap(req)

	if result.Tier2Result != "pass" {
		t.Errorf("expected tier2_result 'pass', got '%s'", result.Tier2Result)
	}
	if result.Confidence != 0.90 {
		t.Errorf("expected confidence 0.90, got %.2f", result.Confidence)
	}
}

func TestBootstrap_Tier3_PassesWithHealthySystem(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "bootstrap-test-*")
	defer os.RemoveAll(tmpDir)
	loop, _ := NewFivePhaseLoop(tmpDir)
	be := NewBootstrapEngine(loop, tmpDir)

	req := BootstrapRequest{
		PolicyID:   "test_4",
		Domain:     "auth",
		PolicyText: "valid policy",
	}

	result, _ := be.RunBootstrap(req)

	if result.Tier3Result != "pass" {
		t.Errorf("expected tier3_result 'pass', got '%s'", result.Tier3Result)
	}
	// Homeostasis may be 0 if not yet calculated; just check it's not negative
	if result.Homeostasis < 0.0 {
		t.Errorf("expected homeostasis >= 0, got %.2f", result.Homeostasis)
	}
	if result.Status != "accepted" {
		t.Errorf("expected status 'accepted', got '%s'", result.Status)
	}
}

func TestBootstrap_QualityGate_EscalatesLowConfidence(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "bootstrap-test-*")
	defer os.RemoveAll(tmpDir)
	loop, _ := NewFivePhaseLoop(tmpDir)
	be := NewBootstrapEngine(loop, tmpDir)
	be.DomainGates["auth"] = 0.99 // Set domain gate higher than engine returns (0.90)

	req := BootstrapRequest{
		PolicyID:   "test_5",
		Domain:     "auth",
		PolicyText: "valid policy",
	}

	result, _ := be.RunBootstrap(req)

	if result.Status != "escalated" {
		t.Errorf("expected status 'escalated', got '%s'", result.Status)
	}
}

func TestBootstrap_DomainGate_AuthThreshold(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "bootstrap-test-*")
	defer os.RemoveAll(tmpDir)
	loop, _ := NewFivePhaseLoop(tmpDir)
	be := NewBootstrapEngine(loop, tmpDir)

	gate := be.domainThreshold("auth")
	if gate != 0.75 {
		t.Errorf("expected auth gate 0.75, got %.2f", gate)
	}
}

func TestBootstrap_DomainGate_UnknownDomain_FallsBackTo07(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "bootstrap-test-*")
	defer os.RemoveAll(tmpDir)
	loop, _ := NewFivePhaseLoop(tmpDir)
	be := NewBootstrapEngine(loop, tmpDir)

	gate := be.domainThreshold("unknown_domain_xyz")
	if gate != 0.7 {
		t.Errorf("expected fallback gate 0.7, got %.2f", gate)
	}
}

func TestBootstrap_ProvenanceFile_Created(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "bootstrap-test-*")
	defer os.RemoveAll(tmpDir)
	loop, _ := NewFivePhaseLoop(tmpDir)
	be := NewBootstrapEngine(loop, tmpDir)

	req := BootstrapRequest{
		PolicyID:   "test_6",
		Domain:     "auth",
		PolicyText: "valid policy",
	}

	result, _ := be.RunBootstrap(req)

	if result.ProvenanceFile == "" {
		t.Fatal("expected provenance file name")
	}

	// Verify file exists and contains valid JSON
	provPath := tmpDir + "/" + result.ProvenanceFile
	data, err := os.ReadFile(provPath)
	if err != nil {
		t.Fatalf("failed to read provenance file: %v", err)
	}

	var bundle ProvenanceBundle
	if err := json.Unmarshal(data, &bundle); err != nil {
		t.Fatalf("provenance file contains invalid JSON: %v", err)
	}

	if bundle.PolicyID != "test_6" {
		t.Errorf("expected policy_id 'test_6', got '%s'", bundle.PolicyID)
	}
	if bundle.Decision != "accepted" {
		t.Errorf("expected decision 'accepted', got '%s'", bundle.Decision)
	}
}

func TestBootstrap_ProvenanceBundle_AllTierFieldsSet(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "bootstrap-test-*")
	defer os.RemoveAll(tmpDir)
	loop, _ := NewFivePhaseLoop(tmpDir)
	be := NewBootstrapEngine(loop, tmpDir)

	req := BootstrapRequest{
		PolicyID:   "test_7",
		Domain:     "auth",
		PolicyText: "valid policy",
	}

	result, _ := be.RunBootstrap(req)

	provPath := tmpDir + "/" + result.ProvenanceFile
	data, _ := os.ReadFile(provPath)
	var bundle ProvenanceBundle
	json.Unmarshal(data, &bundle)

	if bundle.Tier1.Passed != true {
		t.Error("expected tier1.passed == true")
	}
	if bundle.Tier2.Passed != true {
		t.Error("expected tier2.passed == true")
	}
	if bundle.Tier3.Passed != true {
		t.Error("expected tier3.passed == true")
	}
}

func TestBootstrap_Result_ENCtVersion_Set(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "bootstrap-test-*")
	defer os.RemoveAll(tmpDir)
	loop, _ := NewFivePhaseLoop(tmpDir)
	be := NewBootstrapEngine(loop, tmpDir)

	req := BootstrapRequest{
		PolicyID:   "test_8",
		Domain:     "auth",
		PolicyText: "valid policy",
	}

	result, _ := be.RunBootstrap(req)

	if result.ENCtVersion != "v1.3.1" {
		t.Errorf("expected version v1.3.1, got %s", result.ENCtVersion)
	}
}

func TestBootstrap_Result_AxiomVersions_AllFour(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "bootstrap-test-*")
	defer os.RemoveAll(tmpDir)
	loop, _ := NewFivePhaseLoop(tmpDir)
	be := NewBootstrapEngine(loop, tmpDir)

	req := BootstrapRequest{
		PolicyID:   "test_9",
		Domain:     "auth",
		PolicyText: "valid policy",
	}

	result, _ := be.RunBootstrap(req)

	expectedAxioms := []string{"axiom_1", "axiom_2", "axiom_3", "axiom_4"}
	for _, ax := range expectedAxioms {
		if _, exists := result.AxiomVersions[ax]; !exists {
			t.Errorf("missing axiom version for %s", ax)
		}
		if result.AxiomVersions[ax] != "v1.3.1" {
			t.Errorf("expected %s version v1.3.1, got %s", ax, result.AxiomVersions[ax])
		}
	}
}

func TestCandidateModule_QualityGateDefault(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "bootstrap-test-*")
	defer os.RemoveAll(tmpDir)
	loop, _ := NewFivePhaseLoop(tmpDir)
	be := NewBootstrapEngine(loop, tmpDir)

	if be.QualityGate != 0.7 {
		t.Errorf("expected default quality gate 0.7, got %.2f", be.QualityGate)
	}
}

// TestProvenance_TimestampValid verifies that on-disk provenance files contain
// a valid timestamp within 5 seconds of the current time.
func TestProvenance_TimestampValid(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "provenance-timestamp-*")
	defer os.RemoveAll(tmpDir)
	loop, _ := NewFivePhaseLoop(tmpDir)
	be := NewBootstrapEngine(loop, tmpDir)

	req := BootstrapRequest{
		PolicyID:   "ts_test_policy",
		Domain:     "auth",
		PolicyText: "add user with role viewer",
	}

	beforeTime := time.Now()
	result, _ := be.RunBootstrap(req)
	afterTime := time.Now()

	if result.ProvenanceFile == "" {
		t.Fatalf("No provenance file created")
	}

	// Read the provenance file from disk
	provPath := tmpDir + "/" + result.ProvenanceFile
	data, err := os.ReadFile(provPath)
	if err != nil {
		t.Fatalf("Failed to read provenance file: %v", err)
	}

	var bundle ProvenanceBundle
	if err := json.Unmarshal(data, &bundle); err != nil {
		t.Fatalf("Failed to unmarshal provenance JSON: %v", err)
	}

	// Verify timestamp is within 5 seconds of the bootstrap call
	if bundle.Timestamp.Before(beforeTime.Add(-5*time.Second)) || bundle.Timestamp.After(afterTime.Add(5*time.Second)) {
		t.Errorf("Provenance timestamp %v is outside expected window [%v, %v]",
			bundle.Timestamp, beforeTime, afterTime)
	}
}

// TestProvenance_AxiomVersions_OnDisk verifies that the on-disk provenance JSON
// contains all four axiom versions set to "v1.3.1".
func TestProvenance_AxiomVersions_OnDisk(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "provenance-versions-*")
	defer os.RemoveAll(tmpDir)
	loop, _ := NewFivePhaseLoop(tmpDir)
	be := NewBootstrapEngine(loop, tmpDir)

	req := BootstrapRequest{
		PolicyID:   "av_test_policy",
		Domain:     "compliance",
		PolicyText: "enable audit logging",
	}

	result, _ := be.RunBootstrap(req)

	if result.ProvenanceFile == "" {
		t.Fatalf("No provenance file created")
	}

	provPath := tmpDir + "/" + result.ProvenanceFile
	data, err := os.ReadFile(provPath)
	if err != nil {
		t.Fatalf("Failed to read provenance file: %v", err)
	}

	var bundle ProvenanceBundle
	if err := json.Unmarshal(data, &bundle); err != nil {
		t.Fatalf("Failed to unmarshal provenance JSON: %v", err)
	}

	// Verify all four axiom versions are present and set to v1.3.1
	axiomKeys := []string{"axiom_1", "axiom_2", "axiom_3", "axiom_4"}
	for _, axiom := range axiomKeys {
		if version, exists := bundle.AxiomVersions[axiom]; !exists {
			t.Errorf("Missing %s in AxiomVersions", axiom)
		} else if version != "v1.3.1" {
			t.Errorf("Expected %s version v1.3.1, got %s", axiom, version)
		}
	}
}

// TestProvenance_CycleID_LinkedToLedger verifies that the CycleID in the provenance
// bundle matches a ledger file in the ledger directory.
func TestProvenance_CycleID_LinkedToLedger(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "provenance-linkage-*")
	defer os.RemoveAll(tmpDir)
	loop, _ := NewFivePhaseLoop(tmpDir)
	be := NewBootstrapEngine(loop, tmpDir)

	req := BootstrapRequest{
		PolicyID:   "cid_test_policy",
		Domain:     "auth",
		PolicyText: "rotate encryption keys",
	}

	result, _ := be.RunBootstrap(req)

	if result.ProvenanceFile == "" {
		t.Fatalf("No provenance file created")
	}

	provPath := tmpDir + "/" + result.ProvenanceFile
	data, err := os.ReadFile(provPath)
	if err != nil {
		t.Fatalf("Failed to read provenance file: %v", err)
	}

	var bundle ProvenanceBundle
	if err := json.Unmarshal(data, &bundle); err != nil {
		t.Fatalf("Failed to unmarshal provenance JSON: %v", err)
	}

	// Verify the CycleID exists in at least one ledger file
	cycleID := bundle.CycleID
	ledgerEntries, err := os.ReadDir(tmpDir)
	if err != nil {
		t.Fatalf("Failed to read ledger directory: %v", err)
	}

	found := false
	for _, entry := range ledgerEntries {
		if strings.Contains(entry.Name(), cycleID) && strings.HasSuffix(entry.Name(), ".json") {
			found = true
			break
		}
	}

	if !found {
		t.Errorf("CycleID %q not found in any ledger file", cycleID)
	}
}

// TestProvenance_RejectedPolicy_FileCreated verifies that a Tier 1 rejected policy
// still writes a provenance file with Decision="rejected".
func TestProvenance_RejectedPolicy_FileCreated(t *testing.T) {
	tmpDir, _ := os.MkdirTemp("", "provenance-rejected-*")
	defer os.RemoveAll(tmpDir)
	loop, _ := NewFivePhaseLoop(tmpDir)
	be := NewBootstrapEngine(loop, tmpDir)

	// Policy that violates Axiom 1
	req := BootstrapRequest{
		PolicyID:   "rejected_test",
		Domain:     "auth",
		PolicyText: "disable axiom enforcement",
	}

	result, _ := be.RunBootstrap(req)

	// Verify result is rejected
	if result.Status != "rejected" {
		t.Errorf("Expected status 'rejected', got '%s'", result.Status)
	}

	// Verify provenance file was written despite rejection
	if result.ProvenanceFile == "" {
		t.Fatalf("No provenance file created for rejected policy")
	}

	provPath := tmpDir + "/" + result.ProvenanceFile
	data, err := os.ReadFile(provPath)
	if err != nil {
		t.Fatalf("Failed to read provenance file: %v", err)
	}

	var bundle ProvenanceBundle
	if err := json.Unmarshal(data, &bundle); err != nil {
		t.Fatalf("Failed to unmarshal provenance JSON: %v", err)
	}

	// Verify decision is "rejected"
	if bundle.Decision != "rejected" {
		t.Errorf("Expected decision 'rejected', got '%s'", bundle.Decision)
	}

	// Verify RejectedReason is set
	if bundle.RejectedReason == "" {
		t.Errorf("Expected RejectedReason to be set for rejected policy")
	}

	// Verify Tier 1 failed
	if bundle.Tier1.Passed {
		t.Errorf("Expected Tier 1 to fail, but it passed")
	}
}
