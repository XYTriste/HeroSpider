import json

basicInfoFilePath = '..\\..\\resources\\BasicInfo\\heroList.json'
detailedInfoFilePath = '..\\..\\resources\\DetailedInfo\\{fileName}.json'


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
