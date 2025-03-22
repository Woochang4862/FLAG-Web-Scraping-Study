import requests
from bs4 import BeautifulSoup
import certifi
from dotenv import load_dotenv
import os
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context

# .env 파일 로드
load_dotenv()

def get_portal_session():
    # 환경변수에서 로그인 정보 가져오기
    user_id = os.getenv('PORTAL_ID')
    password = os.getenv('PORTAL_PASSWORD')
    
    if not user_id or not password:
        print("Error: .env 파일에 로그인 정보가 없습니다.")
        return None
    
    # 실제 로그인 URL
    login_url = "http://portal.suwon.ac.kr/enpass/login"
    
    try:
        # 세션 생성
        session = requests.Session()
        
        # ID 대문자 변환 (admin 계정 제외)
        if user_id.lower() != "admin":
            user_id = user_id.upper()
            
        # 로그인 데이터 준비
        login_data = {
            'username': user_id.strip(),
            'userId': user_id.strip(),
            'password': password.strip(),
            'pwd': password.strip(),
            '_epLogin_': 'enview',
            'service': 'https://portal.suwon.ac.kr/enview/user/enpassLoginProcess.face'
        }
        
        # 로그인 요청
        response = session.post(
            login_url,
            data=login_data,
            verify=certifi.where(),
            params={
                '_epLogin_': 'enview',
                'service': 'https://portal.suwon.ac.kr/enview/user/enpassLoginProcess.face'
            }
        )
        response.raise_for_status()
        
        # 로그인 성공 여부 확인
        if "로그인 실패" in response.text or "학번/사번을 입력하시기 바랍니다" in response.text:
            print("로그인 실패: 아이디나 비밀번호를 확인해주세요.")
            return None
            
        print("로그인 성공!")
        return session
        
    except requests.exceptions.RequestException as e:
        print(f"오류 발생: {e}")
        return None

def main():
    session = get_portal_session()
    if session:
        print("세션이 성공적으로 생성되었습니다.")
        return session

if __name__ == "__main__":
    main()