import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
import requests # For mocking Session in cookie test
import time # Import time for patching
from scraping.selenium_utils import initialize_driver, switch_to_new_window, get_requests_session_with_cookies

# mocker fixture 사용
def test_initialize_driver_success(mocker):
    """WebDriver 초기화 성공 테스트"""
    # webdriver.Chrome과 chromedriver_autoinstaller.install 모킹
    mock_chrome = mocker.patch('selenium.webdriver.Chrome', return_value=mocker.Mock(spec=webdriver.Chrome))
    mock_install = mocker.patch('chromedriver_autoinstaller.install')
    
    driver = initialize_driver()
    
    mock_install.assert_called_once()
    mock_chrome.assert_called_once()
    # We check if it's an instance of the mock object returned by patch
    assert isinstance(driver, type(mock_chrome.return_value)) 

def test_initialize_driver_failure(mocker):
    """WebDriver 초기화 중 예외 발생 시 전파되는지 테스트"""
    mock_install = mocker.patch('chromedriver_autoinstaller.install')
    # webdriver.Chrome 호출 시 에러 발생시키기
    mock_chrome = mocker.patch('selenium.webdriver.Chrome', side_effect=Exception("Driver init failed"))

    with pytest.raises(Exception, match="Driver init failed"):
        initialize_driver()
    
    mock_install.assert_called_once()
    mock_chrome.assert_called_once()


def test_switch_to_new_window_success(mocker):
    """새 창으로 성공적으로 전환되는지 테스트"""
    mock_driver = mocker.Mock(spec=webdriver.Chrome)
    mock_driver.current_window_handle = 'window1'
    mock_driver.window_handles = ['window1', 'window2']
    
    # time.sleep 모킹
    mocker.patch('time.sleep') 
    
    switch_to_new_window(mock_driver)
    
    # switch_to.window가 'window2' 핸들로 호출되었는지 확인
    mock_driver.switch_to.window.assert_called_once_with('window2')

def test_switch_to_new_window_no_other_window(mocker):
    """다른 창이 없을 때 전환 시도하지 않는지 테스트"""
    mock_driver = mocker.Mock(spec=webdriver.Chrome)
    mock_driver.current_window_handle = 'window1'
    mock_driver.window_handles = ['window1']
    
    mocker.patch('time.sleep')
    
    switch_to_new_window(mock_driver)
    
    # switch_to.window가 호출되지 않았는지 확인
    mock_driver.switch_to.window.assert_not_called()


def test_get_requests_session_with_cookies(mocker):
    """Selenium 쿠키가 requests 세션으로 잘 변환되는지 테스트"""
    mock_driver = mocker.Mock(spec=webdriver.Chrome)
    mock_cookies = [
        {'name': 'sessionid', 'value': '12345', 'domain': '.example.com', 'path': '/', 'secure': True},
        {'name': 'csrftoken', 'value': 'abcde', 'domain': '.example.com', 'path': '/', 'expiry': 1678886400} # expiry 키 테스트
    ]
    mock_driver.get_cookies.return_value = mock_cookies
    
    # requests.Session 및 cookies.set 모킹
    mock_session_cls = mocker.patch('requests.Session')
    mock_session_instance = mock_session_cls.return_value
    
    session = get_requests_session_with_cookies(mock_driver)
    
    mock_driver.get_cookies.assert_called_once()
    mock_session_cls.assert_called_once() # Session 객체 생성 확인
    
    # cookies.set 호출 확인
    assert mock_session_instance.cookies.set.call_count == 2
    # 첫 번째 쿠키 호출 인수 확인
    mock_session_instance.cookies.set.assert_any_call(name='sessionid', value='12345', domain='.example.com', path='/', secure=True)
    # 두 번째 쿠키 호출 인수 확인 (expiry -> expires 변환 확인, secure=False 추가)
    mock_session_instance.cookies.set.assert_any_call(name='csrftoken', value='abcde', domain='.example.com', path='/', expires=1678886400, secure=False)
    
    assert session == mock_session_instance # 모킹된 세션 객체가 반환되었는지 확인 