"""Lenses for Adapt."""

from abc import ABCMeta, abstractmethod
from typing import Any, Dict


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


class Attribute(Lens):
    """Lens targeting an object's specific attribute."""

    def __init__(self, attribute: str) -> None:
        self.attribute = attribute

    def get(self, target: Any) -> Any:
        return getattr(target, self.attribute)

    def set(self, target: Any, value: Any) -> Any:
        setattr(target, self.attribute, value)
        return target


class Object(Lens):
    """Lens converting object's attributes to a dictionary."""

    pointer = Attribute

    def __init__(self, attributes: Dict[str, Lens]) -> None:
        self.attributes = {
            attribute: self.pointer(attribute) * lens
            for attribute, lens in attributes.items()
        }

    def get(self, target: Any) -> Any:
        return {
            attribute: lens.get(target)
            for attribute, lens in self.attributes.items()
        }

    def set(self, target: Any, value: Any) -> Any:
        if type(value) is not dict:
            raise TypeError("Expected a dictionary.")
        for attribute, lens in self.attributes.items():
            target = lens.set(target, value[attribute])
        return target


class Maybe(Lens):
    """Lens identical to a given one, but passing None through unchanged."""

    def __init__(self, base: Lens) -> None:
        self.base = base

    def get(self, target: Any) -> Any:
        if target is None:
            return None
        return self.base.get(target)

    def set(self, target: Any, value: Any) -> Any:
        if value is None:
            return None
        return self.base.set(target, value)
