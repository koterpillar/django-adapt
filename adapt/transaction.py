"""
Compose adapters propagating validation errors and deferring commit actions.
"""

from contextlib import contextmanager
from functools import wraps
from typing import Any, Callable, List, Optional

from .errors import ContextStep, Errors, ValidationError

Hook = Callable[[], None]

AnyFunc = Callable[..., Any]

AnyAction = Callable[..., None]


class TransactionError(Exception):
    """An error raised when a transaction operation cannot be performed."""

    pass


class TransactionState:
    """Global transaction state for adapters."""

    active: bool = False
    hooks: List[Hook] = []
    context_steps: List[ContextStep] = []
    errors: Optional[Errors] = None

    def on_commit(self, hook: Hook) -> None:
        """
        Execute the given function as soon as the transaction is committed.
        """

        if not self.active:
            raise TransactionError(
                "on_commit hooks cannot be added outside of a transaction."
            )

        self.hooks.append(hook)

    def atomic(self, action: AnyFunc) -> AnyFunc:
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

            try:
                self.active = True
                result = action(*args, **kwargs)
                self.active = False

            except:
                # Error (other than validation error) occured, leave the
                # transaction and reset hooks
                self.hooks = []
                raise

            if self.errors is not None:
                self.hooks = []
                errors = self.errors
                self.errors = None
                raise ValidationError(errors)

            # No error, run hooks
            for hook in self.hooks:
                hook()
            self.hooks = []

            return result

        return wrapped

    def _add_error(self, error: ValidationError) -> None:
        """Preserve a validation error until the end of the transaction."""

        if self.errors is None:
            self.errors = Errors()

        message = error.args[0]
        self.errors.add(self.context_steps, message)

    @contextmanager
    def context(self, step: Optional[ContextStep] = None) -> Any:
        """
        Preserve the validation errors until the transaction ends, recording
        them under the given context.
        """

        if not self.active:
            yield
            return

        if step is not None:
            self.context_steps.append(step)

        try:
            yield

        except ValidationError as error:
            self._add_error(error)

        finally:
            if step is not None:
                self.context_steps.pop()


_state = TransactionState()

atomic = _state.atomic

context = _state.context

on_commit = _state.on_commit
