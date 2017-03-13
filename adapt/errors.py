"""Error classes."""

from typing import Dict, List, Union

ContextStep = Union[int, str]


class ValidationError(Exception):
    """An error that occured during validation."""

    pass


class Errors:
    """A collection of errors, each associated with a context."""

    def __init__(self) -> None:
        self.errors: List[str] = []
        self.nested: Dict[ContextStep, 'Errors'] = {}

    def add(self, context: List[ContextStep], message: str) -> None:
        """Record an error with the given context."""

        if context == []:
            self.errors.append(message)
        else:
            self.nested.setdefault(context[0], Errors()).\
                add(context[1:], message)

    def __repr__(self) -> str:
        return '<Errors: {errors}, {nested}>'.format(
            errors=', '.join(map(repr, self.errors)),
            nested=repr(self.nested),
        )
