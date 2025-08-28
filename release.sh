#!/bin/sh

./make.sh && \
./generate-eboot-pbp.sh && \
./generate-patch.sh
