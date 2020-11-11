"""
程序的入口.万恶之源2333.
"""
from spider import BasicInfo_Spider
from file import save_BasicInfo_as_file
from file import save_DetailedInfo_as_file
from file import get_file_content
from file import format_file

from database import save_heroInfo_as_database

import time


def file_operation():
    """
    文件操作的函数.首先获取英雄基本信息并保存到数据库.再使用selenium调用getHeroHeadProfileUrl()函数来
    获取英雄的头像链接.然后将头像链接作为一个键值对写入到文件.再重新写入文件内容.
    接着获取英雄的详细信息并保存到文件.最后对文件进行内容比对并合并.
    :return: 无返回值
    """
    basicHeroInfo = BasicInfo_Spider.getHeroData()
    save_BasicInfo_as_file.save_heroList_as_file(basicHeroInfo)

    heroHeadProfileUrl = BasicInfo_Spider.getHeroHeadProfileUrl()

    save_BasicInfo_as_file.insert_headProfileImage_as_file(basicHeroInfo, heroHeadProfileUrl)
    save_BasicInfo_as_file.save_heroList_as_file(basicHeroInfo)

    save_DetailedInfo_as_file.main()

    format_file.merge_file()


def database_operation():
    """
    数据库操作的函数,首先从指定路径中读取所有的文件名称.接着获取第一个文件的内容.从中读取文件中的所有键的名称.
    接着判断数据库是否已存在.如果不存在则创建数据库并写入所有内容.已存在则判断数据库的更新时间是否为最新并决定
    是否需要进行更新.完成所有操作后关闭数据库的游标与数据库的链接.
    :return:
    """
    files = get_file_content.get_all_files()

    heroListJson = get_file_content.get_detailedInfo_content(files[0])
    keys = list(heroListJson.keys())

    if not save_heroInfo_as_database.database_isExists():
        save_heroInfo_as_database.create_database()
        save_heroInfo_as_database.use_database()

        save_heroInfo_as_database.create_all_table(heroListJson, keys)
        save_heroInfo_as_database.insert_all_data(files, keys)

        print('Database created and data inserted.')
    else:
        save_heroInfo_as_database.use_database()

        fileUpdateTime = heroListJson['fileTime']
        if save_heroInfo_as_database.data_need_update(fileUpdateTime):
            save_heroInfo_as_database.update_all_date(files, keys)
        else:
            print('Data does not need to updated.')

    save_heroInfo_as_database.cursor.close()
    save_heroInfo_as_database.heroDB.close()


def main():
    file_operation()
    # time.sleep(3)
    # database_operation()


if __name__ == '__main__':
    main()
