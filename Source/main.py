#!/usr/bin/env python3

import json
import sys
sys.dont_write_bytecode = True # stop creation of __pycache__

from pathlib import Path
# Path to Submodules/lib_midi_writer_py, relative to this file
midi_path = (Path(__file__).parent.parent / 'Submodules' / 'lib_midi_writer_py').resolve()
if str(midi_path) not in sys.path:
    sys.path.insert(0, str(midi_path))

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
