import re

import pymysql

from file import get_file_content

import datetime

heroDB = pymysql.connect(host='localhost', user='root', password='sa', port=3306)  # 链接数据库
cursor = heroDB.cursor()  # 获取数据库的游标

DATABASE_NAME = 'heroInfo'  # 创建及使用的数据库的名称.一般情况下不要更改

spells_id = 1  # 此变量用于insert_data函数,作用是向spells表中添加数据时作为主键id字段的值使用.


def create_database():
    """
    创建数据库的函数.使用的字符集为utf-8
    :return: 该函数无返回值
    """
    global DATABASE_NAME
    global cursor

    sql = 'CREATE DATABASE IF NOT EXISTS ' + DATABASE_NAME + ' DEFAULT CHARSET utf8'
    cursor.execute(sql)


def create_table(tableName, fieldName, primaryKey=None):
    """
    创建数据库表的函数.
    :param tableName: 类型为str.值为需要创建的表的名称.
    :param fieldName: 类型为str或list.值为创建的表的所有字段名.
    :param primaryKey: 类型为str.值为创建的表的主键名称.默认值为None.因为有些表只有一条记录.不需要主键.
    :return: 该函数无返回值
    """

    global cursor

    sql = 'CREATE TABLE IF NOT EXISTS {tableName}'

    if tableName == 'hero' or tableName == 'skins' or tableName == 'spells':
        # 此处判断是因为除了这三个表以外其他的表都只有一个字段一条记录.fieldName参数为str类型.所以需要进行另一种sql语句拼接.

        if tableName == 'spells':
            # 此处判断是因为在json文件中的key为spells时.取出来的filedName为一个list.其中最后一个filed[-1]的值为range.
            # 而range是sql中的一个关键字.所以需要用间隔号包含起来表明它作为创建表的字段名.
            fieldName.insert(0, 'id')

            fieldName[-1] = "`" + fieldName[-1] + "`"
        elif tableName == 'hero':
            # 与上面同理.此时fieldName[1]的值为name.也是sql中的关键字
            # 10月12更新注释,name不是sql的关键字,但是range是.

            fieldName[1] = '`' + fieldName[1] + '`'

        sql += "("

        sql += " VARCHAR(255) NOT NULL,\n".join(fieldName)
        sql += " VARCHAR(255) NOT NULL, PRIMARY KEY({primaryKey}))"

        sql = sql.format(tableName=tableName, primaryKey=(primaryKey if tableName != 'spells' else 'id'))

        # print(sql)

        cursor.execute(sql)

        if tableName == 'spells':
            modify_field_type(tableName, 'id')
        modify_field_type(tableName=tableName, fieldName='heroId')
        # 修改字段类型.因为在创建表时不够灵活的缘故.主键字段类型同样被设置为varchar.为了方便数据排序以及查询.所以需要将主键字段类型修改为int.
        # 说明:当字段类型为varchar时.数字将作为ASCII码值进行排序.

        if tableName != 'hero':
            # 同样是因为不够灵活的缘故.在创建表的时候不便设置外键.所以添加判断为除了hero以外的表添加对hero表中的heroId字段的外键映射.
            # modify_field_type(tableName=tableName, fieldName=fieldName[0])
            modify_field_attr(tableName)

    else:
        sql += "({fieldName} VARCHAR(30) NOT NULL)"
        sql = sql.format(tableName=tableName, fieldName=fieldName)
        cursor.execute(sql)

    print('Table {tableName} is created.'.format(tableName=tableName))


def modify_field_type(tableName, fieldName):
    """
    该方法用于在创建表以后修改主键所在的字段.由于水平有限创建表的语句使用拼接生成类型固定为varchar.
    为了方便数据在数据库中的排序以及查询方便.所以需要将主键字段更改为int类型.
    :param tableName: 需要修改字段类型的表名
    :param fieldName: 需要修改的字段名称,一般情况下都是主键所在的字段
    :return:
    """
    """ 此处说明:在创建数据表时,由于将所有字段设置成了varchar类型,会导致主键内容被当作字符串进行排序.即默认顺序为: 1 10 101等
    所以额外增加了一个修改主键类型的函数用于将主键所在的字段类型修改为int"""

    global cursor

    sql = 'alter table {tableName} modify column {fieldName} int;'.format(tableName=tableName,
                                                                          fieldName=fieldName)
    cursor.execute(sql)


def modify_field_attr(tableName, majorTableName='hero', fieldName='heroId'):
    """
    修改字段属性的函数.目前的作用仅仅是为表设置外键.
    :param tableName: 需要修改的表的名称.
    :param majorTableName:外键对应的主键所在的表名称.
    :param fieldName:添加外键的字段名.需要和主键对应的字段名一致.(因为sql的代码语句只写了这么简单的...)
    :return:该函数无返回值
    """

    global cursor

    sql = 'alter table {tableName} add constraint {tableName}_ID foreign key({fieldName}) REFERENCES {' \
          'majorTableName}({majorFieldName});'.format(
        tableName=tableName, fieldName=fieldName, majorTableName=majorTableName, majorFieldName='heroId')
    cursor.execute(sql)


