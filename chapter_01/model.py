from datetime import date, timedelta

from exc import (
    SKUDoesntMatchError,
    NotEnoughQuantityError,
    AvailableEqualToRequiredError,
    PrefersWarehouseToShipmentError, PrefersEarlierBatchesError
)


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: date):
        """
        Класс batch представляет партию товара
        :param ref: reference - артикул товара
        :param sku: stock keeping unit - наименование товара
        :param qty: quantity - количество заказа
        :param eta: expected time of arrival - время прибытия
        """
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self.available_quantity = qty

    def allocate(self, line: "OrderLine"):
        """ Проверяет условия заказа """
        if line.sku != self.sku:
            raise SKUDoesntMatchError
        elif line.qty > self.available_quantity:
            raise NotEnoughQuantityError
        elif line.qty == self.available_quantity:
            raise AvailableEqualToRequiredError
        elif self.eta > date.today():
            if self.eta >= date.today() + timedelta(days=10):
                raise PrefersEarlierBatchesError
            raise PrefersWarehouseToShipmentError

        self.available_quantity -= line.qty


class OrderLine:
    def __init__(self, orderid, sku, qty):
        self.orderid = orderid
        self.sku = sku
        self.qty = qty
