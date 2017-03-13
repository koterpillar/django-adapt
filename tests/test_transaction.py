"""Test transactions."""

import unittest
from typing import List, Optional, Set

from adapt.errors import ValidationError
from adapt.transaction import atomic, context, on_commit

Log = List[str]


@atomic
def simple_action(log: Log, marker: str, error: Optional[str] = None) -> None:
    """A simple validation action."""

    with context(marker):
        log.append("{} 1".format(marker))

        on_commit(lambda: log.append("{} commit".format(marker)))

        if error is not None:
            raise ValidationError(error)

        log.append("{} 2".format(marker))


@atomic
def composite_action(log: Log, errors: Optional[Set[str]] = None) -> None:
    """An action calling other actions."""

    with context():
        if errors is None:
            errors = set()

        log.append("outer 1")
        simple_action(log, "A", error="Error A" if "A" in errors else None)
        log.append("outer 2")
        simple_action(log, "B", error="Error B" if "B" in errors else None)

        on_commit(lambda: log.append("outer commit"))

        if "outer" in errors:
            raise ValidationError("Outer error")

        log.append("outer 3")


class TestTransaction(unittest.TestCase):
    """Test transactions."""

    def test_on_commit(self) -> None:
        """Test running commit hooks."""

        log: Log = []

        composite_action(log)

        self.assertEqual(log, [
            "outer 1",
            "A 1",
            "A 2",
            "outer 2",
            "B 1",
            "B 2",
            "outer 3",
            "A commit",
            "B commit",
            "outer commit",
        ])

    def test_on_commit_error(self) -> None:
        """Test commit hooks behavior on errors."""

        log: Log = []

        with self.assertRaises(ValidationError):
            composite_action(log, errors={"B"})

        self.assertEqual(log, [
            "outer 1",
            "A 1",
            "A 2",
            "outer 2",
            "B 1",
            "outer 3",
        ])


class TestErrors(unittest.TestCase):
    """Test error gathering."""

    def test_error_gathering(self) -> None:
        """Test gathering errors from different contexts."""

        log: Log = []

        with self.assertRaises(ValidationError) as raised:
            composite_action(log, errors={"A", "outer"})

        errors = raised.exception.args[0]
        self.assertEqual(errors.errors, ["Outer error"])
        self.assertEqual(list(errors.nested.keys()), ["A"])
        self.assertEqual(errors.nested["A"].errors, ["Error A"])
        self.assertEqual(errors.nested["A"].nested, {})
