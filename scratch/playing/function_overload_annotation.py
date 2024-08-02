from typing import List, Literal, Union, overload, Tuple, Optional
from typing_extensions import assert_type

@overload
def fct(a: str = ..., b: str = ..., c: str = ..., flag_len: Literal[False] = ..., d: str = ..., e: str = ...) -> List[str]:
    ...

@overload
def fct(*, a: str = ..., b: str = ..., c: str = ..., flag_len: Literal[True], d: str = ..., e: str = ...) -> int:
    ...
@overload
def fct(a: str, *, b: str = ..., c: str = ..., flag_len: Literal[True], d: str = ..., e: str = ...) -> int:
    ...
@overload
def fct(a: str, b: str, *, c: str = ..., flag_len: Literal[True], d: str = ..., e: str = ...) -> int:
    ...
@overload
def fct(a: str, b: str, c: str, flag_len: Literal[True], d: str = ..., e: str = ...) -> int:
    ...

@overload
def fct(*, a: str = ..., b: str = ..., c: str = ..., flag_len: bool, d: str = ..., e: str = ...) -> Union[int, List[str]]:
    ...
@overload
def fct(a: str, *, b: str = ..., c: str = ..., flag_len: bool, d: str = ..., e: str = ...) -> Union[int, List[str]]:
    ...
@overload
def fct(a: str, b: str, *, c: str = ..., flag_len: bool, d: str = ..., e: str = ...) -> Union[int, List[str]]:
    ...
@overload
def fct(a: str, b: str, c: str, flag_len: bool, d: str = ..., e: str = ...) -> Union[int, List[str]]:
    ...

def fct(a: str = "", b: str = "", c: str = "", flag_len: bool = False, d: str = "", e: str = "") -> Union[int, List[str]]:
    """
    Return list of parameters a, b, c, d, e which are not empty strings.
    flag_len returns just the length of the created list. This argument is in the middle, for demonstrating purposes.
    I would recommend it to be the first default argument, as this reduces the effort for overload.
    """
    lst_non_empty = list(filter(lambda x: len(x) > 0, [a, b, c, d , e]))
    if flag_len:
        return len(lst_non_empty)
    return lst_non_empty

def test_fct():
    assert fct("a", "b", "c") == ["a", "b", "c"]
    assert fct("a", "b", "c", True) == 3
    assert fct("a", "b", "c", e="e", d="d") == ["a", "b", "c", "d", "e"]
    assert fct("a", "b", "c", True, e="e", d="d") == 5

# CHECK RETURN TYPE OF FCT VIA MYPY
# $ mypy filename.py

assert_type(fct(), List[str])
assert_type(fct("a"), List[str])
assert_type(fct("a", "b"), List[str])
assert_type(fct("a", "b", "c"), List[str])
assert_type(fct("a", "b", "c", d="d"), List[str])
assert_type(fct("a", "b", "c", e="d"), List[str])
assert_type(fct("a", "b", "c", e="d", d="d"), List[str])
assert_type(fct("a", "b", e="d", d="d"), List[str])
assert_type(fct("a", e="d", d="d"), List[str])

assert_type(fct(flag_len=False), List[str])
assert_type(fct("a", flag_len=False), List[str])
assert_type(fct("a", "b", flag_len=False), List[str])
assert_type(fct("a", "b", "c", False), List[str])
assert_type(fct("a", "b", "c", flag_len=False), List[str])
assert_type(fct("a", "b", "c", False, d="d"), List[str])
assert_type(fct("a", "b", "c", flag_len=False, d="d"), List[str])
assert_type(fct("a", "b", "c", e="d", flag_len=False), List[str])
assert_type(fct("a", "b", "c", e="d", d="d", flag_len=False), List[str])
assert_type(fct("a", "b", flag_len=False, e="d", d="d"), List[str])
assert_type(fct("a", e="d", flag_len=False, d="d"), List[str])

assert_type(fct(flag_len=True), int)
assert_type(fct("a", flag_len=True), int)
assert_type(fct("a", "b", flag_len=True), int)
assert_type(fct("a", "b", "c", True), int)
assert_type(fct("a", "b", "c", flag_len=True), int)
assert_type(fct("a", "b", "c", True, d="d"), int)
assert_type(fct("a", "b", "c", flag_len=True, d="d"), int)
assert_type(fct("a", "b", "c", e="d", flag_len=True), int)
assert_type(fct("a", "b", "c", e="d", d="d", flag_len=True), int)
assert_type(fct("a", "b", flag_len=True, e="d", d="d"), int)
assert_type(fct("a", e="d", flag_len=True, d="d"), int)

flag: bool = False
assert_type(fct(flag_len=flag), Union[int, List[str]])
assert_type(fct("a", flag_len=flag), Union[int, List[str]])
assert_type(fct("a", "b", flag_len=flag), Union[int, List[str]])
assert_type(fct("a", "b", "c", flag), Union[int, List[str]])
assert_type(fct("a", "b", "c", flag_len=flag), Union[int, List[str]])
assert_type(fct("a", "b", "c", flag, d="d"), Union[int, List[str]])
assert_type(fct("a", "b", "c", flag_len=flag, d="d"), Union[int, List[str]])
assert_type(fct("a", "b", "c", e="d", flag_len=flag), Union[int, List[str]])
assert_type(fct("a", "b", "c", e="d", d="d", flag_len=flag), Union[int, List[str]])
assert_type(fct("a", "b", flag_len=flag, e="d", d="d"), Union[int, List[str]])
assert_type(fct("a", e="d", flag_len=flag, d="d"), Union[int, List[str]])




# this overload is the straightforward False case
@overload
def thing(value_1: str, value_2: str | None = None, include_extra: Literal[False] = False) -> Tuple[str, str]: ...

# this overload is mostly straightforward, except that we can't include a default value 
# for value_2 because arguments with default values must be at the end
# (if we included a default value for include_extra, the overloads would overlap)
# (if we made include_extra keyword-only, we wouldn't need this overload)
@overload
def thing(value_1: str, value_2: str | None, include_extra: Literal[True]) -> Tuple[str, str, str]: ...

# this overload is needed to cover the cases where value_2 is not provided
# (making include_extra keyword-only in this overload is the trick that lets us not give it a default value)
@overload
def thing(value_1: str, value_2: str | None = None, *, include_extra: Literal[True]) -> Tuple[str, str, str]: ...

# this overload is needed to cover the cases where type checkers can't figure out whether include_extra is True or False
# returning a union forces the user to check the return type; in some cases this is an annoying 
# thing and you might want to consider returning Any
@overload
def thing(value_1: str, value_2: str | None = None, *, include_extra: bool) -> Tuple[str, str] | Tuple[str, str, str]: ...

def thing(value_1: str, value_2: str | None = None, include_extra: bool = False):
    if value_2 is None:
        value_2 = "empty"
    if include_extra:
        return value_1, value_2, "extra"
    return value_1, value_2
