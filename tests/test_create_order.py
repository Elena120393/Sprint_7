import pytest
import requests

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"


class TestCreateOrder:
    @pytest.mark.parametrize("colors", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []  # вариант без указания цвета
    ])
    def test_create_order_with_colors(self, colors):
        """
        Тест проверяет, что при создании заказа:
        - Возможен выбор одного цвета или двух.
        - Возможна отправка заказа без указания цвета.
        - В ответе присутствует поле 'track', содержащее информацию о заказе.
        """
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

        response = requests.post(f"{BASE_URL}/orders", json=payload)
        # Ожидаемый код ответа может быть 200 или 201
        assert response.status_code in [200, 201], f"Неверный статус: {response.status_code}"
        response_json = response.json()
        assert "track" in response_json, "Ответ не содержит поле 'track'"