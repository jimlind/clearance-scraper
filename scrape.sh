#!/bin/bash

# Where the PID should live
PIDFILE=/var/local/scrape.pid

# If the PID file is 3 hours old just delete it
if test `find "$PIDFILE" -mmin +180`
then
    echo "PID is really old. Starting Fresh."
    pkill -F $PIDFILE
    rm $PIDFILE
fi

# If the PID file exists exit early
if [ -f $PIDFILE ]
then
  PID=$(cat $PIDFILE)
  if ps -p $PID > /dev/null
  then
    echo "PID is active. Exiting early."
    exit 1
  fi
fi

# Write the PID to the file and start the script
echo $$ > $PIDFILE
cd $(dirname "$0")
python scrape.py
rm $PIDFILE
