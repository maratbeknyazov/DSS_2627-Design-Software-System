# Lab 4B - Inheritance, Polymorphism and Composition
# Task 1 - a new payment method must not touch Checkout
#
# 1.1  PaymentMethod is an abstract base class (ABC, slide 34): fee(amount) is
#      an @abstractmethod and refundable() is abstract too, so every provider
#      is FORCED to state its own fee rule and whether money can be refunded.
#
# 1.2  One class or two for Click/Payme? I chose TWO classes. Today both rules
#      are 1 %, but the providers change independently: next month one fee
#      changes and I edit exactly one small class. A shared class would need
#      flags or a fork anyway and would couple two partners that have nothing
#      else in common. (Two objects of one class would mean editing that
#      class - and everything that uses it - the moment they diverge.)
#
# 1.3  Checkout.pay(method, amount) now takes a PaymentMethod object; the
#      if/elif chain and any isinstance are gone - polymorphism replaced the
#      branching, and the fee rule lives with the data that owns it.
#
# 1.4  BankTransfer added: fixed 5 000 sum fee, refundable.
#      Checkout: 0 lines changed. Every existing class: 0 lines changed.
#
# Done when: Checkout has no branch on the payment method (a brand-new local
#            class in the test proves it), adding BankTransfer changed no
#            existing class, every method has a test. (Turning the string
#            "click" from the HTTP request into an object is Task 10.)

from abc import ABC, abstractmethod

import pytest


class PaymentMethod(ABC):
    """Base class for every payment provider (slide 34)."""

    @abstractmethod
    def fee(self, amount: int) -> int:
        """Fee in sum for paying `amount` (must stay an int - it is money)."""

    @abstractmethod
    def refundable(self) -> bool:
        """Whether the charged amount can be refunded."""


class Card(PaymentMethod):
    FEE_THOUSANDTHS = 15            # 1.5 %

    def fee(self, amount: int) -> int:
        return amount * self.FEE_THOUSANDTHS // 1000

    def refundable(self) -> bool:
        return True


class Click(PaymentMethod):
    FEE_THOUSANDTHS = 10            # 1 %

    def fee(self, amount: int) -> int:
        return amount * self.FEE_THOUSANDTHS // 1000

    def refundable(self) -> bool:
        return True


class Payme(PaymentMethod):
    # Same rule as Click today, but deliberately a separate class (answer 1.2).
    FEE_THOUSANDTHS = 10            # 1 %

    def fee(self, amount: int) -> int:
        return amount * self.FEE_THOUSANDTHS // 1000

    def refundable(self) -> bool:
        return True


class Cash(PaymentMethod):
    def fee(self, amount: int) -> int:
        return 0

    def refundable(self) -> bool:
        return False


class Checkout:
    """1.3 - no if / elif / isinstance on the payment method."""

    def pay(self, method: PaymentMethod, amount: int) -> dict:
        fee = method.fee(amount)
        return {"charged": amount + fee, "refundable": method.refundable()}


class BankTransfer(PaymentMethod):
    """1.4 - new sprint, new provider: nothing outside this class changed."""

    def fee(self, amount: int) -> int:
        return 5_000

    def refundable(self) -> bool:
        return True


# --------------------------- tests ---------------------------

@pytest.mark.parametrize(
    "method, amount, charged, refundable",
    [
        (Card(), 100_000, 101_500, True),
        (Click(), 100_000, 101_000, True),
        (Payme(), 100_000, 101_000, True),
        (Cash(), 100_000, 100_000, False),
        (BankTransfer(), 100_000, 105_000, True),
    ],
)
def test_each_provider_returns_its_own_rule(method, amount, charged, refundable):
    assert Checkout().pay(method, amount) == {
        "charged": charged,
        "refundable": refundable,
    }


def test_checkout_accepts_a_brand_new_method_with_zero_changes():
    # If Checkout still branched on the method, this locally defined class
    # would raise ValueError("unknown method") - it proves no branch remains.
    class VoucherPayment(PaymentMethod):
        def fee(self, amount: int) -> int:
            return 0

        def refundable(self) -> bool:
            return True

    assert Checkout().pay(VoucherPayment(), 5_000) == {
        "charged": 5_000,
        "refundable": True,
    }


def test_fee_is_never_a_float():
    # Money in sums -> int; integer division from the slide example.
    assert isinstance(Card().fee(99_999), int) and Card().fee(99_999) == 1_499


def test_base_class_cannot_be_created():
    with pytest.raises(TypeError):
        PaymentMethod()
