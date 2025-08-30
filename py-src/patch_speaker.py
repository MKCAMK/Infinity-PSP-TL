#!/usr/bin/env python3

import sys
import os
import r11
import r11.names

r11.names.init("n7")

lang = sys.argv[3]
script_name = os.path.splitext(os.path.basename(sys.argv[1]))[0]
with open(sys.argv[1], "rb") as f:
    data = [l.rstrip(b"\r\n") for l in f.readlines()]
f_out = open(sys.argv[2], "wb")
f_out.write(b"\n".join(data[:3])+b"\n")
del data[:3]
for i, line in enumerate(data):
    j = i % 3
    if j == 1 and not data[i+1]:
        decoded_line = r11.r11_bytes_to_str(line)
        decoded_line, leading_control = r11.rm_leading_control_sequence(decoded_line)
        decoded_line, trailing_control = r11.rm_trailing_control_sequence(decoded_line)
        jp_speaker, jp_leading_bracket, jp_trailing_bracket, tl_speaker = r11.names.detectJpSpeakerAndBrackets(decoded_line, lang)

        if jp_speaker:
            if script_name == "USER04B" and data[i-1] == b"0x2224" and jp_speaker == "優夏" and jp_leading_bracket == "「" and not jp_trailing_bracket:
                print("fixing typo in USER04B.")
                decoded_line += "」"
            elif script_name == "USER31" and data[i-1] == b"0x2830" and jp_speaker == "老人" and jp_leading_bracket == "「" and not jp_trailing_bracket and decoded_line[-1] == "』":
                print("fixing typo in USER31.")
                decoded_line = decoded_line[:-1] + "」"

            new_line = leading_control+tl_speaker+decoded_line[len(jp_speaker):]+trailing_control
            data[i+1] = r11.str_to_r11_bytes(new_line, lang)
    f_out.write(line+b"\n")
f_out.close()
