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
    count_jp = lines[i+1].count('%')
    count_en = lines[i+2].count('%')
    if count_jp != count_en:
        print('line {}: mismatch! {} in jp, {} in en'.format(i+3+1, count_jp, count_en))
        print(lines[i+1], lines[i+2], sep='')
