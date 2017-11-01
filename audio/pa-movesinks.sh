#!/bin/sh

if [ $# -eq 0 ]
then
        echo "Usage: $(basename "$0") <new default sink>"
        exit 64
fi

SINK=$1

pacmd set-default-sink "$SINK"
pacmd list-sink-inputs | grep index | while read -r line
do
	pacmd move-sink-input "$(echo "$line" | cut -f2 -d' ')" "$SINK"
done
