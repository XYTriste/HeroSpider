"""
专门写各种奇怪测试的地方
"""
# import json
# import os
#
# path = '..\\resources\\DetailedInfo'
#
# for root, dirs, files in os.walk(path):
#     for fileStr in files:
#         time = None
#         fileName = path + "\\" + fileStr
#         with open(fileName, 'r', encoding='utf-8') as f:
#             JsonStr = json.loads(f.read())
#             if time is None or time != JsonStr['fileTime']:
#                 print(JsonStr['fileTime'])
#                 time = JsonStr['fileTime']


import json

heroList = open('..\\resources\\BasicInfo\\heroList.json', 'r', encoding='utf-8')
heroDetailList = open('..\\resources\\DetailedInfo\\1.json', 'r', encoding='utf-8')

basicContentTuple = json.loads(heroList.read())
detailedContentTuple = json.loads(heroDetailList.read())

heroInfoList = basicContentTuple['hero']
detailedInfo = detailedContentTuple['hero']

heroInfoListKeys = heroInfoList[0].keys()
detailedInfoKeys = detailedInfo.keys()

# print(heroInfoListKeys)
# print(detailedInfoKeys)

differentKeys = []

for i in heroInfoListKeys:
    if i not in detailedInfoKeys:
        differentKeys.append(i)

print(differentKeys)

sequenceNums = []
for i in heroInfoList:
    sequenceNums.append(i['heroId'])

# print(sequenceNums)
heroDetailList.close()

filePath = "..\\resources\\DetailedInfo\\"

nums = 0

for i in sequenceNums:
    fileName = filePath + str(i) + ".json"
    fileContent = None
    with open(fileName, 'r', encoding='utf-8') as fileObj:
        fileContent = json.loads(fileObj.read())

    with open(fileName, 'w', encoding='utf-8') as fileObj:
        # print("更新前长度:", len(fileContent['hero']))
        heroDetailInfoKeys = fileContent.keys()

        heroInfo = fileContent['hero']
        for k in differentKeys:
            fileContent['hero'][k] = heroInfoList[nums][k]

        # print("更新后长度:", len(fileContent['hero']))
        fileObj.write(json.dumps(fileContent, indent=2, ensure_ascii=False))
