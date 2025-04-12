import pytest
import requests
import json
from scraping.api_interaction import fetch_subjects_api, DEFAULT_HEADERS

# mocker fixture는 pytest-mock 설치 시 사용 가능
def test_fetch_subjects_api_success(mocker):
    """API 호출 성공 시 JSON 데이터를 반환하는지 테스트"""
    mock_session = mocker.Mock(spec=requests.Session)
    mock_response = mocker.Mock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": ["subject1", "subject2"]}
    # raise_for_status는 에러 없을 때 아무것도 안 함
    mock_response.raise_for_status.return_value = None 
    
    mock_session.post.return_value = mock_response
    
    test_url = "http://fake-api.com/subjects"
    test_data = {"year": "2025"}
    test_headers = {"X-Custom": "Test"}
    
    result = fetch_subjects_api(mock_session, test_url, test_data, custom_headers=test_headers)
    
    # API 호출 확인
    expected_merged_headers = DEFAULT_HEADERS.copy()
    expected_merged_headers.update(test_headers)
    mock_session.post.assert_called_once_with(test_url, headers=expected_merged_headers, json=test_data)
    mock_response.raise_for_status.assert_called_once()
    mock_response.json.assert_called_once()
    
    # 결과 확인
    assert result == {"data": ["subject1", "subject2"]}

def test_fetch_subjects_api_request_exception(mocker):
    """requests.exceptions.RequestException 발생 시 None 반환 테스트"""
    mock_session = mocker.Mock(spec=requests.Session)
    mock_session.post.side_effect = requests.exceptions.RequestException("Connection error")
    
    test_url = "http://fake-api.com/subjects"
    test_data = {"year": "2025"}
    
    result = fetch_subjects_api(mock_session, test_url, test_data)
    
    assert result is None

def test_fetch_subjects_api_http_error(mocker):
    """HTTP 에러(4xx, 5xx) 발생 시 None 반환 테스트"""
    mock_session = mocker.Mock(spec=requests.Session)
    mock_response = mocker.Mock(spec=requests.Response)
    mock_response.status_code = 404
    # raise_for_status가 HTTPError를 발생시키도록 설정
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Not Found")
    
    mock_session.post.return_value = mock_response
    
    test_url = "http://fake-api.com/subjects"
    test_data = {"year": "2025"}
    
    result = fetch_subjects_api(mock_session, test_url, test_data)
    
    mock_session.post.assert_called_once()
    mock_response.raise_for_status.assert_called_once()
    assert result is None

def test_fetch_subjects_api_json_decode_error(mocker):
    """JSON 디코딩 에러 발생 시 None 반환 테스트"""
    mock_session = mocker.Mock(spec=requests.Session)
    mock_response = mocker.Mock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)
    mock_response.text = "Invalid JSON response" # 에러 시 출력될 텍스트 설정
    
    mock_session.post.return_value = mock_response
    
    test_url = "http://fake-api.com/subjects"
    test_data = {"year": "2025"}
    
    result = fetch_subjects_api(mock_session, test_url, test_data)
    
    mock_session.post.assert_called_once()
    mock_response.raise_for_status.assert_called_once()
    mock_response.json.assert_called_once()
    assert result is None 