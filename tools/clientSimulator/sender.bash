#!/bin/bash
#
num_of_segments=101
num_of_bytes=38

## check params
######################################
function showHelp()
{
  echo "sender.bash"
  echo ""
  echo "arg 1: seqence_file"
  echo "   if ends with .dat will not be processed"
  echo "arg 2: port number"
  echo " "
  echo "ERROR: $1"
  exit 1;
}

if [ $# -ne 2 ] ;                        then showHelp "wrong arg number"; fi
if [ ! -f $1 ]  ;                        then showHelp "arg1($1) is not a file"; fi
if ! echo -n "$2" | grep -qP '^[0-9]+$'; then showHelp "arg2($2) is not a port number"; fi

## COMPILE
########################################
if ! echo "$1" | grep -qP '.dat$';
then
  BIN_NAME='toBinaryConverter.out'
  rm toBinaryConverter 2>/dev/null
  g++ toBinaryConverter.cpp -o "$BIN_NAME"
  if [ $? -ne 0 ]; then   echo "failed to compile toBinaryConverter.cpp";  exit 1;  fi

  SEQUENCE_BIN=$1".dat"
  echo "converting '$1' into '$SEQUENCE_BIN'..."
  ./$BIN_NAME "$1" "$SEQUENCE_BIN"
  if [ $? -ne 0 ]; then   echo "failed to run '$BIN_NAME' $?";  exit 1;  fi

  rm "$BIN_NAME"
else
  SEQUENCE_BIN="$1"
fi

## SEND SEQUENCE
#########################################
if [ ! -f "$SEQUENCE_BIN" ]; then
  echo "ERROR: cant find sequence file: '$SEQUENCE_BIN'"
  exit 1
else
  echo "using '$SEQUENCE_BIN'"
fi

for i in `seq 1 $num_of_segments`; do
  sleep 0.05;
  head -c $(($i*$num_of_bytes)) $SEQUENCE_BIN | tail -c $num_of_bytes;
done | netcat -q 1 localhost $2
