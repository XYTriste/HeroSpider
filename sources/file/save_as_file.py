from spider import BasicInfo_Spider

import json


def save_heroList_as_file(path, heroListJson):
    with open(BasicInfo_Spider.path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(heroListJson, indent=2, ensure_ascii=False))


def insert_headProfileImage_as_file(heroListJson, headProfileImagesList, fieldName):
    """
    将英雄头像的链接保存到抓取下来的JSON文件中.首先将key为hero的值提取出来.结果为一个类型为列表的heroList
    列表中的每一个元素的类型为一个元组.分别是每个英雄的信息.遍历这个列表并向每个元组插入一个键值对.最后读取文件中
    其他的内容并一同存入新的对象中.最后将新的对象写入到文件.
    :param heroListJson: 从文件中读取出来的JSON数据.作为元组参数被传递到该方法中来
    :param headProfileImagesList: 所有英雄头像的链接,类型为一个列表
    :param fieldName: 数据库中保存英雄头像链接的字段名.如无必要不要随意修改
    :return: 无返回值
    """

    heroList = heroListJson['hero']
    if len(heroList) == len(headProfileImagesList):
        for i in range(len(heroList)):
            heroList[i][fieldName] = headProfileImagesList[i]

    newJson = {'hero': heroList}
    for key in heroListJson.keys():
        if key is not 'hero':
            newJson[key] = heroListJson[key]

    with open(BasicInfo_Spider.path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(newJson, indent=2, ensure_ascii=False))


