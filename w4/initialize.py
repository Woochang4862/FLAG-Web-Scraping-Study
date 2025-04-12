# chrome driver 테스트를 위한 코드
import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from scraping.selenium_utils import initialize_driver

# 테스트 드라이버 생성
driver = initialize_driver()
driver.quit()
