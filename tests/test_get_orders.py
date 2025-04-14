import requests
import pytest
import allure

from config import BASE_URL

@allure.feature("Получение списка заказов")
class TestGetOrders:
    @allure.title("Проверка получения списка заказов")
    def test_get_orders_list(self):
        with allure.step("Отправляем GET-запрос на получение списка заказов"):
            response = requests.get(f"{BASE_URL}/orders")
        with allure.step("Проверяем, что статус ответа равен 200"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        with allure.step("Проверяем, что в ответе присутствует ключ 'orders' и он является списком"):
            response_json = response.json()
            assert "orders" in response_json, "Ответ не содержит ключа 'orders'"
            assert isinstance(response_json["orders"], list), "Поле 'orders' должно быть списком"