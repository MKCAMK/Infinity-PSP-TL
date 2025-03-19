#!/bin/sh
SRC=./src

CFLAGS="-std=c99 -O2 -Wall -Wextra"

mkdir -p bin
gcc $CFLAGS -o bin/extract_scene_text $SRC/extract_scene_text.c && \
gcc $CFLAGS -o bin/repack_afs $SRC/repack_afs.c && \
gcc $CFLAGS -o bin/decompressbip $SRC/decompressbip.c $SRC/lzss.c && \
gcc $CFLAGS -o bin/compressbip $SRC/compressbip.c $SRC/lzss.c && \
gcc $CFLAGS -o bin/unpack_cnt $SRC/unpack_cnt.c && \
gcc $CFLAGS -o bin/repack_cnt $SRC/repack_cnt.c
