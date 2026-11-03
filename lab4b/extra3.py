# Lab 4B - Extra E3 - do we need classes at all?
#
# E3.1  Three rules in BOTH styles (class with apply() and plain functions):
#       10 % off; 20 000 sum off above 200 000; free delivery above 150 000.
#       The third rule does NOT fit apply(total) -> int: "free delivery" is
#       not an amount taken off the total, it is a different fact about the
#       order (delivery charge = 0). Stretching a number to mean it would
#       lie to every caller. What that tells you: apply() is a narrow,
#       single-purpose interface - worth having only when every rule really
#       only moves money off the total.
#
# E3.2  "Never below 0" lives in Cart, in one place: it is an invariant of
#       the total, not of the rules - putting it into N rules means N
#       chances to forget it; one line in Cart covers every future rule.
#
# E3.3  Next week's name + validity period favour the CLASS style - see the
#       review_comment string below (written as a short code-review note).
#
# Done when: both styles pass the same tests, and the comment says when
#            functions are enough and when a class is justified.

import pytest


# ---------- class style ----------
class TenPercentOff:
    def apply(self, total: int) -> int:
        return total * 90 // 100                 # -10 %


class Minus20kAbove200k:
    def apply(self, total: int) -> int:
        return total - 20_000 if total > 200_000 else total


class FreeDelivery:
    """Does NOT fit apply(total): it is about delivery, not the total."""

    def __init__(self) -> None:
        self.waives_delivery_fee = True


# ---------- function style ----------
def ten_percent_off(total: int) -> int:
    return total * 90 // 100


def minus_20k_above_200k(total: int) -> int:
    return total - 20_000 if total > 200_000 else total


def apply_rules(total: int, rules: list) -> int:
    """Same code drives both styles: prefer .apply, fall back to the function.
    A rule that neither has .apply nor is callable (e.g. FreeDelivery, which
    does not fit the money-off interface) is simply not applied here."""
    result = total
    for rule in rules:
        step = rule.apply if hasattr(rule, "apply") else (rule if callable(rule) else None)
        if step is not None:
            result = step(result)
    return max(result, 0)                        # E3.2 - Cart-level invariant


# E3.3 - the code-review comment:
review_comment = (
    "Functions are enough while a rule stays one pure expression of the "
    "total (the two styles here pass identical tests). The moment a rule "
    "needs data or behaviour of its own - a name for the receipt like "
    "'Student discount -10 %', a validity date range, logging - classes "
    "are justified: fields hold the data and __init__ can validate it, "
    "which a bare function cannot carry without turning into globals."
)


# --------------------------- tests ---------------------------

def test_class_style_and_function_style_agree():
    for total in (10_000, 250_000, 500_000):
        assert (
            TenPercentOff().apply(total) == ten_percent_off(total)
            and Minus20kAbove200k().apply(total) == minus_20k_above_200k(total)
        )


def test_rules_compose_in_order():
    assert apply_rules(500_000, [TenPercentOff(), Minus20kAbove200k()]) == 430_000
    assert apply_rules(500_000, [Minus20kAbove200k(), TenPercentOff()]) == 432_000


def test_total_never_goes_below_zero_in_cart():
    def ruinous_rule(total: int) -> int:
        return total - 1_000_000

    assert apply_rules(500_000, [ruinous_rule]) == 0


def test_free_delivery_rule_does_not_fit_the_interface():
    # The honest answer to "does the third rule fit apply(total)?": no.
    assert not hasattr(FreeDelivery, "apply")
    assert FreeDelivery().waives_delivery_fee is True
    # and the pipeline simply ignores what is not a money-off rule:
    assert apply_rules(50_000, [FreeDelivery()]) == 50_000
