from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any


class Matcher(ABC):
    @abstractmethod
    def matches(self, other: Any) -> bool:
        pass


class MatchAny(Matcher):
    def matches(self, other: Any) -> bool:
        return True

    def __eq__(self, other: object) -> bool:
        return True

    def __hash__(self) -> int:
        return hash(self.__class__)


class InstanceMatcher(Matcher):
    def __init__(self, expected_type: type | Callable[[], type]) -> None:
        self.expected_type = expected_type

    def matches(self, other: Any) -> bool:
        expected_type = (
            self.expected_type if isinstance(self.expected_type, type) else self.expected_type()
        )
        return isinstance(other, expected_type)

    def __eq__(self, other: object) -> bool:
        return self.matches(other)

    def __hash__(self) -> int:
        return hash(self.__class__)


_MATCH_ANY = MatchAny()


def anything[T]() -> T:
    """
    Returns a matcher that will match anything. Type safety is still preserved by the mock itself.
    """
    return _MATCH_ANY  # type: ignore[return-value]


def instance_of[T](expected_type: type[T]) -> T:
    """
    Returns a matcher that will match any instance of the given type.
    """
    return InstanceMatcher(expected_type)  # type: ignore[return-value]
