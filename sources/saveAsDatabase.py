import pymysql

import json

# heroDB = pymysql.connect(host='localhost', user='root', password='sa', port=3306)
# cursor = heroDB.cursor()

def main():
    with open("..\\resources\\heroList.json", "r", encoding="utf8") as f:
        heroJsonStr = json.loads(f.read())
        if not 'hero' in heroJsonStr.keys():
            return

def create_database():
    pass

if __name__ == '__main__':
    main()