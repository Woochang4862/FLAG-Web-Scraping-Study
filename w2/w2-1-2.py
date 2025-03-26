import requests as rq
from bs4 import BeautifulSoup
import urllib.parse

url = 'https://ridibooks.com/new-releases/general?order=POPULARITY&page=1'

html = rq.get(url).content
soup = BeautifulSoup(html,'lxml')
items = soup.select('main > section > ul:nth-of-type(2) > li') # nth-of-type(2) : 두번째 ul 태그
for item in items[:5]:
    title = item.select_one('div > div:nth-of-type(2) > div:nth-of-type(1) > a')
    description = item.select_one('div > div:nth-of-type(2) > div:nth-of-type(2) > a > p')
    link = item.select_one('div > div:nth-of-type(1) > a')
    # url 에 경로 연결
    book_link = urllib.parse.urljoin(url, link.get('href'))
    print('-'*100)
    print(f'제목 : {title.text}')
    print(f'내용 : \n{description.text}')
    print(f'링크 : {book_link}')
    print('-'*100)