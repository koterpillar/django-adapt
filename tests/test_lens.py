"""Test lenses."""

import unittest

from adapt.objects import Attribute
from adapt.primitives import string

from .utils import test_person


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
