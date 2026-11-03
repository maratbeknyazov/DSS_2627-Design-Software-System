# Lab 4B - Extra E4 - 'NoneType' object has no attribute 'discount_percent'
#
# E4.1  NoLoyalty is a Null Object: exactly the same interface as a real
#       card - 0 % discount, 0 points - so no call site can even tell it
#       apart, and the fifty copies of "if customer.loyalty is not None"
#       become unnecessary.
#
# E4.2  Customer.__init__ replaces a None with NoLoyalty() - the Customer
#       constructor creates it (it is cheap and stateless; a shared
#       singleton would work too, since NoLoyalty never changes).
#
# E4.3  checkout_summary below has no None check left at all.
#
# E4.4  A Null Object is the wrong choice when ABSENCE itself must stay
#       visible: a customer without a saved bank card is not "a card with
#       0 money" - the UI must show "add a card", the storage layer must
#       know nothing is stored. Use it only for behaviour-neutral absence.
#
# Done when: the checkout code has no None check for loyalty, and tests
#            cover a customer with a card and one without.

import pytest


class LoyaltyCard:
    def __init__(self, level: str) -> None:
        self.level = level

    def discount_percent(self) -> int:
        return {"silver": 3, "gold": 5, "platinum": 10}[self.level]

    def points_for(self, amount: int) -> int:
        return amount // 10_000


class NoLoyalty:
    """E4.1 - the null object: behaves like a card that gives nothing."""

    def discount_percent(self) -> int:
        return 0

    def points_for(self, amount: int) -> int:
        return 0


class Customer:
    def __init__(self, name: str, loyalty: LoyaltyCard | None = None) -> None:
        self.name = name
        self.loyalty = loyalty if loyalty is not None else NoLoyalty()


def checkout_summary(customer: Customer, amount: int) -> tuple[int, int]:
    # E4.3 - no None check anywhere, by design.
    discount = amount * customer.loyalty.discount_percent() // 100
    points = customer.loyalty.points_for(amount)
    return discount, points


# --------------------------- tests ---------------------------

def test_customer_without_card_gets_a_null_object():
    assert isinstance(Customer("ali").loyalty, NoLoyalty)
    assert Customer("ali").loyalty is not None


def test_customer_with_a_gold_card():
    summary = checkout_summary(Customer("ali", LoyaltyCard("gold")), 100_000)
    assert summary == (5_000, 10)                 # 5 % discount, 1 point / 10k


def test_customer_without_a_card():
    summary = checkout_summary(Customer("ali"), 100_000)
    assert summary == (0, 0)


def test_platinum_customer():
    summary = checkout_summary(Customer("x", LoyaltyCard("platinum")), 200_000)
    assert summary == (20_000, 20)


def test_every_level_maps_to_its_discount():
    for level, expected in ("silver", 3), ("gold", 5), ("platinum", 10):
        assert LoyaltyCard(level).discount_percent() == expected
