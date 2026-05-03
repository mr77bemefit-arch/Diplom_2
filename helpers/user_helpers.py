import random
import string
import requests
import allure

from data.data import (
    BASE_URL,
    CREATE_USER_ENDPOINT,
    LOGIN_USER_ENDPOINT,
    USER_ENDPOINT,
    ORDERS_ENDPOINT,
    INGREDIENTS_ENDPOINT
)


def generate_random_string(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


@allure.step("Сгенерировать данные уникального пользователя")
def generate_user_data():
    email = f"{generate_random_string(8)}@yandex.ru"
    password = generate_random_string(10)
    name = generate_random_string(8)
    return {
        "email": email,
        "password": password,
        "name": name
    }


@allure.step("Создать пользователя")
def create_user(user_data):
    return requests.post(
        f"{BASE_URL}{CREATE_USER_ENDPOINT}",
        json=user_data
    )


@allure.step("Авторизоваться пользователем с email: {email}")
def login_user(email, password):
    return requests.post(
        f"{BASE_URL}{LOGIN_USER_ENDPOINT}",
        json={
            "email": email,
            "password": password
        }
    )


@allure.step("Удалить пользователя")
def delete_user(access_token):
    headers = {
        "Authorization": access_token
    }
    return requests.delete(
        f"{BASE_URL}{USER_ENDPOINT}",
        headers=headers
    )


@allure.step("Получить список ингредиентов")
def get_ingredients():
    return requests.get(f"{BASE_URL}{INGREDIENTS_ENDPOINT}")


@allure.step("Создать заказ")
def create_order(ingredients, access_token=None):
    headers = {}
    if access_token:
        headers["Authorization"] = access_token

    return requests.post(
        f"{BASE_URL}{ORDERS_ENDPOINT}",
        json={"ingredients": ingredients},
        headers=headers
    )
