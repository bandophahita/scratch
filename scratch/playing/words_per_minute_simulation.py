#!/usr/bin/env python3

WPM = 100
AVERAGE_WORD_LEN = 5

DELAY = .07


def get_delay(wpm):
    return 1 / ((wpm * AVERAGE_WORD_LEN) / 60)


def get_wpm(delay):
    return (60 * (1 / delay)) / AVERAGE_WORD_LEN 

slow = 50
med  = 100
fast = 200


print(f"WPM:   {slow:<3}   ==> delay: {get_delay(slow):.3f}  SLOW")
print(f"WPM:   {med:<3}   ==> delay: {get_delay(med):.3f}  MEDIUM")
print(f"WPM:   {fast:<3}   ==> delay: {get_delay(fast):.3f}  FAST")

print(f"delay: {DELAY:.3f} ==> WPM:   {get_wpm(DELAY):.0f}")

print()
