"""Test Django adapters."""

import os
import unittest

import django  # type: ignore
from django.core.management import call_command  # type: ignore
from django.forms import model_to_dict  # type: ignore

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

        from tests.sample_app.models import Address

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

        from tests.sample_app.models import Address, User

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

        from tests.sample_app.models import Address

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

        self.assertEqual(address_qs.get(Address.objects.all()), [
            (10, {
                'street': "Banpo",
                'number': 12,
            }),
            (20, {
                'street': "Gangnam",
                'number': 25,
            }),
        ])

        address_qs.set(Address.objects.all(), [
            # This object is preserved, with properties changed
            (10, {
                'street': "Banpo",
                'number': 15,
            }),
            # 20 is missing from the queryset and will be deleted
            # 30 is a new object with a PK given
            (30, {
                'street': "Chenggyecheon",
                'number': 70,
            }),
            # This is a new object with a PK assigned automatically
            (None, {
                'street': "Sejong",
                'number': 50,
            }),
        ])

        self.assertEqual(Address.objects.count(), 3)
        addr1, addr2, addr3 = Address.objects.all().order_by('street')
        self.assertEqual(model_to_dict(addr1), {
            'id': 10,
            'street': "Banpo",
            'number': 15,
        })
        self.assertEqual(model_to_dict(addr2), {
            'id': 30,
            'street': "Chenggyecheon",
            'number': 70,
        })
        # This new object has a PK assigned automatically
        self.assertEqual(addr3.street, "Sejong")
        self.assertEqual(addr3.number, 50)
