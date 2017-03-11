"""Test lenses."""

import unittest

from adapt.lens import Attribute


class Person:
    """Class to test attribute lens."""

    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email


class TestAttribute(unittest.TestCase):

    def test_lens(self):
        name = Attribute('name')

        person = Person("Ayano", "ayano@naver.com")
        self.assertEqual(name.get(person), "Ayano")

        person_ = name.set(person, "Nocchi")
        self.assertEqual(person_.name, "Nocchi")
