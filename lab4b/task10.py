# Lab 4B - Task 10 - choosing the class from a string
#
# 10.1  ONE registry lives here: the dict {"card": Card, ...,
#       "bank_transfer": BankTransfer} and create_payment_method(name)
#       returning a PaymentMethod object. The mapping sits at the EDGE of
#       the system - where the HTTP string enters.
#
# 10.2  An unknown name raises UnknownPaymentMethodError and its message
#       LISTS the supported names, so the mobile developer immediately sees
#       what to send.
#
# 10.3  One normalisation - name.strip().lower() - applied once, before the
#       dict lookup: " Payme ", "PAYME" and "payme" all find the same
#       entry. The payment classes themselves never see a string.
#
# 10.4  One mapping at the edge is fine because the outside world speaks in
#       NAMES: somewhere a name must become a class, and doing it in one
#       tested place gives one rule instead of three drifting copies. The
#       old if/elif inside Checkout was NOT acceptable: it ran on every
#       business call, existed in three modules that disagreed ("Payme" vs
#       "payme"), and made every new provider a change to working code.
#
# 10.5  Adding BankTransfer: one line in the registry here (the class
#       itself was added in task01.py in Task 1) - exactly ONE place.
#
# Done when: exactly one place in the code maps strings to classes, and
#            the tests cover the normalisation and the unknown-name error.

import pytest

from task01 import BankTransfer, Card, Cash, Click, Checkout, Payme, PaymentMethod


class UnknownPaymentMethodError(ValueError):
    """Raised for method names the registry does not know."""


# 10.1 - THE one place where a string becomes a class.
PAYMENT_METHODS: dict[str, type[PaymentMethod]] = {
    "card": Card,
    "click": Click,
    "payme": Payme,
    "cash": Cash,
    "bank_transfer": BankTransfer,        # 10.5 - the only line added
}


def create_payment_method(name: str) -> PaymentMethod:
    key = name.strip().lower()            # 10.3 - normalise exactly once
    try:
        cls = PAYMENT_METHODS[key]
    except KeyError:
        raise UnknownPaymentMethodError(
            f"unknown payment method {name!r}; "
            f"supported: {', '.join(sorted(PAYMENT_METHODS))}"
        ) from None
    return cls()


# --------------------------- tests ---------------------------

@pytest.mark.parametrize(
    "raw, expected_cls",
    [
        ("payme", Payme),
        ("PAYME", Payme),
        (" Payme ", Payme),
        ("card", Card),
        ("cash", Cash),
        ("bank_transfer", BankTransfer),
    ],
)
def test_names_are_normalised_once(raw, expected_cls):
    assert isinstance(create_payment_method(raw), expected_cls)


def test_unknown_name_lists_the_supported_names():
    with pytest.raises(UnknownPaymentMethodError) as exc_info:
        create_payment_method("crypto")
    message = str(exc_info.value)
    assert "crypto" in message
    for supported in ("bank_transfer", "card", "cash", "click", "payme"):
        assert supported in message


def test_error_is_a_value_error():
    # ValueError so a wide `except ValueError` at the API edge still catches it.
    assert issubclass(UnknownPaymentMethodError, ValueError)


def test_created_object_works_in_checkout():
    assert Checkout().pay(create_payment_method("CLICK"), 100_000) == {
        "charged": 101_000,
        "refundable": True,
    }


def test_bank_transfer_added_with_one_registry_line():
    method = create_payment_method(" bank_transfer ")
    assert method.fee(100_000) == 5_000
    assert method.refundable() is True
