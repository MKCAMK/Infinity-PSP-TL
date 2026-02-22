#!/bin/sh

[ -z "$GAME" ] && export GAME=e17
[ -z "$TL_SUFFIX" ] && export TL_SUFFIX=en

command -v sign_np >/dev/null 2>&1 && SIGN_NP=sign_np || SIGN_NP=./tools/sign_np/sign_np

if [ "$GAME" = "n7" ]; then
	TID=ULJM05433
elif [ "$GAME" = "r11" ]; then
	TID=ULJM05444
else # e17
	TID=ULJM05437
fi

mkdir -p pbp/${GAME}-${TL_SUFFIX}

$SIGN_NP -pbp iso/${GAME}-${TL_SUFFIX}.iso pbp/${GAME}-${TL_SUFFIX}/EBOOT.PBP JP9000-${TID}_00-0000000000000001 0
