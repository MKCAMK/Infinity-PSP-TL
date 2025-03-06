#!/bin/bash
# extract all the japanese gametext.
#
GIMCONV="./tools/GimConv/GimConv.exe"
DECOMPRESS="./bin/decompressbip"
REPACK_AFS="./bin/repack_afs"

RES_DIR="e17_iso_extracted/PSP_GAME/USRDIR"
WORK_DIR="./workdir"

unpack_afs () {
	echo Unpacking $1.afs
	$REPACK_AFS $WORK_DIR/$1.afs /dev/null /dev/null e17_$1/ || exit 1
}

mkdir -p $WORK_DIR
mv e17_iso_extracted/PSP_GAME/SYSDIR/BOOT.BIN $WORK_DIR/BOOT.BIN
#mv e17_iso_extracted/PSP_GAME/SYSDIR/EBOOT.BIN $WORK_DIR/EBOOT.BIN

cp $RES_DIR/mac.afs $WORK_DIR/mac.afs
cp $RES_DIR/etc.afs $WORK_DIR/etc.afs
cp $RES_DIR/bg.afs $WORK_DIR/bg.afs
[ -d "e17_x360_BGM" ] && cp $RES_DIR/se.afs $WORK_DIR/se.afs
cp $RES_DIR/init.bin $WORK_DIR/init.bin

PKG=mac
rm -rf e17_$PKG/
unpack_afs $PKG
echo "Decompressing..."
#for i in text/chapters-psp/[A-Z0-9]*_[0-9]*.txt ; do
for i in e17_mac/*.BIP; do
	#f=`basename $i .txt`
	f=`basename $i .BIP`
	#echo "Decompressing $f"
	$DECOMPRESS e17_$PKG/$f{.BIP,.SCN} || exit 1
done
$DECOMPRESS e17_$PKG/SHORTCUT{.BIP,.SCN} || exit 1

PKG=etc
rm -rf e17_$PKG/
unpack_afs $PKG
#for i in $PKG/*.T2P ; do
#	f=`basename $i .T2P`
#	$DECOMPRESS $PKG/$f{.T2P,.GIM} || exit 1
#	$GIMCONV $PKG/$f.GIM -o $f.png -e17
#done
for i in e17_$PKG/*.FOP ; do
	f=`basename $i .FOP`
	$DECOMPRESS e17_$PKG/$f{.FOP,.FNT} || exit 1
done
cp e17_$PKG/FONT00.FNT text/font/FONT00.FNT

#PKG=bg
#rm -rf e17_$PKG/
#unpack_afs $PKG
#for i in e17_$PKG/*.BIP; do
#	f=`basename $i .BIP`
#	#echo "Decompressing $f"
#	$DECOMPRESS e17_$PKG/$f{.BIP,.R11} || exit 1
#done
#for i in e17_$PKG/*.T2P; do
#        f=`basename $i .T2P`
#        #echo "Decompressing $f"
#        $DECOMPRESS e17_$PKG/$f{.T2P,.GIM} || exit 1
#done

cd text/font
python3 ../../py-src/extract_font.py pnghalf || exit 1
cd ../..

$DECOMPRESS $WORK_DIR/init.bin $WORK_DIR/init.dec
