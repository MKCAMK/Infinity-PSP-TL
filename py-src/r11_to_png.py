#!/usr/bin/env python3


# r11_to_png.py

# capable of correctly converting most BG and CG images
# from the "R11" format into 8bpp PNG.
# sprite conversion is not implemented -- sprites
# will be extracted as unordered 30x30 chunks in one image.
# most sprites from n7, however, can be extracted with this
# script, as they are just CGs with transparency.

from PIL import Image
import sys, os, struct

if len(sys.argv) <= 1:
    print("usage: r11_to_png.py <INPUT.R11> [OUTPUT.PNG]")
    sys.exit()

outpath = sys.argv[2] if len(sys.argv)>=3 else os.path.splitext(sys.argv[1])[0] + ".PNG"

with open(sys.argv[1], "rb") as f:
    data = f.read()

marker = struct.unpack("<I", data[:4])[0]
count = marker - 3
palettepointer = 4 + count*4
pixelspointer = palettepointer + 4

paletteaddr = struct.unpack("<I", data[palettepointer:palettepointer+4])[0]
pixelsaddr = struct.unpack("<I", data[pixelspointer:pixelspointer+4])[0]
palette = data[paletteaddr:paletteaddr+4*256]
pixels = data[pixelsaddr:]

(realwidth, realheight) = struct.unpack("<HH", data[0x88:0x8c])
width = 512
height = len(pixels) // width

alphabstr = b""
for i in range(0, len(palette), 4):
    alphabstr += palette[i+3].to_bytes()

with Image.new("P", (realwidth, realheight)) as hr, Image.new("P", (width, height)) as im:
    im.putdata(pixels)
    chunks = []
    for y in range(0, height, 32):
        for x in range(0, width, 32):
            chunks.append(im.crop((x+1, y+1, x+1+30, y+1+30)))
    for y in range((realheight+29) // 30):
        for x in range((realwidth+29) // 30):
            hr.paste(chunks[y*((realwidth+29)//30)+x], (x*30, y*30))
    hr.putpalette(palette, "RGBA")
    hr.save(outpath, transparency=alphabstr)
