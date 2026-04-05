"""
ENCT Loop Module

Exports Loop engine, state definitions, and ledger writer.

Public API:
- FivePhaseLoop: Main Loop orchestration engine
- LoopCycleState: Complete state of a Loop cycle
- LedgerWriter: Persistent storage abstraction
- LoopPhase, LoopStatus: Enumerations
"""

from .five_phase_loop import FivePhaseLoop
from .loop_states import (
    LoopPhase,
    LoopStatus,
    LoopCycleState,
    SensePhaseOutput,
    ValidatePhaseOutput,
    ExecutePhaseOutput,
    AssessPhaseOutput,
    ReEnactPhaseOutput,
)
from .ledger_writer import (
    LedgerWriter,
    LedgerType,
    PolicyLedgerEntryStatus,
    FailureLedgerSeverity,
)

__all__ = [
    # Core engine
    "FivePhaseLoop",
    # State definitions
    "LoopPhase",
    "LoopStatus",
    "LoopCycleState",
    "SensePhaseOutput",
    "ValidatePhaseOutput",
    "ExecutePhaseOutput",
    "AssessPhaseOutput",
    "ReEnactPhaseOutput",
    # Ledger abstraction
    "LedgerWriter",
    "LedgerType",
    "PolicyLedgerEntryStatus",
    "FailureLedgerSeverity",
]
