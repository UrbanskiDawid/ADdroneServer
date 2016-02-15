#!/bin/bash

num_of_segments=101
num_of_bytes=37

for i in `seq 1 $num_of_segments`; do sleep 0.05; head -c $(($i*$num_of_bytes)) $1 | tail -c $num_of_bytes; done | netcat localhost $2
