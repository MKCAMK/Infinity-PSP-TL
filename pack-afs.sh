#!/bin/bash
set -e 

ISO_RES_DIR=n7_iso_extracted/PSP_GAME/USRDIR
ISO_BIN_DIR=n7_iso_extracted/PSP_GAME/SYSDIR
WORKDIR=./workdir
COMPRESS=./bin/compressbip
REPACK_AFS=./bin/repack_afs
REPACK_SCENE=text/repack_scene.py
ARMIPS=./tools/armips
PY=python3
if [ `uname` == "Darwin" ]; then
    ARMIPS=./tools/armips_osx
elif [ `uname` == "Linux" ]; then
    ARMIPS=./tools/armips_lin64
fi

# change this for other translations
# set to "en" if unset
if [ -z "${TL_SUFFIX}" ]; then
    export TL_SUFFIX="en"
fi

# Repack mac.afs (texts)
repack_mac_afs () {
	repack_scene () {
		[ $# -ge 2 ] && in=$2 || in=text/tmp/mac-${TL_SUFFIX}-combined-psp/$1.txt
		$REPACK_SCENE $in n7_mac/$1.SCN n7_mac_${TL_SUFFIX}/$1.SCN
		$COMPRESS ./n7_mac_${TL_SUFFIX}/$1.{SCN,BIP}
	}

	mkdir -p n7_mac_${TL_SUFFIX}/
	mkdir -p text/tmp/mac-jp-${TL_SUFFIX}-names-psp

	$PY ./py-src/apply_shortcuts_translation.py text/other-psp-${TL_SUFFIX}/SHORTCUT.SCN.txt n7_mac/SHORTCUT.SCN n7_mac_${TL_SUFFIX}/SHORTCUT.SCN ${TL_SUFFIX}
	$PY ./py-src/apply_shortcuts_translation.py text/other-psp-${TL_SUFFIX}/APPEND.SCN.txt n7_mac/APPEND.SCN n7_mac_${TL_SUFFIX}/APPEND.SCN ${TL_SUFFIX} append
	# cp -f n7_mac/SHORTCUT.SCN n7_mac_${TL_SUFFIX}/SHORTCUT.SCN
	$COMPRESS ./n7_mac_${TL_SUFFIX}/SHORTCUT.{SCN,BIP}
	$COMPRESS ./n7_mac_${TL_SUFFIX}/APPEND.{SCN,BIP}

	for i in text/tmp/mac-${TL_SUFFIX}-combined-psp/*.txt ; do
		echo Repacking $i
		repack_scene `basename $i .txt` #& WAITPIDS="$! "$WAITPIDS
	done
	for i in text/tmp/mac-jp-psp/USER*.txt ; do
		[ `basename $i` = "USER08.txt" ] && continue
		echo Patching $i
		f=`basename $i .txt`
		$PY ./py-src/patch_speaker.py $i text/tmp/mac-jp-${TL_SUFFIX}-names-psp/$f.txt
		repack_scene $f text/tmp/mac-jp-${TL_SUFFIX}-names-psp/$f.txt
	done
	# wait $WAITPIDS &> /dev/null
	echo "Finished repacking scenes"

	echo "Fixing SL2D4_3.SCN"
	printf "\x05" | dd oflag=seek_bytes conv=notrunc seek=160 of=./n7_mac_${TL_SUFFIX}/SL2D4_3.SCN
	$COMPRESS ./n7_mac_${TL_SUFFIX}/SL2D4_3.{SCN,BIP}

	$REPACK_AFS $WORKDIR/mac.afs $WORKDIR/mac-repacked.afs ./n7_mac_${TL_SUFFIX}
	mv -f $WORKDIR/mac-repacked.afs $ISO_RES_DIR/mac.afs
}

# Compose and repack font
# compose_font builds the font file
compose_font () {
	mkdir -p n7_etc_${TL_SUFFIX}
	cd text/font/
	cp -f glyphs-new/* glyphs/
	if [ "cn" == "${TL_SUFFIX}" ]; then
		7z x glyphs-cn.7z
		mv -f glyphs-cn/* glyphs/
	fi
	$PY ../../py-src/extract_font.py repack glyphs/
	cp FONT00.NEW ../../n7_etc_${TL_SUFFIX}/FONT00.NEW
	cd ../..
}

# repack_etc_afs repacks etc.afs with the new font file from "compose_font"
repack_etc_afs () {
	compose_font

	if [ -f n7_etc_${TL_SUFFIX}/FONT00.NEW ]; then
	$COMPRESS n7_etc_${TL_SUFFIX}/FONT00.NEW n7_etc_${TL_SUFFIX}/FONT00.FOP
	$REPACK_AFS $WORKDIR/etc.afs $WORKDIR/etc-repacked.afs n7_etc_${TL_SUFFIX}
	mv -f $WORKDIR/etc-repacked.afs $ISO_RES_DIR/etc.afs
	fi
}

# Repack init.bin
repack_init_bin () {
	echo "Applying translation to init.bin"
	# Apply init.bin strings
	$PY ./py-src/apply_init_translation.py text/other-psp-${TL_SUFFIX}/init.bin.utf8.txt workdir/init.dec workdir/init.dec.${TL_SUFFIX} ${TL_SUFFIX}

	INIT_SRC=$WORKDIR/init.dec.${TL_SUFFIX}
	if [ ! -f $INIT_SRC ]; then
		# If modified file does not exist, just repack the original one.
		# Used for testing purposes
		INIT_SRC=$WORKDIR/init.dec
	fi
	echo "Compressing $INIT_SRC -> $WORKDIR/init.${TL_SUFFIX}.bin"
	$COMPRESS $INIT_SRC $WORKDIR/init.${TL_SUFFIX}.bin
	mv -f $WORKDIR/init.${TL_SUFFIX}.bin $ISO_RES_DIR/init.bin
}

# Patch BOOT.BIN
patch_boot_bin () {
	# Apply translation
	echo "Applying translation to BOOT"
	$PY ./py-src/apply_boot_translation.py text/other-psp-${TL_SUFFIX}/BOOT.utf8.txt workdir/BOOT.BIN workdir/BOOT.BIN.${TL_SUFFIX} ${TL_SUFFIX}

	echo "Applying other patches to BOOT"
	mv -f $WORKDIR/BOOT.BIN.${TL_SUFFIX} $WORKDIR/BOOT.BIN.patched
	if [ "cn" == "${TL_SUFFIX}" ]; then
		$ARMIPS src/boot-patches-cn.asm -root workdir/
	else
		$ARMIPS src/boot-patches.asm -root workdir/
	fi
	mv -f $WORKDIR/BOOT.BIN.patched $WORKDIR/BOOT.BIN.${TL_SUFFIX}

	rm -f $ISO_BIN_DIR/BOOT.BIN
	rm -f $ISO_BIN_DIR/EBOOT.BIN
	cp -f $WORKDIR/BOOT.BIN.${TL_SUFFIX} ./$ISO_BIN_DIR/BOOT.BIN
	# I think EBOOT is supposed to be encrypted, but it works fine without it on emulators and on a real psp
	cp -f ./$ISO_BIN_DIR/BOOT.BIN ./$ISO_BIN_DIR/EBOOT.BIN
}

# Actually running above functions
repack_mac_afs
repack_etc_afs
repack_init_bin
patch_boot_bin
