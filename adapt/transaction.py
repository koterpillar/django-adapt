"""
Compose adapters propagating validation errors and deferring commit actions.
"""

from functools import wraps
from typing import Any, Callable, List


Hook = Callable[[], None]


class TransactionError(Exception):
    """An error raised when a transaction operation cannot be performed."""

    pass


class TransactionState:
    """Global transaction state for adapters."""

    active: bool = False
    hooks: List[Hook] = []

    def on_commit(self, hook: Hook) -> None:
        """
        Execute the given function as soon as the transaction is committed.
        """

        if not self.active:
            raise TransactionError(
                "on_commit hooks cannot be added outside of a transaction."
            )

        self.hooks.append(hook)

    def atomic(self, action: Callable[..., Any]) -> Callable[..., Any]:
        """
        Decorate the given action to execute as a transaction.
        """

        @wraps(action)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            """Execute the action as a transaction."""

            if self.active:
                # Already in a transaction.
                return action(*args, **kwargs)

            assert self.hooks == [], \
                "Must not have leftover hooks when entering a transaction."
            self.active = True

            try:
                result = action(*args, **kwargs)
            except:
                # Error occured, leave the transaction and reset hooks
                self.active = False
                self.hooks = []
                raise

            # No error, leave the transaction and run hooks
            self.active = False
            for hook in self.hooks:
                hook()
            self.hooks = []

            return result

        return wrapped


_state = TransactionState()

atomic = _state.atomic

on_commit = _state.on_commit
