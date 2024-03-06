from __future__ import annotations
from typing import get_args, Literal, TypeAlias
from enum import Enum


class ValidArgs(Enum):
    FOO = "foo"
    BAR = "bar"



T_foo = Literal['foo']
T_bar = Literal['bar']

FOO: T_foo = get_args(T_foo)[0]
BAR: T_bar = get_args(T_bar)[0]


def func(argument: T_foo | T_bar) -> None:
    ...


#mypy checks

func(FOO)  # OK
func('foo')  # OK
func('baz')  # error: Argument 1 to "func" has incompatible type "Literal['baz']"; expected "Literal['foo', 'bar']"  [arg-type]
# func(ValidArgs.FOO)
# func(ValidArgs.BAR)


# reveal_type(FOO) # note: Revealed type is "Literal['foo']" 
# reveal_type(BAR) # note: Revealed type is "Literal['bar']"
# reveal_type(VALID_ARGUMENTS)  # note: Revealed type is "tuple[Literal['foo'], Literal['bar']]"
