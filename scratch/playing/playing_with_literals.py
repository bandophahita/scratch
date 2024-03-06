from __future__ import annotations
from typing import get_args, Literal, TypeAlias, Final, Type, TypeVar
# from enum import StrEnum  # only works in 3.11 or higher
from enum import Enum

T_foo = Literal["foo"]
T_bar = Literal["bar"]
T_valid_arguments: TypeAlias = T_foo | T_bar

# DRY
FOO: T_foo = get_args(T_foo)[0]
BAR: T_bar = get_args(T_bar)[0]



def func(argument: T_valid_arguments) -> None:
    ...



# VlanId = TypeVar("VlanId")
# Port = TypeVar("Port")

################################################################################
class VlanId(int): pass
class Port: pass

# reveal_type(VlanId)



################################################################################
# TRY 1

# Trunk = Literal["trunk"]
# TRUNK = "trunk"  # TRUNK type becomes Literal[“trunk”]
# NB, TRUNK: Trunk = “trunk” provides the exact same thing.
# Unallocated = Literal["unallocated"]
# UNALLOCATED = "unallocated"  # UNALLOCATED type becomes Literal[“unallocated”]
# PortVlanAllocation = VlanId | list[VlanId] | Trunk | Unallocated





# def get_init_port_value() -> VlanId | Trunk: 
#     rt: VlanId | Trunk
#     return rt
    
# def get_port_status(port: Port) -> PortVlanAllocation:
#     rt: PortVlanAllocation
#     return rt



################################################################################
# Try 2
# TRUNK: Final = "trunk"  # TRUNK type becomes Literal[“trunk”]


################################################################################
# Try 3

# PortVlanAllocation = VlanId | list[VlanId] | Type[TRUNK] | Type[UNALLOCATED]


################################################################################
# Try 4
# PortVlanAllocation = VlanId | list[VlanId] | Literal[TRUNK] | Literal[UNALLOCATED]


################################################################################
# Try 5
class NonVlanAlloc(Enum):
    TRUNK = "trunk"
    UNALLOCATED = "unallocated"


# PortVlanAllocation = NonVlanAlloc | VlanId | list[VlanId]
# def get_init_port_value() -> Literal[NonVlanAlloc.TRUNK] | VlanId: ...



################################################################################
# MY implementation

################################################################################
# DRY 



T_trunk = Literal["trunk"]
T_unalloc = Literal["unallocated"]

# TRUNK: T_trunk = "trunk"
# UNALLOCATED: T_unalloc = "unallocated"

TRUNK: T_trunk = get_args(T_trunk)[0]
UNALLOCATED: T_unalloc = get_args(T_unalloc)[0]


class Either(Enum):
    TRUNK = TRUNK
    UNALLOCATED = UNALLOCATED

class OnlyTrunk(Enum):
    TRUNK = TRUNK


# PortVlanAllocation = VlanId | list[VlanId] | T_trunk | T_unalloc
PortVlanAllocation = VlanId | list[VlanId] | Either


# def get_init_port_value() -> VlanId | T_trunk: 
#     rt: VlanId | T_trunk
#     return rt

# def get_init_port_value() -> NonVlanAlloc | T_trunk:
#     return NonVlanAlloc.UNALLOCATED
    # return "trunk"  # Incompatible return value type (got "Literal['trunk']", expected "Union[Literal[NonVlanAlloc.TRUNK], VlanId]")
    # return NonVlanAlloc.TRUNK  # OK
    # return 42  # Incompatible return value type (got "Literal[42]", expected "Union[Literal[NonVlanAlloc.TRUNK], VlanId]")
    # return VlanId(2345789789)  # OK

def get_port_status(port: Port) -> PortVlanAllocation:
    rt: PortVlanAllocation
    return rt




# def get_init_port_value() -> NonVlanAlloc.TRUNK | VlanId | list[VlanId]: ...
# def get_init_port_value() -> T_trunk | VlanId | list[VlanId]: ...




# def expected_from_port_value(arg: Literal["trunk"] | VlanId):


################################################################################
## OPTION 1
# using enum properly -- the function should return the Enum not the literal string
# def get_init_port_value() -> OnlyTrunk | VlanId:
#     if rt == 1:
#         return OnlyTrunk.TRUNK
#     else:
#         return VlanId()
# 
# def expected_from_port_value(arg: OnlyTrunk | VlanId):
#     return

################################################################################
# OPTION 2
def get_init_port_value() -> T_trunk | VlanId:
    ...
    # rt = 1
    # if rt == 1:
    #     return TRUNK
    # else:
    #     return VlanId()

def expected_from_port_value(arg: T_trunk | VlanId):
    return


rt = get_init_port_value()
# reveal_type(rt)
expected_from_port_value(rt)
