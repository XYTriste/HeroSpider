# This file is stop updating and deprecated.
import pymysql

import json

import re

from spider import BasicInfo_Spider

import datetime

heroDB = pymysql.connect(host='localhost', user='root', password='sa', port=3306)  # 链接数据库
cursor = heroDB.cursor()  # 获取数据库的游标

heroBasicDataBaseName = 'heroInformation'
heroBasicInfoName = 'hero'  # 保存了英雄基本信息的表名.一般情况下不需要更改


def create_database():  # 创建数据库的函数
    sql = 'CREATE DATABASE IF NOT EXISTS HeroInformation DEFAULT CHARSET utf8'
    cursor.execute(sql)


def create_table(keys, table):  # 创建表的函数

    if table == 'hero':
        # 此处说明:由于暂时的水平有限,所以只能把所有字段都设置为字符型,长度固定,等以后技术提升了再想办法更新.
        sql = "CREATE TABLE IF NOT EXISTS " + table + "("
        sql += " VARCHAR(150) NOT NULL,".join(keys)
        sql += " VARCHAR(255) NOT NULL, PRIMARY KEY (heroId))"
        cursor.execute(sql)
        modify_table_type()
    else:
        sql = 'CREATE TABLE IF NOT EXISTS ' + table + "(" + table + " VARCHAR(30) NOT NULL)"
        cursor.execute(sql)


def modify_table_type(table, fieldName):
    """ 此处说明:在创建数据表时,由于将所有字段设置成了varchar类型,会导致主键内容被当作字符串进行排序.即默认顺序为: 1 10 101等
    所以额外增加了一个修改主键类型的函数用于将主键所在的字段类型修改为int"""
    sql = 'alter table ' + table + ' modify column ' + fieldName + ' int;'
    cursor.execute(sql)


def insert_data(table, heroList, keys):
    """
    :param table: 添加数据的表名,由于目前尚不完善.只能传递\'hero\'值
    :param heroList: 添加数据的列表,类型为字典.
    :param keys: 字典的key组,目的是为了获取该字典的值
    :return: 该函数为添加数据的函数,无返回值
    """

    heroListLen = len(heroList)
    print("heroListLen", heroListLen)
    for i in range(heroListLen):
        attrs = ",".join(heroList[i].keys())
        values = ",".join(
            '%s' % "\'" + " - ".join(val) + "\'" if isinstance(val, list) else "\'" + val + "\'" for val in
            heroList[i].values())
        # print(values)
        sql = "Insert into {table}({keys}) VALUES ({values})".format(table=table, keys=attrs, values=values)
        # print(sql)
        try:
            if cursor.execute(sql):
                print('Successful')
                heroDB.commit()
        except Exception as e:
            print(sql)
            print('Failed')
            heroDB.rollback()


def insert_other_data(heroJsonStr, keys):
    """

    :param heroJsonStr: 使用Json.loads()方法从文件中读取出来的JSON数据.是一个具有四个key的字典
    :param keys: heroJsonstr的key值组.目的是为了提取对应的值
    :return:该函数为添加文件名数据、文件更新时间数据、以及版本号进入数据库的函数,无返回值
    """
    for key in keys:
        data = heroJsonStr[key]
        table = key
        sql = "Insert into {table}({keys}) VALUES (\'{values}\')".format(table=table, keys=key, values=data)
        try:
            if cursor.execute(sql):
                print('OtherData Successful')
                heroDB.commit()
        except Exception as e:
            print('OtherData Failed')
            heroDB.rollback()


def table_isExists():
    """
    判断表是否存在的函数
    :return: 如果hero表存在返回True，否则返回false
    """
    sql = 'show tables;'
    cursor.execute(sql)
    tables = [cursor.fetchall()]
    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]

    # print(table_list)

    if heroBasicInfoName in table_list:
        return True
    else:
        return False


