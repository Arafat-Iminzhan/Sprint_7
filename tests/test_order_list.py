import allure
import requests
from const import MessageText, Const


class TestGetOrderList:
    @allure.title('Проверка получения списка заказа')
    def test_get_order_list(self):
        response = requests.get(Const.ORDER_LIST)
        assert response.status_code == 200
        assert MessageText.LIST_ORDERS in response.text