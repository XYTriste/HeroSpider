"""
程序的入口.万恶之源2333.
"""
from spider import BasicInfo_Spider
from file import save_BasicInfo_as_file
from file import save_DetailedInfo_as_file

basicHeroInfo = BasicInfo_Spider.getHeroData()
save_BasicInfo_as_file.save_heroList_as_file(basicHeroInfo)
heroHeadProfileUrl = BasicInfo_Spider.getHeroHeadProfileUrl()

save_BasicInfo_as_file.insert_headProfileImage_as_file(basicHeroInfo, heroHeadProfileUrl)
save_BasicInfo_as_file.save_heroList_as_file(basicHeroInfo)

save_DetailedInfo_as_file.main()

