#!/usr/bin/env python3

import os
import sys

import r11
import r11.names

import merger

r11.names.init("r11")

def prep(jp, tl, lang):
    export = ""
    tl = tl[1:] if tl[0] == " " and tl[1] != " " else tl
    jp, jp_head = r11.rm_leading_control_sequence(jp)
    jp, jp_tail = r11.rm_trailing_control_sequence(jp)
    jp_speaker, jp_head_bracket, jp_tail_bracket, tl_speaker = r11.names.detectJpSpeakerAndBrackets(jp, "ru")
    tl, tl_head = r11.rm_leading_control_sequence(tl)
    tl, tl_tail = r11.rm_trailing_control_sequence(tl)
    if "「" in tl:
        if tl.startswith(tl_speaker+"「"):
            export = tl[len(tl_speaker)+1:]
            if export[-1] == "」":
                export = export[:-1]
        else:
            export = ";"+tl_head+tl+tl_tail
            print("odd!")
            print(tl_head+tl+tl_tail)
    if not export:
        export = tl
    if tl_head != jp_head or tl_tail != jp_tail:
        export = tl_head + export + tl_tail
        print("control seq mismatch!")
        print(jp_head+jp+jp_tail)
        print(tl_head+tl+tl_tail)
        print("")
    return export

mac = open(sys.argv[1], "r", encoding="utf-8-sig")
maclines = [l.rstrip("\n") for l in mac]
mac.close()

maps = merger.chapter_file_to_map_list(sys.argv[2])
if len(maps) != len(maclines)//3-1:
    exit("aborting")
for i in range(len(maclines)//3-1):
    maps[i].ru = prep(maps[i].jp, maclines[i*3+4], "ru")

merger.map_list_to_chapter_file(maps, sys.argv[2])
