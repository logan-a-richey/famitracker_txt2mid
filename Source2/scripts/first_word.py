#!/usr/bin/env python3

import sys
f = sys.argv[1]

def m():
    with open(f, 'r') as file:
        for l in file:
            l.strip()
            if not l:
                continue
            if l == "#":
                continue
            if l[0].isupper():
                print(l.split()[0])

if __name__ == "__main__":
    m()
