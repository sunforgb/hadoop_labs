#!/bin/bash
itr_count=5
cp input.txt input1.txt
for ((itr=1; itr <= $itr_count; itr++)); do
    echo $itr
    ittr=$(($itr+1))
    cat input$itr.txt | ./map.py | sort -g | ./reduce.py > input$ittr.txt
    rm input$itr.txt
done
cat input$itr.txt