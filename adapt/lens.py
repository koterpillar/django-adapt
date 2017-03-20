"""Base lens definitions."""

from abc import ABCMeta, abstractmethod
from typing import Any


class Lens(metaclass=ABCMeta):
    """Abstract lens."""

    @abstractmethod
    def get(self, target: Any) -> Any:
        """Get the value from an object."""
        pass

    @abstractmethod
    def set(self, target: Any, value: Any) -> Any:
        """Update the value in the object."""
        pass

    def __mul__(self, inner: 'Lens') -> 'Lens':
        """Compose lenses."""

        return Composed(self, inner)


class Composed(Lens):
    """A composition of two lenses."""

    def __init__(self, outer: Lens, inner: Lens) -> None:
        self.outer = outer
        self.inner = inner

    def get(self, target: Any) -> Any:
        return self.inner.get(self.outer.get(target))

    def set(self, target: Any, value: Any) -> Any:
        inner_target = self.outer.get(target)
        inner_target_ = self.inner.set(inner_target, value)
        return self.outer.set(target, inner_target_)
