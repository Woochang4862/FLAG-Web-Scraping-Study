import requests as rq
from bs4 import BeautifulSoup

url = 'https://ridibooks.com/new-releases/general?order=POPULARITY&page=1'

html = rq.get(url).content
soup = BeautifulSoup(html,'lxml')
items = soup.select('main > section > ul.fig-1pep8jc.eis6k7i0 > li')
for item in items[:5]:
    title = item.select_one('div > div.b-o96tbl > div.b-1fj4gry > a')
    description = item.select_one('div.b-1int8gb > a > p')
    print('-'*100)
    print(f'제목 : {title.text}')
    print(f'내용 : \n{description.text}')
    print('-'*100)