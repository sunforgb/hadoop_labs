#!/usr/bin/python3
import pyhdfs

def main(prompt: str):
    client = pyhdfs.HdfsClient(hosts="localhost:50070", user_name="user")
    with client.open("/user/user/stripes/output/part-00000") as file:
        hdfs_results = file.readlines()
    result_dictionary = {}
    for i in hdfs_results:
        products, count = i.decode('utf-8').strip().split('|')
        token = sorted(products.strip().split(' '))
        if not result_dictionary.get(token[0], None):
            result_dictionary[token[0]] = {}
        if not result_dictionary.get(token[1], None):
            result_dictionary[token[1]] = {}
        result_dictionary[token[0]][token[1]] = result_dictionary.get(token[0], {}).get(token[1], 0) + int(count)
        result_dictionary[token[1]][token[0]] = result_dictionary.get(token[1], {}).get(token[0], 0) + int(count)
    result = result_dictionary.get(prompt, None)
    if not result:
        print("Ошибся продуктом, заходи в другой раз")
        return
    result = list(map(lambda x: x[0], sorted(result.items(), key=lambda x : x[1], reverse=True)[:10]))
    print("\n\nСледующие продукты могут вам подойти: ")
    print(*result, sep="\n")

if __name__ == "__main__":
    prompt = str(input("Введите название продукта: "))
    main(prompt)