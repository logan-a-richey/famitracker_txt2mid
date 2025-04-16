#!/usr/bin/env python3

import sys

def m():
    count = 0
    with open('../docs/famitracker_export_data.txt', 'r') as file:
        for l in file:
            l.strip()
            if not l:
                continue
            if l == "#":
                continue
            if l[0].isupper():
                print("/* {} */".format(l.split()[0]))
                print("0x{}".format("{:02x}".format(count).upper()))
                count += 1
                print()


if __name__ == "__main__":
    m()
