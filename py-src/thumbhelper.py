#!/usr/bin/env python3

import os
import sys
from PIL import Image

# regular thumbnails are 120x90, and images are usually 480x360
scalefactor = 120/480

gimconv = os.environ["GIMCONV"] if "GIMCONV" in os.environ else "gimconv"

if len(sys.argv) != 2:
    print("usage: thumbhelper.py <in.*>")
    sys.exit()

inpath = sys.argv[1]
imname = os.path.basename(os.path.splitext(inpath)[0])
temppath = os.path.splitext(inpath)[0] + ".TEMP.PNG"
outpath = imname + ".GIM"

with Image.open(inpath) as im:
    im.resize((round(x*scalefactor) for x in im.size)).quantize(256).save(temppath)
os.system(gimconv + " \"" + temppath + "\" -o \"" + outpath + "\"")
os.remove(temppath)
