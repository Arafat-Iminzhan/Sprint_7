import allure
import requests
from const import MessageText, Const
from helpers import Helpers


class TestCreateCourier:

    @allure.title('Проверка создания курьера со всеми обязательными полями')
    def test_create_courier(self):
        helpers = Helpers()

        with allure.step("Генерация данных для курьера"):
            login, password, first_name = helpers.generate_data()
            payload = {
                "login": login,
                "password": password,
                "firstName": first_name
            }

        with allure.step("Отправка запроса на создание курьера"):
            response = requests.post(Const.CREATE_COURIER, data=payload)

        with allure.step("Проверка успешного создания"):
            assert response.status_code == 201
            assert MessageText.CREATE_COURIER in response.text

        with allure.step("Удаление тестового курьера"):
            helpers.delete_courier(login, password)

    @allure.title('Проверка невозможности создания двух одинаковых курьеров')
    def test_create_courier_twice(self):
        helpers = Helpers()

        with allure.step("Регистрация первого курьера"):
            data = helpers.register_new_courier_and_return_login_password()

        with allure.step("Повторная попытка регистрации"):
            response = requests.post(Const.CREATE_COURIER, data={
                "login": data[0],
                "password": data[1],
                "firstName": data[2]
            })

        with allure.step("Проверка ошибки о дублирующемся логине"):
            assert response.status_code == 409
            assert MessageText.CREATE_COURIER_TWICE in response.text

    @allure.title('Проверка создания курьера без логина')
    def test_create_courier_without_login(self):
        helpers = Helpers()

        with allure.step("Подготовка данных без логина"):
            login, password, first_name = helpers.generate_data()
            payload = {
                "password": password,
                "firstName": first_name
            }

        with allure.step("Отправка запроса"):
            response = requests.post(Const.CREATE_COURIER, data=payload)

        with allure.step("Проверка ошибки"):
            assert response.status_code == 400
            assert MessageText.CREATE_COURIER_WITHOUT_LOGIN in response.text

    @allure.title('Проверка создания курьера без пароля')
    def test_create_courier_without_password(self):
        helpers = Helpers()

        with allure.step("Подготовка данных без пароля"):
            login, password, first_name = helpers.generate_data()
            payload = {
                "login": login,
                "firstName": first_name
            }

        with allure.step("Отправка запроса"):
            response = requests.post(Const.CREATE_COURIER, data=payload)

        with allure.step("Проверка ошибки"):
            assert response.status_code == 400
            assert MessageText.CREATE_COURIER_WITHOUT_LOGIN in response.text

    @allure.title('Проверка создания курьера без имени')
    def test_create_courier_without_first_name(self):
        helpers = Helpers()

        with allure.step("Подготовка данных без имени"):
            login, password, first_name = helpers.generate_data()
            payload = {
                "login": login,
                "password": password,
            }

        with allure.step("Отправка запроса"):
            response = requests.post(Const.CREATE_COURIER, data=payload)

        with allure.step("Проверка успешного создания без имени"):
            assert response.status_code == 201
            assert MessageText.CREATE_COURIER in response.text

        with allure.step("Удаление курьера"):
            helpers.delete_courier(login, password)
