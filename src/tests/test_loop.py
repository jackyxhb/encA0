"""
Unit Tests for ENCT 5-Phase Loop Engine

Tests verify:
- Fail-hard semantics on axiom violations
- Full state persistence to ledgers
- Complete cycle execution
- Atomic transitions
- Reproducibility from ledgers

Target: >95% code coverage of Loop engine.
"""

import pytest
import sys
import tempfile
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from enct.axioms import (
    Axiom1ImmutabilityViolation,
    AxiomViolationException,
)
from enct.loop import (
    FivePhaseLoop,
    LoopPhase,
    LoopStatus,
    LoopCycleState,
    LedgerWriter,
    PolicyLedgerEntryStatus,
    FailureLedgerSeverity,
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def temp_ledger_dir():
    """Create temporary ledger directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def loop_engine(temp_ledger_dir):
    """Create FivePhaseLoop instance with temporary ledgers."""
    return FivePhaseLoop(ledger_root=temp_ledger_dir)


@pytest.fixture
def valid_policy_request():
    """Valid policy request that should pass validation."""
    return {
        "domain": "auth",
        "constraint": "confidence > 0.75",
        "escalation": "human_review",
    }


@pytest.fixture
def invalid_policy_request():
    """Invalid policy request that violates Axiom 1."""
    return {
        "action": "disable axiom enforcement",
        "domain": "auth",
    }


@pytest.fixture
def environment_state():
    """Sample environment state."""
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "system_load": 0.65,
        "error_rate": 0.02,
        "policy_count": 42,
    }


# ============================================================================
# Test: Fail-Hard on Axiom Violations
# ============================================================================

class TestLoopFailHardSemantics:
    """Test fail-hard semantics: Loop stops immediately on axiom violation."""

    def test_loop_fails_on_axiom_1_violation(self, loop_engine, invalid_policy_request, environment_state):
        """Loop should fail immediately when Axiom 1 is violated."""
        state = loop_engine.execute_cycle(invalid_policy_request, environment_state)

        # Verify fail-hard: Loop stopped, status is AXIOM_VIOLATION
        assert state.status == LoopStatus.AXIOM_VIOLATION
        assert state.error is not None
        assert "AXIOM 1 VIOLATION" in state.error
        assert state.current_phase == LoopPhase.VALIDATE  # Failed in Validate phase

    def test_loop_incomplete_on_axiom_violation(self, loop_engine, invalid_policy_request, environment_state):
        """Loop should not progress past violation phase."""
        state = loop_engine.execute_cycle(invalid_policy_request, environment_state)

        # Only Sense and Validate phases should have outputs
        assert state.sense_output is not None  # Sense completed
        assert state.validate_output is None  # Validate failed
        assert state.execute_output is None  # Not reached
        assert state.assess_output is None  # Not reached
        assert state.reenact_output is None  # Not reached

    def test_axiom_violation_logs_to_failure_ledger(self, loop_engine, invalid_policy_request, environment_state):
        """Axiom violations should be logged to failure ledger."""
        state = loop_engine.execute_cycle(invalid_policy_request, environment_state)

        # Verify failure ledger entry created
        assert state.failure_ledger_entry_id is not None
        assert state.failure_ledger_entry_id.startswith("failure_")

    def test_axiom_violation_details_preserved(self, loop_engine, invalid_policy_request, environment_state):
        """Axiom violation details should be preserved in state."""
        state = loop_engine.execute_cycle(invalid_policy_request, environment_state)

        # Verify error details
        assert state.error_phase == LoopPhase.VALIDATE
        assert state.error_details is not None
        assert state.error_details.get("axiom") == 1
        assert state.error_details.get("type") == "axiom_violation"

    def test_loop_no_recovery_attempt(self, loop_engine, invalid_policy_request, environment_state):
        """Loop should not attempt recovery from axiom violations."""
        state = loop_engine.execute_cycle(invalid_policy_request, environment_state)

        # Verify end_time is set (cycle ended abruptly)
        assert state.end_time is not None
        # Verify status is failed, not retried
        assert state.status == LoopStatus.AXIOM_VIOLATION


# ============================================================================
# Test: Complete Cycle Execution
# ============================================================================

class TestLoopCompleteCycle:
    """Test successful complete cycle execution."""

    def test_loop_completes_all_phases(self, loop_engine, valid_policy_request, environment_state):
        """Valid cycle should complete all 5 phases."""
        state = loop_engine.execute_cycle(valid_policy_request, environment_state)

        # Verify all phases completed
        assert state.status == LoopStatus.COMPLETE
        assert state.sense_output is not None
        assert state.validate_output is not None
        assert state.execute_output is not None
        assert state.assess_output is not None
        assert state.reenact_output is not None

    def test_loop_cycle_has_timestamps(self, loop_engine, valid_policy_request, environment_state):
        """All phase outputs should have timestamps."""
        state = loop_engine.execute_cycle(valid_policy_request, environment_state)

        assert state.start_time is not None
        assert state.end_time is not None
        assert state.sense_output.timestamp is not None
        assert state.validate_output.timestamp is not None
        assert state.execute_output.timestamp is not None
        assert state.assess_output.timestamp is not None
        assert state.reenact_output.timestamp is not None

    def test_loop_cycle_has_id(self, loop_engine, valid_policy_request, environment_state):
        """Each cycle should have unique ID."""
        state1 = loop_engine.execute_cycle(valid_policy_request, environment_state)
        state2 = loop_engine.execute_cycle(valid_policy_request, environment_state)

        assert state1.cycle_id is not None
        assert state2.cycle_id is not None
        assert state1.cycle_id != state2.cycle_id

    def test_validate_phase_enforces_axioms(self, loop_engine, valid_policy_request, environment_state):
        """Validate phase should enforce all axioms."""
        state = loop_engine.execute_cycle(valid_policy_request, environment_state)

        # Verify Axiom enforcement checks passed
        assert state.validate_output.passed is True
        assert state.validate_output.constraint_checks["immutability"] is True
        assert state.validate_output.constraint_checks["enforceability"] is True
        assert state.validate_output.constraint_checks["determinism"] is True

    def test_validate_phase_has_uncertainty_bounds(self, loop_engine, valid_policy_request, environment_state):
        """Validate phase should include uncertainty bounds (Axiom 2)."""
        state = loop_engine.execute_cycle(valid_policy_request, environment_state)

        bounds = state.validate_output.uncertainty_bounds
        assert "epistemic_lower" in bounds
        assert "epistemic_upper" in bounds
        assert "aleatoric" in bounds
        assert bounds["epistemic_lower"] <= state.validate_output.confidence <= bounds["epistemic_upper"]

    def test_execute_phase_produces_outcome(self, loop_engine, valid_policy_request, environment_state):
        """Execute phase should produce action outcome."""
        state = loop_engine.execute_cycle(valid_policy_request, environment_state)

        assert state.execute_output.outcome is not None
        assert state.execute_output.action_taken is not None
        assert isinstance(state.execute_output.side_effects, list)

    def test_assess_phase_calculates_metrics(self, loop_engine, valid_policy_request, environment_state):
        """Assess phase should calculate all 8 indicators."""
        state = loop_engine.execute_cycle(valid_policy_request, environment_state)

        expected_metrics = {
            "compliance_rate",
            "homeostasis_score",
            "traceability_coverage",
            "bootstrap_confidence",
            "adaptation_resilience",
            "provenance_overhead",
            "axiom_violation_rate",
            "policy_rollback_rate",
        }

        actual_metrics = set(state.assess_output.metrics.keys())
        assert expected_metrics == actual_metrics

    def test_assess_phase_calculates_system_health(self, loop_engine, valid_policy_request, environment_state):
        """Assess phase should calculate overall system health."""
        state = loop_engine.execute_cycle(valid_policy_request, environment_state)

        health = state.assess_output.system_health
        assert 0.0 <= health <= 1.0

    def test_reenact_phase_may_make_adaptations(self, loop_engine, valid_policy_request, environment_state):
        """Re-enact phase should evaluate and possibly make adaptations."""
        state = loop_engine.execute_cycle(valid_policy_request, environment_state)

        # Adaptations list may be empty or populated
        assert isinstance(state.reenact_output.adaptations_made, list)
        # If version updated, should have new version
        if state.reenact_output.version_updated:
            assert state.reenact_output.new_version is not None


# ============================================================================
# Test: Ledger Persistence
# ============================================================================

class TestLoopLedgerPersistence:
    """Test that all Loop state is persisted to ledgers."""

    def test_policy_ledger_entries_created(self, loop_engine, valid_policy_request, environment_state):
        """Each phase should create policy ledger entry."""
        state = loop_engine.execute_cycle(valid_policy_request, environment_state)

        assert state.policy_ledger_entry_id is not None
        assert state.policy_ledger_entry_id.startswith("phase_")

    def test_ledger_entries_readable(self, loop_engine, valid_policy_request, environment_state, temp_ledger_dir):
        """Ledger entries should be readable after write."""
        state = loop_engine.execute_cycle(valid_policy_request, environment_state)

        # Read cycle history
        history = loop_engine.ledger_writer.read_cycle_history(state.cycle_id)
        assert len(history["policy_entries"]) > 0

    def test_ledger_persists_on_failure(self, loop_engine, invalid_policy_request, environment_state):
        """Failure ledger should record axiom violations."""
        state = loop_engine.execute_cycle(invalid_policy_request, environment_state)

        assert state.failure_ledger_entry_id is not None
        # Read failure history
        history = loop_engine.ledger_writer.read_cycle_history(state.cycle_id)
        assert len(history["failure_entries"]) > 0

    def test_ledger_atomic_writes(self, loop_engine, valid_policy_request, environment_state, temp_ledger_dir):
        """Ledger writes should be atomic."""
        state = loop_engine.execute_cycle(valid_policy_request, environment_state)

        # All ledger files should exist and be readable
        policy_ledger = temp_ledger_dir / "POLICY-LEDGER.jsonl"
        assert policy_ledger.exists()

        # Should have valid JSON lines
        with open(policy_ledger) as f:
            lines = f.readlines()
            assert len(lines) > 0
            for line in lines:
                if line.strip():  # Skip empty lines
                    import json
                    json.loads(line)  # Should not raise


# ============================================================================
# Test: State Preservation
# ============================================================================

class TestLoopStatePreservation:
    """Test that Loop state is completely preserved and serializable."""

    def test_cycle_state_to_dict(self, loop_engine, valid_policy_request, environment_state):
        """LoopCycleState should serialize to dict."""
        state = loop_engine.execute_cycle(valid_policy_request, environment_state)

        state_dict = state.to_dict()
        assert isinstance(state_dict, dict)
        assert "cycle_id" in state_dict
        assert "status" in state_dict
        assert "sense_output" in state_dict
        assert "validate_output" in state_dict

    def test_cycle_state_preserves_environment(self, loop_engine, valid_policy_request, environment_state):
        """Loop should preserve environment observations."""
        state = loop_engine.execute_cycle(valid_policy_request, environment_state)

        # Environment should be preserved in Sense output
        assert state.sense_output.observations["system_load"] == environment_state["system_load"]
        assert state.sense_output.observations["error_rate"] == environment_state["error_rate"]

    def test_cycle_state_preserves_policy(self, loop_engine, valid_policy_request, environment_state):
        """Loop should preserve policy request."""
        state = loop_engine.execute_cycle(valid_policy_request, environment_state)

        # Policy should be preserved in Sense output
        assert state.sense_output.policy_request["domain"] == valid_policy_request["domain"]
        assert state.sense_output.policy_request["constraint"] == valid_policy_request["constraint"]


# ============================================================================
# Test: Reproducibility
# ============================================================================

class TestLoopReproducibility:
    """Test that Loop cycles are reproducible from state."""

    def test_cycle_reproducible_from_sense_output(self, loop_engine, valid_policy_request, environment_state):
        """Same inputs should produce same outputs."""
        state1 = loop_engine.execute_cycle(valid_policy_request, environment_state)
        state2 = loop_engine.execute_cycle(valid_policy_request, environment_state)

        # Both should complete successfully
        assert state1.status == LoopStatus.COMPLETE
        assert state2.status == LoopStatus.COMPLETE

        # Both should have same validation result
        assert state1.validate_output.confidence == state2.validate_output.confidence
        assert state1.validate_output.passed == state2.validate_output.passed


# ============================================================================
# Test: Error Handling
# ============================================================================

class TestLoopErrorHandling:
    """Test Loop error handling and recovery."""

    def test_loop_handles_unexpected_errors(self, loop_engine):
        """Loop should handle unexpected errors gracefully."""
        # Pass invalid input
        state = loop_engine.execute_cycle({}, {})

        # Should still return state with error info
        assert state.status in (LoopStatus.FAILED, LoopStatus.AXIOM_VIOLATION)
        assert state.error is not None

    def test_loop_logs_errors(self, loop_engine, invalid_policy_request, environment_state, caplog):
        """Loop should log all errors."""
        state = loop_engine.execute_cycle(invalid_policy_request, environment_state)

        # Should have logged critical error
        assert any(
            "axiom violation" in record.message.lower()
            for record in caplog.records
            if record.levelname == "CRITICAL"
        )


# ============================================================================
# Integration Tests
# ============================================================================

class TestLoopIntegration:
    """Integration tests across complete system."""

    def test_valid_cycle_end_to_end(self, loop_engine, valid_policy_request, environment_state):
        """Valid cycle should execute completely and persistently."""
        state = loop_engine.execute_cycle(valid_policy_request, environment_state)

        # Verify complete execution
        assert state.status == LoopStatus.COMPLETE
        assert state.cycle_id is not None
        assert state.start_time is not None
        assert state.end_time is not None

        # Verify all outputs present
        assert state.sense_output is not None
        assert state.validate_output is not None
        assert state.execute_output is not None
        assert state.assess_output is not None
        assert state.reenact_output is not None

        # Verify ledger references
        assert state.policy_ledger_entry_id is not None

    def test_invalid_cycle_fails_safely(self, loop_engine, invalid_policy_request, environment_state):
        """Invalid cycle should fail safely with full error info."""
        state = loop_engine.execute_cycle(invalid_policy_request, environment_state)

        # Verify failure captured
        assert state.status == LoopStatus.AXIOM_VIOLATION
        assert state.error is not None
        assert state.error_phase is not None
        assert state.failure_ledger_entry_id is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src/enct/loop", "--cov-report=term-missing"])
