# selenium_login.py 테스트를 위한 코드

import os
import sys
import time
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from scraping.selenium_utils import initialize_driver
from scraping.selenium_login import login_with_selenium
from scraping.selenium_utils import switch_to_new_window
from scraping.selenium_utils import get_requests_session_with_cookies
import dotenv

dotenv.load_dotenv()

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

driver = initialize_driver()
try:
    login_with_selenium(driver, os.getenv('PORTAL_ID'), os.getenv('PORTAL_PASSWORD'))
    print("로그인 성공")
    go_to_info_page(driver)
    print("정보 페이지 이동 성공")

    # windwo switch
    print(f"현재 창 : {driver.current_url}")
    switch_to_new_window(driver)
    print(f"새 창으로 전환 성공 : {driver.current_url}")
    
    requests_session = get_requests_session_with_cookies(driver)
    # 쿠키 예쁘게 출력
    print("========== 쿠키 출력 ==========")
    for cookie in requests_session.cookies:
        print(f"{cookie.name} : {cookie.value}")
finally:
    driver.quit()
