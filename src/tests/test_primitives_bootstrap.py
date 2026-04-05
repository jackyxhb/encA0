"""
Unit Tests for ENCT Primitives and Bootstrap Engine

Tests verify:
- Primitives are immutable (write-once)
- Version chains work correctly
- Bootstrap hybrid initialization succeeds
- Checksums verify integrity

Target: >95% code coverage.
"""

import pytest
import sys
import tempfile
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from enct.primitives import (
    Fact,
    Policy,
    Constraint,
    Event,
    PrimitiveType,
)
from enct.bootstrap import BootstrapEngine


# ============================================================================
# Test: Primitive Immutability
# ============================================================================

class TestPrimitiveImmutability:
    """Test that all primitives are immutable."""

    def test_fact_is_frozen(self):
        """Fact instances should be immutable."""
        fact = Fact(fact_id="test", content={"key": "value"})

        # Attempt to modify should raise FrozenInstanceError
        with pytest.raises((TypeError, AttributeError)):
            fact.content["key"] = "modified"

    def test_policy_is_frozen(self):
        """Policy instances should be immutable."""
        policy = Policy(policy_id="test", rule="test_rule")

        with pytest.raises((TypeError, AttributeError)):
            policy.rule = "modified_rule"

    def test_constraint_is_frozen(self):
        """Constraint instances should be immutable."""
        constraint = Constraint(constraint_id="test", expression="test_expr")

        with pytest.raises((TypeError, AttributeError)):
            constraint.expression = "modified"

    def test_event_is_frozen(self):
        """Event instances should be immutable."""
        event = Event(event_id="test", event_type="test_type")

        with pytest.raises((TypeError, AttributeError)):
            event.event_type = "modified"


# ============================================================================
# Test: Version Chains
# ============================================================================

class TestVersionChains:
    """Test immutable version chain pattern."""

    def test_fact_evolve_creates_new_version(self):
        """Fact.evolve() should create new v2 instance."""
        fact_v1 = Fact(fact_id="test", version=1, content={"state": "initial"})
        fact_v2 = fact_v1.evolve({"state": "updated"})

        # V1 unchanged
        assert fact_v1.version == 1
        assert fact_v1.content["state"] == "initial"

        # V2 is new instance
        assert fact_v2.version == 2
        assert fact_v2.content["state"] == "updated"
        assert fact_v2.prior_version_id == "test_v1"

    def test_policy_evolve_creates_new_version(self):
        """Policy.evolve() should create new version."""
        policy_v1 = Policy(
            policy_id="test",
            version=1,
            domain="auth",
            rule="confidence > 0.75",
            confidence=0.75,
        )
        policy_v2 = policy_v1.evolve("confidence > 0.80", 0.80)

        assert policy_v1.version == 1
        assert policy_v2.version == 2
        assert policy_v2.confidence == 0.80
        assert policy_v2.prior_version_id == "test_v1"

    def test_constraint_evolve_creates_new_version(self):
        """Constraint.evolve() should create new version."""
        constraint_v1 = Constraint(
            constraint_id="test",
            name="test_constraint",
            expression="x > 0",
        )
        constraint_v2 = constraint_v1.evolve("x > 10")

        assert constraint_v1.version == 1
        assert constraint_v2.version == 2
        assert constraint_v2.expression == "x > 10"
        assert constraint_v2.prior_version_id == "test_v1"

    def test_event_no_evolve(self):
        """Events are append-only; no evolve method."""
        event = Event(event_id="test", event_type="action_taken")

        # Events should not have evolve method
        assert not hasattr(event, 'evolve')

    def test_version_chain_immutable(self):
        """Entire version chain should be immutable."""
        v1 = Fact(fact_id="test", content={"v": 1})
        v2 = v1.evolve({"v": 2})
        v3 = v2.evolve({"v": 3})

        # All immutable
        with pytest.raises((TypeError, AttributeError)):
            v1.content["v"] = 99
        with pytest.raises((TypeError, AttributeError)):
            v2.content["v"] = 99
        with pytest.raises((TypeError, AttributeError)):
            v3.content["v"] = 99


# ============================================================================
# Test: Checksums & Integrity
# ============================================================================

