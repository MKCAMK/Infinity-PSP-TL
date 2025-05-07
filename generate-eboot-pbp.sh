#!/bin/sh

[ -z "$GAME" ] && export GAME=e17
[ -z "$TL_SUFFIX" ] && export TL_SUFFIX=en
[ "$GAME" = "e17" ] && [ "$TL_SUFFIX" = "ru" ] && [ -z "$TL_VARIANT" ] && export TL_VARIANT=dsp2003
[ -n "$TL_VARIANT" ] && TL_VARIANT="-$TL_VARIANT"

SIGN_NP=./tools/sign_np # placeholder
if [ "$(uname)" = "Darwin" ]; then
        SIGN_NP=./tools/sign_np_osx # placeholder
elif [ "$(uname)" = "Linux" ]; then
        SIGN_NP=./tools/sign_np_lin64
fi

if [ "$GAME" = "n7" ]; then
	TID=ULJM05433
elif [ "$GAME" = "r11" ]; then
	TID=ULJM05444
else # e17
	TID=ULJM05437
fi

mkdir -p pbp

$SIGN_NP -pbp iso/${GAME}-${TL_SUFFIX}${TL_VARIANT}.iso pbp/EBOOT-${GAME}-${TL_SUFFIX}${TL_VARIANT}.PBP JP9000-${TID}_00-0000000000000001 0
