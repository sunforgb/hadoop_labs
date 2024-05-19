#!/usr/bin/python3
import sys

kek = {}
lastToken = None
for line in sys.stdin:
    line = line.strip().split("\t")
    token  = line[0]
    if line[1] not in kek:
        kek[line[1]] = []
    if token != lastToken and lastToken is not None:
        for item in kek['R']:
            for elem in kek['L']:
                if elem[0] == item[0]: 
                    print(item[1], elem[1], sep=",")
        lastToken, kek['R'], kek['L'] = token, [], []     
        kek[line[1]].append(list(item for item in line if item != line[1]))
    else:
        lastToken = token
        kek[line[1]].append(list(item for item in line if item != line[1]))

if lastToken is not None:
    for item in kek['R']:
        for elem in kek['L']:
            if elem[0] == item[0]:    
                print(item[1], elem[1], sep=",")