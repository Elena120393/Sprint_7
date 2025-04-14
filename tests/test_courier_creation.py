
import requests
import pytest
import allure
from config import BASE_URL
from utils.courier_utils import register_new_courier_and_return_login_password

@allure.feature("Создание курьера")
class TestCourierCreation:
    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, registered_courier):
        with allure.step("Проверяем, что курьер создан"):
            assert registered_courier, "Курьер не создан. Функция вернула пустой список."

    @allure.title("Проверка ошибки при создании дубликата курьера")
    def test_duplicate_courier(self, registered_courier):
        with allure.step("Извлекаем данные курьера из предварительной регистрации"):
            assert registered_courier, "Первый курьер не создан"
            login, password, first_name = registered_courier
            payload = {
                "login": login,
                "password": password,
                "firstName": first_name
            }
        with allure.step("Пытаемся создать курьера с такими же данными"):
            response = requests.post(f"{BASE_URL}/courier", data=payload)
        with allure.step("Проверяем, что регистрация дубликата не прошла"):
            assert response.status_code != 201, "Ожидалась ошибка при создании курьера с дублирующими данными"

    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    @allure.title("Регистрация курьера с отсутствующим полем")
    def test_create_courier_missing_field(self, missing_field):
        with allure.step("Генерируем уникальные данные для курьера"):
            def generate_dummy_string():
                import random, string
                return ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
            payload = {
                "login": generate_dummy_string(),
                "password": generate_dummy_string(),
                "firstName": generate_dummy_string()
            }
        with allure.step(f"Удаляем поле: {missing_field}"):
            payload.pop(missing_field)
        with allure.step("Отправляем запрос на регистрацию"):
            response = requests.post(f"{BASE_URL}/courier", data=payload)
        if missing_field == "firstName":
            with allure.step("Проверяем, что регистрация проходит успешно, так как поле не обязательное"):
                assert response.status_code == 201, f"Ожидался успешный результат при отсутствии поля {missing_field}"
        else:
            with allure.step("Проверяем, что регистрация завершается ошибкой при отсутствии обязательного поля"):
                assert response.status_code != 201, f"Ожидалась ошибка при отсутствии поля {missing_field}"