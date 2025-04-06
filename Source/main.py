#!/usr/bin/env python3

import sys
# stop creation of __pycache__
sys.dont_write_bytecode = True

import json

from project import Project

def get_input_file():
    try:
        input_file = sys.argv[1]
        return input_file
    except Exception as e:
        print(e)
        exit(1)

def main():
    print("Hello Famitracker world!")
    input_file = get_input_file()

    p = Project()
    p.reader.run(input_file)
    p.parser.run()
    p.exporter.run()

if __name__ == "__main__":
    main()
