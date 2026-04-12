#!/usr/bin/env python3
import os
import sys
import math
import struct

duration_table_offset = 0x5800
adx_header = b"\x80\x00"

with open(sys.argv[1], "rb") as f_init:
    init_data = bytearray(f_init.read())

for fname in os.listdir("e17_se_mod"):
    name, ext = os.path.splitext(fname)
    if not (ext == ".ADX" and name.startswith("ADX") and name.endswith("NL")): continue
    i = int(name[3:5])-1
    pos = duration_table_offset+i*16
    f = open(os.path.join("e17_se_mod", fname), "rb")
    if f.read(len(adx_header)) != adx_header:
        f.close()
        sys.exit(fname+" not adx")
    f.seek(0x8)
    sample_rate, samples = struct.unpack(">2I", f.read(8))
    f.close()
    duration = math.ceil(samples/sample_rate)
    init_data[pos:pos+4] = struct.pack("<I", duration*60)

with open(sys.argv[1], "wb") as f_init:
    f_init.write(init_data)
