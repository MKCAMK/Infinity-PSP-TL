#!/bin/sh
set -e

ISODIR=./iso
ORIGINAL_ISO=$ISODIR/Never7-jap.iso
REPACKED_ISO=$ISODIR/n7-repacked.iso
[ -z "$TL_SUFFIX" ] && TL_SUFFIX="en"
PATCH_FILE=./patch/n7-$TL_SUFFIX.xdelta

rm $PATCH_FILE 2>/dev/null || true
isosize=$(stat -c %s $REPACKED_ISO)

echo generating `basename $PATCH_FILE`
xdelta3 -v -e -S lzma -9 -B $isosize -A -s $ORIGINAL_ISO $REPACKED_ISO $PATCH_FILE
echo "done!"
