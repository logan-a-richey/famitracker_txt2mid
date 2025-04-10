#!/usr/bin/env python3
# main.py

import sys

from stages.reader import Reader
from stages.parser import Parser
from stages.exporter import Exporter

def get_input_file() -> str:
    try:
        return sys.argv[1]
    except Exception as e:
        print("[ERROR] {}".format(e))
        #print("[USAGE] ./main --input demo.txt"
        print("[USAGE] ./main input.txt")
    exit(1)

def main() -> None:
    input_file = get_input_file()

    project = Project()
    
    reader = Reader(project)
    reader.read(input_file)

    parser = Parser(project)
    parser.parse()

    exporter = Exporter(project)
    export_dir = "Exports/"
    exporter.export(export_dir)

if __name__ == "__main__":
    main()

