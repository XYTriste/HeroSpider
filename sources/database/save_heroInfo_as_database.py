import pymysql

from file import get_file_content

heroDB = pymysql.connect(host='localhost', user='root', password='sa', port=3306)  # 链接数据库
cursor = heroDB.cursor()  # 获取数据库的游标

dataBaseName = 'heroInfo'


def create_database():
    sql = 'CREATE DATABASE IF NOT EXISTS ' + dataBaseName + ' DEFAULT CHARSET utf8'
    cursor.execute(sql)


def create_table(tableName, fieldName, primaryKey=None):
    sql = 'CREATE TABLE IF NOT EXISTS {tableName}'

    if tableName == 'hero' or tableName == 'skins' or tableName == 'spells':

        if tableName == 'spells':
            fieldName[-1] = "`" + fieldName[-1] + "`"

        sql += "("

        sql += " VARCHAR(255) NOT NULL,".join(fieldName)
        sql += " VARCHAR(255) NOT NULL, PRIMARY KEY({primaryKey})"

        if tableName != 'hero':
            sql += ",FOREIGN KEY (heroId) REFERENCES hero"

        sql += ")"

        sql = sql.format(tableName=tableName, primaryKey=primaryKey)

        cursor.execute(sql)


    else:
        sql += "({fieldName} VARCHAR(30) NOT NULL)"
        sql = sql.format(tableName=tableName, fieldName=fieldName)
        cursor.execute(sql)


def modify_table_type(tableName, fieldName):
    """

    :param tableName: 需要修改字段类型的表名
    :param fieldName: 需要修改的字段名称,一般情况下都是主键所在的字段
    :return:
    """
    """ 此处说明:在创建数据表时,由于将所有字段设置成了varchar类型,会导致主键内容被当作字符串进行排序.即默认顺序为: 1 10 101等
    所以额外增加了一个修改主键类型的函数用于将主键所在的字段类型修改为int"""
    sql = 'alter table {tableName} modify column {fieldName} int;'.format(tableName=tableName, fieldName=fieldName)
    cursor.execute(sql)


if __name__ == '__main__':
    create_database()
    cursor.execute("use " + dataBaseName + ";")
    heroListJson = get_file_content.get_detailedInfo_content('1')

    for key in heroListJson.keys():
        tableName = key
        fieldName = heroListJson[key]
        primaryKey = None

        if isinstance(fieldName, dict):
            fieldName = list(fieldName.keys())
            primaryKey = fieldName[0]
        elif isinstance(fieldName, list):
            fieldName = list(fieldName[0].keys())
            primaryKey = fieldName[0]
        else:
            fieldName = key

        print(tableName, fieldName, primaryKey)
        create_table(tableName, fieldName, primaryKey)
