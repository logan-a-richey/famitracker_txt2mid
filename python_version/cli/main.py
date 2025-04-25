#!/usr/bin/env python3

import os
import sys
sys.dont_write_bytecode = True

from containers.project import Project

def get_input_file():
    try:
        return sys.argv[1]
    except:
        print("[USAGE] ./main <input.txt>")
    sys.exit(1)

def main():
    input_file = get_input_file()
    # print("[INFO] Scanning file:", input_file)

    output_dir_name = "exports"
    output_dir_path = os.path.join(os.getcwd(), output_dir_name)
    os.makedirs(output_dir_path, exist_ok=True)

    project = Project()
    project.reader.read(input_file)     # NOTE read data into project
    project.parser.parse()              # NOTE parse track data within project
#   project.exporter.export(output_dir) # NOTE export each track within the project

    # print(project)              # NOTE debug print the project

if __name__ == "__main__":
    main()

