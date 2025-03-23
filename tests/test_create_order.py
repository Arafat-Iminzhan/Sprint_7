import allure
import pytest
import requests
from const import MessageText, Const


class TestCreateOrder:
    person_data = [
        ['Naruto', 'Uchiha', 'Konoha, 192 apt.', '4', '+7 800 355 35 38', '5', '2020-06-06',
         'Saske, come back to Konoha', "BLACK"],
        ['Uchiha', 'Uchiha', 'Konoha, 150 apt.', '6', '+7 800 355 35 39', '6', '2020-06-06',
         'Saske, come back to Konoha', "GREY"],
        ['Naruto', 'Naruto', 'Konoha, 163 apt.', '7', '+7 800 355 35 10', '7', '2020-06-06',
         'Saske, come back to Konoha', "BLACK, GREY"],
        ['Uchiha', 'Naruto', 'Konoha, 177 apt.', '8', '+7 800 355 35 11', '8', '2020-06-06',
         'Saske, come back to Konoha', ""]
    ]


    @pytest.mark.parametrize(
        "firstName, lastName, address, metroStation, phone, rentTime, deliveryDate, comment, color", person_data)
    @allure.title('Создание заказа с цветом')
    def test_create_order_with_color(self, firstName, lastName, address, metroStation, phone, rentTime, deliveryDate,
                                     comment, color):
        data = {
            "firstName": firstName,
            "lastName": lastName,
            "address": address,
            "metroStation": metroStation,
            "phone": phone,
            "rentTime": rentTime,
            "deliveryDate": deliveryDate,
            "comment": comment,
            "color": [color],
        }
        response = requests.post(Const.CREATE_ORDER, json=data)
        assert response.status_code == 201
        assert MessageText.CREATE_ORDER in response.text