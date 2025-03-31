#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import struct

game = "e17"

def read_strings_from_table(all_bytes, seg_table, seg_strings):
  offsets = all_bytes[seg_table[0]:seg_table[1]]
  offsets_n = len(offsets) // 4
  offsets = struct.unpack("<" + "I" * offsets_n, offsets)

  ret_strings = []
  ret_orig_len = []
  ret_table_offs = []
  for i, off in enumerate(offsets):
    table_offs = i*4+seg_table[0]
    # [workaround] skip areas which do not have text references:
    if game == "r11":
      if 0x46a0 <= table_offs < 0x5350: continue
      if 0x7520 <= table_offs < 0x7610: continue
      if 0x7f90 <= table_offs < 0x86f8: continue
    elif game == "n7":
      if 0x5250 <= table_offs < 0x58f0: continue
      if 0x7ec8 <= table_offs < 0x7fbc: continue
    else: # e17
      if 0x3710 <= table_offs < 0x3E94: continue
      if 0x57F8 <= table_offs < 0x5A24: continue
      if 0x64B4 <= table_offs < 0x65C4: continue
      if 0x6EE0 <= table_offs < 0x75E8: continue

    if (seg_strings[0] <= off < seg_strings[1]):
      end = all_bytes.find(b"\x00", off)
      st = all_bytes[off:end]
      ret_strings.append(st);
      ret_orig_len.append(end-off);
      ret_table_offs.append(table_offs);
      # try:
      #   print("%X:%X"%(off,end), st.decode("SJIS"))
      # 0x8753 (circled 20 which is used as a whitespace sometimes in R11) character causes errors
      # except UnicodeDecodeError:
      #   print("%X:%X"%(off,end), "[can't decode]")

  return zip(ret_table_offs, ret_orig_len, ret_strings)

def write_results_to_file(name, res, find_dupes = True):
  string_dict=dict()
  f = open("init.bin." + game + "." + name + ".txt", "wb")
  f.write(b"#===%b\n\n"%name.encode())
  for toff_len_str in res:
    f.write(b";%x;%d;%s\n" % toff_len_str)
    first_tbl_ref = string_dict.get(toff_len_str[2])
    if (find_dupes):
      if (first_tbl_ref != None):
        f.write(b";dupe:%x"%first_tbl_ref)
      else:
        string_dict[toff_len_str[2]] = toff_len_str[0]

    f.write(b"\n")
  f.close()

def main():
  global game
  if "GAME" in os.environ:
    game = os.environ["GAME"]

  if game == "r11":
    seg_init_table = [0x1140, 0x1d38]
    seg_init = [0xba68, 0xdc40]
    seg_tips_table = [0x7610, 0x7f78]
    seg_tips = [0x14c30, 0x2464c]
    seg_chrono_table = [0x90dc, 0xac98]
    seg_chrono = [0x26be8, 0x2c11a]
    seg_all_table = [0x1140, 0xac98]
    seg_all = [0xba68, 0x2c11a]
  elif game == "n7":
    seg_init_table = [0x1ba8, 0x1e44]
    seg_init = [0xaf80, 0xb681]
    seg_tips_table = [0x7fbc, 0x8808]
    seg_tips = [0x13526, 0x20e0f]
    seg_all_table = [0x1ba8, 0x9908] 
    seg_all = [0xaf80, 0x22550]
  else: # e17
    seg_init_table = [0xeb8, 0x1810]
    seg_init = [0x89b0, 0x9FD7]
    seg_tips_table = [0x65C4, 0x6EE4]
    seg_tips = [0xF6EA, 0x1D63F]
    seg_all_table = [0xEB8, 0x7DF8]
    seg_all = [0x89B0, 0x1F709]

  initbin_path = sys.argv[1] if len(sys.argv) > 1 else "init.dec"

  f=open(initbin_path, "r+b")
  all_bytes = f.read()
  f.close()

  # these are only extracted for convenience
  res_init = read_strings_from_table(all_bytes, seg_init_table, seg_init)
  res_tips = read_strings_from_table(all_bytes, seg_tips_table, seg_tips)
  write_results_to_file("init",   res_init)
  write_results_to_file("tips",   res_tips)
  if game == "r11":
    res_chrono = read_strings_from_table(all_bytes, seg_chrono_table, seg_chrono)
    write_results_to_file("chrono", res_chrono)

  # all strings go here
  res_all = read_strings_from_table(all_bytes, seg_all_table, seg_all)
  write_results_to_file("all", res_all)


if __name__ == '__main__':
  main();
