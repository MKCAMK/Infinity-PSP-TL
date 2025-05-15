#!/usr/bin/env python3


# to_r11.py

# HOPEFULLY capable of properly converting
# images into the "R11" format, as found in
# Infinity visual novels on the PSP.

# sprite converstion is not supported.

# the script accepts any image formats, but it
# is recommended that you use 8bpp paletted PNG
# images. if you would like to use other image
# formats, check out the commented-out "quantize"
# command.

import sys, struct
from PIL import Image

if len(sys.argv) != 3:
    print("usage: to_r11.py <in.*> <out.r11>")
    sys.exit()

im = Image.open(sys.argv[1])
#im = im.convert("RGB").resize((480, 360), resample=Image.Resampling.NEAREST).quantize(256, method=Image.Quantize.MEDIANCUT)
im = im.convert("PA", dither=Image.Dither.NONE)

realwidth, realheight = im.width, im.height
palette = im.getpalette("RGBA")
while len(palette) < 4*256:
    palette.extend([0xff]*4)

widthrem = realwidth % 30
heightrem = realheight % 30
paddedwidth = realwidth // 30 * 32
paddedheight = realheight // 30 * 32
if widthrem:
    paddedwidth += widthrem + 2
if heightrem:
    paddedheight += heightrem + 2
xchunks = (paddedwidth + 31) // 32
ychunks = (paddedheight + 31) // 32

width = 512
height = (xchunks*ychunks*32*32 // width + 31) // 32 * 32

paddedim = Image.new("P", (paddedwidth, paddedheight))
for y in range(ychunks):
    for x in range(xchunks):
        paddedim.paste(im.crop((x*30, y*30, (x+1)*30, (y+1)*30)), (x*32+1, y*32+1))

im.close()

# this is so, so fucking horrible
for y in range(0, ychunks*32, 32):
    paddedim.paste(paddedim.crop((1, y-2, paddedwidth-1, y-1)), (1, y))
    paddedim.paste(paddedim.crop((1, y+32+1, paddedwidth-1, y+32+2)), (1, y+31))
for x in range(0, xchunks*32, 32):
    paddedim.paste(paddedim.crop((x-2, 1, x-1, paddedheight-1)), (x, 1))
    paddedim.paste(paddedim.crop((x+32+1, 1, x+32+2, paddedheight-1)), (x+31, 1))
paddedim.paste(paddedim.crop((1, 1, paddedwidth-1, 2)), (1, 0))
paddedim.paste(paddedim.crop((1, paddedheight-2, paddedwidth-1, paddedheight-1)), (1, paddedheight-1))
paddedim.paste(paddedim.crop((1, 0, 2, paddedheight)), (0, 0))
paddedim.paste(paddedim.crop((paddedwidth-2, 0, paddedwidth-1, paddedheight)), (paddedwidth-1, 0))

chunks = []
for y in range(ychunks):
    for x in range(xchunks):
        chunks.append(paddedim.crop((x*32, y*32, (x+1)*32, (y+1)*32)))

paddedim.close()

new = Image.new("P", (width, height))
new.putpalette(palette, "RGBA")
for y in range(height // 32):
    for x in range(width // 32):
        i = y*(width//32)+x
        if len(chunks) <= i: break
        new.paste(chunks[i], (x*32, y*32))

header = bytearray(0x100)
header[0x0:0x4] = struct.pack("<I", 5)
header[0x4:0x4+4*5] = struct.pack("<IIIII", 0x80, 0x94, 0x100, 0x500, 0x100 + 4*256 + width*height)
header[0x80:0x84] = struct.pack("<HH", 1, 1)
header[0x88:0x8c] = struct.pack("<HH", realwidth, realheight)
header[0x8c:0x90] = struct.pack("<I", 2)
header[0x92:0x94] = struct.pack("<BB", xchunks, ychunks)
with open(sys.argv[2], "wb") as f:
    f.write(header)
    f.write(bytes(palette))
    f.write(bytes(list(new.getdata())))
new.close()
