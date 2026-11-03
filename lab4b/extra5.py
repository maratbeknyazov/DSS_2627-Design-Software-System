# Lab 4B - Extra E5 - events that survive a deploy
#
# E5.1  OrderPlaced(order_id, total_tiyin, currency) and
#       OrderCancelled(order_id, reason). Every event has to_dict(), which
#       adds "type" and "version", and a @classmethod from_dict(data) -
#       an ALTERNATIVE CONSTRUCTOR that rebuilds the object from a payload.
#
# E5.2  decode() reads the payload and finds the class by "type" with one
#       dict lookup (EVENT_CLASSES) - no if/elif chain. An unknown type is
#       logged and skipped: decode returns None so one bad message never
#       stops the consumer.
#
# E5.3  Version 2 of OrderPlaced adds the OPTIONAL promo_code (None by
#       default). from_dict builds the object only from the fields the
#       dataclass knows, so:
#         - old code reading a v2 message silently ignores new fields;
#         - new code still reads version 1 messages (promo_code missing ->
#           None). Both directions are covered by tests.
#
# E5.4  from_dict is a @classmethod, not a @staticmethod, because it
#       receives cls: if a SUBCLASS of OrderPlaced (or a versioned subclass)
#       calls it, the subclass is built - the alternative constructor stays
#       polymorphic. A @staticmethod would hard-code the parent class.
#
# Done when: version 1 and version 2 messages are decoded by both old and
#            new code, and an unknown event type does not stop the
#            consumer.

import dataclasses
import logging

from typing import ClassVar

from pytest import LogCaptureFixture

import pytest


class _Event:
    """Shared scaffolding: type tag, version number, payload round-trip."""

    TYPE: ClassVar[str]
    VERSION: ClassVar[int] = 1

    def to_dict(self) -> dict:
        payload = dataclasses.asdict(self)
        payload["type"] = self.TYPE
        payload["version"] = self.VERSION
        return payload

    @classmethod
    def from_dict(cls, payload: dict):
        # E5.3 - build only from fields the class knows; unknown fields in
        # the payload are ignored, missing optional fields keep defaults.
        known = {f.name for f in dataclasses.fields(cls)}
        return cls(**{k: v for k, v in payload.items() if k in known})


@dataclasses.dataclass(frozen=True)
class OrderPlaced(_Event):
    order_id: int
    total_tiyin: int
    currency: str
    promo_code: str | None = None

    TYPE: ClassVar[str] = "order_placed"
    VERSION: ClassVar[int] = 2            # added promo_code in v2


@dataclasses.dataclass(frozen=True)
class OrderCancelled(_Event):
    order_id: int
    reason: str

    TYPE: ClassVar[str] = "order_cancelled"
    VERSION: ClassVar[int] = 1


# E5.2 - the registry instead of an if/elif chain.
EVENT_CLASSES: dict[str, type[_Event]] = {
    OrderPlaced.TYPE: OrderPlaced,
    OrderCancelled.TYPE: OrderCancelled,
}


def decode(payload: dict) -> _Event | None:
    cls = EVENT_CLASSES.get(payload.get("type"))
    if cls is None:
        logging.getLogger(__name__).warning(
            "unknown event type %r - skipping message %r",
            payload.get("type"), payload,
        )
        return None                       # the consumer keeps running
    return cls.from_dict(payload)


# --------------------------- tests ---------------------------

V1_ORDER_PLACED = {
    "type": "order_placed",
    "version": 1,
    "order_id": 1001,
    "total_tiyin": 100_000_00,
    "currency": "UZS",
}


def test_to_dict_adds_type_and_version_and_promo_code():
    event = OrderPlaced(1001, 100_000_00, "UZS", promo_code="SPRING10")
    payload = event.to_dict()
    assert payload["type"] == "order_placed" and payload["version"] == 2
    assert payload["promo_code"] == "SPRING10"


def test_new_code_still_reads_version_1_messages():
    decoded = decode(V1_ORDER_PLACED)
    assert isinstance(decoded, OrderPlaced)
    assert decoded.promo_code is None               # optional field: default


def test_new_code_reads_version_2_messages():
    v2 = dict(V1_ORDER_PLACED, version=2, promo_code="SPRING10")
    decoded = decode(v2)
    assert decoded.promo_code == "SPRING10"


def test_old_code_ignores_fields_it_does_not_know():
    # an old consumer would choke on unknown fields; here they are skipped
    payload = dict(V1_ORDER_PLACED, campaign_id="black-friday")
    decoded = decode(payload)
    assert isinstance(decoded, OrderPlaced)
    assert not hasattr(decoded, "campaign_id")


def test_order_cancelled_round_trip():
    payload = {"type": "order_cancelled", "reason": "customer changed mind",
               "order_id": 2002}
    decoded = decode(payload)
    assert decoded == OrderCancelled(2002, "customer changed mind")
    assert decoded.to_dict()["type"] == "order_cancelled"


def test_unknown_type_is_logged_and_skipped(caplog: LogCaptureFixture):
    assert decode({"type": "order_refunded", "x": 1}) is None
    assert any("unknown event type" in record.message
               for record in caplog.records)


def test_unknown_type_does_not_stop_the_consumer():
    batch = [V1_ORDER_PLACED,
             {"type": "order_refunded", "amount": 1},
             {"type": "order_cancelled", "order_id": 9, "reason": "r"}]
    decoded = [result for payload in batch if (result := decode(payload))]
    assert len(decoded) == 2                        # bad message skipped, loop went on
    assert isinstance(decoded[0], OrderPlaced)
    assert isinstance(decoded[1], OrderCancelled)


def test_from_dict_is_a_classmethod_for_subclasses():
    class RushDelivery(OrderPlaced):
        pass

    # E5.4 - cls flows through: a subclass builds the subclass.
    event = RushDelivery.from_dict(V1_ORDER_PLACED)
    assert type(event) is RushDelivery


def test_needs_pytest_import_guard():               # keeps pytest a real dependency
    assert pytest
