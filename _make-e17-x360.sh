#!/bin/sh

export GAME=e17

./_cleanup-e17-x360.sh && \
./cleanup.sh && \
./compile.sh && \
./unpack-iso.sh && \
./_unpack-xiso.sh && \
./_unpack-afs-e17-x360.sh && \
./unpack-afs.sh && \
./text_1_extract-jap-scenes.sh && \
./repack-all.sh
