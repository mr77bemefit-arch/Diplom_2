import allure

from data.data import LOGIN_INCORRECT_MESSAGE
from helpers.user_helpers import login_user


@allure.suite("Логин пользователя")
class TestUserLogin:

    @allure.title("Вход под существующим пользователем")
    def test_login_existing_user_success(self, created_user):
        user_data, _ = created_user

        with allure.step("Отправить запрос на логин с корректными данными"):
            response = login_user(user_data["email"], user_data["password"])

        with allure.step("Проверить статус-код ответа"):
            assert response.status_code == 200

        with allure.step("Проверить успешный логин"):
            assert response.json()["success"] is True
            assert "accessToken" in response.json()
            assert "refreshToken" in response.json()

    @allure.title("Вход с неверным логином и паролем")
    def test_login_with_invalid_credentials_fail(self):
        with allure.step("Отправить запрос на логин с неверными данными"):
            response = login_user("wrong_email@yandex.ru", "wrong_password")

        with allure.step("Проверить статус-код ответа"):
            assert response.status_code == 401

        with allure.step("Проверить сообщение об ошибке"):
            assert response.json()["success"] is False
            assert response.json()["message"] == LOGIN_INCORRECT_MESSAGE