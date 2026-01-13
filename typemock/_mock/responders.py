from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, Generic, NoReturn, TypeVar

from typemock.api import DoFunction, NoBehaviourSpecifiedError

T = TypeVar("T")
R = TypeVar("R")


class Responder(ABC, Generic[R]):
    """
    Base Responder for a given set of args. Allows for implementation of different logic to get the response.
    """

    @abstractmethod
    def response(self, *args, **kwargs) -> R:
        pass


class ResponderBasic[R](Responder[R]):
    def __init__(self, response: R):
        self._response = response

    def response(self, *args, **kwargs) -> R:
        return self._response


class ResponderRaise(Responder[NoReturn]):
    def __init__(self, error: Exception):
        self._error = error

    def response(self, *args, **kwargs) -> NoReturn:
        raise self._error


class ResponderMany[R](Responder[R]):
    def __init__(self, responses: list[R], loop: bool):
        self._responses = responses
        self._loop = loop
        self._index = 0

    def response(self, *args, **kwargs) -> R:
        if self._index > len(self._responses) - 1:
            if self._loop:
                self._index = 0
            else:
                raise NoBehaviourSpecifiedError(
                    "No more responses. Do you want to loop through many responses?"
                )
        response = self._responses[self._index]
        self._index += 1
        return response


class ResponderDo[R](Responder[R]):
    def __init__(
        self, do_function: DoFunction[R], ordered_call: Callable[..., tuple[tuple[str, Any], ...]]
    ):
        self._ordered_call = ordered_call
        self._do_function = do_function

    def response(self, *args, **kwargs) -> R:
        return self._do_function(*args, **kwargs)
