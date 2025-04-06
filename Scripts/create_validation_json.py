#!/usr/bin/env python3

import sys
import re
import json

class CreateJson:
    def __init__(self):
        self.data = {}
        self.last_tag = ""

    def print_debug_table_line(self, field_name, field_data_type, field_range_lower, field_range_upper):
        print("TAG: {} DATA_TYPE: {} RANGE_LOWER: {} RANGE_UPPER: {}".format(
            *["\'{}\'".format(item).ljust(20) for item in [field_name, field_data_type, field_range_lower, field_range_upper]]
        ))

    def _process_line(self, line):
        # tag line
        if line[0].isupper():
            tag = line.split()[0].upper()
            self.data[tag] = {}
            self.data[tag]["FIELDS"] = {}
            self.last_tag = tag
            return
        
        # field data
        elif line[0] == "-":
            if line.startswith("- Defines"):
                return

            field_name = ""
            field_data_type = ""
            field_range_lower = ""
            field_range_upper = ""
            
            try:
                word_match = re.findall(r'\w+', line)
                if word_match:
                    field_name = word_match[0]
                    field_data_type = word_match[1]
                    
                    if word_match[1] == "string":
                        pass
                    else:
                        range_match = re.findall(r'\-?[0-9A-F]+', line)
                        if range_match: 
                            field_range_lower = range_match[0]
                            field_range_upper = range_match[1]
                    
                    self.print_debug_table_line(field_name, field_data_type, field_range_lower, field_range_upper)

            except Exception as e:          
                print("ERROR {} \nLINE \'{}\'".format(e, line))
                exit(1)
            
            field_range = (field_range_lower, field_range_upper)
            
            self.data[self.last_tag]["FIELDS"][field_name] = {}
            this_field_name = self.data[self.last_tag]["FIELDS"][field_name] 
            this_field_name["TYPE"] = field_data_type
            this_field_name["RANGE"] = {}
            this_field_name["RANGE"]["LOWER"] = field_range_lower
            this_field_name["RANGE"]["UPPER"] = field_range_upper
            
    def read_file(self, ifile):
        with open(ifile, "r") as file:
            for line in file:
                line = line.strip()
                if not line: continue
                if line[0] == "#": continue
                self._process_line(line)

    def write_file(self, ofile):
        with open(ofile, "w") as file:
            file.write(json.dumps(self.data, indent=2))
        print("File \'{}\' has been created.".format(ofile))


def get_input_file():
    try:
        return sys.argv[1]
    except Exception as e:
        print("Error {}".format(e))
        exit(1)

def main():
    ifile = get_input_file()
    cj = CreateJson()
    cj.read_file(ifile)
    cj.write_file("famitracker_export_data.json") 

if __name__ == "__main__":
    main()

