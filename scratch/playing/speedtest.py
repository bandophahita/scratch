#!/usr/bin/env python3

"""

"""
from functools import wraps, partial
import timeit

NUM = 10  # number of times to run the function


# DO NOT EDIT BETWEEN TRIPLE LINES
################################################################################
################################################################################
################################################################################
timers = []
def Benchmark(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        tx = timeit.Timer(partial(function, *args, **kwargs))
        timers.append([function, min(tx.repeat(5, NUM)), args, kwargs])
        return
    return wrapper

# in case you need a decorator with arguments
# class Benchmark(object):
#     def __init__(self, arg1=None):
#         self.arg1 = arg1
#
#     def __call__(self, function):
#         @wraps(function)
#         def wrapper(*args, **kwargs):
#             tx = timeit.Timer(lambda: function(*args, **kwargs))
#             timers.append([function, tx.timeit(NUM), args, kwargs])
#             return
#         return wrapper


def time_all():
    for func, speed, args, kwargs in sorted(timers, key=lambda x: x[1]):
        allargs = list(args)
        for key, val in kwargs.items():
            allargs.append(f"{key}={val}")
        arguments = ",".join(str(arg) for arg in allargs)
        fname = f"{func.__name__}({arguments})"
        print(f"{fname:<35} x {NUM}: ", speed)

################################################################################
################################################################################
################################################################################
### CREATE YOUR CODE SNIPPET FUNCTIONS HERE ###
### PUT THE Benchmark DECORATOR ABOVE EACH FUNCTION YOU WANT TO TIME ###



################################################################################
# depth_1 = []
# depth_2 = 0
import random
import bisect
n = 10000
a = list(range(n))
c = list(range(n))
random.shuffle(a)
random.shuffle(c)
d = []
for i,x in enumerate(a):
    y = c[i]
    d.append((x,y))




@Benchmark
def do_append_sort():
    b = []
    for i in d:
        b.append(i)
        b.sort(key=lambda i: i[0])

@Benchmark
def do_bisect():
    b = []
    for i in d:
        bisect.insort(b, i, key=lambda i: i[0])





### CALL EACH FUNCTION YOU WANT TO TIME.  THE DECORATOR WILL HANDLE THE REST ###


do_append_sort()
do_bisect()





################################################################################
if __name__ == "__main__":
    time_all()



