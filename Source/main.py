#!/usr/bin/env python3

import sys
# stop creation of __pycache__
sys.dont_write_bytecode = True

import json

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
    p.reader.exec(input_file)
    p.parser.exec()
    p.exporter.exec()

    # TODO
    # debug
    '''
    for track in p.tracks:
        print("Track Orders:")
        for k,v in track.orders.items():
            print("{} -> {}".format(k,v))
    '''
    #print(json.dumps(p.tracks[0].patterns, indent=4))
    '''
    for track in p.tracks:
        for pk,pv in track.patterns.items():
            for ck, cv in pv.items():
                print("PATTERN {} - ROW {} - DATA {}".format(pk, ck, cv))
    '''
    print(p)

if __name__ == "__main__":
    main()
