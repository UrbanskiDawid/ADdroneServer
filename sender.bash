#!/bin/bash

num_of_segments=101
num_of_bytes=37

for i in `seq 1 $num_of_segments`
do
  head -c $(($i*$num_of_bytes)) $1 | tail -c $num_of_bytes | netcat localhost 9999
  sleep 0.05 
done
