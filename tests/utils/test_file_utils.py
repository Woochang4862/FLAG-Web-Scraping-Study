import json
import os
import pytest
from utils.file_utils import save_json

# pytest의 tmp_path fixture를 사용하여 임시 디렉토리에서 테스트
def test_save_json_success(tmp_path):
    """save_json이 유효한 데이터로 파일을 성공적으로 생성하는지 테스트"""
    test_data = {"key": "value", "list": [1, 2, 3]}
    output_dir = tmp_path / "output"
    filename = "test_output.json"
    
    save_json(test_data, output_dir=str(output_dir), filename=filename)
    
    expected_file_path = output_dir / filename
    assert expected_file_path.exists() # 파일 생성 확인
    
    # 파일 내용 확인
    with open(expected_file_path, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)
    assert saved_data == test_data

def test_save_json_no_data(tmp_path, capsys):
    """save_json이 None 데이터로 호출될 때 파일을 생성하지 않는지 테스트"""
    output_dir = tmp_path / "output"
    filename = "test_output.json"
    
    save_json(None, output_dir=str(output_dir), filename=filename)
    
    expected_file_path = output_dir / filename
    assert not expected_file_path.exists() # 파일 생성되지 않음 확인
    
    # 콘솔 출력 확인 (선택 사항)
    captured = capsys.readouterr()
    assert "저장할 데이터가 없습니다." in captured.out

def test_save_json_os_error(tmp_path, mocker, capsys): # Added capsys fixture
    """파일 생성 중 OS 에러 발생 시 예외 처리 및 메시지 출력 테스트"""
    test_data = {"key": "value"}
    output_dir = tmp_path / "output"
    filename = "test_output.json"

    # os.makedirs를 모킹하여 에러 발생시키기
    mocker.patch("os.makedirs", side_effect=OSError("Test OS Error"))
    
    save_json(test_data, output_dir=str(output_dir), filename=filename)
    
    # 파일이 생성되지 않았는지 확인 (선택 사항, 에러 발생 시 생성 안 될 것)
    expected_file_path = output_dir / filename
    assert not expected_file_path.exists()
    
    # 에러 메시지 출력 확인
    captured = capsys.readouterr()
    assert "JSON 파일 저장 중 오류 발생" in captured.out 