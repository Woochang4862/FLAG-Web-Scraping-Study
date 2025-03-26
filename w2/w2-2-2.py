import requests as rq
import json
url = 'https://comic.naver.com/api/webtoon/titlelist/new?order=update'

webtoonsResult = rq.get(url).text

data = json.loads(webtoonsResult)

for item in data['titleList']:
    print(item['titleName'])
