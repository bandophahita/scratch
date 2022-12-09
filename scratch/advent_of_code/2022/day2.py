#!/usr/bin/env python3
"""
Appreciative of your help yesterday, one Elf gives you an encrypted strategy guide (your 
puzzle input) that they say will be sure to help you win. "The first column is what your 
opponent is going to play: A for Rock, B for Paper, and C for Scissors. The second column--" 
Suddenly, the Elf is called away to help with someone's tent.

The second column, you reason, must be what you should play in response: X for Rock, Y 
for Paper, and Z for Scissors. Winning every time would be suspicious, so the responses 
must have been carefully chosen.

The winner of the whole tournament is the player with the highest score. Your total score 
is the sum of your scores for each round. The score for a single round is the score for 
the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for 
the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

Since you can't be sure if the Elf is trying to help you or trick you, you should calculate 
the score you would get if you were to follow the strategy guide.

For example, suppose you were given the following strategy guide:

A Y
B X
C Z

This strategy guide predicts and recommends the following:

    In the first round, your opponent will choose Rock (A), and you should choose Paper (Y). 
    This ends in a win for you with a score of 8 (2 because you chose Paper + 6 because you won).
    
    In the second round, your opponent will choose Paper (B), and you should choose Rock (X). 
    This ends in a loss for you with a score of 1 (1 + 0).
    
    The third round is a draw with both players choosing Scissors, giving you a score of 3 + 3 = 6.

In this example, if you were to follow the strategy guide, you would get a total score of 15 (8 + 1 + 6).

What would your total score be if everything goes exactly according to your strategy guide?
"""

class Base:
    val = 0
    def __repr__(self):
        return f"{self.val}"
    def __eq__(self, other):
        if self is other:
            return True
        elif type(self) != type(other):
            return False
        return self.val == other.val

    def __hash__(self):
        return hash(self.val)

    def __add__(self, other):
        return self.val + other.val


class Rock(Base):
    val = 1


class Paper(Base):
    val = 2


class Scissors(Base):
    val = 3


class Win(Base):
    val = 6


class Draw(Base):
    val = 3


class Lose(Base):
    val = 0


ROCK = Rock()
PAPER = Paper()
SCISSORS = Scissors()

WIN = Win()
DRAW = Draw()
LOSE = Lose()


def detect(val):
    d = {
        "A": ROCK,
        "B": PAPER,
        "C": SCISSORS,
        # "X": ROCK,
        # "Y": PAPER,
        # "Z": SCISSORS,
        "X": LOSE,
        "Y": DRAW,
        "Z": WIN,
    }
    return d[val]


def calc_win(them, you):
    if them == you:
        return DRAW

    victories = {
        ROCK: SCISSORS,
        PAPER: ROCK,
        SCISSORS: PAPER,
    } 
    if int(them == victories[you]):
        return WIN
    else:
        return LOSE

# assert calc_win(ROCK, PAPER) == WIN
# assert calc_win(ROCK, ROCK) == DRAW
# assert calc_win(ROCK, SCISSORS) == LOSE
# assert calc_win(PAPER, PAPER) == DRAW
# assert calc_win(PAPER, ROCK) == LOSE
# assert calc_win(PAPER, SCISSORS) == WIN
# assert calc_win(SCISSORS, SCISSORS) == DRAW
# assert calc_win(SCISSORS, ROCK) == WIN
# assert calc_win(SCISSORS, PAPER) == LOSE


def calc_need(them, need):
    if need == DRAW:
        return them

    victories = {
        ROCK: SCISSORS,
        PAPER: ROCK,
        SCISSORS: PAPER,
    }
    losses = {
        SCISSORS: ROCK,
        ROCK: PAPER, 
        PAPER: SCISSORS,
    }

    if need == WIN:
        return losses[them]
    elif need == LOSE:
        return victories[them]


assert calc_need(ROCK, WIN) == PAPER
assert calc_need(ROCK, DRAW) == ROCK
assert calc_need(ROCK, LOSE) == SCISSORS 
assert calc_need(PAPER, DRAW) == PAPER 
assert calc_need(PAPER, LOSE) == ROCK
assert calc_need(PAPER, WIN) == SCISSORS 
assert calc_need(SCISSORS, DRAW) == SCISSORS
assert calc_need(SCISSORS, WIN) == ROCK
assert calc_need(SCISSORS, LOSE) == PAPER


