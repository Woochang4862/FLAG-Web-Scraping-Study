import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from w4.env import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

from scraping.selenium_login import login_with_selenium
from scraping.selenium_utils import switch_to_new_window, get_requests_session_with_cookies, initialize_driver
from scraping.api_interaction import fetch_subjects_api
from utils.file_utils import save_json

# .env 파일 로드 (환경 변수 사용)
load_dotenv()

def go_to_info_page(driver):
    """로그인 후 정보 페이지로 이동합니다."""
    try:
        # 헤더의 정보 버튼이 클릭 가능할 때까지 대기
        info_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='header']/div/div/ul/li[1]"))
        )
        # 정보 버튼 클릭
        info_button.click()
        print("정보 버튼 클릭 성공.")
    except TimeoutException:
        # 지정된 시간 내에 버튼을 찾거나 클릭할 수 없는 경우
        print("정보 버튼을 찾거나 클릭하는 데 실패했습니다.")
        raise Exception("정보 버튼 클릭 실패") # 오류 발생시키고 종료

def main():
    driver = None # Selenium 웹 드라이버 변수 초기화
    session = None # requests 세션 변수 초기화
    try:
        # --- 드라이버 초기화 --- 
        driver = initialize_driver() # Initialize driver here
        
        # --- 1단계: Selenium으로 포털 로그인 --- 
        portal_id = os.getenv('PORTAL_ID') # .env 파일에서 아이디 읽기
        portal_password = os.getenv('PORTAL_PASSWORD') # .env 파일에서 비밀번호 읽기
        # 환경 변수 설정 확인
        if not portal_id or not portal_password:
            # Quit driver if env vars are missing
            if driver: driver.quit()
            raise ValueError("PORTAL_ID와 PORTAL_PASSWORD가 .env 파일에 설정되어야 합니다.")

        # 로그인 함수 호출 (driver 주입)
        login_with_selenium(driver, portal_id, portal_password)
        print("로그인 성공. 정보 페이지로 이동 중...")

        # --- 2단계: 정보 페이지로 이동 --- 
        go_to_info_page(driver)

        # --- 3단계: 새 창/탭으로 전환 --- 
        print("새 창/탭으로 전환 시도 중...")
        # 새 창이 완전히 열릴 시간을 확보하기 위해 잠시 대기 (필요에 따라 조절)
        time.sleep(3) 
        switch_to_new_window(driver)
        print(f"새 창으로 전환 완료. 현재 URL: {driver.current_url}")

        # --- 4단계: 새 창의 특정 요소 로딩 대기 --- 
        print("새 창의 콘텐츠 로딩 대기 중...")
        try:
            WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.TAG_NAME, "body"))
            )
            print("새 창의 필요한 요소 로딩 완료.")
        except TimeoutException:
             print("새 창에서 특정 요소 로딩 시간 초과. API 요청을 계속 시도합니다.")
             raise Exception("새 창에서 특정 요소 로딩 시간 초과")

        # --- 5단계: Selenium 쿠키를 사용하여 requests 세션 생성 --- 
        print("쿠키 추출 및 requests 세션 생성 중...")
        session = get_requests_session_with_cookies(driver)
        if not session or not session.cookies:
             print("경고: 쿠키가 추출되지 않았거나 세션 생성에 실패했습니다. API 요청이 실패할 수 있습니다.")
             raise Exception("쿠키 추출 실패")

        # --- 6단계: API 요청 정보 준비 --- 
        api_url = 'https://info.suwon.ac.kr/estbLectDtai/listVEstbLectDtai.do' # 대상 API URL
        api_data = { # API 요청 본문(payload)
            "subjtEstbSmrCd": "10", # 학기 코드 1학기 : 10, 여름학기 : 15, 2학기 : 20, 겨울학기 : 25
            "subjtEstbYear": "2025", # 학년도
            # "lCls": "2000574", # 단과대학 코드 2000574 : 지능형SW융합대학
            # "mCls": "2000596", # 학부 코드 2000595 : 데이터과학부 / 2000596 : 컴퓨터공학부 / 2000597 : 정보통신학부
            # "sCls": "2000644", # 학과 코드 2000644 : 컴퓨터SW / 미디어SW : 2000645
            # "trgtGrdeCd": "1", # 학년
            # "dayCd": "2", # 요일 코드 2 : 월요일 / 3 : 화요일 / 4 : 수요일 / 5 : 목요일 / 6 : 금요일 / 7 : 토요일
            # "ltrPrdCd": "1", # 교시 코드
            "subjtCd": "", # 과목 코드
            "reprPrfsEno": "", # 교수 이름 혹은 사번
        }
        api_headers = { # 특정 API에 필요한 추가/수정 헤더
            'Origin': 'https://info.suwon.ac.kr',
            'Referer': 'https://info.suwon.ac.kr/websquare/websquare.jsp?w2xPath=/views/usw/sa/su/SA_SU_4017.xml', # Referer 헤더가 중요
            'submissionid': 'sub1',
        }

        # --- 7단계: API 호출하여 데이터 가져오기 --- 
        print(f"API를 통해 강의 정보 요청 시작: {api_url}")
        subjects_data = fetch_subjects_api(session, api_url, api_data, custom_headers=api_headers)


        # --- 8단계: 결과 저장 --- 
        if subjects_data:
             # 가져온 데이터를 JSON 파일로 저장 (최상위 'output' 디렉토리에)
             output_path = os.path.join(project_root, 'output') 
             save_json(subjects_data, filename='subjects_list.json', output_dir=output_path) 
        else:
             print("API로부터 데이터를 받지 못해 파일을 저장하지 않습니다.")

    except Exception as e:
        # 스크립트 실행 중 발생하는 모든 예외 처리
        print(f"스크립트 실행 중 오류 발생: {e}")
        # 디버깅을 위해 상세한 오류 로그 출력 가능
        # import traceback
        # traceback.print_exc()
    finally:
        # --- 9단계: 리소스 정리 --- 
        # 오류 발생 여부와 관계없이 항상 브라우저 종료
        if driver:
            driver.quit()
            print("브라우저 종료")

if __name__ == "__main__":
    main()