def update_data(table, keys, values):
    """
    更新数据库中数据的函数
    :param table: 需要进行更新的表名
    :param keys: 需要更新的表的字段名
    :param values: 需要更新的表的值
    :return: 更新函数，无返回值
    """
    if table is heroBasicInfoName:  # 对hero表的更新(以后有时间可以修改为匹配文件中发生更新的行,只对发生更新的行对应的数据进行更新)
        formatData = []
        for key, value in zip(keys, values):
            if isinstance(value, list):
                value = value[0]
            # print(type(key))
            formatData.append(str(key + '=' + '\'' + value + '\''))
        formatData = ",".join(formatData)

        # print(formatData)

        updateSql = 'UPDATE ' + table + ' SET ' + formatData + ' WHERE ' + list(keys)[0] + ' = ' + list(values)[0]
        # 构建更新hero表的sql语句

        try:
            if cursor.execute(updateSql):
                print('Update Successful')
                heroDB.commit()
        except:
            print('Update Failed')
            heroDB.rollback()
    else:
        updateSql = 'UPDATE ' + table + ' SET {keys} = \'{values}\''.format(keys=keys, values=values)
        print(updateSql)
        try:
            cursor.execute(updateSql)
            heroDB.commit()
        except:
            print('Update Failed')
            heroDB.rollback()


def queryBasicInfo(tableName, fieldName):
    cursor.execute("use heroinformation;")
    sql = 'SELECT {fieldName} from {tableName}'.format(fieldName=fieldName, tableName=tableName)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def main():
    """
    主函数,首先从爬虫中读取数据.然后打开一个保存了爬下来的数据的文件.
    判断数据文件的内容是否正确.不正确的情况下则直接结束程序.正确时
    查询数据库是否存在,根据数据库是否存在进行下一步的操作.
    :return:主函数,无返回值
    """

    BasicInfo_Spider.getHeroData()
    BasicInfo_Spider.getHeroHeadProfileUrl()

    with open(BasicInfo_Spider.path, "r", encoding="utf8") as f:
        heroJsonStr = json.loads(f.read())

        if heroBasicInfoName not in heroJsonStr.keys():  # 这一行的作用是判断读出来的文件内容对不对,如果是正确的内容则在json中有一个key值为hero.
            print("Hero is not in heroJsonStr")
            return
        heroList = heroJsonStr[heroBasicInfoName]  # 获取读取的json数据的hero键的值,应该是一个长度为150的json对象列表
        keys = list(heroList[0].keys())  # 获取hero列表每一个对象的所有key,由于每个对象的key都相同,所以直接取下标为0的hero的key.

        cursor.execute(
            "SELECT * FROM information_schema.SCHEMATA where SCHEMA_NAME='heroinformation';")  #
        # 查询数据库列表中是否有名为heroinformation的数据库

        if cursor.fetchall() == ():  # 如果查询的结果为一个空元组,则无该数据库,进行创建并添加数据的操作
            create_database()  # 创建hero数据库
            cursor.execute("use heroinformation;")

            create_table(keys)  # 根据文件中读取出来的hero对象的key值列表创建数据表.
            insert_data(heroBasicInfoName, heroList, keys)

            other_keys = ['version', 'fileName', 'fileTime']
            for key in other_keys:
                create_table(None, key)
            insert_other_data(heroJsonStr, other_keys)

        else:   # 如果查询有结果则数据库存在,使用该数据库并判断是否更新数据,需要更新则更新数据
            cursor.execute("use heroinformation;")

            other_keys = ['version', 'fileName', 'fileTime']

            fileUpdateTime = heroJsonStr['fileTime']
            print(fileUpdateTime)
            queryUpdateTimeSql = 'select fileTime from filetime;'
            cursor.execute(queryUpdateTimeSql)
            dataBaseUpdateTime = cursor.fetchone()[0]

            # 将字符串格式化为日期方便进行比对
            fut = datetime.datetime.strptime(fileUpdateTime, '%Y-%m-%d %H:%M:%S')  # fut是fileUpdateTime的缩写
            dut = datetime.datetime.strptime(dataBaseUpdateTime, '%Y-%m-%d %H:%M:%S')  # dut是dataBaseUpdateTime的缩写

            total_seconds = (dut - fut).total_seconds()

            if total_seconds > 0.0:
                for i in range(len(heroList)):
                    update_data('hero', heroList[i].keys(), heroList[i].values())
                for t in other_keys:
                    key = t
                    value = heroJsonStr[key]
                    update_data(t, key, value)
            else:
                print('Data needn\'t update')