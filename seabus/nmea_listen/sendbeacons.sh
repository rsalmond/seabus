#!/bin/bash

while read beacon; do
    echo "sending " $beacon
    echo $beacon | nc -u -q 1 localhost 3001
done < $1
