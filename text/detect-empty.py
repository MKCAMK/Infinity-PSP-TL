#!/usr/bin/env python

import os

for filename in os.listdir('mac-en-only-utf8'):
    print()
    print(filename)
    with open(os.path.join('mac-psp-en-utf8', filename), encoding='UTF-8') as f_comb:
        comblines = f_comb.readlines()

    with open(os.path.join('mac-en-only-utf8', filename), encoding='UTF-8') as f_en:
        for i, line in enumerate(f_en):
            combindex = i*3+3+1
            if line == '\n' and not (
                comblines[combindex].startswith('%N')
                or comblines[combindex].startswith('%p')
                or comblines[combindex].startswith('%P')
                or comblines[combindex].startswith('%K')
                or comblines[combindex].startswith('%O')
            ):
                print(i+1, combindex+1, ':')
                print(comblines[combindex], end='')
