#!/bin/bash

[ -z "$GAME" ] && export GAME=e17
[ -z "$TL_SUFFIX" ] && export TL_SUFFIX=en
[ "$GAME" = "e17" ] && [ "$TL_SUFFIX" = "ru" ] && [ -z "$TL_VARIANT" ] && export TL_VARIANT=dsp2003
[ -n "$TL_VARIANT" ] && TL_VARIANT="-$TL_VARIANT"

for i in ${GAME}_iso_extracted/PSP_GAME/SYSDIR/UPDATE/*.* ; do echo > $i ; done
[ -d "xmb-${GAME}" ] && cp xmb-${GAME}/* ${GAME}_iso_extracted/PSP_GAME

mkisofs -U -xa -A "PSP GAME" -V "" -sysid "PSP GAME" -volset "" -p "" -publisher "" -o iso/${GAME}-${TL_SUFFIX}${TL_VARIANT}.iso ${GAME}_iso_extracted/
