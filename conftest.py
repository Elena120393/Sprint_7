
import pytest

@pytest.fixture(scope="session")
def base_url():
    """
    Фикстура возвращает базовый URL для API Яндекс Самокат.
    """
    return "https://qa-scooter.praktikum-services.ru/api/v1"
