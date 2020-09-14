import pymysql

import json


heroDB = pymysql.connect(host='localhost', user='root', password='sa', port=3306, db='heroinformation')
cursor = heroDB.cursor()

def main():
    with open("..\\resources\\heroList.json", "r", encoding="utf8") as f:
        heroJsonStr = json.loads(f.read())
        if 'hero' not in heroJsonStr.keys():
            return
        heroList = heroJsonStr['hero']
        attrs = list(heroList[0].keys())
        create_database()


def create_database():
    sql = 'CREATE DATABASE IF NOT EXISTS HeroInformation DEFAULT CHARSET utf8'
    cursor.execute(sql)


if __name__ == '__main__':
    main()
