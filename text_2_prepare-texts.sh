#!/bin/sh

[ -z "$TL_SUFFIX" ] && export TL_SUFFIX=en
[ -z "$GAME" ] && export GAME=e17

prepare_translation () {
	python3 ./text/utf8tor11.py text/mac-psp-${GAME}-${TL_SUFFIX}-utf8/$1.txt text/tmp-${GAME}/mac-psp-${TL_SUFFIX}/$1.txt || exit 1
}

mkdir -p text/tmp-${GAME}/mac-psp-${TL_SUFFIX}
for i in text/mac-psp-${GAME}-${TL_SUFFIX}-utf8/*.txt ; do
	f=$(basename $i .txt)
	echo "Preparing chapter: $f"
	prepare_translation $f
done
