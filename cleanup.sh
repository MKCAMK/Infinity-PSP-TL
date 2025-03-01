#!/bin/sh

rm -rf e17_mac/ e17_etc/ e17_iso_extracted/ e17_mac_en/ e17_etc_en/
rm -rf bin/
rm -f workdir/{mac.afs,etc.afs,init.*,BOOT.BIN*}
rm -rf text/mac-en-only
rm -rf text/tmp
rm -f text/font/FONT00.{FNT,mod}
rm -rf text/font/glyphs
