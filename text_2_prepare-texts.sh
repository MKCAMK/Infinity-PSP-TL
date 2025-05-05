#!/bin/sh

[ -z "$GAME" ] && export GAME=e17
[ -z "$TL_SUFFIX" ] && export TL_SUFFIX=en
[ "$GAME" = "e17" ] && [ "$TL_SUFFIX" = "ru" ] && [ -z "$TL_VARIANT" ] && export TL_VARIANT=dsp2003

mkdir -p text/tmp-${GAME}/mac-psp-${TL_SUFFIX}

if [ -d text/chapters-psp-${GAME} ] && [ "$TL_SUFFIX" != "ru" ]; then
	for i in text/chapters-psp-${GAME}/*.txt ; do
		f=$(basename $i .txt)
		echo "Preparing chapter: $i"
		python3 ./py-src/translation_preproc.py -i $i -o text/tmp-${GAME}/mac-psp-${TL_SUFFIX}/$1.txt -t ${TL_SUFFIX} || exit 1
	done
else
	if [ -n "$TL_SUFFIX" ]; then
		python3 ./py-src/linebreaker.py ${GAME} ${TL_SUFFIX} "text/mac-psp-${GAME}-${TL_SUFFIX}-${TL_VARIANT}-utf8" || exit 1
	else
		python3 ./py-src/linebreaker.py ${GAME} ${TL_SUFFIX} || exit 1
	fi
	for i in text/tmp-${GAME}/mac-psp-${TL_SUFFIX}-utf8-wrapped/*.txt ; do
		f=$(basename $i .txt)
		echo "Preparing chapter: $f"
		python3 ./py-src/utf8_to_comb.py $i text/tmp-${GAME}/mac-psp-${TL_SUFFIX}/$f.txt ${TL_SUFFIX} || exit 1
	done
fi
