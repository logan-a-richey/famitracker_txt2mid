#!/usr/bin/env python3
# main.py

import os 
import sys
import re
import json

from stages.reader import Reader
from containers.project import Project
#from containers.instrument import Instrumnet
#from containers.macro import Macro
#from containers.groove import Groove
#from containers.track import Track

def get_input_file():
    try:
        return sys.argv[1]
    except Exception as e:
        print("Usgae: ./main input.txt. Error: {}".format(e))
    exit(1)

def main():
    input_file = get_input_file()
    
    project = Project()
    reader = Reader(project)
    
    reader.read(input_file)
    print(project)
    #p.parser.parse()
    
    #os.makedirs("Exports", exist_ok=True)
    #p.exporter.export(output_dir_path)
    
    pass

if __name__ == "__main__":
    main()
