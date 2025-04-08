from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

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

def get_subjects_list(driver):
    subjects_list = []
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
    
    search_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@id='group59']"))
    )
    search_button.click()
    
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//tbody[@id='grid1_body_tbody']/tr"))
    )
    
    table = driver.find_element(By.XPATH, "//tbody[@id='grid1_body_tbody']")
    
    first_row = table.find_element(By.CSS_SELECTOR, "tr > td:nth-of-type(3)")
    if first_row:
        first_row.click()
    else:
        raise Exception("첫 번째 행을 찾을 수 없습니다.")
    
    while True:
        rows = table.find_elements(By.TAG_NAME, "tr")
        if not rows:
            break
        if subjects_list and rows[-1].text == subjects_list[-1]:
            break
        
        for row in rows:
            subjects_list.append(row.text)
            
        first_row.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)

    return driver, subjects_list

def main():
    driver = login_with_selenium(os.getenv('PORTAL_ID'), os.getenv('PORTAL_PASSWORD'))
    
    driver = go_to_info_page(driver)
    
    driver.switch_to.window(driver.window_handles[1])
    
    driver = go_to_subjects_list(driver)
    
    driver, subjects_list = get_subjects_list(driver)
    
    # subjects_list 를 txt 파일로 저장
    with open('../output/subjects_list.txt', 'w', encoding='utf-8') as f:
        for subject in subjects_list:
            f.write(subject + '\n')

if __name__ == "__main__":
    main()
