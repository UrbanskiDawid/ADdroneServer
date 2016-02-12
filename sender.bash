while read LINE; do echo $LINE; sleep 1; done < packets | netcat localhost 9999
