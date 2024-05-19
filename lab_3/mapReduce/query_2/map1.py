#!/usr/bin/python3

import sys

for line in sys.stdin:
    line = line.strip().split(",")
    if len(line) > 3:
        print(line[1], "L", line[2], sep="\t")
    else:
        print(line[0], "R", line[1], sep="\t")