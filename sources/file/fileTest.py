from database import save_heroInfo_as_database
from file import get_file_content

# save_heroInfo_as_database.cursor.execute('use heroInfo')
# fileName = get_file_content.get_all_files()[0]
# fileContent = get_file_content.get_detailedInfo_content(fileName)
# fileUpdateTime = fileContent['fileTime']
# print(save_heroInfo_as_database.data_need_update(fileUpdateTime))

import os
files = os.listdir('../../resources')
print(files)