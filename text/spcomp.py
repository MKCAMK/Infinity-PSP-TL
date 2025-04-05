#!/usr/bin/env python

import sys

if len(sys.argv) != 2:
    print('usage: spcomp.py scene.txt')
    sys.exit()

with open(sys.argv[1], encoding='UTF-8') as f:
    lines = f.readlines()

del lines[:3]

for i in range(len(lines) // 3):
    i *= 3
    if lines[i+2] == '\n': continue
    jp_line = lines[i+1].replace('%N', '')
    en_line = lines[i+2].replace('%N', '')
    count_jp = jp_line.count('%')
    count_en = en_line.count('%')
    if count_jp != count_en:
        print('line {}: mismatch! {} in jp, {} in en'.format(i+3+1, count_jp, count_en))
        print(lines[i+1], lines[i+2], sep='')
