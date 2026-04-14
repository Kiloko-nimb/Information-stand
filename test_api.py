"""
Тестовый скрипт для проверки API
"""
import requests

BASE_URL = "http://localhost:8000"

def test_api():
    print("Тестирование API...")

    # Тест 1: Главная страница
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"\n[OK] GET / - {response.status_code}")
        print(f"  {response.json()}")
    except Exception as e:
        print(f"\n[ERROR] GET / - Ошибка: {e}")

    # Тест 2: Список сотрудников
    try:
        response = requests.get(f"{BASE_URL}/api/v1/staff/")
        print(f"\n[OK] GET /api/v1/staff/ - {response.status_code}")
        data = response.json()
        print(f"  Найдено сотрудников: {len(data)}")
        if data:
            print(f"  Первый: {data[0]['full_name']}")
    except Exception as e:
        print(f"\n[ERROR] GET /api/v1/staff/ - Ошибка: {e}")

    # Тест 3: Расписание группы
    try:
        response = requests.get(f"{BASE_URL}/api/v1/schedule/group/9ИС-1.25")
        print(f"\n[OK] GET /api/v1/schedule/group/9ИС-1.25 - {response.status_code}")
        data = response.json()
        print(f"  Найдено занятий: {len(data)}")
        if data:
            print(f"  Первое: {data[0]['subject']}")
    except Exception as e:
        print(f"\n[ERROR] GET /api/v1/schedule/group/... - Ошибка: {e}")

if __name__ == "__main__":
    test_api()
