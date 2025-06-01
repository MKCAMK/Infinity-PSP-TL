#!/usr/bin/env python3

import os, sys
from PIL import Image

gimconv = os.environ["GIMCONV"] if "GIMCONV" in os.environ else "gimconv"

if len(sys.argv) != 2:
    print("usage: thumbhelper.py <in.*>")
    sys.exit()

inpath = sys.argv[1]
temppath = os.path.splitext(inpath)[0] + ".TEMP.PNG"
outpath = os.path.basename(os.path.splitext(inpath)[0]) + ".GIM"

with Image.open(inpath) as im:
    im.resize((120, 90)).quantize(256).save(temppath)
os.system(gimconv + " \"" + temppath + "\" -o \"" + outpath + "\"")
os.remove(temppath)
