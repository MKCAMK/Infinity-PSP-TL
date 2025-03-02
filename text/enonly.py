#!/usr/bin/env python

import os

if not os.path.exists('mac-en-only-utf8'): os.mkdir('mac-en-only-utf8')
files = os.listdir('mac-psp-en-utf8')
for filename in files:
    with open(os.path.join('mac-psp-en-utf8', filename), encoding='UTF-8') as f:
        lines = f.readlines()

    del lines[:3]

    enlines = []
    for i in range(len(lines) // 3):
        enlines.append(lines[i*3+2])

    with open(os.path.join('mac-en-only-utf8', filename), 'w', encoding='UTF-8') as f:
        f.writelines(enlines)
