#!/bin/bash

# Extracts text from scenes (aka chapters, main text) to text files with the original encoding.
# Before running this, iso and afs packages must be unpacked, so that .SCN files are present in ${GAME}_mac/ folder.
. ./text_1_extract-jap-scenes-func.sh

for i in ${GAME}_mac/[A-Z0-9]*_[0-9]*.SCN ; do
	extract_scene $(basename $i .SCN)
done
if [ "$GAME" = "n7" ]; then
	for i in n7_mac/{C_IL2D1A,C_IL2D7,C_YUKA[0-6],DC_*,[A-Z]CYARI,HL1D6,HL2D[2-4],HL2D7,[A-Z]POOL,HTURI,HUMI,IKIMO,ILUNA,KJINJYA,KL2D3,KL2D7,L1D2E,L1D4E,L1D4N,OP,SCOTTAGE,SL1D6,SL2D3,SL2D[5-7],USER[0-9]*,YHANA,YL2D[5-6]}.SCN ; do
		extract_scene $(basename $i .SCN)
	done
fi
echo "Done."
