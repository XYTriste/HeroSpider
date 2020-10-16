import threading
from spider import DetailedInfo_Spider
from file import get_file_content
import json

PATH = '..\\resources\\DetailedInfo\\{fileName}.json'
detail_info_url = 'https://game.gtimg.cn/images/lol/act/img/js/hero/{heroId}.js'
"""
此处定义了三个全局变量,第一个All_heroId类型为元组.包含了从数据库中查询出来的所有的英雄的id.用于和第三个全局变量detail_info_url
进行组合格式化成为链接提取所有英雄的详细信息.
第二个全局变量path类型为str.表示抓取下来的JSON文件的存储路径.一般情况下没有必要不要去更改.
"""


def save_heroDetailedInfo_as_file(detail_info_json, filePath):
    """
    保存文件的方法.用于创建并写入JSON文件
    :param detail_info_json: 类型为str的json数据.用来写入文件
    :param filePath:文件存储的路径及文件名
    :return:保存文件的方法,无返回值.
    """
    with open(filePath, 'w', encoding='utf-8') as file_object:
        file_object.write(json.dumps(detail_info_json, indent=2, ensure_ascii=False))


def getDetailedInfo(start, end, All_heroId):
    """
    线程的回调方法.用于获取英雄详细信息的JSON数据并保存在文件中.
    :param start: 参数start,类型为int,表示从第几个开始提取
    :param end: 参数end,类型为int,表示提取到第几个结束
    :return: 无返回值.
    """
    for i in range(start, end):
        heroId = All_heroId[i]

        url = detail_info_url.format(heroId=heroId)
        detail_info_json = DetailedInfo_Spider.get_DetailedInfo_Json(url)

        filePath = PATH.format(fileName=heroId)
        save_heroDetailedInfo_as_file(detail_info_json, filePath)


def call_thread(All_heroId):
    threads = []
    threadsLen = len(All_heroId)
    threadsNums = int(threadsLen / 10)
    start = 0
    end = 10
    for i in range(threadsNums):
        thread = threading.Thread(target=getDetailedInfo, args=(start, end, All_heroId))
        threads.append(thread)
        start = end
        end += 10
        thread.start()
        if threadsLen - end < 10:
            end = threadsLen


def main():
    All_heroId = get_file_content.get_all_heroId()
    call_thread(All_heroId)


if __name__ == '__main__':
    main()
