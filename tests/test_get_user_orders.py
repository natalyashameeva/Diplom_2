import requests
from conftest import BASE_URL, HEADERS

class TestGetUserOrders:
    #Получение заказов авторизованного пользователя
    def test_get_orders_authorized_user(self, auth_token):
        headers = {**HEADERS, "Authorization": auth_token}
        response = requests.get(f"{BASE_URL}/orders", headers=headers)
        assert response.status_code == 200
        assert "orders" in response.json()

    #Получение заказов неавторизованного пользователя
    def test_get_orders_unauthorized_user(self):
        response = requests.get(f"{BASE_URL}/orders", headers=HEADERS)
        assert response.status_code == 401
        assert response.json()["message"] == "You should be authorised"
