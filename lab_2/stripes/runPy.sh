#!/bin/bash

hdfs dfs -rm -r stripes/output

yarn jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
-D mapreduce.job.name="WordCount Job via Streaming" \
-files `pwd`/countMap.py,`pwd`/countReduce.py \
-input stripes/input/ \
-output stripes/output/ \
-mapper `pwd`/countMap.py \
-reducer `pwd`/countReduce.py

hdfs dfs -cat stripes/output/part-00000
