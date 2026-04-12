#!/usr/bin/env python3

import sys
import struct

import r11

f = open(sys.argv[1], "rb")
fout = open(sys.argv[2], "w", encoding="utf-8-sig")

f.seek(0x88)
f.seek(struct.unpack("<I", f.read(4))[0])

entries = []
while (entry := struct.unpack("<2I", f.read(8)))[0] != 0:
    entries.append(entry)

i = -1
for e in entries:
    if e[1] != i:
        i = e[1]
        fout.write(f"{i}:\n")
    f.seek(e[0])
    b = b""
    while b'\0' not in b: b += f.read(128)
    fout.write(r11.r11_bytes_to_str(b.split(b'\0')[0]))
    fout.write('\n')
f.close()
fout.close()
