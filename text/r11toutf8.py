#!/usr/bin/env python

import os, sys

if len(sys.argv) != 3:
    print('usage: r11toutf8.py r11.txt utf8.txt')
    sys.exit()

n7 = 'GAME' in os.environ and os.environ['GAME'] == 'n7'

with open(sys.argv[1], encoding='sjisx0213') as f, open(sys.argv[2], 'w', encoding='UTF-8') as fout:
    for line in f:
        if not n7:
            line = line.replace('⑩', 'ä')
        line = line.replace('⑪', 'ö')
        line = line.replace('⑫', 'ü')
        line = line.replace('⑬', 'é')
        line = line.replace('⑭', 'à')
        line = line.replace('⑮', 'ö')
        line = line.replace('⑱', '™')
        fout.write(line)
