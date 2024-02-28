import random
import time


order_names = ["apple", "banana", "mango", "grapefruit", "kiwi", "lemon", "pineapple", "peach", "pear", "nectarine", "plum", "tangerine", "lime", "apricot", "fig","orange","papaya","pomegranate", "persimmon", "pomelo"]

random.seed(time.time())
for i in range(200):
    positions = set(random.choice(order_names) for _ in range(1,random.randint(1, len(order_names))))
    if not positions:
        continue
    with open('test.txt', 'a') as f:
        f.write(" ".join(positions))
        f.write("\n")
        f.close()