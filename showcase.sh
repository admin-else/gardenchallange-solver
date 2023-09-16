#!/bin/bash
cd $(dirname $0)
./garden-tester -generate garden.txt
python3 ./solver.py
./garden-tester -input cmds.txt ./garden.txt
echo "You can now press ENTER to exit."
read
rm -f cmds.txt
rm -f garden.txt
rm -rf ./__pycache__