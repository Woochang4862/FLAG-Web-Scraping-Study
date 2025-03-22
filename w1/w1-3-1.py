import requests as rq
from bs4 import BeautifulSoup

url = 'https://ridibooks.com/new-releases/general?order=POPULARITY&page=1'

response = rq.get(url)
if response.status_code == 200:
    # 성공
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('#__next > main > section > ul.fig-1pep8jc.eis6k7i0 > li')
    for item in items[:5]:
        title = item.select_one('div > div.b-o96tbl > div.b-1fj4gry > a')
        description = item.select_one('div > div.b-o96tbl > div.b-1int8gb > a > p')
        print('-'*100)
        print(title.text)
        print()
        print(description.text)
        print('-'*100)
else:
    # 실패
    print('실패!')