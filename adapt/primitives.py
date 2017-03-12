"""Lenses for primitive types."""

from typing import Any

from .lens import Lens


class String(Lens):
    """Only accept strings as attribute values."""

    def get(self, target: Any) -> Any:
        return target

    def set(self, target: Any, value: str) -> Any:
        if type(value) is not str:
            raise TypeError("Value must be a string.")
        return value


string = String()
