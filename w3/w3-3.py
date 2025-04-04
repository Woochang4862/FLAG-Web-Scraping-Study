import requests as rq
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 로그인 url
login_url = "http://dowellcomputer.com/member/memberLoginForm.jsp"

# 로그인 정보
login_info = {
  'memberID' : 'ds2023',
  'memberPassword' : '2023ds'
}

# 크롤링할 url
target_url = f"http://dowellcomputer.com/member/memberUpdateForm.jsp?ID={login_info['memberID']}"

#세션 만들기
with rq.Session() as s:
    ## action url 만들기
    res = s.get(login_url)
    soup = BeautifulSoup(res.text, 'lxml')
    action = soup.select_one('form').get('action')
    action_url = urljoin(login_url, action)
    ## login 요청
    login_res = s.post(action_url, data=login_info)
    if login_res.status_code != 200:
      raise Exception("로그인 실패")
    ## 사용자 정보(email 주소) 추출

    print(dict(s.cookies))
    res = s.get(target_url)
    soup = BeautifulSoup(res.text, 'lxml')
    email_input = soup.select_one('input[name=memberEmail]')
    email = email_input.get('value')
    print(f'Email: {email}')