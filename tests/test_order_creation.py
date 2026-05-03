import allure

from data.data import ORDER_INGREDIENTS_REQUIRED_MESSAGE
from helpers.user_helpers import get_ingredients, create_order


@allure.suite("Создание заказа")
class TestOrders:

    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth_success(self, created_user):
        _, user_response = created_user
        access_token = user_response.json().get("accessToken")

        with allure.step("Получить список ингредиентов"):
            ingredients_response = get_ingredients()
            ingredients = ingredients_response.json()["data"]
            ingredient_ids = [ingredients[0]["_id"], ingredients[1]["_id"]]

        with allure.step("Отправить запрос на создание заказа с авторизацией"):
            response = create_order(ingredient_ids, access_token)

        with allure.step("Проверить статус-код ответа"):
            assert response.status_code == 200

        with allure.step("Проверить успешное создание заказа"):
            assert response.json()["success"] is True
            assert "name" in response.json()
            assert "order" in response.json()

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth_success(self):
        with allure.step("Получить список ингредиентов"):
            ingredients_response = get_ingredients()
            ingredients = ingredients_response.json()["data"]
            ingredient_ids = [ingredients[0]["_id"], ingredients[1]["_id"]]

        with allure.step("Отправить запрос на создание заказа без авторизации"):
            response = create_order(ingredient_ids)

        with allure.step("Проверить статус-код ответа"):
            assert response.status_code == 200

        with allure.step("Проверить успешное создание заказа"):
            assert response.json()["success"] is True
            assert "name" in response.json()
            assert "order" in response.json()

    @allure.title("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients_success(self):
        with allure.step("Получить список ингредиентов"):
            ingredients_response = get_ingredients()
            ingredients = ingredients_response.json()["data"]
            ingredient_ids = [ingredients[0]["_id"], ingredients[1]["_id"]]

        with allure.step("Отправить запрос на создание заказа с ингредиентами"):
            response = create_order(ingredient_ids)

        with allure.step("Проверить статус-код ответа"):
            assert response.status_code == 200

        with allure.step("Проверить успешное создание заказа"):
            assert response.json()["success"] is True

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients_fail(self):
        with allure.step("Отправить запрос на создание заказа без ингредиентов"):
            response = create_order([])

        with allure.step("Проверить статус-код ответа"):
            assert response.status_code == 400

        with allure.step("Проверить сообщение об ошибке"):
            assert response.json()["success"] is False
            assert response.json()["message"] == ORDER_INGREDIENTS_REQUIRED_MESSAGE

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash_fail(self):
        with allure.step("Отправить запрос на создание заказа с невалидным хешем ингредиента"):
            response = create_order(["invalid_hash_123"])

        with allure.step("Проверить статус-код ответа"):
            assert response.status_code == 500