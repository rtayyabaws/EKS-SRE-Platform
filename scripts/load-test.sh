#!/bin/bash

URL="https://eks.nourdemo.com"

echo "Starting load test against $URL"
echo "Press CTRL+C to stop."

while true
do
  for i in {1..20}; do
    curl -s "$URL" > /dev/null &
    curl -s "$URL/healthz" > /dev/null &
    curl -s "$URL/readyz" > /dev/null &
    curl -s "$URL/slow" > /dev/null &
  done

  wait
  echo "Batch sent at $(date '+%H:%M:%S')"
  sleep 1
done