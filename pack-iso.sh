#!/bin/bash

[ -z "$GAME" ] && export GAME=e17

for i in ${GAME}_iso_extracted/PSP_GAME/SYSDIR/UPDATE/*.* ; do rm $i; touch $i ; done
[ -d "xmb-${GAME}" ] && cp xmb-${GAME}/* ${GAME}_iso_extracted/PSP_GAME

mkisofs -U -xa -A "PSP GAME" -V "" -sysid "PSP GAME" -volset "" -p "" -publisher "" -o iso/${GAME}-repacked.iso ${GAME}_iso_extracted/
