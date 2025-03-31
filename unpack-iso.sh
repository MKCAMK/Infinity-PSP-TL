#!/bin/sh

[ -z "$GAME" ] && export GAME=e17

if [ "$GAME" = "n7" ]; then
	ISO_FILE=iso/Never7-jap.iso
elif [ "$GAME" = "r11" ]; then
	ISO_FILE=iso/Remember11-jap.iso
else
	ISO_FILE=iso/Ever17-jap.iso
fi

#isoinfo -f -i $ISO_FILE | nl -nln -s ";" | awk -F ";" '{print substr($2,2) " -" $1}' > iso/sort_file
echo "Extracting ISO '$ISO_FILE'."
7z x -y $ISO_FILE -o${GAME}_iso_extracted/
