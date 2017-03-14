"""Test Django adapters."""

import os
import unittest

import django  # type: ignore
from django.core.management import call_command  # type: ignore

from adapt import integer, string
from adapt.django import Model


class TestDjango(unittest.TestCase):

    def setUp(self) -> None:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.sample_app.settings'
        django.setup()

        call_command('check')
        call_command('migrate', run_syncdb=True)

    def test_model(self) -> None:
        """Test updating a model."""

        from .sample_app.models import Address

        address_obj = Address.objects.create(
            street="Banpo",
            number=12,
        )

        address = Model({
            'street': string,
            'number': integer,
        })

        self.assertEqual(address.get(address_obj), {
            'street': "Banpo",
            'number': 12,
        })

        address_obj_ = address.set(address_obj, {
            'street': "Gangnam",
            'number': 25,
        })
        self.assertEqual(address_obj_.street, "Gangnam")
        self.assertEqual(address_obj_.number, 25)

        address_obj_.refresh_from_db()
        self.assertEqual(address_obj_.street, "Gangnam")
        self.assertEqual(address_obj_.number, 25)
