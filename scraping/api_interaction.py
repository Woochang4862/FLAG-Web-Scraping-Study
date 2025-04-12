import requests
import json

DEFAULT_HEADERS = { # 기본 헤더 설정
    'Accept': 'application/json',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json; charset="UTF-8"',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
}

def fetch_subjects_api(session, url, data, custom_headers=None):
    """지정된 API 엔드포인트에서 강의 데이터를 가져옵니다.

    Args:
        session (requests.Session): 필요한 쿠키가 포함된 requests 세션.
        url (str): API 엔드포인트 URL.
        data (dict): 요청 페이로드 데이터.
        custom_headers (dict, optional): 기본 헤더와 병합/덮어쓰기할 사용자 정의 헤더.

    Returns:
        dict or None: JSON 응답 데이터를 딕셔너리로 반환하거나, 실패 시 None.
    """
    headers = DEFAULT_HEADERS.copy() # 기본 헤더 복사
    if custom_headers:
        headers.update(custom_headers) # 사용자 정의 헤더 병합/덮어쓰기

    response = None # 응답 변수 초기화
    try:
        print(f"API 요청 시작: {url}")
        response = session.post(url, headers=headers, json=data)
        response.raise_for_status() # 오류 상태 코드(4xx 또는 5xx) 시 예외 발생
        subjects_data = response.json()
        print("API 요청 성공")
        return subjects_data
    except requests.exceptions.RequestException as e:
        print(f"API 요청 실패 (RequestException): {e}")
        if response is not None:
            print(f"응답 상태 코드: {response.status_code}")
        return None
    except json.JSONDecodeError:
        print("JSON 파싱 실패")
        if response is not None:
            print(f"응답 상태 코드: {response.status_code}")
            print(f"응답 내용: {response.text[:500]}...") # 디버깅 위해 처음 500자 출력
        return None
    except Exception as e:
        print(f"API 호출 중 예상치 못한 오류 발생: {e}")
        return None 