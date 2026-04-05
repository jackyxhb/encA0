"""
ENCT Ledger Writer

Persistent storage abstraction for POLICY-LEDGER and FAILURE-LEDGER.
All Loop state changes written synchronously to ledgers (immutable audit trail).
"""

import logging
import json
from typing import Any, Optional
from datetime import datetime
from pathlib import Path
from enum import Enum

logger = logging.getLogger(__name__)


class LedgerType(Enum):
    """Types of ledgers."""
    POLICY = "policy"
    FAILURE = "failure"


class PolicyLedgerEntryStatus(Enum):
    """Status of policy ledger entries."""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    VALIDATED = "validated"
    ACTIVE = "active"
    ROLLED_BACK = "rolled_back"
    REJECTED = "rejected"


class FailureLedgerSeverity(Enum):
    """Severity levels for failure ledger entries."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class LedgerWriter:
    """
    Abstraction for writing to POLICY-LEDGER and FAILURE-LEDGER.

    Guarantees:
    - Synchronous writes (write completes before function returns)
    - Atomic entries (either fully written or not written)
    - Immutable once written (append-only)
    - Timestamped (all entries have creation timestamp)
    """

    def __init__(self, ledger_root: Path = Path("/tmp/enct-ledgers")):
        """Initialize ledger writer."""
        self.ledger_root = ledger_root
        self.ledger_root.mkdir(parents=True, exist_ok=True)

        self.policy_ledger_path = self.ledger_root / "POLICY-LEDGER.jsonl"
        self.failure_ledger_path = self.ledger_root / "FAILURE-LEDGER.jsonl"

    def write_policy_entry(
        self,
        policy_id: str,
        policy_content: dict[str, Any],
        status: PolicyLedgerEntryStatus,
        validation_result: Optional[dict[str, Any]] = None,
        author: str = "system",
        notes: str = "",
    ) -> str:
        """
        Write policy ledger entry.

        Returns:
            Entry ID (for linking in Loop state)

        Raises:
            IOError if write fails (fail-hard)
        """
        entry_id = f"policy_{policy_id}_{datetime.utcnow().isoformat()}"

        entry = {
            "entry_id": entry_id,
            "policy_id": policy_id,
            "timestamp": datetime.utcnow().isoformat(),
            "status": status.value,
            "policy_content": policy_content,
            "validation_result": validation_result,
            "author": author,
            "notes": notes,
        }

        try:
            with open(self.policy_ledger_path, "a") as f:
                f.write(json.dumps(entry) + "\n")
            logger.info(f"Policy ledger entry written: {entry_id}")
            return entry_id
        except IOError as e:
            logger.critical(f"Failed to write policy ledger: {e}")
            raise

    def write_failure_entry(
        self,
        cycle_id: str,
        failure_type: str,
        severity: FailureLedgerSeverity,
        description: str,
        phase: Optional[str] = None,
        context: Optional[dict[str, Any]] = None,
        root_cause: Optional[str] = None,
    ) -> str:
        """
        Write failure ledger entry.

        Returns:
            Entry ID (for linking in Loop state)

        Raises:
            IOError if write fails (fail-hard)
        """
        entry_id = f"failure_{cycle_id}_{datetime.utcnow().isoformat()}"

        entry = {
            "entry_id": entry_id,
            "cycle_id": cycle_id,
            "timestamp": datetime.utcnow().isoformat(),
            "failure_type": failure_type,
            "severity": severity.value,
            "description": description,
            "phase": phase,
            "context": context or {},
            "root_cause": root_cause,
        }

        try:
            with open(self.failure_ledger_path, "a") as f:
                f.write(json.dumps(entry) + "\n")
            logger.warning(f"Failure ledger entry written: {entry_id} (severity={severity.value})")
            return entry_id
        except IOError as e:
            logger.critical(f"Failed to write failure ledger: {e}")
            raise

    def write_axiom_violation_entry(
        self,
        cycle_id: str,
        axiom_number: int,
        violation_type: str,
        message: str,
        phase: str,
        context: Optional[dict[str, Any]] = None,
    ) -> str:
        """
        Write failure ledger entry for axiom violation.

        Axiom violations are always CRITICAL severity.

        Returns:
            Entry ID (for linking in Loop state)
        """
        return self.write_failure_entry(
            cycle_id=cycle_id,
            failure_type=f"axiom_{axiom_number}_violation",
            severity=FailureLedgerSeverity.CRITICAL,
            description=f"Axiom {axiom_number} violation ({violation_type}): {message}",
            phase=phase,
            context=context or {},
            root_cause=violation_type,
        )

    def write_phase_completion_entry(
        self,
        cycle_id: str,
        phase: str,
        phase_output: dict[str, Any],
    ) -> str:
        """
        Write policy ledger entry when a Loop phase completes successfully.

        Records phase output for audit trail.
        """
        entry_id = f"phase_{cycle_id}_{phase}_{datetime.utcnow().isoformat()}"

        entry = {
            "entry_id": entry_id,
            "cycle_id": cycle_id,
            "timestamp": datetime.utcnow().isoformat(),
            "type": "phase_completion",
            "phase": phase,
            "output": phase_output,
        }

        try:
            with open(self.policy_ledger_path, "a") as f:
                f.write(json.dumps(entry) + "\n")
            logger.info(f"Phase completion logged: {entry_id}")
            return entry_id
        except IOError as e:
            logger.critical(f"Failed to write phase completion: {e}")
            raise

    def read_policy_history(self, policy_id: str) -> list[dict[str, Any]]:
        """Read all entries for a policy from ledger."""
        entries = []
        try:
            with open(self.policy_ledger_path, "r") as f:
                for line in f:
                    if not line.strip():
                        continue
                    entry = json.loads(line)
                    if entry.get("policy_id") == policy_id:
                        entries.append(entry)
        except FileNotFoundError:
            pass
        return entries

    def read_cycle_history(self, cycle_id: str) -> dict[str, list[dict[str, Any]]]:
        """Read all entries for a cycle from both ledgers."""
        policy_entries = []
        failure_entries = []

        try:
            with open(self.policy_ledger_path, "r") as f:
                for line in f:
                    if not line.strip():
                        continue
                    entry = json.loads(line)
                    if entry.get("cycle_id") == cycle_id:
                        policy_entries.append(entry)
        except FileNotFoundError:
            pass

        try:
            with open(self.failure_ledger_path, "r") as f:
                for line in f:
                    if not line.strip():
                        continue
                    entry = json.loads(line)
                    if entry.get("cycle_id") == cycle_id:
                        failure_entries.append(entry)
        except FileNotFoundError:
            pass

        return {
            "policy_entries": policy_entries,
            "failure_entries": failure_entries,
        }
