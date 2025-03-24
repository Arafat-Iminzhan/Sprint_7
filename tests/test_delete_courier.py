import allure
import requests
from const import Const, MessageText
from helpers import Helpers


class TestDeleteCourier:

    @allure.title('Проверка удаления курьера со всеми обязательными полями')
    def test_delete_courier(self):
        helpers = Helpers()

        with allure.step("Создание курьера"):
            data = helpers.register_new_courier_and_return_login_password()

        with allure.step("Авторизация курьера"):
            response_post = requests.post(Const.LOGIN_COURIER, data={
                "login": data[0],
                "password": data[1],
            })
            courier_id = response_post.json()['id']

        with allure.step("Удаление курьера по id"):
            response_delete = requests.delete(f'{Const.DELETE_COURIER}{courier_id}', data={'id': courier_id})

        with allure.step("Проверка успешного удаления"):
            assert response_delete.status_code == 200
            assert MessageText.DELETE_COURIER in response_delete.text

    @allure.title('Проверка удаления курьера без id курьера')
    def test_delete_courier_without_id(self):
        with allure.step("Попытка удалить курьера без ID"):
            response_delete = requests.delete(Const.DELETE_COURIER)

        with allure.step("Проверка ошибки при отсутствии ID"):
            assert response_delete.status_code == 404
            assert MessageText.DELETE_COURIER_WITHOUT_ID in response_delete.text
            # здесь баг, ответ не совпадает со свагером

    @allure.title('Проверка удаления курьера с несуществующим id курьера')
    def test_delete_courier_fake_id(self):
        helpers = Helpers()

        with allure.step("Создание и авторизация курьера"):
            data = helpers.register_new_courier_and_return_login_password()
            response_post = requests.post(Const.LOGIN_COURIER, data={
                "login": data[0],
                "password": data[1],
            })
            courier_id = response_post.json()['id']

        with allure.step("Попытка удалить несуществующего курьера"):
            response_delete = requests.delete(f'{Const.DELETE_COURIER}{courier_id}1', data={'id': courier_id})

        with allure.step("Проверка ошибки для несуществующего ID"):
            assert response_delete.status_code == 404
            assert MessageText.DELETE_COURIER_FAKE_ID in response_delete.text
