# typemock

[![CI](https://github.com/hexvon/typemock/actions/workflows/ci.yml/badge.svg)](https://github.com/hexvon/typemock/actions/workflows/ci.yml)
[![Documentation Status](https://readthedocs.org/projects/typemock/badge/?version=latest)](https://typemock.readthedocs.io/en/latest/?badge=latest)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Type safe mocking for Python 3.12+.

1. [Motivation](#motivation)
2. [Installation](#installation)
3. [Quick example usage](#quick-example-usage)
4. [Features](#features)

[Detailed Documentation](https://typemock.readthedocs.io)

## Motivation

The mocking tools in Python are powerful, flexible and useful for building independent tests at various levels.

This flexibility is part of what is considered a strength of Python, and possibly any dynamically typed language.

However, this flexibility comes at a cost.

It is possible to build mocks which do not conform to the actual behaviour or contract defined by the things they are mocking. Or, for them to be initially correct, and then to go out of sync with actual behaviour and for tests to remain green.

We do not have compile time protections for us doing things with/to things which do not align with the contracts they define and the clients of those contracts expect.

But, now we have type hints. And so, we can explicitly define the contracts of our objects, and, if we have done this, we can mock them in a type safe way as well. This is what this library aims to help achieve. **Type safe mocking.**

Used in conjunction with a type checker basedpyright, this should result in much more high fidelity independent tests.

## Installation

From GitHub (this fork):

```bash
pip install git+https://github.com/hexvon/typemock.git
```

Or with uv:

```bash
uv add git+https://github.com/hexvon/typemock.git
```

From PyPI (original, may be outdated):

```bash
pip install typemock
```

## Quick Example Usage

Given some class (the implementation of its method is not relevant):

```python
class MyThing:
    def multiple_arg(self, prefix: str, number: int) -> str:
        pass
```

### Mock and verify

We can mock behaviour and verify interactions as follows:

```python
from typemock import tmock, setup_mock, when, verify

expected_result = "a string"

my_thing_mock = tmock(MyThing)

with setup_mock(my_thing_mock):
    when(my_thing_mock.multiple_arg("p", 1)).then_return(expected_result)

actual = my_thing_mock.multiple_arg(number=1, prefix="p")

assert expected_result == actual
verify(my_thing_mock).multiple_arg("p", 1)

# Or use calls() for more flexible verification
from typemock import calls

calls(my_thing_mock).multiple_arg.assert_called_once()
calls(my_thing_mock).multiple_arg.call_count  # 1

# Mock attributes/properties with attr()
from typemock import attr

class Config:
    name: str = "default"

config_mock = tmock(Config)
with setup_mock(config_mock):
    attr(config_mock.name).then_return("mocked")

assert config_mock.name == "mocked"
```

### Type safety

When we try to specify behaviour that does not conform to the contract of the object we are mocking:

```python
my_thing_mock = tmock(MyThing)

with setup_mock(my_thing_mock):
    when(my_thing_mock.multiple_arg(prefix="p", number="should be an int")).then_return("a string")
```

We get an informative error:

```
typemock.api.MockTypeSafetyError: Method: multiple_arg Arg: number must be of type:<class 'int'>
```

<details>
<summary>Legacy API</summary>

The older context manager syntax is still supported:

```python
with tmock(MyThing) as my_thing_mock:
    when(my_thing_mock.multiple_arg("p", 1)).then_return("result")
```

</details>

## Features

- **Type safe mocking** — validates argument and return types at runtime
- **Argument matchers** — use `match.anything()` or `match.instance_of(Type)` for flexible matching
- **Multiple responses** — `then_return_many()` for sequential responses
- **Exception mocking** — `then_raise()` to mock error conditions
- **Custom callbacks** — `then_do()` for custom response logic
- **Async support** — works with async/await methods
- **Attribute mocking** — mock class and instance attributes with `attr()`
- **Verification** — verify method calls with `verify()`
- **Call introspection** — inspect calls with `calls()` (call_count, call_args, assert_called_*)

## Requirements

- Python 3.12+
- typeguard >= 4.4.4

## License

MIT License — see [LICENSE](LICENSE) for details.

## Credits

Originally created by [Laurence Willmore](https://github.com/lgwillmore).

Currently maintained by [Matt Poletaev](https://github.com/hexvon).