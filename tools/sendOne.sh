#!/bin/bash

if [ $# -ne 1 ]; then
echo "sending single message to port"
echo " arg1: port "
exit 1
fi

echo -n '$$$$assaaabbbbbbbbbbccccccccccdddddddd' > /dev/tcp/localhost/$1
