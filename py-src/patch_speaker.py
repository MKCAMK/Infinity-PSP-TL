#!/usr/bin/env python

import sys, re
import r11, r11.names

main_text_pattern_ja = "^((?:[^%]*?\u300c|『)?).*?(\u300d|』)?$"

with open(sys.argv[1], encoding='sjisx0213') as f, open(sys.argv[2], 'w', encoding='sjisx0213') as fout:
    for line in f:
        if not line.rstrip('\n'):
            continue
        if line.startswith('0x') or line.startswith('text area offset and size:'):
            fout.write(line)
            continue
        match_ja = re.match(main_text_pattern_ja, line)
        jp_speaker = match_ja.group(1)
        if not jp_speaker.rstrip('\n'):
            fout.write(line)
            fout.write('\n')
            continue
        jp_leading_bracket = jp_speaker[-1:]
        jp_trailing_bracket = match_ja.group(2)
        jp_speaker = jp_speaker[:-1]
        if '『' in jp_speaker:
            fout.write(line)
            fout.write('\n')
            continue
        en_speaker = r11.names.translateNamesString(jp_speaker, "en")
        en_line = en_speaker + jp_leading_bracket + line[match_ja.end(1):]
        fout.write(line)
        fout.write(en_line)