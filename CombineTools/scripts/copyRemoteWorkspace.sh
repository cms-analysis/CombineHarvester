#!/bin/bash

MAXATTEMPTS=5
PAUSE=60
REMOTEFILE=$1
LOCALFILE=$2
SUCCESS=0

if [ -f $LOCALFILE ]; then
  exit 0
fi


for (( ATTEMPT=1; ATTEMPT<=MAXATTEMPTS; ATTEMPT++ ))
do
  echo "Attempt ${ATTEMPT}"
  xrdcp ${REMOTEFILE} ./${LOCALFILE}
  if [ $? -eq 0 ]; then
    exit 0
  else
    if [ -f ${LOCALFILE} ]; then
      rm ${LOCALFILE}
    fi
    sleep ${PAUSE}
  fi
done

exit 1
