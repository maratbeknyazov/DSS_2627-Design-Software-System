# Lab 4B - Extra E1 - headers that came back in capitals
#
# E1.1  RAN the original dict subclass (test below). Three ways of adding a
#       key do NOT go through the overridden __setitem__:
#       the CONSTRUCTOR ({"Accept": ...}), update() and setdefault(). The
#       original snippet therefore ends with BOTH 'Content-Type' and
#       'content-type' keys, and the server rejects the request.
#
# E1.2  That is the fragile base class problem: dict is C-implemented and
#       the subclass silently depended on internal behaviour dict never
#       promised to call __setitem__. collections.UserDict is written as a
#       Python layer that routes EVERY write through the same __setitem__:
#       the constructor, update() and setdefault() all follow the rule now
#       (all four entry points are tested).
#
# E1.3  Case-insensitive READING needs __getitem__ and __contains__ (and get(),
#       which is overridden too: in this Python version UserDict.get does not
#       route through self[key]).
#
# Done when: there is never more than one key per header name, whichever
#            method adds it.

from collections import UserDict

import pytest


# ---- the original fragile subclass (E1.1 evidence) ----
class HeadersBroken(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key.lower(), value)


# ---- the fixed version: UserDict routes everything through us ----
class Headers(UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(key.lower(), value)

    def __getitem__(self, key):
        return super().__getitem__(key.lower())

    def __contains__(self, key):
        return super().__contains__(key.lower())

    def get(self, key, default=None):
        return super().get(key.lower(), default)


# --------------------------- tests ---------------------------

def test_broken_version_lets_duplicate_capitalisation_through():
    h = HeadersBroken({"Accept": "application/json"})          # bypasses
    h["Content-Type"] = "text/plain"                           # goes through
    h.update({"Content-Type": "application/json"})             # bypasses
    h.setdefault("X-Request-Id", "42")                         # bypasses
    # two spellings of one header now coexist -> server rejects:
    assert "Content-Type" in h and "content-type" in h


def test_fixed_all_entry_points_follow_the_lower_case_rule():
    h = Headers({"Accept": "application/json"})
    h["Content-Type"] = "text/plain"
    h.update({"X-Custom": "1"})
    h.setdefault("X-Request-Id", "42")
    assert dict(h) == {
        "accept": "application/json",
        "content-type": "text/plain",
        "x-custom": "1",
        "x-request-id": "42",
    }


def test_never_more_than_one_key_per_header_name():
    h = Headers()
    h["Content-Type"] = "a"
    h.update({"Content-TYPE": "b"})
    h.setdefault("CONTENT-TYPE", "c")
    spellings = [k for k in h if k.lower() == "content-type"]
    assert spellings == ["content-type"]       # exactly one, always lower-case
    # setdefault() only sets when the header is MISSING, so "b" stays:
    assert h["Content-Type"] == "b"


def test_reading_is_case_insensitive():
    h = Headers({"Content-Type": "application/json"})
    assert h["CONTENT-TYPE"] == "application/json"
    assert h["content-type"] == "application/json"
    assert "CONTENT-TYPE" in h
    assert h.get("CONTENT-TYPE", "missing") == "application/json"
