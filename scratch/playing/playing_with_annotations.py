from __future__ import annotations

import typing_extensions as t

if t.TYPE_CHECKING:
    from collections.abc import Callable

P = t.ParamSpec("P")
T_co = t.TypeVar("T_co", covariant=True)


class ExpectCallable(t.Generic[P, T_co]): ...


class ExpectType(ExpectCallable[P, T_co]): ...


@t.overload
def expect(
    v: type[T_co], /, *args: P.args, **kwargs: P.kwargs
) -> ExpectType[P, T_co]: ...
@t.overload
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


t.assert_type(expect(A), ExpectType[[], A])  # Shouldn't be allowed
t.assert_type(expect(fn, "inp"), ExpectCallable[[str], None])
