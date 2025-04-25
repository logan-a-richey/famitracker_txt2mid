#!/bin/bash
# run_all.sh

# run all input files!
find ../input_files/ -name "*.txt" -exec ./main.py {} \;

