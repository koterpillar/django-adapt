"""Utilities for tests."""

from typing import Optional


class Address:
    """
    Sample address class.

    Real addresses aren't as simple as a street and a number, and a "street
    number" isn't really a number anyway.
    """

    def __init__(self, street: str, number: int) -> None:
        self.street = street
        self.number = number

class Person:
    """Sample person class."""

    def __init__(self, name: str, email: str, address: Optional[Address] = None) -> None:
        self.name = name
        self.email = email
        self.address = address


def test_person() -> Person:
    return Person(
        "Ayano",
        "ayano@naver.com",
        Address("Banpo", 12),
    )
