#!/usr/bin/env python3

# script for writing dispatch from doc file

import sys

def print_dispatch_dict_items(first_word):
    print("\"{}\": {},".format( first_word, "self._handle_{}".format(first_word.lower())))
    pass

def print_dispatch_functions(first_word):
    print("def _handle_{}(self, line):".format(first_word.lower()))

def main():
    try:
        ifile = sys.argv[1]
    except Exception as e:
        print("Usage: `./make_table.py ../Docs/fami_text_export_docs.txt`")
        exit(1)

    with open(ifile, 'r') as file:
        for line in file:
            if line[0].isupper():
                first_word = line.split()[0]

                # uncomment these lines to generate useful code:
                # print_dispatch_dict_items(first_word)
                # print_dispatch_functions(first_word)
                pass

if __name__ == "__main__":
    main()

