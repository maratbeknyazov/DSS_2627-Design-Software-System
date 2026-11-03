# Lab 4B - Task 2 - the notifier that silently did nothing
#
# 2.1  Why no error at all: Python looks send() up on the instance at RUN
#      time. The typo `sned` did not override send() - it created a NEW,
#      unrelated method. notify() called the inherited base-class send(),
#      whose body is `pass`; a method that exists and returns None cannot
#      raise anything, so the channel "worked" and delivered nothing fora
#      week, with zero trace in the logs.
#
# 2.2  Notifier became an ABC with an abstract send(). The ABC machinery
#      checks the abstract names when the object is CREATED, so a subclass
#      that still lacks send() fails instantly with TypeError in the
#      constructor - the typo is found at creation instead of never.
#
# 2.3  send() is abstract: every channel speaks its own wire format.
#      notify() is concrete shared logic, written exactly once, inherited by
#      every child; max_length stays per-channel data (class attribute).
#
# 2.4  SmsNotifier with max_length = 160: the test proves notify() cuts the
#      text to each channel's own limit.
#
# Done when: creating the typo subclass raises TypeError, Notifier() cannot
#            be created, and notify() is written only once (on the base).

from abc import ABC, abstractmethod

import pytest


class Notifier(ABC):
    max_length = 1000

    @abstractmethod
    def send(self, recipient: str, text: str) -> None:
        """Deliver the message (specific to each channel)."""

    # 2.3: concrete, shared - never redefined by children.
    def notify(self, recipient: str, text: str) -> None:
        self.send(recipient, text[: self.max_length])


class TelegramNotifier(Notifier):
    max_length = 4096

    def send(self, recipient: str, text: str) -> None:
        print(f"telegram -> {recipient}: {text}")


class SmsNotifier(Notifier):
    max_length = 160

    def send(self, recipient: str, text: str) -> None:
        print(f"sms -> {recipient}: {text}")


# --------------------------- tests ---------------------------

def test_notifier_itself_cannot_be_created():
    with pytest.raises(TypeError):
        Notifier()


def test_typo_subclass_fails_at_creation():
    with pytest.raises(TypeError):
        class TelegramNotifierWithTypo(Notifier):
            max_length = 4096

            def sned(self, recipient: str, text: str) -> None:  # the typo
                print(f"telegram -> {recipient}: {text}")

        TelegramNotifierWithTypo()


def test_notify_is_written_only_once_on_the_base_class():
    assert "notify" in vars(Notifier)
    assert "notify" not in vars(TelegramNotifier)
    assert "notify" not in vars(SmsNotifier)


def test_notify_cuts_to_each_channels_own_limit(capsys):
    TelegramNotifier().notify("@ali", "x" * 5000)
    out = capsys.readouterr().out
    assert len(out.split(": ", 1)[1].strip()) == 4096

    SmsNotifier().notify("+99890", "y" * 5000)
    out = capsys.readouterr().out
    assert len(out.split(": ", 1)[1].strip()) == 160


def test_each_channel_sends_its_own_format(capsys):
    TelegramNotifier().notify("@ali", "hello")
    assert "telegram -> @ali: hello" in capsys.readouterr().out
