import sys
import re

import r11
import r11.names

with open(sys.argv[1], encoding='sjisx0213') as file_in:
    jp_lines = file_in.readlines()

main_text_pattern_ja = "^((?:[^%]*?\u300c|『)?).*?(\u300d|』)?$"
en_lines = []
for jp_line in jp_lines:
    match_ja = re.match(main_text_pattern_ja, jp_line)
    jp_speaker = match_ja.group(1)
    if not jp_speaker or not jp_speaker[:-1]:
        en_lines.append(jp_line)
        continue
    jp_leading_bracket = jp_speaker[-1:]
    jp_trailing_bracket = match_ja.group(2)
    jp_speaker = jp_speaker[:-1]
    if '『' in jp_speaker:
        en_lines.append(jp_line)
        continue
    en_speaker = r11.names.translateNamesString(jp_speaker, "en")
    en_line = en_speaker + jp_leading_bracket + jp_line[match_ja.end(1):]
    en_lines.append(en_line)

with open(sys.argv[2], 'w', encoding='sjisx0213') as file_out:
    file_out.writelines(en_lines)

