import requests as rq
import json

url = 'https://comic.naver.com/api/webtoon/titlelist/new?order=update'

headers = {"referer" : "https://comic.naver.com/webtoon",\
           "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}

response = rq.get(url, headers=headers)
if response.status_code == 200:
    data = json.loads(response.text)
    print(data)
