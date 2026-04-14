"""
Тестовый скрипт для проверки API новостей
"""
import requests
import json

API_URL = "http://localhost:8000/api/v1/news"

print("🔍 Проверка API новостей...")
print(f"URL: {API_URL}\n")

try:
    response = requests.get(API_URL, timeout=5)

    if response.status_code == 200:
        news = response.json()
        print(f"✅ API работает! Получено новостей: {len(news)}\n")

        for item in news:
            print(f"{item['icon']} {item['title']}")
            print(f"   {item['description'][:80]}...")
            print()
    else:
        print(f"❌ Ошибка: HTTP {response.status_code}")
        print(response.text)

except requests.exceptions.ConnectionError:
    print("❌ Не удалось подключиться к API")
    print("\n💡 Убедитесь, что backend запущен:")
    print("   cd backend")
    print("   python run.py")

except Exception as e:
    print(f"❌ Ошибка: {e}")
