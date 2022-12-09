#!/usr/bin/env python3

from queue import LifoQueue
import re

START = """
[J]             [F] [M]            
[Z] [F]     [G] [Q] [F]            
[G] [P]     [H] [Z] [S] [Q]        
[V] [W] [Z] [P] [D] [G] [P]        
[T] [D] [S] [Z] [N] [W] [B] [N]    
[D] [M] [R] [J] [J] [P] [V] [P] [J]
[B] [R] [C] [T] [C] [V] [C] [B] [P]
[N] [S] [V] [R] [T] [N] [G] [Z] [W]
 1   2   3   4   5   6   7   8   9 
"""

START2 = """
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 
"""

INPUT2 = """move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""

INPUT = """move 2 from 4 to 6
move 1 from 9 to 5
move 3 from 2 to 4
move 8 from 4 to 7
move 2 from 9 to 7
move 3 from 8 to 3
move 2 from 1 to 2
move 5 from 7 to 9
move 1 from 9 to 4
move 1 from 8 to 3
move 1 from 3 to 4
move 2 from 4 to 9
move 7 from 3 to 5
move 6 from 1 to 8
move 11 from 7 to 9
move 12 from 5 to 3
move 6 from 6 to 9
move 3 from 3 to 8
move 4 from 2 to 7
move 3 from 5 to 7
move 1 from 5 to 7
move 2 from 2 to 5
move 1 from 5 to 2
move 5 from 8 to 9
move 7 from 7 to 2
move 3 from 8 to 7
move 1 from 8 to 9
move 4 from 3 to 6
move 1 from 5 to 1
move 9 from 9 to 6
move 7 from 9 to 6
move 20 from 6 to 5
move 12 from 9 to 8
move 5 from 5 to 1
move 3 from 7 to 4
move 6 from 2 to 7
move 2 from 3 to 1
move 4 from 3 to 8
move 1 from 4 to 1
move 7 from 7 to 5
move 4 from 8 to 2
move 3 from 6 to 2
move 3 from 2 to 9
move 4 from 1 to 7
move 2 from 1 to 2
move 3 from 9 to 5
move 11 from 8 to 5
move 1 from 6 to 9
move 1 from 8 to 5
move 1 from 1 to 2
move 24 from 5 to 4
move 2 from 1 to 6
move 11 from 5 to 4
move 2 from 7 to 9
move 1 from 6 to 2
move 4 from 2 to 1
move 28 from 4 to 2
move 1 from 7 to 8
move 9 from 2 to 5
move 2 from 9 to 6
move 4 from 4 to 2
move 1 from 7 to 4
move 3 from 4 to 7
move 1 from 6 to 9
move 21 from 2 to 3
move 3 from 1 to 6
move 5 from 6 to 2
move 7 from 2 to 3
move 1 from 9 to 3
move 1 from 8 to 4
move 1 from 7 to 8
move 3 from 5 to 8
move 1 from 1 to 7
move 2 from 7 to 9
move 2 from 8 to 4
move 1 from 9 to 2
move 1 from 8 to 6
move 11 from 3 to 4
move 1 from 7 to 8
move 6 from 5 to 9
move 2 from 8 to 7
move 1 from 6 to 5
move 7 from 3 to 8
move 9 from 3 to 6
move 1 from 8 to 3
move 1 from 7 to 4
move 2 from 3 to 5
move 4 from 5 to 7
move 4 from 6 to 8
move 2 from 7 to 9
move 11 from 4 to 2
move 1 from 4 to 2
move 6 from 8 to 9
move 1 from 7 to 1
move 1 from 3 to 7
move 3 from 7 to 8
move 6 from 8 to 9
move 6 from 4 to 8
move 18 from 9 to 3
move 1 from 5 to 8
move 5 from 6 to 5
move 6 from 8 to 1
move 3 from 5 to 4
move 1 from 9 to 8
move 3 from 4 to 8
move 15 from 3 to 6
move 2 from 5 to 9
move 3 from 3 to 1
move 9 from 6 to 4
move 2 from 1 to 5
move 2 from 5 to 8
move 6 from 4 to 2
move 6 from 1 to 6
move 3 from 4 to 6
move 6 from 9 to 1
move 4 from 2 to 1
move 7 from 8 to 1
move 1 from 6 to 7
move 17 from 1 to 5
move 1 from 7 to 1
move 5 from 2 to 1
move 1 from 8 to 6
move 11 from 6 to 4
move 2 from 2 to 3
move 3 from 1 to 8
move 7 from 2 to 5
move 4 from 6 to 7
move 4 from 1 to 5
move 15 from 5 to 9
move 2 from 3 to 7
move 2 from 8 to 2
move 1 from 1 to 9
move 6 from 2 to 6
move 7 from 5 to 6
move 5 from 7 to 3
move 1 from 6 to 1
move 2 from 3 to 4
move 1 from 3 to 4
move 5 from 6 to 4
move 14 from 9 to 2
move 1 from 8 to 9
move 1 from 7 to 8
move 1 from 9 to 6
move 2 from 9 to 5
move 1 from 1 to 2
move 7 from 6 to 9
move 1 from 3 to 4
move 8 from 5 to 2
move 1 from 6 to 7
move 1 from 7 to 4
move 1 from 8 to 4
move 1 from 3 to 9
move 7 from 9 to 5
move 1 from 9 to 1
move 6 from 5 to 1
move 8 from 2 to 4
move 1 from 5 to 6
move 1 from 6 to 7
move 1 from 7 to 9
move 7 from 2 to 9
move 1 from 9 to 4
move 3 from 9 to 1
move 1 from 9 to 6
move 11 from 2 to 8
move 9 from 1 to 8
move 1 from 6 to 4
move 1 from 1 to 9
move 12 from 4 to 2
move 4 from 9 to 3
move 3 from 4 to 6
move 9 from 8 to 6
move 12 from 4 to 9
move 8 from 6 to 3
move 8 from 2 to 7
move 11 from 3 to 4
move 2 from 2 to 7
move 2 from 6 to 1
move 1 from 2 to 3
move 2 from 6 to 2
move 3 from 2 to 6
move 2 from 1 to 6
move 1 from 6 to 1
move 1 from 6 to 4
move 2 from 6 to 3
move 1 from 6 to 5
move 4 from 3 to 8
move 12 from 4 to 5
move 5 from 9 to 7
move 3 from 8 to 7
move 1 from 9 to 1
move 3 from 8 to 2
move 13 from 5 to 6
move 1 from 2 to 9
move 13 from 6 to 7
move 7 from 9 to 6
move 2 from 4 to 6
move 1 from 8 to 6
move 1 from 1 to 6
move 1 from 2 to 9
move 1 from 2 to 3
move 12 from 7 to 9
move 7 from 8 to 4
move 1 from 1 to 3
move 2 from 7 to 9
move 15 from 7 to 4
move 8 from 6 to 3
move 1 from 8 to 9
move 1 from 7 to 2
move 10 from 3 to 5
move 6 from 5 to 9
move 1 from 2 to 8
move 1 from 5 to 8
move 2 from 8 to 9
move 10 from 4 to 9
move 20 from 9 to 6
move 1 from 7 to 6
move 4 from 9 to 3
move 1 from 5 to 9
move 4 from 4 to 9
move 8 from 9 to 7
move 2 from 5 to 1
move 7 from 4 to 3
move 8 from 3 to 2
move 6 from 9 to 8
move 1 from 3 to 7
move 1 from 3 to 1
move 7 from 7 to 8
move 13 from 8 to 3
move 2 from 2 to 8
move 1 from 8 to 2
move 1 from 4 to 1
move 1 from 1 to 8
move 2 from 8 to 2
move 24 from 6 to 2
move 2 from 7 to 8
move 5 from 3 to 4
move 25 from 2 to 6
move 5 from 4 to 9
move 2 from 8 to 7
move 2 from 7 to 3
move 4 from 6 to 2
move 2 from 6 to 4
move 9 from 2 to 3
move 11 from 3 to 7
move 10 from 7 to 8
move 1 from 7 to 9
move 3 from 2 to 4
move 8 from 8 to 2
move 1 from 2 to 6
move 2 from 4 to 1
move 1 from 8 to 2
move 1 from 6 to 9
move 1 from 8 to 3
move 6 from 9 to 7
move 2 from 9 to 1
move 9 from 6 to 8
move 7 from 2 to 3
move 7 from 8 to 2
move 10 from 6 to 8
move 7 from 1 to 2
move 9 from 3 to 2
move 5 from 3 to 8
move 4 from 7 to 2
move 2 from 3 to 2
move 12 from 2 to 3
move 6 from 4 to 2
move 1 from 7 to 6
move 5 from 3 to 5
move 16 from 8 to 4
move 12 from 2 to 7
move 5 from 5 to 7
move 1 from 8 to 3
move 1 from 6 to 4
move 17 from 7 to 4
move 1 from 7 to 1
move 1 from 1 to 9
move 1 from 9 to 5
move 11 from 4 to 9
move 10 from 2 to 3
move 1 from 5 to 4
move 1 from 9 to 2
move 2 from 2 to 1
move 1 from 2 to 3
move 23 from 4 to 5
move 7 from 9 to 7
move 3 from 9 to 1
move 20 from 5 to 6
move 3 from 5 to 8
move 1 from 4 to 1
move 2 from 8 to 3
move 4 from 6 to 4
move 7 from 7 to 2
move 1 from 8 to 4
move 19 from 3 to 9
move 5 from 1 to 7
move 7 from 2 to 6
move 3 from 7 to 5
move 2 from 3 to 4
move 1 from 5 to 4
move 1 from 1 to 4
move 1 from 7 to 6
move 13 from 6 to 7
move 6 from 9 to 3
move 1 from 3 to 5
move 2 from 3 to 4
move 2 from 6 to 2
move 3 from 4 to 3
move 8 from 9 to 1
move 2 from 2 to 1
move 8 from 6 to 7
move 2 from 9 to 4
move 20 from 7 to 1
move 2 from 7 to 5
move 2 from 5 to 1
move 8 from 1 to 8
move 8 from 8 to 6
move 1 from 6 to 9
move 8 from 6 to 1
move 1 from 5 to 3
move 7 from 3 to 2
move 1 from 5 to 2
move 2 from 9 to 7
move 1 from 5 to 8
move 18 from 1 to 4
move 1 from 8 to 9
move 3 from 2 to 3
move 2 from 7 to 4
move 5 from 2 to 4
move 3 from 3 to 8
move 8 from 1 to 7
move 2 from 9 to 2
move 32 from 4 to 5
move 1 from 9 to 7
move 1 from 2 to 1
move 6 from 1 to 6
move 1 from 2 to 4
move 3 from 8 to 1
move 3 from 6 to 5
move 1 from 3 to 6
move 2 from 1 to 9
move 4 from 4 to 7
move 31 from 5 to 4
move 4 from 5 to 6
move 1 from 6 to 1
move 7 from 6 to 5
move 1 from 9 to 4
move 19 from 4 to 2
move 1 from 5 to 9
move 5 from 5 to 6
move 3 from 4 to 2
move 2 from 7 to 1
move 4 from 7 to 8
move 3 from 8 to 6
move 2 from 6 to 7
move 6 from 7 to 8
move 3 from 1 to 5
move 4 from 5 to 9
move 15 from 2 to 1
move 4 from 6 to 4
move 2 from 6 to 3
move 1 from 3 to 7
move 4 from 1 to 2
move 1 from 3 to 4
move 2 from 7 to 4
move 5 from 9 to 3
move 2 from 7 to 3
move 16 from 4 to 8
move 8 from 8 to 5
move 2 from 1 to 5
move 1 from 9 to 6
move 1 from 6 to 5
move 7 from 5 to 9
move 3 from 1 to 8
move 1 from 8 to 4
move 8 from 2 to 7
move 3 from 1 to 3
move 1 from 3 to 9
move 2 from 4 to 2
move 7 from 8 to 5
move 7 from 9 to 1
move 6 from 3 to 5
move 6 from 7 to 4
move 3 from 4 to 1
move 3 from 2 to 5
move 1 from 7 to 8
move 1 from 7 to 5
move 1 from 9 to 8
move 2 from 2 to 4
move 15 from 1 to 6
move 8 from 5 to 9
move 3 from 3 to 4
move 4 from 4 to 3
move 1 from 9 to 7
move 6 from 9 to 4
move 1 from 9 to 2
move 6 from 4 to 9
move 2 from 4 to 6
move 5 from 6 to 9
move 1 from 3 to 1
move 8 from 6 to 8
move 12 from 5 to 3
move 1 from 5 to 3
move 1 from 3 to 8
move 4 from 6 to 1
move 11 from 3 to 8
move 1 from 2 to 1
move 23 from 8 to 2
move 3 from 1 to 2
move 1 from 1 to 9
move 2 from 2 to 3
move 6 from 3 to 6
move 1 from 7 to 6
move 1 from 4 to 7
move 1 from 4 to 3
move 1 from 7 to 3
move 4 from 8 to 4
move 2 from 1 to 8
move 3 from 8 to 1
move 4 from 6 to 2
move 7 from 9 to 1
move 1 from 9 to 6
move 2 from 2 to 3
move 3 from 9 to 4
move 1 from 9 to 3
move 10 from 2 to 8
move 16 from 2 to 5
move 2 from 3 to 6
move 6 from 1 to 8
move 1 from 1 to 5
move 8 from 8 to 5
move 11 from 5 to 9
move 2 from 1 to 8
move 1 from 1 to 8
move 4 from 4 to 6
move 3 from 3 to 9
move 14 from 9 to 3
move 15 from 8 to 5
move 9 from 5 to 4
move 7 from 6 to 1
move 1 from 6 to 3
move 4 from 4 to 7
move 2 from 6 to 2
move 4 from 7 to 4
move 4 from 1 to 4
move 10 from 4 to 3
move 14 from 3 to 6
move 5 from 4 to 1
move 6 from 5 to 7
move 1 from 2 to 6
move 3 from 7 to 2
move 2 from 2 to 3
move 3 from 7 to 8
move 2 from 8 to 2
move 2 from 2 to 7
move 6 from 6 to 2
move 1 from 8 to 7
move 8 from 2 to 7
move 1 from 4 to 1
move 5 from 5 to 3
move 3 from 3 to 2
move 5 from 1 to 3
move 7 from 5 to 8
move 6 from 6 to 3
move 1 from 5 to 9
move 10 from 7 to 9
move 26 from 3 to 4
move 1 from 5 to 1
move 6 from 8 to 2
move 9 from 2 to 9
move 1 from 7 to 5
move 1 from 8 to 5
move 2 from 6 to 2
move 20 from 9 to 6
move 1 from 1 to 6
move 1 from 4 to 2
move 1 from 5 to 8
move 1 from 5 to 7
move 3 from 1 to 3
move 1 from 3 to 6
move 12 from 4 to 8
move 11 from 4 to 5
move 1 from 7 to 5
move 1 from 2 to 8
move 1 from 1 to 8
move 2 from 2 to 5
move 8 from 6 to 2
move 5 from 6 to 4
move 2 from 5 to 3
move 12 from 8 to 4
move 5 from 2 to 6
move 3 from 8 to 1
move 11 from 6 to 8
move 10 from 4 to 6
move 5 from 4 to 6
move 12 from 6 to 5
move 22 from 5 to 6
move 3 from 6 to 5
move 3 from 8 to 5
move 1 from 3 to 8
move 4 from 8 to 1
move 6 from 1 to 7
move 5 from 6 to 9
"""

pat = re.compile(r'move (\d+) from (\d+) to (\d+)')


class Column(LifoQueue):
    def __repr__(self):
        return f"{self.queue}"


class Columns:
    def __init__(self, number):
        self.columns = {}
        numbers = list(range(1,number+1))
        for n in numbers:
            self.columns[n] = Column()

    def __getitem__(self, item):
        return self.columns[item]

    def move(self, from_n, to_n):
        #fetch columns before doing actions in case bad index was given.
        from_col = self.columns[from_n]
        to_col = self.columns[to_n]

        box = from_col.get()
        to_col.put(box)

    def move_many(self, moves, from_n, to_n):
        for x in range(moves):
            self.move(from_n, to_n)
    
    def move_many_9001(self, moves, from_n, to_n):
        from_col = self.columns[from_n]
        to_col = self.columns[to_n]
        
        temp_holding = []
        for n in range(moves):
            temp_holding.append(from_col.get())
        temp_holding.reverse()
        for box in temp_holding:
            to_col.put(box)
        

    def top_boxes(self):
        l = []
        for n, column in self.columns.items():
            l.append(column.queue[-1])
        return l


def remove_box(s):
    return s.strip("[").strip("] ").strip("]")


def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


def create_columns():
    lines = START.splitlines()
    
    lines.pop(0)  # because we left the triple quoted string first line blank
    vals = lines.pop(-1).split()
    numbers = [int(n) for n in vals]
    
    # columns = {}
    # for n in numbers:
    #     columns[n] = Column()
    columns = Columns(len(numbers))
    
    lines.reverse()
    for line in lines:
        chunks = list(divide_chunks(line, 4))
        boxes = [remove_box(raw) for raw in chunks]
        for i,box in enumerate(boxes, start=1):
            if not box:
                continue
            columns[i].put(box)
    return columns





def part1():
    """
    The expedition can depart as soon as the final supplies have been unloaded from 
    the ships. Supplies are stored in stacks of marked crates, but because the needed 
    supplies are buried under many other crates, the crates need to be rearranged.

    The ship has a giant cargo crane capable of moving crates between stacks. To ensure 
    none of the crates get crushed or fall over, the crane operator will rearrange them 
    in a series of carefully-planned steps. After the crates are rearranged, the desired 
    crates will be at the top of each stack.
    
    The Elves don't want to interrupt the crane operator during this delicate procedure, 
    but they forgot to ask her which crate will end up where, and they want to be ready 
    to unload them as soon as possible so they can embark.
    
    They do, however, have a drawing of the starting stacks of crates and the 
    rearrangement procedure (your puzzle input). For example:
    
        [D]    
    [N] [C]    
    [Z] [M] [P]
     1   2   3 
    
    move 1 from 2 to 1
    move 3 from 1 to 3
    move 2 from 2 to 1
    move 1 from 1 to 2
    
    In this example, there are three stacks of crates. Stack 1 contains two crates: crate 
    Z is on the bottom, and crate N is on top. Stack 2 contains three crates; from bottom 
    to top, they are crates M, C, and D. Finally, stack 3 contains a single crate, P.
    
    Then, the rearrangement procedure is given. In each step of the procedure, a quantity 
    of crates is moved from one stack to a different stack. In the first step of the 
    above rearrangement procedure, one crate is moved from stack 2 to stack 1, resulting 
    in this configuration:
    
    [D]        
    [N] [C]    
    [Z] [M] [P]
     1   2   3 
    
    In the second step, three crates are moved from stack 1 to stack 3. Crates are moved 
    one at a time, so the first crate to be moved (D) ends up below the second and third 
    crates:
    
            [Z]
            [N]
        [C] [D]
        [M] [P]
     1   2   3
    
    Then, both crates are moved from stack 2 to stack 1. Again, because crates are moved 
    one at a time, crate C ends up below crate M:
    
            [Z]
            [N]
    [M]     [D]
    [C]     [P]
     1   2   3
    
    Finally, one crate is moved from stack 1 to stack 2:
    
            [Z]
            [N]
            [D]
    [C] [M] [P]
     1   2   3
    
    The Elves just need to know which crate will end up on top of each stack; in this 
    example, the top crates are C in stack 1, M in stack 2, and Z in stack 3, 
    so you should combine these together and give the Elves the message CMZ.
    
    After the rearrangement procedure completes, what crate ends up on top of each stack?
    """
    columns = create_columns()
    for line in INPUT.splitlines():
        match = pat.search(line)
        vals = [int(val) for val in match.groups()]
        columns.move_many(*vals)
    print(f"{''.join(columns.top_boxes())}")
    return


def part2():
    """
    As you watch the crane operator expertly rearrange the crates, you notice the 
    process isn't following your prediction.

    Some mud was covering the writing on the side of the crane, and you quickly wipe 
    it away. The crane isn't a CrateMover 9000 - it's a CrateMover 9001.
    
    The CrateMover 9001 is notable for many new and exciting features: air 
    conditioning, leather seats, an extra cup holder, and the ability to pick up and 
    move multiple crates at once.
    
    Again considering the example above, the crates begin in the same configuration:
    
        [D]    
    [N] [C]    
    [Z] [M] [P]
     1   2   3 
    
    Moving a single crate from stack 2 to stack 1 behaves the same as before:
    
    [D]        
    [N] [C]    
    [Z] [M] [P]
     1   2   3 
    
    However, the action of moving three crates from stack 1 to stack 3 means that 
    those three moved crates stay in the same order, resulting in this new 
    configuration:
    
            [D]
            [N]
        [C] [Z]
        [M] [P]
     1   2   3
    
    Next, as both crates are moved from stack 2 to stack 1, they retain their order 
    as well:
    
            [D]
            [N]
    [C]     [Z]
    [M]     [P]
     1   2   3
    
    Finally, a single crate is still moved from stack 1 to stack 2, but now it's 
    crate C that gets moved:
    
            [D]
            [N]
            [Z]
    [M] [C] [P]
     1   2   3
    
    In this example, the CrateMover 9001 has put the crates in a totally different 
    order: MCD.
    
    Before the rearrangement process finishes, update your simulation so that the 
    Elves know where they should stand to be ready to unload the final supplies. 
    After the rearrangement procedure completes, what crate ends up on top of each 
    stack?
    """
    columns = create_columns()
    for line in INPUT.splitlines():
        match = pat.search(line)
        vals = [int(val) for val in match.groups()]
        columns.move_many_9001(*vals)
    print(f"{''.join(columns.top_boxes())}")


part1()
part2()
