package engine

import (
	"os"
	"testing"
)

// BenchmarkBootstrap_Tier1 benchmarks the Tier 1 (Axiom 1) validation cost
func BenchmarkBootstrap_Tier1(b *testing.B) {
	tmpDir, _ := os.MkdirTemp("", "bench-tier1-*")
	defer os.RemoveAll(tmpDir)

	loop, _ := NewFivePhaseLoop(tmpDir)
	be := NewBootstrapEngine(loop, tmpDir)

	req := BootstrapRequest{
		PolicyID:   "bench-t1-policy",
		Domain:     "auth",
		PolicyText: "add user with role viewer",
		Metadata:   map[string]interface{}{},
	}

	b.ResetTimer()
	b.ReportAllocs()

	for i := 0; i < b.N; i++ {
		be.RunBootstrap(req)
	}
}

// BenchmarkBootstrap_Tier2 benchmarks the Tier 1+2 (Axiom 1,2,3) validation cost
func BenchmarkBootstrap_Tier2(b *testing.B) {
	tmpDir, _ := os.MkdirTemp("", "bench-tier2-*")
	defer os.RemoveAll(tmpDir)

	loop, _ := NewFivePhaseLoop(tmpDir)
	be := NewBootstrapEngine(loop, tmpDir)

	req := BootstrapRequest{
		PolicyID:   "bench-t2-policy",
		Domain:     "api_rate_limiting",
		PolicyText: "set rate limit to 1000 requests per minute",
		Metadata:   map[string]interface{}{},
	}

	b.ResetTimer()
	b.ReportAllocs()

	for i := 0; i < b.N; i++ {
		be.RunBootstrap(req)
	}
}

// BenchmarkBootstrap_Tier3 benchmarks the full 3-tier bootstrap including cycle execution
func BenchmarkBootstrap_Tier3(b *testing.B) {
	tmpDir, _ := os.MkdirTemp("", "bench-tier3-*")
	defer os.RemoveAll(tmpDir)

	loop, _ := NewFivePhaseLoop(tmpDir)
	be := NewBootstrapEngine(loop, tmpDir)

	req := BootstrapRequest{
		PolicyID:   "bench-t3-policy",
		Domain:     "compliance",
		PolicyText: "enable audit logging for all API calls",
		Metadata:   map[string]interface{}{},
	}

	b.ResetTimer()
	b.ReportAllocs()

	for i := 0; i < b.N; i++ {
		be.RunBootstrap(req)
	}
}

// BenchmarkCycle_FullLoop benchmarks a complete ExecuteCycle call
func BenchmarkCycle_FullLoop(b *testing.B) {
	tmpDir, _ := os.MkdirTemp("", "bench-cycle-*")
	defer os.RemoveAll(tmpDir)

	loop, _ := NewFivePhaseLoop(tmpDir)

	policyRequest := map[string]interface{}{
		"action": "rotate encryption keys",
	}

	envState := map[string]interface{}{
		"system_load": 0.5,
		"error_rate":  0.01,
	}

	b.ResetTimer()
	b.ReportAllocs()

	for i := 0; i < b.N; i++ {
		loop.ExecuteCycle(policyRequest, envState)
	}
}
