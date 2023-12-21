#!/bin/bash

# For some reason, wsl doesn't load this if this file is directly run with wsl.exe
# Missing this means missing a important PATH adjustments, to run poetry.
source ~/.bash_profile

poetry env use 3.10
poetry install
poetry run build_executable
