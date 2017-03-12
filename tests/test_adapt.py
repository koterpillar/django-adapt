"""Test adapters."""

import unittest

from adapt import Object, string
from .utils import test_person

class TestObject(unittest.TestCase):

    def test_lens(self) -> None:
        person = Object({
            'name': string,
            'email': string,
        })

        person_obj = test_person()

        self.assertEqual(person.get(person_obj), {
            'name': "Ayano",
            'email': "ayano@naver.com",
        })

        person_obj_ = person.set(person_obj, {
            'name': "Nocchi",
            'email': "nocchi@naver.com",
        })

        self.assertEqual(person_obj_.name, "Nocchi")
        self.assertEqual(person_obj_.email, "nocchi@naver.com")
