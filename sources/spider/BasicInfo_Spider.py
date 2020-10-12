import requests

import json

from file import save_BasicInfo_as_file

from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC

path = "../../resources/BasicInfo/heroList.json"  # 全局变量.指定JSON数据文件路径.一般情况下不要随意更改


def getHeroData():
    """
    从指定链接中保存内容.链接是使用Ajax技术从网页中保存出来的.访问该链接可以获得一个
    保存了所有英雄部分信息的JSON对象
    :return: 抓取JSON数据的函数,无返回值
    """
    url = 'https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js'
    response = requests.get(url)
    heroListJson = response.json()

    save_BasicInfo_as_file.save_heroList_as_file(path, heroListJson)


def getHeroHeadProfileUrl():  # 获取英雄的头像链接
    """
    使用Selenium获取所有英雄头像的链接,首先创建一个selenium.webdriver.chrome对象.使用它的get方法打开指定网页.
    并指定一个显示等待的最大时间.接着构建一个指向所有的英雄头像图片的xpath路径,将所有英雄头像的WebElement对象获取下来.
    接着遍历每个对象并获取它们的src属性,即英雄头像的链接.最后使用列表生成并返回头像链接的列表.
    :return:
    """
    driver = webdriver.Chrome()
    driver.get('https://lol.qq.com/data/info-heros.shtml')

    wait = WebDriverWait(driver, 10)  # 为driver指定一个加载节点的最长等待时间

    headProfile_xpath = '//*[@id="jSearchHeroDiv"]/li/a/img'
    headProfileImages = wait.until(EC.presence_of_all_elements_located((By.XPATH, headProfile_xpath)))

    headProfileImagesList = [x.get_attribute('src') for x in headProfileImages]

    file = open(path, 'r', encoding='utf-8')
    heroListJson = json.loads(file.read())

    field_name = 'headProfileImage' # 将英雄头像链接保存至数据库时的字段名.如无必要不要随意更改
    save_BasicInfo_as_file.insert_headProfileImage_as_file(heroListJson, headProfileImagesList, field_name)


if __name__ == '__main__':
    getHeroData()
    getHeroHeadProfileUrl()
