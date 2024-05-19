#!/usr/bin/python3

import sys

for line in sys.stdin:
    line = line.strip().split(",")
    if len(line) > 2:
        print(line[0], "L", line[1], sep="\t")
    else:
        print(line[1], "R", line[0], sep="\t")