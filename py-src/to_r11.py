#!/usr/bin/env python3


# to_r11.py

# HOPEFULLY capable of properly converting
# images into the "R11" format, as found in
# Infinity visual novels on the PSP.

# sprite converstion is not supported.

import sys, struct
from PIL import Image

def flatten(xss):
    return [x for xs in xss for x in xs]

def main():
    if len(sys.argv) != 3:
        print("usage: to_r11.py <in.*> <out.r11>")
        sys.exit()

    im = Image.open(sys.argv[1])
    ispaletted = (im.mode == "P")
    if ispaletted:
        immode = "P"
        palette = im.getpalette("RGBA")
        while len(palette) < 4*256:
            palette.extend([0xff]*4)
    else:
        immode = "RGBA"
        im = im.convert(immode)

    realwidth, realheight = im.size

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

    paddedim = Image.new(immode, (paddedwidth, paddedheight))
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

    new = Image.new(immode, (width, height))
    if ispaletted:
        new.putpalette(palette, "RGBA")
    for y in range(height // 32):
        for x in range(width // 32):
            i = y*(width//32)+x
            if len(chunks) <= i: break
            new.paste(chunks[i], (x*32, y*32))

    datasize = (0x100 + 256*4 + width*height) if ispaletted else (0x100 + width*height * 4)
    header = bytearray(0x100)
    header[0x0:0x4] = struct.pack("<I", 5)
    header[0x4:0x4+4*5] = struct.pack("<5I", 0x80, 0x94, 0x100, 0x500 if ispaletted else 0x100, datasize)
    header[0x80:0x84] = struct.pack("<2H", 1, ispaletted)
    header[0x88:0x8c] = struct.pack("<2H", realwidth, realheight)
    header[0x8c:0x8e] = struct.pack("<H", 2)
    header[0x92:0x94] = struct.pack("<2B", xchunks, ychunks)
    with open(sys.argv[2], "wb") as f:
        f.write(header)
        if ispaletted:
            f.write(bytes(palette))
            newdata = bytes(list(new.getdata()))
        else:
            newdata = bytes(flatten(list(new.getdata())))
        f.write(newdata)
    new.close()

if __name__ == "__main__":
    main()
