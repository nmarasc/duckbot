#!/bin/bash
version="$1"
file="$2"

if [[ -z "$file" ]]; then
  echo "No file specified"
  exit 0
elif [[ ! -f "$file" ]]; then
  echo "error: $file does not exist"
  exit 1
fi

update_count=$(cat $file | grep -n '^# Last Updated:' | wc -l)
if [[ $update_count -gt 1 ]]; then
  echo "error: $file contains multiple update lines"
  exit 2
elif [[ $update_count -eq 1 ]]; then
  echo "Update line exists"
#   sed -i 's/^# Last Updated: [0-9]\.[0-9]\(\.[0-9]\)\?$/# Last Updated: 1.0/g' main.py
else
  echo "Update line does not exist"
  qline=$(cat $file | grep -n '^\"\"\"$' | grep -o '^[0-9]*')
  if [[ -z "$qline" ]]; then
    echo "error: $file contains no triple quote line"
    exit 3
  elif [[ $(echo "$qline" | wc -l) -gt 1 ]]; then
    echo "error: $file contains multiple triple quote lines"
    exit 4
  else
    echo "Line: $qline"
    qline=$(( qline + 1 ))
#     sed -i "${qline}i\# Last Updated: $version" $file
  fi
fi
