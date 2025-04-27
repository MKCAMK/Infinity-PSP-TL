#!/bin/sh

[ -z "$TL_SUFFIX" ] && export TL_SUFFIX=en
[ -z "$GAME" ] && export GAME=e17

mkdir -p text/tmp-${GAME}/mac-psp-${TL_SUFFIX}

if [ -d text/chapters-psp-${GAME} ] && [ "$TL_SUFFIX" != "ru" ]; then
	prepare_translation () {
		python3 ./py-src/translation_preproc.py -i text/chapters-psp-${GAME}/$1.txt -o text/tmp-${GAME}/mac-psp-${TL_SUFFIX}/$1.txt -t ${TL_SUFFIX} || exit 1
	}

	for i in text/chapters-psp-${GAME}/*.txt ; do
		f=$(basename $i .txt)
		echo "Preparing chapter: $i"
		prepare_translation $f
	done
else
	prepare_translation () {
		python3 ./py-src/utf8_to_comb.py text/tmp-${GAME}/mac-psp-${TL_SUFFIX}-utf8-wrapped/$1.txt text/tmp-${GAME}/mac-psp-${TL_SUFFIX}/$1.txt ${TL_SUFFIX} || exit 1
	}
	python3 ./py-src/linebreaker.py ${GAME} ${TL_SUFFIX} || exit 1
	for i in text/mac-psp-${GAME}-${TL_SUFFIX}-utf8/*.txt ; do
		f=$(basename $i .txt)
		echo "Preparing chapter: $f"
		prepare_translation $f
	done
fi
