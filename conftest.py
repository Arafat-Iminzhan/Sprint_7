import pytest
import requests
from const import Const
from data import DataForTest
from helpers import Helpers


@pytest.fixture(scope='function')
def helpers():
    return Helpers()


@pytest.fixture(scope='function')
def create_order():
    response_create_order = requests.post(Const.CREATE_ORDER, json=DataForTest.person_data)
    track = response_create_order.json()['track']
    return track


@pytest.fixture(scope='function')
def create_courier(helpers):
    data = helpers.register_new_courier_and_return_login_password()
    response_post = requests.post(Const.LOGIN_COURIER, data={
        "login": data[0],
        "password": data[1],
    })
    courier_id = response_post.json()['id']
    yield courier_id
    requests.delete(f'{Const.DELETE_COURIER}/{courier_id}')