#!/usr/bin/python3

import sys
import json

for line in sys.stdin:
    line = line.strip().split(" ")
    for index, token in enumerate(line):
        dictionary = {}
        for joken in line[index:]:
            if token!=joken:
                dictionary[joken] = dictionary.get(joken, 0) + 1
        if dictionary.get(joken, None):
            print(token, json.dumps(dictionary),sep="|")