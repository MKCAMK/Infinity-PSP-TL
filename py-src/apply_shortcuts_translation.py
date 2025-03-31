#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re

import r11


table_offset = 0x10
table_entry_sz = 0x34

addr_text_e17 = [0x694, 0x1582]
addr_text_r11 = [0x62c, 0xf2e]
addr_text_n7 = [0xde4, 0x2eca]
addr_text_n7_append = [0x6c8, 0xe99]

def main():

  if not 4 <= len(sys.argv) <= 6:
    exit("Usage: %s translation.txt in.SHORTCUTS.SCN out.SHORTCUTS.SCN [translation_lang] [-a]"%(sys.argv[0]))

  txt     = sys.argv[1]
  bin_in  = sys.argv[2]
  bin_out = sys.argv[3]
  encoding_table_lang = sys.argv[4] if len(sys.argv) >= 5 else "en"

  game = os.environ["GAME"] if "GAME" in os.environ else "e17"

  if len(sys.argv) == 6 and sys.argv[5] == "-a" and game == "n7":
    addr_text = addr_text_n7_append
  elif game == "r11":
    addr_text = addr_text_r11
  elif game == "n7":
    addr_text = addr_text_n7
  else:
    addr_text = addr_text_e17

  table_entry_count = (addr_text[0] - table_offset) // table_entry_sz
  shortcut_data_offset = (addr_text[1] + 3) & ~3

  txt_lines = r11.readlines_utf8_crop_crlf(txt)
  with open(bin_in, "rb") as f_scn:
    scn_bytes = bytearray(f_scn.read())


  head = scn_bytes[:addr_text[0]]
  shortcut_data = scn_bytes[shortcut_data_offset:]

  head_mv = memoryview(head)
  head_int = head_mv.cast("I")

  body = bytearray()

  jp_pattern = re.compile("^;([\\da-fA-F]*);([\\d]*);(.*)$")
  text_pos = 0
  text_max_len = 0
  for i in range(len(txt_lines)):
    match = jp_pattern.match(txt_lines[i])
    if match:
      table_off = int(match.group(1), 16)
      max_len = int(match.group(2), 10)

      if i < len(txt_lines)-1 and txt_lines[i+1]:
        string = txt_lines[i+1]
      else:
        string = match.group(3)

      text_max_len += max_len + 1

      str_bytes = r11.str_to_r11_bytes(string, encoding_table_lang, exception_on_unknown=True)

      strbytelen = len(str_bytes) + 1
      body += str_bytes + b'\x00'

      head_int[table_off // 4] = addr_text[0] + text_pos
      text_pos += strbytelen

  print("text_max_len: {}".format(text_max_len))
  if (text_pos > text_max_len):
    # raise Exception("text_pos > text_max_len: {} > {}".format(text_pos, text_max_len))
    print("text_pos > text_max_len: {} > {}".format(text_pos, text_max_len))

  # adjust data offsets
  new_data_offset = ((addr_text[0] + text_pos + 3) & ~3) # align new offset
  # new_data_offset = shortcut_data_offset # Keep old offset. No bugs, but all texts must fit the original size.
  data_offset_diff = new_data_offset - shortcut_data_offset
  print("Shortcuts data offset", new_data_offset, data_offset_diff)
  if (data_offset_diff != 0):
    head_int[2] = new_data_offset

    for i in range(table_entry_count):
      data_offset_i = (table_offset + i*table_entry_sz + 0x8) // 4
      head_int[data_offset_i] += data_offset_diff

  head_mv.release()

  f_out=open(bin_out, "wb")
  f_out.write(head)
  f_out.write(body)

  f_out.seek(new_data_offset)
  f_out.write(shortcut_data)

  f_out.close()


if __name__ == '__main__':
  main();
