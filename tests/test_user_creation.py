import pytest
import allure
import requests

from data.data import (
    BASE_URL,
    CREATE_USER_ENDPOINT,
    USER_EXISTS_MESSAGE,
    USER_REQUIRED_FIELDS_MESSAGE
)
from helpers.user_helpers import create_user, delete_user


@allure.suite("Создание пользователя")
class TestUserCreation:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user_success(self, user_data):
        with allure.step("Отправить запрос на создание нового пользователя"):
            response = create_user(user_data)

        with allure.step("Проверить статус-код ответа"):
            assert response.status_code == 200

        with allure.step("Проверить успешность создания пользователя"):
            assert response.json()["success"] is True
            assert "accessToken" in response.json()
            assert "refreshToken" in response.json()

        with allure.step("Удалить созданного пользователя"):
            access_token = response.json().get("accessToken")
            if access_token:
                delete_user(access_token)

    @allure.title("Создание уже зарегистрированного пользователя")
    def test_create_existing_user_fail(self, created_user):
        user_data, _ = created_user

        with allure.step("Повторно отправить запрос на создание того же пользователя"):
            response = create_user(user_data)

        with allure.step("Проверить статус-код ответа"):
            assert response.status_code == 403

        with allure.step("Проверить текст ошибки"):
            assert response.json()["success"] is False
            assert response.json()["message"] == USER_EXISTS_MESSAGE

    @allure.title("Создание пользователя без одного обязательного поля")
    @pytest.mark.parametrize("field", ["email", "password", "name"])
    def test_create_user_without_required_field_fail(self, user_data, field):
        with allure.step(f"Удалить обязательное поле '{field}' из тела запроса"):
            invalid_user = user_data.copy()
            invalid_user.pop(field)

        with allure.step("Отправить запрос на создание пользователя с неполными данными"):
            response = requests.post(
                f"{BASE_URL}{CREATE_USER_ENDPOINT}",
                json=invalid_user
            )

        with allure.step("Проверить статус-код ответа"):
            assert response.status_code == 403

        with allure.step("Проверить сообщение об ошибке"):
            assert response.json()["success"] is False
            assert response.json()["message"] == USER_REQUIRED_FIELDS_MESSAGE