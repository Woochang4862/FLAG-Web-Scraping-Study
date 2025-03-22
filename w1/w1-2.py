import requests
from bs4 import BeautifulSoup

url = 'https://www.naver.com'

response = requests.get(url)
if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    print(soup.title.string)
else :
    print(response.status_code)