def insert_data(tableName, fieldName, values, isSpeclia=False):
    """
    添加数据的函数.整体逻辑是首先初始化一个可格式化的sql语句字符串.
    然后通过判断表名来判断数据要插入的是否是一张特殊表(特殊表与普通表的区别就是特殊表的内容是每个文件都具有的且值相同.所以特殊表只进行一次存储)
    如果是特殊表且表不为空则表明数据表已有特殊数据.不需要进行插入.
    接着对fieldName参数进行模式匹配.这里的作用是判断字段名中是否包含了range.range作为sql的关键字,被用作字段名是需要使用分隔符(`)包含起来.
    该if对参数进行了匹配且进行了更正.
    最后将字符串格式化并尝试执行sql语句.执行成功则cursor.execute()返回非None.进行提交操作.否则进行异常处理并对数据库回滚.

    :param tableName: 类型为str,表示插入数据的表的表名.
    :param fieldName: 类型为str,表示插入数据的表的字段名.
    :param values: 类型为str.表示插入的表的值.
    :param isSpeclia: 类型为布尔值.表示插入的是否是特殊表.默认情况下值为False.表明插入的是一张普通表.
    :return: 插入数据的函数.无返回值.
    """
    global heroDB
    global cursor
    global spells_id

    sql = 'Insert into {tableName}({fieldName}) values ({values})'

    if isSpeclia:
        if not table_isEmpty(tableName):
            return

    if re.search(',range', fieldName) is not None:
        # 特殊判断,与创建表时的问题相同.range作为sql的关键字.必须使用分隔符括起来才不会有sql语法错误.
        fieldName = fieldName.replace('range', '`range`')
        fieldName = "id," + fieldName

        values = str(spells_id) + "," + values
        spells_id += 1

    sql = sql.format(tableName=tableName, fieldName=fieldName, values=values)
    # print(sql)
    try:
        if cursor.execute(sql):
            print('Insert Successful')
            heroDB.commit()
    except Exception as e:
        print(e)
        print('Insert Failed')
        heroDB.rollback()


def data_need_update(fileUpdateTime, fieldName='fileTime'):
    """

    :param fileUpdateTime: 类型为str.可用datetime包格式化为日期时间.表示文件更新的时间.用于比对数据库的更新时间判断是否需要更新.
    :param fieldName: 从数据库中查询时间的字段名.由于特殊性.存储时间的表名与它的列名一致.
    :return: 当数据库时间与文件更新时间不一致时返回True.否则返回False.
    """
    global cursor

    tableName = fieldName
    queryUpdateTimeFromDatabase = 'select {fieldName} from {tableName}'
    queryUpdateTimeFromDatabase = queryUpdateTimeFromDatabase.format(tableName=tableName, fieldName=fieldName)

    cursor.execute(queryUpdateTimeFromDatabase)
    databaseUpdateTime = cursor.fetchone()[0]

    fut = datetime.datetime.strptime(fileUpdateTime,
                                     '%Y-%m-%d %H:%M:%S')
    dut = datetime.datetime.strptime(databaseUpdateTime,
                                     '%Y-%m-%d %H:%M:%S')

    # print('fut:', fut)
    # print('dut', dut)
    total_seconds = (fut - dut).total_seconds()

    if total_seconds > 0.0:
        return True
    else:
        return False


def update_data(tableName, formatDate, fieldName, value, isSpecial=False):
    if not isSpecial:
        sql = 'update {tableName} set {formatDate} where {fieldName} = {value}'
        sql = sql.format(tableName=tableName, formatDate=formatDate, fieldName=fieldName, value=value)
    else:
        sql = 'update {tableName} set {formatDate}'
        sql = sql.format(tableName=tableName, formatDate=formatDate)
    try:
        if cursor.execute(sql):
            print('Update Successful')
            heroDB.commit()
    except Exception as e:
        print(e)
        print('Update Failed')
        heroDB.rollback()


def table_isExists(tableName):
    """
    判断表是否存在的函数
    :return: 如果hero表存在返回True，否则返回false
    """

    global cursor

    sql = 'show tables;'
    cursor.execute(sql)
    tables = [cursor.fetchall()]
    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]

    # print(table_list)

    if tableName in table_list:
        return True
    else:
        return False


