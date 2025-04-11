#!/usr/bin/env python3
# main.py

import sys

from containers.project import Project
from stages.reader import Reader

# TODO argparse
def get_input_file() -> str:
    try:
        return sys.argv[1]
    except Exception as e:
        print("[ERROR] {}".format(e))
        print("[USAGE] ./main file.txt")
    exit(1)

def main():
    input_file = get_input_file()
    project = Project()
    reader = Reader(project)
    #parser = Parser(project)
    #exporter = Exporter(project)

    reader.read(input_file)
    print(project)
    return

if __name__ == "__main__":
    main()

