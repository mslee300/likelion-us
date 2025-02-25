import json
from models import Company


def save_companies_from_json(json_file_path):
    """
    JSON 파일에서 회사 데이터를 읽어 데이터베이스에 저장하는 함수.

    Args:
        json_file_path (str): JSON 파일 경로 (예: 'companies.json')
    """
    try:
        # JSON 파일 읽기
        with open(json_file_path, 'r', encoding='utf-8') as file:
            companies_data = json.load(file)

        # 각 회사 데이터를 순회하며 저장
        for company_data in companies_data:
            ticker = company_data.get('symbol')
            name = company_data.get('name')
            category = company_data.get('category')
            description = company_data.get('description')
            founding_date = company_data.get('founding_date')

        print(Company)
    # except FileNotFoundError:
    #     print(f"File not found: {json_file_path}")
    # except json.JSONDecodeError:
    #     print(f"Invalid JSON format in file: {json_file_path}")
    except Exception as e:
        print(f"Unexpected error: {e}")


save_companies_from_json("likelion/companies.json")
