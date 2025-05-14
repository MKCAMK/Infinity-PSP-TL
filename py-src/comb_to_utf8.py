#!/usr/bin/env python3

import os, sys
import r11

if len(sys.argv) != 3 and len(sys.argv) != 4:
    print('usage: comb_to_utf8.py comb.txt comb_utf8.txt [lang]')
    sys.exit()

print(sys.argv[1])

lang = sys.argv[3] if len(sys.argv) == 4 else "en"

with open(sys.argv[1], "rb") as f, open(sys.argv[2], 'w', encoding='UTF-8') as fout:
    for i in range(3):
        headerline = next(f)
        fout.write(headerline.decode('ascii'))
    for i, line in enumerate(f):
        if i % 3 == 0:
            fout.write(line.decode('ascii'))
            continue
        fout.write(r11.r11_bytes_to_str(line, lang))
