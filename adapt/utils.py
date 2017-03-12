"""Utilities for use by all the lens."""

from typing import Any


WRONG_TYPE_MESSAGE = "Expected type {expected}, got a value of type {actual}."

def validate_type(expected: type, value: Any) -> None:
    actual = type(value)
    if actual is not expected:
        raise TypeError(WRONG_TYPE_MESSAGE.format(
            expected=expected,
            actual=actual,
        ))
