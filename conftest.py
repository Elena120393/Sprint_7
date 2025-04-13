import pytest
import requests
from config import BASE_URL
from utils.courier_utils import register_new_courier_and_return_login_password

# Фикстура для регистрации курьера с последующим удалением после теста
@pytest.fixture
def registered_courier():
    """
    Регистрирует курьера до выполнения теста и удаляет его после.
    Возвращает данные курьера: (login, password, first_name).
    """
    courier_data = register_new_courier_and_return_login_password()
    yield courier_data

    # Если курьер был успешно создан, осуществляем удаление
    if courier_data:
        login, password, _ = courier_data
        payload = {
            "login": login,
            "password": password
        }
        # Получаем ID курьера через авторизацию
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        if response.status_code == 200:
            response_json = response.json()
            if "id" in response_json:
                courier_id = response_json["id"]
                # Удаляем курьера по идентификатору
                requests.delete(f"{BASE_URL}/courier/{courier_id}")