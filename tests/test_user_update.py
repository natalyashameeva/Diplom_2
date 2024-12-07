import requests
from conftest import BASE_URL, HEADERS

class TestUserUpdate:
    #Изменение данных авторизованного пользователя
    def test_update_user_with_auth(self, create_test_user):
        _, auth_token = create_test_user
        headers = {**HEADERS, "Authorization": auth_token}
        update_data = {"name": "New Name"}
        response = requests.patch(f"{BASE_URL}/auth/user", json=update_data, headers=headers)
        assert response.status_code == 200
        assert response.json()["user"]["name"] == "New Name"

    #Изменение данных без авторизации
    def test_update_user_without_auth(self):
        update_data = {"name": "New Name"}
        response = requests.patch(f"{BASE_URL}/auth/user", json=update_data, headers=HEADERS)
        assert response.status_code == 401
        assert response.json()["message"] == "You should be authorised"
