import requests
from conftest import BASE_URL, HEADERS

class TestCreateOrder:
    #Создание заказа с авторизацией
    def test_create_order_with_auth(self, auth_token, ingredients):
        headers = {**HEADERS, "Authorization": auth_token}
        order_data = {"ingredients": ingredients}
        response = requests.post(f"{BASE_URL}/orders", json=order_data, headers=headers)
        assert response.status_code == 200
        assert "order" in response.json()

    #Создание заказа без авторизации
    def test_create_order_without_auth(self, ingredients):
        order_data = {"ingredients": ingredients}
        response = requests.post(f"{BASE_URL}/orders", json=order_data, headers=HEADERS)
        assert response.status_code == 200

    #Создание заказа с неверным хешем ингредиентов
    def test_create_order_with_invalid_ingredients(self, auth_token):
        headers = {**HEADERS, "Authorization": auth_token}
        order_data = {"ingredients": ["invalid_hash"]}
        response = requests.post(f"{BASE_URL}/orders", json=order_data, headers=headers)
        assert response.status_code == 400
        assert "message" in response.json()

    #Создание заказа с пустым списком ингредиентов
    def test_create_order_with_empty_ingredients(self, auth_token):
        headers = {**HEADERS, "Authorization": auth_token}
        order_data = {"ingredients": []}
        response = requests.post(f"{BASE_URL}/orders", json=order_data, headers=headers)
        assert response.status_code == 400
        assert "message" in response.json()
