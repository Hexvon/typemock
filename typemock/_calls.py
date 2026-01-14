from typing import Any, Generic, TypeVar, cast

from typemock._mock.methods import MockMethodState
from typemock._mock.object import MockObject
from typemock.api import VerifyError

T = TypeVar("T")

type CallArgs = tuple[tuple[str, Any], ...]


class CallInfo:
    """Provides information about calls to a mocked method."""

    def __init__(self, method_state: MockMethodState) -> None:
        self._method_state = method_state

    @property
    def call_count(self) -> int:
        """Total number of times the method was called."""
        return len(self._method_state._call_record)

    @property
    def call_args(self) -> CallArgs | None:
        """Arguments of the last call, or None if never called."""
        if not self._method_state._call_record:
            return None
        return self._method_state._call_record[-1]

    @property
    def call_args_list(self) -> list[CallArgs]:
        """List of arguments for all calls."""
        return list(self._method_state._call_record)

    def assert_called(self) -> None:
        """Assert that the method was called at least once."""
        if self.call_count == 0:
            raise VerifyError(
                f"\nExpected '{self._method_state.name}' to have been called, but it was not called.\n"
            )

    def assert_called_once(self) -> None:
        """Assert that the method was called exactly once."""
        if self.call_count != 1:
            raise VerifyError(
                f"\nExpected '{self._method_state.name}' to have been called once. "
                f"Called {self.call_count} times.\n"
            )

    def assert_not_called(self) -> None:
        """Assert that the method was never called."""
        if self.call_count != 0:
            raise VerifyError(
                f"\nExpected '{self._method_state.name}' to not have been called. "
                f"Called {self.call_count} times.\n"
            )

    def assert_called_with(self, *args, **kwargs) -> None:
        """Assert that the last call had the specified arguments."""
        if self.call_count == 0:
            raise VerifyError(
                f"\nExpected '{self._method_state.name}' to have been called with {args}, {kwargs}. "
                f"Not called.\n"
            )
        expected = self._method_state._ordered_call(None, *args, **kwargs)
        actual = self.call_args
        if expected != actual:
            raise VerifyError(
                f"\nExpected call: {self._method_state.name}{expected}\n"
                f"Actual call: {self._method_state.name}{actual}\n"
            )

    def assert_called_once_with(self, *args, **kwargs) -> None:
        """Assert that the method was called exactly once with the specified arguments."""
        self.assert_called_once()
        self.assert_called_with(*args, **kwargs)


def _call_info_for_method(method_state: MockMethodState) -> CallInfo:
    return CallInfo(method_state)


class CallsWrapper(Generic[T]):
    """
    Type wrapper for calls() return type.

    Provides CallInfo for each method attribute access.
    """

    def __getattr__(self, name: str) -> CallInfo: ...


class _CallsObject(Generic[T]):
    """Wrapper that provides CallInfo for each method of a mock."""

    _tmock_initialised = False

    def __init__(self, mock: MockObject[T]) -> None:
        self._mock = mock
        self._method_infos: dict[str, CallInfo] = {}
        for method_state in mock._mock_method_states:
            self._method_infos[method_state.name] = CallInfo(method_state)
        self._tmock_initialised = True

    def __getattribute__(self, item: str) -> CallInfo:
        if item.startswith("_"):
            return object.__getattribute__(self, item)
        if object.__getattribute__(self, "_tmock_initialised"):
            method_infos = object.__getattribute__(self, "_method_infos")
            if item in method_infos:
                return method_infos[item]
        return object.__getattribute__(self, item)


def _calls(mock: T) -> CallsWrapper[T]:
    """
    Get call information for a mock's methods.

    Example:
        calls(my_mock).some_method.call_count
        calls(my_mock).some_method.assert_called_once()

    Args:
        mock: A mock object created with tmock()

    Returns:
        A wrapper that provides CallInfo for each method
    """
    return cast(CallsWrapper[T], cast(object, _CallsObject(cast(MockObject[T], mock))))
