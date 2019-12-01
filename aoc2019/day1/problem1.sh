#! /bin/bash

total=0

while read -r line; do
  total=$((total+line/3-2))
done

echo "$total"
