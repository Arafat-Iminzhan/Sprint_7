import allure
import requests
from const import MessageText, Const
from conftest import helpers


class TestLoginCourier:
    @allure.title('Проверка авторизации курьера')
    def test_login_courier(self, helpers):
        data = helpers.register_new_courier_and_return_login_password()
        response = requests.post(Const.LOGIN_COURIER, data={
            "login": data[0],
            "password": data[1],
        })
        assert response.status_code == 200
        assert MessageText.LOGING_COURIER in response.text
        helpers.delete_courier(data[0], data[1])


    @allure.title('Проверка авторизации курьера без логина')
    def test_login_courier_without_login(self, helpers):
        data = helpers.register_new_courier_and_return_login_password()
        response = requests.post(Const.LOGIN_COURIER, data={
            "login": data[0],
            "password": '',
        })
        assert response.status_code == 400
        assert MessageText.LOGING_COURIER_WITHOUT_DATA in response.text


    @allure.title('Проверка авторизации курьера без пароля')
    def test_login_courier_without_password(self, helpers):
        data = helpers.register_new_courier_and_return_login_password()
        response = requests.post(Const.LOGIN_COURIER, data={
            "login": '',
            "password": data[1],
        })
        assert response.status_code == 400
        assert MessageText.LOGING_COURIER_WITHOUT_DATA in response.text


    @allure.title('Проверка авторизации курьера без логина и пароля')
    def test_login_courier_without_data(self, helpers):
        response = requests.post(Const.LOGIN_COURIER, data={
            "login": '',
            "password": '',
        })
        assert response.status_code == 400
        assert MessageText.LOGING_COURIER_WITHOUT_DATA in response.text


    @allure.title('Проверка авторизации с несуществующими данными')
    def test_login_courier_fake_data(self):
        response = requests.post(Const.LOGIN_COURIER, data={
            "login": 'victor',
            "password": 'qwertyuiopasd',
        })
        assert response.status_code == 404
        assert MessageText.LOGING_COURIER_FAKE_DATA in response.text