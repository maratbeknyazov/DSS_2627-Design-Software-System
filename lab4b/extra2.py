# Lab 4B - Extra E2 - payment methods that register themselves
#
# E2.1  PaymentMethod.__init_subclass__ registers every concrete subclass
#       automatically under the name given in the class header:
#           class Click(PaymentMethod, name="click")
#       The registry fills itself - no hand-maintained list anywhere.
#
# E2.2  A concrete subclass WITHOUT a name fails the moment the class is
#       defined (= when its module is imported), with a message saying how
#       to fix it. Abstract middle classes may skip the name; they are
#       recognised with inspect.isabstract(cls) - True while the class
#       still carries abstract methods.
#
# E2.3  Two classes with the same name: TypeError at import - never a
#       silent overwrite of the earlier registration.
#
# E2.4  Trade-off: __init_subclass__ fires only when the module is actually
#       imported. The explicit Task-10 registry wins when modules may never
#       be imported: lazy/optional loading or a plugin file that the
#       process does not read.
#
# Done when: adding a class and importing its module is enough, and a
#            duplicate name fails loudly.

import inspect
from abc import ABC, abstractmethod
from typing import ClassVar

import pytest


class PaymentMethod(ABC):
    registry: ClassVar[dict[str, type["PaymentMethod"]]] = {}

    @abstractmethod
    def fee(self, amount: int) -> int: ...

    # E2.1 - self-registration.
    def __init_subclass__(cls, /, name: str | None = None, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        if name is None:
            if not inspect.isabstract(cls):
                raise TypeError(
                    f"{cls.__name__} is concrete but has no name; write "
                    f"class {cls.__name__}(PaymentMethod, "
                    f"name='{cls.__name__.lower()}')"
                )
            return                                  # abstract may skip the name
        key = name.strip().lower()
        if key in PaymentMethod.registry:           # E2.3 - fail loudly
            raise TypeError(
                f"payment method name '{key}' is already taken by "
                f"{PaymentMethod.registry[key].__name__}"
            )
        PaymentMethod.registry[key] = cls


class AbstractBankPayment(PaymentMethod):
    """Abstract middle class: keeps abstract fee, allowed without a name."""


class Click(PaymentMethod, name="click"):
    def fee(self, amount: int) -> int:
        return amount * 10 // 1000


class Payme(PaymentMethod, name="payme"):
    def fee(self, amount: int) -> int:
        return amount * 10 // 1000


def create(name: str) -> PaymentMethod:
    return PaymentMethod.registry[name.strip().lower()]()


# --------------------------- tests ---------------------------

def test_concrete_classes_register_themselves_at_import():
    assert PaymentMethod.registry["click"] is Click
    assert PaymentMethod.registry["payme"] is Payme
    assert isinstance(create("click"), Click)


def test_abstract_middle_class_may_skip_the_name():
    assert inspect.isabstract(AbstractBankPayment)
    assert "abstractbankpayment" not in PaymentMethod.registry


def test_concrete_subclass_without_name_fails_at_definition_time():
    with pytest.raises(TypeError, match="no name"):
        class Cash(PaymentMethod):            # noqa: F811 (intentional demo)
            def fee(self, amount: int) -> int:
                return 0


def test_duplicate_name_fails_loudly_at_definition_time():
    with pytest.raises(TypeError, match="already taken"):
        class AnotherClick(PaymentMethod, name="click"):
            def fee(self, amount: int) -> int:
                return 0


def test_registry_name_is_normalised():
    class BankTransfer(PaymentMethod, name=" bank_transfer "):
        def fee(self, amount: int) -> int:
            return 5_000

    assert PaymentMethod.registry["bank_transfer"] is BankTransfer
