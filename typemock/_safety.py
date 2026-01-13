import inspect
from typing import TypeVar

from typemock._utils import Blank, attributes, methods, try_instantiate_class
from typemock.api import MemberType, MissingHint, MissingTypeHintsError, TypeSafety

T = TypeVar("T")


def _validate_method_annotations(
    clazz: type[T], type_safety: TypeSafety, missing: list[MissingHint]
) -> None:
    for func_entry in methods(clazz):
        func = func_entry.func
        name = func_entry.name
        sig = inspect.signature(func_entry.func)
        if len(sig.parameters) > 0:
            annotations = func.__annotations__
            for param_name in sig.parameters:
                if param_name == "self":
                    continue
                else:
                    if param_name not in annotations:
                        missing.append(
                            MissingHint(path=[name, param_name], member_type=MemberType.ARG)
                        )

            if type_safety != TypeSafety.NO_RETURN_IS_NONE_RETURN and "return" not in annotations:
                missing.append(MissingHint(path=[name], member_type=MemberType.RETURN))


def _validate_attributes(clazz: type[T], instance: T | None, missing: list[MissingHint]) -> None:
    for attribute_entry in attributes(clazz, instance):
        if attribute_entry.type_hint is Blank:
            missing.append(
                MissingHint(path=[attribute_entry.name], member_type=MemberType.ATTRIBUTE)
            )


def get_missing_class_type_hints(
    clazz: type[T], instance: T | None, type_safety: TypeSafety
) -> list[MissingHint]:
    missing: list[MissingHint] = []
    _validate_attributes(clazz, instance, missing)
    _validate_method_annotations(clazz, type_safety, missing)
    return missing


def validate_class_type_hints(
    clazz: type[T],
    instance: T | None = None,
    type_safety: TypeSafety = TypeSafety.STRICT,
) -> None:
    """
    Args:
        clazz:
        instance:
        type_safety:

    Raises:

        MissingTypeHintsError

    """
    if type_safety == TypeSafety.RELAXED:
        return
    instance = instance or try_instantiate_class(clazz)
    missing = get_missing_class_type_hints(clazz, instance, type_safety)
    if len(missing) > 0:
        raise MissingTypeHintsError("{} has missing type hints.".format(clazz), missing)
