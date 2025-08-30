#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import re

import r11
import r11.tipsparser

def string_preproc(string: str, game: str, lang: str):
    if lang == "cn":
        string = r11.clean_cn_translation_line(string)
    else:
        if game == "r11":
            string = r11.clean_en_translation_line_r11(string)
        string = r11.clean_en_translation_line(string)
    return string

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("translation")
    parser.add_argument("init_input")
    parser.add_argument("init_output")
    parser.add_argument("-g", "--game", default="e17")
    parser.add_argument("-l", "--lang", default="en")
    parser.add_argument("-t", "--tips")
    args = parser.parse_args(sys.argv[1:])

    if args.game == "r11":
        tip_amount = 110
        seg_text = [0xba68, 0x2c11a]
        # seg_table = [0x1140, 0xac98]
        seg_table_tips = [0x7610, 0x7f7c]
    elif args.game == "n7":
        tip_amount = 112
        seg_text = [0xaf80, 0x2254f]
        # seg_table = [0x1ba8, 0x9904]
        seg_table_tips = [0x7fbc, 0x880c]
    elif args.game == "e17":
        tip_amount = 119
        seg_text = [0x89b0, 0x1f709]
        # seg_table = [0xeb8, 0x7df8]
        seg_table_tips = [0x65c4, 0x6ee8]
    else:
        sys.exit("game not supported.")

    txt_lines = r11.readlines_utf8_crop_crlf(args.translation)
    with open(args.init_input, "rb") as f_bin:
        init_bytes = bytearray(f_bin.read())

    head = init_bytes[:seg_text[0]]
    mv = memoryview(head)
    head_int_view = mv.cast("I")
    body = bytearray()

    jp_pattern = re.compile(r"^;([\da-fA-F]*);([\d]*);(.*)$")
    dupestr = ";dupe:"
    unusedstr = ";unused"
    litstr = ";lit;"
    i = -1
    pos = seg_text[0]
    while i < len(txt_lines)-1:
        i += 1
        ln = txt_lines[i]
        jp_match = jp_pattern.match(ln)
        if not jp_match:
            continue
        i += 1
        ln2 = txt_lines[i] if (i < len(txt_lines)) else ""

        addr = jp_match.group(1)
        table_offset = int(addr, 16)
        #jp_len = jp_match.group(2) # not relevant

        if ln2.startswith(dupestr):
            dupe_ref_bytes = ln2[len(dupestr):]
            dupe_ref = int(dupe_ref_bytes, 16)
            # Just reference the same string
            head_int_view[table_offset // 4] = head_int_view[dupe_ref // 4]
            continue
        jp_string = jp_match.group(3)
        tl_string = ln2
        if not ln2 or ln2[0] == "#":
            # fallback to original line
            tl_string = jp_string
        elif ln2.startswith(unusedstr):
            # clearly mark as untranslated to make detection more easy
            tl_string = "<" + addr + ":not_translated>"
        elif ln2.startswith(litstr):
            tl_string = tl_string[len(litstr):]
            if not tl_string: tl_string = jp_string
        elif ln2[0] == ";":
            print("Warning, unexpected ';' in the beginning of line [{}]".format(ln2))

        tl_string = string_preproc(tl_string, args.game, args.lang)

        if ln2.startswith(litstr):
            tl_bytes = r11.str_to_r11_bytes(tl_string, exception_on_unknown=True)
        else:
            tl_bytes = r11.str_to_r11_bytes(tl_string, lang=args.lang, exception_on_unknown=True)

        head_int_view[table_offset // 4] = pos
        body += tl_bytes + b'\0'
        pos += len(tl_bytes) + 1

    tips_txt = args.tips
    if tips_txt:
        tips = r11.tipsparser.parse_tip_file(tips_txt)
        if len(tips) != tip_amount:
            raise Exception(tip_amount, "tips expected, got", len(tips))
        tip_i = seg_table_tips[0]//4
        for tip in tips:
            tl_title = getattr(tip.title, args.lang)
            tl_pages = getattr(tip.pages, args.lang)
            pages = tl_pages or tip.pages.jp
            title = string_preproc(tl_title or tip.title.jp, args.game, args.lang)
            title_bytes = r11.str_to_r11_bytes(title, lang=args.lang)+b'\0'
            head_int_view[tip_i] = pos
            tip_i += 1
            body += title_bytes
            pos += len(title_bytes)
            for p in pages:
                p_bytes = r11.str_to_r11_bytes(string_preproc(p, args.game, args.lang), lang=args.lang)+b'\0'
                head_int_view[tip_i] = pos
                tip_i += 1
                body += p_bytes
                pos += len(p_bytes)
            tip_i += 2
        if tip_i*4 != seg_table_tips[1]:
          raise Exception("expected off", seg_tips_table[1], "ended up with", tip_i*4)

    mv.release()

    with open(args.init_output, "wb") as f_out:
        f_out.write(head)
        f_out.write(body)

if __name__ == "__main__":
    main()
