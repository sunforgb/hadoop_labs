from pyspark.context import SparkContext
import csv
from pyspark.sql.session import SparkSession

zapad = ["Обама","Трамп","Клинтон","Байден","Пенс","Райан","Макконнелл","Уоррен","Сандерс","Маккейн"]

sc = SparkContext.getOrCreate()

# RDD task

rdd = sc.textFile("hdfs://localhost:9000/user/user/input/tweets/ira_tweets_csv_hashed.csv")
# some fields have ',' inside, so we will use csv lib
rdd = rdd.mapPartitions(lambda x: csv.reader(x))
# removing useless header
header = rdd.first()
rdd1 = rdd.filter(lambda row: row != header)

# get userid, account_language and tweet_text
tweets = rdd1.map(lambda elem: (elem[1], elem[10], elem[12]))

# russian account and zapad in tweet text
tweets = tweets.filter(lambda row: row[1] == "ru" and [x for x in zapad if x in row[2]])
# new rdd, more compact
tweets = tweets.map(lambda elem : (elem[0], str(elem[2])))

# groupBy text and then map grouped values with len
user_tweets = tweets.groupByKey().mapValues(len)
# sort descending, our guy is on top
sorted_users = user_tweets.sortBy(lambda elem: elem[1], ascending=False)
print("User ID RDD: ", sorted_users.first()[0])


# SQL starts here
spark = SparkSession(sc)
tweets = spark.read.csv("hdfs://localhost:9000/user/user/input/tweets/ira_tweets_csv_hashed.csv", header=True)
tweets.createOrReplaceTempView("tweets")
query_ru = """create or replace temp view tweets_temp as
              select userid, account_language, tweet_text
              from tweets where account_language == 'ru'"""
spark.sql(query_ru)
query_user = f"select userid from tweets_temp where tweet_text LIKE '%{zapad[0]}%'"
for member in zapad[1:]:
    query_user += f" OR tweet_text LIKE '%{member}%'"
query_user += f" GROUP BY userid ORDER BY COUNT(tweet_text) DESC LIMIT 1"
print("USER ID in SQL: ")
spark.sql(query_user).show()