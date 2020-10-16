import json
from file import get_file_content

HERO_DETAILED_INFO_PATH = get_file_content.detailedInfoFilePath.format(fileName='1.json')
# 格式化的字符串.表示第一个英雄详细信息文件的完整路径.用于比对文件内容并进行合并.

FILE_PATH = '..\\resources\\DetailedInfo\\' # 英雄详细信息文件所在的目录.用于合并后的内容保存.


def merge_file():
    """
    比对文件内容并进行合并
    :return: 无返回值.
    """
    heroBasicInfo = open(get_file_content.basicInfoFilePath, 'r', encoding='utf-8')
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
