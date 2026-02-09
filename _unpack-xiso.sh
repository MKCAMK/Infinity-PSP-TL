#!/bin/sh

ISO_FILE=iso/Ever17-x360.iso
command -v extract-xiso >/dev/null 2>&1 && EXTRACT_XISO=extract-xiso || EXTRACT_XISO=tools/extract-xiso/build/extract-xiso
[ ! -f "$ISO_FILE" ] && echo "$ISO_FILE does not exist" && exit
rm -rf e17_x360_iso_extracted

if command -v extract-xiso >/dev/null 2>&1; then
	EXTRACT_XISO=extract-xiso
elif [ -e tools/extract-xiso/build/extract-xiso ]; then
	EXTRACT_XISO=tools/extract-xiso/build/extract-xiso
else
	EXTRACT_XISO=tools/extract-xiso/build/extract-xiso
	rm -rf tools/extract-xiso/build/
	mkdir tools/extract-xiso/build/
	cmake -S tools/extract-xiso -B tools/extract-xiso/build && \
	cmake --build tools/extract-xiso/build -j$(nproc --all) || exit 1
fi
$EXTRACT_XISO -d e17_x360_iso_extracted -x "$ISO_FILE"
