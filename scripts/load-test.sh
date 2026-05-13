#!/bin/bash

URL="https://eks.nourdemo.com"

echo "Starting load test against $URL"
echo "Press CTRL+C to stop."

while true
do
  curl -s "$URL" > /dev/null
  curl -s "$URL/healthz" > /dev/null
  curl -s "$URL/readyz" > /dev/null
  curl -s "$URL/slow" > /dev/null
  echo "Requests sent at $(date '+%H:%M:%S')"
  sleep 0.2
done