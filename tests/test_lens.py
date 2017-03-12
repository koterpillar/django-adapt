"""Test lenses."""

import unittest
from typing import Optional

from adapt.lens import Attribute


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


class TestAttribute(unittest.TestCase):

    def test_lens(self) -> None:
        name = Attribute('name')

        person = Person("Ayano", "ayano@naver.com")
        self.assertEqual(name.get(person), "Ayano")

        person_ = name.set(person, "Nocchi")
        self.assertEqual(person_.name, "Nocchi")


class TestCompose(unittest.TestCase):

    def test_lens(self) -> None:
        address_lens = Attribute('address')
        number = Attribute('number')
        address_number = address_lens * number

        address = Address("Banpo", 12)
        person = Person("Ayano", "ayano@naver.com", address)

        self.assertEqual(address_number.get(person), 12)

        person_ = address_number.set(person, 14)
        assert person_.address is not None
        self.assertEqual(person_.address.number, 14)
