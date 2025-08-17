#!/bin/sh

# The png files for fonts must be greyscale and have a bit depth of 2.
# This script below helps to batch-convert any png to proper format using ImageMagick 'convert' tool.
# Use it on your fonts or just for reference.

# imagemagick version 7 is recommended

[ -z "$TL_SUFFIX" ] && export TL_SUFFIX=en
TGT="glyphs-${TL_SUFFIX}"

mkdir -p $TGT
for i in "$@"; do
	convert "$i" -colorspace Gray -depth 2 -define png:bit-depth=2 -define png:exclude-chunks=date,time $TGT/$(basename $i)
done
