import requests as rq
from bs4 import BeautifulSoup

url = 'https://ridibooks.com/new-releases/general?order=POPULARITY&page=1'

response = rq.get(url)
if response.status_code == 200:
    # 성공
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('#__next > main > section > ul.fig-wzw9xn.eis6k7i0 > li')
    for item in items:
        title = item.select_one('div > div.b-o96tbl > div.b-1fj4gry > a')
        if not title:
            title = item.select_one('div')
        print(title.text)
else:
    # 실패
    print('실패!')