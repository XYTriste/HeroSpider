import unittest
from spider import DetailedInfo_Spider


class TestDetailedInfoSpider(unittest.TestCase):
    def test_getDetailedInfoUrl(self):
        url = 'https://game.gtimg.cn/images/lol/act/img/js/hero/1.js'
        self.assertEqual(type(DetailedInfo_Spider.get_DetailedInfo_Json(url)), dict)


if __name__ == '__main__':
    unittest.main()
