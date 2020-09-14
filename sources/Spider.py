import requests

import json

url = 'https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js'
response = requests.get(url)
heroListJson = response.json()
with open("..\\resources\\heroList.json", 'w', encoding='utf-8') as f:
    f.write(json.dumps(heroListJson, indent=2, ensure_ascii=False))