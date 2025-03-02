#!/bin/sh

ISODIR=./iso
ORIGINAL_ISO=$ISODIR/Ever17-jap.iso
REPACKED_ISO=$ISODIR/e17-repacked.iso
[ -z "$TL_SUFFIX" ] && TL_SUFFIX="en"
PATCH_FILE=./patch/e17-$TL_SUFFIX.xdelta

rm $PATCH_FILE 2>/dev/null

echo "generating $(basename $PATCH_FILE)"
xdelta3 -v -e -S lzma -9 -B 2147483648 -A -s $ORIGINAL_ISO $REPACKED_ISO $PATCH_FILE || exit 1
echo "done!"
