import requests
import pytest
from utils.courier_utils import register_new_courier_and_return_login_password

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

class TestCourierLogin:
    def test_login_success(self):
        """
        Тест проверяет успешную авторизацию курьера.
        1. Регистрируется новый курьер и получаются уникальные логин и пароль.
        2. Вызывается ручка логина.
        3. Проверяется, что статус ответа 200 и в теле содержится ключ 'id'.
        """
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data, "Не удалось зарегистрировать курьера"
        login, password, _ = courier_data

        payload = {
            "login": login,
            "password": password
        }
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        response_json = response.json()
        assert "id" in response_json, "Ответ не содержит идентификатора курьера (id)"

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field(self, missing_field):
        """
        Тест проверяет, что при отсутствии обязательного поля (login или password) происходит ошибка авторизации.
        """
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data, "Не удалось зарегистрировать курьера"
        login, password, _ = courier_data

        payload = {
            "login": login,
            "password": password
        }
        payload.pop(missing_field)
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        assert response.status_code != 200, f"Ожидалась ошибка при отсутствии поля {missing_field}"

    def test_login_incorrect_credentials(self):
        """
        Тест проверяет, что авторизация с неверными данными возвращает ошибку.
        """
        payload = {
            "login": "nonexistent",
            "password": "wrongpassword"
        }
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        assert response.status_code != 200, "Ожидалась ошибка при попытке авторизации с неверными данными" 