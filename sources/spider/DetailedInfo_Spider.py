import requests


def get_DetailedInfo_Json(url):
    """
    获取英雄详细信息的json数据并返回的函数.
    :param url: 类型为str.表示需要从网络中读取的json文件的网络路径.
    :return: 返回类型为str.表示从网络中读取的json数据.
    """
    detail_info = requests.get(url)

    if detail_info.status_code == 200:
        return detail_info.json()
    else:
        return None
