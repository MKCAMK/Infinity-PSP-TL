#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import collections

TlNames = collections.namedtuple("TlNames", ["en", "cn", "ru"])
# key - original japanese name
# value - list of translated values [en, cn]
names_dict_generic = {
  "？？": TlNames("???", "？？", "???"),
  "みんな": TlNames("Everyone", "所有人", "Все"),
  "男": TlNames("Man", "男", "Мужчина"),
  "女": TlNames("Woman", "女", "Девушка"),
}
game_names_dicts = {
  "r11": {
    "少年": TlNames("Boy", "男孩", "Мальчик"),
    "少女": TlNames("Girl", "女孩", "Девочка"),
    "こころ": TlNames("Kokoro", "心", "Кокоро"),
    "悟": TlNames("Satoru", "悟", "Сатору"),
    "黛": TlNames("Mayuzumi", "黛", "Маюдзуми"),
    "黄泉木": TlNames("Yomogi", "黄泉木", "Ёмоги"),
    "内海": TlNames("Utsumi", "内海", "Уцуми"),
    "犬伏": TlNames("Inubushi", "犬伏", "Инубуси"),
    "ゆに": TlNames("Yuni", "悠尼", "Юни"),
    "穂鳥": TlNames("Hotori", "穗鸟", "Хотори"),
    "榎本": TlNames("Enomoto", "鼷本", "Эномото"),
    "機長": TlNames("Pilot", "机长", "Пилот"),
    # "Yukidoh", rather than "Yuukidou", because it is written everywhere else this way
    "ユウキドウ": TlNames("Yukidoh", "优希堂", "Юкидо"),
    # These occur in init.bin only, but pasting them here, for reference
    "山岳救助隊員": TlNames("Mountain rescue worker", ";unused", ";unused"),
    "沙也香": TlNames("Sayaka", ";unused", ";unused"),
  },
  "e17": {
    "武": TlNames("Takeshi", None, "Такеши"),
    "少年": TlNames("Kid", None, "Кид"),
    "優": TlNames("You", None, "Ю"),
    "優春": TlNames("You'haru'", None, "Ю'хару"),
    "優秋": TlNames("You'aki'", None, "Ю'аки"),
    "つぐみ": TlNames("Tsugumi", None, "Цугуми"),
    "空": TlNames("Sora", None, "Сора"),
    "空Ａ": TlNames("Sora A", None, "Сора-А"),
    "空Ｂ": TlNames("Sora B", None, "Сора-Б"),
    "空Ｃ": TlNames("Sora C", None, "Сора-В"),
    "偽空": TlNames("Fake Sora", None, "Фальшивая Сора"),
    "沙羅": TlNames("Sara", None, "Сара"),
    "沙羅": TlNames("Sara", None, "Сара"),
    "ココ": TlNames("Coco", None, "Коко"),
    "ピピ": TlNames("Pipi", None, "Пипи"),
    "タヌキ": TlNames("Tanuki", None, "Тануки"),
    "ホクト": TlNames("Hokuto", None, "Хокуто"),
    "桑古木": TlNames("Kaburaki", None, "Кабураки"),
    "管制官": TlNames("Mission Control", None, "Рация"),
    "救助隊員": TlNames(";unused", ";unused", ";unused"),
    "研究員": TlNames("Researcher", None, "Учёный"),
    "自衛隊員": TlNames(";unused", ";unused", ";unused"),
    "係員": TlNames("Park Staff", None, "Персонал"),
    "部長": TlNames("Club President", None, "Президент Клуба"),
    "客": TlNames("Visitors", None, "Люди"),
    "少女": TlNames("Young Girl", None, "Девочка"),
    "アナウンス": TlNames("Announcement", None, "Автообъявление"),
    "田中先生": TlNames("Doctor Tanaka", None, "Доктор Танака"),
    "ＢＷ": TlNames("Blick Winkel", None, "БВ"),
    "マヨ": TlNames("Mayo", None, "Майо"),
    "女の子": TlNames("Girl", None, "Девочка"),
    "男の人": TlNames("Man", None, "Парень"),
    "女の人": TlNames("Woman", None, "Девушка"),
    "医師": TlNames("Doctor", None, "Врач"),
    "松永": TlNames("Matsunaga", None, "Сара"),
  },
  "n7": {
    "少年": TlNames("Boy", "男孩", "Мальчик"),
    "少女": TlNames("Girl", "女孩", "Девочка"),
    "誠": TlNames("Makoto", None, None),
    "優夏": TlNames("Yuka", None, None),
    "億彦": TlNames("Okuhiko", None, None),
    "遙": TlNames("Haruka", None, None),
    "いづみ": TlNames("Izumi", None, None),
    "くるみ": TlNames("Kurumi", None, None),
    "沙紀": TlNames("Saki", None, None),
    "医者": TlNames("Doctor", None, None),
    "漁師": TlNames("Fisherman", None, None),
    "声": TlNames("Announcer", None, None),
    "運転手": TlNames("Driver", None, None),
    "守野姉妹": TlNames("Morino sisters", None, None),
    "男の子": TlNames("Boy", None, None),
    "女の子": TlNames("Girl", None, None),
    "先輩": TlNames("Senpai", None, None),
    "警官の声": TlNames("Police officer", None, None),
    "警備員": TlNames("Security guard", None, None),
    "看護師": TlNames("Nurse", None, None),
    "店員": TlNames("Clerk", None, None),
    "老人": TlNames("Old person", None, None),
    "店長": TlNames("Manager", None, None),
    "父": TlNames("Father", None, None),
    "半魚人": TlNames("Merman", None, None),
    "謎の声": TlNames("Mysterious voice", None, None),
    "サメ子": TlNames("Shark", None, None),
    "ラプラス": TlNames("Laplace", None, None),
    "ときみ": TlNames("Tokimi", None, None),
    "北大路": TlNames("Kitaoji", None, None),
    "女の声": TlNames("Female voice", None, None),
    "男の声": TlNames("Male voice", None, None),
    "少年の声": TlNames("Boy's voice", None, None),
    "新入生": TlNames("Freshman", None, None),
    "上級生": TlNames("Senior", None, None),
    "青年": TlNames("Kid", None, None),
    "教授": TlNames("Professor", None, None),
    "ふたり": TlNames("Couple", None, None),
    "漁師の客": TlNames("Fisherman client", None, None),
    "客": TlNames("Customer", None, None),
    "母親": TlNames("Mother", None, None),
    "ゆえ": TlNames("Yue", None, None),
    "不審人物": TlNames("Suspicious person", None, None),
    "誠＆優夏": TlNames("Makoto & Yuka", None, None),
    "誠＆くるみ": TlNames("Makoto & Kurumi", None, None),
    "優夏＆億彦": TlNames("Yuka & Okuhiko", None, None),
    "島民Ａ": TlNames("Islander A", None, None),
    "いづみ以外": TlNames("Everyone but Izumi", None, None),
    "サメの意識": TlNames("Shark's Consciousness", None, None),
    "人影": TlNames("Silhouette", None, None),
    "やさ男": TlNames("Kind Man", None, None),
    "キザな男": TlNames("Pretentious Man", None, None)
  }
}

