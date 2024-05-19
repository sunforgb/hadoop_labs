#!/usr/bin/python3
import sys

for line in sys.stdin:
    kv = line.strip().split("\t")
    node_id = kv[0]
    value_list = kv[1].split(";")
    pr = float(value_list[0])
    if value_list[1]:
        links = value_list[1].split(" ")
        p = pr / len(links)
    else:
        print(f"reporter:counter:MyGroup,MyCounter,{int(pr*100000)}", file=sys.stderr)
        links = []
    line = line.replace("\n", "")
    for m in links:
        print(m + "\t" + str(p))
    print(line)
