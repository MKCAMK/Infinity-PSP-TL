#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import struct

def main():

  text_areas = [
    [0x11F649, 0x11FCF5],
    [0x11FE58, 0x12204C],
    [0x122118, 0x122188],
    [0x122368, 0x1261C1],
    [0x129448, 0x1294A1]
  ]

  path = sys.argv[1] if len(sys.argv) > 1 else "BOOT.BIN"
  outpath = path + ".jp.txt"

  f=open(path, "rb")
  data_bytes = f.read()
  f.close()

  f = open(outpath, "wb")

  strings = []
  positions = []
  for text_area in text_areas:
    start = len(strings)
    strings[start:] = data_bytes[text_area[0]:text_area[1]].split(b'\x00')
    # calc positions
    pos = text_area[0]
    for stringbytes in strings[start:]:
      positions.append(pos)
      pos += len(stringbytes) + 1

  for i, s in enumerate(strings):
    if s != b'':
      f.write(';{:x};{:d};'.format(positions[i], len(s)|3).encode()
              + s + b'\n\n')
  f.close()


if __name__ == '__main__':
  main();
