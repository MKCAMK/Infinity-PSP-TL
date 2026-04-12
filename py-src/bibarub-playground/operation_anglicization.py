#!/usr/bin/env python3

import sys

NAN = 0
JP = 1
EN = 2
CN = 3
RU = 4

f = open(sys.argv[1], "r", encoding="utf-8-sig")
lines = f.readlines()
f.close()
fout = open(sys.argv[1], "w", encoding="utf-8-sig", newline="\n")
state = NAN
for l in lines:
    if l == "\n":
        state = NAN
    elif l.startswith("//"):
        state -= 1
    elif state == EN:
        l = l.replace("\u2015", "\u2014")
        l = l.replace("\u300c", "\u201c")
        l = l.replace("\u300d", "\u201d")
        l = l.replace("\u300e", "\u2018")
        l = l.replace("\u300f", "\u2019")
    elif state == RU:
        l = l.replace("\u2015", "\u2013")
        l = l.replace("\u2014", "\u2013")
        l = l.replace(" - ", " \u2013 ")
        l = l.replace("\u300c", "\u00ab")
        l = l.replace("\u300d", "\u00bb")
        l = l.replace("\u201d", "\u201c")
        if any(x in l for x in "\u300e\u300f"):
            print(l)
    state += 1
    fout.write(l)
fout.close()
