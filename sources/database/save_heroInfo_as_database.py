import pymysql

heroDB = pymysql.connect(host='localhost', user='root', password='sa', port=3306)  # 链接数据库
cursor = heroDB.cursor()  # 获取数据库的游标

dataBaseName = 'heroInfo'


def create_database():
    sql = 'CREATE DATABASE IF NOT EXISTS ' + dataBaseName + ' DEFAULT CHARSET utf8'
    cursor.execute(sql)


def create_table(tableName, fieldName):
    if tableName == 'hero':
        pass
    elif tableName == 'skins':
        pass
    elif tableName == 'spells':
        pass
    else:
        sql = 'CREATE TABLE IF NOT EXISTS ' + tableName + "(" + tableName + " VARCHAR(30) NOT NULL)"
