#!/bin/sh

./_cleanup.sh && \
./cleanup.sh && \
./compile.sh && \
./unpack-iso.sh && \
./_unpack-xiso.sh && \
./_unpack-afs.sh && \
./unpack-afs.sh && \
./repack-all.sh
