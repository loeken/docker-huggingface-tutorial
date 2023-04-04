#!/bin/bash

count=0
match_count=0

while read -r line; do
    label=$(echo $line | jq -r '.label')
    ccsentiment=$(echo $line | jq -r '.ccsentiment')

    # Ignore lines with neutral ccsentiment
    if [[ "$ccsentiment" != "NEUTRAL" ]]; then
        ((count++))
        if [[ "$label" == "$ccsentiment" ]]; then
            ((match_count++))
        fi
    fi
done < $1

if [[ "$count" -eq 0 ]]; then
    echo "No matching records found."
else
    match_percent=$((match_count*100/count))
    echo "Match percentage: $match_percent%"
fi
