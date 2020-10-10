import json

import os

basicInfoFilePath = '..\\..\\resources\\BasicInfo\\heroList.json'

detailedInfoDirectoryPath = '..\\..\\resources\\DetailedInfo'
detailedInfoFilePath = detailedInfoDirectoryPath + '\\{fileName}'


def get_basicInfo_content():
    basicInfo = None
    with open(basicInfoFilePath, 'r', encoding='utf-8') as f:
        basicInfo = json.loads(f.read())
    return basicInfo


def get_detailedInfo_content(fileName):
    filePath = detailedInfoFilePath.format(fileName=fileName)
    detailedInfo = None
    with open(filePath, 'r', encoding='utf-8') as f:
        detailedInfo = json.loads(f.read())
    return detailedInfo


def get_all_files():
    files = os.listdir(detailedInfoDirectoryPath)
    return files


if __name__ == '__main__':
    for file in get_all_files():
        print(file)
