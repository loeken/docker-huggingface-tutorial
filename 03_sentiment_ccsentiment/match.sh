#!/bin/bash

# Check if the file path is provided as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 <file-path>"
  exit 1
fi

# Initialize counters
total_lines=0
matched_lines=0

# Read the file line by line
while read -r line; do
  # Extract label and ccsentiment fields using jq
  label=$(echo "$line" | jq -r '.label')
  ccsentiment=$(echo "$line" | jq -r '.ccsentiment')

  # Compare the values and update counters
  echo "$label" = "$ccsentiment" $matched_lines/$total_lines
  if [ "$label" = "$ccsentiment" ]; then
    matched_lines=$((matched_lines + 1))
  fi
  total_lines=$((total_lines + 1))
done < "$1"

# Compute the percentage of matches
if [ "$total_lines" -gt 0 ]; then
  match_percent=$(echo "scale=2; $matched_lines/$total_lines*100" | bc)
  echo "Match percentage: $match_percent%"
else
  echo "Error: File is empty or does not exist."
fi
