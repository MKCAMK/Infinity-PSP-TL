#!/bin/sh

DECOMPRESS="./bin/decompressbip"
REPACK_AFS="./bin/repack_afs"

RES_DIR="e17_iso_extracted/PSP_GAME/USRDIR"
X360_RES_DIR="e17_x360_iso_extracted/media"

unpack_afs_x360 () {
	echo Unpacking $1.afs
	$REPACK_AFS $X360_RES_DIR/$1.afs /dev/null /dev/null e17_x360_$1/ || exit 1
}

unpack_afs () {
        echo Unpacking $1.afs
        $REPACK_AFS $RES_DIR/$1.afs /dev/null /dev/null e17_$1/ || exit 1
}

[ ! -d e17_x360_BGM ] && unpack_afs_x360 BGM
unpack_afs se
