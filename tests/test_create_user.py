import requests
from conftest import BASE_URL, HEADERS, generate_unique_email

class TestCreateUser:
    #Создание пользователя:
    def test_create_unique_user(self):
        user_data = {
            "email": generate_unique_email(),
            "password": "testpass123",
            "name": "Test User"
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data, headers=HEADERS)
        assert response.status_code == 200
        assert "accessToken" in response.json()

    #Создание пользователя, который уже зарегистрирован:
    def test_create_existing_user(self, create_test_user):
        user_data, _ = create_test_user
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data, headers=HEADERS)
        assert response.status_code == 403
        assert response.json()["message"] == "User already exists"

    #Создание пользователя с пропуском обязательного поля:
    def test_create_user_missing_field(self):
        user_data = {
            "email": generate_unique_email(),
            "name": "Test User"
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data, headers=HEADERS)
        assert response.status_code == 403
        assert response.json()["message"] == "Email, password and name are required fields"