names_dict = None
tl_names_list = None

ja_original_separator = "・" # "\u30fb"
en_separator = ","
cn_separator = "、"
ru_separator = ","

separators = TlNames(en_separator, cn_separator, ru_separator)

def populateNamesDict(game: str) -> dict:
  global names_dict
  if not game in game_names_dicts:
    raise Exception(f"Game {game} is not supported.")
  names_dict = names_dict_generic
  names_dict.update(game_names_dicts[game])
  return names_dict

def populateTlNamesList(lang: str = "en") -> list[str]:
  global tl_names_list
  if not names_dict:
    raise Exception("names_dict is empty")
  tl_names_list = []
  for tltuple in names_dict.values():
      tl_names_list.append(getattr(tltuple, lang))
  return tl_names_list

# tl_lang should be one of TlNames field names: "en" or "cn"
def translateNamesString(character_names: str, tl_lang: str) -> str:
  if not names_dict:
    raise Exception("names_dict is empty")
  if not character_names:
    return ""

  jp_names = character_names.split(ja_original_separator)
  # print(jp_names, file=sys.stderr)
  translated_names = [names_dict.get(jp_name)._asdict()[tl_lang] for jp_name in jp_names]
  if (None in translated_names):
    raise Exception("Speaker translation for %s not found. Values: %s"%(character_names, translated_names))
  translated_names_joined = separators._asdict()[tl_lang].join(translated_names)
  return translated_names_joined

def checkTranslatedName(character_names: str, tl_lang: str):
  if not tl_names_list:
    populateTlNamesList(tl_lang)
  if not character_names:
    return ""

  names = character_names.split(getattr(separators, tl_lang))
  results = [name in tl_names_list for name in names]
  return (False not in results)
