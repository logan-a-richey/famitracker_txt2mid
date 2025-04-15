#!/usr/bin/env python3
# main.py

import sys
sys.dont_write_bytecode = True

from containers.project import Project
from stages.reader import Reader
from stages.parser import Parser

# TODO - use argparse instead?
def get_input_file() -> str:
    try:
        return sys.argv[1]
    except Exception as e:
        print("[ERROR] {}".format(e))
        print("[USAGE] ./main file.txt")
    exit(1)

def main() -> int:
    input_file = get_input_file()
    project = Project()
    
    reader = Reader(project)
    parser = Parser(project)
    
    reader.read(input_file)
    parser.parse()
    
    exit(0)
    
    #exporter = Exporter(project)
    
    # KeyDpcm
    #for inst_key, inst_obj in project.instruments.items():
    #    if hasattr(inst_obj, "key_dpcm"):
    #        if (inst_obj.key_dpcm):
    #            print("---\nInstrument {}: \'{}\'".format(inst_key, inst_obj.name))
    #            for note_key, note_obj in inst_obj.key_dpcm.items():
    #                print("{} -> {}".format(note_key, note_obj))

    # N163 Data:
    #for ik,iv in project.instruments.items():
    #    if hasattr(iv, "n163_waves"):
    #        print("Instrument {} \'{}\'".format(ik, iv.name))
    #        for wi, wv in iv.n163_waves.items():
    #           print("{} -> {}".format(wi, wv))
    
    # FDS Data:
    #for ik, iv in project.instruments.items():
    #    if isinstance(iv, InstFDS):
    #        print(iv.macros)
    
    print(project)
    return 0

if __name__ == "__main__":
    main()

