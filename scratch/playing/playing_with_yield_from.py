
import asyncio

# generators have throw and send methods


def print_count(n):
    yield "Hello World\n"
    yield "\n"
    yield "Look at me count to %d\n" % n
    for i in range(n):
        yield " %d\n" % i
    yield "I'm done!\n"

# out = print_count(5)
# print("".join(out))


def reader():
    """A generator that fakes a read from a file, socket, etc."""
    for i in range(4):
        yield f'<< {i}'

def reader_wrapper(g):
    for v in g:
        yield v

# wrap = reader_wrapper(reader())
# for i in wrap:
#     print(i)


# @coroutine
# def null():
#     while True: 
#         item = (yield)
# 
# 
# @coroutine
# async def grep(pattern,target):
#     while True:
#         line = (yield)
#         if pattern in line:
#             target.send(line)
# 
# asyncio.run(grep('*',))


def grep2(pattern):
    print("Looking for %s" % pattern)
    while True:
        line = (yield)
        if pattern in line:
            print(line)

# g = grep2("python")
# next(g)



# def writer():
#     """A coroutine that writes data *sent* to it to fd, socket, etc."""
#     while True:
#         w = (yield)
#         print('>> ', w)


class SpamException(Exception):
    pass

def writer():
    while True:
        try:
            w = yield
        except SpamException:
            print('***')
        else:
            print('>> ', w)



def writer2():
    try:
        w = (yield)
    except SpamException:
        print('***')
    else:
        print('>> ', w)

# def writer_wrapper(coro):
#     coro.send(None)  # prime the coro
#     while True:
#         try:
#             x = (yield)  # Capture the value that's sent
#             coro.send(x)  # and pass it to the writer
#         except StopIteration:
#             pass

# def writer_wrapper(coro):
#     """Works. Manually catches exceptions and throws them"""
#     coro.send(None)  # prime the coro
#     while True:
#         try:
#             try:
#                 x = (yield)
#             except Exception as e:   # This catches the SpamException
#                 coro.throw(e)
#             else:
#                 coro.send(x)
#         except StopIteration:
#             pass

# this replaces the above
def writer_wrapper(coro):
    yield from coro




# in order to accomplish this block of code, the writer generator needs be suspended
# after each send
w = writer()
wrap = writer_wrapper(w)
wrap.send(None)  # "prime" the coroutine
for i in [0, 1, 2, 'spam', 4]:
    if i == 'spam':
        wrap.throw(SpamException)
    else:
        wrap.send(i)