INPUT = """A Y
A Z
A X
B X
A Y
B Y
B Y
A X
A Z
A X
A X
A X
B X
B X
B X
B X
C Z
B Z
B Y
B X
A X
A Y
B X
B X
B X
B Z
B X
B X
B X
B Z
B Z
A X
A X
C X
B X
B X
B X
A X
B X
B X
A Z
B X
B X
B X
B Z
B X
A X
B X
B Z
B X
B X
B Z
A Z
B X
B X
B X
A X
C Z
A X
A X
C Y
A X
B X
B X
B X
A X
B X
B X
A X
C X
B Y
A Z
A Y
B Z
B Z
C X
B Y
A X
B Y
A Y
B X
C X
B X
B X
C X
B X
A X
B X
B X
A Y
A X
B X
B Z
A Z
B Z
B Y
A Y
B Z
B X
B X
B X
A Z
B X
B X
A X
A Y
B X
B Z
B X
B X
B Y
B X
C X
B Z
C X
B Z
B X
A Y
B X
A Z
C Y
B Z
B Y
B X
A X
A Y
A X
B Z
B Z
A Z
B X
B Z
B X
A Y
B Z
B X
B Z
C X
B X
B X
B X
B Z
B Y
C Z
A X
B Y
B X
B X
B Z
B X
B Z
B X
A X
B Z
B Z
B Z
B Y
B X
C Z
B X
B Y
A X
B X
B Z
A X
B X
B X
B Z
B X
B Z
B Y
B Y
B Z
A X
B X
B Y
A Y
A Y
C X
B Z
B X
B X
A Y
C Y
B X
A Z
A Y
B Z
B X
B X
B Z
A Y
B X
B Z
A Y
B Z
B X
B X
A X
B Z
A X
B X
B Z
A X
B X
A X
A X
B X
A Y
B Z
B X
B Y
B X
B X
A Y
A X
C X
A Z
B Y
B Z
C X
B X
B Z
B Z
B Z
B X
B X
C X
C X
C Y
A Z
B X
A X
A Z
A X
B Y
A Z
B Z
B X
B Y
B X
C Z
A Y
B X
A X
B Z
B Z
A Z
A X
A X
B X
B Y
B Y
B Z
B X
B Z
A X
B X
B X
A X
A Y
A Z
B Z
B X
B Z
B X
A X
C Z
B X
A Z
B X
B X
B Z
B X
B Z
B X
B X
A Z
B Z
B X
C X
B X
A X
B X
C X
B X
B X
B X
B X
B X
A X
A Z
A X
B Z
C Z
B X
A Z
C Y
B Z
B Z
B X
A Z
B X
A Z
B Y
B X
A X
B X
B X
B X
A Z
B X
C X
B Y
C X
B Y
B X
B X
B Z
A X
B X
A Y
A Y
A Y
A Y
A Y
B X
A X
B X
A Z
A Z
B Y
A Z
A Y
A X
B X
A Z
A X
A X
B Z
B Z
A Z
B Z
B X
B X
A X
B X
B X
B X
A X
B X
C Z
A Z
A X
A X
B X
B X
B X
B X
A X
A X
A X
B Y
B Y
B X
A X
A Y
A Y
B X
A X
B X
A X
A Z
B Z
B X
B X
A Y
C X
C X
A Y
B X
B Z
B X
B X
A Z
C X
C X
B X
B X
C X
B X
B X
B X
B Y
B X
A Y
B X
A Y
B Z
B X
B X
B X
B X
A X
B X
B X
B X
B X
B Y
B Y
B Z
A Y
B X
B Z
A X
B X
A X
A Y
B Y
B X
B X
C Z
B X
A Z
C Y
B Z
C Z
A X
B X
A X
A Z
A X
A X
A Y
B X
B X
B Y
A X
B Z
B Z
B X
B Y
C X
B X
B X
B X
A X
C X
A Y
B Z
B X
B Z
B Y
C Y
A X
C Z
A X
B X
A Y
B Z
C X
B Z
B X
A X
A Z
B X
C Y
A X
B X
B X
B Z
B Z
B X
A X
A X
B X
B Z
A X
A Z
A Z
A Y
A Z
B X
C Z
A Y
B X
B Z
B X
B X
B X
B Z
A X
B X
A X
B Y
B Y
B X
C Z
A X
A X
A X
B X
B X
B X
B X
A Z
B X
B X
B Y
A X
B Z
C X
A Y
B X
A Y
A Y
B X
C X
C X
B Z
B Z
B Z
B X
B Y
A Y
B Z
B X
C Z
B Z
A Z
A X
A Z
A X
B X
B Z
B X
B X
A Z
B Z
C Y
B Z
B X
B X
A X
A X
C X
B X
C Z
B Z
B X
A Y
B Z
B X
B X
A Z
A X
B X
A X
A X
A X
A Z
C Y
B X
B X
A X
B X
B Y
B Y
B X
B X
B X
C Z
B X
B X
C Z
B Z
A X
C Y
A X
A X
A X
A X
B X
A X
C Y
B Z
A X
B X
B Y
C X
B Z
A X
B X
B Y
B X
C Y
A X
B Z
B Y
B X
B X
B Z
B X
B Y
B Z
B X
C X
B Y
B X
B Z
B Z
B Z
B X
B X
B X
B Y
A Y
B X
B X
B X
B Z
B Y
C X
C X
C Z
B X
A X
B X
B Z
B Z
B Z
A Z
A Y
B X
A X
A Z
B Y
A X
B X
A Y
A X
B X
B Z
A X
A X
A Z
B X
B X
A X
B Y
B X
B Z
A Y
B X
A X
B X
B X
B X
A Y
B X
B X
B Z
C X
C Y
B X
A X
B Y
B X
B X
B Y
B X
B Z
B Y
C X
B Y
B X
C Y
A Z
C X
B X
B Z
A X
B X
B X
B X
B X
A Y
C Z
B X
B X
B Z
A Y
B X
B Y
A X
C X
B X
A Y
A X
B X
B X
B X
B Y
A X
C X
B X
A X
B X
B Z
C Z
A X
A X
B X
A X
C X
A X
B Z
B X
B X
B X
A Y
A Z
B X
C X
B Y
B Z
A Z
A Y
B Y
A Y
B X
B X
C X
B X
A X
B X
B Z
A Y
B Z
A X
B X
A Y
B X
B X
B X
B Z
B X
B X
A X
B X
B X
B X
B X
C X
A Y
A Z
B Z
A X
A Z
A X
B Z
B Z
B X
B X
B X
A X
B X
B Y
A X
B X
C X
A Z
B X
B X
C Z
B X
B Z
A Y
A X
A Y
A X
B X
B Y
B Z
B X
B X
B X
B Z
B Z
A X
A X
B X
B Z
A X
A Y
A Y
A X
B X
A Z
B X
A Y
B Z
A X
C X
B X
B X
A X
B X
C X
B Z
B X
B X
C X
A Y
B X
B X
B Z
B X
A Y
B Z
C Z
B Y
B X
A Y
B X
B X
B X
B X
C X
A Y
B X
B Z
B X
B X
C Z
A X
B X
A Y
A X
B X
B X
A X
A Z
C X
A X
A Y
A Y
B Z
A X
B Z
B X
B Y
A Z
A X
A X
A Y
C Z
B X
A Y
B Z
B X
B X
B Z
B X
A Z
C Z
B Z
A Z
B X
A X
B Z
A X
B X
B Z
B X
A X
B Y
A Z
A Z
B X
B Z
A Y
B Z
A Y
B X
C X
A Y
B Z
A X
B X
B X
C X
B Y
B Z
B Z
B X
A X
A X
B X
A X
C Y
A Y
A X
A Z
A X
A X
B X
B X
B X
B Y
C Y
A X
B X
B X
B X
B X
B X
C Y
A Z
B X
A X
A X
A Z
A Y
C X
A Z
B X
B X
B X
A X
B Z
B X
C Z
A Y
B X
A Y
B Y
B X
A Y
B Z
B X
B Z
B X
A Y
B Y
B Y
A X
B X
C Z
B Z
B Z
B X
A Z
C X
B Z
C Y
B X
A Y
A X
B X
A X
B Z
A Y
B Y
B Y
B X
C X
C X
A Y
A Z
B X
B X
B X
B X
C X
B X
C X
B X
B Z
A X
A X
B X
A Y
B Z
B X
A X
B X
B X
A Z
C X
B Z
C X
A X
B Z
C X
B X
B Z
A X
C X
A Y
A X
A X
A Y
B Y
B X
B X
B X
B Y
B X
A Y
B X
A X
B X
C X
B X
B X
B X
B X
B X
A X
C X
C Z
B X
B X
B Z
B Z
A X
B Y
B X
B X
A Y
B X
B Z
A X
A X
C X
B X
B X
C X
B X
B X
B X
A X
A X
C X
B X
B X
B Z
B Z
A Z
B X
A X
A X
B X
B Y
A X
B X
B X
A X
B X
B X
B X
B X
A Y
A X
B X
A X
B X
A Z
A Y
B X
B X
A Z
B Z
B X
B X
B X
B X
A X
B X
B X
B X
A Y
C Y
A X
B Z
A X
B X
B X
B X
B Y
C X
A X
B Z
B X
C X
A X
A X
A Y
B Z
B X
B X
B Z
C Z
B X
B Z
B X
A X
A Y
A Y
B Z
B X
C Y
B X
B Z
A Y
B Z
A Y
B Y
B X
C Z
B X
A X
A Z
B Z
C X
A Y
C X
A Y
B Y
B X
C X
A X
A Y
A Y
B X
A Z
A Z
A Z
B X
A Z
B Z
A X
B X
A Y
A Z
A X
B X
A Y
B X
B X
B Z
A X
B X
B Y
C Y
B Y
B X
C Y
A X
C Y
A Z
A Y
B Z
B X
A X
C X
B X
C Z
C Y
B Z
B X
C X
B Z
B X
C X
B Z
B Z
C X
B X
B Z
A X
A Y
C Y
B X
A Y
A Y
A Z
B X
B Z
A Y
B Y
A Z
B X
B Y
A Y
B Y
A X
A Y
B Z
A Y
B Z
B Z
B X
B X
C Z
A Y
A Y
B Y
B Z
B Z
A X
B X
A Y
C Z
B X
B Z
B X
B Z
B X
C X
A X
B Z
A X
B Z
C X
B X
A X
A X
A Y
B X
B Z
B X
A X
B Z
B Z
B Y
B Z
C Y
B X
B X
B X
A X
B X
C Z
B X
C Z
A X
B Y
B X
C Y
C X
B X
B X
B Z
B Z
B X
B X
B Z
B X
B Y
A X
B X
A X
C Z
B X
B Z
B X
B X
B X
A X
A X
A Y
B Z
C X
B X
C Y
A Y
B Y
B Y
A X
B Z
B X
A Y
B Z
B Z
A X
B Z
B Y
C X
C X
B X
B X
B Y
B Y
B Y
A X
B X
B X
A Y
B Z
A X
A Z
A Y
A Z
B Z
B Z
A Y
A X
A X
B X
B Z
A Y
B X
A Y
B X
B X
A Y
B X
B X
B Z
C X
A Y
B X
B X
C Y
B Y
B X
B X
B X
A X
B X
A Z
B X
A Z
B Z
A Y
B X
C X
B X
A X
A Z
B Z
B Z
B X
B X
C X
B X
B Z
B X
B Z
B X
B X
A Y
B X
B Y
B X
B X
B Y
B X
B Z
B X
B Z
A X
A Y
B Y
A X
B X
A X
B X
A X
A Y
B Y
B Y
B X
B X
B Z
A X
B X
A X
A X
A Y
B X
A Y
A X
A Y
B Y
B Z
B X
A X
B X
B X
A Y
A Z
B X
A Z
B X
B X
C Z
B Z
B Z
B Y
A Z
B Z
A Z
B Y
B X
C Z
A Z
B Z
A X
B X
B X
B X
C Y
C Z
B Z
C Z
B X
B X
B X
B X
B X
A X
A Z
B X
A X
B X
C Z
B Z
B X
A Z
A X
B X
A X
B X
A Y
B X
A X
A Y
C X
B X
C X
A Z
C Z
B X
C X
B Z
A X
B X
B X
B Z
A Y
A Z
B Z
B X
A X
C Y
B Z
B Z
B X
B X
A X
B X
A Y
B X
B Y
A Z
B X
B X
A Z
A X
B Y
B Z
B X
B X
C X
B Z
A X
B X
A Z
B X
B X
B X
B X
B X
B X
B Z
A X
B X
B X
B X
B X
B Z
B Z
A Y
B X
C Y
B Z
B Z
A Z
B Z
C Y
B X
B Y
A X
A X
A Z
B X
B Y
C X
B Z
B X
B X
B X
B Z
B X
B X
C Y
C X
A X
B X
B Y
B X
B X
A Y
A X
B X
A X
B X
A Z
B X
C Y
C Y
A Y
B Z
C Y
C Y
C X
C Y
C Z
C X
B X
B X
B X
B Y
B X
A Y
C Y
B X
B X
A Z
B X
B X
B X
C Z
B Y
A Z
C Z
B X
B Z
A X
B X
B Z
B X
B X
B Z
A Y
B Z
A X
A X
B X
B X
B X
B X
A Y
A Z
B X
B Z
B Z
B Z
B X
B X
B Y
A Y
B X
C Y
B Z
B Y
B Z
B X
C Y
B Z
A X
B X
A X
B Z
B Y
B X
B Z
C Y
A Y
B X
C Y
C Y
A X
A X
A X
A X
B X
B X
A Y
A Z
B Y
B Z
B X
B X
B X
B Y
B Y
A X
B Y
B X
B Z
B X
B Z
B X
A X
B X
B X
B Y
B X
B Z
B Z
B X
B X
B X
B X
B Z
B X
B Z
A Z
B X
B X
B X
B Y
A X
B Z
A X
C Y
B Y
B Z
C X
C X
B Z
B Z
C X
A X
B X
A X
B X
B X
A Z
B X
A Y
A X
A X
B Y
A Y
A Y
C X
A X
B X
B Y
B Y
A Y
A X
C Y
A Y
B Z
B X
B Y
B Z
A Y
A Y
B Z
A X
C X
A Z
B X
B X
B X
B X
A X
A Y
B X
B X
B Z
A Y
A Y
C Z
B Z
B Y
A Y
A X
C X
A Y
B X
C X
A X
A Z
B X
A X
B X
B Z
C X
B X
A Y
B X
B Z
B X
B X
B X
C X
B X
C Y
B Z
B Z
B X
B X
B Z
C X
B X
B X
A Z
B X
A Y
B X
B Y
B Z
A X
A Z
A X
B X
B Z
B Z
B X
A Y
B Z
B X
C Y
A X
A Y
A Y
B Z
B X
A X
A Y
C X
A Y
A X
B X
B X
A X
C X
B Z
A X
B Y
B X
A X
C Z
C X
B Z
A X
B X
B Y
B X
B X
A Y
B Y
A X
A X
A Z
B X
A Z
A X
B X
A X
B Z
A X
A X
A X
B X
A Y
B X
B Z
C Z
B X
A X
B X
C Z
B X
B Z
A X
C X
B X
B X
A X
B X
B Z
A X
C X
B Z
B X
B X
B X
B X
B X
A Y
C Y
B Z
C Z
B X
A X
A X
A Y
B X
B X
C Y
B X
C Z
A X
B X
A Y
B X
B X
A X
C X
B X
C Y
B X
C Y
A X
B X
B Y
C Y
B Z
B X
A X
B X
B X
B Y
A X
B X
A Z
A Y
A X
A Z
B X
A Y
C Y
B Z
C Y
B X
B X
A Y
C X
C Z
B Z
B X
B X
A Y
B X
B Y
A X
A X
B X
B Z
A Y
A Y
A Y
B X
B X
C X
B Y
B X
A Y
A X
C X
B X
B Z
A Z
B Z
A Y
B Z
A X
B X
B X
B X
B Y
C Z
B Y
B X
A X
B X
A X
A Z
B Z
B X
B X
B X
C X
C Z
B Z
A X
B X
B X
A Y
B X
B Z
A X
B X
A X
A X
C Y
B Z
A X
A X
B Y
B X
A Y
B Y
C X
B Z
A X
A Z
B X
B X
A X
B X
A Y
A X
C X
B X
A X
C X
B Z
B X
A X
A Z
B X
B X
B Z
B X
B Z
C X
B Z
A X
A X
B X
B X
B Y
B X
B X
B Z
A Y
A X
C X
A X
B X
A Z
B X
A X
A X
B X
A X
B X
B X
A Y
A Y
A X
B X
B Z
C X
A X
B X
B X
B Z
B X
B X
A Z
B Z
B Z
B X
B Y
C X
B Z
A X
B X
B X
B Z
A Y
B X
B X
B X
B X
B X
C X
C Y
A Z
B X
C Y
A Y
C X
B X
B X
B Z
B X
B X
A X
A X
A Z
C Y
B X
B X
A Y
B Z
B Z
A X
A Z
C X
B X
B X
B X
B X
A X
C X
B Z
B X
A X
A X
A Y
B X
B X
A Z
C X
B X
A X
B Z
A X
B Y
B X
B X
A Y
C Y
B Z
A X
A Z
A Y
C Y
B X
C X
B X
B Y
B X
B Z
A X
C Y
A Y
B Z
B X
A X
C Z
B X
B Z
A X
C Y
B Y
B X
B X
A Y
B X
B Z
B X
B Z
B X
B Z
A Y
A X
B X
B X
A Y
C X
A X
C X
B X
B X
B X
A X
B Z
B Z
C Z
B Z
A X
A X
B Z
C X
A Z
A Y
B Y
B X
A X
A Y
A X
A Z
B X
B X
B Z
B Z
A Y
B X
B X
B Z
B X
A X
C X
B X
B X
B Y
A X
B X
B X
C Z
B X
B Z
B X
B Y
B X
B X
A X
A Y
A Y
B X
A X
A Z
B Z
B Z
B X
B X
B Z
B X
A Z
B X
A X
C X
B X
B X
B Z
B X
A X
B Z
B X
B Z
C Y
B X
B X
B X
B Z
C X
B X
B X
B Y
B Z
B X
C Y
A Y
C X
A X
B X
A X
B Z
B X
B X
A Y
C Z
A X
B Y
A X
B Z
B X
C Z
B X
C Z
A X
B X
A X
B X
A Y
B X
B Z
B X
B Z
C Z
B X
B X
A Z
A X
A X
B X
A X
B X
B X
B X
B X
A X
B Z
B X
A X
B Z
C Y
C Z
A X
B X
B X
B Z
B Z
A X
A Y
B X
A Y
B X
B X
C X
B Z
B Y
B Z
B Z
A Y
C X
B Y
B X
B X
A Z
B X
B Y
C X
B Y
C Y
B X
B X
C Y
A Z
C X
B X
C X
A Y
B X
C Z
B Z
B X
B Y
A Y
A X
B X
C Y
C X
A X
B X
B X
A X
B X
B X
C X
C Y
A Z
C X
A X
C X
B X
A Y
B X
A Y
C X
B X
C Z
C X
B Z
B X
B X
A X
A X
A Y
B Y
B Y
A Y
C Z
A Y
A X
B Z
B X
B X
C X
B X
C X
A Y
B Z
B X
A Y
A Y
C X
A Y
B Z
B Z
A X
B X
A Y
B Y
B X
A Z
B X
B X
B Z
C X
B X
C X
B X
B X
C X
A X
A Y
B X
A Y
C Z
C X
A Z
B X
B X
B X
A X
B X
B Y
B X
B Z
B X
A Y
B X
B X
B X
B X
B Y
B Y
B Z
C X
A Y
C X
B Y
B X
B Y
B X
A X
B Z
B Z
B X
A Z
C X
A X
B Z
B Y
A Y
B X
B X
B X
A X
B X
A Y
A X
B X
B Z
B X
A X
A Y
B X
B X
A X
B Z
A Z
A X
A Y
C X
A Z
B X
B X
A X
B Z
B Z
A X
A Y
B X
B Z
B X
A Y
B Y
A Y
B X
B X
A X
B X
A X
B X
C Z
A X
B X
C Z
A X
A X
B X
A X
A X
C Z
B Z
B X
B Z
A X
B Z
B X
B X
B X
A Z
B X
B X
B Z
A X
A Y
B X
A X
C X
A Y
A X
B X
B X
B Y
A Y
B X
A Y
A Z
B Z
B Z
B Z
B X
B X
A Y
A Z
B X
B X
B X
B X
B X
A Z
A Z
B X
B X
B X
B X
A X
B X
A X
B X
B Z
C X
A X
B X
C Z
B X
B X
B X
A X
A Z
B Z
C X
A X
B X
C X
B X
A X
C Z
A Z
A Y
B X
C X
B X
C X
B X
B Y
B Z
A X
B X
B X
A X
A Z
B Z
"""


def part1():
    their_points = 0
    your_points = 0
    
    for line in INPUT.splitlines():
        them_raw, you_raw = line.split()
        them = detect(them_raw)
        you = detect(you_raw)
        your_outcome = calc_win(them, you)
        their_outcome = calc_win(you, them)
        
        their_rnd_pts = them + their_outcome
        your_rnd_pts = you + your_outcome
        
        their_points += their_rnd_pts
        your_points += your_rnd_pts
    
    print(f"{their_points=} {your_points=}")
# part1()

def part2():
    your_points = 0
    for line in INPUT.splitlines():
        them_raw, need_raw = line.split()
        them = detect(them_raw)
        need = detect(need_raw)
        you = calc_need(them, need)
        your_rnd_pts = you + need
        your_points += your_rnd_pts
    print(f"{your_points=}")
part2()
print()
