# Lab 4B - Task 7 - dollars added to sums
#
# 7.1  Money is a frozen value object: amount in MINOR units (tiyin / cents),
#      currency as a 3-letter code; objects never change. NOT
#      @dataclass(order=True): the generated < would compare bare amounts -
#      Money(100, 'USD') > Money(1, 'UZS') evaluates True (100 cents vs 1
#      tiyin across currencies), which is nonsense for money. I write < by
#      hand: same currency only, different currencies raise
#      CurrencyMismatchError.
#
# 7.2  sum([m1, m2]) first fails with
#          TypeError: unsupported operand type(s) for +: 'int' and 'Money'
#      because sum() starts from int 0. Fixed with __radd__ that accepts
#      exactly 0. I chose __radd__ over sum(items, start=Money(0, 'UZS'))
#      for production: a start value hard-codes a currency that would be
#      wrong for any USD report, and every call site would have to remember
#      to pass it - plain sum(money_list) keeps working for any currency.
#
# 7.3  When the other object is not Money, __add__/__eq__ (and every other
#      two-sided operator) must return NotImplemented - NOT False, NOT an
#      exception: Python then lets the other operand try before giving up.
#
# 7.4  Money * Money or Money / Money: NO. Money is a value, not a ratio;
#      only "amount times a plain number" (a quantity) has an obvious
#      meaning, so only quantity multiplication is supported.
#
# Done when: adding different currencies raises CurrencyMismatchError,
#            sum() works, Money(5, 'UZS') == 5 is False, and Money objects
#            can be dictionary keys.

from dataclasses import dataclass

import pytest


class CurrencyMismatchError(ValueError):
    """Adding or comparing two different currencies is a data error."""


@dataclass(frozen=True)
class Money:
    amount: int          # minor units: tiyin (UZS), cents (USD)
    currency: str        # 'UZS', 'USD', ...

    # ---------- addition: same currency only ------------------------------
    def __add__(self, other: object):
        if not isinstance(other, Money):
            return NotImplemented                      # 7.3
        if other.currency != self.currency:
            raise CurrencyMismatchError(
                f"cannot add {self.currency} and {other.currency}"
            )
        return Money(self.amount + other.amount, self.currency)

    def __radd__(self, other: object):
        # 7.2: sum() starts from int 0, so Python evaluates 0 + first_money.
        if isinstance(other, int) and other == 0:
            return self
        return NotImplemented

    # ---------- quantity multiplication ------------------------------------
    def __mul__(self, factor: object):
        if isinstance(factor, bool) or not isinstance(factor, int):
            return NotImplemented
        return Money(self.amount * factor, self.currency)

    def __rmul__(self, factor: object):
        if isinstance(factor, bool) or not isinstance(factor, int):
            return NotImplemented
        return self * factor

    # ---------- ordering: same currency only (7.1) -------------------------
    def __lt__(self, other: object):
        if not isinstance(other, Money):
            return NotImplemented
        if other.currency != self.currency:
            raise CurrencyMismatchError(
                f"cannot compare {self.currency} with {other.currency}"
            )
        return self.amount < other.amount


# --------------------------- tests ---------------------------

def test_add_same_currency():
    assert Money(1_000, "UZS") + Money(500, "UZS") == Money(1_500, "UZS")


def test_add_different_currencies_raises():
    with pytest.raises(CurrencyMismatchError):
        Money(1_000, "UZS") + Money(1_000, "USD")


def test_sum_of_a_money_list():
    total = sum([Money(3_000, "UZS"), Money(4_500, "UZS"), Money(2_500, "UZS")])
    assert total == Money(10_000, "UZS")


def test_money_is_never_equal_to_a_number():
    assert (Money(500, "UZS") == 500) is False        # does not crash
    assert (Money(500, "UZS") != 500) is True


def test_money_is_a_dictionary_key():
    invoices = {Money(1, "USD"): "invoice 1"}
    assert invoices[Money(1, "USD")] == "invoice 1"


def test_quantity_multiplication_on_both_sides():
    m = Money(100, "UZS")
    assert m * 3 == Money(300, "UZS")
    assert 3 * m == Money(300, "UZS")


def test_booleans_do_not_count_as_quantities():
    with pytest.raises(TypeError):
        True * Money(100, "UZS")                      # see 4.1 of Lab 4A


def test_money_times_money_has_no_meaning():
    with pytest.raises(TypeError):
        Money(100, "UZS") * Money(2, "UZS")           # answer 7.4


def test_ordering_inside_one_currency():
    assert Money(100, "USD") < Money(1_000, "USD")
    assert not Money(1_000, "USD") < Money(100, "USD")


def test_ordering_across_currencies_raises():
    with pytest.raises(CurrencyMismatchError):
        Money(100, "USD") < Money(1, "UZS")


def test_money_does_not_mutate():
    m = Money(50, "UZS")
    with pytest.raises(AttributeError):
        m.amount = 60
