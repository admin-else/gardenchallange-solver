#!/bin/bash

if ! [[ "$1" =~ ^[0-9]+$ ]]; then
  echo "./testbench <AMOUNT_OF_TESTS>"
  exit 1
fi

for ((i=1; i<=$1; i++))
do
  ./garden-tester -generate -size random -area-count random garden.txt # generates a random garden
  echo "generating commands"
  python3 ./solver.py
  if [ $? -ne 0 ]; then
    echo "Error: The python script failed."
    exit 1
  fi
  echo "testing"
  ./garden-tester -no-delay -input cmds.txt ./garden.txt > /dev/null 
  if [ $? -ne 0 ]; then
    echo "Error: The garden tester failed."
    exit 1
  fi
  echo "Done with iteration $i."
done
rm -f cmds.txt
rm -f garden.txt
echo "No errors."
