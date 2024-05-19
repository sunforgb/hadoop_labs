#!/usr/bin/python3
import sys
import random

a = random.uniform(0.0001, 0.9999)
nodes = []
counter = 4
pr_loss = 0
for line in sys.stdin:
    node = []
    kv = line.strip().split("\t")
    if len(kv) == 1:
        pr_loss = int(kv[0]) / 100000
    else:
        # counter += 1
        node.append(kv[0])
        values_list = kv[1].split(";")
        node += values_list
        if node[-1] == '':
            node.pop()
        nodes.append(node)
    
node_loss = float(pr_loss) / counter
for node in nodes:
    if len(node) <=2:
        print(node[0] + '\t' + str(round(float(node[1]), 3)) + ';')
        continue
    node[1] = a*(1/counter) + (1-a)*(node_loss + float(node[1]))
    string = node[0] + '\t' + str(round(float(node[1]), 3)) + ';'
    if len(node) > 2:
        string += ' '.join(node[2:])
    print(string)
    