#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import struct

def main():

  game = os.environ["GAME"] if "GAME" in os.environ else "e17"

  if game == "r11":
    text_areas = [
      [0x11FF50, 0x11FFA4],
      [0x120AC8, 0x120AEF],
      [0x121118, 0x1217d4],
      [0x121930, 0x1243d0],
      [0x12449c, 0x12465c],
      [0x12483c, 0x128698],
      [0x12b948, 0x12b9a4],
      [0x136AC0, 0x136B21]
    ]
  elif game == "n7":
    text_areas = [
      [0x11BF28, 0x11BF7C],
      [0x11CAA0, 0x11CAC7],
      [0x11d0c4, 0x11d794],
      [0x11d8f0, 0x11fa50],
      [0x11fb1c, 0x11fb8c],
      [0x11fd6c, 0x123bc0],
      [0x126dd0, 0x126e2c],
      [0x131AB8, 0x131B15]
    ]
  else: # e17
    text_areas = [
      [0x11E480, 0x11E4D4],
      [0x11EFF8, 0x11F01F],
      [0x11F648, 0x11FCF5],
      [0x11FE58, 0x12204C],
      [0x122118, 0x122188],
      [0x122368, 0x1261C1],
      [0x129448, 0x1294A1],
      [0x134174, 0x1341C2]
    ]

  path = sys.argv[1] if len(sys.argv) > 1 else "BOOT.BIN"
  outpath = path + "." + game + ".jp.txt"

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
