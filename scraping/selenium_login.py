from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def login_with_selenium(driver: webdriver.Chrome, user_id: str, password: str):
    """
    제공된 Selenium WebDriver 인스턴스를 사용하여 수원대학교 포털에 로그인합니다.

    Args:
        driver (webdriver.Chrome): 초기화된 Selenium WebDriver 인스턴스.
        user_id (str): 로그인에 사용할 사용자 ID.
        password (str): 로그인에 사용할 비밀번호.

    Raises:
        Exception: 로그인 실패 시.
    """
    # 드라이버 초기화는 호출 측에서 수행합니다.
    try:
        # 로그인 페이지로 이동
        driver.get("http://portal.suwon.ac.kr/enview/index.html")
        print(f"로그인 페이지 로딩: {driver.title}")

        # mainFrame이 나타날 때까지 명시적으로 대기 후 해당 프레임으로 전환
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "mainFrame"))
        )
        driver.switch_to.frame("mainFrame")
        print("로그인 프레임으로 전환 완료.")

        # 아이디, 비밀번호 필드를 찾아 값 입력
        username_field = driver.find_element(By.NAME, "userId")
        password_field = driver.find_element(By.NAME, "pwd")
        # 자동 완성 문제 방지를 위해 필드 내용 먼저 클리어
        username_field.clear()
        password_field.clear()
        username_field.send_keys(user_id)
        password_field.send_keys(password)
        print("아이디 및 비밀번호 입력 완료.")

        # 로그인 버튼을 찾아 클릭
        login_button = driver.find_element(By.CLASS_NAME, "mainbtn_login")
        login_button.click()
        print("로그인 버튼 클릭 완료.")

        # 로그인 성공 후 나타나는 요소 대기 (로그인 및 페이지 로딩 확인용)
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//body"))
        )
        print("로그인 후 메인 페이지 로딩 확인됨.")

    except TimeoutException as e:
        print(f"로그인 과정 중 타임아웃 발생 또는 요소 찾기 실패: {e}")
        raise Exception("로그인 실패: 타임아웃 또는 요소 찾기 실패")
    except Exception as e:
        # 다른 잠재적 오류 처리
        print(f"로그인 중 예상치 못한 오류 발생: {e}")
        raise 