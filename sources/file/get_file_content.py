import json

import os

basicInfoFilePath = '..\\resources\\BasicInfo\\heroList.json'   # 存储英雄基本信息的文件路径.

detailedInfoDirectoryPath = '..\\resources\\DetailedInfo'   # 存储英雄详细信息的文件路径.
detailedInfoFilePath = detailedInfoDirectoryPath + '\\{fileName}'   # 与英雄详细信息的路径结合.表示文件的完整路径.


def get_basicInfo_content():
    """
    返回英雄基本信息的文件内容.
    :return: 返回类型为str.返回内容为从文件中读取的英雄基本信息.
    """
    basicInfo = None
    with open(basicInfoFilePath, 'r', encoding='utf-8') as f:
        basicInfo = json.loads(f.read())
    return basicInfo


def get_detailedInfo_content(fileName):
    """
    返回英雄详细信息的文件内容.由于英雄详细信息有多个文件.所以使用参数指定返回具体哪一个.
    :param fileName: 类型为str.表示指定读取返回内容的文件。
    :return: 类型为str.返回读取的英雄详细信息.
    """
    filePath = detailedInfoFilePath.format(fileName=fileName)
    detailedInfo = None
    with open(filePath, 'r', encoding='utf-8') as f:
        detailedInfo = json.loads(f.read())
    return detailedInfo


def get_all_files():
    """
    读取指定路径中的所有文件并返回.
    :return: 返回类型为list.包含了指定路径下的所有文件的名称.
    """
    files = os.listdir(detailedInfoDirectoryPath)
    return files


def get_all_heroId():
    """
    读取英雄基本信息的文件并返回所有英雄的id.
    :return: 返回类型为list.包含了所有英雄的id信息
    """
    basicInfo = get_basicInfo_content()
    All_hero = basicInfo['hero']
    All_heroId = []
    for hero in All_hero:
        All_heroId.append(hero['heroId'])
    return All_heroId


if __name__ == '__main__':
    for file in get_all_files():
        print(file)
