import requests
from conftest import BASE_URL, HEADERS

class TestUserLogin:
    #Логин под существующим пользователем
    def test_login_existing_user(self, create_test_user):
        user_data, _ = create_test_user
        response = requests.post(f"{BASE_URL}/auth/login", json=user_data, headers=HEADERS)
        assert response.status_code == 200
        assert "accessToken" in response.json()

    #Логин с неверным логином и паролем
    def test_login_invalid_credentials(self):
        user_data = {
            "email": "invalid_user@example.com",
            "password": "wrongpassword"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=user_data, headers=HEADERS)
        assert response.status_code == 401
        assert "message" in response.json()
