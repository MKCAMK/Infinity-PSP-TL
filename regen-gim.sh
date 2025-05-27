#!/bin/sh

if  [ -z "$GIMCONV" ]; then
	if [ -e "./tools/GimConv/GimConv.exe" ] &&
		command -v "wine" >/dev/null 2>&1
	then
		export GIMCONV="wine $PWD/tools/GimConv/GimConv.exe"
	elif command -v "gimconv" >/dev/null 2>&1
	then
		export GIMCONV="gimconv"
	else
		echo "gimconv not found. set the GIMCONV environment variable accordingly."
		exit 1
	fi
fi

for i in assets/bg-*-*/*.PNG assets/ev-*-*/*.PNG; do
	[ -e "$i" ] || continue
	$GIMCONV "$i" -s 120,90 -o "$(basename "$i" .PNG).GIM" || exit 1
done
for i in assets/etc-*-*/*/*.PNG; do
	[ -e "$i" ] || continue
	$GIMCONV "$i" -o "$(basename "$i" .PNG).GIM" || exit 1
done

for i in assets/nowloading/*.png; do
	[ -e "$i" ] || continue
	$GIMCONV "$i" -N -nfi -o "$(basename "$i" .png).gim" || exit 1
done
