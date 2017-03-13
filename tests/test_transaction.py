"""Test transactions."""

import unittest
from typing import List, Optional

from adapt.transaction import atomic, on_commit
from adapt.errors import ValidationError


Log = List[str]


@atomic
def simple_action(log: Log, marker: str, error: Optional[str] = None) -> None:
    """A simple action registering a commit hook."""
    log.append("{} 1".format(marker))

    on_commit(lambda: log.append("{} commit".format(marker)))

    if error is not None:
        raise ValidationError(error)

    log.append("{} 2".format(marker))


class TestTransaction(unittest.TestCase):
    """Test transactions."""

    def test_on_commit(self) -> None:
        """Test running commit hooks."""

        log = []

        @atomic
        def composite_action() -> None:
            """An action calling other actions."""

            log.append("outer 1")
            simple_action(log, "A")
            log.append("outer 2")
            simple_action(log, "B")

            on_commit(lambda: log.append("outer commit"))

            log.append("outer 3")

        composite_action()

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

        log = []

        @atomic
        def composite_action() -> None:
            """An action calling other actions."""

            log.append("outer 1")
            simple_action(log, "A")
            log.append("outer 2")
            simple_action(log, "B", error="Fails")

            on_commit(lambda: log.append("outer commit"))

            log.append("outer 3")

        with self.assertRaises(ValidationError):
            composite_action()

        self.assertEqual(log, [
            "outer 1",
            "A 1",
            "A 2",
            "outer 2",
            "B 1",
        ])
