#!/usr/bin/env python3

from collections import defaultdict

lang_tags = ("jp", "en", "cn", "ru")
special_tags = ("tip",)

class TlMap:
    def __init__(self, jp=None, en=None, cn=None, ru=None):
        self.jp = jp
        self.en = en
        self.cn = cn
        self.ru = ru

class Tip:
    def __init__(self, id=None, title=None, pages=None):
        self.id = id
        self.title = title
        self.pages = pages if pages != None else []

class Tag:
    def __init__(self, name, args, is_closing=False):
        self.name = name
        self.args = args
        self.is_closing = is_closing
    def __eq__(self, other):
        if not isinstance(other, Tag):
            return False
        return (self.name == other.name and self.args == other.args and self.is_closing == other.is_closing)

def parse_tag(tag_line):
    tag_line = tag_line.strip(" \t\r\n").lower()
    if not tag_line or tag_line[0] != "~":
        return None
    t = tag_line.split("~")[1:]
    tag_is_closing = (len(t) >= 2 and t[-1] == "")
    tag_name = t[0]
    tag_args = t[1:-1] if tag_is_closing else t[1:]
    return Tag(tag_name, tag_args, tag_is_closing)

def parse_tip_file(tip_file_path, encoding="utf-8-sig"):
    temp_tip, temp_pages = None, None
    def reset_tip():
        nonlocal temp_tip, temp_pages
        lang_amount = len(lang_tags)
        temp_tip = Tip(title=TlMap(*["" for i in range(lang_amount)]), pages=TlMap(*[[] for i in range(lang_amount)]))
        temp_pages = TlMap(jp=defaultdict(str), en=defaultdict(str), cn=defaultdict(str), ru=defaultdict(str))
    def prepare_tip():
        for l in lang_tags:
            pages_list = getattr(temp_tip.pages, l)
            for page in [x[1] for x in sorted(getattr(temp_pages, l).items(), key=lambda t: t[0])]:
                page = page[:-2] if page.endswith("%N") else page
                pages_list.append(page)
        return temp_tip
    tips = []
    tag_stack = []
    reset_tip()
    with open(tip_file_path, "r", encoding=encoding) as tip_file:
        tip_text = tip_file.read().splitlines()
    for tip_line in tip_text:
        if tip_line.startswith("#"):
            continue
        tag = parse_tag(tip_line)
        closing_tag = Tag(tag_stack[-1].name, tag_stack[-1].args, True) if tag_stack else None
        if not tag_stack:
            if not tag:
                if tip_line:
                    print("warning: unexpected text '"+tip_line+"'")
                continue
            if tag.name not in special_tags:
                raise Exception("unsupported tag", tag)
            if len(tag.args) != 1:
                raise Exception("bad args", tag)
            if tag.is_closing:
                raise Exception("closing tag on empty stack", tag)
            tag_stack.append(tag)
            temp_tip.id = int(tag.args[0], 0)
        elif tag_stack[-1].name == "tip":
            if not tag:
                if tip_line:
                    print("warning: unexpected text '"+tip_line+"'")
                continue
            if tag == closing_tag:
                tips.append(prepare_tip())
                reset_tip()
                continue
            if tag.name not in lang_tags+special_tags:
                raise Exception("unsupported tag", tag)
            if len(tag.args) > 1:
                raise Exception("bad args")
            if tag.is_closing:
                raise Exception("unbound closing tag", tag)
            if tag.name == "tip":
                tips.append(prepare_tip())
                reset_tip()
                temp_tip.id = int(tag.args[0], 0)
                tag_stack.pop()
            tag_stack.append(tag)
        elif tag_stack[-1].name in lang_tags:
            if tag:
                if tag == closing_tag:
                    tag_stack.pop()
                    continue
                if tag_stack[-1].args:
                    raise Exception("lang tag was not closed", temp_tip.id)
                tag_stack[-1] = tag
                continue
            else:
                if not tag_stack[-1].args:
                    if getattr(temp_tip.title, tag_stack[-1].name):
                        raise Exception("unknown text after title tag", tip_line)
                    setattr(temp_tip.title, tag_stack[-1].name, tip_line)
                else:
                    pages_dict = getattr(temp_pages, tag_stack[-1].name)
                    pages_dict[int(tag_stack[-1].args[0], 0)] += tip_line + "%N"
    if tag_stack:
        if tag_stack[-1].name != "tip":
            raise Exception("unclosed tag after parsing end", tag_stack)
        tips.append(prepare_tip())
    tips.sort(key=lambda t: t.id)
    return tips
