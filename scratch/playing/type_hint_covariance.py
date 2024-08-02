from typing import TypeVar, Generic, Iterator, Iterable


T_C = TypeVar("T_C")

class A(Generic[T_C]):
    pass

class B(A):
    pass

# covariant=False is actually the default, but making it explicit for the sake of the answer
A_nonco = TypeVar("A_nonco", bound=A, covariant=True, 
                  # contravariant=True
                  )

def foo(obj: A):
    pass

foo(B()) # I'd like the type checker to warn me here that it expects A, not B


T = TypeVar('T', covariant=False)
# T = TypeVar('T', contravariant=True)


class ImmutableList(Generic[T]):
    def __init__(self, items: Iterable[T]) -> None: 
        self.items = items
    def __iter__(self) -> Iterator[T]:
        return iter(self.items)

class Employee: 
    ...

class Manager(Employee): 
    ...

def dump_employees(emps: ImmutableList[Employee]) -> None:
    for emp in emps:
        ...

mgrs = ImmutableList([Manager()])
dump_employees(mgrs)  # Should be caught by type-checker


################################################################################
# def dump_more_employees(employees: list[Employee]) -> None:
#     for employee in employees:
#         ...
# 
# managers: list[Manager] = list([Manager()])
# dump_more_employees(managers)  # Should be caught by type-checker
