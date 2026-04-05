"""
ENCT Primitives Module

Exports immutable primitive types: Fact, Policy, Constraint, Event.
"""

from .primitive_types import (
    PrimitiveType,
    Fact,
    Policy,
    Constraint,
    Event,
)

__all__ = [
    "PrimitiveType",
    "Fact",
    "Policy",
    "Constraint",
    "Event",
]
