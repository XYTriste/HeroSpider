from database import save_heroBasicInfo_as_database
from database import save_heroInfo_as_database
"""
程序的入口.万恶之源2333.
"""
# save_heroBasicInfo_as_database.main()  # 将数据保存进数据库.包含抓取操作等.
save_heroInfo_as_database.cursor.execute('use heroInfo')
print(save_heroInfo_as_database.cursor.execute('select * from fileTime'))
print(save_heroInfo_as_database.table_isEmpty('fileTime'))
