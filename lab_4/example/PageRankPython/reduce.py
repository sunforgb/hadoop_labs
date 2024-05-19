#!/usr/bin/python3
import sys

old_node_id = None
node_id = None
links = ""
s = 0.0
for line in sys.stdin:
    kv = line.strip().split("\t")
    old_node_id = node_id
    node_id = kv[0]
    if (old_node_id != node_id) and (old_node_id is not None):
        print(old_node_id + "\t" + str(s) + ";" + links)
        s = 0.0
        links = ""
    value_list = kv[1].split(";")
    if len(value_list) > 1:
        links = value_list[1]
        if not links:
            s += float(value_list[0])
    else:
        s += float(value_list[0])
print(node_id + "\t" + str(s) + ";" + links)
