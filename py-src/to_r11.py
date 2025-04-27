#!/usr/bin/env python

import sys, struct
from PIL import Image

if len(sys.argv) != 3:
    print("usage: to_r11.py <in.*> <out.r11>")
    sys.exit()

im = Image.open(sys.argv[1])
#im = im.convert("RGB").resize((480, 360), resample=Image.Resampling.NEAREST).quantize(256, method=Image.Quantize.MEDIANCUT)
im = im.convert("P", dither=Image.Dither.NONE)

realwidth, realheight = im.width, im.height
palette = im.getpalette("RGBA")
while len(palette) < 4*256:
    palette.extend([0xff]*4)

width = 512
height = realwidth*realheight//30//30*32*32 // 512

chunks = []
for y in range(realheight // 30):
    for x in range(realwidth // 30):
        chunks.append(im.crop((x*30, y*30, (x+1)*30, (y+1)*30)))

im.close()

new = Image.new("P", (width, height))
new.putpalette(palette, "RGBA")
for y in range(height // 32):
    for x in range(width // 32):
        new.paste(chunks[y*(width//32)+x], (x*32+1, y*32+1))

# this is so, so fucking horrible
for y in range(0, height, 32):
    for x in range(0, width, 32):
        new.paste(new.crop((x+1, y-2, x+1+30, y-2+1)), (x+1, y))
        new.paste(new.crop((x+1, y+32+1, x+1+30, y+32+2)), (x+1, y+31))
for y in range(0, height, 32):
    for x in range(0, width, 32):
        new.paste(new.crop((x-2, y, x-2+1, y+32)), (x, y))
        new.paste(new.crop((x+32+1, y, x+32+2, y+32)), (x+31, y))
new.paste(new.crop((1, 1, width-1, 2)), (1, 0))
new.paste(new.crop((1, height-2, width-1, height-1)), (1, height-1))
new.paste(new.crop((1, 0, 2, height-1)), (0, 0))
new.paste(new.crop((width-2, 0, width-1, height-1)), (width-1, 0))

header = bytearray(0x100)
header[0x0:0x4] = struct.pack("<I", 5)
header[0x4:0x4+4*5] = struct.pack("<IIIII", 0x80, 0x94, 0x100, 0x500, 0x100 + 4*256 + width*height)
header[0x80:0x84] = struct.pack("<HH", 1, 1)
header[0x88:0x8c] = struct.pack("<HH", realwidth, realheight)
header[0x8c:0x90] = struct.pack("<I", 2)
header[0x92:0x94] = struct.pack("<BB", realwidth//30, realheight//30)
with open(sys.argv[2], "wb") as f:
    f.write(header)
    f.write(bytes(palette))
    f.write(bytes(list(new.getdata())))
new.close()
