"""Test primitive lenses."""

import unittest

from adapt.primitives import string


class TestPrimitives(unittest.TestCase):

    def test_string(self) -> None:
        value = "Contents"

        self.assertEqual(string.get(value), "Contents")

        value_ = string.set(value, "Different")
        self.assertEqual(value_, "Different")

        with self.assertRaises(TypeError):
            string.set(value, 12)  # type: ignore
