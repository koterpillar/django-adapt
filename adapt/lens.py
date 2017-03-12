"""Lenses for Adapt."""

from abc import ABCMeta, abstractmethod
from typing import Any, TypeVar


T = TypeVar('T')

class Lens(metaclass=ABCMeta):
    """Abstract lens."""

    @abstractmethod
    def get(self, target: T) -> Any:
        """Get the value from an object."""
        pass

    @abstractmethod
    def set(self, target: T, value: Any) -> T:
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

    def get(self, target: T) -> Any:
        return self.inner.get(self.outer.get(target))

    def set(self, target: T, value: Any) -> T:
        inner_target = self.outer.get(target)
        inner_target_ = self.inner.set(inner_target, value)
        return self.outer.set(target, inner_target_)


class Attribute(Lens):
    """Lens targeting an object's specific attribute."""

    def __init__(self, attribute: str) -> None:
        self.attribute = attribute

    def get(self, target: T) -> Any:
        return getattr(target, self.attribute)

    def set(self, target: T, value: Any) -> T:
        setattr(target, self.attribute, value)
        return target
