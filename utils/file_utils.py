import json
import os

def save_json(json_data, output_dir='output', filename='output.json'):
    """파이썬 딕셔너리 또는 리스트 데이터를 JSON 파일로 저장합니다.

    Args:
        json_data: 저장할 딕셔너리 또는 리스트.
        output_dir (str): 파일을 저장할 디렉토리.
        filename (str): 출력 JSON 파일의 이름.
    """
    if json_data:
        try:
            os.makedirs(output_dir, exist_ok=True) # 출력 디렉토리가 없으면 생성
            output_file = os.path.join(output_dir, filename)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)
            print(f"데이터를 {output_file} 에 저장했습니다.")
        except Exception as e:
            print(f"JSON 파일 저장 중 오류 발생: {e}")
    else:
        print("저장할 데이터가 없습니다.") 