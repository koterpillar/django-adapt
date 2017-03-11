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


class Attribute(Lens):
    """Lens targeting an object's specific attribute."""

    def __init__(self, attribute: str) -> None:
        self.attribute = attribute

    def get(self, target: T) -> Any:
        return getattr(target, self.attribute)

    def set(self, target: T, value: Any) -> T:
        setattr(target, self.attribute, value)
        return target
