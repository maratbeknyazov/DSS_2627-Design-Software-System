# Lab 4B - Task 9 - invoices that were never saved
#
# 9.1  BEFORE running I expected all four lines, ending with
#      "Model.save: INSERT/UPDATE". Reality (verified): only two lines -
#          TimestampMixin: set updated_at
#          ValidateMixin: validate fields
#      ValidateMixin forgot super().save(), and the co-operative chain
#      stops there: AuditMixin and Model never run, so the invoice is never
#      INSERTed and never audited - "201 Created" with nothing saved and
#      nothing in the logs (no error: every save() "completed").
#      Invoice.__mro__ shows the route the calls must follow:
#          Invoice -> TimestampMixin -> ValidateMixin -> AuditMixin -> Model
#      every class MUST call super().save() to move the work down the MRO.
#
# 9.2  Fixed ValidateMixin (super().save() restored). The four lines now
#      appear in this order: TimestampMixin / ValidateMixin / Model /
#      AuditMixin. "write audit entry" comes AFTER the INSERT because
#      AuditMixin calls super().save() FIRST and prints afterwards - the
#      audit records what has just been committed, not what is about to be.
#
# 9.3  Validation must RAISE. A silent return looks like a successful save:
#      no database row AND no traceback - the same "no error in the logs"
#      that created the incident. Raising stops everything after the
#      validation: nothing after the validation runs (verified in a test).
#
# 9.4  Reordered bases Invoice(TimestampMixin, AuditMixin, Model,
#      ValidateMixin) - predicted output: TimestampMixin / Model /
#      AuditMixin, and the ValidateMixin lines never appear. Confirmed by
#      running it (test below). The rule it shows: a concrete base that
#      does NOT call super() (Model) must be LAST in the base list - the
#      chain always dies at the first class that forgets to move the call
#      down the MRO, and everything after it is silently skipped.
#
# Done when: Invoice().save() prints all four lines in the right order and
#            an invalid invoice raises an error so that nothing after the
#            validation runs.

import pytest


class Model:
    """Concrete base: intentionally does NOT call super().save()."""

    def save(self) -> None:
        print("Model.save: INSERT/UPDATE")


class TimestampMixin:
    def save(self) -> None:
        print("TimestampMixin: set updated_at")
        super().save()


class ValidateMixin:
    """9.2 - fixed: validates, raises on invalid, then super().save()."""

    def save(self) -> None:
        print("ValidateMixin: validate fields")
        errors = self.validation_errors()
        if errors:
            raise ValueError(f"invalid invoice: {errors}; save stopped")
        super().save()


class AuditMixin:
    def save(self) -> None:
        super().save()
        print("AuditMixin: write audit entry")


class Invoice(TimestampMixin, ValidateMixin, AuditMixin, Model):
    def __init__(self, total: int = 0) -> None:
        self.total = total

    def validation_errors(self) -> list[str]:
        return [] if self.total > 0 else ["total must be positive"]


class InvoiceReordered(TimestampMixin, AuditMixin, Model, ValidateMixin):
    """9.4 - the teammate's reordering, run to prove the rule."""

    def __init__(self, total: int = 0) -> None:
        self.total = total

    def validation_errors(self) -> list[str]:
        return [] if self.total > 0 else ["total must be positive"]


# --- the original broken code from the task, kept for the 9.1 evidence ---
class ValidateMixinOriginal:
    """The version that forgot super().save() (the incident itself)."""

    def save(self) -> None:
        print("ValidateMixin: validate fields")
        # forgot super().save()


class InvoiceOriginal(TimestampMixin, ValidateMixinOriginal, AuditMixin, Model):
    def __init__(self, total: int = 0) -> None:
        self.total = total

    def validation_errors(self) -> list[str]:
        return [] if self.total > 0 else ["total must be positive"]


# --------------------------- tests ---------------------------

def test_mro_is_exactly_the_base_order():
    names = [cls.__name__ for cls in Invoice.__mro__]
    assert names == [
        "Invoice",
        "TimestampMixin",
        "ValidateMixin",
        "AuditMixin",
        "Model",
        "object",
    ]


def test_original_broken_code_prints_only_two_lines(capsys):
    InvoiceOriginal(total=100).save()
    assert capsys.readouterr().out.splitlines() == [
        "TimestampMixin: set updated_at",
        "ValidateMixin: validate fields",
    ]


def test_fixed_invoice_prints_all_four_lines_in_the_right_order(capsys):
    Invoice(total=100).save()
    assert capsys.readouterr().out.splitlines() == [
        "TimestampMixin: set updated_at",
        "ValidateMixin: validate fields",
        "Model.save: INSERT/UPDATE",
        "AuditMixin: write audit entry",
    ]


def test_invalid_invoice_raises_and_nothing_after_validation_runs(capsys):
    with pytest.raises(ValueError):
        Invoice(total=-5).save()
    assert capsys.readouterr().out.splitlines() == [
        "TimestampMixin: set updated_at",
        "ValidateMixin: validate fields",
    ]


def test_reordered_bases_silently_skip_validate_mixin_9_4(capsys):
    InvoiceReordered(total=100).save()
    out = capsys.readouterr().out
    assert out.splitlines() == [
        "TimestampMixin: set updated_at",
        "Model.save: INSERT/UPDATE",
        "AuditMixin: write audit entry",
    ]                      # yes: ValidateMixin is never reached
    assert "validate fields" not in out
