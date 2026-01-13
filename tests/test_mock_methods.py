from typing import Any
from unittest import TestCase

from typemock import match, setup_mock, tmock, verify, when
from typemock.api import NoBehaviourSpecifiedError


class NestedThing:
    nested_att: str = "internal"


class MyThing:
    def return_a_str(self) -> str:
        pass

    def convert_int_to_str(self, number: int) -> str:
        pass

    def multiple_arg(self, prefix: str, number: int) -> str:
        pass

    def do_something_with_side_effects(self) -> None:
        pass

    def method_with_default_args(self, first_number: int, second_string: str = "default") -> None:
        pass

    def method_with_standard_generic_args_and_return(
        self, list_arg: list[str], dict_arg: dict[str, int]
    ) -> dict[str, Any]:
        pass

    def method_with_object(self, nested_obj_arg: NestedThing) -> int:
        pass

    def method_with_args_and_kwargs(self, *args: str, **kwargs: int) -> bool:
        pass

    def method_with_normal_args_and_kwargs(
        self, explicit1: int, *args: str, explicit2: int, **kwargs: int
    ) -> bool:
        pass


mocked_things = [MyThing, MyThing()]


class TestBasicMethodMocking(TestCase):
    def test_mock__isinstance_of_mocked_class(self):
        for mocked_thing in mocked_things:
            with self.subTest("{}".format(mocked_thing)):
                my_thing_mock = tmock(mocked_thing)

                self.assertIsInstance(my_thing_mock, MyThing)

    def test_mock__can_mock_method__no_args__returns(self):
        for mocked_thing in mocked_things:
            with self.subTest("{}".format(mocked_thing)):
                expected_result = "a string"

                with tmock(mocked_thing) as my_thing_mock:
                    when(my_thing_mock.return_a_str()).then_return(expected_result)

                actual = my_thing_mock.return_a_str()

                self.assertEqual(expected_result, actual)
                verify(my_thing_mock).return_a_str()

    def test_mock__unmocked_method__NoBehaviourError(self):
        for mocked_thing in mocked_things:
            with self.subTest("{}".format(mocked_thing)):
                my_thing_mock: MyThing = tmock(mocked_thing)

                with self.assertRaises(NoBehaviourSpecifiedError):
                    my_thing_mock.return_a_str()

    def test_mock__try_to_mock_method_out_of_context(self):
        for mocked_thing in mocked_things:
            with self.subTest("{}".format(mocked_thing)):
                my_thing_mock: MyThing = tmock(mocked_thing)

                with self.assertRaises(NoBehaviourSpecifiedError):
                    when(my_thing_mock.return_a_str()).then_return("some string")

    def test_mock__can_mock_method__arg__returns(self):
        for mocked_thing in mocked_things:
            with self.subTest("{}".format(mocked_thing)):
                expected_result = "a string"

                with tmock(mocked_thing) as my_thing_mock:
                    when(my_thing_mock.convert_int_to_str(1)).then_return(expected_result)

                actual = my_thing_mock.convert_int_to_str(1)

                self.assertEqual(expected_result, actual)
                verify(my_thing_mock).convert_int_to_str(1)

    def test_mock__can_mock_method__object_arg__returns(self):
        for mocked_thing in mocked_things:
            with self.subTest("{}".format(mocked_thing)):
                expected_result = 2

                object_arg = NestedThing()

                with tmock(mocked_thing) as my_thing_mock:
                    when(my_thing_mock.method_with_object(object_arg)).then_return(expected_result)

                actual = my_thing_mock.method_with_object(object_arg)

                self.assertEqual(expected_result, actual)
                verify(my_thing_mock).method_with_object(object_arg)

    def test_mock__can_mock_method__args_and_kwargs__returns(self):
        for mocked_thing in mocked_things:
            with self.subTest("{}".format(mocked_thing)):
                expected_result = False

                with tmock(mocked_thing) as my_thing_mock:
                    when(
                        my_thing_mock.method_with_args_and_kwargs("a", "b", key1=1, key2=2)
                    ).then_return(expected_result)

                actual = my_thing_mock.method_with_args_and_kwargs("a", "b", key1=1, key2=2)

                self.assertEqual(expected_result, actual)
                verify(my_thing_mock).method_with_args_and_kwargs("a", "b", key1=1, key2=2)

    def test_mock__can_mock_method__multiple_args__returns(self):
        for mocked_thing in mocked_things:
            with self.subTest("{}".format(mocked_thing)):
                expected_result = "a string"

                with tmock(mocked_thing) as my_thing_mock:
                    when(my_thing_mock.multiple_arg("p", 1)).then_return(expected_result)

                actual = my_thing_mock.multiple_arg("p", 1)

                self.assertEqual(expected_result, actual)
                verify(my_thing_mock).multiple_arg("p", 1)

    def test_mock__can_mock_method__generic_args_and_return__returns(self):
        for mocked_thing in mocked_things:
            with self.subTest("{}".format(mocked_thing)):
                expected_result = {"my_key": True}

                with tmock(mocked_thing) as my_thing_mock:
                    when(
                        my_thing_mock.method_with_standard_generic_args_and_return(
                            list_arg=["hello"], dict_arg={"foo": False}
                        )
                    ).then_return(expected_result)

                actual = my_thing_mock.method_with_standard_generic_args_and_return(
                    list_arg=["hello"], dict_arg={"foo": False}
                )

                self.assertEqual(expected_result, actual)
                verify(my_thing_mock).method_with_standard_generic_args_and_return(
                    list_arg=["hello"], dict_arg={"foo": False}
                )

    def test_mock__can_mock_method__multiple_args__mixed_with_kwargs_in_usage(self):
        for mocked_thing in mocked_things:
            with self.subTest("{}".format(mocked_thing)):
                expected_result = "a string"

                with tmock(mocked_thing) as my_thing_mock:
                    when(my_thing_mock.multiple_arg("p", 1)).then_return(expected_result)

                actual = my_thing_mock.multiple_arg(number=1, prefix="p")

                self.assertEqual(expected_result, actual)
                verify(my_thing_mock).multiple_arg("p", 1)

    def test_mock__can_mock_method__multiple_args__mixed_with_kwargs_in_setup(self):
        for mocked_thing in mocked_things:
            with self.subTest("{}".format(mocked_thing)):
                expected_result = "a string"

                with tmock(mocked_thing) as my_thing_mock:
                    when(my_thing_mock.multiple_arg(number=1, prefix="p")).then_return(
                        expected_result
                    )

                actual = my_thing_mock.multiple_arg("p", 1)

                self.assertEqual(expected_result, actual)
                verify(my_thing_mock).multiple_arg("p", 1)

    def test_mock__can_mock_method__default_args(self):
        for mocked_thing in mocked_things:
            with self.subTest("{}".format(mocked_thing)):
                with tmock(mocked_thing) as my_thing_mock:
                    when(my_thing_mock.method_with_default_args(first_number=1)).then_return(None)

                my_thing_mock.method_with_default_args(1)

                verify(my_thing_mock).method_with_default_args(1)

    def test_mock__can_mock_method__default_args_with_matchers(self):
        for mocked_thing in mocked_things:
            with self.subTest("{}".format(mocked_thing)):
                with tmock(mocked_thing) as my_thing_mock:
                    when(
                        my_thing_mock.method_with_default_args(
                            first_number=match.anything(), second_string=match.anything()
                        )
                    ).then_return(None)

                my_thing_mock.method_with_default_args(1)

                verify(my_thing_mock).method_with_default_args(1)

    def test_mock__can_mock_method__no_args__no_return(self):
        for mocked_thing in mocked_things:
            with self.subTest("{}".format(mocked_thing)):
                with tmock(mocked_thing) as my_thing_mock:
                    when(my_thing_mock.do_something_with_side_effects()).then_return(None)

                my_thing_mock.do_something_with_side_effects()

                verify(my_thing_mock).do_something_with_side_effects()

    def test_mock__then_raise(self):
        for mocked_thing in mocked_things:
            with self.subTest("{}".format(mocked_thing)):
                expected_error = IOError()

                with tmock(mocked_thing) as my_thing_mock:
                    when(my_thing_mock.do_something_with_side_effects()).then_raise(expected_error)

                with self.assertRaises(IOError):
                    my_thing_mock.do_something_with_side_effects()

    def test_mock__then_return_many__loop_false(self):
        expected_responses = ["first response", "second response"]

        for mocked_thing in mocked_things:
            with self.subTest("{}".format(mocked_thing)):
                with tmock(mocked_thing) as my_thing_mock:
                    when(my_thing_mock.return_a_str()).then_return_many(expected_responses, False)

                for expected in expected_responses:
                    actual = my_thing_mock.return_a_str()
                    self.assertEqual(expected, actual)

                # Not looping, and responses have run out.
                with self.assertRaises(NoBehaviourSpecifiedError):
                    my_thing_mock.return_a_str()

    def test_mock__then_return_many__loop_true(self):
        expected_responses = ["first response", "second response"]

        for mocked_thing in mocked_things:
            with self.subTest("{}".format(mocked_thing)):
                with tmock(mocked_thing) as my_thing_mock:
                    when(my_thing_mock.return_a_str()).then_return_many(expected_responses, True)

                for i in range(2):
                    for expected in expected_responses:
                        actual = my_thing_mock.return_a_str()
                        self.assertEqual(expected, actual)

    def test_mock__then_do(self):
        expected_arg = 1

        def bounce_back_handler(number: int):
            assert number == expected_arg
            return "{}".format(number)

        for mocked_thing in mocked_things:
            with self.subTest("{}".format(mocked_thing)):
                with tmock(mocked_thing) as my_thing_mock:
                    when(my_thing_mock.convert_int_to_str(match.anything())).then_do(
                        bounce_back_handler
                    )

            actual = my_thing_mock.convert_int_to_str(expected_arg)

            self.assertEqual("1", actual)


