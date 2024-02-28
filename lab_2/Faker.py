import random


orders = []
order_names = ["Astra Linux Common Edition", "Astra Linux Special Edition", "Brest", "RuBackup", "RuPost", "Termidesk", "Tantor", "WorksPad"]
number = 1
positions = []
for i in range(10):
    for num in range(1,random.randint(1, 5)):
        positions.append(random.choice(order_names))
    order = {
        'number': number,
        'order_products': set(positions)         
    }
    number+=1
    orders.append(order)
with open('dataset.txt', 'w') as f:
    f.write(str(orders))
    f.close()
