#!/usr/bin/python3
import sys
import json

def prnt(product, result):
    for item, value in result.items():
        print(f"{product} {item}", value, sep="|")

lastToken = None
result = {}

for line in sys.stdin:
    token, value = line.strip().split("|")
    value = json.loads(value)
    if token != lastToken and lastToken is not None:
        prnt(lastToken, result)
        lastToken, result = token, value
    else:
        lastToken = token
        for key in value.keys():
            result[key] = result.get(key, 0) + value[key]
if lastToken is not None:
    prnt(lastToken, result)