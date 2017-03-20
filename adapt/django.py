"""Adapters for Django models."""

from operator import attrgetter
from typing import Any, List

from .lens import Lens
from .objects import Object
from .transaction import atomic, on_commit
from .utils import validate_type


class Model(Object):
    """A lens for Django models."""

    @atomic
    def set(self, target: Any, value: Any) -> Any:
        """Set the values and save the model."""
        target_ = super().set(target, value)
        on_commit(target_.save)
        return target_


GET_PK = attrgetter('pk')


class QuerySet(Lens):
    """A lens for querysets."""

    def __init__(self, model: Model) -> None:
        self.model = model

    def get(self, target: Any) -> Any:
        return [
            (instance.pk, self.model.get(instance))
            for instance in target
        ]

    @atomic
    def set(self, target: Any, value: Any) -> Any:
        validate_type(list, value)

        existing: List[Any] = []

        for key, item in value:
            if key is None:
                # Create a new model instance with no explicit PK
                instance = target.model()
            else:
                try:
                    # Get the existing model instance
                    instance = target.get(pk=key)
                except target.model.DoesNotExist:
                    # Create a new model instance with explicit PK
                    instance = target.model(pk=key)

            instance_ = self.model.set(instance, item)

            # Remember the instance, not to delete it
            existing.append(instance_)

        def cleanup() -> None:
            """Remove models omitted from the value."""
            target.exclude(pk__in=map(GET_PK, existing)).delete()

        on_commit(cleanup)

        return target
