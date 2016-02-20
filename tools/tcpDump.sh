#!/bin/bash
if [ $# -ne 1 ]; then
  echo "arg1: port to listen"
  exit 1
fi

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

tcpdump -v -X -i any -n dst port $1
