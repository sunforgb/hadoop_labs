#!/usr/bin/python3

import sys

for line in sys.stdin:
    line = line.strip().split(" ")
    for index, token in enumerate(line):
        for joken in line[index:]:
            if token and joken and token!=joken: print(f"{token} {joken}",1,sep="|")