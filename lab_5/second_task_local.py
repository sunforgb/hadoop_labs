from pyspark.sql.session import SparkSession
from pyspark.context import SparkContext
from graphframes import *

n = 1
path_length = 1

sc = SparkContext.getOrCreate()
sc.setCheckpointDir("hdfs://localhost:9000/tmp")
spark = SparkSession(sc)
tweets = spark.read.csv("hdfs://localhost:9000/user/user/input/tweets/ira_tweets_csv_hashed_40000.csv", header=True)
tweets.createOrReplaceTempView("tweets")

cleaned_tweets = spark.sql("select * from tweets where in_reply_to_tweetid is null or in_reply_to_tweetid rlike '^\\\d{18}$'")

cleaned_tweets.createOrReplaceTempView("cleaned_tw")

v = spark.sql("select tweetid as id, userid, reply_count, in_reply_to_userid, in_reply_to_tweetid from cleaned_tw")

e = spark.sql("select in_reply_to_tweetid as src, tweetid as dst from cleaned_tw")

g = GraphFrame(v, e)

g.dropIsolatedVertices()

vertexes = g.vertices.rdd.filter(lambda row: row[2] != '0' and row[3]==None).collect()
# print(vertexes[0])
# chebupels = g.vertices.rdd.filter(lambda row: row[3]!=None).collect()

# from_query=""" id in select tweetid as id from cleaned_tw where reply_count != '0' and in_reply_to_userid is null'
# """
# to_query = """ id in select tweetid as id from cleaned_tw where in_reply_to_userid is not null'
# """

for vertex in vertexes:
  print(f"Trying vertex {vertex['id']}")
  paths = g.bfs(fromExpr="id='"+vertex["id"]+"'", toExpr="id<>'"+vertex["id"]+"'", maxPathLength=path_length)
  paths.show()
  tmp = v.rdd.filter(lambda row: row[4] == vertex["id"]).collect()
  print(len(tmp))
  if not paths.rdd.isEmpty():
      paths.show()
      if paths.count() >= n:
          paths.limit(n)
          path = paths.orderBy("from").first()
          print("User ID is: ", path["from"]["userid"])
          break
# paths = g.bfs(fromExpr=from_query, toExpr=to_query, maxPathLength=path_length)
# if not paths.rdd.isEmpty():
#     paths.show()
#     if paths.count() >= n:
#         paths.limit(n)
#         path = paths.orderBy("from").first()
#         print("User ID is: ", path["from"]["userid"])
#         exit()

# result = g.stronglyConnectedComponents(maxIter=4)


# components = result.groupBy("component").count().orderBy("count", ascending=False).limit(n)
# largest_component = components.orderBy("count").first()
# largest_component_id = largest_component["component"]
# parent_vertex = result.filter(result['component']==largest_component_id).select("userid").first()["userid"]
# print("USER ID IS: ", parent_vertex)