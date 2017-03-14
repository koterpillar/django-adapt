"""Adapters for Django models."""

from typing import Any

from .lens import Object
from .transaction import atomic, on_commit


class Model(Object):
    """A lens for Django models."""

    @atomic
    def set(self, target: Any, value: Any) -> Any:
        """Set the values and save the model."""
        target_ = super().set(target, value)
        on_commit(target_.save)
        return target_
