import allure
import requests
from const import MessageText, Const
from helpers import Helpers


class TestLoginCourier:

    @allure.title('Проверка авторизации курьера')
    def test_login_courier(self):
        helpers = Helpers()

        with allure.step("Регистрация курьера"):
            data = helpers.register_new_courier_and_return_login_password()

        with allure.step("Отправка запроса на авторизацию"):
            response = requests.post(Const.LOGIN_COURIER, data={
                "login": data[0],
                "password": data[1],
            })

        with allure.step("Проверка успешной авторизации"):
            assert response.status_code == 200
            assert MessageText.LOGING_COURIER in response.text

        with allure.step("Удаление тестового курьера"):
            helpers.delete_courier(data[0], data[1])

    @allure.title('Проверка авторизации курьера без логина')
    def test_login_courier_without_login(self):
        helpers = Helpers()

        with allure.step("Регистрация курьера"):
            data = helpers.register_new_courier_and_return_login_password()

        with allure.step("Попытка авторизации без логина"):
            response = requests.post(Const.LOGIN_COURIER, data={
                "login": data[0],
                "password": '',
            })

        with allure.step("Проверка ошибки"):
            assert response.status_code == 400
            assert MessageText.LOGING_COURIER_WITHOUT_DATA in response.text

    @allure.title('Проверка авторизации курьера без пароля')
    def test_login_courier_without_password(self):
        helpers = Helpers()

        with allure.step("Регистрация курьера"):
            data = helpers.register_new_courier_and_return_login_password()

        with allure.step("Попытка авторизации без пароля"):
            response = requests.post(Const.LOGIN_COURIER, data={
                "login": '',
                "password": data[1],
            })

        with allure.step("Проверка ошибки"):
            assert response.status_code == 400
            assert MessageText.LOGING_COURIER_WITHOUT_DATA in response.text

    @allure.title('Проверка авторизации курьера без логина и пароля')
    def test_login_courier_without_data(self):
        with allure.step("Отправка запроса без логина и пароля"):
            response = requests.post(Const.LOGIN_COURIER, data={
                "login": '',
                "password": '',
            })

        with allure.step("Проверка ошибки"):
            assert response.status_code == 400
            assert MessageText.LOGING_COURIER_WITHOUT_DATA in response.text

    @allure.title('Проверка авторизации с несуществующими данными')
    def test_login_courier_fake_data(self):
        with allure.step("Отправка запроса с фейковыми данными"):
            response = requests.post(Const.LOGIN_COURIER, data={
                "login": 'victor',
                "password": 'qwertyuiopasd',
            })

        with allure.step("Проверка ошибки"):
            assert response.status_code == 404
            assert MessageText.LOGING_COURIER_FAKE_DATA in response.text
