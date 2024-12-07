import pytest
import requests
import random
import string

BASE_URL = "https://stellarburgers.nomoreparties.site/api"
HEADERS = {'Content-Type': 'application/json'}

#Генерация уникального email:
def generate_unique_email():
    return f"test_{''.join(random.choices(string.ascii_lowercase, k=8))}@example.com"

#Фикстура для получения авторизационного токена:
@pytest.fixture
def auth_token():
    user_data = {
        "email": generate_unique_email(),
        "password": "testpass123",
        "name": "Test User"
    }

    # Попытка регистрации
    registration_response = requests.post(f"{BASE_URL}/auth/register", json=user_data, headers=HEADERS)
    print(f"Registration Response: {registration_response.status_code}, {registration_response.json()}")

    if registration_response.status_code == 403:
        print(f"User already exists. Proceeding to login.")

    # Логин
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data, headers=HEADERS)
    print(f"Login Response: {login_response.status_code}, {login_response.json()}")

    assert login_response.status_code == 200, f"Failed to get auth token, received status {login_response.status_code}"

    return login_response.json().get("accessToken")


#Фикстура для получения списка валидных ингредиентов:
@pytest.fixture
def ingredients():
    response = requests.get(f"{BASE_URL}/ingredients", headers=HEADERS)
    assert response.status_code == 200, "Failed to get ingredients"
    return [ingredient["_id"] for ingredient in response.json().get("data", [])]

#Фикстура для создания уникального пользователя перед тестом и удаления после теста:
@pytest.fixture
def create_test_user():
    user_data = {
        "email": generate_unique_email(),
        "password": "testpass123",
        "name": "Test User"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data, headers=HEADERS)
    assert response.status_code == 200, "Failed to create test user"
    access_token = response.json().get("accessToken")

    # Возвращаем данные пользователя и токен для использования в тестах
    yield user_data, access_token

    # Удаление тестового пользователя после выполнения теста
    requests.delete(f"{BASE_URL}/auth/user", headers={"Authorization": f"Bearer {access_token}"})
