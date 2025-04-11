#!/usr/bin/env python3
# main.py

import sys
sys.dont_write_bytecode = True

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
    reader.read(input_file)
    
    #parser = Parser(project)
    #exporter = Exporter(project)
    
    # TODO - debug
    print(project)

if __name__ == "__main__":
    main()

