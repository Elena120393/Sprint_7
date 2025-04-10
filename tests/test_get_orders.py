import requests
import pytest

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"


class TestGetOrders:
    def test_get_orders_list(self):
        """
        Тест проверяет, что при выполнении GET-запроса на получение списка заказов:
        - Статус ответа равен 200.
        - В теле ответа присутствует поле 'orders', являющееся списком.
        """
        response = requests.get(f"{BASE_URL}/orders")
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        response_json = response.json()
        assert "orders" in response_json, "Ответ не содержит ключа 'orders'"
        assert isinstance(response_json["orders"], list), "Поле 'orders' должно быть списком"