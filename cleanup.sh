#!/bin/sh

[ -z "$GAME" ] && export GAME=e17
[ -z "$TL_SUFFIX" ] && export TL_SUFFIX=en

rm -rf ${GAME}_mac/ ${GAME}_etc/ ${GAME}_iso_extracted/ ${GAME}_mac_${TL_SUFFIX}/ ${GAME}_etc_${TL_SUFFIX}/ ${GAME}_se/ ${GAME}_se_mod/ ${GAME}_bg/ ${GAME}_bg_${TL_SUFFIX}/
rm -rf bin/
rm -rf workdir-${GAME}
rm -rf text/mac-${GAME}-${TL_SUFFIX}-only*/
rm -rf text/tmp-${GAME}
rm -rf text/font/${GAME} text/font/${GAME}-${TL_SUFFIX}
rm -f patch/${GAME}-${TL_SUFFIX}.xdelta
rm -f iso/${GAME}-${TL_SUFFIX}.iso
rm -f pbp/EBOOT-${GAME}-${TL_SUFFIX}.PBP
