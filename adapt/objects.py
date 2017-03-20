"""Lenses for objects."""

from typing import Any, Dict

from .lens import Lens


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

