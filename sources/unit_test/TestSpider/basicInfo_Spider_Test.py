import unittest
from spider import BasicInfo_Spider


class TestBasicInfoSpider(unittest.TestCase):
    def test_getHeroData(self):
        self.assertEqual(type(BasicInfo_Spider.getHeroData()), dict)

    def test_getHeroHeadProfileUrl(self):
        self.assertEqual(type(BasicInfo_Spider.getHeroHeadProfileUrl()), list)


if __name__ == '__main__':
    unittest.main()
