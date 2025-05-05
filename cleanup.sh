#!/bin/sh

[ -z "$GAME" ] && export GAME=e17
[ -z "$TL_SUFFIX" ] && export TL_SUFFIX=en
[ "$GAME" = "e17" ] && [ "$TL_SUFFIX" = "ru" ] && [ -z "$TL_VARIANT" ] && export TL_VARIANT=dsp2003

[ -d bg-${GAME}-${TL_SUFFIX} ] && rm -rf bg-${GAME}-${TL_SUFFIX}/*.R11
[ -d ev-${GAME}-${TL_SUFFIX} ] && rm -rf ev-${GAME}-${TL_SUFFIX}/*.R11
for i in ev bg etc mac ; do rm -rf ${GAME}_${i}/; rm -rf ${GAME}_${i}_${TL_SUFFIX}/; done
rm -rf ${GAME}_se/ ${GAME}_se_mod/ ${GAME}_iso_extracted/
rm -rf bin/
rm -rf workdir-${GAME}
rm -rf text/mac-${GAME}-${TL_SUFFIX}-only*/
rm -rf text/tmp-${GAME}
rm -rf text/font/${GAME} text/font/${GAME}-${TL_SUFFIX}
rm -f patch/${GAME}-${TL_SUFFIX}.xdelta patch/${GAME}-${TL_SUFFIX}-${TL_VARIANT}.xdelta
rm -f iso/${GAME}-${TL_SUFFIX}.iso iso/${GAME}-${TL_SUFFIX}-${TL_VARIANT}.iso
rm -f pbp/EBOOT-${GAME}-${TL_SUFFIX}.PBP pbp/EBOOT-${GAME}-${TL_SUFFIX}-${TL_VARIANT}.PBP
