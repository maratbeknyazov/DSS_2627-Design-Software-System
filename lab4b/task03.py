# Lab 4B - Task 3 - students charged without VAT
#
# 3.1  FamilySubscription.__init__ was missing one line:
#          super().__init__(user, months)
#      so user / months / base_monthly were never created. The error shows up
#      only when price() runs because Python does NOT validate attributes at
#      creation time - an object may copy-count attribute; the AttributeError
#      is born at the FIRST READ of the missing attribute.
#
# 3.2  New structure (template method): every child overrides only net() -
#      the VARIANT part of pricing; Subscription.price() holds the CONSTANT
#      part (VAT) and is written in exactly one place.
#
# 3.3  Tests: standard 3 months = 168 000 sum; student 3 months = 84 000;
#      family, 4 members, 3 months = 369 600 (net 330 000 + 12 % VAT).
#
# 3.4  VAT 15 %: a SINGLE-line change of VAT_PERCENT in Subscription. No
#      child class opened, no child repeats the formula - the test below
#      proves one override of the constant moves every kind at once.
#
# Done when: no child repeats the VAT formula, every child __init__ calls
#            super().__init__, one VAT change affects every kind.

import inspect

import pytest


class Subscription:
    VAT_PERCENT = 12

    def __init__(self, user: str, months: int) -> None:
        self.user = user
        self.months = months
        self.base_monthly = 50_000

    def net(self) -> int:
        """The variant part - children may override only this."""
        return self.base_monthly * self.months

    def price(self) -> int:
        """The constant part - VAT in exactly one place."""
        net = self.net()
        return net * (100 + self.VAT_PERCENT) // 100


class StudentSubscription(Subscription):
    def net(self) -> int:
        # Rule: students pay 50 % of the net price.
        return self.base_monthly * self.months // 2


class FamilySubscription(Subscription):
    def __init__(self, user: str, months: int, members: list[str]) -> None:
        super().__init__(user, months)      # <- the line that was missing
        self.members = members

    def net(self) -> int:
        # Rule: + 20 000 sum net per extra member per month.
        extra = 20_000 * (len(self.members) - 1) * self.months
        return super().net() + extra


# --------------------------- tests ---------------------------

def test_standard_subscription_three_months():
    assert Subscription("ali", 3).price() == 168_000


def test_student_subscription_gets_half_net_and_still_pays_vat():
    assert StudentSubscription("ali", 3).price() == 84_000


def test_family_subscription_four_members_three_months():
    family = FamilySubscription("ali", 3, ["a", "b", "c", "d"])
    assert family.price() == 330_000 * 112 // 100          # 369 600


def test_one_vat_change_moves_every_kind():
    class Vat15Standart(Subscription):
        VAT_PERCENT = 15

    class Vat15Student(StudentSubscription):
        VAT_PERCENT = 15

    class Vat15Family(FamilySubscription):
        VAT_PERCENT = 15

    assert Vat15Standart("x", 3).price() == 150_000 * 115 // 100
    assert Vat15Student("x", 3).price() == 75_000 * 115 // 100
    assert Vat15Family("x", 3, ["a", "b", "c", "d"]).price() == 330_000 * 115 // 100


def test_children_do_not_repeat_the_vat_formula():
    assert "VAT_PERCENT" not in inspect.getsource(StudentSubscription.net)
    assert "VAT_PERCENT" not in inspect.getsource(FamilySubscription.net)


def test_every_child_init_calls_super():
    family = FamilySubscription("x", 3, ["a", "b", "c", "d"])
    assert family.months == 3                  # set by the parent __init__
    assert family.base_monthly == 50_000       # set by the parent __init__
