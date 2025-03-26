import requests as rq
from bs4 import BeautifulSoup

order = 'POPULARITY' # RECENT : 최신, POPULARITY : 인기

url = f'https://ridibooks.com/new-releases/general?order={order}&page=1'
response = rq.get(url)
if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    last_page = soup.select('#__next > main > section > div:nth-child(5) > div > ul > li:last-child > a')
    last_page = int(last_page[0].text.strip('페이지'))
else:
    print('실패!')
    exit()

for page in range(1, last_page+1):
    url = f'https://ridibooks.com/new-releases/general?order={order}&page={page}'
    response = rq.get(url)
    print('-'*45+f' 페이지 : {page} ' + '-'*45)
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
        
    print('-'*100)