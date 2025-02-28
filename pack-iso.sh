#!/bin/bash
for i in e17_iso_extracted/PSP_GAME/SYSDIR/UPDATE/*.* ; do rm $i; touch $i ; done

mkisofs -U -xa -A "PSP GAME" -V "" -sysid "PSP GAME" -volset "" -p "" -publisher "" -o iso/e17-repacked.iso e17_iso_extracted/
