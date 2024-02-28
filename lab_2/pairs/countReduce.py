#!/usr/bin/python3
import sys

lastToken = None
result = 0
# Полагаемся на Shuffle and Sort, что он отправит на Reducer все совпадающие token.
for line in sys.stdin:
    line = line.strip().split("|")
    (token, value) = line[0], line[1]
    if lastToken and lastToken != token:
        print(lastToken, result, sep="|")
        lastToken, result = token, int(value)
    else:
        lastToken, result= token, result +int(value)

if lastToken:
    print(lastToken, result, sep="|")