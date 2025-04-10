import requests
import pytest
import allure
from utils.courier_utils import register_new_courier_and_return_login_password

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

@allure.feature("Авторизация курьера")
class TestCourierLogin:
    @allure.title("Успешная авторизация курьера")
    def test_login_success(self):
        with allure.step("Регистрируем нового курьера и получаем логин и пароль"):
            courier_data = register_new_courier_and_return_login_password()
            assert courier_data, "Не удалось зарегистрировать курьера"
            login, password, _ = courier_data
        with allure.step("Формируем данные для запроса авторизации"):
            payload = {
                "login": login,
                "password": password
            }
        with allure.step("Отправляем запрос на авторизацию"):
            response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        with allure.step("Проверяем, что авторизация прошла успешно"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
            response_json = response.json()
            assert "id" in response_json, "Ответ не содержит идентификатора курьера (id)"

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    @allure.title("Ошибка авторизации при отсутствии обязательного поля")
    def test_login_missing_field(self, missing_field):
        with allure.step("Регистрируем нового курьера и получаем уникальные данные"):
            courier_data = register_new_courier_and_return_login_password()
            assert courier_data, "Не удалось зарегистрировать курьера"
            login, password, _ = courier_data
        with allure.step("Формируем данные для запроса авторизации"):
            payload = {
                "login": login,
                "password": password
            }
        with allure.step(f"Удаляем обязательное поле: {missing_field}"):
            payload.pop(missing_field)
        with allure.step("Отправляем запрос на авторизацию без обязательного поля"):
            response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        with allure.step("Проверяем, что авторизация не проходит"):
            assert response.status_code != 200, f"Ожидалась ошибка при отсутствии поля {missing_field}"

    @allure.title("Ошибка авторизации при неверных данных")
    def test_login_incorrect_credentials(self):
        with allure.step("Формируем данные с неверными значениями"):
            payload = {
                "login": "nonexistent",
                "password": "wrongpassword"
            }
        with allure.step("Отправляем запрос на авторизацию с неверными данными"):
            response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        with allure.step("Проверяем, что авторизация не проходит"):
            assert response.status_code != 200, "Ожидалась ошибка при попытке авторизации с неверными данными"