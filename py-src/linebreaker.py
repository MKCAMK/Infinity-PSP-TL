#!/usr/bin/env python

import os, sys
import r11, r11.names

control_sequences = [
    "K", "N", "O", "P", "V", "p", "n", "TS", "TE", 
    "FS", "LL", "LC", "LR", "FE", "XS", "XE", "W", "X"
]
dont_break_after = "\"('「["
dont_break_before = (
    "1234567890"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    ",.!?\"'」]-:―)〜♪"
)
max_width = 433

def load_font_table(lang):
    chars = {}
    widths = {}

    with open(os.path.join(os.path.dirname(__file__), os.pardir, "text", "charset-tables", f"r11-{lang}-font-table.txt"), encoding="utf-8") as file:
        for line in file:
            num, _, char, _ = line.split('\t')
            chars[int(num.rstrip(':'))] = char

    with open(os.path.join(os.path.dirname(__file__), os.pardir, "text", "font", f"glyphs-{lang}", "glyph_data.txt"), encoding="utf-8") as file:
        glyph_data = file.readlines()[4:]

    for glyph_line in glyph_data:
        glyph_line = glyph_line.replace(' ', '').split(':')
        num = int(glyph_line[0])
        widths[chars[num]] = int(glyph_line[2]) - int(glyph_line[1]) + 1

    widths[' '] = 3 if lang == "ru" else 2
    return widths

def write_widths_file(lang, widths, path = None):
    if not path:
        path = f"widths-{lang}.txt"
    with open(path, "w", encoding="utf-8") as file:
        for char, width in widths.items():
            file.write(f"{char} {width}\n")

def process_script(game, lang, widths, scn_path = ""):
    if not scn_path:
        scn_path = os.path.join(os.path.dirname(__file__), os.pardir, "text", f"mac-psp-{game}-{lang}-utf8")
    r11.names.populateNamesDict(game)
    r11.names.populateTlNamesList(lang)

    output_path = os.path.join(os.path.dirname(__file__), os.pardir, "text", f"tmp-{game}", f"mac-psp-{lang}-utf8-wrapped")
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    for scn_file in os.listdir(scn_path):
        process_file(os.path.join(scn_path, scn_file), output_path, widths, lang)

def process_file(scn_file, output_path, widths, lang):
    """Process individual script files."""
    with open(scn_file, encoding="utf-8") as file:
        lines = file.readlines()

    outlines = lines[:3]
    content_lines = lines[3:]

    counter = 0
    for i in range(0, len(content_lines), 3):
        outlines.extend(content_lines[i:i+2])
        counter, newline = process_line(content_lines[i+2].rstrip('\n'), counter, widths, lang)
        outlines.append(newline)

    with open(os.path.join(output_path, os.path.basename(scn_file)), "w", encoding="utf-8") as file:
        file.writelines(outlines)

def process_line(line, counter, widths, lang):
    if not line.endswith(("%K", "%P", "%O", "%N", "%p")):
        return counter, line + '\n'

    newline = ""
    speaker = ""

    line_iterator = iter(enumerate(line))

    if '「' in line:
        speaker = line.split('「', 1)[0]
    if r11.names.checkTranslatedName(speaker, lang):
        newline += speaker
        for _ in range(len(speaker)): next(line_iterator)

    for i, char in line_iterator:
        if char == '%':
            seq = handle_control_sequence(line, i)
            newline += '%' + seq
            for _ in range(len(seq)): next(line_iterator)
            if seq in ('N', 'P', 'p', 'O'):
                counter = 0
            continue

        newline += char
        counter += widths[char] + 2
        if counter > max_width:
            counter, newline = handle_line_break(newline, widths)

    if line.endswith("%K") and not line.endswith(" %K"):
        counter = 0

    return counter, newline + '\n'

def handle_control_sequence(line, index):
    seq = line[index + 1:index + 3]
    if seq[0].isdigit():
        seq = line[index+1:index+4]
    elif seq[:2] in control_sequences:
        seq = seq[:2]
    elif seq[0] == 'C':
        seq = line[index+1:index+6]
    elif seq[0] == 'T':
        seq = line[index+1:index+5]
    elif seq[0] in control_sequences:
        seq = seq[0]
    else:
        raise Exception(f"unhandled control sequence " + seq)

    return seq

def handle_line_break(line, widths):
    i = len(line) - 1
    while line[i] in dont_break_before or line[i - 1] in dont_break_after:
        i -= 1
        if i < 0:
            raise Exception("failed to break: " + line)
    newline = line[:i] + '%N'
    if line[i] == ' ':
        i += 1
    newline += line[i:]

    width = sum(widths[x] for x in line[i:]) + len(line[i:]) * 2

    return width, newline

def main():
    game = sys.argv[1] if len(sys.argv) > 1 else "e17"
    lang = sys.argv[2] if len(sys.argv) > 2 else "en"
    scn_path = sys.argv[3] if len(sys.argv) >  3 else ""

    widths = load_font_table(lang)
    #write_widths_file(lang, widths)

    process_script(game, lang, widths, scn_path)

if __name__ == "__main__":
    main()
