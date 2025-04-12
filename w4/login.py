# selenium_login.py 테스트를 위한 코드

import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from scraping.selenium_utils import initialize_driver
from scraping.selenium_login import login_with_selenium
import dotenv

dotenv.load_dotenv()

# 테스트 드라이버 생성
driver = initialize_driver()
try:
    login_with_selenium(driver, os.getenv('PORTAL_ID'), os.getenv('PORTAL_PASSWORD'))
finally:
    driver.quit()
