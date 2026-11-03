# Lab 4B - Task 4 - the audit log that could be erased
#
# 4.1  is-a test: NO, an AuditLog is not a list - an audit log *keeps* a list
#      of entries. "AuditLog is-a list" would promise every list operation,
#      and these break the append-only rule: clear(), sort(), pop()
#      (also remove(), reverse(), and the item assignment log[3] = ...).
#
# 4.2  Rewritten with composition: the log HAS a private list; the public
#      surface is exactly record(), len(), iteration, indexing and last(n).
#
# 4.3  One entry is a NamedTuple: immutable, so a recorded entry cannot be
#      edited after the fact (a frozen dataclass would work too; NamedTuple
#      is the lightest immutable record).
#
# 4.4  "Keep the inheritance, just override clear() and pop()" is worse:
#      dir(list) has 11 PUBLIC methods - append, clear, copy, count, extend,
#      index, insert, pop, remove, reverse, sort - plus ~40 dunder paths
#      such as __setitem__/__delitem__ that any mutation can sneak through.
#      You would have to hunt all of them forever and still trust an
#      interface you refuse to support; composition shows the reviewer
#      exactly the four safe operations and hides everything else.
#
# Done when: log.clear(), log.sort() and log[0] = ... are impossible, while
#            iteration and len() still work.

from typing import NamedTuple

import pytest


class AuditEntry(NamedTuple):
    """4.3 - immutable audit record."""
    user: str
    action: str


class AuditLog:
    """Append-only audit log - it HAS a list, it is not a list (4.2)."""

    def __init__(self) -> None:
        self._entries: list[AuditEntry] = []

    def record(self, user: str, action: str) -> None:
        self._entries.append(AuditEntry(user, action))

    def __len__(self) -> int:
        return len(self._entries)

    def __iter__(self):
        # Iterate a SNAPSHOT: a reader can never observe a mid-iteration write.
        return iter(tuple(self._entries))

    def __getitem__(self, index: int) -> AuditEntry:
        return self._entries[index]

    def last(self, n: int = 1) -> list[AuditEntry]:
        """The final n entries, oldest first."""
        return list(self._entries[-n:])


# --------------------------- tests ---------------------------

def _log_with_two_entries() -> AuditLog:
    log = AuditLog()
    log.record("admin", "approve_loan#77")
    log.record("controller", "close_day")
    return log


def test_clear_is_impossible():
    with pytest.raises(AttributeError):
        _log_with_two_entries().clear()


def test_sort_is_impossible():
    with pytest.raises(AttributeError):
        _log_with_two_entries().sort()


def test_item_assignment_is_impossible():
    with pytest.raises(TypeError):
        _log_with_two_entries()[0] = AuditEntry("hacker", "erase")


def test_len_and_iteration_still_work():
    log = _log_with_two_entries()
    assert len(log) == 2
    assert [entry.action for entry in log] == ["approve_loan#77", "close_day"]


def test_last_n_returns_the_final_entries():
    log = _log_with_two_entries()
    assert log.last(2) == [
        AuditEntry("admin", "approve_loan#77"),
        AuditEntry("controller", "close_day"),
    ]


def test_recorded_entry_cannot_be_edited():
    entry = _log_with_two_entries()[0]
    with pytest.raises(AttributeError):
        entry.user = "someone else"
