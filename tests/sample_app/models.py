"""Models for the test Django app."""

from django.db import models  # type: ignore


class Address(models.Model):  # type: ignore
    """Oversimplified address."""

    street = models.CharField(max_length=100)
    number = models.IntegerField()


class User(models.Model):  # type: ignore
    """A user."""

    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
