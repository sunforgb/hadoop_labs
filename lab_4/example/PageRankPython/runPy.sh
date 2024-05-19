#!/bin/bash
itr_count=2
rnd=$((130 + $RANDOM % 10))
counter=0
for ((itr=1; itr <= $itr_count; itr++)); do
    echo "Doing iteration $itr of $itr_count..."
    hdfs dfs -rm -r PR/itr_$((itr+1))
    hdfs dfs -rm -r PR/itr_$((itr+1))_tmp
    hdfs dfs -rm -r PR/itr_$((itr+1))_tmp_counter
    yarn jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
        -D mapreduce.job.name="PageRank Job via Streaming $rnd" \
        -files $(pwd)/map.py,$(pwd)/reduce.py \
        -input PR/itr_$itr/ \
        -output PR/itr_$((itr+1))_tmp/ \
        -mapper $(pwd)/map.py \
        -reducer $(pwd)/reduce.py
    yarn application -list -appStates FINISHED | grep "PageRank Job via Streaming $rnd" | awk -F '/' '{print $NF}' > tmp.txt
    jobId=`cat tmp.txt | tail -n 1` 
    echo $jobId
    counter=`mapred job -counter $jobId MyGroup MyCounter | tail -n 1`
    echo $counter > counter.txt
    hdfs dfs -mkdir PR/itr_$((itr+1))_tmp_counter
    hdfs dfs -put counter.txt PR/itr_$((itr+1))_tmp_counter/

    yarn jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
        -D mapreduce.job.name="PageRank Job Counter via Streaming $rnd" \
        -files $(pwd)/map2.py,$(pwd)/reduce2.py \
        -input PR/itr_$((itr+1))_tmp/ \
        -input PR/itr_$((itr+1))_tmp_counter/ \
        -output PR/itr_$((itr+1))/ \
        -mapper $(pwd)/map2.py \
        -reducer $(pwd)/reduce2.py

    rnd=$(($rnd + 1))
done
hdfs dfs -cat PR/itr_$((itr_count+1))/part-00000
# rnd=$(($rnd-1))
# jobId=`yarn application -list -appStates FINISHED | grep "PageRank Job via Streaming $rnd" | awk -F '/' '{print $NF}'`
# echo $jobId
# mapred job -counter $jobId MyGroup MyCounter
# echo "Total leaks is: $counter"