#!/usr/bin/env python

import sys

if len(sys.argv) != 3:
    print('usage: utf8toe17.py utf8.txt r11.txt')
    sys.exit()

with open(sys.argv[1], encoding='UTF-8') as f, open(sys.argv[2], 'w', encoding='sjisx0213') as fout:
    for line in f:
        line = line.replace('ä', '⑩')
        line = line.replace('ö', '⑪')
        line = line.replace('ü', '⑫')
        line = line.replace('é', '⑬')
        line = line.replace('à', '⑭')
        line = line.replace('™', '⑱')
        line = line.replace('~', '〜')
        line = line.replace('ç', 'c')
        line = line.replace('ï', 'i')
        fout.write(line)
