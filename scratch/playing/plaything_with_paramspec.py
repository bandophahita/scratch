#!/usr/bin/env python3

from __future__ import annotations

from typing import (
    Any,
    Concatenate,
    ParamSpec,
    ParamSpecArgs,
    Tuple,
    Type,
    TypeVar,
    Union,
    Callable,
)


P = ParamSpec('P')


def bar(x: int, *args: bool) -> int:
    ...


def add(x: Callable[P, int]) -> Callable[Concatenate[str, P], int]:
    ...


t = add(bar)  # (str, /, x: int, *args: bool) -> int
reveal_type(t)

def remove(x: Callable[Concatenate[int, P], int]) -> Callable[P, int]:
    ...


y = remove(bar)  # (*args: bool) -> int
reveal_type(y)


def transform(x: Callable[Concatenate[int, P], int]) -> Callable[Concatenate[str, P], bool]:
    ...


z = transform(bar)  # (str, /, *args: bool) -> bool
reveal_type(z)
