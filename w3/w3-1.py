import requests as rq
import json

url = 'https://comic.naver.com/api/webtoon/titlelist/new?order=update'

webtoonsResult = rq.get(url).text

data = json.loads(webtoonsResult)
file_url = data['titleList'][1]['thumbnailUrl']
path_to_save = 'output/thumbnail.jpg'

# 헤더 추가 : 브라우저처럼 보이게 하기 위해
headers = { 
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = rq.get(file_url, headers=headers)
with open(path_to_save, 'wb') as file:
    file.write(response.content)