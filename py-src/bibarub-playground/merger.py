#!/usr/bin/env python3
import sys

STATE_NONE = 0
STATE_JP = 1
STATE_EN = 2
STATE_CN = 3
STATE_RU = 4

class TlMap:
    def __init__(self, jp=None, en=None, cn=None, ru=None):
        self.jp = jp
        self.en = en
        self.cn = cn
        self.ru = ru

def chapter_to_map_list(chapter_lines):
    maps = []
    i = -1
    state = STATE_NONE
    current_map = TlMap()
    while i < len(chapter_lines)-1:
        i += 1
        line = chapter_lines[i]
        if not line:
            if state == STATE_NONE:
                continue
            state = STATE_NONE
            #if not (current_map.jp and current_map.en and current_map.cn and current_map.ru):
            #    sys.exit("could not collect all languages")
            maps.append(current_map)
            current_map = TlMap()
            continue
        if line.startswith("//"):
            print("comment on line "+str(i)+": "+line+"\n")
            continue
        state += 1
        if state == STATE_RU+1:
            sys.exit("state overflow")
        if state == STATE_JP:
            current_map.jp = line
        elif state == STATE_EN:
            current_map.en = line
        elif state == STATE_CN:
            current_map.cn = line
        elif state == STATE_RU:
            current_map.ru = line
    return maps

def chapter_file_to_map_list(chapter_path):
    return chapter_to_map_list(open(chapter_path, encoding="utf-8-sig").read().splitlines())

def map_list_to_chapter_file(map_list, chapter_path):
    with open(chapter_path, "w", encoding="utf-8-sig") as f:
        for _map in map_list:
            f.write(_map.jp+"\n")
            if _map.en:
                f.write(_map.en+"\n")
                f.write(_map.cn+"\n")
                f.write(_map.ru+"\n")
            f.write("\n")

def main():
    # 1 old, 2 new, 3 out
    old_maps = chapter_file_to_map_list(sys.argv[1])
    #for t in old_maps:
    #    print(t.en)
    new_maps = chapter_file_to_map_list(sys.argv[2])
    if len(old_maps) != len(new_maps):
        sys.exit("map amount unmatched")
    f_new = open(sys.argv[3], "w", encoding="utf-8-sig")
    for i in range(len(new_maps)):
        old = old_maps[i]
        new = new_maps[i]
        f_new.write(new.jp+"\n")
        if new.en:
            f_new.write(new.en+"\n")
            f_new.write(new.cn+"\n")
            f_new.write(old.ru+"\n")
        f_new.write("\n")
    f_new.close()

if __name__ == "__main__":
    main()
