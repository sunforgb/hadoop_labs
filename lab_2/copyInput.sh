#!/bin/bash
hdfs dfs -rm -r pairs/input

hdfs dfs -mkdir pairs
hdfs dfs -mkdir pairs/input

hdfs dfs -put test pairs/input/

hdfs dfs -rm -r stripes/input

hdfs dfs -mkdir stripes
hdfs dfs -mkdir stripes/input

hdfs dfs -put test stripes/input/