from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Self



class Base(ABC):
    arg1: int
    # arg2: bool

    @property
    @abstractmethod
    def arg2(self) -> bool:
        pass

    def __init__(self, arg3: str) -> None:
        self.arg3 = arg3
    
    def foo(self):
        print(self.arg2)
    
    @classmethod
    def with_stuff(cls, arg3: str) -> Self:
        return cls(arg3=arg3)



class SubClassA(Base):
    arg1 = 1
    # arg2 = False


class SubbyA(SubClassA):
    ...

# art = Base("asdf")
rt = SubbyA("arg")
sba = SubClassA.with_stuff("bla") # <---
# sba = SubClassA("bla")
sba.foo()
# SubClassB().with_stuff("bla")
