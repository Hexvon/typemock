from unittest import TestCase

from typemock import calls, setup_mock, tmock, when
from typemock.api import VerifyError


class MyThing:
    def no_args(self) -> str:
        pass

    def with_args(self, name: str, count: int) -> str:
        pass


class TestCallCount(TestCase):
    def test_call_count__not_called(self):
        mock = tmock(MyThing)
        with setup_mock(mock):
            when(mock.no_args()).then_return("result")

        self.assertEqual(0, calls(mock).no_args.call_count)

    def test_call_count__called_once(self):
        mock = tmock(MyThing)
        with setup_mock(mock):
            when(mock.no_args()).then_return("result")

        mock.no_args()

        self.assertEqual(1, calls(mock).no_args.call_count)

    def test_call_count__called_multiple_times(self):
        mock = tmock(MyThing)
        with setup_mock(mock):
            when(mock.no_args()).then_return("result")

        mock.no_args()
        mock.no_args()
        mock.no_args()

        self.assertEqual(3, calls(mock).no_args.call_count)


class TestCallArgs(TestCase):
    def test_call_args__not_called(self):
        mock = tmock(MyThing)
        with setup_mock(mock):
            when(mock.with_args("test", 1)).then_return("result")

        self.assertIsNone(calls(mock).with_args.call_args)

    def test_call_args__returns_last_call(self):
        mock = tmock(MyThing)
        with setup_mock(mock):
            when(mock.with_args("first", 1)).then_return("result1")
            when(mock.with_args("second", 2)).then_return("result2")

        mock.with_args("first", 1)
        mock.with_args("second", 2)

        last_call = calls(mock).with_args.call_args
        self.assertEqual((("name", "second"), ("count", 2)), last_call)


class TestCallArgsList(TestCase):
    def test_call_args_list__empty_when_not_called(self):
        mock = tmock(MyThing)
        with setup_mock(mock):
            when(mock.with_args("test", 1)).then_return("result")

        self.assertEqual([], calls(mock).with_args.call_args_list)

    def test_call_args_list__contains_all_calls(self):
        mock = tmock(MyThing)
        with setup_mock(mock):
            when(mock.with_args("first", 1)).then_return("result1")
            when(mock.with_args("second", 2)).then_return("result2")

        mock.with_args("first", 1)
        mock.with_args("second", 2)

        call_list = calls(mock).with_args.call_args_list
        self.assertEqual(2, len(call_list))
        self.assertEqual((("name", "first"), ("count", 1)), call_list[0])
        self.assertEqual((("name", "second"), ("count", 2)), call_list[1])


class TestAssertCalled(TestCase):
    def test_assert_called__passes_when_called(self):
        mock = tmock(MyThing)
        with setup_mock(mock):
            when(mock.no_args()).then_return("result")

        mock.no_args()

        calls(mock).no_args.assert_called()

    def test_assert_called__fails_when_not_called(self):
        mock = tmock(MyThing)
        with setup_mock(mock):
            when(mock.no_args()).then_return("result")

        with self.assertRaises(VerifyError):
            calls(mock).no_args.assert_called()


class TestAssertCalledOnce(TestCase):
    def test_assert_called_once__passes_when_called_once(self):
        mock = tmock(MyThing)
        with setup_mock(mock):
            when(mock.no_args()).then_return("result")

        mock.no_args()

        calls(mock).no_args.assert_called_once()

    def test_assert_called_once__fails_when_not_called(self):
        mock = tmock(MyThing)
        with setup_mock(mock):
            when(mock.no_args()).then_return("result")

        with self.assertRaises(VerifyError):
            calls(mock).no_args.assert_called_once()

    def test_assert_called_once__fails_when_called_multiple_times(self):
        mock = tmock(MyThing)
        with setup_mock(mock):
            when(mock.no_args()).then_return("result")

        mock.no_args()
        mock.no_args()

        with self.assertRaises(VerifyError):
            calls(mock).no_args.assert_called_once()


class TestAssertNotCalled(TestCase):
    def test_assert_not_called__passes_when_not_called(self):
        mock = tmock(MyThing)
        with setup_mock(mock):
            when(mock.no_args()).then_return("result")

        calls(mock).no_args.assert_not_called()

    def test_assert_not_called__fails_when_called(self):
        mock = tmock(MyThing)
        with setup_mock(mock):
            when(mock.no_args()).then_return("result")

        mock.no_args()

        with self.assertRaises(VerifyError):
            calls(mock).no_args.assert_not_called()


class TestAssertCalledWith(TestCase):
    def test_assert_called_with__passes_when_args_match(self):
        mock = tmock(MyThing)
        with setup_mock(mock):
            when(mock.with_args("test", 42)).then_return("result")

        mock.with_args("test", 42)

        calls(mock).with_args.assert_called_with("test", 42)

    def test_assert_called_with__fails_when_args_dont_match(self):
        mock = tmock(MyThing)
        with setup_mock(mock):
            when(mock.with_args("test", 42)).then_return("result")

        mock.with_args("test", 42)

        with self.assertRaises(VerifyError):
            calls(mock).with_args.assert_called_with("different", 99)

    def test_assert_called_with__fails_when_not_called(self):
        mock = tmock(MyThing)
        with setup_mock(mock):
            when(mock.with_args("test", 42)).then_return("result")

        with self.assertRaises(VerifyError):
            calls(mock).with_args.assert_called_with("test", 42)


class TestAssertCalledOnceWith(TestCase):
    def test_assert_called_once_with__passes_when_called_once_with_args(self):
        mock = tmock(MyThing)
        with setup_mock(mock):
            when(mock.with_args("test", 42)).then_return("result")

        mock.with_args("test", 42)

        calls(mock).with_args.assert_called_once_with("test", 42)

    def test_assert_called_once_with__fails_when_called_multiple_times(self):
        mock = tmock(MyThing)
        with setup_mock(mock):
            when(mock.with_args("test", 42)).then_return("result")

        mock.with_args("test", 42)
        mock.with_args("test", 42)

        with self.assertRaises(VerifyError):
            calls(mock).with_args.assert_called_once_with("test", 42)

    def test_assert_called_once_with__fails_when_args_dont_match(self):
        mock = tmock(MyThing)
        with setup_mock(mock):
            when(mock.with_args("test", 42)).then_return("result")

        mock.with_args("test", 42)

        with self.assertRaises(VerifyError):
            calls(mock).with_args.assert_called_once_with("wrong", 99)
