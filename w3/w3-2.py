from urllib.request import urlretrieve

# 파일 URL
url = "https://www.naver.com/favicon.ico"

# GET 요청 보내기
path, response = urlretrieve(url, "../output/naver.ico")

# 파일 저장 경로
print("파일 저장 경로 : ", path)