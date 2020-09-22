from spider import BasicInfo_Spider

import json


def save_heroList_as_file(path, heroListJson):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(heroListJson, indent=2, ensure_ascii=False))


def insert_headProfileImage_as_file(heroListJson, headProfileImagesList):
    heroList = heroListJson['hero']
    if len(heroList) == len(headProfileImagesList):
        for hero in heroList:
            pass

