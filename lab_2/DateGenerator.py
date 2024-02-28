import random


order_names = ["Astra Linux Common Edition", "Astra Linux Special Edition", "Brest", "RuBackup", "RuPost", "Termidesk", "Tantor", "WorksPad", "Word 2024", "Excel 2024", "PowerPoint 2024", "Photoshop 2024", "Premier 2024", "MaxPatrol VM", "PT Sandbox", "PT ISIM", "PT Application Firewall", "PT Platform 187", "XSpider", "PT BlackBox" ]
number = 1
random.seed(10)
positions = [random.choice(order_names) for num in range(1,random.randint(1, 5))]
orders=[]
for i in range(10):
    order = {
        'number': number,
        'order_products': set(positions)         
    }
    number+=1
    orders.append(order)
with open('dataset.txt', 'w') as f:
    f.write(str(orders))
    f.close()
