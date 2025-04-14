import pytest
import requests
import allure

from config import BASE_URL

@allure.feature("Создание заказа")
class TestCreateOrder:
    @pytest.mark.parametrize("colors", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []  # вариант без указания цвета
    ])
    @allure.title("Создание заказа с цветом {colors}")
    def test_create_order_with_colors(self, colors):
        with allure.step("Формируем тело запроса для создания заказа"):
            payload = {
                "firstName": "Test",
                "lastName": "User",
                "address": "Some street 123",
                "metroStation": 4,
                "phone": "+7 901 123-45-67",
                "rentTime": 5,
                "deliveryDate": "2023-12-12",
                "comment": "Test order",
                "color": colors  # параметр цвета
            }
        with allure.step("Отправляем запрос на создание заказа"):
            response = requests.post(f"{BASE_URL}/orders", json=payload)
        with allure.step("Проверяем статус ответа и наличие поля 'track'"):
            # Ожидаемый код ответа может быть 200 или 201
            assert response.status_code in [200, 201], f"Неверный статус: {response.status_code}"
            response_json = response.json()
            assert "track" in response_json, "Ответ не содержит поле 'track'"