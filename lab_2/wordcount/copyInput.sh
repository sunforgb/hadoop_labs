#!/bin/bash

hdfs dfs -mkdir wordcount
hdfs dfs -mkdir wordcount/input

hdfs dfs -put file01 wordcount/input/
hdfs dfs -put file02 wordcount/input/