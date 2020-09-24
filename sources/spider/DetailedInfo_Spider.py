import requests
import pymysql
import json

import threading


def get_DetailedInfo_Json(url):
    detail_info = requests.get(url)

    if detail_info.status_code == 200:
        return detail_info.json()
    else:
        return None
