from bs4 import BeautifulSoup

html = """
<html>
    <head>
        <title>웹 스크래핑 스터디</title>
    </head>
    <body>
        <h1>웹 스크래핑 스터디</h1>
        <p>웹 스크래핑 스터디는 웹 페이지에서 데이터를 추출하는 기술을 배우는 스터디입니다.</p>
        <!-- 중첩 태그 -->
        <ul>
            <li>웹 스크래핑 기초</li>
            <li>웹 스크래핑 실전</li>
            <li>웹 스크래핑 활용</li>
        </ul>
    </body>
</html>
"""
soup = BeautifulSoup(html, 'lxml')
print(soup.title.string)
print(soup.find('h1').string)
print(soup.find('p').string)
print(soup.find('ul').find_all('li'))