class TestChecksumIntegrity:
    """Test that primitives have integrity checksums."""

    def test_fact_has_checksum(self):
        """Fact should compute SHA256 checksum."""
        fact = Fact(fact_id="test", content={"data": "value"})
        assert fact.checksum is not None
        assert len(fact.checksum) == 64  # SHA256 hex

    def test_policy_has_checksum(self):
        """Policy should compute SHA256 checksum."""
        policy = Policy(policy_id="test", rule="test_rule", confidence=0.8)
        assert policy.checksum is not None
        assert len(policy.checksum) == 64

    def test_constraint_has_checksum(self):
        """Constraint should compute SHA256 checksum."""
        constraint = Constraint(constraint_id="test", expression="x > 0")
        assert constraint.checksum is not None
        assert len(constraint.checksum) == 64

    def test_event_has_checksum(self):
        """Event should compute SHA256 checksum."""
        event = Event(event_id="test", event_type="action")
        assert event.checksum is not None
        assert len(event.checksum) == 64

    def test_same_content_same_checksum(self):
        """Same content should yield same checksum."""
        fact1 = Fact(fact_id="test", content={"key": "value"})
        fact2 = Fact(fact_id="test", content={"key": "value"})

        assert fact1.checksum == fact2.checksum

    def test_different_content_different_checksum(self):
        """Different content should yield different checksum."""
        fact1 = Fact(fact_id="test", content={"key": "value1"})
        fact2 = Fact(fact_id="test", content={"key": "value2"})

        assert fact1.checksum != fact2.checksum


# ============================================================================
# Test: Primitive Properties
# ============================================================================

class TestPrimitiveProperties:
    """Test primitive properties and methods."""

    def test_fact_full_id(self):
        """Fact.full_id should include version."""
        fact = Fact(fact_id="test_fact", version=3)
        assert fact.full_id == "test_fact_v3"

    def test_policy_full_id(self):
        """Policy.full_id should include version."""
        policy = Policy(policy_id="test_policy", version=2)
        assert policy.full_id == "test_policy_v2"

    def test_constraint_full_id(self):
        """Constraint.full_id should include version."""
        constraint = Constraint(constraint_id="test_constraint", version=5)
        assert constraint.full_id == "test_constraint_v5"

    def test_event_full_id(self):
        """Event.full_id should be unique."""
        event = Event(event_id="test_event", event_type="action")
        assert "test_event" in event.full_id
        assert event.timestamp in event.full_id


# ============================================================================
# Test: Bootstrap Initialization
# ============================================================================

class TestBootstrapInitialization:
    """Test bootstrap engine hybrid initialization."""

    def test_bootstrap_engine_creates_state(self):
        """Bootstrap should return complete agent state."""
        with tempfile.TemporaryDirectory() as tmpdir:
            engine = BootstrapEngine(ledger_root=Path(tmpdir))
            state = engine.bootstrap()

            assert state["status"] == "ready"
            assert "facts" in state
            assert "policies" in state
            assert "constraints" in state
            assert "events" in state
            assert "initialized_at" in state

    def test_bootstrap_loads_static_facts(self):
        """Bootstrap should load foundational facts."""
        with tempfile.TemporaryDirectory() as tmpdir:
            engine = BootstrapEngine(ledger_root=Path(tmpdir))
            state = engine.bootstrap()

            facts = state["facts"]
            assert len(facts) >= 2
            assert any(f.fact_id == "system_initialized" for f in facts)
            assert any(f.fact_id == "axioms_loaded" for f in facts)

    def test_bootstrap_loads_static_policies(self):
        """Bootstrap should load foundational policies."""
        with tempfile.TemporaryDirectory() as tmpdir:
            engine = BootstrapEngine(ledger_root=Path(tmpdir))
            state = engine.bootstrap()

            policies = state["policies"]
            assert len(policies) >= 2
            assert any(p.policy_id == "base_compliance" for p in policies)
            assert any(p.policy_id == "base_traceability" for p in policies)

    def test_bootstrap_loads_static_constraints(self):
        """Bootstrap should load foundational constraints."""
        with tempfile.TemporaryDirectory() as tmpdir:
            engine = BootstrapEngine(ledger_root=Path(tmpdir))
            state = engine.bootstrap()

            constraints = state["constraints"]
            assert len(constraints) >= 3
            constraint_ids = {c.constraint_id for c in constraints}
            assert "immutability_constraint" in constraint_ids
            assert "determinism_constraint" in constraint_ids
            assert "enforcement_constraint" in constraint_ids

    def test_bootstrap_all_facts_immutable(self):
        """All facts from bootstrap should be immutable."""
        with tempfile.TemporaryDirectory() as tmpdir:
            engine = BootstrapEngine(ledger_root=Path(tmpdir))
            state = engine.bootstrap()

            for fact in state["facts"]:
                with pytest.raises((TypeError, AttributeError)):
                    fact.content["key"] = "value"

    def test_bootstrap_all_policies_immutable(self):
        """All policies from bootstrap should be immutable."""
        with tempfile.TemporaryDirectory() as tmpdir:
            engine = BootstrapEngine(ledger_root=Path(tmpdir))
            state = engine.bootstrap()

            for policy in state["policies"]:
                with pytest.raises((TypeError, AttributeError)):
                    policy.rule = "modified"

    def test_bootstrap_all_constraints_immutable(self):
        """All constraints from bootstrap should be immutable."""
        with tempfile.TemporaryDirectory() as tmpdir:
            engine = BootstrapEngine(ledger_root=Path(tmpdir))
            state = engine.bootstrap()

            for constraint in state["constraints"]:
                with pytest.raises((TypeError, AttributeError)):
                    constraint.expression = "modified"

    def test_bootstrap_version_count(self):
        """Bootstrap should report version count."""
        with tempfile.TemporaryDirectory() as tmpdir:
            engine = BootstrapEngine(ledger_root=Path(tmpdir))
            state = engine.bootstrap()

            version_count = state["version_count"]
            assert version_count > 0

    def test_bootstrap_multiple_times_same_result(self):
        """Running bootstrap twice on same ledger should yield same state."""
        with tempfile.TemporaryDirectory() as tmpdir:
            engine = BootstrapEngine(ledger_root=Path(tmpdir))
            state1 = engine.bootstrap()
            state2 = engine.bootstrap()

            # Same number of facts/policies/constraints
            assert len(state1["facts"]) == len(state2["facts"])
            assert len(state1["policies"]) == len(state2["policies"])
            assert len(state1["constraints"]) == len(state2["constraints"])


