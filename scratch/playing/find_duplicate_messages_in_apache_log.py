#!/usr/bin/env python3
import re

file_name = "/Users/m.wilson/Downloads/logs/sms/send_sms_302.log"

with open(file_name, 'r') as fp:
    lines = fp.readlines()




seen = {}


for n, line in enumerate(lines):
    # print(f"{n} {line}")
    _, msg = re.split("^.*]", line)
    if msg in seen.keys():
        print(f"{n} has duplicate from {seen[msg]}")
        print(f"{msg}")
        seen[msg].append(n)
        continue
    seen[msg] = [n]

print()
