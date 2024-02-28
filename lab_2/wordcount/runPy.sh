#!/bin/bash

hdfs dfs -rm -r wordcount/output

yarn jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
-D mapreduce.job.name="WordCount Job via Streaming" \
-files `pwd`/countMap.py,`pwd`/countReduce.py \
-input wordcount/input/ \
-output wordcount/output/ \
-mapper `pwd`/countMap.py \
-combiner `pwd`/countReduce.py \
-reducer `pwd`/countReduce.py

hdfs dfs -cat wordcount/output/part-00000
