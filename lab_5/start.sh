#!/bin/bash

$SPARK_HOME/sbin/start-master.sh

$SPARK_HOME/sbin/start-slave.sh spark://hadoop-datanode:7077

spark-submit --class org.apache.spark.examples.SparkPi --master spark://hadoop-datanode:7077 --executor-memory 1G --total-executor-cores 1 $SPARK_HOME/examples/jars/spark-examples_2.11-2.4.8.jar 10