def table_isEmpty(tableName):
    """
    判断表是否为空的函数,用于判断存储了相同信息的特殊表中是否有内容.如果有内容的话则不需要再存一遍了.
    :param tableName: 类型为str,表示需要判断的表的名称.
    :return: 返回表是否为空.是则返回True,否则返回False
    """
    sql = 'select * from {tableName}'.format(tableName=tableName)  # 从参数tableName作为表名的表中查询所有数据
    if cursor.execute(sql) > 0:  # 如果查询到的结果条数大于0则非空.
        return False
    else:
        return True


def create_all_table(keys):
    """
    创建所有表的函数.根据参数keys的值来逐个遍历并创建表.
    :param keys: 类型为list.存储了所有的表名.
    :return: 创建表的函数,无返回值
    """
    if not table_isExists(keys[0]):
        for key in keys:
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

            create_table(tableName, fieldName, primaryKey)


def insert_all_data(files, keys):
    """
    添加所有表的数据的函数.根据文件名读取内容并取出.逐个存入表中.keys参数是表的名称.根据表的名称的不同所做的操作也不同.
    :param files: 类型为list.包含所有的需要插入的表的数据文件的名称.
    :param keys: 类型为list.包含所有的表的名称.
    :return: 插入数据函数无返回值.
    """
    for file in files:
        fileContent = get_file_content.get_detailedInfo_content(file)
        for key in keys:
            tableName = key

            if tableName == 'hero':
                dataKeysList = list(fileContent[key].keys())
                dataValuesList = list(fileContent[key].values())

                dataKeys = ",".join(dataKeysList)
                dataValues = ",\n".join('%s' % "\'" + " - ".join(val) + "\'"
                                        if isinstance(val, list) else "\'" + val + "\'" for val in dataValuesList)
                insert_data(tableName, dataKeys, dataValues)

            elif tableName == 'skins' or tableName == 'spells':
                dataKeysList = list(fileContent[key][0].keys())
                dataValuesList = fileContent[key]

                dataKeys = ",".join(dataKeysList)
                for dataValues in dataValuesList:
                    value = []
                    for dataKey in dataKeysList:
                        dataValue = dataValues[dataKey]
                        value.append(dataValue)
                    try:
                        values = ",\n".join('%s' % "\'" + " - ".join(val) + "\'"
                                            if isinstance(val, list) else "\'" + str(val) + "\'" for val in value)
                    except Exception as e:
                        print(value)
                    insert_data(tableName, dataKeys, values)

            else:
                dataKeys = key
                dataValue = "\'" + fileContent[key] + "\'"

                insert_data(tableName, dataKeys, dataValue, True if tableName != 'fileName' else False)


def update_all_date(files, keys):
    for file in files:
        fileContent = get_file_content.get_detailedInfo_content(file)

        for key in keys:
            tableName = key
            if tableName == 'hero':
                fieldNames = list(fileContent[key].keys())
                values = list(fileContent[key].values())
                # print(fieldNames, values)

                if len(fieldNames) != len(values):
                    raise Exception('数据完整性有问题.')

                formatData = []
                for key, value in zip(fieldNames, values):
                    if isinstance(value, list):
                        value = "-".join(value)
                    formatData.append(str(key + '=' + '\'' + value + '\''))

                formatData = ",".join(formatData)
                fieldName = fieldNames[0]
                value = values[0]
                update_data(tableName, formatData, fieldName, value)
            elif tableName == 'skins':
                datas = fileContent[key]
                for data in datas:
                    fieldNames = list(data.keys())
                    values = list(data.values())
                    formatData = []
                    for key, value in zip(fieldNames, values):
                        if isinstance(value, list):
                            value = "-".join(value)
                        formatData.append(str(key + '=' + '\'' + value + '\''))

                formatData = ",".join(formatData)
                fieldName = fieldNames[0]
                value = values[0]
                update_data(tableName, formatData, fieldName, value)
            elif tableName == 'spells':
                datas = fileContent[key]
                for data in datas:
                    fieldNames = list(data.keys())
                    values = list(data.values())
                    formatData = []

                    fieldNames[fieldNames.index('range')] = "`" + fieldNames[fieldNames.index('range')] + "`"

                    for key, value in zip(fieldNames, values):
                        if isinstance(value, list):
                            value = "-".join(value)
                        elif isinstance(value, bool):
                            value = "0"
                        formatData.append(str(key + '=' + '\'' + value + '\''))

                    formatData = ",".join(formatData)
                    fieldName = fieldNames[0]
                    value = values[0]

                    update_data(tableName, formatData, fieldName, value)
            else:
                formatData = str(key + '=' + '\'' + fileContent[key] + '\'')
                update_data(tableName, formatData, None, None, True)


if __name__ == '__main__':
    # create_database()
    cursor.execute("use " + DATABASE_NAME + ";")

    files = get_file_content.get_all_files()

    heroListJson = get_file_content.get_detailedInfo_content(files[0])
    keys = list(heroListJson.keys())

    # create_all_table(keys)
    #
    # insert_all_data(files, keys)
    update_all_date(files, keys)
