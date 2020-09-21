import pymysql

import json

import re

import Spider

import datetime

heroDB = pymysql.connect(host='localhost', user='root', password='sa', port=3306)  # 链接数据库
cursor = heroDB.cursor()  # 获取数据库的游标


def create_database():  # 创建数据库的函数
    sql = 'CREATE DATABASE IF NOT EXISTS HeroInformation DEFAULT CHARSET utf8'
    cursor.execute(sql)


def create_table(keys, table='hero'):  # 创建表的函数

    if table == 'hero':
        # 此处说明:由于暂时的水平有限,所以只能把所有字段都设置为字符型,长度固定,等以后技术提升了再想办法更新.
        sql = "CREATE TABLE IF NOT EXISTS hero("
        sql += " VARCHAR(60) NOT NULL,".join(keys)
        sql += " VARCHAR(255) NOT NULL, PRIMARY KEY (heroId))"
        cursor.execute(sql)
        modify_table_type()
    else:
        sql = 'CREATE TABLE IF NOT EXISTS ' + table + "(" + table + " VARCHAR(30) NOT NULL)"
        cursor.execute(sql)


def modify_table_type():
    """ 此处说明:在创建数据表时,由于将所有字段设置成了varchar类型,会导致主键内容被当作字符串进行排序.即默认顺序为: 1 10 101等
    所以额外增加了一个修改主键类型的函数用于将主键所在的字段类型修改为int """
    sql = 'alter table hero modify column heroId int;'
    cursor.execute(sql)


def insert_data(table, heroList, keys):
    heroListLen = len(heroList)
    print("heroListLen", heroListLen)
    for i in range(heroListLen):
        attrs = ",".join(heroList[i].keys())
        values = ",".join(
            '%s' % "\'" + " and ".join(val) + "\'" if isinstance(val, list) else "\'" + val + "\'" for val in
            heroList[i].values())
        # print(values)
        sql = "Insert into {table}({keys}) VALUES ({values})".format(table=table, keys=attrs, values=values)
        # print(sql)
        try:
            if cursor.execute(sql):
                print('Successful')
                heroDB.commit()
        except Exception as e:
            print(e)
            print('Failed')
            heroDB.rollback()


def insert_other_data(heroJsonStr, keys):
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
    sql = 'show tables;'
    cursor.execute(sql)
    tables = [cursor.fetchall()]
    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]

    # print(table_list)

    if 'hero' in table_list:
        return True
    else:
        return False


def update_data(table, keys, values):
    if table is 'hero':  # 对hero表的更新(以后有时间可以修改为匹配文件中发生更新的行,只对发生更新的行对应的数据进行更新)
        formatData = []
        for key, value in zip(keys, values):
            if isinstance(value, list):
                value = value[0]
            # print(type(key))
            formatData.append(str(key + '=' + '\'' + value + '\''))
        formatData = ",".join(formatData)

        # print(formatData)

        updateSql = 'UPDATE ' + table + ' SET ' + formatData + ' WHERE ' + list(keys)[0] + ' = ' + list(values)[0]
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


def main():
    Spider.getData()
    with open("..\\resources\\heroList.json", "r", encoding="utf8") as f:
        heroJsonStr = json.loads(f.read())

        if 'hero' not in heroJsonStr.keys():  # 这一行的作用是判断读出来的文件内容对不对,如果是正确的内容则在json中有一个key值为hero.
            print("Hero is not in heroJsonStr")
            return
        heroList = heroJsonStr['hero']  # 获取读取的json数据的hero键的值,应该是一个长度为150的json对象列表
        keys = list(heroList[0].keys())  # 获取hero列表每一个对象的所有key,由于每个对象的key都相同,所以直接取下标为0的hero的key.

        cursor.execute(
            "SELECT * FROM information_schema.SCHEMATA where SCHEMA_NAME='heroinformation';")  #
        # 查询数据库列表中是否有名为heroinformation的数据库

        if cursor.fetchall() == ():  # 如果查询的结果为一个空元组,则无该数据库,进行创建并添加数据的操作
            create_database()  # 创建hero数据库
            cursor.execute("use heroinformation;")

            create_table(keys)  # 根据文件中读取出来的hero对象的key值列表创建数据表.
            insert_data('hero', heroList, keys)

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


if __name__ == '__main__':
    main()
