"""Adapters for Django models."""

from typing import Any

from .lens import Lens, Object
from .transaction import atomic, on_commit


class Model(Object):
    """A lens for Django models."""

    @atomic
    def set(self, target: Any, value: Any) -> Any:
        """Set the values and save the model."""
        target_ = super().set(target, value)
        on_commit(target_.save)
        return target_


class QuerySet(Lens):
    """A lens for querysets."""

    def __init__(self, model: Model) -> None:
        self.model = model

    def get(self, target: Any) -> Any:
        return {
            instance.pk: self.model.get(instance)
            for instance in target
        }

    @atomic
    def set(self, target: Any, value: Any) -> Any:
        raise NotImplementedError
