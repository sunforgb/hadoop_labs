import random
import time
import os

order_names = ["apple", "banana", "mango", "grapefruit", "kiwi", "lemon", "pineapple", "peach", "pear", "nectarine", "plum", "tangerine", "lime", "apricot", "fig","orange","papaya","pomegranate", "persimmon", "pomelo"]
path = "test"
random.seed(time.time())
if os.path.exists(path):
    os.remove(path)
with open(path, 'a') as f:
    for i in range(200):
        positions = set(random.choice(order_names) for _ in range(1,random.randint(2, len(order_names))))
        f.write(" ".join(positions))
        f.write("\n")