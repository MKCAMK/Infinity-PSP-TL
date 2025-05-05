#!/bin/sh

[ -z "$GAME" ] && export GAME=e17
[ -z "$TL_SUFFIX" ] && export TL_SUFFIX=en
[ "$GAME" = "e17" ] && [ "$TL_SUFFIX" = "ru" ] && [ -z "$TL_VARIANT" ] && export TL_VARIANT=dsp2003

./cleanup.sh && \
./compile.sh && \
./unpack-iso.sh && \
./unpack-afs.sh && \
./text_1_extract-jap-scenes.sh && \
./repack-all.sh
