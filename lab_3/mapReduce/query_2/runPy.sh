#!/bin/bash
# REPARTITION JOIN
hdfs dfs -rm -r mapReduce/query_results_1/output
hdfs dfs -rm -r tmpMapReduce/query_tmp_results_1/output/

yarn jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
-D mapreduce.job.name="Query Join 1 via Streaming" \
-files `pwd`/map1.py,`pwd`/reduce1.py \
-input warehouse/customers/000000_0/ \
-input warehouse/cart/000000_0/ \
-output tmpMapReduce/query_tmp_results_1/output \
-mapper `pwd`/map1.py \
-reducer `pwd`/reduce1.py

yarn jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
-D mapreduce.job.name="Query Join 1 via Streaming" \
-files `pwd`/map2.py,`pwd`/reduce2.py \
-input tmpMapReduce/query_tmp_results_1/output/part-00000 \
-input warehouse/goods/000000_0/ \
-output mapReduce/query_results_1/output \
-mapper `pwd`/map2.py \
-reducer `pwd`/reduce2.py

hdfs dfs -cat mapReduce/query_results_1/output/part-00000
