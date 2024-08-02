
from typing import TypeVar, Generic

class A: ...
class B(A): ...
class C(B): ...

# InB = TypeVar('InB', bound=B)
# ContraB = TypeVar('ContraB', bound=B, contravariant=True)
# CoB = TypeVar('CoB', bound=B, covariant=True)
# 
# class In(Generic[InB]):
#     x: InB
# class Contra(Generic[ContraB]):
#     x: ContraB
# class Co(Generic[CoB]):
#     x: CoB
# 
# a = A()
# b = B()
# c = C()
# 
# m_in: In[B] = In()
# m_contra: Contra[B] = Contra()
# m_co: Co[B] = Co()
# 
# m_in.x = a  # mypy: Incompatible types in assignment (expression has type "A", variable has type "B").
# m_in.x = b
# m_in.x = c
# 
# m_contra.x = a # mypy: Incompatible types in assignment (expression has type "A", variable has type "B").
# m_contra.x = b
# m_contra.x = c
# 
# m_co.x = a # mypy: Incompatible types in assignment (expression has type "A", variable has type "B").
# m_co.x = b
# m_co.x = c

################################################################################
TV = TypeVar("TV")



class BoxCovariantChecked(Generic[TV]):
    def __init__(self, x: TV) -> None:
        self._x = x
        self._t = type(x)

    def check(self, x: TV) -> None:
        if not isinstance(x, self._t):
            raise TypeError(f"x is of type {type(x)}, which is not a {self._t}.")

    @property
    def x(self) -> TV:
        x = self._x
        self.check(x)
        return x

    @x.setter
    def x(self, x: TV) -> None:
        self.check(x)
        self._x = x


tb = BoxCovariantChecked(A())
tb.x = A()
print(tb.x)  # <__main__.A object at 0x104b0f0d0>
tb.x = B()
print(tb.x)  # <__main__.B object at 0x104b0eb60>
tb.x = C()
print(tb.x)  # <__main__.C object at 0x104b0f0d0>

mb = BoxCovariantChecked(B())

# mb.x = A() # Incompatible types in assignment (expression has type "A", variable has type "B")  [assignment]
print(mb.x)
mb.x = B()
print(mb.x)
mb.x = C()
print(mb.x)

bb = BoxCovariantChecked(C())
# Runtime TypeError: x is of type <class '__main__.T'>, which is not a <class '__main__.B'>.
# mypy error: Incompatible types in assignment (expression has type "T", variable has type "B")  [assignment]
# bb.x = A()
print(bb.x)
# Runtime TypeError: x is of type <class '__main__.M'>, which is not a <class '__main__.B'>.
# mypy error: Incompatible types in assignment (expression has type "M", variable has type "B")  [assignment]
# bb.x = B()
print(bb.x)
bb.x = C()
print(bb.x)
