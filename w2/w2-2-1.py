# 네이버 웹툰 스크래핑 코드 작성
import requests as rq
from bs4 import BeautifulSoup

url = 'https://comic.naver.com/webtoon?tab=new'

html = rq.get(url).content
soup = BeautifulSoup(html,'lxml')

print(soup.body)
