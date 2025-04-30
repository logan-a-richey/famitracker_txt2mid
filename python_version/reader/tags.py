#!/usr/bin/env python3

import sys
def main():
    x = sys.argv[1]
    with open(x, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            if line[0].isupper():
                print(line.split()[0])

if __name__ == "__main__":
    main()

