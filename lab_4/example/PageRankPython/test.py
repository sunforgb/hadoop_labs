#!/usr/bin/python3
import sys


for line in sys.stdin:
    print(line.strip().split("\t"))

