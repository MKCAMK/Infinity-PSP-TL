#!/bin/sh

ISO_FILE=iso/Ever17-jap.iso

#isoinfo -f -i iso/Ever17-jap.iso | nl -nln -s ";" | awk -F ";" '{print substr($2,2) " -" $1}' > iso/sort_file
echo "Extracting ISO '$ISO_FILE'."
7z x -y $ISO_FILE -oe17_iso_extracted/
