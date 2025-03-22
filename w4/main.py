import requests
from bs4 import BeautifulSoup
import certifi
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time  # 파일 상단에 추가

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

def access_info_page(session):
    info_url = "http://info.suwon.ac.kr/websquare/websquare.jsp?w2xPath=/views/main.xml"
    
    try:
        # info 페이지 접속
        response = session.get(info_url)
        response.raise_for_status()
        
        # HTML 파일로 저장
        with open('info_page.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        print("info 페이지 접속 성공!")
        print("페이지가 info_page.html 파일로 저장되었습니다.")
        
        # BeautifulSoup으로 페이지 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        print("\n페이지 타이틀:", soup.title.string if soup.title else "타이틀 없음")
        
    except requests.exceptions.RequestException as e:
        print(f"info 페이지 접속 중 오류 발생: {e}")

def login_with_selenium(user_id, password):
    driver = webdriver.Chrome()  # 또는 다른 브라우저 드라이버
    driver.get("http://portal.suwon.ac.kr/enview/index.html")
    
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
    
    
    return driver

def go_to_info_page(driver):
    info_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='header']/div/div/ul/li[1]"))
    )
    info_button.click()
    
    return driver

def go_to_subjects_list(driver):    
    major_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[@id='treeMenu_label_3']"))
    )
    major_button.click()
    
    subjects_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[@id='treeMenu_label_6']"))
    )
    subjects_button.click()
    
    return driver

def set_filter(driver):
    iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="windowContainer1_subWindow1_iframe"]'))
    )
    
    zoom_out_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@id='anchor5']"))
    )
    for _ in range(5):
        zoom_out_button.click()
        time.sleep(1)
    
    driver.switch_to.frame(iframe)
    
    college_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@id='schLcls_label']"))
    )
    college_button.click()
    
    ict_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//td[@id='schLcls_itemTable_16']"))
    )
    ict_button.click()
    
    
    major_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@id='schMcls_label']"))
    )
    major_button.click()
    
    ds_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//td[@id='schMcls_itemTable_1']"))
    )
    ds_button.click()
    
    search_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@id='group59']"))
    )
    search_button.click()
    
    time.sleep(10)
    
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//tbody[@id='grid1_body_tbody']"))
    )
    
    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        # check 속성 체크
        print(cells[15].is_selected())
        # 뒤 부터 삭제해서 아래 인덱스 번호가 변경되지 않도록 함
        del cells[15]
        del cells[13]
        del cells[:2]
        print(','.join(map(lambda cell : cell.text, cells)))
    
    return driver

def main():
    # 포털 로그인
    # session = get_portal_session()
    # if session:
    #     print("세션이 성공적으로 생성되었습니다.")
    #     # info 페이지 접속
    #     # access_info_page(session)
    #     # 세션 정보 출력
    #     print(session.cookies)
    #     print(session.headers)
    
    driver = login_with_selenium(os.getenv('PORTAL_ID'), os.getenv('PORTAL_PASSWORD'))
    
    driver = go_to_info_page(driver)
    
    driver.switch_to.window(driver.window_handles[1])
    
    driver = go_to_subjects_list(driver)
    
    driver = set_filter(driver)

if __name__ == "__main__":
    main()
