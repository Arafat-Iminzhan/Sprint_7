import pytest
import requests
import allure
from const import Const
from data import DataForTest
from helpers import Helpers


@pytest.fixture(scope='function')
def create_order():
    with allure.step("Создание заказа через API"):
        response_create_order = requests.post(Const.CREATE_ORDER, json=DataForTest.person_data)
        track = response_create_order.json()['track']
        return track


@pytest.fixture(scope='function')
def create_courier():
    helpers = Helpers()

    with allure.step("Регистрация нового курьера"):
        data = helpers.register_new_courier_and_return_login_password()

    with allure.step("Авторизация курьера"):
        response_post = requests.post(Const.LOGIN_COURIER, data={
            "login": data[0],
            "password": data[1],
        })
        courier_id = response_post.json()['id']

    yield courier_id

    with allure.step("Удаление тестового курьера"):
        requests.delete(f'{Const.DELETE_COURIER}/{courier_id}')
