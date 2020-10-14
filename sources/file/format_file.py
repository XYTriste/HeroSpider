import json
from file import get_file_content

HERO_BASIC_INFO_PATH = '..\\..\\resources\\BasicInfo\\heroList.json'
HERO_DETAILED_INFO_PATH = '..\\..\\resources\\DetailedInfo\\1.json'

FILE_PATH = '..\\..\\resources\\DetailedInfo\\'


def merge_file():
    heroBasicInfo = open(HERO_BASIC_INFO_PATH, 'r', encoding='utf-8')
    heroDetailedInfo = open(HERO_DETAILED_INFO_PATH, 'r', encoding='utf-8')

    heroBasicInfoTuple = json.loads(heroBasicInfo.read())
    heroDetailedInfoTuple = json.loads(heroDetailedInfo.read())

    heroInfoAsBasic = heroBasicInfoTuple['hero']
    heroInfoAsDetailed = heroDetailedInfoTuple['hero']

    heroInfoAsBasicKeys = heroInfoAsBasic[0].keys()
    heroInfoAsDetailedKeys = heroInfoAsDetailed.keys()

    differentKeys = []

    for i in heroInfoAsBasicKeys:
        if i not in heroInfoAsDetailedKeys:
            differentKeys.append(i)

    files = get_file_content.get_all_files()

    number = 0
    for file in files:
        fileRelativePath = FILE_PATH + file
        fileContent = None

        with open(fileRelativePath, 'r', encoding='utf-8') as file_object:
            fileContent = json.loads(file_object.read())

        with open(fileRelativePath, 'w', encoding='utf-8') as file_object:
            print("更新前长度:", len(fileContent['hero']))

            for dk in differentKeys:
                fileContent['hero'][dk] = heroInfoAsBasic[number][dk]

            print("更新后长度:", len(fileContent['hero']))
            file_object.write(json.dumps(fileContent, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    merge_file()
