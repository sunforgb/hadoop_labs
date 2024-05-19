#!/bin/bash

hdfs dfs -mkdir PR
hdfs dfs -mkdir PR/itr_1

hdfs dfs -put input.txt PR/itr_1
