#!/bin/sh

./_cleanup-e17-x360.sh
for i in e17 n7 r11; do
	GAME=$i ./cleanup.sh
done
