import requests
import pymysql
import json
import database.save_heroBasicInfo_as_database
import threading

All_heroId = database.save_heroBasicInfo_as_database.queryBasicInfo('hero', 'heroId')
path = '..\\..\\resources\\DetailedInfo\\{fileName}.json'


def getDetailedInfo(start, end):
    for i in range(start, end):
        heroId = All_heroId[i][0]
        url = 'https://game.gtimg.cn/images/lol/act/img/js/hero/{heroId}.js'.format(heroId=heroId)
        detail_info = requests.get(url)

        if detail_info.status_code is not 200:
            print('detail_info.status_code:', detail_info.status_code)
            return

        fileName = path.format(fileName=heroId)
        with open(fileName, 'w', encoding='utf-8') as file_object:
            file_object.write(json.dumps(detail_info.json(), indent=2, ensure_ascii=False))


def main():
    threads = []
    threadsLen = len(All_heroId)
    threadsNums = int(threadsLen / 10)
    print(threadsNums)
    start = 0
    end = 10
    for i in range(threadsNums):
        thread = threading.Thread(target=getDetailedInfo, args=(start, end))
        threads.append(thread)
        start = end
        end += 10
        thread.start()
        if threadsLen - end < 10:
            end = threadsLen


if __name__ == '__main__':
    main()
