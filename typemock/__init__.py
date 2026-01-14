from collections.abc import Generator
from contextlib import contextmanager
from typing import TypeVar

from typemock._calls import CallsWrapper, _calls
from typemock._mock import _attr, _setup_mock, _tmock, _when
from typemock._verify import _verify
from typemock.api import ResponseBuilder, TypeSafety

T = TypeVar("T")
R = TypeVar("R")


def tmock(clazz: type[T] | T, type_safety: TypeSafety = TypeSafety.STRICT) -> T:
    return _tmock(clazz=clazz, type_safety=type_safety)


def when(mock_call_result: R) -> ResponseBuilder[R]:
    return _when(mock_call_result=mock_call_result)


def attr(mock_attr_access: R) -> ResponseBuilder[R]:
    return _attr(mock_attr_access=mock_attr_access)


def verify(mock: T, exactly: int = -1) -> T:
    return _verify(mock=mock, exactly=exactly)


def calls(mock: T) -> CallsWrapper[T]:
    return _calls(mock=mock)


@contextmanager
def setup_mock(mock: T) -> Generator[T, None, None]:
    with _setup_mock(mock) as m:
        yield m
