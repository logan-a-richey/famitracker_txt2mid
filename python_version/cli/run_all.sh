#!/bin/bash
# run_all.sh

# TODO - changed input file path! Will fix in the future
# run all input files!
find ../input_files/ -name "*.txt" -exec ./main.py {} \;

