#!/bin/bash

PIDFILE=/var/local/scrape.pid
if [ -f $PIDFILE ]
then
  PID=$(cat $PIDFILE)
  ps -p $PID > /dev/null 2>&1
  if [ $? -eq 0 ]
  then
    echo "PID is active. Exiting early."
    exit 1
  fi
fi

echo $$ > $PIDFILE
cd $(dirname "$0")
python scrape.py
rm $PIDFILE
