"""Test Django adapters."""

import os
import unittest

import django  # type: ignore
from django.core.management import call_command  # type: ignore

from adapt import integer, string
from adapt.django import Model, QuerySet


class TestDjango(unittest.TestCase):

    def setUp(self) -> None:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.sample_app.settings'
        django.setup()

        with open('/dev/null', 'w') as null:
            call_command('check', verbosity=0, stdout=null)
        call_command('migrate', run_syncdb=True, interactive=False, verbosity=0)
        call_command('flush', interactive=False, verbosity=0)

        self.address = Model({
            'street': string,
            'number': integer,
        })

        self.user = Model({
            'name': string,
            'email': string,
            'address': self.address,
        })

    def test_model(self) -> None:
        """Test updating a model."""

        from .sample_app.models import Address

        address_obj = Address.objects.create(
            street="Banpo",
            number=12,
        )

        self.assertEqual(self.address.get(address_obj), {
            'street': "Banpo",
            'number': 12,
        })

        address_obj_ = self.address.set(address_obj, {
            'street': "Gangnam",
            'number': 25,
        })
        self.assertEqual(address_obj_.street, "Gangnam")
        self.assertEqual(address_obj_.number, 25)

        address_obj_.refresh_from_db()
        self.assertEqual(address_obj_.street, "Gangnam")
        self.assertEqual(address_obj_.number, 25)

    def test_nested(self) -> None:
        """Test updating a nested model."""

        from .sample_app.models import Address, User

        address_obj = Address.objects.create(
            street="Banpo",
            number=12,
        )
        user_obj = User.objects.create(
            name="Ayano",
            email="ayano@example.com",
            address=address_obj,
        )

        self.assertEqual(self.user.get(user_obj), {
            'name': "Ayano",
            'email': "ayano@example.com",
            'address': {
                'street': "Banpo",
                'number': 12,
            },
        })

        user_obj_ = self.user.set(user_obj, {
            'name': "Nocchi",
            'email': "nocchi@example.com",
            'address': {
                'street': "Gangnam",
                'number': 25,
            },
        })

        self.assertEqual(user_obj_.name, "Nocchi")

        # Old address must have been updated in-place
        address_obj.refresh_from_db()
        self.assertEqual(address_obj.street, "Gangnam")

    def test_queryset(self) -> None:
        """Test queryset lens."""

        from .sample_app.models import Address

        address_qs = QuerySet(self.address)

        Address.objects.create(
            pk=10,
            street="Banpo",
            number=12,
        )
        Address.objects.create(
            pk=20,
            street="Gangnam",
            number=25,
        )

        self.assertEqual(address_qs.get(Address.objects.all()), {
            10: {
                'street': "Banpo",
                'number': 12,
            },
            20: {
                'street': "Gangnam",
                'number': 25,
            },
        })
