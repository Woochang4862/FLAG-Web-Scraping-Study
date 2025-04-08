import requests as rq
import json
import os

url = 'https://comic.naver.com/api/webtoon/titlelist/new?order=update'

webtoonsResult = rq.get(url).text

data = json.loads(webtoonsResult)
file_url = data['titleList'][6]['thumbnailUrl']
path_to_save = '../output/thumbnail.jpg'

# 헤더 추가 : 브라우저처럼 보이게 하기 위해
headers = { 
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
}

response = rq.get(file_url, headers=headers)
if not os.path.exists("../output"):
    os.makedirs("../output")
with open(path_to_save, 'wb') as file:
    file.write(response.content)