# ============================================================================
# Test: Edge Cases
# ============================================================================

class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_fact_with_empty_content(self):
        """Fact with empty content should work."""
        fact = Fact(fact_id="test", content={})
        assert fact.content == {}

    def test_fact_with_nested_content(self):
        """Fact with nested content should compute checksum."""
        fact = Fact(
            fact_id="test",
            content={
                "nested": {
                    "level": {
                        "deep": "value"
                    }
                }
            }
        )
        assert fact.checksum is not None

    def test_policy_with_zero_confidence(self):
        """Policy can have zero confidence."""
        policy = Policy(policy_id="test", confidence=0.0)
        assert policy.confidence == 0.0

    def test_policy_with_100_confidence(self):
        """Policy can have 100% confidence."""
        policy = Policy(policy_id="test", confidence=1.0)
        assert policy.confidence == 1.0

    def test_constraint_enforcement_flag(self):
        """Constraint enforcement flag should be preserved."""
        enforced = Constraint(constraint_id="test1", enforced=True)
        not_enforced = Constraint(constraint_id="test2", enforced=False)

        assert enforced.enforced is True
        assert not_enforced.enforced is False

    def test_event_with_complex_payload(self):
        """Event should handle complex payloads."""
        event = Event(
            event_id="test",
            event_type="policy_submitted",
            payload={
                "policy_id": "test_policy",
                "domain": "auth",
                "constraints": ["c1", "c2", "c3"],
            }
        )
        assert event.payload["policy_id"] == "test_policy"
        assert len(event.payload["constraints"]) == 3


# ============================================================================
# Integration Tests
# ============================================================================

class TestBootstrapIntegration:
    """Integration tests across bootstrap and primitives."""

    def test_bootstrap_axiom_facts_immutable(self):
        """Axiom facts from bootstrap should be immutable."""
        with tempfile.TemporaryDirectory() as tmpdir:
            engine = BootstrapEngine(ledger_root=Path(tmpdir))
            state = engine.bootstrap()

            axiom_fact = next(f for f in state["facts"] if f.fact_id == "axioms_loaded")
            assert "axiom_1" in axiom_fact.content

            # Should be immutable
            with pytest.raises((TypeError, AttributeError)):
                axiom_fact.content["axiom_1"] = "modified"

    def test_bootstrap_creates_coherent_system(self):
        """Bootstrap should create coherent initial state."""
        with tempfile.TemporaryDirectory() as tmpdir:
            engine = BootstrapEngine(ledger_root=Path(tmpdir))
            state = engine.bootstrap()

            # All axioms present
            axiom_fact = next(f for f in state["facts"] if f.fact_id == "axioms_loaded")
            for axiom_num in [1, 2, 3, 4]:
                assert f"axiom_{axiom_num}" in axiom_fact.content

            # All foundational constraints enforced
            for constraint in state["constraints"]:
                assert constraint.enforced is True


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src/enct/primitives", "--cov=src/enct/bootstrap", "--cov-report=term-missing"])
