# Lab 4B - Task 6 - the export that refused the cloud
#
# 6.1  export_report does not need "a file"; it needs ONE BEHAVIOUR:
#      target.write(bytes) -> int. The isinstance(io.IOBase) check rejected a
#      perfectly capable upload object - the check is removed: duck typing
#      (slide 38). The need is described by a type, never by class identity.
#
# 6.2  typing.Protocol states that need statically:
#          class Writable(Protocol):
#              def write(self, data: bytes) -> int: ...
#      S3Upload matches Writable STRUCTURALLY - no inheritance anywhere.
#
# 6.3  Tests: io.BytesIO (a real file object), S3Upload (cloud) and a small
#      local FakeTarget - three classes with no common parent.
#
# 6.4  Passing something without write() moves the error LATER: Python
#      raises AttributeError only when the loop actually calls
#      target.write(...) in production. Static typing catches the same
#      mistake EARLIER, before the program runs. Verified:
#
#      $ mypy task06.py
#      Success: no issues found in 1 source file
#
#      and for the original defective design (a target without write()):
#      $ mypy mypy_demo.py
#      mypy_demo.py:23: error: Argument 2 to "export_report" has
#      incompatible type "NotWritable"; expected "Writable"  [arg-type]
#      Found 1 error in 1 file (checked 1 source file)
#
# Run once for verification, as the task requires:
#     pip install mypy pyflakes
#     mypy task06.py
#
# Done when: all three targets work without isinstance, and mypy reports a
#            target without write() before the program runs.

from collections.abc import Iterable
from typing import Protocol


class Writable(Protocol):
    """6.2 - the only capability export_report uses."""

    def write(self, data: bytes) -> int: ...


def export_report(
    rows: Iterable[Iterable[object]],
    target: Writable,
) -> None:
    # 6.1 - isinstance(io.IOBase) check removed; any object with write() works.
    for r in rows:
        target.write((",".join(map(str, r)) + "\n").encode())


class S3Upload:
    """Cloud 'file' - structurally a Writable, inherits from nothing."""

    def __init__(self, bucket: str, key: str) -> None:
        self.bucket, self.key = bucket, key
        self.parts: list[bytes] = []

    def write(self, data: bytes) -> int:
        self.parts.append(data)          # real code uploads them later
        return len(data)


# --------------------------- tests ---------------------------

def test_bytesio_target():
    import io

    out = io.BytesIO()
    export_report([["a", 1], ["b", 2]], out)
    assert out.getvalue() == b"a,1\nb,2\n"


def test_s3upload_target():
    upload = S3Upload("reports", "2026/11/03.csv")
    export_report([["a", 1], ["b", 2]], upload)
    assert upload.parts == [b"a,1\n", b"b,2\n"]


class FakeTarget:
    """Test fake: also just a Writable by structure."""

    def __init__(self) -> None:
        self.chunks: list[bytes] = []

    def write(self, data: bytes) -> int:
        self.chunks.append(data)
        return len(data)


def test_own_fake_target():
    fake = FakeTarget()
    export_report([["x", "y"]], fake)
    assert fake.chunks == [b"x,y\n"]
