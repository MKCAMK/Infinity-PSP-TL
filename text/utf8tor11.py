#!/usr/bin/env python

import os, sys

if len(sys.argv) != 3:
    print('usage: utf8tor11.py utf8.txt r11.txt')
    sys.exit()

with open(sys.argv[1], encoding='UTF-8') as f, open(sys.argv[2], 'w', encoding='sjisx0213') as fout:
    for line in f:
        line = line.replace('ä', '⑮')
        line = line.replace('ö', '⑪')
        line = line.replace('ü', '⑫')
        line = line.replace('é', '⑬')
        line = line.replace('à', '⑭')
        line = line.replace('™', '⑱')
        line = line.replace('~', '\u301c') # tilde to wave dash
        line = line.replace('\uff5e', '\u301c') # full-width tilde to wave dash
        line = line.replace('ç', 'c')
        line = line.replace('ï', 'i')
        line = line.replace('Ö', '⑪')
        line = line.replace('\u2014', '\u2015') # em dash to horizontal bar
        fout.write(line)
