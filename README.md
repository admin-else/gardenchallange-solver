# sdssh 2023 solver

this solves the 2023 sdssh entry [challagen](https://github.com/maxwellmatthis/sdssh-challenge-2023).

## How to run

execute the ``showcase.sh`` file.

## Files

### showcase.sh

This will run a showcase of the program prompting the user to enter size, width and amount of areas and will then demonstrate the program.

### solver.py

the main file where all the logic is it will try to read from garden.txt and will create a file called cmds.txt that contains all commands for garden tester.

### testbench.sh

This file is used to test the solver.py over and over again on newly generated gardens. To test the program 1000 times you run this command ``./testbench.sh 1000``.

### garden-tester

This is the tester from [here](https://github.com/juho05/sdssh-gartentester/releases/download/v0.4.0/gartentester-linux-arm64).

## requirements

- bash

- python3

- linux based machine to run the ``garden-tester`` file.
