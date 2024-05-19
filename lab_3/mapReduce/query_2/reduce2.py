#!/usr/bin/python3
import sys

kek = {}
for line in sys.stdin:
    line = line.strip().split("\t")
    if line[1] not in kek:
        kek[line[1]] = []
    kek[line[1]].append(list(item for item in line if item != line[1]))

for item in kek['R']:
    for elem in kek['L']:
        if elem[0] == item[0]:    
            print(item[1], elem[1], sep=",")