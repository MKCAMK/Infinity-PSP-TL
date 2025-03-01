#!/bin/sh

./cleanup.sh && \
./compile.sh && \
./unpack-iso.sh && \
./unpack-afs.sh && \
./repack-all.sh
