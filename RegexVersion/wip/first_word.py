#!/usr/bin/env python3

with open('../Docs/famitracker_export_data.txt', 'r') as file:
    for line in file:
        line = line.strip()
        
        if not line:
            continue
        
        if line[0].isupper():
            print(line.split()[0])

