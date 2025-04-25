#!/usr/bin/env python3

import os
import sys

# Prevent Pycache
sys.dont_write_bytecode = True

# Add the project root to sys.path manually
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.containers.project import Project

def get_input_file():
    try:
        return sys.argv[1]
    except:
        print("[USAGE] ./main <input.txt>")
    sys.exit(1)

def main():
    input_file = get_input_file()

    # set up output folder
    output_dir_name = "output_midi"
    output_dir_path = os.path.join(os.getcwd(), output_dir_name)
    os.makedirs(output_dir_path, exist_ok=True)

    project = Project()
    project.reader.read(input_file)         
    project.parser.parse(output_dir_name)   

    # debug print project data:
    # print(project)
    return

if __name__ == "__main__":
    main()

