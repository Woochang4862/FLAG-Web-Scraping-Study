from selenium import webdriver
import requests
import time
import chromedriver_autoinstaller # 크롬드라이버 자동 설치 도구 임포트

def initialize_driver():
    """Selenium Chrome WebDriver 인스턴스를 초기화하고 반환합니다.
    올바른 chromedriver가 설치되도록 합니다.
    """
    try:
        # 현재 Chrome 버전에 맞는 chromedriver 확인 및 설치 시도
        print("ChromeDriver 확인 및 설치 시도...")
        chromedriver_autoinstaller.install()
        print("ChromeDriver 준비 완료.")
        # Chrome 드라이버 초기화
        driver = webdriver.Chrome()
        print("WebDriver 인스턴스 생성 완료.")
        return driver
    except Exception as e:
        print(f"WebDriver 초기화 중 오류 발생: {e}")
        raise

def switch_to_new_window(driver):
    """Selenium 드라이버의 제어 컨텍스트를 가장 최근의 창/탭으로 전환합니다.

    Args:
        driver: Selenium WebDriver 인스턴스.
    """
    original_window = driver.current_window_handle # 현재 창 핸들 저장
    time.sleep(1) # 간단한 대기, 필요에 따라 조절
    
    all_windows = driver.window_handles # 모든 창 핸들 가져오기
    new_window_handle = None
    if len(all_windows) > 1:
        # 원래 창이 아닌 다른 핸들 찾기 (보통 가장 마지막 핸들이 새 창)
        for handle in all_windows:
            if handle != original_window:
                new_window_handle = handle
                break # 찾으면 반복 중단
        
        if new_window_handle:
            driver.switch_to.window(new_window_handle) # 새 창으로 전환
            print(f"창 핸들 전환 완료: {new_window_handle}")
        else:
             print("전환할 새 창 핸들을 찾지 못했습니다.")
    else:
        print("전환할 다른 창이 없습니다.")

def get_requests_session_with_cookies(driver):
    """Selenium 드라이버에서 쿠키를 추출하고 이를 포함한 requests.Session을 반환합니다.

    Args:
        driver: Selenium WebDriver 인스턴스.

    Returns:
        requests.Session: 쿠키가 설정된 requests 세션 객체.
    """
    selenium_cookies = driver.get_cookies() # 드라이버에서 쿠키 가져오기
    requests_session = requests.Session() # requests 세션 생성

    print(f"Selenium에서 {len(selenium_cookies)}개의 쿠키 추출됨. requests 세션으로 변환 중...")
    # Selenium 쿠키를 requests 세션에 추가
    for cookie in selenium_cookies:
        # 'expiry' 키 처리 (requests는 'expires' 사용)
        if 'expiry' in cookie:
            # 값이 None이 아닐 경우 정수로 변환
            expiry_val = cookie.get('expiry')
            cookie['expires'] = int(expiry_val) if expiry_val is not None else None
            del cookie['expiry']
        
        # requests가 인식하는 키만 필터링 (cookie.get 사용으로 안전하게 접근)
        cookie_args = {
            'name': cookie.get('name'),
            'value': cookie.get('value'),
            'domain': cookie.get('domain'),
            'path': cookie.get('path'),
            'expires': cookie.get('expires'),
            'secure': cookie.get('secure', False), # 없으면 False로 기본값 설정
        }
        cookie_args = {k: v for k, v in cookie_args.items() if v is not None}
        
        # name과 value가 모두 존재할 경우에만 쿠키 추가
        if cookie_args.get('name') is not None and cookie_args.get('value') is not None:
             try:
                 requests_session.cookies.set(**cookie_args)
             except Exception as e:
                 print(f"쿠키 설정 중 오류 발생 ({cookie.get('name')}): {e}")
                 print(f"오류 발생 쿠키 정보: {cookie_args}")
        else:
            print(f"이름 또는 값이 없어 쿠키를 건너뜀: {cookie}")
            
    print(f"requests 세션에 {len(requests_session.cookies)}개의 쿠키 설정 완료.")
    return requests_session 