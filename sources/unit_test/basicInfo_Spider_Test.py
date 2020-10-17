import unittest
from spider import BasicInfo_Spider


class TestBasicInfoSpider(unittest.TestCase):
    def test_getHeroData(self):
        self.assertEquals(type(BasicInfo_Spider.getHeroData()), str)


if __name__ == '__main__':
    unittest.main()
