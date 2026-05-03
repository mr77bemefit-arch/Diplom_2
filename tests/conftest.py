import pytest
import allure

from helpers.user_helpers import generate_user_data, create_user, delete_user


@pytest.fixture
def user_data():
    with allure.step("Подготовить данные нового пользователя"):
        return generate_user_data()


@pytest.fixture
def created_user(user_data):
    with allure.step("Создать пользователя через API"):
        response = create_user(user_data)
        access_token = response.json().get("accessToken")

    yield user_data, response

    if access_token:
        with allure.step("Очистка после теста: удалить пользователя"):
            delete_user(access_token)