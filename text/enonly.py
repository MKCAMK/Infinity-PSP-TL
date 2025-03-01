#!/usr/bin/env python

import os

if not os.path.exists('mac-en-only'): os.mkdir('mac-en-only')
files = os.listdir('mac-psp-en')
for filename in files:
    with open(os.path.join('mac-psp-en', filename), encoding='sjisx0213') as f:
        lines = f.readlines()

    for i in range(3):
        lines.pop(0)

    enlines = []
    for i in range(len(lines) // 3):
        i *= 3
        enlines.append(lines[i+2])

    with open(os.path.join('mac-en-only', filename), 'w', encoding='sjisx0213') as f:
        f.writelines(enlines)
