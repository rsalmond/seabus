#!/bin/bash

get_channels() {
  cmd="/usr/bin/kal -s $1 -d 0 -g 40"
  while read -r line
  # iterate over the three highest power channels found
  do
      channel=$(echo $line | awk '{print $2}')
      channels=`echo $channels $channel`
  done < <($cmd | grep chan | awk '{print $7, $2}' | sort -k1,1nr | head -n 3)
  echo $channels
}

get_offset() {
  cmd="./kal -c $channel -d 0 -g 40"
  error_value=$($cmd | grep average\ absolute\ error)
  echo $error_value | awk '{print $4}'
}

#Change this band if you need to, see kalibrate-rtl help for more info.
band='GSM900'
echo "Scanning for channels on band $band"
count=0
for channel in $(get_channels $band); do
  for i in $(seq 1 3); do
    count=$(expr $count + 1)
    offset=$(get_offset $channel)
    echo "Offset $i for channel $channel is $offset"
    if [ $count -eq 9 ]; then
      offsets=`echo $offsets $offset`
    else
      offsets=`echo $offsets $offset +`
    fi
  done
done

average=$(echo "($offsets) / 9" | bc)

echo "Average offset: $average"
