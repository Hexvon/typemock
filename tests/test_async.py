from unittest import TestCase

import trio as trio

from typemock import setup_mock, tmock, verify, when
from typemock.api import MockingError


class MyAsyncThing:
    async def get_an_async_result(self) -> str:
        pass

    async def get_list_result(self) -> list[str]:
        pass


def async_test(f):
    """
    An annotation for running an async test case with the trio.
    """

    def wrapper(*args):
        result = trio.run(f, *args)
        return result

    return wrapper


class TestAsyncMocking(TestCase):
    @async_test
    async def test_we_can_mock_and_verify_an_async_method(self):
        expected = "Hello"

        with tmock(MyAsyncThing) as my_async_mock:
            when(await my_async_mock.get_an_async_result()).then_return(expected)

        self.assertEqual(expected, await my_async_mock.get_an_async_result())

        verify(my_async_mock).get_an_async_result()

    @async_test
    async def test_we_get_an_error_if_we_do_not_await(self):
        expected = "Hello"

        with self.assertRaises(MockingError):
            with tmock(MyAsyncThing) as my_async_mock:
                when(my_async_mock.get_an_async_result()).then_return(expected)


class TestAsyncMockingWithSetupMock(TestCase):
    @async_test
    async def test_async_method_with_setup_mock(self):
        """Test async method mocking with setup_mock API."""
        mock = tmock(MyAsyncThing)
        with setup_mock(mock):
            when(await mock.get_an_async_result()).then_return("hello")

        result = await mock.get_an_async_result()
        self.assertEqual("hello", result)

    @async_test
    async def test_async_method_returns_list(self):
        """Test async method that returns a list."""
        mock = tmock(MyAsyncThing)
        with setup_mock(mock):
            when(await mock.get_list_result()).then_return(["a", "b", "c"])

        result = await mock.get_list_result()
        self.assertEqual(["a", "b", "c"], result)

    @async_test
    async def test_async_method_multiple_responses(self):
        """Test async method with multiple different responses."""
        mock = tmock(MyAsyncThing)
        with setup_mock(mock):
            when(await mock.get_an_async_result()).then_return_many(["first", "second", "third"])

        self.assertEqual("first", await mock.get_an_async_result())
        self.assertEqual("second", await mock.get_an_async_result())
        self.assertEqual("third", await mock.get_an_async_result())
