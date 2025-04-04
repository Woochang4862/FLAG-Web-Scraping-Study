import requests
import os

# 파일 URL
url = "https://www.naver.com/favicon.ico"

# GET 요청 보내기
response = requests.get(url)

#request User-Agent 헤더 확인
print(response.request.headers)
# 요청이 성공했는지 확인
if response.status_code == 200:
    # 파일로 저장
    if not os.path.exists("output"):
        os.makedirs("output")
    with open("output/naver.ico", "wb") as file:
        file.write(response.content)
    print("파일 다운로드 완료")
else:
    print(f"다운로드 실패: {response.status_code}")