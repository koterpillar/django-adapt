"""Exception classes."""

from typing import Any, Dict, Union




class ValidationError(Exception):
    """
    An error that occured during validation.
    """

    def __init__(self, arg: Union[str, list, Dict[str, Any]]) -> None:
        if not isinstance(arg, list):
            arg = [arg]
        super().__init__(arg)
