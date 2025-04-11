#!/usr/bin/env python3
# create_validation_json.py

import os
import sys
import re
import json
import logging

# stop creation of __pycache__
sys.dont_write_bytecode = True 

# init logging path if it does not exist
LOG_DIR = '/tmp/logs'
os.makedirs(LOG_DIR, exist_ok=True)

# create the logging path
LOG_FILE_PATH = LOG_DIR + '/create_json_check.log'

# files to read and write
ifile = os.path.abspath("../Docs/famitracker_export_data.txt")
ofile = os.path.abspath("../Docs/famitracker_export_data.json")


class CreateJsonReader:
    ''' Helper class to parse famitracker_export_data.txt into a dictionary for json creation. '''
    
    def __init__(self, parent) -> None:
        self.parent = parent
        self.data = {}
        self.last_tag = ""

    def _handle_tag(self, line) -> None:
        tag = line.split()[0].upper()
        self.data[tag] = {}
        self.data[tag]["FIELDS"] = {}
        self.last_tag = tag
    
    def _handle_data(self, line) -> None:
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
                
                # Display data to be used in json in an ascii text table. Writes to logger and stdout.
                self.parent.writer.print_debug_table_line(
                    field_name, field_data_type, field_range_lower, field_range_upper
                )

        except Exception as e:          
            self.logger.error("ERROR {} \nLINE \'{}\'".format(e, line))
            exit(1)
        
        self.data[self.last_tag]["FIELDS"][field_name] = {}
        this_field_name = self.data[self.last_tag]["FIELDS"][field_name] 
        this_field_name["TYPE"] = field_data_type
        this_field_name["RANGE"] = {}
        this_field_name["RANGE"]["LOWER"] = field_range_lower
        this_field_name["RANGE"]["UPPER"] = field_range_upper

    def _process_line(self, line) -> None:
        if line[0].isupper():
            self._handle_tag(line)
        elif line[0] == "-":
            self._handle_data(line)

    def read_file(self, ifile):
        with open(ifile, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                if line[0] == "#":
                    continue
                self._process_line(line)


class CreateJsonWriter:
    ''' Helper class to writes logging info & create the json file. '''

    def __init__(self, parent):
        self.parent = parent

    def print_debug_table_line(self, field_name, field_data_type, field_range_lower, field_range_upper):
        params = [field_name, field_data_type, field_range_lower, field_range_upper]
        self.parent.logger.info("TAG: {} DATA_TYPE: {} RANGE_LOWER: {} RANGE_UPPER: {}".format( \
            *["\'{}\'".format(item).ljust(20) for item in params])
        )

    def write_file(self, ofile):
        with open(ofile, "w") as file:
            file.write(json.dumps(self.parent.reader.data, indent=2))
        self.parent.logger.info("File \'{}\' has been created.".format(ofile))


class CreateJson:
    '''
    Reads famitracker_export_data.txt. Converts it into .json format for later use.
    Contains a CreateJsonReader and a CreateJsonWriter object.
    Contains logic for handling the logger. The logger can write to both file and stdout.
    '''
    def __init__(self, log_to_console=True):
        self.reader = CreateJsonReader(self)
        self.writer = CreateJsonWriter(self)
        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Avoid duplicate handlers if __init__ is called more than once
        if not self.logger.handlers:
            # Shared formatter
            formatter = logging.Formatter(
                fmt='%(asctime)s - %(levelname)s - %(filename)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

            # File handler
            file_handler = logging.FileHandler(LOG_FILE_PATH, mode='w')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

            # Optional console handler
            if log_to_console:
                console_handler = logging.StreamHandler(sys.stdout)
                console_handler.setFormatter(formatter)
                self.logger.addHandler(console_handler)
        

def main():
    cj = CreateJson()
    cj.reader.read_file(ifile)
    cj.writer.write_file(ofile) 

if __name__ == "__main__":
    main()

