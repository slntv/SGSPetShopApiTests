import jsonschema
import requests
import allure
from tests.schemas.order_schema import ORDER_SCHEMA
from tests.schemas.inventory_schema import INVENTORY_SCHEMA

BASE_URL = 'http://5.181.109.28:9090/api/v3'


@allure.feature('Store')
class TestStore:

    @allure.title('Размещение заказа')
    def test_place_order(self):
        with allure.step('Отправка запроса на размещение заказа'):
            payload = {"id": 1,
                       "petId": 1,
                       "quantity": 1,
                       "status": "placed",
                       "complete": True}
            response = requests.post(url=f'{BASE_URL}/store/order', json=payload)
            response_json = response.json()

        with allure.step('Проверка статуса ответа и данных заказа'):
            assert response.status_code == 200, 'Код ошибки не совпал с ожидаемым'
            jsonschema.validate(response_json, ORDER_SCHEMA)
            assert response_json['id'] == payload['id'], 'id не совпадает с ожидаемым'
            assert response_json['petId'] == payload['petId'], 'petId не совпадает с ожидаемым'
            assert response_json['quantity'] == payload['quantity'], 'quantity не совпадает с ожидаемым'
            assert response_json['status'] == payload['status'], 'status не совпадает с ожидаемым'
            assert response_json['complete'] == payload['complete'], 'complete не совпадает с ожидаемым'

    @allure.title('Получение информации о заказе по ID')
    def test_get_order_by_id(self, create_order):
        with allure.step('Отправка запроса на получение информации по ID'):
            order_id = create_order["id"]
            response = requests.get(url=f'{BASE_URL}/store/order/{order_id}')
            response_json = response.json()

        with allure.step('Проверка статуса ответа и данных заказа'):
            assert response.status_code == 200, 'Код ошибки не совпал с ожидаемым'
            assert response.json()["id"] == order_id
            jsonschema.validate(response_json, ORDER_SCHEMA)

    @allure.title('Удаление заказа по ID')
    def test_delete_order_by_id(self, create_order):
        with allure.step('Отправка запроса удаление по ID'):
            order_id = create_order["id"]
            response = requests.delete(url=f'{BASE_URL}/store/order/{order_id}')

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200

        with allure.step('Отправка запроса на получение информации о заказе'):
            response = requests.get(url=f'{BASE_URL}/store/order/{order_id}')

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404

    @allure.title('Попытка получить информацию о несуществующем заказе')
    def test_get_unexisting_order_by_id(self):
        with allure.step('Отправка запроса на получение информации по ID'):
            response = requests.get(url=f'{BASE_URL}/store/order/{9999}')

        with allure.step('Проверка статуса ответа и данных заказа'):
            assert response.status_code == 404, 'Код ошибки не совпал с ожидаемым'

    @allure.title('Получение инвентаря магазина')
    def test_get_store_inventory(self):
        with allure.step('Отправка запроса на получение инвентаря магазина'):
            response = requests.get(url=f'{BASE_URL}/store/inventory')

        with allure.step('Проверка статуса ответа и данных заказа'):
            assert response.status_code == 200, f'Ожидаемый статус 200, получен {response.status_code}'
            response_json = response.json()
            jsonschema.validate(instance=response_json, schema=INVENTORY_SCHEMA)
            assert isinstance(response_json['approved'], int)
            assert isinstance(response_json['placed'], int)
            assert isinstance(response_json['delivered'], int)
