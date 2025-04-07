#!/usr/bin/env python3

import json
import sys

from project import Project

sys.dont_write_bytecode = True # stop creation of __pycache__

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
