"""
ENCT Primitives: Core building blocks

4 immutable primitive types:
1. Fact - Observable state about the world
2. Policy - Guidance rules for the agent
3. Constraint - Normative boundaries for behavior
4. Event - Timestamped occurrence
"""

from dataclasses import dataclass, field
from typing import Any, Optional
from datetime import datetime
from enum import Enum
import hashlib


class PrimitiveType(Enum):
    """Types of ENCT primitives."""
    FACT = "fact"
    POLICY = "policy"
    CONSTRAINT = "constraint"
    EVENT = "event"


@dataclass(frozen=True)  # Immutable
class Fact:
    """
    Fact: Observable state about the world.

    Immutable: once created, cannot change.
    Modifications create new Fact_v2, Fact_v3, etc.
    """
    fact_id: str
    version: int = 1
    content: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    prior_version_id: Optional[str] = None  # Reference to Fact_v1
    checksum: str = field(default="")

    def __post_init__(self):
        # Compute checksum for immutability verification
        content_str = str(sorted(self.content.items()))
        _checksum = hashlib.sha256(content_str.encode()).hexdigest()
        object.__setattr__(self, 'checksum', _checksum)

    def evolve(self, new_content: dict[str, Any]) -> 'Fact':
        """
        Create next version of this Fact.
        Original remains immutable; returns new instance.
        """
        return Fact(
            fact_id=self.fact_id,
            version=self.version + 1,
            content=new_content,
            timestamp=datetime.utcnow().isoformat(),
            prior_version_id=f"{self.fact_id}_v{self.version}",
        )

    @property
    def full_id(self) -> str:
        """Unique identifier including version."""
        return f"{self.fact_id}_v{self.version}"


@dataclass(frozen=True)  # Immutable
class Policy:
    """
    Policy: Guidance rule for agent behavior.

    Immutable: once created, cannot change.
    Modifications create new Policy_v2, Policy_v3, etc.
    """
    policy_id: str
    version: int = 1
    domain: str = ""
    rule: str = ""
    confidence: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    prior_version_id: Optional[str] = None
    checksum: str = field(default="")

    def __post_init__(self):
        content_str = f"{self.domain}:{self.rule}:{self.confidence}"
        _checksum = hashlib.sha256(content_str.encode()).hexdigest()
        object.__setattr__(self, 'checksum', _checksum)

    def evolve(self, new_rule: str, new_confidence: float) -> 'Policy':
        """Create next version of this Policy."""
        return Policy(
            policy_id=self.policy_id,
            version=self.version + 1,
            domain=self.domain,
            rule=new_rule,
            confidence=new_confidence,
            timestamp=datetime.utcnow().isoformat(),
            prior_version_id=f"{self.policy_id}_v{self.version}",
        )

    @property
    def full_id(self) -> str:
        """Unique identifier including version."""
        return f"{self.policy_id}_v{self.version}"


@dataclass(frozen=True)  # Immutable
class Constraint:
    """
    Constraint: Normative boundary for behavior.

    Immutable: once created, cannot change.
    Modifications create new Constraint_v2, etc.
    """
    constraint_id: str
    version: int = 1
    name: str = ""
    expression: str = ""
    enforced: bool = True
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    prior_version_id: Optional[str] = None
    checksum: str = field(default="")

    def __post_init__(self):
        content_str = f"{self.name}:{self.expression}:{self.enforced}"
        _checksum = hashlib.sha256(content_str.encode()).hexdigest()
        object.__setattr__(self, 'checksum', _checksum)

    def evolve(self, new_expression: str) -> 'Constraint':
        """Create next version of this Constraint."""
        return Constraint(
            constraint_id=self.constraint_id,
            version=self.version + 1,
            name=self.name,
            expression=new_expression,
            enforced=self.enforced,
            timestamp=datetime.utcnow().isoformat(),
            prior_version_id=f"{self.constraint_id}_v{self.version}",
        )

    @property
    def full_id(self) -> str:
        """Unique identifier including version."""
        return f"{self.constraint_id}_v{self.version}"


@dataclass(frozen=True)  # Immutable
class Event:
    """
    Event: Timestamped occurrence in the system.

    Immutable: once created, cannot change.
    Events are append-only (no evolve method).
    """
    event_id: str
    event_type: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    source: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    checksum: str = field(default="")

    def __post_init__(self):
        content_str = f"{self.event_type}:{self.source}:{str(self.payload)}"
        _checksum = hashlib.sha256(content_str.encode()).hexdigest()
        object.__setattr__(self, 'checksum', _checksum)

    @property
    def full_id(self) -> str:
        """Unique identifier."""
        return f"{self.event_id}_{self.timestamp}"
