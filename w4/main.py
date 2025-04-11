import requests
import json
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import TimeoutException

# .env 파일 로드
load_dotenv()

def login_with_selenium(user_id, password):
    driver = webdriver.Chrome()  # 또는 다른 브라우저 드라이버
    driver.get("http://portal.suwon.ac.kr/enview/index.html")

    # 명시적으로 mainFrame이 로드될 때까지 기다립니다.
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "mainFrame"))
    )

    driver.switch_to.frame("mainFrame")

    # 로그인 폼 입력
    username_field = driver.find_element(By.NAME, "userId")
    password_field = driver.find_element(By.NAME, "pwd")

    username_field.send_keys(user_id)
    password_field.send_keys(password)

    # 로그인 버튼 클릭
    login_button = driver.find_element(By.CLASS_NAME, "mainbtn_login")
    login_button.click()

    # 로그인 후 페이지 로딩 및 세션 설정 대기
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='header']"))
        )
        print("로그인 후 메인 페이지 로딩 확인됨")
    except TimeoutException:
        print("로그인 후 메인 페이지 로딩 시간 초과 또는 요소 찾기 실패")
        # 필요하다면 여기서 에러 처리 또는 드라이버 종료
        driver.quit()
        raise Exception("로그인 실패") # 로그인 실패 처리

    return driver

def go_to_info_page(driver):
    try:
        info_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='header']/div/div/ul/li[1]"))
        )
        info_button.click()
        print("정보 버튼 클릭 성공.")
        return driver
    except TimeoutException:
        print("정보 버튼을 찾거나 클릭하는 데 실패했습니다.")
        raise Exception("정보 버튼 클릭 실패") # 더 이상 진행 불가
  
def switch_to_new_window(driver):
    original_window = driver.current_window_handle
    for handle in driver.window_handles:
        if handle != original_window:
            driver.switch_to.window(handle)
            return driver
    
def fetch_subjects_with_requests(driver):
    """Selenium 드라이버에서 쿠키를 가져와 requests를 사용해 강의 목록 API를 호출합니다."""
    selenium_cookies = driver.get_cookies()
    requests_session = requests.Session()

    # Selenium 쿠키를 requests 세션에 추가
    for cookie in selenium_cookies:
        # 'expiry' 키가 있으면 정수로 변환 (requests는 float을 지원하지 않음)
        if 'expiry' in cookie:
            cookie['expires'] = int(cookie['expiry'])
            del cookie['expiry']
        # 'httpOnly', 'secure'는 boolean이어야 함
        if 'httpOnly' in cookie:
             cookie['httpOnly'] = bool(cookie['httpOnly'])
        if 'secure' in cookie:
             cookie['secure'] = bool(cookie['secure'])
        # requests가 인식하지 못하는 키 ('httpOnly' 제외) 제거
        cookie_args = {k: v for k, v in cookie.items() if k in ['name', 'value', 'domain', 'path', 'expires', 'secure']}
        requests_session.cookies.set(**cookie_args)


    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset="UTF-8"',
        'Origin': 'https://info.suwon.ac.kr',
        'Referer': 'https://info.suwon.ac.kr/websquare/websquare.jsp?w2xPath=/views/usw/sa/su/SA_SU_4017.xml&w2xHome=/views/&w2xDocumentRoot=',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'submissionid': 'sub1',
    }
    data = {
        "subjtEstbSmrCd": "10", # 학기 코드 1학기 : 10, 여름학기 : 15, 2학기 : 20, 겨울학기 : 25
        "subjtEstbYear": "2025", # 학년도
        #"lCls": "2000574", # 단과대학 코드 2000574 : 지능형SW융합대학
        #"mCls": "2000595", # 학부 코드 2000595 : 데이터과학부
        #"sCls": "", # 학과 코드 컴퓨터SW : 2000644 / 
        #"trgtGrdeCd": "1", # 학년
        #"dayCd": "2", # 요일 코드 2 : 월요일 / 3 : 화요일 / 4 : 수요일 / 5 : 목요일 / 6 : 금요일 / 7 : 토요일
        #"ltrPrdCd": "1", # 교시 코드
        "subjtCd": "", # 과목 코드
        "reprPrfsEno": "", # 교수 이름 혹은 사번
    }
    url = 'https://info.suwon.ac.kr/estbLectDtai/listVEstbLectDtai.do'

    try:
        response = requests_session.post(url, headers=headers, json=data)
        response.raise_for_status() # 오류 발생 시 예외 발생
        subjects_data = response.json()
        print("API 요청 성공")
        return subjects_data
    except requests.exceptions.RequestException as e:
        print(f"API 요청 실패: {e}")
        # API 응답 내용을 함께 출력하여 디버깅에 도움
        if response is not None:
            print(f"Response status code: {response.status_code}")
            print(f"Response text: {response.text}")
        return None
    except json.JSONDecodeError:
        print("JSON 파싱 실패")
        print(f"Response text: {response.text}")
        return None

def save_json(json_data):
    if json_data:
        # subjects_data 를 JSON 파일로 저장
        output_dir = '../output'
        os.makedirs(output_dir, exist_ok=True) # Ensure output directory exists
        output_file = os.path.join(output_dir, 'subjects_list.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        print(f"데이터를 {output_file} 에 저장했습니다.")
    else:
        print("데이터를 가져오지 못했습니다.")


def main():
    driver = None # driver 변수 초기화
    try:
        driver = login_with_selenium(os.getenv('PORTAL_ID'), os.getenv('PORTAL_PASSWORD'))

        print("로그인 성공. 정보 페이지로 이동 중...")

        driver = go_to_info_page(driver)

        # 새 창 또는 탭이 열릴 때까지 잠시 대기
        time.sleep(3) # 로딩 시간에 따라 조절 필요
        
        # 새 창으로 전환
        driver = switch_to_new_window(driver)
        print(f"새 창으로 전환 성공. 현재 URL: {driver.current_url}")
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@id='treeMenu_label_3']"))
        )
        print("새 창 로딩 완료. 쿠키 추출 및 API 요청 시작...")

        subjects_data = fetch_subjects_with_requests(driver)

        save_json(subjects_data)

    finally:
        if driver:
            driver.quit()
            print("브라우저 종료")

if __name__ == "__main__":
    main() 