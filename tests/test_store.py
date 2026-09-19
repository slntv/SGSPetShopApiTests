import jsonschema
import requests
import pytest
import allure
from tests.schemas.order_schema import ORDER_SCHEMA

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
    def test_get_order_by_id(self):
        pass

    @allure.title('Удаление заказа по ID')
    def test_delete_order_by_id(self):
        pass

    @allure.title('Попытка получить информацию о несуществующем заказе')
    def test_get_unexisting_order_by_id(self):
        pass

    @allure.title('Получение инвентаря магазина')
    def test_get_store_inventory(self):
        pass
