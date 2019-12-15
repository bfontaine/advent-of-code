#! /bin/bash

total=0

module_fuel() {
  local mass=$1
  local fuel=$((mass/3-2))
  local additional=

  if [ $fuel -le 0 ]; then
    echo 0
    return
  fi

  additional=$(module_fuel $fuel)
  echo $((fuel+additional))
}

while read -r line; do
  fuel=$(module_fuel $line)
  total=$((total+fuel))
done

echo "$total"
