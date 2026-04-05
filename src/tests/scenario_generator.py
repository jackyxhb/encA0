"""
ENCT Phase 3: Synthetic Scenario Generator

Generates all 500+ test scenarios programmatically.
Provides framework for creating axiom, domain, and edge case scenarios.
"""

import logging
from typing import Any, Callable, Optional
from datetime import datetime

from scenario_definitions import (
    Scenario,
    ScenarioCategory,
    ExpectedOutcome,
    SeverityLevel,
)
from scenario_executor import ScenarioExecutor
from scenario_verifiers import ScenarioVerifier

logger = logging.getLogger(__name__)


class SyntheticScenarioGenerator:
    """
    Generator for all 500+ synthetic test scenarios.

    Creates scenarios across:
    - Axiom violations (160 scenarios)
    - Domain-specific tests (250 scenarios)
    - Edge cases (90 scenarios)
    """

    def __init__(self):
        """Initialize generator."""
        self.scenarios: list[Scenario] = []
        self.scenario_count = 0
        self.executor = ScenarioExecutor()
        self.verifier = ScenarioVerifier()

    def generate_all_scenarios(self) -> list[Scenario]:
        """Generate all 500+ scenarios."""
        logger.info("Starting synthetic scenario generation")

        self.generate_axiom_1_scenarios()
        self.generate_axiom_2_scenarios()
        self.generate_axiom_3_scenarios()
        self.generate_axiom_4_scenarios()
        self.generate_domain_auth_scenarios()
        self.generate_domain_rate_limiting_scenarios()
        self.generate_domain_data_validation_scenarios()
        self.generate_domain_access_control_scenarios()
        self.generate_domain_compliance_scenarios()
        self.generate_edge_case_scenarios()

        logger.info(f"Generated {len(self.scenarios)} scenarios")
        return self.scenarios

    # ========================================================================
    # Axiom 1: Immutability (40 scenarios)
    # ========================================================================

    def generate_axiom_1_scenarios(self):
        """Generate 40 Axiom 1 (Immutability) scenarios."""
        logger.info("Generating Axiom 1 scenarios...")

        # Scenario 1: Direct policy override attempt
        self._add_scenario(
            category=ScenarioCategory.AXIOM_1_IMMUTABILITY,
            scenario_id="A1_001",
            description="Policy attempts to override Axiom 1 enforcement",
            severity=SeverityLevel.CRITICAL,
            expected_outcome=ExpectedOutcome.AXIOM_VIOLATION,
            axiom=1,
            setup_fn=lambda: {"policy": {"action": "disable axiom enforcement"}},
            execute_fn=lambda setup: self.executor.execute_axiom_1_override(setup),
            verify_fn=lambda result: self.verifier.verify_axiom_violation(result),
        )

        # Scenario 2: Skip validation phase
        self._add_scenario(
            category=ScenarioCategory.AXIOM_1_IMMUTABILITY,
            scenario_id="A1_002",
            description="Policy attempts to skip validation phase",
            severity=SeverityLevel.CRITICAL,
            expected_outcome=ExpectedOutcome.AXIOM_VIOLATION,
            axiom=1,
            setup_fn=lambda: {"policy": {"action": "skip validation"}},
            execute_fn=lambda setup: self.executor.execute_axiom_1_override(setup),
            verify_fn=lambda result: self.verifier.verify_axiom_violation(result),
        )

        # Scenario 3: Remove constraint from loop
        self._add_scenario(
            category=ScenarioCategory.AXIOM_1_IMMUTABILITY,
            scenario_id="A1_003",
            description="Policy attempts to remove constraint from Loop",
            severity=SeverityLevel.CRITICAL,
            expected_outcome=ExpectedOutcome.AXIOM_VIOLATION,
            axiom=1,
            setup_fn=lambda: {"policy": {"action": "remove constraint from loop"}},
            execute_fn=lambda setup: self.executor.execute_axiom_1_override(setup),
            verify_fn=lambda result: self.verifier.verify_axiom_violation(result),
        )

        # Scenarios 4-40: Variations on immutability violations
        for i in range(4, 41):
            violation_types = [
                "disable axiom",
                "bypass enforcement",
                "override primitive",
                "modify axiom",
                "remove foundational rule",
                "disable verification",
            ]
            violation_type = violation_types[(i - 4) % len(violation_types)]

            self._add_scenario(
                category=ScenarioCategory.AXIOM_1_IMMUTABILITY,
                scenario_id=f"A1_{i:03d}",
                description=f"Attempt to {violation_type}",
                severity=SeverityLevel.CRITICAL,
                expected_outcome=ExpectedOutcome.AXIOM_VIOLATION,
                axiom=1,
                setup_fn=lambda vt=violation_type: {"policy": {"action": vt}},
                execute_fn=lambda setup: self.executor.execute_axiom_1_override(setup),
                verify_fn=lambda result: self.verifier.verify_axiom_violation(result),
            )

    # ========================================================================
    # Axiom 2: Determinism (40 scenarios)
    # ========================================================================

    def generate_axiom_2_scenarios(self):
        """Generate 40 Axiom 2 (Determinism) scenarios."""
        logger.info("Generating Axiom 2 scenarios...")

        # Scenario 1: Identical validation results
        self._add_scenario(
            category=ScenarioCategory.AXIOM_2_DETERMINISM,
            scenario_id="A2_001",
            description="Same policy validates identically twice",
            severity=SeverityLevel.HIGH,
            expected_outcome=ExpectedOutcome.PASS,
            axiom=2,
            setup_fn=lambda: {"policy": {"domain": "auth", "confidence": 0.85}},
            execute_fn=lambda setup: self.executor.execute_axiom_2_reproducibility(setup),
            verify_fn=lambda result: self.verifier.verify_reproducible_results(result),
        )

        # Scenario 2: Missing uncertainty bounds
        self._add_scenario(
            category=ScenarioCategory.AXIOM_2_DETERMINISM,
            scenario_id="A2_002",
            description="Validation missing uncertainty bounds",
            severity=SeverityLevel.CRITICAL,
            expected_outcome=ExpectedOutcome.DETERMINISM_VIOLATION,
            axiom=2,
            setup_fn=lambda: {"policy": {"confidence": 0.85}},  # No bounds
            execute_fn=lambda setup: self.executor.execute_axiom_2_bounds_check(setup),
            verify_fn=lambda result: self.verifier.verify_determinism_violation(result),
        )

        # Scenario 3: Non-deterministic outcome detection
        self._add_scenario(
            category=ScenarioCategory.AXIOM_2_DETERMINISM,
            scenario_id="A2_003",
            description="Non-deterministic outcome detected",
            severity=SeverityLevel.CRITICAL,
            expected_outcome=ExpectedOutcome.DETERMINISM_VIOLATION,
            axiom=2,
            setup_fn=lambda: {"policy": {"outcome_1": "ACCEPT", "outcome_2": "REJECT"}},
            execute_fn=lambda setup: self.executor.execute_axiom_2_non_determinism(setup),
            verify_fn=lambda result: self.verifier.verify_determinism_violation(result),
        )

        # Scenarios 4-40: Determinism edge cases
        for i in range(4, 41):
            confidence_values = [0.0, 0.25, 0.50, 0.75, 0.99, 1.0]
            confidence = confidence_values[(i - 4) % len(confidence_values)]

            self._add_scenario(
                category=ScenarioCategory.AXIOM_2_DETERMINISM,
                scenario_id=f"A2_{i:03d}",
                description=f"Determinism with confidence {confidence}",
                severity=SeverityLevel.MEDIUM,
                expected_outcome=ExpectedOutcome.PASS,
                axiom=2,
                setup_fn=lambda conf=confidence: {
                    "policy": {
                        "confidence": conf,
                        "bounds": {"lower": conf - 0.05, "upper": conf + 0.05},
                    }
                },
                execute_fn=lambda setup: self.executor.execute_axiom_2_reproducibility(setup),
                verify_fn=lambda result: self.verifier.verify_reproducible_results(result),
            )

    # ========================================================================
    # Axiom 3: Enforcement (40 scenarios)
    # ========================================================================

    def generate_axiom_3_scenarios(self):
        """Generate 40 Axiom 3 (Enforcement) scenarios."""
        logger.info("Generating Axiom 3 scenarios...")

        # Scenario 1: Constraint not mechanically enforced
        self._add_scenario(
            category=ScenarioCategory.AXIOM_3_ENFORCEMENT,
            scenario_id="A3_001",
            description="Constraint not mechanically enforced",
            severity=SeverityLevel.CRITICAL,
            expected_outcome=ExpectedOutcome.ENFORCEMENT_VIOLATION,
            axiom=3,
            setup_fn=lambda: {"constraint": {"enforced": False}},
            execute_fn=lambda setup: self.executor.execute_axiom_3_enforcement_check(setup),
            verify_fn=lambda result: self.verifier.verify_enforcement_violation(result),
        )

        # Scenario 2: Soft enforcement (documentation only)
        self._add_scenario(
            category=ScenarioCategory.AXIOM_3_ENFORCEMENT,
            scenario_id="A3_002",
            description="Constraint only documented, not enforced",
            severity=SeverityLevel.CRITICAL,
            expected_outcome=ExpectedOutcome.ENFORCEMENT_VIOLATION,
            axiom=3,
            setup_fn=lambda: {"constraint": {"enforcement": "documentation"}},
            execute_fn=lambda setup: self.executor.execute_axiom_3_soft_enforcement(setup),
            verify_fn=lambda result: self.verifier.verify_enforcement_violation(result),
        )

        # Scenario 3: Pre-commit hook enforcement
        self._add_scenario(
            category=ScenarioCategory.AXIOM_3_ENFORCEMENT,
            scenario_id="A3_003",
            description="Constraint enforced by pre-commit hook",
            severity=SeverityLevel.HIGH,
            expected_outcome=ExpectedOutcome.PASS,
            axiom=3,
            setup_fn=lambda: {"constraint": {"enforcement": "pre_commit_hook", "enforced": True}},
            execute_fn=lambda setup: self.executor.execute_axiom_3_enforcement_check(setup),
            verify_fn=lambda result: self.verifier.verify_enforcement_active(result),
        )

        # Scenarios 4-40: Various enforcement mechanisms
        for i in range(4, 41):
            enforcement_types = [
                "tier_1_hook",
                "tier_2_ci_pipeline",
                "tier_3_runtime_gate",
                "linter",
                "test_suite",
            ]
            enforcement = enforcement_types[(i - 4) % len(enforcement_types)]

            self._add_scenario(
                category=ScenarioCategory.AXIOM_3_ENFORCEMENT,
                scenario_id=f"A3_{i:03d}",
                description=f"Constraint enforced via {enforcement}",
                severity=SeverityLevel.HIGH,
                expected_outcome=ExpectedOutcome.PASS,
                axiom=3,
                setup_fn=lambda enf=enforcement: {"constraint": {"enforcement": enf, "enforced": True}},
                execute_fn=lambda setup: self.executor.execute_axiom_3_enforcement_check(setup),
                verify_fn=lambda result: self.verifier.verify_enforcement_active(result),
            )

    # ========================================================================
    # Axiom 4: Resilience (40 scenarios)
    # ========================================================================

    def generate_axiom_4_scenarios(self):
        """Generate 40 Axiom 4 (Resilience) scenarios."""
        logger.info("Generating Axiom 4 scenarios...")

        # Scenario 1: Adaptation missing version
        self._add_scenario(
            category=ScenarioCategory.AXIOM_4_RESILIENCE,
            scenario_id="A4_001",
            description="Adaptation missing version tracking",
            severity=SeverityLevel.CRITICAL,
            expected_outcome=ExpectedOutcome.RESILIENCE_VIOLATION,
            axiom=4,
            setup_fn=lambda: {"adaptation": {"version": None}},
            execute_fn=lambda setup: self.executor.execute_axiom_4_versioning(setup),
            verify_fn=lambda result: self.verifier.verify_resilience_violation(result),
        )

        # Scenario 2: Adaptation missing audit trail
        self._add_scenario(
            category=ScenarioCategory.AXIOM_4_RESILIENCE,
            scenario_id="A4_002",
            description="Adaptation missing audit trail",
            severity=SeverityLevel.CRITICAL,
            expected_outcome=ExpectedOutcome.RESILIENCE_VIOLATION,
            axiom=4,
            setup_fn=lambda: {"adaptation": {"audit": None}},
            execute_fn=lambda setup: self.executor.execute_axiom_4_audit(setup),
            verify_fn=lambda result: self.verifier.verify_resilience_violation(result),
        )

        # Scenario 3: Adaptation cannot rollback
        self._add_scenario(
            category=ScenarioCategory.AXIOM_4_RESILIENCE,
            scenario_id="A4_003",
            description="Adaptation not reversible",
            severity=SeverityLevel.CRITICAL,
            expected_outcome=ExpectedOutcome.RESILIENCE_VIOLATION,
            axiom=4,
            setup_fn=lambda: {"adaptation": {"rollback_path": None}},
            execute_fn=lambda setup: self.executor.execute_axiom_4_reversibility(setup),
            verify_fn=lambda result: self.verifier.verify_resilience_violation(result),
        )

        # Scenarios 4-40: Bounded adaptation scenarios
        for i in range(4, 41):
            adaptations = [
                "tighten_confidence_gate",
                "adjust_homeostasis_target",
                "modify_escalation_rule",
                "update_constraint",
                "bump_version",
            ]
            adaptation = adaptations[(i - 4) % len(adaptations)]

            self._add_scenario(
                category=ScenarioCategory.AXIOM_4_RESILIENCE,
                scenario_id=f"A4_{i:03d}",
                description=f"Bounded adaptation: {adaptation}",
                severity=SeverityLevel.HIGH,
                expected_outcome=ExpectedOutcome.PASS,
                axiom=4,
                setup_fn=lambda ad=adaptation: {
                    "adaptation": {
                        "type": ad,
                        "version": "v1.1",
                        "audit": {"who": "system", "what": ad, "why": "test", "when": "now"},
                        "rollback_path": "v1.0",
                    }
                },
                execute_fn=lambda setup: self.executor.execute_axiom_4_bounded_adaptation(setup),
                verify_fn=lambda result: self.verifier.verify_resilience_success(result),
            )

    # ========================================================================
    # Domain: Auth (50 scenarios)
    # ========================================================================

    def generate_domain_auth_scenarios(self):
        """Generate 50 authentication domain scenarios."""
        logger.info("Generating Domain: Auth scenarios...")

        confidence_values = [0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.0]

        for i in range(1, 51):
            confidence = confidence_values[(i - 1) % len(confidence_values)]
            expected = ExpectedOutcome.PASS if confidence >= 0.75 else ExpectedOutcome.REJECTED

            self._add_scenario(
                category=ScenarioCategory.DOMAIN_AUTH,
                scenario_id=f"AUTH_{i:03d}",
                description=f"Auth domain: confidence > 0.75 with value {confidence}",
                severity=SeverityLevel.HIGH,
                expected_outcome=expected,
                domain="auth",
                setup_fn=lambda conf=confidence: {
                    "policy": {
                        "domain": "auth",
                        "rule": f"confidence > 0.75",
                        "confidence": conf,
                    }
                },
                execute_fn=lambda setup: self.executor.execute_domain_policy(setup),
                verify_fn=lambda result: self.verifier.verify_domain_policy(result),
            )

    # ========================================================================
    # Domain: Rate Limiting (50 scenarios)
    # ========================================================================

    def generate_domain_rate_limiting_scenarios(self):
        """Generate 50 rate limiting domain scenarios."""
        logger.info("Generating Domain: Rate Limiting scenarios...")

        limits = [100, 500, 1000, 5000, 10000]

        for i in range(1, 51):
            limit = limits[(i - 1) % len(limits)]

            self._add_scenario(
                category=ScenarioCategory.DOMAIN_RATE_LIMITING,
                scenario_id=f"RATE_{i:03d}",
                description=f"Rate limiting: {limit} requests/hour",
                severity=SeverityLevel.HIGH,
                expected_outcome=ExpectedOutcome.PASS,
                domain="rate_limiting",
                setup_fn=lambda lim=limit: {
                    "policy": {
                        "domain": "rate_limiting",
                        "rule": f"requests_per_hour <= {lim}",
                        "confidence": 0.85,
                    }
                },
                execute_fn=lambda setup: self.executor.execute_domain_policy(setup),
                verify_fn=lambda result: self.verifier.verify_domain_policy(result),
            )

    # ========================================================================
    # Domain: Data Validation (50 scenarios)
    # ========================================================================

    def generate_domain_data_validation_scenarios(self):
        """Generate 50 data validation domain scenarios."""
        logger.info("Generating Domain: Data Validation scenarios...")

        types = ["string", "integer", "float", "boolean", "list"]

        for i in range(1, 51):
            data_type = types[(i - 1) % len(types)]

            self._add_scenario(
                category=ScenarioCategory.DOMAIN_DATA_VALIDATION,
                scenario_id=f"DATA_{i:03d}",
                description=f"Data validation: type {data_type}",
                severity=SeverityLevel.MEDIUM,
                expected_outcome=ExpectedOutcome.PASS,
                domain="data_validation",
                setup_fn=lambda dt=data_type: {
                    "policy": {
                        "domain": "data_validation",
                        "rule": f"type == {dt}",
                        "confidence": 0.85,
                    }
                },
                execute_fn=lambda setup: self.executor.execute_domain_policy(setup),
                verify_fn=lambda result: self.verifier.verify_domain_policy(result),
            )

    # ========================================================================
    # Domain: Access Control (50 scenarios)
    # ========================================================================

    def generate_domain_access_control_scenarios(self):
        """Generate 50 access control domain scenarios."""
        logger.info("Generating Domain: Access Control scenarios...")

        roles = ["admin", "user", "viewer", "editor", "guest"]

        for i in range(1, 51):
            role = roles[(i - 1) % len(roles)]

            self._add_scenario(
                category=ScenarioCategory.DOMAIN_ACCESS_CONTROL,
                scenario_id=f"AC_{i:03d}",
                description=f"Access control: role {role}",
                severity=SeverityLevel.HIGH,
                expected_outcome=ExpectedOutcome.PASS,
                domain="access_control",
                setup_fn=lambda r=role: {
                    "policy": {
                        "domain": "access_control",
                        "rule": f"role == {r}",
                        "confidence": 0.85,
                    }
                },
                execute_fn=lambda setup: self.executor.execute_domain_policy(setup),
                verify_fn=lambda result: self.verifier.verify_domain_policy(result),
            )

    # ========================================================================
    # Domain: Compliance & Governance (50 scenarios)
    # ========================================================================

    def generate_domain_compliance_scenarios(self):
        """Generate 50 compliance & governance domain scenarios."""
        logger.info("Generating Domain: Compliance scenarios...")

        requirements = [
            "audit_trail_required",
            "compliance_check_pass",
            "data_retention_30_days",
            "encryption_enabled",
            "access_log_enabled",
        ]

        for i in range(1, 51):
            req = requirements[(i - 1) % len(requirements)]

            self._add_scenario(
                category=ScenarioCategory.DOMAIN_COMPLIANCE,
                scenario_id=f"COMP_{i:03d}",
                description=f"Compliance: {req}",
                severity=SeverityLevel.MEDIUM,
                expected_outcome=ExpectedOutcome.PASS,
                domain="compliance",
                setup_fn=lambda r=req: {
                    "policy": {
                        "domain": "compliance",
                        "rule": r,
                        "confidence": 0.85,
                    }
                },
                execute_fn=lambda setup: self.executor.execute_domain_policy(setup),
                verify_fn=lambda result: self.verifier.verify_domain_policy(result),
            )

    # ========================================================================
    # Edge Cases (40 scenarios)
    # ========================================================================

    def generate_edge_case_scenarios(self):
        """Generate 90+ edge case scenarios."""
        logger.info("Generating Edge Case scenarios...")

        edge_cases = [
            ("empty_policy", {"policy": {}}),
            ("zero_confidence", {"policy": {"confidence": 0.0}}),
            ("100_percent_confidence", {"policy": {"confidence": 1.0}}),
            ("null_domain", {"policy": {"domain": None}}),
            ("empty_rule", {"policy": {"rule": ""}}),
            ("very_long_rule", {"policy": {"rule": "x" * 10000}}),
            ("special_characters", {"policy": {"rule": "!@#$%^&*()"}}),
            ("unicode_characters", {"policy": {"rule": "你好世界"}}),
            ("negative_confidence", {"policy": {"confidence": -0.5}}),
            ("confidence_over_100", {"policy": {"confidence": 1.5}}),
            ("null_policy", {"policy": None}),
            ("deeply_nested", {"policy": {"a": {"b": {"c": {"d": "value"}}}}}),
            ("circular_reference_like", {"policy": {"self": "policy"}}),
            ("mixed_types", {"policy": {"str": "text", "int": 42, "float": 3.14}}),
            ("large_list", {"policy": {"items": list(range(1000))}}),
        ]

        for i in range(1, 91):
            case_name, setup = edge_cases[(i - 1) % len(edge_cases)]

            self._add_scenario(
                category=ScenarioCategory.EDGE_CASE,
                scenario_id=f"EDGE_{i:03d}",
                description=f"Edge case: {case_name}",
                severity=SeverityLevel.MEDIUM,
                expected_outcome=ExpectedOutcome.PASS,
                setup_fn=lambda s=setup: s,
                execute_fn=lambda setup: self.executor.execute_edge_case(setup),
                verify_fn=lambda result: self.verifier.verify_edge_case(result),
            )

    # ========================================================================
    # Helper Methods: Adding Scenarios
    # ========================================================================

    def _add_scenario(
        self,
        category: ScenarioCategory,
        scenario_id: str,
        description: str,
        severity: SeverityLevel,
        expected_outcome: ExpectedOutcome,
        setup_fn: Callable,
        execute_fn: Callable,
        verify_fn: Callable,
        axiom: Optional[int] = None,
        domain: Optional[str] = None,
        tags: Optional[list[str]] = None,
    ):
        """Add scenario to collection."""
        scenario = Scenario(
            scenario_id=scenario_id,
            category=category,
            description=description,
            severity=severity,
            expected_outcome=expected_outcome,
            setup_fn=setup_fn,
            execute_fn=execute_fn,
            verify_fn=verify_fn,
            axiom_related=axiom,
            domain=domain,
            tags=tags or [],
        )
        self.scenarios.append(scenario)
        self.scenario_count += 1

    # ========================================================================
    # Scenario Execution Integration
    #
    # Note: The actual execute_fn and verify_fn are created as lambda expressions
    # in the _add_scenario calls above. They wrap calls to:
    # - self.executor (ScenarioExecutor instance)
    # - self.verifier (ScenarioVerifier instance)
    #
    # These integrations wire each scenario to actual ENCT code:
    # - Axiom scenarios call axiom validators
    # - Domain scenarios call policy validation logic
    # - Edge case scenarios test graceful degradation
    # ========================================================================