class TestSetupMockAPI(TestCase):
    """Tests for the new setup_mock() context manager API."""

    def test_setup_mock__basic_usage(self):
        """Test that setup_mock works as an alternative to 'with tmock() as'."""
        expected_result = "a string"

        my_thing_mock = tmock(MyThing)

        with setup_mock(my_thing_mock):
            when(my_thing_mock.return_a_str()).then_return(expected_result)

        actual = my_thing_mock.return_a_str()

        self.assertEqual(expected_result, actual)
        verify(my_thing_mock).return_a_str()

    def test_setup_mock__with_args(self):
        """Test setup_mock with method arguments."""
        expected_result = "result"

        my_thing_mock = tmock(MyThing)

        with setup_mock(my_thing_mock):
            when(my_thing_mock.multiple_arg("prefix", 42)).then_return(expected_result)

        actual = my_thing_mock.multiple_arg("prefix", 42)

        self.assertEqual(expected_result, actual)
        verify(my_thing_mock).multiple_arg("prefix", 42)

    def test_setup_mock__multiple_setups(self):
        """Test that setup_mock can be called multiple times on the same mock."""
        my_thing_mock = tmock(MyThing)

        with setup_mock(my_thing_mock):
            when(my_thing_mock.return_a_str()).then_return("first")

        self.assertEqual("first", my_thing_mock.return_a_str())

        # Setup again with different behaviour
        with setup_mock(my_thing_mock):
            when(my_thing_mock.convert_int_to_str(1)).then_return("one")

        self.assertEqual("one", my_thing_mock.convert_int_to_str(1))

    def test_setup_mock__yields_same_mock(self):
        """Test that setup_mock yields the same mock object."""
        my_thing_mock = tmock(MyThing)

        with setup_mock(my_thing_mock) as yielded_mock:
            self.assertIs(my_thing_mock, yielded_mock)


# TODO: We can still mock a context object - idea: setup can only happen on_first - successive contexts revert.
