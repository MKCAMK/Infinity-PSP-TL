#!/bin/sh

DECOMPRESS="./bin/decompressbip"
UNPACK_AFS="./bin/unpack_afs"

WORK_DIR="workdir-e17"
RES_DIR="e17_iso_extracted/PSP_GAME/USRDIR"
X360_RES_DIR="e17_x360_iso_extracted/media"

unpack_afs_x360 () {
	echo Unpacking $1.afs
	$UNPACK_AFS $X360_RES_DIR/$1.afs e17_x360_$1/ || exit 1
}

[ ! -d e17_x360_BGM ] && unpack_afs_x360 BGM
mkdir -p $WORK_DIR
cp $RES_DIR/se.afs $WORK_DIR/se.afs
