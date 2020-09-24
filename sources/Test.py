"""
专门写各种奇怪测试的地方
"""
import json
import os

path = '..\\resources\\DetailedInfo'

for root, dirs, files in os.walk(path):
    for fileStr in files:
        time = None
        fileName = path + "\\" + fileStr
        with open(fileName, 'r', encoding='utf-8') as f:
            JsonStr = json.loads(f.read())
            if time is None or time != JsonStr['fileTime']:
                print(JsonStr['fileTime'])
                time = JsonStr['fileTime']
