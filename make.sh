#!/bin/sh

[ -z "$GAME" ] && export GAME=e17
[ -z "$TL_SUFFIX" ] && export TL_SUFFIX=en

./cleanup.sh && \
./compile.sh && \
./unpack-iso.sh && \
./unpack-afs.sh && \
./text_1_extract-jap-scenes.sh && \
./text_2_prepare-texts.sh && \
./pack-afs.sh && \
./pack-iso.sh
