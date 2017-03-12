"""Test lenses."""

import unittest

from adapt.lens import Attribute

from .utils import test_person


class TestAttribute(unittest.TestCase):

    def test_lens(self) -> None:
        name = Attribute('name')

        person = test_person()
        self.assertEqual(name.get(person), "Ayano")

        person_ = name.set(person, "Nocchi")
        self.assertEqual(person_.name, "Nocchi")


class TestCompose(unittest.TestCase):

    def test_lens(self) -> None:
        address_lens = Attribute('address')
        number = Attribute('number')
        address = address_lens * number

        person = test_person()

        self.assertEqual(address.get(person), 12)

        person_ = address.set(person, 14)
        assert person_.address is not None
        self.assertEqual(person_.address.number, 14)
