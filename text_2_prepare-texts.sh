#!/bin/sh

# set to "en" if unset
if [ -z "${TL_SUFFIX}" ]; then
    export TL_SUFFIX="en"
fi

prepare_translation () {
	python3 ./text/utf8toe17.py text/mac-psp-${TL_SUFFIX}-utf8/$1.txt text/tmp/mac-psp-${TL_SUFFIX}/$1.txt || exit 1
}

mkdir -p text/tmp/mac-psp-${TL_SUFFIX}
for i in text/mac-psp-${TL_SUFFIX}-utf8/*.txt ; do
	f=`basename $i .txt`
	echo "Preparing chapter: $f"
	prepare_translation $f
done
