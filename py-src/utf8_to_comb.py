#!/usr/bin/env python3

import os, sys
import r11

if len(sys.argv) != 3 and len(sys.argv) != 4:
    print('usage: utf8_to_comb.py comb_utf8.txt comb.txt [lang]')
    sys.exit()

print(sys.argv[1])

lang = sys.argv[3] if len(sys.argv) == 4 else "en"

with open(sys.argv[1], encoding='UTF-8') as f, open(sys.argv[2], 'wb') as fout:
    for i in range(3):
        headerline = next(f)
        fout.write(headerline.encode('ascii'))
    for i, line in enumerate(f):
        state = i % 3
        if state == 0:
            fout.write(line.encode('ascii'))
        elif state == 1:
            fout.write(r11.str_to_r11_bytes(line, lang, False))
        elif state == 2:
            fout.write(r11.str_to_r11_bytes(line, lang, True))
