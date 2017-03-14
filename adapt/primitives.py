"""Lenses for primitive types."""

from __future__ import absolute_import

from typing import Any

from .lens import Lens
from .utils import validate_type


class Typed(Lens):
    """Only accept values of a specific type."""

    def __init__(self, expected: type) -> None:
        self.expected = expected

    def get(self, target: Any) -> Any:
        return target

    def set(self, target: Any, value: str) -> Any:
        validate_type(self.expected, value)
        return value


string = Typed(str)

integer = Typed(int)
