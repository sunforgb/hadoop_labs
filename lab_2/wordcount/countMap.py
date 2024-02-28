#!/usr/bin/python3

import sys

for line in sys.stdin:
    for token in line.strip().split(" "):
        if token: print(token,1,sep="\t")