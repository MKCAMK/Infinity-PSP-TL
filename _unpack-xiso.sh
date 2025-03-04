#!/bin/sh

ISO_FILE=iso/Ever17-x360.iso
[ ! -f "$ISO_FILE" ] && echo "$ISO_FILE does not exist" && exit
rm -rf e17_x360_iso_extracted
./tools/extract-xiso_lin64 -d e17_x360_iso_extracted -x "$ISO_FILE"
