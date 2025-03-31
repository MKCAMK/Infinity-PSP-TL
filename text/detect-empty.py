#!/usr/bin/env python

import os

game = os.environ['GAME'] if 'GAME' in os.environ else 'e17'

for filename in os.listdir(f'mac-psp-{game}-en-utf8'):
    print()
    print(filename)
    with open(os.path.join(f'mac-psp-{game}-en-utf8', filename), encoding='UTF-8') as f_comb:
        comblines = f_comb.readlines()

    del comblines[:3]

    for i in range(len(comblines) // 3):
        index = i*3+3+1
        enline = comblines[i*3+2]
        jpline = comblines[i*3+1]
        if enline == '\n' and not (
            jpline.startswith('%N')
            or jpline.startswith('%p')
            or jpline.startswith('%P')
            or jpline.startswith('%K')
            or jpline.startswith('%O')
        ):
            print(index+1, ':')
            print(jpline, end='')
