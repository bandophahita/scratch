from __future__ import annotations

from typing import TYPE_CHECKING, Generic, ParamSpec, TypeVar, assert_type, overload

if TYPE_CHECKING:
    from collections.abc import Callable

P = ParamSpec("P")
T_co = TypeVar("T_co", covariant=True)


class ExpectCallable(Generic[P, T_co]): ...


class ExpectType(ExpectCallable[P, T_co]): ...


@overload
def expect(
    v: type[T_co], /, *args: P.args, **kwargs: P.kwargs
) -> ExpectType[P, T_co]: ...
@overload
def expect(
    v: Callable[P, T_co], /, *args: P.args, **kwargs: P.kwargs
) -> ExpectCallable[P, T_co]: ...
def expect(
    v: type[T_co] | Callable[P, T_co], /, *args: P.args, **kwargs: P.kwargs
) -> ExpectType[P, T_co] | ExpectCallable[P, T_co]:
    return ExpectType() if isinstance(v, type) else ExpectCallable()


class A:
    def __init__(self, inp: str, /) -> None: ...


def fn(inp: str, /) -> None: ...


assert_type(expect(A), ExpectType[[], A])  # Shouldn't be allowed
assert_type(expect(fn, "inp"), ExpectCallable[[str], None])

expect(A)
expect(fn, "inp")

