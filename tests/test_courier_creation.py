import requests
import pytest
from utils.courier_utils import register_new_courier_and_return_login_password

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"


class TestCourierCreation:
    def test_create_courier_success(self):
        """
        Тест проверяет, что курьер создаётся успешно.
        """
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data, "Курьер не создан. Функция вернула пустой список."

    def test_duplicate_courier(self):
        """
        Тест проверяет, что создание дубликата курьера (с одинаковыми данными) приводит к ошибке.
        """
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data, "Первый курьер не создан"
        login, password, first_name = courier_data

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        # Пытаемся создать курьера с теми же данными ещё раз
        response = requests.post(f"{BASE_URL}/courier", data=payload)
        # Ожидаем, что повторная регистрация не будет успешной (код не равен 201)
        assert response.status_code != 201, "Ожидалась ошибка при создании курьера с дублирующими данными"

    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    def test_create_courier_missing_field(self, missing_field):
        """
        Тест проверяет, что при отсутствии обязательного поля регистрация курьера завершается с ошибкой
        для полей 'login' и 'password'.
        """

        # Генерация уникальных данных вручную
        def generate_dummy_string():
            import random, string
            return ''.join(random.choice(string.ascii_lowercase) for _ in range(10))

        payload = {
            "login": generate_dummy_string(),
            "password": generate_dummy_string(),
            "firstName": generate_dummy_string()
        }
        # Удаляем одно из обязательных полей
        payload.pop(missing_field)
        response = requests.post(f"{BASE_URL}/courier", data=payload)

        if missing_field == "firstName":
            # Если отсутствует поле firstName, регистрация проходит успешно (201), так как оно не является обязательным.
            assert response.status_code == 201, f"Ожидался успешный результат при отсутствии поля {missing_field}"
        else:
            # Для остальных обязательных полей ожидается ошибка (код не равен 201)
            assert response.status_code != 201, f"Ожидалась ошибка при отсутствии поля {missing_field}"