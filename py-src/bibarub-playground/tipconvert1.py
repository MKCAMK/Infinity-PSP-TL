#!/usr/bin/env python3

import os
import sys
import re

tipsdir = "/home/bibarub/Infinity-PSP-TL/text/tips-psp-r11"
outpath = "/home/bibarub/Infinity-PSP-TL/text/tips-psp-r11.txt"

fout = open(outpath, "w", encoding="utf-8-sig")
for tipfile in [os.path.join(tipsdir, x) for x in sorted(os.listdir(tipsdir))]:
    tip = open(tipfile, "r", encoding="utf-8-sig")
    tiplines = tip.read().splitlines() + [""]
    tip.close()
    i = int(tiplines[0].strip()[3:6])
    jp_title, en_title, cn_title = tiplines[1:4]
    pages_amount = int(tiplines[4].split(":")[1])
    jp_pages, en_pages, cn_pages = [], [], []
    current_page = ""
    for pline in tiplines[7:]:
        if not pline and current_page:
            if current_page[-1] == "\n": current_page = current_page[:-1] + "%N"
            pages = jp_pages if current_lang == "JP" else en_pages if current_lang == "EN" else cn_pages if current_lang == "CN" else None
            pages.append(current_page)
            current_page = ""
            current_lang = None
            continue
        if not pline:
            continue
        if re.match(r"#[A-Z]{2}#\d+", pline):
            current_lang = pline[1:3]
            continue
        if pline.startswith(("#", "//")):
            continue
        if current_lang == "JP" and pline[0] == ";":
            pline = pline.split(";", 3)[3]
        current_page += pline.replace("%N", "\n")
    if pages_amount != len(jp_pages) != len(en_pages) != len(cn_pages):
        print("page amount mismatch")
        sys.exit()
    fout.write("#"*100+"\n~tip~"+str(i)+"\n")
    for t in [("jp", jp_title, jp_pages), ("en", en_title, en_pages), ("cn", cn_title, cn_pages)]:
        lang, title, pages = t
        fout.write("~"+lang+"\n")
        fout.write(title+"\n")
        for j, p in enumerate(pages):
            fout.write("~"+lang+"~"+str(j)+"\n")
            fout.write(p)
            fout.write("\n~"+lang+"~"+str(j)+"~\n")
        fout.write("\n")
    fout.write("#"*100+"\n\n\n")#"~tip~"+str(i)+"~\n\n\n")
fout.close()
