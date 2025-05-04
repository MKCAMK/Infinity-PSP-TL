#!/bin/sh

if  [ -z "$GIMCONV" ] &&
	[ -e "./tools/GimConv/GimConv.exe" ] &&
	command -v "wine" >/dev/null 2>&1
then
	export GIMCONV="wine ./tools/GimConv/GimConv.exe"
elif command -v "gimconv" >/dev/null 2>&1
then
	export GIMCONV="gimconv"
else
	echo "gimconv not found. set the GIMCONV environment variable accordingly."
	exit 1
fi

for i in bg-*-*/*.PNG ev-*-*/*.PNG; do
	[ -e "$i" ] || continue
	$GIMCONV "$i" -s 120,90 -o "$(basename "$i" .PNG).GIM" || exit 1
done
for i in etc-*-*/*/*.PNG; do
	[ -e "$i" ] || continue
	$GIMCONV "$i" -o "$(basename "$i" .PNG).GIM" || exit 1
done

for i in nowloading/*.png; do
	[ -e "$i" ] || continue
	$GIMCONV "$i" -o "$(basename "$i" .png).gim" || exit 1
done
